from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore # , RetrievalMode
# from langchain_community.vectorstores import Qdrant
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.http import models
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from pydantic import BaseModel


from configparser import ConfigParser
try:
    config = ConfigParser()
    config.read('config.ini', encoding='utf-8')

    # Azure OpenAI Embedding
    EMBEDDING_MODEL = config.get('Azure', 'EMBEDDING_MODEL')
    AZURE_OPENAI_API_KEY = config.get('Azure', 'OPENAI_KEY')
    AZURE_OPENAI_ENDPOINT = config.get('Azure', 'OPENAI_ENDPOINT')
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME = config.get('Azure', 'OPENAI_EMBEDDING_DEPLOYMENT_NAME')
    AZURE_OPENAI_API_EMBEDDING_VERSION = config.get('Azure', 'OPENAI_API_EMBEDDING_VERSION')
    if not all([EMBEDDING_MODEL, AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME, AZURE_OPENAI_API_EMBEDDING_VERSION]):
        raise Exception("Please provide all required Azure OpenAI Embedding configuration values in config.ini.")
    
    # Qdrant
    QDRANT_URL = config.get('QDRANT', 'ENDPOINT') + ':6333'
    QDRANT_API_KEY = config.get('QDRANT', 'API_KEY')
    if QDRANT_URL == ':6333' or not QDRANT_API_KEY:
        raise Exception("Please provide all required Qdrant configuration values in config.ini.")
    
    # Azure OpenAI Chat
    AZURE_OPENAI_DEPLOYMENT_NAME = config.get('Azure', 'OPENAI_DEPLOYMENT_NAME')
    AZURE_OPENAI_API_VERSION = config.get('Azure', 'OPENAI_API_VERSION')
    if not all([AZURE_OPENAI_DEPLOYMENT_NAME, AZURE_OPENAI_API_VERSION]):
        raise Exception("Please provide all required Azure OpenAI configuration values in config.ini.")
except Exception as e:
    print(f"Error: {str(e)}")


embeddings_model = AzureOpenAIEmbeddings(
    api_key=AZURE_OPENAI_API_KEY,
    azure_deployment=AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME, 
    openai_api_version=AZURE_OPENAI_API_EMBEDDING_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
)

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

model = AzureChatOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME,
    openai_api_version=AZURE_OPENAI_API_VERSION,
    api_key=AZURE_OPENAI_API_KEY,
    temperature=0,
)

# 讀取 PDF 文件
loader = PyPDFLoader("docs/RoadTrafficRegu.pdf")
pages  = loader.load()

len(pages) # 共 62 頁
# type(pages[0]) # langchain_core.documents.base.Document

# 分割文檔，建立一個 Splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=320,
    chunk_overlap=80,
)
# 分割文檔為更小的片段
chunks: list = splitter.split_documents(pages)
# print(chunks[1].page_content)
# len(chunks)


collection_name = "road_traffic_regulation"
# 刪除 collection
# client.delete_collection(collection_name=collection_name)
# 建立 Qdrant collection
client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)
# 會 return True

# 將分割後的文檔上傳儲存到 Qdrant 中
# 這裡的 chunks 是一個 Document 對象的列表，每個 Document 對象都包含了分割後的文本內容和元數據。
qdrant = QdrantVectorStore.from_documents(
    chunks,
    embeddings_model,
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    collection_name=collection_name,
)


retriever = qdrant.as_retriever(search_kwargs={"k": 3}) # 取得前 3 個最相關的文檔


prompt = ChatPromptTemplate.from_template('''
請依照 context 裡的資訊來回答問題:
<context>
{context}
</context>
Question: {input}''')

# 建立一個鏈，用於將檢索到的文檔（context）與用戶的查詢合併，
# 並傳遞給 LLM 進行生成答案。
document_chain = create_stuff_documents_chain(model, prompt)

# 建立一個檢索鏈，將檢索器（retriever）與文檔鏈（document_chain）連接起來。
retrieval_chain = create_retrieval_chain(retriever, document_chain)


response_1 = retrieval_chain.invoke({"input": "汽車可以行駛在慢車道嗎？"})
print(response_1['answer'])


response_2 = retrieval_chain.invoke({"input": "慢車有哪幾種？"})
print(response_2['answer'])

# print(response['context'][0].model_dump_json(exclude_none=True, indent=4))


response_3 = retrieval_chain.invoke({"input": "轉彎時有哪些規定"})
print(response_3['answer'])





# 每分鐘權杖數速率限制：1k
# Q1: 汽車可以行駛在慢車道嗎？
# Q2: 慢車有哪幾種？

# test 1
# chunk_size=300,
# chunk_overlap=120,
# k = 3
'''Q1
{'input': '汽車可以行駛在慢車道嗎？',
 'context': [Document(metadata={'producer': 'Aspose.Words for .NET 24.5.0', 'creator': 'Microsoft Office Word', 'creationdate': '2020-09-27T12:01:00+00:00', 'title': '道路交通安全規則', 'author': '全國法規資料庫', 'moddate': '2025-01-22T03:11:00+00:00', 'source': 'docs/RoadTrafficRegu.pdf', 'total_pages': 62, 'page': 57, 'page_label': '58', '_id': '5c9f5872-0fdb-4b7d-a25d-84d152808e45', '_collection_name': 'road_traffic_regulation'}, page_content='3   慢車行駛之車道，應依標誌或標線之規定行駛；無標誌或標線者，應依下列規定行駛：\n一、應在劃設之慢車道上靠右順序行駛，在未劃設慢車道之道路，應靠右側路邊行駛。但公路主\n管機關、市區道路主管機關或警察機關對行駛地區、路線或時間有特別規定者，應依其規定。\n二、單行道道路應在最左、右側車道行駛。\n三、不得侵入快車道或人行道行駛。\n四、不得在禁止穿越地段穿越道路。\n4   慢車在同一車道行駛時，後車與前車之間應保持隨時可以煞停之距離；變換車道時，應讓直行車\n先行，並應注意安全之距離。\n5   慢車行駛時，駕駛人應注意車前狀況及與他車行駛間隔，並隨時採取必要之安全措施。\n第 124-1 條'),
  Document(metadata={'producer': 'Aspose.Words for .NET 24.5.0', 'creator': 'Microsoft Office Word', 'creationdate': '2020-09-27T12:01:00+00:00', 'title': '道路交通安全規則', 'author': '全國法規資料庫', 'moddate': '2025-01-22T03:11:00+00:00', 'source': 'docs/RoadTrafficRegu.pdf', 'total_pages': 62, 'page': 46, 'page_label': '47', '_id': '9da4c285-fce8-4088-af56-d3f4c7ff940b', '_collection_name': 'road_traffic_regulation'}, page_content='一、均應在遵行車道內行駛。\n二、在劃有分向限制線之路段，不得駛入來車之車道內。\n三、在劃有行車分向線之路段，超車時得駛越，但不能並行競駛。\n四、除準備停車或臨時停車外，不得駛出路面邊線。\n2   汽車在設有慢車道之雙向二車道，除應依前項各款規定行駛外，於快慢車道間變換車道時，應顯\n示方向燈，讓直行車先行，並注意安全距離。\n第 98 條\n1   汽車在同向二車道以上之道路（車道數計算，不含車種專用車道、機車優先道及慢車道） ，除應依\n標誌或標線之指示行駛外，並應遵守下列規定：\n一、大型汽車在同向三車道以上之道路，除準備左轉彎外，不得在內側車道行駛。'),
  Document(metadata={'producer': 'Aspose.Words for .NET 24.5.0', 'creator': 'Microsoft Office Word', 'creationdate': '2020-09-27T12:01:00+00:00', 'title': '道路交通安全規則', 'author': '全國法規資料庫', 'moddate': '2025-01-22T03:11:00+00:00', 'source': 'docs/RoadTrafficRegu.pdf', 'total_pages': 62, 'page': 46, 'page_label': '47', '_id': 'ec07c049-558f-4066-9e72-f8d174e0f795', '_collection_name': 'road_traffic_regulation'}, page_content='2   四輪以上汽車及大型重型機車在劃有快慢車道分隔線之道路行駛，除起駛、準備轉彎、準備停車\n或臨時停車，不得行駛慢車道。但設有快慢車道分隔島之道路不在此限。\n第 96 條\n汽車在單行道行駛時，應在快車道上按遵行方向順序行駛，劃有路面邊線者，除起駛、準備停車\n或臨時停車外，不得駛出路面邊線。\n第 97 條\n1   汽車在未劃設慢車道之雙向二車道行駛時，應依下列規定：\n一、均應在遵行車道內行駛。\n二、在劃有分向限制線之路段，不得駛入來車之車道內。\n三、在劃有行車分向線之路段，超車時得駛越，但不能並行競駛。\n四、除準備停車或臨時停車外，不得駛出路面邊線。')],
 'answer': '根據提供的資訊，汽車在劃有快慢車道分隔線的道路上，除非是起駛、準備轉彎、準備停車或臨時停車，否則不得行駛慢車道。因此，汽車一般情況下是不可以行駛在慢車道的。'}
'''
'''
{'input': '慢車有哪幾種？',
 'context': [Document(metadata={'producer': 'Aspose.Words for .NET 24.5.0', 'creator': 'Microsoft Office Word', 'creationdate': '2020-09-27T12:01:00+00:00', 'title': '道路交通安全規則', 'author': '全國法規資料庫', 'moddate': '2025-01-22T03:11:00+00:00', 'source': 'docs/RoadTrafficRegu.pdf', 'total_pages': 62, 'page': 2, 'page_label': '3', '_id': 'c09b13d1-6983-4ebc-8e43-8c37d978a331', '_collection_name': 'road_traffic_regulation'}, page_content='（三）前二目三輪機車以車輪為前一後二或前二後一對稱型式排列之機車為限。\n第 4 條\n汽車依其使用目的，分為下列二類：\n一、自用：機關、學校、團體、公司、行號或個人自用而非經營客貨運之車輛。\n二、營業：汽車運輸業以經營客貨貨運為目的之車輛。\n第 5 條\n汽車駕駛人分類如下：\n一、職業駕駛人：指以駕駛汽車為職業者。\n二、普通駕駛人：指以駕駛自用車而非駕駛汽車為職業者。\n第 6 條\n慢車種類及名稱如下：'),
  Document(metadata={'producer': 'Aspose.Words for .NET 24.5.0', 'creator': 'Microsoft Office Word', 'creationdate': '2020-09-27T12:01:00+00:00', 'title': '道路交通安全規則', 'author': '全國法規資料庫', 'moddate': '2025-01-22T03:11:00+00:00', 'source': 'docs/RoadTrafficRegu.pdf', 'total_pages': 62, 'page': 3, 'page_label': '4', '_id': '619938cf-deb6-48ef-b563-03108d1104c1', '_collection_name': 'road_traffic_regulation'}, page_content='一、自行車：\n（一）腳踏自行車。\n（二）電動輔助自行車：指經型式審驗合格，以人力為主，電力為輔，最大行駛速率在每小時二\n十五公里以下，且車重在四十公斤以下之二輪車輛。\n（三）微型電動二輪車：指經型式審驗合格，以電力為主，最大行駛速率在每小時二十五公里以\n下，且車重不含電池在四十公斤以下或車重含電池在六十公斤以下之二輪車輛。\n二、其他慢車：\n（一）人力行駛車輛：指客、貨車、手拉（推）貨車等。包含以人力為主、電力為輔，最大行駛\n速率在每小時二十五公里以下，且行駛於指定路段之慢車。\n（二）獸力行駛車輛：指牛車、馬車等。'),
  Document(metadata={'producer': 'Aspose.Words for .NET 24.5.0', 'creator': 'Microsoft Office Word', 'creationdate': '2020-09-27T12:01:00+00:00', 'title': '道路交通安全規則', 'author': '全國法規資料庫', 'moddate': '2025-01-22T03:11:00+00:00', 'source': 'docs/RoadTrafficRegu.pdf', 'total_pages': 62, 'page': 55, 'page_label': '56', '_id': '84c49867-aebb-4d96-a2a4-5abadc3daa9b', '_collection_name': 'road_traffic_regulation'}, page_content='（刪除）\n第 118 條\n（刪除）\n第 119 條\n1   慢車不得擅自變更裝置，並應保持煞車、鈴號、燈光及反光裝置等安全設備之良好與完整。\n2   電動輔助自行車及微型電動二輪車之安全設備，應符合電動輔助自行車及微型電動二輪車安全檢\n測基準，不得擅自增、減、變更電子控制裝置或原有規格。\n3   其他慢車，其安全設備應符合直轄市、縣（市）政府依道路交通管理處罰條例第六十九條第三項、\n第四項授權另定之管理辦法規定。\n4   慢車擅自加裝補助引擎或馬達行駛者，依汽車之拼裝車輛處理。')],
 'answer': '慢車的種類及名稱如下：\n\n一、自行車：\n1. 腳踏自行車。\n2. 電動輔助自行車：以人力為主，電力為輔，最大行駛速率在每小時二十五公里以下，且車重在四十公斤以下之二輪車輛。\n3. 微型電動二輪車：以電力為主，最大行駛速率在每小時二十五公里以下，且車重不含電池在四十公斤以下或車重含電池在六十公斤以下之二輪車輛。\n\n二、其他慢車：\n1. 人力行駛車輛：包括客、貨車、手拉（推）貨車等，以人力為主、電力為輔，最大行駛速率在每小時二十五公里以下，且行駛於指定路段之慢車。\n2. 獸力行駛車輛：如牛車、馬車等。'}
'''
'''Q2-answer
慢車的種類及名稱如下：

一、自行車：
1. 腳踏自行車。
2. 電動輔助自行車：以人力為主，電力為輔，最大行駛速率在每小時二十五公里以下，且車重在四十公斤以下之二輪車輛。
3. 微型電動二輪車：以電力為主，最大行駛速率在每小時二十五公里以下，且車重不含電池在四十公斤以下或車重含電池在六十公斤以下之二輪車輛。

二、其他慢車：
1. 人力行駛車輛：包括客、貨車、手拉（推）貨車等，以人力為主、電力為輔，最大行駛速率在每小時二十五公里以下，且行駛於指定路段之慢車。
2. 獸力行駛車輛：如牛車、馬車等。
'''
# 少了 3. 個人行動器具：指設計承載一人，以電力為主，最大行駛速率在每小時二十五公里以下之自平衡或立式器具。


# test 2
# chunk_size=300,
# chunk_overlap=60,
# k = 3
'''
{'input': '汽車可以行駛在慢車道嗎？',
 'context': [Document(metadata={'producer': 'Aspose.Words for .NET 24.5.0', 'creator': 'Microsoft Office Word', 'creationdate': '2020-09-27T12:01:00+00:00', 'title': '道路交通安全規則', 'author': '全國法規資料庫', 'moddate': '2025-01-22T03:11:00+00:00', 'source': 'docs/RoadTrafficRegu.pdf', 'total_pages': 62, 'page': 46, 'page_label': '47', '_id': '3f43533e-e9fb-4b66-9dde-f329841cf195', '_collection_name': 'road_traffic_regulation'}, page_content='三、在劃有行車分向線之路段，超車時得駛越，但不能並行競駛。\n四、除準備停車或臨時停車外，不得駛出路面邊線。\n2   汽車在設有慢車道之雙向二車道，除應依前項各款規定行駛外，於快慢車道間變換車道時，應顯\n示方向燈，讓直行車先行，並注意安全距離。\n第 98 條\n1   汽車在同向二車道以上之道路（車道數計算，不含車種專用車道、機車優先道及慢車道） ，除應依\n標誌或標線之指示行駛外，並應遵守下列規定：\n一、大型汽車在同向三車道以上之道路，除準備左轉彎外，不得在內側車道行駛。\n二、小型汽車內外側車道均可行駛，行駛速度較慢時，應在外側車道行駛，但不得任意變換車道\n行駛。'),
  Document(metadata={'producer': 'Aspose.Words for .NET 24.5.0', 'creator': 'Microsoft Office Word', 'creationdate': '2020-09-27T12:01:00+00:00', 'title': '道路交通安全規則', 'author': '全國法規資料庫', 'moddate': '2025-01-22T03:11:00+00:00', 'source': 'docs/RoadTrafficRegu.pdf', 'total_pages': 62, 'page': 57, 'page_label': '58', '_id': '57a631b0-1b90-4588-8ac0-154c5ebf9c93', '_collection_name': 'road_traffic_regulation'}, page_content='一、應在劃設之慢車道上靠右順序行駛，在未劃設慢車道之道路，應靠右側路邊行駛。但公路主\n管機關、市區道路主管機關或警察機關對行駛地區、路線或時間有特別規定者，應依其規定。\n二、單行道道路應在最左、右側車道行駛。\n三、不得侵入快車道或人行道行駛。\n四、不得在禁止穿越地段穿越道路。\n4   慢車在同一車道行駛時，後車與前車之間應保持隨時可以煞停之距離；變換車道時，應讓直行車\n先行，並應注意安全之距離。\n5   慢車行駛時，駕駛人應注意車前狀況及與他車行駛間隔，並隨時採取必要之安全措施。\n第 124-1 條\n公路主管機關、市區道路主管機關或警察機關得在不妨礙通行或行車安全無虞之原則，於人行道'),
  Document(metadata={'producer': 'Aspose.Words for .NET 24.5.0', 'creator': 'Microsoft Office Word', 'creationdate': '2020-09-27T12:01:00+00:00', 'title': '道路交通安全規則', 'author': '全國法規資料庫', 'moddate': '2025-01-22T03:11:00+00:00', 'source': 'docs/RoadTrafficRegu.pdf', 'total_pages': 62, 'page': 46, 'page_label': '47', '_id': '551346a3-b959-4bbd-9cbc-7aafe706fe4a', '_collection_name': 'road_traffic_regulation'}, page_content='2   四輪以上汽車及大型重型機車在劃有快慢車道分隔線之道路行駛，除起駛、準備轉彎、準備停車\n或臨時停車，不得行駛慢車道。但設有快慢車道分隔島之道路不在此限。\n第 96 條\n汽車在單行道行駛時，應在快車道上按遵行方向順序行駛，劃有路面邊線者，除起駛、準備停車\n或臨時停車外，不得駛出路面邊線。\n第 97 條\n1   汽車在未劃設慢車道之雙向二車道行駛時，應依下列規定：\n一、均應在遵行車道內行駛。\n二、在劃有分向限制線之路段，不得駛入來車之車道內。\n三、在劃有行車分向線之路段，超車時得駛越，但不能並行競駛。\n四、除準備停車或臨時停車外，不得駛出路面邊線。')],
 'answer': '根據提供的資訊，四輪以上汽車及大型重型機車在劃有快慢車道分隔線之道路行駛時，除起駛、準備轉彎、準備停車或臨時停車外，不得行駛慢車道。因此，汽車在一般情況下是不可以行駛在慢車道的。'}
'''
'''
{'input': '慢車有哪幾種？',
 'context': [Document(metadata={'producer': 'Aspose.Words for .NET 24.5.0', 'creator': 'Microsoft Office Word', 'creationdate': '2020-09-27T12:01:00+00:00', 'title': '道路交通安全規則', 'author': '全國法規資料庫', 'moddate': '2025-01-22T03:11:00+00:00', 'source': 'docs/RoadTrafficRegu.pdf', 'total_pages': 62, 'page': 2, 'page_label': '3', '_id': 'b523b06e-989b-453d-b7c6-b4d15cdd1e7a', '_collection_name': 'road_traffic_regulation'}, page_content='2.小型輕型機車：電動機車之馬達及控制器最大輸出馬力小於一點三四馬力（電動機功率小於\n一千瓦） ，且最大行駛速率在每小時四十五公里以下之二輪或三輪機車。\n（三）前二目三輪機車以車輪為前一後二或前二後一對稱型式排列之機車為限。\n第 4 條\n汽車依其使用目的，分為下列二類：\n一、自用：機關、學校、團體、公司、行號或個人自用而非經營客貨運之車輛。\n二、營業：汽車運輸業以經營客貨貨運為目的之車輛。\n第 5 條\n汽車駕駛人分類如下：\n一、職業駕駛人：指以駕駛汽車為職業者。\n二、普通駕駛人：指以駕駛自用車而非駕駛汽車為職業者。\n第 6 條\n慢車種類及名稱如下：'),
  Document(metadata={'producer': 'Aspose.Words for .NET 24.5.0', 'creator': 'Microsoft Office Word', 'creationdate': '2020-09-27T12:01:00+00:00', 'title': '道路交通安全規則', 'author': '全國法規資料庫', 'moddate': '2025-01-22T03:11:00+00:00', 'source': 'docs/RoadTrafficRegu.pdf', 'total_pages': 62, 'page': 3, 'page_label': '4', '_id': '1d273390-852f-464e-a848-4f1a800c8e25', '_collection_name': 'road_traffic_regulation'}, page_content='一、自行車：\n（一）腳踏自行車。\n（二）電動輔助自行車：指經型式審驗合格，以人力為主，電力為輔，最大行駛速率在每小時二\n十五公里以下，且車重在四十公斤以下之二輪車輛。\n（三）微型電動二輪車：指經型式審驗合格，以電力為主，最大行駛速率在每小時二十五公里以\n下，且車重不含電池在四十公斤以下或車重含電池在六十公斤以下之二輪車輛。\n二、其他慢車：\n（一）人力行駛車輛：指客、貨車、手拉（推）貨車等。包含以人力為主、電力為輔，最大行駛\n速率在每小時二十五公里以下，且行駛於指定路段之慢車。\n（二）獸力行駛車輛：指牛車、馬車等。'),
  Document(metadata={'producer': 'Aspose.Words for .NET 24.5.0', 'creator': 'Microsoft Office Word', 'creationdate': '2020-09-27T12:01:00+00:00', 'title': '道路交通安全規則', 'author': '全國法規資料庫', 'moddate': '2025-01-22T03:11:00+00:00', 'source': 'docs/RoadTrafficRegu.pdf', 'total_pages': 62, 'page': 55, 'page_label': '56', '_id': '02aced64-d2d2-4536-bdaa-0616ce3478d8', '_collection_name': 'road_traffic_regulation'}, page_content='測基準，不得擅自增、減、變更電子控制裝置或原有規格。\n3   其他慢車，其安全設備應符合直轄市、縣（市）政府依道路交通管理處罰條例第六十九條第三項、\n第四項授權另定之管理辦法規定。\n4   慢車擅自加裝補助引擎或馬達行駛者，依汽車之拼裝車輛處理。')],
 'answer': '慢車的種類及名稱如下：\n\n一、自行車：\n1. 腳踏自行車。\n2. 電動輔助自行車：以人力為主，電力為輔，最大行駛速率在每小時二十五公里以下，且車重在四十公斤以下之二輪車輛。\n3. 微型電動二輪車：以電力為主，最大行駛速率在每小時二十五公里以下，且車重不含電池在四十公斤以下或車重含電池在六十公斤以下之二輪車輛。\n\n二、其他慢車：\n1. 人力行駛車輛：如客、貨車、手拉（推）貨車等，包含以人力為主、電力為輔，最大行駛速率在每小時二十五公里以下，且行駛於指定路段之慢車。\n2. 獸力行駛車輛：如牛車、馬車等。'}
'''
'''Q2-answer
慢車的種類及名稱如下：

一、自行車：
1. 腳踏自行車。
2. 電動輔助自行車：以人力為主，電力為輔，最大行駛速率在每小時二十五公里以下，且車重在四十公斤以下之二輪車輛。
3. 微型電動二輪車：以電力為主，最大行駛速率在每小時二十五公里以下，且車重不含電池在四十公斤以下或車重含電池在六十公斤以下之二輪車輛。

二、其他慢車：
1. 人力行駛車輛：如客、貨車、手拉（推）貨車等，包含以人力為主、電力為輔，最大行駛速率在每小時二十五公里以下，且行駛於指定路段之慢車。
2. 獸力行駛車輛：如牛車、馬車等。
'''


# test 3
# chunk_size=320,
# chunk_overlap=80,
# k = 3
'''
{'input': '汽車可以行駛在慢車道嗎？',
 'context': [Document(metadata={'producer': 'Aspose.Words for .NET 24.5.0', 'creator': 'Microsoft Office Word', 'creationdate': '2020-09-27T12:01:00+00:00', 'title': '道路交通安全規則', 'author': '全國法規資料庫', 'moddate': '2025-01-22T03:11:00+00:00', 'source': 'docs/RoadTrafficRegu.pdf', 'total_pages': 62, 'page': 57, 'page_label': '58', '_id': '41532399-ee42-4b7d-929a-f9241d190c82', '_collection_name': 'road_traffic_regulation'}, page_content='一、應在劃設之慢車道上靠右順序行駛，在未劃設慢車道之道路，應靠右側路邊行駛。但公路主\n管機關、市區道路主管機關或警察機關對行駛地區、路線或時間有特別規定者，應依其規定。\n二、單行道道路應在最左、右側車道行駛。\n三、不得侵入快車道或人行道行駛。\n四、不得在禁止穿越地段穿越道路。\n4   慢車在同一車道行駛時，後車與前車之間應保持隨時可以煞停之距離；變換車道時，應讓直行車\n先行，並應注意安全之距離。\n5   慢車行駛時，駕駛人應注意車前狀況及與他車行駛間隔，並隨時採取必要之安全措施。\n第 124-1 條\n公路主管機關、市區道路主管機關或警察機關得在不妨礙通行或行車安全無虞之原則，於人行道'),
  Document(metadata={'producer': 'Aspose.Words for .NET 24.5.0', 'creator': 'Microsoft Office Word', 'creationdate': '2020-09-27T12:01:00+00:00', 'title': '道路交通安全規則', 'author': '全國法規資料庫', 'moddate': '2025-01-22T03:11:00+00:00', 'source': 'docs/RoadTrafficRegu.pdf', 'total_pages': 62, 'page': 46, 'page_label': '47', '_id': 'ba6ef6c0-f48b-4669-87ad-9caec927fa33', '_collection_name': 'road_traffic_regulation'}, page_content='二、在劃有分向限制線之路段，不得駛入來車之車道內。\n三、在劃有行車分向線之路段，超車時得駛越，但不能並行競駛。\n四、除準備停車或臨時停車外，不得駛出路面邊線。\n2   汽車在設有慢車道之雙向二車道，除應依前項各款規定行駛外，於快慢車道間變換車道時，應顯\n示方向燈，讓直行車先行，並注意安全距離。\n第 98 條\n1   汽車在同向二車道以上之道路（車道數計算，不含車種專用車道、機車優先道及慢車道） ，除應依\n標誌或標線之指示行駛外，並應遵守下列規定：\n一、大型汽車在同向三車道以上之道路，除準備左轉彎外，不得在內側車道行駛。\n二、小型汽車內外側車道均可行駛，行駛速度較慢時，應在外側車道行駛，但不得任意變換車道\n行駛。'),
  Document(metadata={'producer': 'Aspose.Words for .NET 24.5.0', 'creator': 'Microsoft Office Word', 'creationdate': '2020-09-27T12:01:00+00:00', 'title': '道路交通安全規則', 'author': '全國法規資料庫', 'moddate': '2025-01-22T03:11:00+00:00', 'source': 'docs/RoadTrafficRegu.pdf', 'total_pages': 62, 'page': 46, 'page_label': '47', '_id': '5b738110-4ba1-4986-adc2-bfcb6ca5593b', '_collection_name': 'road_traffic_regulation'}, page_content='2   四輪以上汽車及大型重型機車在劃有快慢車道分隔線之道路行駛，除起駛、準備轉彎、準備停車\n或臨時停車，不得行駛慢車道。但設有快慢車道分隔島之道路不在此限。\n第 96 條\n汽車在單行道行駛時，應在快車道上按遵行方向順序行駛，劃有路面邊線者，除起駛、準備停車\n或臨時停車外，不得駛出路面邊線。\n第 97 條\n1   汽車在未劃設慢車道之雙向二車道行駛時，應依下列規定：\n一、均應在遵行車道內行駛。\n二、在劃有分向限制線之路段，不得駛入來車之車道內。\n三、在劃有行車分向線之路段，超車時得駛越，但不能並行競駛。\n四、除準備停車或臨時停車外，不得駛出路面邊線。')],
 'answer': '根據提供的資訊，四輪以上汽車及大型重型機車在劃有快慢車道分隔線之道路行駛時，除起駛、準備轉彎、準備停車或臨時停車外，不得行駛慢車道。因此，汽車一般情況下是不可以行駛在慢車道的。'}
'''
'''
{'input': '慢車有哪幾種？',
 'context': [Document(metadata={'producer': 'Aspose.Words for .NET 24.5.0', 'creator': 'Microsoft Office Word', 'creationdate': '2020-09-27T12:01:00+00:00', 'title': '道路交通安全規則', 'author': '全國法規資料庫', 'moddate': '2025-01-22T03:11:00+00:00', 'source': 'docs/RoadTrafficRegu.pdf', 'total_pages': 62, 'page': 2, 'page_label': '3', '_id': 'd8ab4d1d-23b6-4d2b-a26b-e32edf03a8bc', '_collection_name': 'road_traffic_regulation'}, page_content='2.小型輕型機車：電動機車之馬達及控制器最大輸出馬力小於一點三四馬力（電動機功率小於\n一千瓦） ，且最大行駛速率在每小時四十五公里以下之二輪或三輪機車。\n（三）前二目三輪機車以車輪為前一後二或前二後一對稱型式排列之機車為限。\n第 4 條\n汽車依其使用目的，分為下列二類：\n一、自用：機關、學校、團體、公司、行號或個人自用而非經營客貨運之車輛。\n二、營業：汽車運輸業以經營客貨貨運為目的之車輛。\n第 5 條\n汽車駕駛人分類如下：\n一、職業駕駛人：指以駕駛汽車為職業者。\n二、普通駕駛人：指以駕駛自用車而非駕駛汽車為職業者。\n第 6 條\n慢車種類及名稱如下：'),
  Document(metadata={'producer': 'Aspose.Words for .NET 24.5.0', 'creator': 'Microsoft Office Word', 'creationdate': '2020-09-27T12:01:00+00:00', 'title': '道路交通安全規則', 'author': '全國法規資料庫', 'moddate': '2025-01-22T03:11:00+00:00', 'source': 'docs/RoadTrafficRegu.pdf', 'total_pages': 62, 'page': 3, 'page_label': '4', '_id': 'ba4fb6d8-1172-4754-bba2-3af1a7c17317', '_collection_name': 'road_traffic_regulation'}, page_content='一、自行車：\n（一）腳踏自行車。\n（二）電動輔助自行車：指經型式審驗合格，以人力為主，電力為輔，最大行駛速率在每小時二\n十五公里以下，且車重在四十公斤以下之二輪車輛。\n（三）微型電動二輪車：指經型式審驗合格，以電力為主，最大行駛速率在每小時二十五公里以\n下，且車重不含電池在四十公斤以下或車重含電池在六十公斤以下之二輪車輛。\n二、其他慢車：\n（一）人力行駛車輛：指客、貨車、手拉（推）貨車等。包含以人力為主、電力為輔，最大行駛\n速率在每小時二十五公里以下，且行駛於指定路段之慢車。\n（二）獸力行駛車輛：指牛車、馬車等。\n（三）個人行動器具：指設計承載一人，以電力為主，最大行駛速率在每小時二十五公里以下之\n自平衡或立式器具。\n第 7 條'),
  Document(metadata={'producer': 'Aspose.Words for .NET 24.5.0', 'creator': 'Microsoft Office Word', 'creationdate': '2020-09-27T12:01:00+00:00', 'title': '道路交通安全規則', 'author': '全國法規資料庫', 'moddate': '2025-01-22T03:11:00+00:00', 'source': 'docs/RoadTrafficRegu.pdf', 'total_pages': 62, 'page': 55, 'page_label': '56', '_id': '4b4254fe-6b46-4d83-96db-dc2a250d66ec', '_collection_name': 'road_traffic_regulation'}, page_content='2   電動輔助自行車及微型電動二輪車之安全設備，應符合電動輔助自行車及微型電動二輪車安全檢\n測基準，不得擅自增、減、變更電子控制裝置或原有規格。\n3   其他慢車，其安全設備應符合直轄市、縣（市）政府依道路交通管理處罰條例第六十九條第三項、\n第四項授權另定之管理辦法規定。\n4   慢車擅自加裝補助引擎或馬達行駛者，依汽車之拼裝車輛處理。')],
 'answer': '慢車的種類及名稱如下：\n\n一、自行車：\n1. 腳踏自行車。\n2. 電動輔助自行車：以人力為主，電力為輔，最大行駛速率在每小時二十五公里以下，且車重在四十公斤以下之二輪車輛。\n3. 微型電動二輪車：以電力為主，最大行駛速率在每小時二十五公里以下，且車重不含電池在四十公斤以下或車重含電池在六十公斤以下之二輪車輛。\n\n二、其他慢車：\n1. 人力行駛車輛：如客、貨車、手拉（推）貨車等，包含以人力為主、電力為輔，最大行駛速率在每小時二十五公里以下，且行駛於指定路段之慢車。\n2. 獸力行駛車輛：如牛車、馬車等。\n3. 個人行動器具：設計承載一人，以電力為主，最大行駛速率在每小時二十五公里以下之自平衡或立式器具。'}
'''
'''Q2-answer: complete answer
慢車的種類及名稱如下：

一、自行車：
1. 腳踏自行車。
2. 電動輔助自行車：以人力為主，電力為輔，最大行駛速率在每小時二十五公里以下，且車重在四十公斤以下之二輪車輛。
3. 微型電動二輪車：以電力為主，最大行駛速率在每小時二十五公里以下，且車重不含電池在四十公斤以下或車重含電池在六十公斤以下之二輪車輛。

二、其他慢車：
1. 人力行駛車輛：如客、貨車、手拉（推）貨車等，包含以人力為主、電力為輔，最大行駛速率在每小時二十五公里以下，且行駛於指定路段之慢車。
2. 獸力行駛車輛：如牛車、馬車等。
3. 個人行動器具：設計承載一人，以電力為主，最大行駛速率在每小時二十五公里以下之自平衡或立式器具。
'''






# test 4
# chunk_size=400,
# chunk_overlap=120,
# k = 2
'''
{'input': '汽車可以行駛在慢車道嗎？',
 'context': [Document(metadata={'producer': 'Aspose.Words for .NET 24.5.0', 'creator': 'Microsoft Office Word', 'creationdate': '2020-09-27T12:01:00+00:00', 'title': '道路交通安全規則', 'author': '全國法規資料庫', 'moddate': '2025-01-22T03:11:00+00:00', 'source': 'docs/RoadTrafficRegu.pdf', 'total_pages': 62, 'page': 46, 'page_label': '47', '_id': '3210eaec-0fc9-4208-a380-c3e88e277748', '_collection_name': 'road_traffic_regulation'}, page_content='2   四輪以上汽車及大型重型機車在劃有快慢車道分隔線之道路行駛，除起駛、準備轉彎、準備停車\n或臨時停車，不得行駛慢車道。但設有快慢車道分隔島之道路不在此限。\n第 96 條\n汽車在單行道行駛時，應在快車道上按遵行方向順序行駛，劃有路面邊線者，除起駛、準備停車\n或臨時停車外，不得駛出路面邊線。\n第 97 條\n1   汽車在未劃設慢車道之雙向二車道行駛時，應依下列規定：\n一、均應在遵行車道內行駛。\n二、在劃有分向限制線之路段，不得駛入來車之車道內。\n三、在劃有行車分向線之路段，超車時得駛越，但不能並行競駛。\n四、除準備停車或臨時停車外，不得駛出路面邊線。\n2   汽車在設有慢車道之雙向二車道，除應依前項各款規定行駛外，於快慢車道間變換車道時，應顯\n示方向燈，讓直行車先行，並注意安全距離。\n第 98 條'),
  Document(metadata={'producer': 'Aspose.Words for .NET 24.5.0', 'creator': 'Microsoft Office Word', 'creationdate': '2020-09-27T12:01:00+00:00', 'title': '道路交通安全規則', 'author': '全國法規資料庫', 'moddate': '2025-01-22T03:11:00+00:00', 'source': 'docs/RoadTrafficRegu.pdf', 'total_pages': 62, 'page': 57, 'page_label': '58', '_id': 'ba9566d4-8250-4790-9488-32b621b0a1da', '_collection_name': 'road_traffic_regulation'}, page_content='管機關、市區道路主管機關或警察機關對行駛地區、路線或時間有特別規定者，應依其規定。\n二、單行道道路應在最左、右側車道行駛。\n三、不得侵入快車道或人行道行駛。\n四、不得在禁止穿越地段穿越道路。\n4   慢車在同一車道行駛時，後車與前車之間應保持隨時可以煞停之距離；變換車道時，應讓直行車\n先行，並應注意安全之距離。\n5   慢車行駛時，駕駛人應注意車前狀況及與他車行駛間隔，並隨時採取必要之安全措施。\n第 124-1 條\n公路主管機關、市區道路主管機關或警察機關得在不妨礙通行或行車安全無虞之原則，於人行道\n設置必要之標誌或標線供慢車行駛。慢車應依標誌或標線之指示行駛，並應讓行人優先通行。\n第 125 條\n1   慢車行駛至交岔路口，其行進或轉彎，應依標誌、標線或號誌之規定行駛，無標誌、標線或號誌\n者，應依第一百零二條及下列規定行駛：\n一、直行時，應順其遵行方向直線通過，不得蛇行搶先。')],
 'answer': '根據提供的資訊，四輪以上汽車在劃有快慢車道分隔線的道路上，除起駛、準備轉彎、準備停車或臨時停車外，不得行駛慢車道。因此，汽車一般情況下是不可以行駛在慢車道的。'}
'''
'''
{'input': '慢車有哪幾種？',
 'context': [Document(metadata={'producer': 'Aspose.Words for .NET 24.5.0', 'creator': 'Microsoft Office Word', 'creationdate': '2020-09-27T12:01:00+00:00', 'title': '道路交通安全規則', 'author': '全國法規資料庫', 'moddate': '2025-01-22T03:11:00+00:00', 'source': 'docs/RoadTrafficRegu.pdf', 'total_pages': 62, 'page': 2, 'page_label': '3', '_id': '41dc7801-29c4-454a-ba85-c33bc04a751d', '_collection_name': 'road_traffic_regulation'}, page_content='（三）前二目三輪機車以車輪為前一後二或前二後一對稱型式排列之機車為限。\n第 4 條\n汽車依其使用目的，分為下列二類：\n一、自用：機關、學校、團體、公司、行號或個人自用而非經營客貨運之車輛。\n二、營業：汽車運輸業以經營客貨貨運為目的之車輛。\n第 5 條\n汽車駕駛人分類如下：\n一、職業駕駛人：指以駕駛汽車為職業者。\n二、普通駕駛人：指以駕駛自用車而非駕駛汽車為職業者。\n第 6 條\n慢車種類及名稱如下：'),
  Document(metadata={'producer': 'Aspose.Words for .NET 24.5.0', 'creator': 'Microsoft Office Word', 'creationdate': '2020-09-27T12:01:00+00:00', 'title': '道路交通安全規則', 'author': '全國法規資料庫', 'moddate': '2025-01-22T03:11:00+00:00', 'source': 'docs/RoadTrafficRegu.pdf', 'total_pages': 62, 'page': 55, 'page_label': '56', '_id': '6a9cf0e8-f63c-4a64-842e-e0b26a9355e4', '_collection_name': 'road_traffic_regulation'}, page_content='上，不致上下左右晃動，且不可遮蔽視線。\n第 116 條\n各直轄市、縣（市）政府因地方交通發展，對各種慢車認為須予淘汰者，報請行政院核定後公告\n禁止行駛。\n第 117 條\n（刪除）\n第 118 條\n（刪除）\n第 119 條\n1   慢車不得擅自變更裝置，並應保持煞車、鈴號、燈光及反光裝置等安全設備之良好與完整。\n2   電動輔助自行車及微型電動二輪車之安全設備，應符合電動輔助自行車及微型電動二輪車安全檢\n測基準，不得擅自增、減、變更電子控制裝置或原有規格。\n3   其他慢車，其安全設備應符合直轄市、縣（市）政府依道路交通管理處罰條例第六十九條第三項、\n第四項授權另定之管理辦法規定。\n4   慢車擅自加裝補助引擎或馬達行駛者，依汽車之拼裝車輛處理。')],
 'answer': '根據提供的上下文，慢車的種類及名稱並未具體列出，因此無法直接回答慢車的具體種類。上下文中提到的慢車主要是指在交通管理中需要遵循的安全規定和管理辦法。如果需要了解慢車的具體種類，可能需要查閱相關的法律法規或交通管理文件。'}
'''


# test 5
# chunk_size=900,
# chunk_overlap=200,
# k = 1
'''
{'input': '汽車可以行駛在慢車道嗎？',
 'context': [Document(metadata={'producer': 'Aspose.Words for .NET 24.5.0', 'creator': 'Microsoft Office Word', 'creationdate': '2020-09-27T12:01:00+00:00', 'title': '道路交通安全規則', 'author': '全國法規資料庫', 'moddate': '2025-01-22T03:11:00+00:00', 'source': 'docs/RoadTrafficRegu.pdf', 'total_pages': 62, 'page': 46, 'page_label': '47', '_id': '2a117d0f-da45-4a22-8c33-caf7251535c2', '_collection_name': 'road_traffic_regulation'}, page_content='2   四輪以上汽車及大型重型機車在劃有快慢車道分隔線之道路行駛，除起駛、準備轉彎、準備停車\n或臨時停車，不得行駛慢車道。但設有快慢車道分隔島之道路不在此限。\n第 96 條\n汽車在單行道行駛時，應在快車道上按遵行方向順序行駛，劃有路面邊線者，除起駛、準備停車\n或臨時停車外，不得駛出路面邊線。\n第 97 條\n1   汽車在未劃設慢車道之雙向二車道行駛時，應依下列規定：\n一、均應在遵行車道內行駛。\n二、在劃有分向限制線之路段，不得駛入來車之車道內。\n三、在劃有行車分向線之路段，超車時得駛越，但不能並行競駛。\n四、除準備停車或臨時停車外，不得駛出路面邊線。\n2   汽車在設有慢車道之雙向二車道，除應依前項各款規定行駛外，於快慢車道間變換車道時，應顯\n示方向燈，讓直行車先行，並注意安全距離。\n第 98 條\n1   汽車在同向二車道以上之道路（車道數計算，不含車種專用車道、機車優先道及慢車道） ，除應依\n標誌或標線之指示行駛外，並應遵守下列規定：\n一、大型汽車在同向三車道以上之道路，除準備左轉彎外，不得在內側車道行駛。\n二、小型汽車內外側車道均可行駛，行駛速度較慢時，應在外側車道行駛，但不得任意變換車道\n行駛。\n三、執行任務中之消防車、救護車、警備車、工程救險車，內外側車道均可行駛。\n四、由同向二車道進入一車道，應讓直行車道之車輛先行，無直行車道者，外車道之車輛應讓內\n車道之車輛先行。但在交通壅塞時，內、外側車道車輛應互為禮讓，逐車交互輪流行駛，並\n保持安全距離及間隔。\n五、除準備停車或臨時停車外，不得駛出路面邊線或跨越兩條車道行駛。\n六、變換車道時，應讓直行車先行，並注意安全距離。\n2   設有左右轉彎專用車道之交岔路口，直行車不得占用轉彎專用車道。\n3   汽車在調撥車道或雙向車道數不同之道路，除依第一項各款規定行駛外，並應依道路交通標誌、\n標線、號誌之指示行駛。\n第 99 條\n1   機車行駛之車道，應依標誌或標線之規定行駛；無標誌或標線者，依下列規定行駛：\n一、在未劃分快慢車道之道路，應在最外側二車道行駛；單行道應在最左、右側車道行駛。')],
 'answer': '根據提供的資訊，四輪以上汽車在劃有快慢車道分隔線的道路上，除非是起駛、準備轉彎、準備停車或臨時停車，否則不得行駛慢車道。因此，汽車一般情況下是不可以行駛在慢車道的。'}
'''
'''
{'input': '慢車有哪幾種？',
 'context': [Document(metadata={'producer': 'Aspose.Words for .NET 24.5.0', 'creator': 'Microsoft Office Word', 'creationdate': '2020-09-27T12:01:00+00:00', 'title': '道路交通安全規則', 'author': '全國法規資料庫', 'moddate': '2025-01-22T03:11:00+00:00', 'source': 'docs/RoadTrafficRegu.pdf', 'total_pages': 62, 'page': 2, 'page_label': '3', '_id': '81a8a8aa-960e-4b60-988a-cf4b3dadf630', '_collection_name': 'road_traffic_regulation'}, page_content='過二十五人。\n（二）代用小客車：小貨車兼供代用客車者，為代用小客車，其載客人數包括駕駛人在內不得超\n過九人。\n五、特種車：\n（一）大型特種車：總重量逾三千五百公斤，或全部座位在十座以上之特種車。\n（二）小型特種車：總重量在三千五百公斤以下，或全部座位在九座以下之特種車。\n六、機車：\n（一）重型機車：\n1.普通重型機車：\n（1）汽缸總排氣量逾五十立方公分且在二百五十立方公分以下之二輪或三輪機車。\n（2）電動機車之馬達及控制器最大輸出馬力逾五馬力且在四十馬力（HP）以下之二輪或三輪機\n車。\n2.大型重型機車：\n（1）汽缸總排氣量逾二百五十立方公分之二輪或三輪機車。\n（2）電動機車之馬達及控制器最大輸出馬力逾四十馬力（HP）之二輪或三輪機車。\n（二）輕型機車：\n1.普通輕型機車：\n（1）汽缸總排氣量在五十立方公分以下之二輪或三輪機車。\n（2）電動機車之馬達及控制器最大輸出馬力在五馬力（HP）以下、一點三四馬力（電動機功率\n一千瓦）以上或最大輸出馬力小於一點三四馬力（電動機功率小於一千瓦） ，且最大行駛速\n率逾每小時四十五公里之二輪或三輪機車。\n2.小型輕型機車：電動機車之馬達及控制器最大輸出馬力小於一點三四馬力（電動機功率小於\n一千瓦） ，且最大行駛速率在每小時四十五公里以下之二輪或三輪機車。\n（三）前二目三輪機車以車輪為前一後二或前二後一對稱型式排列之機車為限。\n第 4 條\n汽車依其使用目的，分為下列二類：\n一、自用：機關、學校、團體、公司、行號或個人自用而非經營客貨運之車輛。\n二、營業：汽車運輸業以經營客貨貨運為目的之車輛。\n第 5 條\n汽車駕駛人分類如下：\n一、職業駕駛人：指以駕駛汽車為職業者。\n二、普通駕駛人：指以駕駛自用車而非駕駛汽車為職業者。\n第 6 條\n慢車種類及名稱如下：')],
 'answer': '根據提供的上下文，並未明確列出慢車的種類及名稱。因此，無法從中獲得具體的慢車種類。如果需要更詳細的資訊，建議查閱相關的交通法規或文件。'}
'''






# Add typing for input
class Question(BaseModel):
    input: str


rag_chain = retrieval_chain.with_types(input_type=Question)