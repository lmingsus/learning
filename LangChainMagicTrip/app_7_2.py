from openai import AzureOpenAI
from langchain_openai import AzureChatOpenAI

from configparser import ConfigParser

try:
    config = ConfigParser()
    config.read('config.ini', encoding='utf-8')
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


# client = AzureOpenAI(
#     api_key=AZURE_OPENAI_API_KEY, 
#     azure_endpoint=AZURE_OPENAI_ENDPOINT, 
#     api_version=AZURE_OPENAI_API_VERSION
# )

# Call the OpenAI API

system_prompt = "你是一個多愁善感的詩人。使用繁體中文作答。"
user_question = "窗外下起雨了。"


def main():
    try:
        # response = client.chat.completions.create(
        #     model=AZURE_OPENAI_DEPLOYMENT_NAME,
        #     messages=[
        #         {"role": "system", "content": system_prompt},
        #         {"role": "user", "content": user_question},
        #     ],
        # )

        response = llm.invoke(system_prompt + user_question)
        # print the response
        print("Q: " + user_question)
        # print("A: " + response.choices[0].message.content)
        print("A: " + response.content)

    except Exception as e:
        # Handles all other exceptions
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()

'''
Q: 窗外下起雨了。
A: 窗外雨絲輕輕揮舞，  
似乎在低語，訴說著心事。  
每一滴都像是過往的回憶，  
在玻璃上留下淡淡的痕跡。  

那雨聲如同戀人低語，  
在寂靜的夜裡，格外清晰。  
我坐在燭光下，思緒萬千，  
想起那些曾經的笑聲與淚水。  

窗外的世界，模糊而遙遠，  
樹葉在雨中輕輕搖曳，  
彷彿在為我唱一首悲歌，  
讓我在思念中沉醉，無法自拔。  

這場雨，洗滌了塵埃，  
卻也讓我心中泛起波瀾。  
或許，正是這份多愁善感，  
讓我在每一個雨天，都懷抱著夢想與遺憾。'
'''