import os
from configparser import ConfigParser
from langchain_openai import AzureChatOpenAI
# from openai import AzureOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser 

try:
    # Azure AI Foundry 部屬端點目標URI：
    # {AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT_NAME}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_KEY")
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME") # the custom name you chose for your deployment
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


model = AzureChatOpenAI(api_key=AZURE_OPENAI_API_KEY,
                        openai_api_version=AZURE_OPENAI_API_VERSION,
                        azure_endpoint=AZURE_OPENAI_ENDPOINT,
                        azure_deployment= AZURE_OPENAI_DEPLOYMENT_NAME
                        )


parser = StrOutputParser()
chain = model | parser

user_input = "知之為知之，不知為不知，是知也。"

### 1
messages = [
    # SystemMessage：系統提示訊息，設定大型語言模型的任務／角色／相關注意事項
    SystemMessage("你是一位哲學家，請用哲學的角度解析。"),
    # HumanMessage：使用者輸入的問題或訊息
    HumanMessage(user_input)
]

response = chain.invoke(messages)
# print("這條來自《論語·為政》的經典語句，通常解釋為：「知道就是知道，不知道就是不知道，這是真正的智慧（知識）」。從哲學的角度來看，這句話蘊含了對知識、真理與自我認識的深刻反思。\n\n### 1. **知識與真理的本質**\n這句話首先揭示了對知識誠實的重要性。知識（epistemology）是哲學的基本研究領域，它探究什麼是知識、知識如何被獲得，以及我們如何能確定自己所知的內容。孔子的觀點提醒我們，認識到自己的知識邊界是一種知識的核心表現——這具有現代哲學的「反省意識」。對於人類而言，承認「不知」意味著放棄虛偽的、自以為是的觀念，為真理的探索打開了大門。\n\n**蘇格拉底與孔子的對話**\n孔子的名句與西方哲學家蘇格拉底的名言「我知道我一無所知」異曲同工。兩者都體現了一種哲學上的謙卑，提醒我們：承認自己的無知才是真正探求知識的第一步。這種態度避免傲慢，並促使個體在學習和探究時更具批判性。\n\n### 2. **自我認識與誠實**\n在哲學的倫理維度上，這句話也涉及到個人對自我認識的誠實。誠實（virtue ethics）是一種道德美德，而「知之為知之，不知為不知」需要一種深刻的自我省察，並且拒絕一切形式的矯飾和虛偽。這實踐了中國哲學中對「內聖外王」的要求，即修養自己的內在品質，方能在外界有所建樹。\n\n自我欺騙（self-deception）是哲學上一個常見的課題。當人們假裝知道自己實際上並不了解的事物時，就跌入了自我欺騙的陷阱。而孔子的教導強調，我們應該做真實的自己，對自己的認識保持誠實——這種道德態度本身構成了智慧的一部分。\n\n### 3. **知識的有限性與無限性**\n「不知」的承認同時也表現出對人類理性與知識有限性的接受。康德在其哲學體系中討論了人類認識能力的界限，即我們的知識來源於感性經驗與理智推導，但我們永遠無法全面理解超越這些範疇的事物。類似地，孔子的智慧在於指出，人的知識總是有限的，所以不承認「不知」就等於妨礙了進一步學習的可能性。\n\n然而，孔子並未因此陷入懷疑論（skepticism），相反，他的強調是真實地面對未知，永遠保持積極探索的態度。這並非否定知識，而是倡導一種更積極的求知精神。\n\n### 4. **教育與學習方法論**\n從教育哲學的角度看，這句話也提出了一種務實的學習方法論。學生在學習中，常常會因為害怕承認自己的無知，而停止提問或假裝掌握某些知識。但孔子的這種「坦然認知邊界」的態度告訴我們，承認不知道才是真正學習的起點，也是一種拒絕僵化思維、鼓勵探索與創新的方式。\n\n### 5. **規範智慧的實用性**\n這句話將知識與實踐聯繫起來，反對任何形式的空洞之識或者虛假的智慧。在中國哲學中，知識和「行」是密切相關的，例如孔子所提倡的「知行合一」（儘管這一思想後來由王陽明進一步闡發）。真正的智慧往往體現在如何應用知識於實際的行為中，而不是炫耀不經實踐檢驗的理論。因此，承認「不知」也成為避免誤用知識的重要途徑。\n\n---\n\n### 總結\n「知之為知之，不知為不知，是知也」是一則高度哲學化的智慧箴言，其啟示涵蓋了知識論、自我認識、倫理學、教育哲學以及實踐哲學等領域的核心問題。它提醒我們，在追求智慧時，謙卑與真誠是必不可少的態度，並且只有直面自己的無知，才能為自己打開通向真理的大門。在當代社會依然充滿噪音、假象的信息時代，孔子的這句話格外凸顯了其穿越時空的價值。")


### 2
messages = [
    SystemMessage("你是一位哲學家，也是一位語言專家，請用你的專業翻譯以下內容為英文。"),
    HumanMessage(user_input)
]
response = chain.invoke(messages)
print(response)
# To know what you know and to acknowledge what you do not know—this is true wisdom.