import asyncio
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter, SimpleFileNodeParser
from llama_index.core.ingestion import IngestionPipeline
from llama_index.readers.file import FlatReader


async def p1():

    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=10, chunk_overlap=2)
        ]
    )

    doc = Document.example()
 

    # 同步版本
    # node = pipeline.run(documents=[doc])

    nodes = await pipeline.arun(documents=[doc])
    print(nodes)

    # 创建一个本地缓存
    pipeline.persist("./pipeline_storage")

    # 清楚本地缓存
    # Note: 不起作用！
    pipeline.cache.clear()

    # 建议使用专业的Redis Cache
    # ingest_cache = IngestionCache(
    #     cache=RedisCache.from_host_and_port(host="127.0.0.1", port=6379),
    #     collection="my_test_cache",
    # )


async def t1():
    # Transformations
    # node层级的处理，输入是nodes，输出也是nodes
    # TransformComponent base class has both a synchronous __call__() definition and an async acall() definition.

    node_parser = SentenceSplitter(chunk_size=512)
    doc = Document.example()

    # 同步
    # nodes = node_parser([doc])

    nodes = await node_parser.acall([doc])

    print(nodes)


    """
    可自定义Transform
    class TextCleaner(TransformComponent):
        def __call__(self, nodes, **kwargs):
    """

async def t2():
    # 针对md，html，json
    parser = SimpleFileNodeParser()

    from pathlib import Path
    docs = FlatReader().load_data(Path("./data.json"))
    nodes = parser.get_nodes_from_documents(docs)

    doc = Document.example()
    nodes = parser.get_nodes_from_documents(documents=[doc])





if __name__  == "__main__":
    asyncio.run(
        # p1()
        # t1()
        t2()
    )