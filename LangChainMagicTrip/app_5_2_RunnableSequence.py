from langchain_core.runnables import RunnableSequence
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from typing import TypedDict

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


# 建立提示樣板
chinese_prompt = ChatPromptTemplate.from_messages(
    [("system", "你是一位短文寫作高手，將以使用者指定的主題進行寫作創作，字數約五十字"),
     ("user", "{topic}")]
)

translation_prompt = ChatPromptTemplate.from_messages(
    [("system", "你是一位中英文語言專家，負責中文英的翻譯工作，翻譯的品質必須確保不可以失去文章內容原意"),
     ("user", "{chinese_article}")]
)


# 使用 RunnableSequence 方式建立工作流程
work_flow = RunnableSequence(
    chinese_prompt, llm, translation_prompt, llm, StrOutputParser()
)


result = work_flow.invoke({"topic": "琴酒"})

print(result)



# =========================================================
# 使用 LCEL 表達式建立工作流程，結果相同

work_flow2 = chinese_prompt | llm | translation_prompt | llm | StrOutputParser()

result2 = work_flow2.invoke({"topic":"琴酒"})

print(result2)
# Gin, a refreshing and unique alcoholic beverage, originates from England and is often based on juniper berries. Its aroma is fragrant, and its taste is smooth, commonly paired with various tonic waters or juices, making it a star in the cocktail world. Whether at a party or during a quiet evening, gin always brings a delightful atmosphere.


# =========================================================
# 使用 with_structured_output 建立工作流程


class TranslationOutput(TypedDict):
    chinese_article: str
    english_article: str


# 使用 with_structured_output 建立工作流程
translator = llm.with_structured_output(TranslationOutput)


work_flow3 = RunnableSequence(
    {"chinese_article": chinese_prompt | llm | StrOutputParser()} | translation_prompt | translator
)

result3 = work_flow3.invoke({"topic": "天使的眼淚"})

print(result3)  # dict
# {'chinese_article': '在遙遠的天界，生活著一群美麗的天使，他們的翅膀閃閃發光，身披潔白的長袍，能夠自由翱翔於雲端。這些天使擁有無盡的愛與慈悲，常常俯視人間，關懷著每一個生靈。\n\n然而，天使們的心中也隱藏著一種無法言說的悲傷。這悲傷來自於人類的痛苦與掙扎。每當他們看到人類經歷戰爭、失去和悲傷，便會流下淚水；這些淚水化作星星，點亮了夜空，提醒著人們：無論多麼黑暗的時刻，愛依然會存在。\n\n有一天，一位年輕的天使名叫莉雅，她因為看到人間的一場災難而心痛不已。她決定飛往人間，親自去感受那些苦難與喜悅。在那裡，莉雅遇見了一位名叫阿明的少年，他的家在大火中化為灰燼，面對失去，他依然堅強地微笑，幫助其他失去家園的人。\n\n莉雅被阿明的勇氣所感動，於是她決定用自己的力量來幫助這些人。她在夜裡默默流下眼淚，這些眼淚變成了一股神奇的力量，為失去家園的人們帶來了庇護和希望。當人們在星空下看到那些閃耀的星星時，心中燃起了一絲光明，不再感到孤單。\n\n莉雅知道，她的眼淚不僅是悲傷的象徵，更是天使對人類無私支持的表現。最終，人間的人們明白了愛的意義，開始彼此扶持，共同面對困難。在這份力量的影響下，莉雅也回到了天界。\n\n不再是悲傷的天使，莉雅的心中充滿了信念與希望。每當她看到星空中那閃亮的星星，她就會想起那些用愛與勇氣改變世界的人，與他們分享著天使的眼淚──那是愛的延續，是對世界永恒的祝福。',
#  'english_article': "In a distant celestial realm, there lived a group of beautiful angels. Their wings shimmered, and they wore pure white robes, free to soar among the clouds. These angels possessed endless love and compassion, often looking down upon the earthly realm, caring for every living being.\n\nHowever, within the hearts of the angels lay an unspoken sorrow. This sorrow stemmed from the suffering and struggles of humanity. Whenever they witnessed humans experiencing war, loss, and grief, tears would flow from their eyes; these tears transformed into stars, illuminating the night sky, reminding people that no matter how dark the moment, love will always exist.\n\nOne day, a young angel named Lya was deeply pained by a disaster she witnessed on Earth. She decided to fly down to the human realm to personally feel the pain and joy of those people. There, Lya met a boy named Amin, whose home had turned to ashes in a fire. Facing his loss, he still smiled bravely, helping others who had also lost their homes.\n\nMoved by Amin's courage, Lya chose to use her power to help these people. In the quiet of the night, she wept silently, and her tears became a magical force, bringing shelter and hope to those who had lost their homes. When people looked up at the shining stars in the night sky, a spark of light ignited in their hearts, and they no longer felt alone.\n\nLya understood that her tears were not only a symbol of sadness but also a manifestation of the angels' selfless support for humanity. Eventually, the people on Earth understood the meaning of love, began to support each other, and faced difficulties together. Under the influence of this strength, Lya also returned to the celestial realm.\n\nNo longer a sorrowful angel, Lya's heart was filled with faith and hope. Whenever she gazed at the twinkling stars in the night sky, she would remember those who had changed the world with love and courage, sharing with them the tears of angels—an extension of love, an eternal blessing for the world."}
print(result3['chinese_article'])
print(result3['english_article'])