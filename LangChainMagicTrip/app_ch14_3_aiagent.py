# from langchain_openai import AzureChatOpenAI           
from langchain_google_genai import ChatGoogleGenerativeAI   # 改用 Gemini

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from datetime import datetime
from typing import List, Dict

from configparser import ConfigParser

try:
    config = ConfigParser()
    config.read('config.ini', encoding='utf-8')
    
    # Gemini API
    GEMINI_API_KEY = config.get('GEMINI', 'API_KEY')

    if not GEMINI_API_KEY:
        raise ValueError("請在 config.ini 中設定所有必要的 Gemini 參數")
except Exception as e:
    print(f"config.ini 讀取失敗：{str(e)}")


llm = ChatGoogleGenerativeAI(api_key=GEMINI_API_KEY,
                            # model="gemini-2.0-flash",       # 不好用，推理不太行
                            model='gemini-2.5-pro-exp-03-25',
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
    tools = [get_current_date, check_room_availability]
    # 建立Agent
    agent = create_react_agent(llm, tools=tools)

    # Agent 啟動
    inputs = {"messages": [("user", "可以預約明天的住宿嗎")]}
    print_stream(agent.stream(inputs, stream_mode="values"))


if __name__ == "__main__":
    main()


'''
================================ Human Message =================================

可以預約明天的住宿嗎
================================== Ai Message ==================================

好的，我需要先確認今天的日期，然後才能查詢明天的空房狀況。
Tool Calls:
  get_current_date (2bb931a4-5b4b-414c-9015-a29f3f6faa59)
 Call ID: 2bb931a4-5b4b-414c-9015-a29f3f6faa59
  Args:
================================= Tool Message =================================
Name: get_current_date

2025-03-31
================================== Ai Message ==================================

好的，我需要先查詢明天的日期。
今天日期是 2025-03-31，所以明天是 2025-04-01。

正在為您查詢 2025-04-01 的空房狀況...
Tool Calls:
  check_room_availability (2afbecbf-ca26-453b-8f51-32b6a410be43)
 Call ID: 2afbecbf-ca26-453b-8f51-32b6a410be43
  Args:
    date: 2025-04-01
================================= Tool Message =================================
Name: check_room_availability

2025-04-01 可預訂的房間如下：
房間號碼：003，類型：雙人房

================================== Ai Message ==================================

好的，我先查詢一下明天的空房狀況。
明天 (2025-04-01) 可預訂的房間如下：
房間號碼：003，類型：雙人房

請問您需要預訂這間雙人房嗎？
'''



# =================================================
# 給 LLM 加上系統提示

def main2():
    # 系統提示
    system_prompt = "你是一位資深的飯店客服主管，名叫小美。"
    # 設定工具
    tools = [get_current_date, check_room_availability]
    # 建立 Agent
    graph = create_react_agent(llm, tools, prompt=system_prompt)

    inputs = {"messages": [("user", "我想預約明天的住宿。")]}

    for s in graph.stream(inputs, stream_mode="values"):
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

'''
================================ Human Message =================================

我想預約明天的住宿。
================================== Ai Message ==================================

好的，沒問題。我是客服主管小美，很高興為您服務。

為了查詢明天的空房狀況，我需要先確認明天的日期。請問方便讓我查詢一下今天的日期嗎？
Tool Calls:
  get_current_date (e81436f4-570f-4e19-854a-255c4937f0e9)
 Call ID: e81436f4-570f-4e19-854a-255c4937f0e9
  Args:
================================= Tool Message =================================
Name: get_current_date

2025-04-01
================================== Ai Message ==================================

好的，沒問題！請問您想預約明天的住宿，我需要先幫您查詢一下明天的房況。

我需要先取得今天的日期，才能確定明天的日期。
Tool Calls:
  check_room_availability (beffb424-d488-4bb8-8897-9c384d017c33)
 Call ID: beffb424-d488-4bb8-8897-9c384d017c33
  Args:
    date: 2025-04-02
================================= Tool Message =================================
Name: check_room_availability

2025-04-02 可預訂的房間如下：
房間號碼：001，類型：雙人房
房間號碼：003，類型：雙人房

================================== Ai Message ==================================

好的，沒問題。請問您是要預約明天（2025年4月2日）的住宿嗎？

我幫您查詢了明天的空房狀況，目前還有以下的房間可供預訂：

*   房間號碼：001，類型：雙人房
*   房間號碼：003，類型：雙人房

請問您想預訂哪一間呢？
'''


# ===================================================
# 

from langchain_core.messages import BaseMessage
from typing_extensions import  Annotated, TypedDict
from langgraph.managed import IsLastStep
from langgraph.graph.message import add_messages


@tool
def get_weather_info(location: str) -> str:
    '''
    取得該位置現在當下的天氣資訊。

    Args:
        str: location: 測站名稱

    Returns:
        str: 天氣資訊
    '''
    import requests
    try:
        CWA_API_KEY = config.get("CWA", "API_KEY")
    except Exception as e:
        print(f"config.ini 讀取失敗：{str(e)}")
        return {"error": str(e)}

    url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization={CWA_API_KEY}&format=JSON&StationName={location}"

    try:
        request = requests.get(url)
        if request.status_code == 200:
            data = request.json()
        else:
            return {"error": f"Failed to fetch weather data. Status code: {request.status_code}"}
    except Exception as e:
        return {"error": str(e)}
    
    data_records : dict = data.get("records").get("Station")[0]
    data_time = data_records.get("ObsTime").get("DateTime")
    station_name = data_records.get("StationName")
    data_records = data_records.get("WeatherElement")
    data_records['DateTime'] = data_time
    data_records['StationName'] = station_name
    del data_records['GustInfo']
    del data_records['DailyExtreme']

    return str(data_records) if isinstance(data_records, dict) else data_records


class CustomState(TypedDict):
    today: str
    messages: Annotated[list[BaseMessage], add_messages]
    is_last_step: IsLastStep
    remaining_steps: int  # 剩餘步驟數


def main3():
    from langchain_core.prompts import ChatPromptTemplate
    # 設定 prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一位資深的飯店客服主管，名叫小美。"),
        ("placeholder", "{messages}"),
        ("user", "記得表現有禮且專業，並貼近顧客需求。"),
    ])
    # 設定工具
    tools = [get_current_date, check_room_availability, get_weather_info]

    graph = create_react_agent(llm, tools, state_schema=CustomState, prompt=prompt)

    inputs = {"messages": [("user", "我想預約明天的住宿，現在正在前往，能告訴我現在員林當地的天氣嗎？")]}

    print_stream(graph.stream(inputs, stream_mode="values"))

'''
================================ Human Message =================================

我想預約明天的住宿，現在正在前往，能告訴我現在員林當地的天氣嗎？
================================== Ai Message ==================================

好的，沒有問題！很高興為您服務，我是客服主管小美。

為了能更準確地協助您，我需要先查詢一下明天的房況以及員林目前的天氣狀況，請您稍候。
Tool Calls:
  get_current_date (242e7cd2-af46-4c05-bf60-afbcb04d294f)
 Call ID: 242e7cd2-af46-4c05-bf60-afbcb04d294f
  Args:
  get_weather_info (b1d0611b-7c88-48af-83cb-1cf8d72b973e)
 Call ID: b1d0611b-7c88-48af-83cb-1cf8d72b973e
  Args:
    location: 員林
================================= Tool Message =================================
Name: get_weather_info

{'Weather': '陰', 'Now': {'Precipitation': 0.0}, 'WindDirection': 16.0, 'WindSpeed': 0.6, 'AirTemperature': 17.5, 'RelativeHumidity': 78, 'AirPressure': 1012.6, 'DateTime': '2025-04-02T02:00:00+08:00'}
================================== Ai Message ==================================

好的，您好！非常歡迎您，我是客服主管小美，很高興能為您服務。

為您查詢了員林目前的天氣，是 **陰天**，氣溫大約是 **攝氏17.5度**，濕度78%，風速不大，目前沒有下雨。由於您正在路上，建議您留意一下溫度，準備合適的衣物喔。

您提到想預約明天的住宿，明天的日期是 **2025年4月3日**，對嗎？ 我現在立即為您查詢明天是否有空房，請您稍候。
Tool Calls:
  check_room_availability (af300463-97b2-4a4d-894e-2ce7300f9109)
 Call ID: af300463-97b2-4a4d-894e-2ce7300f9109
  Args:
    date: 2025-04-03
================================= Tool Message =================================
Name: check_room_availability

2025-04-03 可預訂的房間如下：
房間號碼：001，類型：雙人房
房間號碼：002，類型：單人房
房間號碼：003，類型：雙人房

================================== Ai Message ==================================

好的，沒問題！我是客服主管小美，很高興為您服務。

剛剛為您查詢了員林目前的天氣：
現在是 **陰天**，氣溫大約 **17.5 度**，濕度稍高，風速不大，目前沒有下雨。天氣稍微有點涼，您正在路上，請注意一下路況和保暖喔！

另外，關於您想預訂明天 (也就是 2025年4月3日) 的住宿，我們還有空房可以預訂喔！目前可預訂的房型有：

*   單人房
*   雙人房

請問您比較偏好哪一種房型呢？我可以先幫您保留，等您抵達時再完成入住手續。

期待您的光臨！
'''