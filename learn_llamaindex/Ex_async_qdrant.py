from llama_index.core import (
    VectorStoreIndex, SimpleDirectoryReader, 
    Settings, StorageContext
)
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.openai_like import OpenAILikeEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client.async_qdrant_client import AsyncQdrantClient

# uv add llama-index-vector-stores-qdrant

Settings.embed_model = OpenAILikeEmbedding(
    model_name="Qwen3-Embedding-0.6B",
    api_base="http://192.168.0.101:7392/v1",
    api_key="EMPTY"
)
Settings.llm = OpenAILike(
    model="Qwen3-0.6B",
    api_base="http://192.168.0.101:7393/v1",
    api_key="EMPTY"
)

documents = SimpleDirectoryReader("data/").load_data()

# 使用 aclient
client = AsyncQdrantClient(host="localhost", port=6333)



async def query():

    global documents, client
    vector_store = QdrantVectorStore(aclient=client, collection_name="paul_graham")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 使用 use_async=True
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        use_async=True,
    )
    query_engine = index.as_query_engine(use_async=True)

    response = await query_engine.aquery("应该推荐那两本书？")
    print(response)


async def retrieve():

    vector_store = QdrantVectorStore(aclient=client, collection_name="paul_graham")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        use_async=True,
    )

    retrieve_engine = index.as_retriever(use_async=True)
    response = await retrieve_engine.aretrieve("应该推荐那两本书？")
    print(response)


async def main():
    await query()
    await retrieve()




if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
