# pip install langchain-huggingface
from langchain_huggingface import HuggingFacePipeline
# https://python.langchain.com/api_reference/huggingface/llms/langchain_huggingface.llms.huggingface_pipeline.HuggingFacePipeline.html


llm = HuggingFacePipeline.from_model_id(
    # model_id="microsoft/Phi-3-mini-4k-instruct",
    model_id="microsoft/Phi-4-mini-instruct",
    task="text-generation",
    pipeline_kwargs={
        "max_new_tokens": 100,
        "top_k": 50,
        "do_sample": False
    },
)

response = llm.invoke("世界上最高的山是哪一座？")
print(response)