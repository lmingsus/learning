'''
from langchain_core.runnables import RunnableBranch

branch = RunnableBranch(
    (condition1, chain1),
    (condition2, chain2),
    (condition3, chain3),
    default_action=chain4
)
'''
from langchain_core.runnables import RunnableBranch,RunnableSequence
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from configparser import ConfigParser

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




# 語言識別 Chain
language_identification_prompt= ChatPromptTemplate.from_template(
    "Please identify the language of the following text."
    "Respond with 'Chinese' for Chinese, "
    "'English' for English, "
    "or 'Other' for any other language."
    "Text: {text}")
language_identification_chain = language_identification_prompt | llm | StrOutputParser()


# 建立中文服務 Chain
chinese_prompt = ChatPromptTemplate.from_template(
    "你是一位中文客服機器人，請根據用戶的問題提供正體中文回應。 ### {text} ### "
    )
chinese_chain = chinese_prompt | llm | StrOutputParser()


# 建立英文服務 Chain
english_prompt = ChatPromptTemplate.from_template(
    "You are an English customer service bot."
    "Please respond to the user's query in English.###{text}"
    )
english_chain = english_prompt | llm | StrOutputParser()



# 建立 RunnableBranch
workflow = RunnableSequence(
    # 先進行語言識別
    {"language": language_identification_chain,
      "text": lambda x: x["text"]},
    
    # 再根據語言進行不同的處理
    RunnableBranch(
        (lambda x: x["language"].strip().lower() == "chinese" , chinese_chain),
        (lambda x: x["language"].strip().lower() == "english" , english_chain),
        english_chain  # 預設回應
    )
)


def main():
    # text = "台北酒店是一家非常高端的五星級酒店，地處市中心，交通非常便利。酒店大堂氣派非凡，員工服務也十分親切，讓人一進門就感受到無微不至的關懷。"
    # text = "The hotel is comfortable and elegant, the food is rich and delicious, and the service is considerate and warm. Thank you for the hotel's reception."
    text = "ホテルは快適でエレガント、食事は豊富で美味しい、サービスは丁寧で温かい ホテルのフロントに感謝します。"
    results = workflow.invoke({"text": text})
    print(results)
    # 您好！感謝您對台北酒店的關注。這家五星級酒店的確位於市中心，交通十分便利，方便您前往各大景點。
    # 酒店的大堂設計氣派，讓人感受到奢華的氛圍。
    # 此外，酒店的員工也非常友善，致力於提供優質的服務，讓每位客人都能享受到貼心的關懷。
    # 如果您有任何其他問題或需要進一步的資訊，隨時都可以詢問我！

    '''
    Thank you for your kind words! We're delighted to hear that you found our hotel comfortable and elegant,
    enjoyed the delicious and varied meals, and appreciated the attentive and warm service from our front desk staff.
    Your feedback means a lot to us, and we look forward to welcoming you back soon! 
    If you have any further questions or need assistance, please let us know.
    '''


if __name__ == "__main__":
    main()