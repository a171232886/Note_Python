from llama_index.core import Document
from llama_index.core.schema import MetadataMode, TextNode
from llama_index.core.node_parser import SentenceSplitter

from uuid import uuid4


def the_doc():
    # 样例doc
    document = Document.example()


    doc = Document(
        text="txtddd",
        metadata={"hello":"world"},
        # doc_id = "how"
    )

    # 创建之后，也支持调整
    print(doc.doc_id)
    doc.doc_id = str(uuid4())


    # 设置哪些key，不向LLM展示（the embedding model ）
    doc.excluded_llm_metadata_keys = ["file_name"]
    print(doc.get_content(metadata_mode=MetadataMode.LLM))

    print(doc)


def the_node():
    long_text = """这是第一句。这是第二句。这是第三句。这是第四句。这是第五句。这是第六句。这是第七句。这是第八句。这是第九句。这是第十句。"""
    document = Document(text=long_text)
    parser = SentenceSplitter(chunk_size=30, chunk_overlap=10)
    # document = Document.example()
    # parser = SentenceSplitter(chunk_size=100, chunk_overlap=10)

    nodes = parser.get_nodes_from_documents(documents=[document])
    for node in nodes:
        print(node.text)
        print("===============================")

    print("Node ID: ", nodes[1].node_id)
    print("Node Relationships: ", nodes[1].relationships)
    
    print("Pre Node: ", nodes[1].prev_node)   # 至少是双向链表
    print("Next Node: ",nodes[1].next_node)


    print(nodes[0].ref_doc_id == document.doc_id)       # True
    print(nodes[0].metadata == document.metadata)       # True
    print(nodes[0].ref_doc_id == nodes[1].ref_doc_id)   # True


    # 可以单独创建
    own_node = TextNode(text="hello")


# the_doc()
the_node()