from configparser import ConfigParser

from langchain.chains import LLMChain
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate


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



# 定義情緒分析的提示樣板
sentiment_analysis_prompt = PromptTemplate(
    input_variables=["user_input"],
    template="根據這段話分析情緒，並僅回答 'positive' 或 'negative'：'{user_input}'"
)
# 建立情緒分析的 LLMChain
sentiment_analysis_chain = sentiment_analysis_prompt | llm



# 負面情緒應對的 PromptTemplate
negative_response_prompt = PromptTemplate(
    input_variables=["user_input"],
    template="使用者說了這段話：'{user_input}'。請給出一段安撫的回應。"
)
negative_response_chain = negative_response_prompt | llm


# 正面情緒應對的 PromptTemplate
positive_response_prompt = PromptTemplate(
    input_variables=["user_input"],
    template="使用者說了這段話：'{user_input}'。請給出一段正向互動的回應。"
)
positive_response_chain = positive_response_prompt | llm




def execute_conditional_chain(user_input):
    # 第一步：使用 LLM 來分析情緒
    sentiment_result = sentiment_analysis_chain.invoke({"user_input": user_input}).content.strip()
    
    # 第二步：根據情緒結果選擇要執行的chain
    if sentiment_result.strip().lower() == "negative":
        # 如果情緒為負面，執行負面應對chain
        response = negative_response_chain.invoke({"user_input": user_input})
    else:
        # 如果情緒為正面，執行正面應對鏈結
        response = positive_response_chain.invoke({"user_input": user_input})
    
    return response.content



if __name__ == "__main__":
    # 執行 Conditional Chain
    result = execute_conditional_chain("我對於你們的服務感到非常滿意，服務人員很用心，環境也很整潔。")

    print("\n回應結果：")
    print(result)

    # 回應結果：
    # 非常感謝您的正面評價！我們很高興聽到您對我們的服務感到滿意。服務人員的用心和整潔的環境是我們一直以來努力的方向。您的支持是我們前進的動力，期待您再次光臨，為您提供更好的服務！如果有任何建議或需求，隨時告訴我們喔！
