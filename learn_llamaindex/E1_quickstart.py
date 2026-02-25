from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.openai_like import OpenAILikeEmbedding

Settings.embed_model = OpenAILikeEmbedding(
    model_name="text-embedding-v4",
    api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-2020f984b4cf4cf49db7668fd5b597d0"
)
Settings.llm = OpenAILike(
    model="qwen3-next-80b-a3b-instruct",
    api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-2020f984b4cf4cf49db7668fd5b597d0",
    is_chat_model=True
)


# 1. 加载数据
documents = SimpleDirectoryReader("data/").load_data()

# 2. 构建索引
index = VectorStoreIndex.from_documents(documents)

# 3. 创建查询引擎
query_engine = index.as_query_engine()
# index.as_retriever()

# 4. 提问
response = query_engine.query("应该推荐那两本书？")
print(response)