from langchain_core.runnables import RunnableSequence, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser

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
except Exception as e:
    print(f"Error: {str(e)}")
    print("Please provide a valid API key and endpoint")
    exit(1)


# 定義模型
llm = AzureChatOpenAI(azure_endpoint=AZURE_OPENAI_ENDPOINT,
                        azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME,
                        openai_api_version=AZURE_OPENAI_API_VERSION,
                        api_key=AZURE_OPENAI_API_KEY,
                        temperature=0.8,
                        )



# 寫作風格的參考資料
style_examples = """
1. 一鄉二里，共三夫子不識四書五經六義，竟敢教七八九子，十分大膽
2. 十室九貧，湊得八兩七錢六分五毫四厘，尚且又三心二意，一等下流
3. 圖畫裡，龍不吟，虎不嘯，小小書童可笑可笑
4. 棋盤裡，車無輪，馬無韁，叫聲將軍提防提防
5. 鶯鶯燕燕翠翠紅紅處處融融洽洽
6. 雨雨風風花花葉葉年年暮暮朝朝
"""

# 定義提示模板
writing_template = ChatPromptTemplate.from_template("""
你是一位精通對聯創作的文學大師。請根據以下提供的主題創作一組對聯。

主題: {topic}

請參考以下的寫作風格範例，創作時要體現類似的韻律感和文字技巧：

{style_examples}

要求：
1. 創作一組對仗工整、意境深遠的對聯
2. 對聯應與給定主題相關
3. 儘量融入範例中展現的數字遞進、重複疊字等修辭技巧
4. 確保對聯在音律和結構上和諧統一

請提供：
- 上聯
- 下聯
- 簡短解釋（說明對聯與主題的關聯，以及使用的技巧）
""")


# 定義分析函數
def analyze_couplet(couplet):
    lines = couplet.split('\n')
    if len(lines) < 2:
        return {"error": "無法識別完整對聯"}
    
    upper = lines[0].split('：')[-1].strip() if lines[0] else "" # 取得上聯
    lower = lines[1].split('：')[-1].strip() if lines[1] else "" # 取得下聯
    
    upper_ = upper.replace('，', '').replace('。', '') # 移除逗號和句號
    lower_ = lower.replace('，', '').replace('。', '')

    word_count = len(upper_)
    char_set = set(upper_ + lower_)
    repeated_chars = [char for char in char_set if (upper + lower).count(char) > 1]
    
    return {
        "word_count": word_count,
        "unique_chars": len(char_set),
        "repeated_chars": '、'.join(repeated_chars),
        "upper": upper,
        "lower": lower
    }



# 建立對聯生成系統
couplet_generation_system = RunnableSequence(
    {
        "topic": RunnablePassthrough(),
        "style_examples": lambda _: style_examples
    },
    writing_template,
    llm,
    lambda x: {"content": x.content}, # 將 LLM 輸出轉換為字典
    RunnablePassthrough.assign(
        analysis=lambda x: analyze_couplet(x["content"])
    ),
    # lambda x: {
    #     "content": x["content"],
    #     "analysis": x["analysis"],
    # }
)

# RunnablePassthrough.assign 預設會：
# 1. 保留輸入字典中的所有鍵值
# 2. 添加新指定的鍵值
# 3. 不會刪除任何既有資料



def main():
    # 使用對聯生成系統
    result = couplet_generation_system.invoke("笛卡爾")
    print(result["content"])
    print("\n分析:")
    print(result["analysis"])


if __name__ == "__main__":
    main()


"""
**上聯**：一思二辨，三心四意五感六識，思無邪才有七悟八通九絕  
**下聯**：十指九針，八面玲瓏七情六欲，知自省方能五常四德三生  

**簡短解釋**：這組對聯以「笛卡爾」的思維哲學為主題，強調了他「我思故我在」的觀念。
            上聯通過「一思二辨」等數字遞進，展現了思考、辨析的深入過程，並提及「七悟八通九絕」的智慧境界。
            下聯同樣使用數字結構，強調對於人性和道德的反省與掌握，特別是「五常四德三生」的倫理哲學。
            整體上聯與下聯工整對仗，音律和諧，充分體現了笛卡爾哲學中思考與自省的重要性，
            並且使用了重複疊字和數字遞進的修辭技巧，增強了詩意和意境。

分析:
{'word_count': 23,
 'unique_chars': 38,
 'repeated_chars': '思、四、八、七、五、九、三、六',
 'upper': '一思二辨，三心四意五感六識，思無邪才有七悟八通九絕',
 'lower': '十指九針，八面玲瓏七情六欲，知自省方能五常四德三生'}
"""