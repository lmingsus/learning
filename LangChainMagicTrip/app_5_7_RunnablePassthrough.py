'''
RunnablePassthrough 是 LangChain 中用於資料傳遞和轉換的重要元件。

## 主要用途

1. 資料傳遞
2. 參數映射
3. 鏈式處理中的資料轉換

## 基本使用方式

````python
from langchain_core.runnables import RunnablePassthrough

# 簡單資料傳遞
chain = (
    RunnablePassthrough()  # 直接傳遞輸入
    | prompt 
    | llm
)

# 參數映射
chain = (
    {"question": RunnablePassthrough()}  # 將輸入映射到 "question" 鍵
    | prompt
    | llm
)

# 資料轉換
chain = (
    RunnablePassthrough.assign(
        question=lambda x: x["input"],
        context=lambda x: retrieve_context(x["input"])
    )
    | prompt
    | llm
)
````

## 進階應用

### 1. 多重輸入處理
````python
chain = (
    {
        "question": lambda x: x["question"],
        "context": lambda x: get_context(x["question"]),
        "history": lambda x: x.get("history", [])
    }
    | prompt_template
    | llm
)
````

### 2. 條件式資料轉換
````python
chain = (
    RunnablePassthrough.assign(
        processed_input=lambda x: process_input(x) if needs_processing(x) else x
    )
    | next_step
)
````

### 3. 資料合併
````python
chain = (
    RunnablePassthrough.assign(
        **{
            "original": lambda x: x,
            "enhanced": lambda x: enhance_data(x),
            "metadata": lambda x: get_metadata(x)
        }
    )
    | final_processor
)
````

## 實用範例

### QA 系統
````python
qa_chain = (
    {
        "context": retriever,  # 從檢索器獲取上下文
        "question": RunnablePassthrough()  # 直接傳遞問題
    }
    | prompt
    | llm
    | StrOutputParser()
)
````

### 翻譯系統
````python
translate_chain = (
    {
        "text": RunnablePassthrough(),
        "source_lang": lambda _: "zh-tw",
        "target_lang": lambda _: "en"
    }
    | translate_prompt
    | llm
    | StrOutputParser()
)
````

## 使用建議

1. 保持資料流清晰
2. 適當使用 lambda 函數
3. 善用 `.assign()` 方法
4. 考慮資料型別的一致性

這樣的設計能讓資料在處理鏈中更有條理地流動，同時保持程式碼的可讀性和可維護性。
'''

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
1. 露從今夜白，月是故鄉明。有弟皆分散，無家問死生。寄書長不達，況乃未休兵。
2. 玉露凋傷楓樹林，巫山巫峽氣蕭森。江間波浪兼天湧，塞上風雲接地陰。叢菊兩開他日淚，孤舟一繫故園心。寒衣處處催刀尺，白帝城高急暮砧。
3. 夔府孤城落日斜，每依南鬥望京華。聽猿實下三聲淚，奉使虛隨八月槎。畫省香爐違伏枕，山樓粉堞隱悲笳。請看石上藤蘿月，已映洲前蘆荻花。
4. 千家山郭靜朝暉，日日江樓坐翠微。信宿漁人還泛泛，清秋燕子故飛飛。匡衡抗疏功名薄，劉向傳經心事違。同學少年多不賤，五陵裘馬自輕肥。
5. 聞道長安似弈棋，百年世事不勝悲。王侯第宅皆新主，文武衣冠異昔時。直北關山金鼓振，徵西車馬羽書馳。魚龍寂寞秋江冷，故國平居有所思。
6. 瞻華清之莘莘漠漠，而山殿戌削，縹焉天風，藉由回薄。上揚雲旓兮下列猛獸。
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


# 建立對聯生成系統
couplet_generation_system = RunnableSequence(
    {
        "topic": RunnablePassthrough(),
        "style_examples": lambda _: style_examples,
        # "style_examples": style_examples # 不能直接使用字串，Expected a Runnable, callable or dict.
    },
    writing_template,
    llm
)

def main():
    # 使用對聯生成系統
    result = couplet_generation_system.invoke({"topic": "高斯"})
    print(result.content)


if __name__ == "__main__":
    main()


# {"topic": "高斯"}
"""
**上聯**：高山仰止景無涯，數理根基追夢遠。  
**下聯**：低谷隱忍志更堅，方程思維逐浪行。

**簡短解釋**：此對聯以“高斯”為主題，第一句突出了高斯在數學和科學上的卓越與追求，描繪了他對知識的追尋不懈的精神；而第二句則表達了在困難與挑戰
中持續克服自我，勇往直前的堅韌。整體上聯和下聯在意境上形成了高低起伏的對比，展現了對數學思想的敬仰和對探索真理的勇氣。修辭上使用了“高”、“低”及“夢”、“行”的對應，並有數理與方程的呼應，音律也和諧統一。"
"""