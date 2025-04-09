from langchain_huggingface import HuggingFaceEndpointEmbeddings

from configparser import ConfigParser

try:
    config = ConfigParser()
    config.read('config.ini', encoding='utf-8')
    
    ACCESS_TOKEN = config.get('HUGGING_FACE', 'ACCESS_TOKEN')

    if not ACCESS_TOKEN:
        raise ValueError("請在 config.ini 中設定所有必要的 HUGGING_FACE 參數")
except Exception as e:
    print(f"Error: {str(e)}")
    print("Please provide a valid API key and endpoint")
    exit(1)

api_token = ACCESS_TOKEN

model = "sentence-transformers/all-MiniLM-L6-v2"

hf_embeddings = HuggingFaceEndpointEmbeddings(
    model=model,
    task="feature-extraction",
    huggingfacehub_api_token=api_token,
)

texts = ["統一發票中獎號碼於今（25）日稍早正式開出", 
         "中獎發票購買品項也多為礦泉水及飲料等商品。"]

response = hf_embeddings.embed_documents(texts)

print(response)
'''
[[-0.02978665940463543,
  0.1029471680521965,
  0.06525994092226028,
  ...
  -0.051936812698841095,
  -0.03224768117070198],
  
  [-0.01656695082783699,
  0.0788000300526619,
  0.018402792513370514,
  ...
  0.023697659373283386,
  0.03412717953324318]]
'''