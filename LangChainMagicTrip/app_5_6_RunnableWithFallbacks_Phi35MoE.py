'''
RunnableWithFallbacks 是一個包裝器，用於建立具有備援機制的處理鏈。
基本概念
- 主要執行器（Primary Runnable）：優先使用的處理邏輯
- 備援執行器（Fallback Runnables）：當主要執行器失敗時的替代方案
- 錯誤處理：自動切換到下一個備援方案


from langchain.runnables import RunnableWithFallbacks

main_runnable = SomeRunnable()
fallback1 = FallbackRunnable1()
fallback2 = FallbackRunnable2()

runnable_with_fallbacks = RunnableWithFallbacks(main_runnable,
                                                fallbacks=[fallback1, fallback2])

result = runnable_with_fallbacks.invoke(input_data)
'''

from langchain_core.runnables import RunnableSequence, RunnableWithFallbacks, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI

# pip install -U langchain-azure-ai
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
# from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

import time
from configparser import ConfigParser

try:
    config = ConfigParser()
    config.read('config.ini')
    # Azure AI Foundry 部屬端點目標URI：
    # {AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT_NAME}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}
    
    # Azure OpenAI Model
    AZURE_OPENAI_API_KEY = config.get('Azure', 'OPENAI_KEY')
    AZURE_OPENAI_API_VERSION = config.get('Azure', 'OPENAI_API_VERSION')
    AZURE_OPENAI_ENDPOINT = config.get('Azure', 'OPENAI_ENDPOINT')
    AZURE_OPENAI_DEPLOYMENT_NAME = config.get('Azure', 'OPENAI_DEPLOYMENT_NAME')
    if not all([AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT_NAME]):
        raise ValueError("請在 config.ini 中設定所有必要的 Azure OpenAI 參數")

    # Phi-3.5-MoE-instruct
    # https://learn.microsoft.com/en-us/azure/ai-foundry/model-inference/how-to/inference?tabs=python
    # ENDPOINT = https://<resource>.services.ai.azure.com/models
    PHI_API_KEY = config.get('Azure', 'PHI35MOE_KEY')
    PHI_API_VERSION = config.get('Azure', 'PHI35MOE_API_VERSION')
    PHI_ENDPOINT = config.get('Azure', 'PHI35MOE_ENDPOINT')
    PHI_DEPLOYMENT_NAME = config.get('Azure', 'PHI35MOE_DEPLOYMENT_NAME')
    PHI_MODEL_NAME = config.get('Azure', 'PHI35MOE_MODEL_NAME')
    if not all([PHI_API_KEY, PHI_API_VERSION, PHI_ENDPOINT, PHI_DEPLOYMENT_NAME, PHI_MODEL_NAME]):
        raise ValueError("請在 config.ini 中設定所有必要的 Phi-3.5-MoE 參數")

except Exception as e:
    print(f"Error: {str(e)}")
    print("Please provide a valid API key and endpoint")
    exit(1)


# 定義模型
base_llm = AzureChatOpenAI(azure_endpoint=AZURE_OPENAI_ENDPOINT,
                            azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME,
                            openai_api_version=AZURE_OPENAI_API_VERSION,
                            api_key=AZURE_OPENAI_API_KEY,
                            temperature=0.5,
                            )

advanced_llm = AzureAIChatCompletionsModel(
    endpoint=PHI_ENDPOINT,
    # credential=AzureKeyCredential(PHI_API_KEY),
    credential=PHI_API_KEY,
    model=PHI_MODEL_NAME,
    model_name=PHI_MODEL_NAME,
)


# 定義提示樣版
base_prompt = ChatPromptTemplate.from_template("請回答以下問題：{question}")
advanced_prompt = ChatPromptTemplate.from_template("請回答以下問題：{question}")



# 基礎模型 Chain
base_chain = RunnableSequence(
    base_prompt,
    base_llm
)

# 進階模型 Chain
advanced_chain = RunnableSequence(
    advanced_prompt,
    advanced_llm
)



# 模擬不穩定隨機失敗的進階模型
def unstable_advanced_model(query):
    # 模擬隨機失敗
    if int(time.time()) % 2 == 0:
        raise Exception("LLM Service unavailable")
    return advanced_chain.invoke(query)

# 預設失敗回應
def predefined_fallback(query):
    return "很抱歉，目前無法回應您的問題，請洽客服專線。"


def main():
    # 建立問答 Chain
    qa_chain = RunnableLambda(unstable_advanced_model)

    # 使用 RunnableWithFallbacks 建立問答系統
    qa_system = RunnableWithFallbacks(
        runnable=qa_chain,                 # 主要執行器     
        fallbacks=[                        # 備援執行器列表
            base_chain,                    # 第一備援            
            RunnableLambda(predefined_fallback)   # 第二備援
        ]
    )

    # 測試問答系統
    for _ in range(5):
        try:
            result = qa_system.invoke({"question": "用五十字介紹歐拉"})
            print(f"回答：{result.content}")
            if model_name := result.response_metadata.get("model"):
                print(f"使用模型：{model_name}")
            else:
                print(f"使用模型：{result.response_metadata.get("model_name")}")
            # print(result)
        except Exception as e:
            print(f"錯誤: {str(e)}")
        print("-------------")
        time.sleep(2)



if __name__ == "__main__":
    main()

# test 1: {"question": "用五十字介紹歐拉"}
'''
回答： 歐拉，18世紀瑞士數學家，生於柏林。專注於數學和物理學，革新了微積分。他對數論、幾何學和數論的貢獻巨大，包括歐拉公式和歐拉恆等。歐拉被認為是歷史上最多產的數學家之一。他的工作為現代數
學和物理學奠定了基礎。
使用模型：phi35-moe-instruct
-------------
回答： 歐拉，18世紀瑞典數學家，物理學家和天文學家。他對微積分、數論和級數做出了重大貢獻。他的公式和定理，如歐拉方程、歐拉恆等式和歐拉定理，廣泛應用於數學和工程領域。他是著名的數學期刊《歐
拉通信》的創辦人。
使用模型：phi35-moe-instruct
-------------
回答：萊昂哈德·歐拉（Leonhard Euler，1707-1783）是瑞士數學家和物理學家，對數學的許多領域有深遠貢獻，包括數論、圖論和微積分。他引入了許多數學符號，如函數符號f(x)和指數符號e，對現代數學影響
深遠。
使用模型：gpt-4o-mini-2024-07-18
-------------
回答： 歐拉，數學家，物理學家，1707-1783年。他在微積分、數論、光學等領域有開創性貢獻。歐拉公式、歐拉方程式等著名。他對數學的影響深遠，他的工作仍被廣泛應用。
使用模型：phi35-moe-instruct
-------------
回答：歐拉（Leonhard Euler，1707-1783）是瑞士數學家和物理學家，對數學各領域貢獻卓著。他創立了圖論，發展了微積分和數論，並引入了許多數學符號，如函數符號f(x)和歐拉公式。其著作影響深遠。
使用模型：gpt-4o-mini-2024-07-18
-------------
'''

# test 2: {"question": "用五十字介紹高斯"}
'''
回答： 高斯，全名為卡爾·高斯，是一位德國數學家和天文學家。他對數學的重大貢獻包括高斯定律和高斯函數。他在數學分析、統計學和幾何學領域享有盛譽。高斯因其著名的高斯消元法而聞名，這是一種解線
性方程組的有效技術。他的工作對後來的發展，包括對數學和理論物理學的深遠影響，產生了深遠的影響。
使用模型：phi35-moe-instruct
-------------
回答：卡尔·弗里德里希·高斯（1777-1855）是德国数学家和物理学家，被誉为“数学王子”。他在数论、代数、统计学、天文学等领域做出了重要贡献，特别是高斯定理和高斯曲率等理论，影响深远。
使用模型：gpt-4o-mini-2024-07-18
-------------
回答：高斯（Carl Friedrich Gauss）是德國數學家和物理學家，被譽為“數學之王”。他在數論、代數、統計、天文學等領域做出重大貢獻，特別是高斯定理和高斯曲率等概念，對現代數學影響深遠。
使用模型：gpt-4o-mini-2024-07-18
-------------
回答： 高斯，全名戈特弗里德·威廉·莱布尼茨·高斯，是一位德國數學家、天文學家。他在1777年出生，被認為是最偉大的數學家之一。高斯做出了重要貢獻，包括高斯定理、高斯積分和高斯趨勢。他對數學、物
理學和天文學的研究影響深遠。高斯的工作形成了數學的基礎，成為許多現代專業的基礎。他是一位傑出的科學家，其創新與智慧激勵了後世。
使用模型：phi35-moe-instruct
-------------
回答： 高斯，全名戈特弗里德·威廉·莱布尼茨·高斯，德國數學家、物理學家。被譽為數學界的「皇帝」，因其卓越貢獻至今影響深遠。他在代數、幾何、統計、天文學等領域的開創性研究，使他成為歷史上最重
要的數學家之一。高斯的成就包括高斯定律、高斯積分、高斯曲線、高斯求和等。他的工作為後來的科學發展奠定了基礎，對數學、物理學和工程學的發展產生了深遠的影響。
使用模型：phi35-moe-instruct
-------------
'''