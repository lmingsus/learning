'''
from langchain_core.runnables import RunnableLambda

custom_function = RunnableLambda(lambda x: x.upper())
result = custom_function.invoke("hello world")
print(result) # HELLO WORLD
'''
from langchain_core.runnables import RunnableSequence, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import json

from configparser import ConfigParser

try:
    config = ConfigParser()
    config.read('config.ini')
    # Azure OpenAI Model
    # Azure AI Foundry 部屬端點目標URI：
    # {AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT_NAME}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}
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
                        temperature=0.5,
                        )



def validate_order(order) -> dict:
    """
    驗證訂單資訊
    """
    errors = []
    if not order.get("customer_id"):
        errors.append("缺少客戶ID")
    if not order.get("items") or len(order["items"]) == 0:
        errors.append("訂單中沒有商品")
    
    # 回傳 processed_order 的 dict
    return {"order": order, "is_valid": len(errors) == 0, "errors": errors}

validate_order_RunnableLambda = RunnableLambda(validate_order)



def prepare_llm_input(processed_order):
    """
    準備 LLM 輸入
    """
    return {"order_info": json.dumps(processed_order, ensure_ascii=False)}

prepare_llm_input_RunnableLambda = RunnableLambda(prepare_llm_input)


# 建立 LLM 摘要Chain
summary_prompt = ChatPromptTemplate.from_template(
        "你是一個電子商務平台的客戶服務助手。請根據以下訂單內容生成訂單摘要。"
        "如果訂單無效，請解釋原因。訂單內容：### {order_info} ### "
    )
summary_chain = summary_prompt | llm



# 建立訂單處理工作流程 (勘誤,範例中 validate_order 應為 validate_order_RunnableLambda）
workflow = RunnableSequence(
    validate_order_RunnableLambda,
    prepare_llm_input_RunnableLambda,
    summary_chain,
    StrOutputParser()
)


def main():
    # 測試工作流程
    test_orders = [
        {
            "customer_id": "CUS001",
            "items": [
                {"name": "筆記本電腦", "price": 35000, "quantity": 1},
                {"name": "滑鼠", "price": 2500, "quantity": 2}
            ]
        },
        {
            "customer_id": "CUS003",
            "items": []
        },
        {
            "items": [
                {"name": "鍵盤", "price": 500, "quantity": 1}
            ]
        },
        {
            "customer_id": "CUS005",
            "items": [
                {"name": "路由器", "price": 6000, "quantity": 1},
                {"name": "網路線", "price": 300, "quantity": 2},
                {"name": "氮化鎵快充器", "price": 699, "quantity": 1}
            ]
        },
        {
            "customer_id": "CUS00",
            "items": [
                {"name": "滑鼠", "price": 2500, "quantity": 20},
                {"name": "鍵盤", "price": 500, "quantity": 20}
            ]
        },
        {
            "customer_id": "CUS045",
            "items": [
                {"name": "滑鼠", "price": 2500, "quantity": 0},
                {"name": "鍵盤", "price": 500, "quantity": 20}
            ]
        }
    ]

    for order in test_orders:
        result = workflow.invoke(order)
        print(result)
        print("--------------------------------------------------")

if __name__ == "__main__":
    main()


# 測試結果：
'''
### 訂單摘要

- **客戶ID**: CUS001       
- **訂單有效性**: 有效     

#### 訂單項目：
1. **商品名稱**: 筆記本電腦
   - **價格**: 35,000元    
   - **數量**: 1
   - **小計**: 35,000元

2. **商品名稱**: 滑鼠
   - **價格**: 2,500元
   - **數量**: 2
   - **小計**: 5,000元

#### 總計：
- **總金額**: 40,000元

感謝您的訂購！如有任何問題，請隨時聯繫我們的客戶服務團隊。
--------------------------------------------------
訂單摘要：
   - **小計**: 35,000元

2. **商品名稱**: 滑鼠
   - **價格**: 2,500元
   - **數量**: 2
   - **小計**: 5,000元

#### 總計：
- **總金額**: 40,000元

感謝您的訂購！如有任何問題，請隨時聯繫我們的客戶服務團隊。
--------------------------------------------------
訂單摘要：

- **客戶ID**: CUS003
- **訂單商品**: 無
- **訂單有效性**: 無效
- **錯誤原因**: 訂單中沒有商品

這筆訂單無效的原因是未包含任何商品。請您添加商品後重新提交訂單。如需進一步協助，請隨時告訴我們！
--------------------------------------------------
訂單摘要：

- **訂單內容**:
  - 商品名稱: 鍵盤
  - 價格: 500
  - 數量: 1

- **訂單有效性**: 無效

- **無效原因**: 此訂單缺少客戶ID，無法進行處理。請提供有效的客戶ID以便重新提交訂單。
--------------------------------------------------
訂單摘要：

- **客戶ID**: CUS005
- **訂單項目**:
  1. **商品名稱**: 路由器
     - 價格: 6000 元
     - 數量: 1
  2. **商品名稱**: 網路線
     - 價格: 300 元
     - 數量: 2
  3. **商品名稱**: 氮化鎵快充器
     - 價格: 699 元
     - 數量: 1

- **訂單有效性**: 有效
- **總金額**: 6000 + (300 * 2) + 699 = 6999 元

這是一個有效的訂單，沒有任何錯誤。感謝您的訂購！
--------------------------------------------------
### 訂單摘要

- **客戶ID**: CUS00
- **訂單有效性**: 有效

#### 訂單詳情
1. **商品名稱**: 滑鼠
   - **單價**: 2500
   - **數量**: 20
   - **小計**: 50000

2. **商品名稱**: 鍵盤
   - **單價**: 500
   - **數量**: 20
   - **小計**: 10000

#### 總計
- **訂單總額**: 60000

感謝您的訂單！如有任何問題，請隨時聯繫我們的客戶服務團隊。
--------------------------------------------------
訂單摘要：

- **客戶ID**: CUS045
- **訂單有效性**: 有效
- **訂單項目**:
  1. **商品名稱**: 滑鼠
     - 價格: 2500元
     - 數量: 0（無法購買，數量需大於0）
  2. **商品名稱**: 鍵盤
     - 價格: 500元
     - 數量: 20

雖然訂單標記為有效，但滑鼠的數量為0，這使得該項目無法完成購買。因此，雖然訂單整體被標記為有效，但實際上存在問題。請確認並調整滑鼠的數量，確保 
其大於0以完成訂單。
--------------------------------------------------
'''