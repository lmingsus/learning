'''
建立檔案：app_ch12.py
內容：
services:
  qdrant:
    image: qdrant/qdrant
    restart: always
    ports:
      - "6333:6333"
    volumes:
      - ./qdrant_storage:/qdrant/storage

運行指令： docker-compose up -d
進 http://localhost:6333/ 後看到以下即成功
{
    "title": "qdrant - vector search engine",
    "version": "1.13.5",
    "commit": "e2xxxxx1xxxxxaxxxxx9d5xxxxxb13b065bxxxxx"
}
-d 參數（detached mode）：在背景執行容器，不會顯示容器的輸出日誌，適合用於生產環境

安裝 pip install qdrant-client

'''

# 下面為 qdrant 進階使用技巧的參考程式碼，因為每個專案的需求不同，所以這裡只提供一個簡單的範例，讓讀者可以參考。
from qdrant_client import QdrantClient, models
from qdrant_client.models import Filter, FieldCondition, Range

from configparser import ConfigParser
config = ConfigParser()
config.read('config.ini', encoding='utf8')
try:
    QDRANT_URL = config.get('QDRANT', 'ENDPOINT') + ':6333'
    QDRANT_API_KEY = config.get('QDRANT', 'API_KEY')
except Exception as e:
    print(f"Error: {str(e)}")

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

# 查看 collections
# print(client.get_collections())
for collection_description in client.get_collections().collections:
    print(collection_description)


# Create a new collection
client.create_collection(
    collection_name="my_collection250329",
    vectors_config=models.VectorParams(size=3, distance=models.Distance.COSINE),
    hnsw_config=models.HnswConfigDiff(
        payload_m=16,
        m=0,
    ),
)
# 會 return True


## 	
# 12-1 Qdrant多租戶的設計
##

# 1. Insert vectors into a collection，帶有 user_id 的 payload 
client.upsert(
    collection_name="my_collection250329",
    points=[
        models.PointStruct(
            id=1,
            payload={"user_id": "user_1"},
            vector=[0.9, 0.1, 0.1],
        ),
        models.PointStruct(
            id=2,
            payload={"user_id": "user_1"},
            vector=[0.1, 0.9, 0.1],
        ),
        models.PointStruct(
            id=3,
            payload={"user_id": "user_2"},
            vector=[0.1, 0.1, 0.9],
        ),
    ],
)
# 會 return UpdateResult(operation_id=0, status=<UpdateStatus.COMPLETED: 'completed'>)

# 2.	進行搜尋，並且帶有 user_id 的條件
results = client.query_points(
    collection_name="my_collection250329",
    query=[0.1, 0.1, 0.9],
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="user_id",
                match=models.MatchValue(value="user_1")
            )
        ]
    ),
    limit=10
)
print(results.model_dump_json(exclude_none=True, indent=4))
'''
{
    "points": [
        {
            "id": 2,
            "version": 0,
            "score": 0.22891569,
            "payload": {
                "user_id": "user_1"
            }
        },
        {
            "id": 1,
            "version": 0,
            "score": 0.22891569,
            "payload": {
                "user_id": "user_1"
            }
        }
    ]
}
'''

# 3. 建立 collection 的索引，以加速搜尋

client.create_collection(
    collection_name="my_collection2",
    vectors_config=models.VectorParams(
        size=1536,    # 設定向量維度
        distance=models.Distance.COSINE    # 使用餘弦相似度計算向量距離
        ),
    hnsw_config=models.HnswConfigDiff(
        payload_m=16, # payload graph 的最大連接數
        m=0,  # 禁止建立全域 payload 索引，節省資源
    ),
)
client.create_payload_index(
    collection_name="my_collection25032",
    field_name="user_id",
    field_schema=models.PayloadSchemaType.KEYWORD,    # 使用 KEYWORD 類型的索引
    # 常用於 ID、標籤等需要精確比對的欄位
)
# 會 return UpdateResult(operation_id=2, status=<UpdateStatus.COMPLETED: 'completed'>)




## 	
# 12-2 Qdrant 索引設計
##

# 1. 全文檢索的索引設計

from qdrant_client import QdrantClient, models

client_local = QdrantClient(url="http://localhost:6333")

print(client_local.get_collections())

client.create_payload_index(
    collection_name="my_collection",
    field_name="content",
    field_schema=models.TextIndexParams(    # 建立文字索引
        type="text",    # 指定為文字類型索引，適用於全文檢索
        tokenizer=models.TokenizerType.WORD,    # 使用詞級別的分詞器，亦有 PREFIX、WHITESPACE、MULTILINGUAL
        min_token_len=2,    # 最短詞長：2 個字符
        max_token_len=15,    # 最長詞長：15 個字符
        lowercase=True,    # 轉換為小寫，提高搜索匹配率
    ),
)

# 2. 參數化的索引設計

from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")

client.create_payload_index(
    collection_name="my_collection",
    field_name="age",    # 指定要索引的欄位
    field_schema=models.IntegerIndexParams(
        type=models.IntegerIndexType.INTEGER,    #　整數類型
        lookup=False,    # 不建立精確查詢索引
        range=True,      # 啟用範圍查詢
    ),
)
# 會 return UpdateResult(operation_id=2, status=<UpdateStatus.COMPLETED: 'completed'>)


# 3.    集合的向量索引

from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")

client.update_collection(
    collection_name="my_collection",
    hnsw_config=models.HnswConfigDiff(
        m=16,    # 每個節點的最大連接數，較大的值會提高搜索精度，但會增加記憶體使用和索引構建時間
        ef_construct=100,     # 索引構建時的搜索深度，每個節點搜尋其鄰居時考慮的候選節點數量
                            # ，較大的值會提高索引構建的品質，但會增加構建時間
        # 當需要提高集合的檢索精度時，可以增加 m 和 ef_construct 的值
    )
)

# 4. 稀疏向量索引
# 適合：
# 自然語言處理應用
# 大規模文本檢索
# 需要高效記憶體使用的系統

from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")

client.create_collection(
    collection_name="my_collection",
    sparse_vectors={                                 # 定義稀疏向量配置
        "text": models.SparseVectorIndexParams(
            index=models.SparseVectorIndexType(
                on_disk=False,                       # 索引儲存在記憶體中，而不是硬碟
            ),
        ),
    },
)





## 	###############################################
# 12-3 Qdrant分散式部署
##  ###############################################


# 1.	建立 Qdrant 的分散式部署的配置檔案

# qdrant 部署的同個資料夾進，建立一個 config.yaml 檔。可以參考以下的配置的內容
'''
cluster:
  enabled: true
  p2p:
    port: 6335
  consensus:
    tick_period_ms: 100
'''

# 2.	Qdrant 的 sharding

from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")

client.create_collection(
    collection_name="my_collection",
    vectors_config=models.VectorParams(
        size=1536,           # OpenAI embedding 常用維度
        distance=models.Distance.COSINE # 使用餘弦相似度
        ),
    shard_number=6,         # 將集合分成 6 個分片，分片可以提高並行處理能力，適合大規模數據處理
    replication_factor=2,   # 每個分片保存 2 個副本，提高資料可用性和容錯性，可以在節點故障時保持服務可用，3個副本提供更高的可用性

)

# 3.	Qdrant 的資料一致性 Write consistency factor

from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")

client.create_collection(
    collection_name="{collection_name}",
    vectors_config=models.VectorParams(size=300, distance=models.Distance.COSINE),
    shard_number=6,                 # 將集合分割成 6 個分片，提高並行處理能力，適合大規模資料處理
    replication_factor=2,           # 每個分片保存 2 個副本
    write_consistency_factor=2,     # 確保至少 2 個副本成功寫入，提供寫入操作的資料一致性保證
)


# 4.	Qdrant 的資料一致性 Read Consistency Parameter

from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")

client.search(
    collection_name="{collection_name}",
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="city",
                match=models.MatchValue(
                    value="London",
                ),
            )
        ]
    ),
    search_params=models.SearchParams(hnsw_ef=128, exact=False),
    query_vector=[0.2, 0.1, 0.9, 0.7],
    limit=3,
    consistency="majority",     # 等待大多數副本回應
    # consistency="all",          # 等待所有副本回應
    # consistency="quorum",       # 等待法定數量副本回應
)

# 5.	Qdrant 的資料一致性 Write Order Paremeter

from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")

client.upsert(                              # 更新或插入，已存在則更新，不存在則新增
    collection_name="{collection_name}",
    points=models.Batch(                    # 批量更新
        ids=[1, 2, 3],                      # 為每個點指定唯一 ID
        payloads=[                          # 每個向量的附加資訊
            {"color": "red"},
            {"color": "green"},
            {"color": "blue"},
        ],
        vectors=[                           # 實際的向量數據，每個向量對應一個 ID 和 payload
            [0.9, 0.1, 0.1],                # 紅色向量
            [0.1, 0.9, 0.1],                # 綠色向量
            [0.1, 0.1, 0.9],                # 藍色向量
        ],
    ),
    ordering=models.WriteOrdering.STRONG,   # 使用強一致性寫入，確保資料完全寫入後才返回
)