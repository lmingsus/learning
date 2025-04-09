from langchain_openai import AzureChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from datetime import datetime
from typing import List, Dict
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser



from configparser import ConfigParser
try:
    config = ConfigParser()
    config.read('config.ini', encoding='utf-8')
    # Azure AI Foundry 部屬端點目標URI：
    # {AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT_NAME}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}
    
    # Azure OpenAI Model
    # gpt-35-turbo
    AZURE_OPENAI_API_KEY = config.get('Azure', 'OPENAI_KEY')
    AZURE_OPENAI_API_VERSION = config.get('Azure', 'GPT35_TURBO_API_VERSION')
    AZURE_OPENAI_ENDPOINT = config.get('Azure', 'OPENAI_ENDPOINT')
    AZURE_OPENAI_DEPLOYMENT_NAME = config.get('Azure', 'GPT35_TURBO_DEPLOYMENT_NAME')

    # gpt-4o-mini
    AZURE_OPENAI_API_VERSION = config.get('Azure', 'OPENAI_API_VERSION')
    AZURE_OPENAI_DEPLOYMENT_NAME = config.get('Azure', 'OPENAI_DEPLOYMENT_NAME')

    if not all([AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT_NAME]):
        raise ValueError("請在 config.ini 中設定所有必要的 Azure OpenAI 參數")
except Exception as e:
    print(f"Error: {str(e)}")
    print("Please provide a valid API key and endpoint")


# 定義模型
llm = AzureChatOpenAI(azure_endpoint=AZURE_OPENAI_ENDPOINT,
                        azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME,
                        openai_api_version=AZURE_OPENAI_API_VERSION,
                        api_key=AZURE_OPENAI_API_KEY,
                        temperature=0.2,
                        )



# 模擬房間的可用資料，通常來自外部串接系統
rooms_availability: List[Dict] =  [
    {"room_no":"001","room_type":"雙人房","available_date":"2025-03-31"},
    {"room_no":"001","room_type":"雙人房","available_date":"2025-04-02"},
    {"room_no":"001","room_type":"雙人房","available_date":"2025-04-06"},

    {"room_no":"002","room_type":"單人房","available_date":"2025-03-31"},
    {"room_no":"002","room_type":"單人房","available_date":"2025-04-01"},
    {"room_no":"002","room_type":"單人房","available_date":"2025-04-04"},
    {"room_no":"002","room_type":"單人房","available_date":"2025-04-06"},

    {"room_no":"003","room_type":"雙人房","available_date":"2025-03-30"},
    {"room_no":"003","room_type":"雙人房","available_date":"2025-03-31"},
    {"room_no":"003","room_type":"雙人房","available_date":"2025-04-01"},
    {"room_no":"003","room_type":"雙人房","available_date":"2025-04-02"},
    {"room_no":"003","room_type":"雙人房","available_date":"2025-04-03"},
    {"room_no":"003","room_type":"雙人房","available_date":"2025-04-04"},
    {"room_no":"003","room_type":"雙人房","available_date":"2025-04-05"},
]


# 取得當前日期
@tool
def get_current_date() -> str:
    """
    取得今天日期。

    Returns:
        str: 今天日期，格式為 YYYY-MM-DD
    """
    return datetime.now().strftime("%Y-%m-%d")


# 客戶評價
@tool
def get_customer_service_chain(input: str) -> str:
    """
    回應客戶評論。

    Args:
        input (str): 客戶提交的評論

    Returns:
        str: 根據客戶評論的情感回應
    """
    system_prompt ="""
    請分析客戶評論的情感是正面(positive)還是負面(negative)。
    
    ### 請注意：
    當客戶提供了正面評論時，請以感謝的態度回應這個評論。
    當客戶提供了負面評論時，請以安撫和道歉的態度回應這個評論。
    """
    prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])

    response_chain = prompt | llm | StrOutputParser()
    return response_chain.invoke(input=input)


# 查詢指定日期的可用房間
@tool
def check_room_availability(date: str) -> str:
    """
    查詢指定日期的可用房間。

    Args:
        date (str): 查詢日期，格式為 YYYY-MM-DD

    Returns:
        str: 可用房間的資訊，如果沒有可用房間則返回無可預訂空房的訊息
    """
    try:
        # 驗證日期格式
        query_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return "日期格式不正確，請使用 YYYY-MM-DD 格式。"

    available_rooms = [
            room for room in rooms_availability 
            if datetime.strptime(room["available_date"], "%Y-%m-%d").date() == query_date.date()
        ]

    if not available_rooms:
        return f"抱歉，{date} 沒有可預訂的房間。"

    result = f"{date} 可預訂的房間如下：\n"
    for room in available_rooms:
        result += f"房間號碼：{room['room_no']}，類型：{room['room_type']}\n"

    return result


# 輸出 LLM 回應過程
def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print("----- 這是 tuple 開始 -----")
            print(message)
            print("----- 這是 tuple 結束 -----")
        else:
            print("----- 這是 pretty_print 開始 -----")
            message.pretty_print()
            print("----- 這是 pretty_print 結束 -----")



def main():
    # 設定工具
    tools = [get_current_date, check_room_availability, get_customer_service_chain]

    # 設定 prompt
    agent_prompt = "你是彰化員林市蘭芊大酒店的訂房機器人，請你作為一位資深的飯店客服主管，幫客人查詢空房資訊及預約住宿。"
    agent_prompt += "回覆時請同時回應正體中文以及日文二個語言資料。"

    # 建立 Agent
    graph = create_react_agent(llm, tools, checkpointer=MemorySaver(), state_modifier=agent_prompt)

    # Agent 啟動
    config = {"configurable": {'thread_id': "135"}}

    inputs = {"messages": [("user", "我從台北市前往，現在中壢，我想預約今晚的住宿，有空房嗎？")]}
    print_stream(graph.stream(inputs, config=config, stream_mode="values"))

    inputs = {"messages": [("user", "現在我到豐原了，我想在這裡住一晚，明天再到你那邊。")]}
    print_stream(graph.stream(inputs, config=config, stream_mode="values"))

    inputs = {"messages": [("user", "我決定就預約你建議的房間，謝謝你貼心的服務。")]}
    print_stream(graph.stream(inputs, config=config, stream_mode="values"))


if __name__ == "__main__":
    main()


# 使用 'model_name': 'gpt-3.5-turbo-0125'
'''   
----- 這是 pretty_print 開始 -----
================================ Human Message =================================

我從台北市前往，現在中壢，我想預約今晚的住宿，有空房嗎？
----- 這是 pretty_print 結束 -----
----- 這是 pretty_print 開始 -----
================================== Ai Message ==================================
Tool Calls:
  get_current_date (call_XCI3tUu29VxDv6CFEOMHkW1u)
 Call ID: call_XCI3tUu29VxDv6CFEOMHkW1u
  Args:
----- 這是 pretty_print 結束 -----
----- 這是 pretty_print 開始 -----
================================= Tool Message =================================
Name: get_current_date

2025-04-03
----- 這是 pretty_print 結束 -----
----- 這是 pretty_print 開始 -----
================================== Ai Message ==================================
Tool Calls:
  check_room_availability (call_ECWrmal9aoTQnyRJUWCRDf9o)
 Call ID: call_ECWrmal9aoTQnyRJUWCRDf9o
  Args:
    date: 2025-04-03
  check_room_availability (call_dNiingfUnvjLi2bKOmCI4ndm)
 Call ID: call_dNiingfUnvjLi2bKOmCI4ndm
  Args:
    date: 2025-04-04
----- 這是 pretty_print 結束 -----
----- 這是 pretty_print 開始 -----
================================= Tool Message =================================
Name: check_room_availability

2025-04-04 可預訂的房間如下：
房間號碼：002，類型：單人房
房間號碼：003，類型：雙人房

----- 這是 pretty_print 結束 -----
----- 這是 pretty_print 開始 -----
================================== Ai Message ==================================

根據您的需求，以下是今晚和明晚可預訂的房間資訊：

- 今晚（2025年4月3日）可預訂的房間如下：
  - 房間號碼：003
  - 類型：雙人房

- 明晚（2025年4月4日）可預訂的房間如下：
  - 房間號碼：002
  - 類型：單人房
  - 房間號碼：003
  - 類型：雙人房

請問您要預訂哪一天的房間呢？如果需要進一步協助或有其他問題，請隨時告訴我。ありがとうございます。
----- 這是 pretty_print 結束 -----
----- 這是 pretty_print 開始 -----
================================ Human Message =================================

現在我到豐原了，我想在這裡住一晚，明天再到你那邊。請問這裡的天氣怎麼樣？
----- 這是 pretty_print 結束 -----
----- 這是 pretty_print 開始 -----
================================== Ai Message ==================================
Tool Calls:
  get_customer_service_chain (call_reD9B9KfTNKsUfMTuIPgZTLl)
 Call ID: call_reD9B9KfTNKsUfMTuIPgZTLl
  Args:
    input: 請問這裡的天氣怎麼樣？
----- 這是 pretty_print 結束 -----
----- 這是 pretty_print 開始 -----
================================= Tool Message =================================
Name: get_customer_service_chain

感謝您的詢問！我們這裡的天氣非常好，陽光明媚，溫度也很舒適。希望您能享受美好的天氣！如果您有任何其他問題，歡迎隨時向我們詢問。
----- 這是 pretty_print 結束 -----
----- 這是 pretty_print 開始 -----
================================== Ai Message ==================================

感謝您的詢問！我們這裡的天氣非常好，陽光明媚，溫度也很舒適。希望您能享受美好的天氣！如果您有任何其他問題，歡迎隨時向我們詢問。ありがとうございます。
----- 這是 pretty_print 結束 -----
----- 這是 pretty_print 開始 -----
================================ Human Message =================================

我決定就預約你建議的房間，謝謝你貼心的服務。
----- 這是 pretty_print 結束 -----
----- 這是 pretty_print 開始 -----
================================== Ai Message ==================================

非常感謝您的預約！我們很高興能為您提供貼心的服務。如果您需要任何幫助或有其他需求，請隨時告訴我們。期待您的光臨，祝您有個愉快的住宿體驗！ありがとうございます。
'''


# 使用 'model_name': 'gpt-4o-mini'
'''
----- 這是 pretty_print 開始 -----
================================ Human Message =================================

我從台北市前往，現在中壢，我想預約今晚的住宿，有空房嗎？
----- 這是 pretty_print 結束 -----
----- 這是 pretty_print 開始 -----
================================== Ai Message ==================================
Tool Calls:
  get_current_date (call_Kse7rOjlIs9uqhveMBXbbUoJ)
 Call ID: call_Kse7rOjlIs9uqhveMBXbbUoJ
  Args:
----- 這是 pretty_print 結束 -----
----- 這是 pretty_print 開始 -----
================================= Tool Message =================================
Name: get_current_date

2025-04-03
----- 這是 pretty_print 結束 -----
----- 這是 pretty_print 開始 -----
================================== Ai Message ==================================
Tool Calls:
  check_room_availability (call_QdkyY29RjNe1ueARKL5gzVq5)
 Call ID: call_QdkyY29RjNe1ueARKL5gzVq5
  Args:
    date: 2025-04-03
----- 這是 pretty_print 結束 -----
----- 這是 pretty_print 開始 -----
================================= Tool Message =================================
Name: check_room_availability

2025-04-03 可預訂的房間如下：
房間號碼：003，類型：雙人房

----- 這是 pretty_print 結束 -----
----- 這是 pretty_print 開始 -----
================================== Ai Message ==================================

今晚（2025年4月3日）我們有可預訂的房間，房間號碼為003，類型為雙人房。請問您需要我為您進行預約嗎？

今晩（2025年4月3日）、予約可能な部屋があります。部屋番号は003、タイプはダブルルームです。ご予約を希望されますか？
----- 這是 pretty_print 結束 -----
----- 這是 pretty_print 開始 -----
================================ Human Message =================================

現在我到豐原了，我想在這裡住一晚，明天再到你那邊。
----- 這是 pretty_print 結束 -----
----- 這是 pretty_print 開始 -----
================================== Ai Message ==================================
Tool Calls:
  get_current_date (call_N0uQFT8oCyP475yNZwNC2g7u)
 Call ID: call_N0uQFT8oCyP475yNZwNC2g7u
  Args:
----- 這是 pretty_print 結束 -----
----- 這是 pretty_print 開始 -----
================================= Tool Message =================================
Name: get_current_date

2025-04-03
----- 這是 pretty_print 結束 -----
----- 這是 pretty_print 開始 -----
================================== Ai Message ==================================
Tool Calls:
  check_room_availability (call_vIW7lBMiluaWs89LQT0QDdsy)
 Call ID: call_vIW7lBMiluaWs89LQT0QDdsy
  Args:
    date: 2025-04-04
----- 這是 pretty_print 結束 -----
----- 這是 pretty_print 開始 -----
================================= Tool Message =================================
Name: check_room_availability

2025-04-04 可預訂的房間如下：
房間號碼：002，類型：單人房
房間號碼：003，類型：雙人房

----- 這是 pretty_print 結束 -----
----- 這是 pretty_print 開始 -----
================================== Ai Message ==================================

明天（2025年4月4日）我們有可預訂的房間，以下是可用的房間資訊：
- 房間號碼：002，類型：單人房
- 房間號碼：003，類型：雙人房

請問您需要我為您進行預約嗎？

明日（2025年4月4日）、予約可能な部屋があります。以下は利用可能な部屋の情報です：
- 部屋番号：002、タイプはシングルルーム
- 部屋番号：003、タイプはダブルルーム

ご予約を希望されますか？
----- 這是 pretty_print 結束 -----
----- 這是 pretty_print 開始 -----
================================ Human Message =================================

我決定就預約你建議的房間，謝謝你貼心的服務。
----- 這是 pretty_print 結束 -----
----- 這是 pretty_print 開始 -----
================================== Ai Message ==================================

感謝您的選擇！我將為您預約房間號碼003，類型為雙人房。請您提供以下資訊以完成預約：
1. 姓名
2. 聯絡電話
3. 入住時間

謝謝您的支持，我們期待您的光臨！

ご選択いただきありがとうございます！部屋番号003、タイプはダブルルームを予約いたします。予約を完了するために、以下の情報を提供してください：
1. お名前
2. 連絡先電話番号
3. チェックイン時間

ご支援いただきありがとうございます。お越しをお待ちしております！
----- 這是 pretty_print 結束 -----
'''