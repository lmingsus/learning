
from configparser import ConfigParser

# 引入必要的模組
from operator import itemgetter
from typing import Literal

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
# from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
# pip install langgraph
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict



try:
    config = ConfigParser()
    config.read('config.ini')
    # Azure OpenAI Model
    AZURE_OPENAI_API_KEY = config.get('Azure', 'OPENAI_KEY')
    AZURE_OPENAI_API_VERSION = config.get('Azure', 'OPENAI_API_VERSION')
    AZURE_OPENAI_ENDPOINT = config.get('Azure', 'OPENAI_ENDPOINT')
    AZURE_OPENAI_DEPLOYMENT_NAME = config.get('Azure', 'OPENAI_DEPLOYMENT_NAME')
    if not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_API_VERSION or not AZURE_OPENAI_ENDPOINT or not AZURE_OPENAI_DEPLOYMENT_NAME:
        raise ValueError("請在 config.ini 中設定所有必要的 Azure OpenAI 參數")
except Exception as e:
    print(f"Error: {str(e)}")
    print("Please provide a valid API key and endpoint")
    exit(1)

llm = AzureChatOpenAI(azure_endpoint=AZURE_OPENAI_ENDPOINT,
                        azure_deployment= AZURE_OPENAI_DEPLOYMENT_NAME,
                        openai_api_version=AZURE_OPENAI_API_VERSION,
                        api_key=AZURE_OPENAI_API_KEY,
                        temperature=0.5,
                        )


# 定義 翻譯 prompt
translate_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一位日本人，也精通各國語言，請將以下文本翻譯成日文："),
        ("human", "{input}")
    ]
)
# 定義 寫作 prompt
write_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一位暢銷散文作家，請根據以下提示創作一五十字左右文字："),
        ("human", "{input}")
    ]
)

# 建構每個 route 的 Chain
translate_chain = translate_prompt | llm | StrOutputParser()
write_chain = write_prompt | llm | StrOutputParser()


# 定義分配分支的 Chain
route_system = "Route the user's query to either the translator or writer."
route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", route_system),
        ("human", "{input}")
    ]
)


# 定義輸出模式
# Define schema for output:
class RouteQuery(TypedDict):
    """Route query to destination expert."""

    destination: Literal["translator", "writer"]



route_chain = route_prompt | llm.with_structured_output(RouteQuery)



# 對於 LangGraph，我們將定義 graph 的狀態來保存查詢、目的和最終答案。
# For LangGraph, we will define the state of the graph to hold the query,
# destination, and final answer.
class State(TypedDict):
    query: str  # 使用者的「查詢」
    destination: RouteQuery  # 查詢的「目的地」
    answer: str  # 最終「答案」



# 定義每個節點的函數，包括路由查詢：
# We define functions for each node, including routing the query:
async def route_query(state: State, config: RunnableConfig):
    destination = await route_chain.ainvoke(state["query"], config)
    # return {"destination": destination}
    return destination



# 為每個提示定義一個節點
# And one node for each prompt
async def prompt_translate(state: State, config: RunnableConfig):
    return {"answer": await translate_chain.ainvoke(state["query"], config)}

async def prompt_write(state: State, config: RunnableConfig):
    return {"answer": await write_chain.ainvoke(state["query"], config)}



# 定義邏輯：根據分類選擇 prompt
# We then define logic that selects the prompt based on the classification
def select_node(state: State) -> Literal["prompt_translate", "prompt_write"]:
    # if state["destination"] == "translator":
    #     return "prompt_translate"
    # else:
    #     return "prompt_write"

    # if state["destination"]["destination"] == "translator":
    #     return "prompt_translate"
    # else:
    #     return "prompt_write"

    if state["destination"] == "translator":
        return "prompt_translate"
    else:
        return "prompt_write"




# 最後，組合多提示鏈。這是兩個步驟的序列：
# Finally, assemble the multi-prompt chain. This is a sequence of two steps:
# 1) 通過 route_chain 選擇「translate」或「write」，並將答案與輸入查詢一起收集。
# 1) Select "translate" or "write" via the route_chain, and collect the answer
# alongside the input query.
# 2) 根據選擇將輸入查詢路由到 translate_chain 或 write_prompt
# 2) Route the input query to translate_chain or write_prompt, based on the
# selection.
graph = StateGraph(State)
graph.add_node("route_query", route_query)
graph.add_node("prompt_translate", prompt_translate)
graph.add_node("prompt_write", prompt_write)

graph.add_edge(START, "route_query")
graph.add_conditional_edges("route_query", select_node)  # 根據 select_node 的返回值選擇下一個節點
graph.add_edge("prompt_translate", END)
graph.add_edge("prompt_write", END)
app = graph.compile()



from IPython.display import Image

Image(app.get_graph().draw_mermaid_png())



# # invoke the chain
# state = await app.ainvoke({"query": "鋒面來襲！全台天氣不穩防強降雨"})
# print(state["destination"])
# print(state["answer"])


import asyncio

# 定義主要非同步函數
async def main():
    state = await app.ainvoke({"query": "威士忌迷有個非常浪漫的說法─那是「天使的分享」。請依此為題。"})
    print(f"處理結果：{state}")
    return state

# 正確執行非同步函數
# 一般 Python 腳本使用方式
if __name__ == "__main__":
    state = asyncio.run(main())
    print(state["destination"])
    print(state["answer"])
    
    # test 1:
    # 處理結果：{'query': '鋒面來襲！全台天氣不穩防強降雨', 'destination': {'destination': 'translator'}, 'answer': '鋒面來襲，雲層厚重，似乎在低語著不安的預兆。全台各地，天氣如同心情般變幻莫測，強降雨隨時可能降臨。讓我們在這不穩定的時刻，學會珍惜每一縷陽光，與雨水共舞。'}       
    # {'destination': 'translator'}
    # 鋒面來襲，雲層厚重，似乎在低語著不安的預兆。全台各地，天氣如同心情般變幻莫測，強降雨隨時可能降臨。讓我們在這不穩定的時刻，學會珍惜每一縷陽光，與雨水共舞。

    # test 2:
    # 處理結果：{'query': '莫斯科不希望暫時停火，認為停火協議只會讓烏克蘭軍隊有喘息的空間，強調俄羅斯追求的是長期的和平解決方案。', 
    #             'destination': {'destination': 'translator'}, 
    #             'answer': '莫斯科堅持不願暫時停火，認為這只會給予烏克蘭軍隊喘息的機會。俄羅斯追求的，是一個持久的和平解決方案，希望通過穩定的協商，為未來鋪設一條真正的和平之路。'}
    
    # test 3:
    # 處理結果：{'query': '莫斯科不希望暫時停火，認為停火協議只會讓烏克蘭軍隊有喘息的空間，強調俄羅斯追求的是長期的和平解決方案。', 'destination': {'destination': 'translator'}, 'answer': 'モスクワは一時的な停戦を望んでおらず、停戦合意はウクライナ軍に喘息の余地を与えるだけだと考えています。ロシアが追求しているのは、長期的な平和解決策であると強調しています。'}
    # {'destination': 'translator'}
    # モスクワは一時的な停戦を望んでおらず、停戦合意はウクライナ軍に喘息の余地を与えるだけだと考えています。ロシアが追求しているのは、長期的な平和解決策であると強調しています。

    # test 4:
    # 處理結果：{'query': '根據中央氣象署地震測報中心資料，今天下午1時09分台灣東部海域發生芮氏規模5.7地震，震央在台東縣政府東北方53.0公里處，深度12.5公里，屬於極淺層地震。', 'destination': 'translator', 'answer': '中央気象局の地震測報センターのデータによると、今日の午後1時09分に台湾東部海域でマグニチュード5.7の地震が発生しました。震源は台東県政府の東北53.0キロメートルの地点で、深さは12.5キロメートルであり、極浅層地震に分類されます。'}
    # translator
    # 中央気象局の地震測報センターのデータによると、今日の午後1時09分に台湾東部海域でマグニチュード5.7の地震が発生しました。震源は台東県政府の東北53.0キロメートルの地点で、深さは12.5キロメートルであり、極浅層地震に分類されます。

    # test 5:
    # 處理結果：{'query': '根據中央氣象署地震測報中心資料，今天下午1時09分台灣東部海域發生芮氏規模5.7地震，震央在台東縣政府東北方53.0公里處，深度12.5公里，屬於極淺層地震。', 'destination': 'writer', 'answer': '今天午後，台灣東部海域傳來一陣震動，芮氏規模5.7的地震如同自然的低語，震央距台東縣政府53公里，深度僅12.5公里。這極淺層的震撼，提醒著我們大自然的力量與無常。'}
    # writer
    # 今天午後，台灣東部海域傳來一陣震動，芮氏規模5.7的地震如同自然的低語，震央距台東縣政府53公里，深度僅12.5公里。這極淺層的震撼，提醒著我們大自然的力量與無常。

    # test 6:
    # 處理結果：{'query': '威士忌迷有個非常浪漫的說法─那是「天使的分享」。請依此為題。', 'destination': 'writer', 'answer': '在威士忌的世界裡，「天使的分享」如同一場靜謐的舞蹈。每一滴流失的酒液，都是與天使的約定，讓酒桶中的故事愈發醇厚。這份浪漫，讓每一杯威士忌都承載著時間的記憶與夢想的芬芳。'}
    # writer
    # 在威士忌的世界裡，「天使的分享」如同一場靜謐的舞蹈。每一滴流失的酒液，都是與天使的約定，讓酒桶中的故事愈發醇厚。這份浪漫，讓每一杯威士忌都承載著時間的記憶與夢想的芬芳。
