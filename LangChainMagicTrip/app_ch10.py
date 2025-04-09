from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureChatOpenAI,AzureOpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# # 使用 QdrantVectorStore
# from qdrant_client import QdrantClient
# from langchain_qdrant import QdrantVectorStore

# 改用 FAISS
from langchain_community.vectorstores import FAISS


from configparser import ConfigParser
try:
    # Azure AI Foundry 部屬端點目標URI：
    # {AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT_NAME}/embeddings?api-version={AZURE_OPENAI_API_VERSION}
    config = ConfigParser()
    config.read('config.ini', encoding='utf-8')
    AZURE_OPENAI_API_KEY = config.get('Azure', 'OPENAI_KEY')
    AZURE_OPENAI_API_VERSION = config.get('Azure', 'OPENAI_API_VERSION')
    AZURE_OPENAI_ENDPOINT = config.get('Azure', 'OPENAI_ENDPOINT')
    AZURE_OPENAI_DEPLOYMENT_NAME = config.get('Azure', 'OPENAI_DEPLOYMENT_NAME')
    
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME = config.get('Azure', 'OPENAI_EMBEDDING_DEPLOYMENT_NAME')
    AZURE_OPENAI_API_EMBEDDING_VERSION = config.get('Azure', 'OPENAI_API_EMBEDDING_VERSION')
    EMBEDDING_MODEL = config.get('Azure', 'EMBEDDING_MODEL')
    if not all([AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT_NAME]):
        raise Exception("Please provide a valid API key and endpoint")
except:
    print("Please provide a valid API key and endpoint")
    exit()


# 初始化語言模型
generator_llm = AzureChatOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME,
    openai_api_version=AZURE_OPENAI_API_VERSION,
    api_key=AZURE_OPENAI_API_KEY,
)

embedding_llm = AzureOpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME,
    api_key=AZURE_OPENAI_API_KEY,
    openai_api_version=AZURE_OPENAI_API_EMBEDDING_VERSION,
)

# ----- 第一次要把知識文件加入Qdrant 向量資料庫時，執行以下程式碼 -----

# Load PDF文件：pip install pypdf
loader = PyPDFLoader("docs/勞動基準法.pdf")
pages = loader.load_and_split()

# 分割文本
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splits = text_splitter.split_documents(pages)

# # Qdrant向量資料庫
# qdrant = QdrantVectorStore.from_documents(
#     splits,
#     embedding=embedding_llm,
#     url="http://localhost:6333",  # 假設Qdrant運行在本地的6333端口
#     collection_name="km_docs",
# )

# 建立 FAISS 向量資料庫
faiss_vectorstore = FAISS.from_documents(
    splits,
    embedding_llm
)

# 儲存向量資料庫到本地
faiss_vectorstore.save_local("faiss_index")


#---------------------------------------------------------




# ------- 後續查詢時，已有向量資料，請執行以下程式碼 -------

# # Qdrant client
# client = QdrantClient(url="http://localhost:6333")
# collection_name = "km_docs"
# qdrant = QdrantVectorStore(
#         client=client,
#         collection_name=collection_name,
#         embedding=embedding_llm
#     )

# 載入已存在的向量資料庫
faiss_vectorstore0 = FAISS.load_local("FAISS/faiss_index", 
                                      embedding_llm,
                                      allow_dangerous_deserialization=True  # 允許反序列化，請確保資料來源可信
                                      )


# -------------------------------------------------------


# # 設置檢索器
# retriever = qdrant.as_retriever(search_kwargs={"k": 3}) # 檢索前3個最相似的文檔
retriever = faiss_vectorstore.as_retriever(search_kwargs={"k": 3})

# 建立提示樣板
my_template = ChatPromptTemplate.from_template("""你是一位精通台灣勞基法的專家。請根據以下參考資料回答問題：

參考資料：{context}

問題：{question}

專家回答：""")

# 建立 QA Chain
qa_chain = (
    {
        "context": retriever ,
        "question": RunnablePassthrough(),
    }
    | my_template
    | generator_llm
    | StrOutputParser()
)


# 步驟 7: 進行查詢
response = qa_chain.invoke("勞工加班費的計算方式是什麼？")

print(response)
# Requests to the ChatCompletions_Create Operation under Azure OpenAI API 
# version 2025-01-01-preview have exceeded token rate limit 
# of your current AIServices S0 pricing tier. Please retry after 60 seconds. 
# Please go here: https://aka.ms/oai/quotaincrease if you would like to further increase the default rate limit. 
# For Free Account customers, upgrade to Pay as you Go here: https://aka.ms/429TrialUpgrade.