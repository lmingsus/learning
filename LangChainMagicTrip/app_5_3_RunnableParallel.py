from langchain_core.runnables import RunnableParallel
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



# 情感傾向
sentiment_prompt = ChatPromptTemplate.from_template("分析以下文本的情感傾向，你的回答必須使用正體中文並且使用台灣慣用語: {text}")
# 主要重點
topic_prompt = ChatPromptTemplate.from_template("提取以下文本的主要主題，你的回答必須使用正體中文並且使用台灣慣用語: {text}")
# 簡短摘要
summary_prompt = ChatPromptTemplate.from_template("為以下文本生成一個簡短的摘要，你的回答必須使用正體中文並且使用台灣慣用語: {text}")


sentiment_chain = sentiment_prompt | llm | StrOutputParser()
topic_chain = topic_prompt | llm | StrOutputParser()
summary_chain = summary_prompt | llm | StrOutputParser()



# 建立 RunnableParallel
text_analyzer = RunnableParallel(
    sentiment=sentiment_chain,
    topic=topic_chain,
    summary=summary_chain
)


def main():
    text = """君悅的商務早餐我第一次吃，感覺非常好，雖然是有年紀的飯店了，但是各方面都維持的很好，" \
    "這是一件非常不容易的事情，期待台北也能有跟歐洲、日本一樣經營超過百年，" \
    "歷久不衰成為經典的飯店，讓台北這個城市多一點深度。"""

    results = text_analyzer.invoke({"text": text})


    print(results)
    # {'sentiment': '這段文本的情感傾向非常正面，表達了對君悅飯店商務早餐的讚賞與滿意。作者提到這是他第一次體驗，感覺「非常好」，顯示出對食物品質的肯定。雖然飯店有年紀，但仍然維持得很好，這讓人感受到一種尊重與欣賞，認為這樣的經營不容易。\n\n此外，作者期待台北能有像歐洲和日本那樣經營超過百年的飯店，這不僅是對君悅的讚美，也反映出他對台北餐飲文化的期待與希望，想要讓這個城市更具深度與歷史感。整體來說，文本流露出對於飯店的喜愛，以及對未來的美好願景，情感上是充滿正能量的。',
    #  'topic': '這段文本的主要主題是對君悅飯店商務早餐的讚賞，以及對於台北飯店業的期待，希望能有更多歷久不衰的經典飯店，提升城市的深度與文化。',
    #  'summary': '我第一次品嚐君悅的商務早餐，感覺相當不錯。這家飯店雖然有些年頭，但各方面維持得很好，真不容易。希望台北也能有像歐洲和日本那樣，經營超過百年的經典飯店，讓這個城市更添深度。'}
    print("情感分析:", results["sentiment"])
    print("主題:", results["topic"])
    print("摘要:", results["summary"])


if __name__ == "__main__":
    main()