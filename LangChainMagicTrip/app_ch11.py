'''
拉取 Ollama Docker 映像並執行
docker run --name ollama -v ollama:/root/.ollama -p 11434:11434 ollama/ollama
啟動一個名為 "ollama" 的容器
--name ollama
設定容器名稱為 "ollama"
-v ollama:/root/.ollama
將主機上的名為 "ollama" 的資料卷掛載到容器內的路徑 /root/.ollama，
以便儲存和持久化容器內的資料（例如設定檔或模型下載結果）。
-p 11434:11434
將主機的 11434 埠映射到容器的 11434 埠，使你可以透過主機的該埠存取容器內的服務。
ollama/ollama
指定要使用的映像檔（image）為 ollama/ollama。

下載 Meta 的 llama3:8b 模型（以量化後相對較小的模型）並運行
docker exec -it ollama ollama run llama3:8b
在已運行的容器「ollama」內執行一個命令
docker exec 用來在正在運行的容器中執行指令
-it 表示以交互模式啟動容器內的終端（即保持標準輸入打開並附加一個偽終端），方便你即時看到命令的輸出，也可以進行交互。
ollama 是容器名稱，即在這個容器中執行接下來的命令
ollama run llama3:8b：
這是容器內真正要執行的命令。首先調用容器內的 ollama 應用（或 CLI 工具），
run llama3:8b 命令表示讓 ollama 應用運行名為 llama3:8b 的模型（這個模型名稱可能代表特定版本或特定配置的模型）。


安裝 Open WebUI
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
docker run 啟動一個新的容器。
-p 3000:8080 把主機的 3000 埠映射到容器的 8080 埠，使你可以透過主機的 3000 埠訪問容器中的服務。
--add-host=host.docker.internal:host-gateway
將主機內部名稱 host.docker.internal 映射到宿主機 IP（透過 host-gateway），方便容器內部訪問宿主機。
-v open-webui:/app/backend/data
使用名為 open-webui 的資料卷將主機（或 Docker volume）中的數據掛載到容器內的 /app/backend/data，用於持久化存儲資料。
--name open-webui 設定此容器的名字為 open-webui。
--restart always 當容器意外停止時，自動重啟容器，確保服務持續運行。
ghcr.io/open-webui/open-webui:main
指定使用 GitHub Container Registry 上的映像檔 ghcr.io/open-webui/open-webui 並使用 main 標籤（版本）。
綜上，這個命令會在背景啟動一個名為 open-webui 的容器，
將容器內 /app/backend/data 目錄映射到持久化資料卷 open-webui，
並將主機的 3000 埠轉發到容器的 8080 埠，同時設定連接宿主機的 DNS 名稱，
並在意外停止時自動重啟服務。

打開 http://localhost:3000/
Ming
123456789
'''

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureChatOpenAI,AzureOpenAIEmbeddings
from langchain_ollama.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore

import os
from dotenv import dotenv_values
config = dotenv_values(".env")


# 初始化語言模型
# generator_llm = AzureChatOpenAI(
#     azure_endpoint=config.get("AZURE_OPENAI_ENDPOINT"),
#     azure_deployment=config.get("AZURE_OPENAI_DEPLOYMENT_NAME"),
#     openai_api_version=config.get("AZURE_OPENAI_API_VERSION"),
#     api_key=config.get("AZURE_OPENAI_KEY"),
# )

# 使用本地的Llama-3-TW-8B-Instruct模型
generator_llm = ChatOllama(model="Llama-3-TW-8B-Instruct:latest",base_url="http://xxx.xxx.xxx.xxx:11434") 

# 初始化嵌入模型，使用Azure OpenAI Embeddings
embedding_llm = AzureOpenAIEmbeddings(
    azure_endpoint=config.get("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=config.get("AZURE_OPENAI_Embedding_DEPLOYMENT_NAME"),
    api_key=config.get("AZURE_OPENAI_KEY"),
    openai_api_version=config.get("AZURE_OPENAI_API_VERSION"),
)

# ----- 第一次要把知識文件加入Qdrant 向量資料庫時，執行以下程式碼 -----

# # Load PDF文件
# loader = PyPDFLoader("../docs/勞動基準法.pdf")
# pages = loader.load_and_split()

# # 分割文本
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# splits = text_splitter.split_documents(pages)

# # Qdrant向量資料庫
# qdrant = QdrantVectorStore.from_documents(
#     splits,
#     embedding=embedding_llm,
#     url="http://localhost:6333",  # 假設Qdrant運行在本地的6333端口
#     collection_name="km_docs",
# )

#---------------------------------------------------------




# ------- 後續查詢時，已有向量資料，請執行以下程式碼 -------

# Qdrant client
client = QdrantClient(url="http://localhost:6333")
collection_name = "km_docs"
qdrant = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embedding_llm
    )

# -------------------------------------------------------


# 設置檢索器
retriever = qdrant.as_retriever(search_kwargs={"k": 1}) # 檢索前3個最相似的文檔

# 建立提示樣板
q_template = ChatPromptTemplate.from_template("""你是一位精通台灣勞基法的專家。請根據以下參考資料回答問題：

參考資料：{context}

問題：{question}

專家回答：""")

# 建立 QA Chain
qa_chain = (
    {
        "context": retriever ,
        "question": RunnablePassthrough(),
    }
    | q_template
    | generator_llm
    | StrOutputParser()
)


# 步驟 7: 進行查詢
response = qa_chain.invoke("勞工加班費的計算方式是什麼？")

print(response)