# https://python.langchain.com/docs/integrations/vectorstores/qdrant/
from qdrant_client import QdrantClient, models
# from langchain_community.vectorstores import Qdrant       # deprecated
from langchain_qdrant import QdrantVectorStore, RetrievalMode
from qdrant_client.http.models import Distance, VectorParams
from langchain_core.documents import Document

from langchain_openai import AzureOpenAIEmbeddings

from uuid import uuid4



from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini', encoding='utf8')
try:
    # Azure OpenAI Embedding
    EMBEDDING_MODEL = config.get('Azure', 'EMBEDDING_MODEL')
    AZURE_OPENAI_API_KEY = config.get('Azure', 'OPENAI_KEY')
    AZURE_OPENAI_ENDPOINT = config.get('Azure', 'OPENAI_ENDPOINT')
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME = config.get('Azure', 'OPENAI_EMBEDDING_DEPLOYMENT_NAME')
    AZURE_OPENAI_API_EMBEDDING_VERSION = config.get('Azure', 'OPENAI_API_EMBEDDING_VERSION')
    if not all([EMBEDDING_MODEL, AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME, AZURE_OPENAI_API_EMBEDDING_VERSION]):
        raise Exception("Please provide all required Azure OpenAI Embedding configuration values in config.ini.")
    
    QDRANT_URL = config.get('QDRANT', 'ENDPOINT') + ':6333'
    QDRANT_API_KEY = config.get('QDRANT', 'API_KEY')
    if QDRANT_URL == ':6333' or not QDRANT_API_KEY:
        raise Exception("Please provide all required Qdrant configuration values in config.ini.")
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

collection_name = "langchain_example"

client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)


# qdrant = Qdrant(client, collection_name, embeddings_model) # deprecated
vector_store = QdrantVectorStore(
    client=client,
    collection_name=collection_name,
    embedding=embeddings_model,
)

# =================================================
# Add items to vector store
document_1 = Document(
    page_content="I had chocolate chip pancakes and scrambled eggs for breakfast this morning.",
    metadata={"source": "tweet"},
)

document_2 = Document(
    page_content="The weather forecast for tomorrow is cloudy and overcast, with a high of 62 degrees Fahrenheit.",
    metadata={"source": "news"},
)

document_3 = Document(
    page_content="Building an exciting new project with LangChain - come check it out!",
    metadata={"source": "tweet"},
)

document_4 = Document(
    page_content="Robbers broke into the city bank and stole $1 million in cash.",
    metadata={"source": "news"},
)

document_5 = Document(
    page_content="Wow! That was an amazing movie. I can't wait to see it again.",
    metadata={"source": "tweet"},
)

document_6 = Document(
    page_content="Is the new iPhone worth the price? Read this review to find out.",
    metadata={"source": "website"},
)

document_7 = Document(
    page_content="The top 10 soccer players in the world right now.",
    metadata={"source": "website"},
)

document_8 = Document(
    page_content="LangGraph is the best framework for building stateful, agentic applications!",
    metadata={"source": "tweet"},
)

document_9 = Document(
    page_content="The stock market is down 500 points today due to fears of a recession.",
    metadata={"source": "news"},
)

document_10 = Document(
    page_content="I have a bad feeling I am going to get deleted :(",
    metadata={"source": "tweet"},
)

documents = [
    document_1,
    document_2,
    document_3,
    document_4,
    document_5,
    document_6,
    document_7,
    document_8,
    document_9,
    document_10,
]
uuids = [str(uuid4()) for _ in range(len(documents))]
vector_store.add_documents(documents, ids=uuids)
# return
['9016034d-xxxx-xxxx-ad9d-xxxxxxxxxxxx',
 '5325f672-xxxx-xxxx-a355-xxxxxxxxxxxx',
 'b76e8917-xxxx-xxxx-9a7b-xxxxxxxxxxxx',
 '6580fc0c-xxxx-xxxx-b011-xxxxxxxxxxxx',
 'a995c9eb-xxxx-xxxx-b783-xxxxxxxxxxxx',
 'ac8b670d-xxxx-xxxx-b757-xxxxxxxxxxxx',
 '49fdaef5-xxxx-xxxx-847f-xxxxxxxxxxxx',
 'd3e4193f-xxxx-xxxx-9dd0-xxxxxxxxxxxx',
 '7e3c4002-xxxx-xxxx-a9e0-xxxxxxxxxxxx',
 '6d585698-xxxx-xxxx-a6a9-xxxxxxxxxxxx']

# Delete items from vector store
# vector_store.delete(ids=[uuids[-1]])

# ============================================================

results = vector_store.similarity_search(
    "LangChain provides abstractions to make working with LLMs easy", k=2
)

for res in results:
    print(res.model_dump_json(indent=4))

'''
{
    "id": null,
    "metadata": {
        "source": "tweet",
        "_id": "b76e8917-90f3-4676-9a7b-c4ff3ecdb518",
        "_collection_name": "langchain_example"
    },
    "page_content": "Building an exciting new project with LangChain - come check it out!",
    "type": "Document"
}
{
    "id": null,
    "metadata": {
        "source": "tweet",
        "_id": "d3e4193f-c041-46fd-9dd0-39db800d5a8e",
        "_collection_name": "langchain_example"
    },
    "page_content": "LangGraph is the best framework for building stateful, agentic applications!",
    "type": "Document"
}
'''

# ============================================================
# Dense Vector Search


qdrant = QdrantVectorStore(
    client=client,
    collection_name=collection_name,
    embedding=embeddings_model,
    retrieval_mode=RetrievalMode.DENSE,    # default
)

query = "How much money did the robbers steal?"
found_docs = qdrant.similarity_search(query)
[Document(metadata={'source': 'news', '_id': '6580fc0c-8d95-40d4-b011-8fa5d463536c', '_collection_name': 'langchain_example'}, page_content='Robbers broke into the city bank and stole $1 million in cash.'),
 Document(metadata={'source': 'website', '_id': 'ac8b670d-4caf-413c-b757-9463b7354d76', '_collection_name': 'langchain_example'}, page_content='Is the new iPhone worth the price? Read this review to find out.'),
 Document(metadata={'source': 'news', '_id': '7e3c4002-ab1c-4c3d-a9e0-478719d17a2e', '_collection_name': 'langchain_example'}, page_content='The stock market is down 500 points today due to fears of a recession.'),
 Document(metadata={'source': 'tweet', '_id': 'a995c9eb-0d6c-46a3-b783-87a84c8fc6b6', '_collection_name': 'langchain_example'}, page_content="Wow! That was an amazing movie. I can't wait to see it again.")]

results = qdrant.similarity_search_with_score(query = "LLM", k = 5)
[(Document(metadata={'source': 'tweet', '_id': 'b76e8917-90f3-4676-9a7b-c4ff3ecdb518', '_collection_name': 'langchain_example'}, page_content='Building an exciting new project with LangChain - come check it out!'),
  0.16408929),
 (Document(metadata={'source': 'tweet', '_id': 'd3e4193f-c041-46fd-9dd0-39db800d5a8e', '_collection_name': 'langchain_example'}, page_content='LangGraph is the best framework for building stateful, agentic applications!'),
  0.14287144),
 (Document(metadata={'source': 'tweet', '_id': 'a995c9eb-0d6c-46a3-b783-87a84c8fc6b6', '_collection_name': 'langchain_example'}, page_content="Wow! That was an amazing movie. I can't wait to see it again."),
  0.10488176),
 (Document(metadata={'source': 'tweet', '_id': '6d585698-a2df-443d-a6a9-c495c52b8f43', '_collection_name': 'langchain_example'}, page_content='I have a bad feeling I am going to get deleted :('),
  0.10438569),
 (Document(metadata={'source': 'website', '_id': '49fdaef5-5e05-4a90-847f-b382ae95b612', '_collection_name': 'langchain_example'}, page_content='The top 10 soccer players in the world right now.'),
  0.06487662)]


# ============================================================
# Metadata filtering


results = vector_store.similarity_search(
    query="Who are the best soccer players in the world?",
    k=2,                    # 即使設定為 2
    filter=models.Filter(
        should=[
            models.FieldCondition(
                key="page_content",
                match=models.MatchValue(
                    value="The top 10 soccer players in the world right now."
                ),
            ),
        ]
    ),
)

for res in results:
    print(res.model_dump_json(indent=4))
'''
{
    "id": null,
    "metadata": {
        "source": "website",
        "_id": "49fdaef5-5e05-4a90-847f-b382ae95b612",
        "_collection_name": "langchain_example"
    },
    "page_content": "The top 10 soccer players in the world right now.",
    "type": "Document"
}
'''