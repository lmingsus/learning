from configparser import ConfigParser

# 引入 Chain 模組
from langchain.chains.sequential import SimpleSequentialChain
# 引入 Azure OpenAI LLM 模組
from langchain_openai import AzureChatOpenAI
# 引入 Prompt Template 模組
from langchain_core.prompts import PromptTemplate
# 引入 Output Parser 模組
from langchain_core.output_parsers import StrOutputParser

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
                        temperature=0.9,
                        )

# 定義描述模板
describe_prompt = PromptTemplate(
    input_variables=["city"],
    template="請用一段優雅的文字描述 {city} 這個城市。"
)

# 定義生成旅遊建議模板
travel_prompt = PromptTemplate(
    input_variables=["description"],
    template="請根據以下描述，為旅客提供一些旅遊指南: ### {description} ###"
)

# 定義翻譯模板
translate_prompt = PromptTemplate(
    input_variables=["travel"],
    template="請將以下描述翻譯成日文: ### {travel} ###"
)

# 定義輸出解析器
output_parser = StrOutputParser()

# 建立三個 Chain，分別對應描述、翻譯與生成旅遊建議
describe_chain = describe_prompt | llm | output_parser
travel_chain = travel_prompt | llm | output_parser
translate_chain = translate_prompt | llm | output_parser

# from langchain.chains.sequential import SequentialChain
# seq_chain = SequentialChain(chains=[describe_chain, travel_chain, translate_chain],
#                             input_variables=["city"],
#                             output_variables=["final_advice"]
#                             )
# result = seq_chain.invoke("台北")

# =======================================================
from langchain_core.runnables import RunnablePassthrough, RunnableSequence

chain = describe_chain | RunnablePassthrough() | travel_chain | RunnablePassthrough() | translate_chain

# 執行處理鏈
result = chain.invoke("員林")

# 印出結果
print(result)

'''
### 員林観光ガイド

ようこそ員林へ！この街は古き良き魅力と現代的な魅力を兼ね備えており、豊かな文化と魅力的な自然風景を誇っています。以下は、員林での時間を最大限に楽しむためのいくつかの観光アドバイスです。

#### おすすめスポット

1. **伝統寺院巡り**
   - 地元の寺院、例えば員林慈惠宮を訪れて、その独特な建築様式や精巧な彫刻を楽しみ、台湾の伝統的な信仰の魅力を感じてください。

2. **文化イベント**
   - 祭りの期間中に訪れる場合は、地元の民俗イベントを見逃さないでください。寺会や龍舞、獅子舞など、これらのイベントは非常に賑やかで、台湾文化の真髄を体験できます。

3. **自然探索**
   - 周辺の田園や山々を訪れてみてください。春の桜、夏の稲穂、秋冬の雲海など、美しい自然の景色が広がっており、写真撮影やハイキングに最適です。

#### グルメ探索

1. **ローカルフード**
   - 市中心部の通りには多くの屋台があり、牛肉麺や鹽酥鶏、臭豆腐などのクラシックな料理を楽しむことができます。台湾の風味を存分に味わってください。

2. **カフェで休憩**
   - 員林には独特なスタイルのカフェがたくさんあります。お気に入りの一軒で腰を下ろし、香り高いコーヒーを楽しみながら、窓の外の田園風景に癒されてください。

#### 旅行のヒント

- **交通の便利さ**：員林の公共交通は非常に便利です。市内のバスやレンタサイクルを利用して、街の隅々を探索しましょう。

- **静けさを保つ**：賑やかな市場がある一方で、伝統的な寺院を訪れる際は、文化や信仰に対する敬意を表すために静かにしていてください。

- **地元の習慣を尊重する**：民俗イベントに参加する際は、地元の習慣を理解し遵守することで、旅行体験がより充実したものになります。

この観光ガイドが、あなたの員林での旅をより楽しいものにし、この街の独特な魅力を感じられることを願っています！
'''


# =========================================================

chain2 = describe_chain | travel_chain | translate_chain

result2 = chain2.invoke("三重")
print(result2)
'''
### ### 三重旅行ガイド

#### 導入
三重は台湾北部に位置し、現代と伝統が見事に融合した都市で、壮大な自然景観と豊かな文化歴史を備えています。美食愛好者や文化探索者にとって、ここには無限の驚きが待っています。

#### 必見スポット

1. **陽明山**
   - **活動**: ハイキングと自然観賞
   - **特徴**: 壮観な山の景色を提供し、特に朝や夕方には特別に美しい景色が楽しめます。

2. **三重夜市**
   - **グルメ**: 餃子や海鮮などの地元のスナック。
   - **雰囲気**: 夜は賑やかで多様な屋台が立ち並び、ストリートフードを楽しむことができます。

3. **古街と寺院**
   - **おすすめ**: 地元の古い寺院を訪れて、伝統文化の雰囲気を感じてみてください。地元の祭りに参加し、住民と共に文化の継承を体験できます。

4. **河川公園**
   - **活動**: 散歩とサイクリング
   - **特徴**: 美しい川沿いの散歩道は散歩に最適で、ゆったりとした午後のひとときを楽しみながら流れる川を眺めることができます。

#### グルメおすすめ

- **三重名物餃子**: 地元の料理として見逃せない一品で、皮は薄く、具材は新鮮で、タレを添えてさらに美味しさが増します。
- **海鮮スナック**: 新鮮な海鮮の選択肢が豊富で、焼きイカやエビなど、味わい深い料理が楽しめます。
- **屋台**: 各屋台には独特の味がありますので、ぜひいくつか試してみて、現地の味を体験してください。

#### 小さなヒント

- **交通**: 三重の公共交通機関は便利で、地下鉄やバスを利用して主要な観光スポットに簡単にアクセスできます。
- **文化的礼儀**: 寺院を訪れる際は、地元の信仰を尊重し、静かにして、迷惑をかけないようにしましょう。
- **ベスト旅行時期**: 春と秋の気候は心地よく、旅行するのに最適です。

#### まとめ 
三重は魅力あふれる都市で、現代的な都市の雰囲気と濃厚な伝統文化を併せ持っています。美食を楽しみたい方も、歴史を探求したい方も、三重は忘れられない体験を提供してくれます。この素晴らしい旅の準備はできましたか？###

'''

# ============================================


# 定義描述模板
describe_prompt3 = PromptTemplate(
    input_variables=["city"],
    template="請用一段優雅的文字描述 {city} 這個城市，字數一百字左右。",
    output_variables=["description"]
)

# # 定義生成旅遊建議模板
# travel_prompt = PromptTemplate(
#     input_variables=["description"],
#     template="請根據以下描述，為旅客提供一些旅遊指南: ### {description} ###"
# )

# 定義翻譯模板
translate_prompt3 = PromptTemplate(
    input_variables=["description"],
    template="請將以下描述翻譯成日文: ### {description} ###",
    output_variables=["translate"]
)

chain3 = describe_prompt3 | llm | translate_prompt3

result3 = chain3.invoke("員林")
print(result3)
'''
StringPromptValue(text="請將以下描述翻譯成日文: 
                ### content='員林，這座位於台灣中部的小城，以其悠閒的氛圍與豐富的文化底蘊而聞名。街道兩旁，古老的建築與現代商業區相互輝映，仿佛在訴說著過去與現在的故事。市中心的公園綠意盎然，是居民休憩的好去處；而夜市則彌漫著各式美食的香氣，吸引著人們流連忘返。每年舉辦的傳統節慶，更是讓這座城市充滿了熱情與活力，彰顯出員林獨特的人文魅力與生活風貌。' 
                  additional_kwargs={'refusal': None} 
                  response_metadata={'token_usage': {'completion_tokens': 164, 'prompt_tokens': 31, 'total_tokens': 195, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_b705f0c291', 'prompt_filter_results': [{'prompt_index': 0, 'content_filter_results': {'hate': {'filtered': False, 'severity': 'safe'}, 'jailbreak': {'filtered': False, 'detected': False}, 'self_harm': {'filtered': False, 'severity': 'safe'}, 'sexual': {'filtered': False, 'severity': 'safe'}, 'violence': {'filtered': False, 'severity': 'safe'}}}], 'finish_reason': 'stop', 'logprobs': None, 'content_filter_results': {'hate': {'filtered': False, 'severity': 'safe'}, 'self_harm': {'filtered': False, 'severity': 'safe'}, 'sexual': {'filtered': False, 'severity': 'safe'}, 'violence': {'filtered': False, 'severity': 'safe'}}} 
                  id='run-84cdf577-c613-4fd4-9d5b-fb1160fd5b47-0' 
                  usage_metadata={'input_tokens': 31, 'output_tokens': 164, 'total_tokens': 195, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}} 
                ###")
'''

# =======
chain31 = (
    {"city": lambda x: x}
    | describe_prompt3
    | llm
    | {"description": lambda x: x.content} 
    | translate_prompt3
    | llm
    | {"translate123": lambda x: x.content}
)

result31 = chain31.invoke({"city": "員林"})
print(result31)
{'translate123': '### 員林（エンリン）、この台湾中部に位置する小さな街は、まるで静かな水彩画のようです。街には緑豊かな木々が茂り、通りの両側には古い建物と現代の商業地区が調和しながら人文的な雰囲気を醸し出しています。夕暮れ時には、夕陽がこの土地に金色の薄いヴェールをかけ、住民たちは街角の屋台で地元の美味しい料理を味わい、笑い声が響き渡ります。員林は交通の要所であるだけでなく、心の港でもあり、どこにいてもここでの温かさとくつろぎは、常に人々を魅了します。 ###'}

# =======

# "x" 未定義
# chain4 = {'city': x} | describe_prompt3 | llm | {'description': x.content} 
