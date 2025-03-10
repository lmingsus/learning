import os
from configparser import ConfigParser
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


try:
    # Azure AI Foundry 部屬端點目標URI：
    # {AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT_NAME}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_KEY")
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    if not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_API_VERSION or not AZURE_OPENAI_ENDPOINT:
        raise Exception("Please provide a valid API key and endpoint")
except:
    try:
        config = ConfigParser()
        config.read('config.ini')
        AZURE_OPENAI_API_KEY = config.get('Azure', 'OPENAI_KEY')
        AZURE_OPENAI_API_VERSION = config.get('Azure', 'OPENAI_API_VERSION')
        AZURE_OPENAI_ENDPOINT = config.get('Azure', 'OPENAI_ENDPOINT')
        AZURE_OPENAI_DEPLOYMENT_NAME = config.get('Azure', 'OPENAI_DEPLOYMENT_NAME')

        if not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_API_VERSION or not AZURE_OPENAI_ENDPOINT or not AZURE_OPENAI_DEPLOYMENT_NAME:
            raise Exception("Please provide a valid API key and endpoint")
    except:
        print("Please provide a valid API key and endpoint")
        exit()


model = AzureChatOpenAI(azure_endpoint=AZURE_OPENAI_ENDPOINT,
                        azure_deployment= AZURE_OPENAI_DEPLOYMENT_NAME,
                        openai_api_version=AZURE_OPENAI_API_VERSION,
                        api_key=AZURE_OPENAI_API_KEY,
                        )

parser = StrOutputParser()

system_prompt = """
請依照這個格式回答：
單字：{text}
情境：{scenario}
{native_language}翻譯：
{target_language}造句：
{native_language}翻譯：
"""

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_prompt),
     ("user", "{text}")]
)

chain = prompt_template | model | parser

native_language = "正體中文"
target_language = "英文"
scenario_array = [
    "在餐廳",
    "在學校",
    # "在醫院",
    # "在銀行",
    # "在超市",
    # "在圖書館",
    # "在機場",
    # "在火車站",
    # "在公園",
    # "在辦公室",
    # "在家裡",
    "在商店",
]
vocabularies = [
    "hungry",
    # "glad",
    "stranger",
    # "proud",
    "excited",
]
results = []

for voc in vocabularies:
    for scenario in scenario_array:
        response = chain.invoke(
            {"text": voc, 
            "scenario": scenario,
            "native_language": native_language, 
            "target_language": target_language}
            )
        results.append(response)

for res in results:
    print(res)
    print("======")

'''
單字：hungry  
情境：在餐廳  
正體中文翻譯：飢餓的  
英文造句：I am so hungry that I could eat a horse.  
正體中文翻譯：我非常飢餓，感覺可以吃下一匹馬。
======
單字：hungry  
情境：在學校  
正體中文翻譯：饑餓的  
英文造句：I always feel hungry during my afternoon classes.  
正體中文翻譯：我在下午的課堂上總是感到饑餓。
======
單字：hungry  
情境：在商店  
正體中文翻譯：餓  
英文造句：I am so hungry; I need to buy some snacks.  
正體中文翻譯：我好餓，我需要買一些零食。  
======
單字：stranger  
情境：在餐廳  
正體中文翻譯：陌生人  
英文造句：I noticed a stranger sitting alone at the corner table of the restaurant.  
正體中文翻譯：我注意到一個陌生人獨自坐在餐廳的角落桌子上。  
======
單字：stranger  
情境：在學校  
正體中文翻譯：陌生人  
英文造句：I saw a stranger sitting alone in the cafeteria.  
正體中文翻譯：我看到一個陌生人獨自在餐廳裡坐著。
======
單字：stranger  
情境：在商店  
正體中文翻譯：陌生人  
英文造句：I saw a stranger looking at the same item on the shelf as I was.  
正體中文翻譯：我看到一個陌生人在和我一樣的貨架上看著同樣的商品。
======
單字：excited  
情境：在餐廳  
正體中文翻譯：興奮的  
英文造句：I am so excited to try the new dishes on the menu!  
正體中文翻譯：我非常興奮能嘗試菜單上的新菜！
======
單字：excited  
情境：在學校  
正體中文翻譯：興奮的  
英文造句：I was excited to see my friends after the summer vacation.  
正體中文翻譯：我在暑假後見到朋友們時感到很興奮。  
======
單字：excited  
情境：在商店  
正體中文翻譯：興奮的  
英文造句：I was excited to see the new toys on the shelf.  
正體中文翻譯：我看到貨架上的新玩具時感到興奮。
======
'''