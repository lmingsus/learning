from langchain_core.runnables import RunnableParallel
from langchain_core.prompts import ChatPromptTemplate
# from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from app_5_3_RunnableParallel import llm

# 翻譯
english_prompt = ChatPromptTemplate.from_template("你是一位英文語言專家，請將以下短文翻譯成英文 : {text}")
japan_prompt = ChatPromptTemplate.from_template("你是一位日文語言專家，請將以下短文翻譯成日文 : {text}")
french_prompt = ChatPromptTemplate.from_template("你是一位法語語言專家，請將以下短文翻譯成法文 : {text}")

english_chain = english_prompt | llm | StrOutputParser()
japan_chain = japan_prompt | llm | StrOutputParser()
french_chain = french_prompt | llm | StrOutputParser()

# 建立 RunnableParallel
text_analyzer = RunnableParallel(
    english=english_chain,
    japan=japan_chain,
    french=french_chain
)

def main():
    text = "酒店的房間，所呈現出的繽紛色彩，給人煥然一新的感覺。確實有其水準和質感！"
    results = text_analyzer.invoke({"text": text})

    print(results)
    # {'english': 'The vibrant colors presented in the hotel rooms give a refreshing feeling. They truly reflect a certain level of quality and sophistication!',
    #  'japan': 'ホテルの部屋が見せる鮮やかな色彩は、まるで新たな気分をもたらしてくれます。確かにその水準と質感がありますね！',
    #  'french': "Les chambres de l'hôtel, avec leurs couleurs vives, offrent une sensation de renouveau. Elles ont en effet un certain niveau et une qualité indéniables !"}

    print("英文:", results["english"])
    print("日文:", results["japan"])
    print("法文:", results["french"])


if __name__ == "__main__":
    main()