# LlamaIndex 

官方文档：[Welcome to LlamaIndex 🦙 ! | LlamaIndex Python Documentation](https://developers.llamaindex.ai/python/framework/)

# 1. 基础介绍

## 1.1 概念

1. [What is context augmentation?](https://developers.llamaindex.ai/python/framework/#what-is-context-augmentation)

   > Context augmentation makes your data available to the LLM to solve the problem at hand. LlamaIndex provides the tools to build any of context-augmentation use case, from prototype to production.

2. [LlamaIndex is the framework for Context-Augmented LLM Applications](LlamaIndex is the framework for Context-Augmented LLM Applications)

   （仅保留和RAG相关的三点）

   > - **Data connectors** ingest your existing data from their native source and format. These could be APIs, PDFs, SQL, and (much) more.
   > - **Data indexes** structure your data in intermediate representations that are easy and performant for LLMs to consume.
   > - **Engines** provide natural language access to your data.

3. 其实LlamaIndex可以用来构建Agent

4. [RAG的简要概述](pip install uv)

   > Retrieval-Augmented Generation (RAG) is a core technique for building data-backed LLM applications with LlamaIndex. It allows LLMs to answer questions about your private data by providing it to the LLM at query time, rather than training the LLM on your data. To avoid sending **all** of your data to the LLM every time, RAG indexes your data and selectively sends only the relevant parts along with your query. 

   

   

## 1.2 快速开始

1. 安装

   ```
   pip install llama-index
   ```

   注意：llama-index框架高度插件化，官方在 [llamahub](https://llamahub.ai/) 中提供了大量插件，若使用，需要额外安装。比如

   ```
   pip install llama-index-llms-openai-like
   ```

   

2. 在`data`文件夹下准备几个文件

   比如：1.txt

   ```
   关于敏捷开发（Agile Development）理论，这是一个非常庞大且不断发展的体系。如果我们要梳理它的“代表作”，通常可以分为奠基经典、核心框架和工程实践三大类。
   
   基于我为你检索到的信息，以下是该领域最具权威性和代表性的书籍清单：
   
   📚 1. 奠基与核心理论（必读经典）
   如果你想理解敏捷的“为什么”和“是什么”，这两本书是绕不开的基石：
   
   《敏捷软件开发：原则、模式与实践》 (Agile Software Development: Principles, Patterns, and Practices)
   作者： Robert C. Martin (Uncle Bob)
   地位： 被誉为敏捷开发的“圣经”。这本书不仅阐述了敏捷的原则，还结合了面向对象设计的原则（SOLID原则）。
   核心内容： 它深入探讨了敏捷开发的核心理念、设计模式以及实际编程规范，强调了代码的整洁和可维护性。对于开发者和管理者来说，这是理解敏捷全貌的最佳起点。
   《敏捷宣言》 (Agile Manifesto)
   注意： 虽然它不是一本书，但它是所有敏捷理论的源头。由Kent Beck等17位软件开发领军人物于2001年签署，确立了“个体和互动、可工作的软件、客户合作、响应变化”四大价值观。
   🏗️ 2. 主流框架详解（Scrum与看板）
   在实际操作中，大多数团队使用的是 Scrum 或 看板。以下是这两个领域的权威著作：
   ...
   ```

   

3. 测试代码

   ```python
   # E1_quickstart.py
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
   ```
   输出
   ```
   《敏捷软件开发：原则、模式与实践》和《Scrum指南》
   ```




# 2. RAG介绍

## 2.1 理论

（根据[Introduction to RAG](https://developers.llamaindex.ai/python/framework/understanding/rag/)精简得来）

1. 背景

   > LLMs are trained on enormous bodies of data but they aren’t trained on **your** data. Retrieval-Augmented Generation (RAG) solves this problem by adding your data to the data LLMs already have access to.

2. 步骤概览

   > - In RAG, your data is loaded and prepared for queries or “indexed”. 
   >
   > - User queries act on the index, which filters your data down to the most relevant context. 
   >
   > - This context and your query then go to the LLM along with a prompt, and the LLM provides a response.

   ![img](images/LlamaIndex/basic_rag.sdlwNwWz_Z1yQWLG.png)

3. 核心步骤

   ![img](images/LlamaIndex/stages.B-QMnT9I_1uEetk.png)

   - **Loading**: this refers to getting your data from where it lives — whether it’s text files, PDFs, another website, a database, or an API — into your workflow.
     -  [LlamaHub](https://llamahub.ai/) provides hundreds of connectors to choose from.
     - 注意 RAG 核心的“数据分段”技术，在LlamaIndex中被划分至“数据载入”
   - **Indexing**: this means creating a data structure that allows for querying the data. 
     - For LLMs this nearly always means creating `vector embeddings`, **numerical representations of the meaning of your data**, as well as numerous other metadata strategies to make it easy to accurately find contextually relevant data.
   - **Storing**: once your data is indexed you will almost always want to store your index, as well as other metadata, to avoid having to re-index it.
     - 数据与索引存储相关，也是LlamaIndex框架下最需要用户关注的地方
   - **Querying**: for any given indexing strategy there are many ways you can utilize LLMs and LlamaIndex data structures to query, including sub-queries, multi-step queries and hybrid strategies.
     - 先从数据库中取回问题相关资料，然后再送到LLM中
   - **Evaluation**: a critical step in any flow is checking how effective it is relative to other strategies, or when you make changes. Evaluation provides objective measures of how accurate, faithful and fast your responses to queries are.



## 2.2 关键实体

1. [**Nodes and Documents**](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes): 

   > - A `Document` is a container around any data source - for instance, a PDF, an API output, or retrieve data from a database. 
   > - **A `Node` is the atomic unit of data in LlamaIndex and represents a “chunk” of a source `Document`. **
   > - Nodes have metadata that relate them to the document they are in and to other nodes.

   即一份文件对应的是Document，会被拆分成多个Node

2. [**Embeddings**](https://developers.llamaindex.ai/python/framework/module_guides/models/embeddings): 

   > LLMs generate numerical representations of data called `embeddings`. When filtering your data for relevance, LlamaIndex will convert queries into embeddings.

3. [**Indexes**](https://developers.llamaindex.ai/python/framework/module_guides/indexing):
   - 当node及其对应的embedding构建结束后，选择一部分（或全部）node作为一个整体集合，成为index
   - 未来进行检索时，选择在哪个集合，也就是在哪个index中检索

4. [**Retrievers**](https://developers.llamaindex.ai/python/framework/module_guides/querying/retriever):

   > A retriever defines how to efficiently retrieve relevant context from an index when given a query. 

   根据问题，从数据库中获取相关node

5. [**Node Postprocessors**](https://developers.llamaindex.ai/python/framework/module_guides/querying/node_postprocessors): A node postprocessor takes in a set of retrieved nodes and applies transformations, filtering, or re-ranking logic to them.
   - 输入是node，输出也是node
   - 对node的处理操作集合

6. 在复杂情况下（多个Retrievers），还有[**Routers**](https://developers.llamaindex.ai/python/framework/module_guides/querying/router)用于确定选择哪个Retrievers





# 3. Loading

## 3.1 数据结构

### 3.1.1 Document

（结合[Documents / Nodes](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/)与[Defining and Customizing Documents](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_documents/)）

1. A **Document** is a generic container around any data source 

   for instance, a PDF, an API output, or retrieved data from a database. 

   - They can be constructed manually, 

     ```python
     from llama_index.core import Document, VectorStoreIndex
     
     text_list = [text1, text2, ...]
     documents = [Document(text=t) for t in text_list]
     ```

     

   - or created automatically via our data loaders.

     ```python
     from llama_index.core import SimpleDirectoryReader
     documents = SimpleDirectoryReader("./data").load_data()
     ```

     

2. Document stores text along with some other attributes

   - `metadata` - a dictionary of annotations that can be appended to the text.
     - This information can be anything, such as filenames or categories.
     -  If you are integrating with a vector database, keep in mind that some vector databases require that the keys must be strings, and the values must be flat (either `str`, `float`, or `int`).
   - `relationships` - a dictionary containing relationships to other Documents/Nodes.



3. 框架提供了一个默认Document用于研究和原型开发

   ```
   document = Document.example()
   ```

   ```json
   {
       "id_": "a27b5ad3-4430-4b7e-a247-da8af9fd034e",
       "embedding": null,
       "metadata": {
           "filename": "README.md",
           "category": "codebase"
       },
       "excluded_embed_metadata_keys": [],
       "excluded_llm_metadata_keys": [],
       "relationships": {},
       "metadata_template": "{key}: {value}",
       "metadata_separator": "\n",
       "text_resource": {
           "embeddings": null,
           "text": "\nContext\nLLMs are a phenomenal piece of technology for knowledge generation and reasoning.\nThey are pre-trained on large amounts of publicly available data.\nHow do we best augment LLMs with our own private data?\nWe need a comprehensive toolkit to help perform this data augmentation for LLMs.\n\nProposed Solution\nThat's where LlamaIndex comes in. LlamaIndex is a \"data framework\" to help\nyou build LLM  apps. It provides the following tools:\n\nOffers data connectors to ingest your existing data sources and data formats\n(APIs, PDFs, docs, SQL, etc.)\nProvides ways to structure your data (indices, graphs) so that this data can be\neasily used with LLMs.\nProvides an advanced retrieval/query interface over your data:\nFeed in any LLM input prompt, get back retrieved context and knowledge-augmented output.\nAllows easy integrations with your outer application framework\n(e.g. with LangChain, Flask, Docker, ChatGPT, anything else).\nLlamaIndex provides tools for both beginner users and advanced users.\nOur high-level API allows beginner users to use LlamaIndex to ingest and\nquery their data in 5 lines of code. Our lower-level APIs allow advanced users to\ncustomize and extend any module (data connectors, indices, retrievers, query engines,\nreranking modules), to fit their needs.\n",
           "path": null,
           "url": null,
           "mimetype": null
       },
       "image_resource": null,
       "audio_resource": null,
       "video_resource": null,
       "text_template": "{metadata_str}\n\n{content}",
       "class_name": "Document",
       "text": "\nContext\nLLMs are a phenomenal piece of technology for knowledge generation and reasoning.\nThey are pre-trained on large amounts of publicly available data.\nHow do we best augment LLMs with our own private data?\nWe need a comprehensive toolkit to help perform this data augmentation for LLMs.\n\nProposed Solution\nThat's where LlamaIndex comes in. LlamaIndex is a \"data framework\" to help\nyou build LLM  apps. It provides the following tools:\n\nOffers data connectors to ingest your existing data sources and data formats\n(APIs, PDFs, docs, SQL, etc.)\nProvides ways to structure your data (indices, graphs) so that this data can be\neasily used with LLMs.\nProvides an advanced retrieval/query interface over your data:\nFeed in any LLM input prompt, get back retrieved context and knowledge-augmented output.\nAllows easy integrations with your outer application framework\n(e.g. with LangChain, Flask, Docker, ChatGPT, anything else).\nLlamaIndex provides tools for both beginner users and advanced users.\nOur high-level API allows beginner users to use LlamaIndex to ingest and\nquery their data in 5 lines of code. Our lower-level APIs allow advanced users to\ncustomize and extend any module (data connectors, indices, retrievers, query engines,\nreranking modules), to fit their needs.\n"
   }
   ```

   

4. doc_id 可通过属性修改

   ```
   document.doc_id = "My new document id!"
   ```
   
   
   
5. metadata的自定义

   ```python
   # 方法一
   document = Document(
       text="text",
       metadata={"filename": "<doc_file_name>", "category": "<category>"},
   )
   
   # 方法二
   document.metadata = {"filename": "<doc_file_name>"}
   ```



6. metadata的高级设置

   大模型的上下文长度有限制，非必要的无关信息应该不传入

   ```python
   # 向 embedding model 传入prompt时，忽略哪些字段
   document.excluded_embed_metadata_keys = ["file_name"]
   
   # 向对话 llm 传入prompt时，忽略哪些字段
   document.excluded_llm_metadata_keys = ["file_name"]
   ```

   

### 3.1.2 Node

（结合[Documents / Nodes](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/)与[Defining and Customizing Nodes](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_nodes/)）

1. A **Node** represents a “chunk” of a source Document, whether that is a text chunk, an image, or other. 

   - contain metadata and relationship information with other nodes.

   

2. 两种构建方式

   - 通过对Document的切分

     ```python
     from llama_index.core.node_parser import SentenceSplitter
     document = Document.example()
     parser = SentenceSplitter(chunk_size=10, chunk_overlap=1)
     nodes = parser.get_nodes_from_documents(documents=[document])
     ```

     

   - 自行创建

     ```python
     from llama_index.core.schema import TextNode
     node1 = TextNode(text="<text_chunk>", id_="<node_id>")
     ```

     

3. Nodes are a first-class citizen in LlamaIndex.

   - Document 是 Node 的子类，确切的说是 TextNode 的子类

   

4. node_id 可通过属性修改

   ```
   node.node_id = "My new node_id!"
   ```

   

5. By default **every Node derived from a Document will inherit the same metadata from that Document** (e.g. a “file_name” filed in the Document is propagated to every Node).



6. node的其他属性

   - `ref_doc_id`指当前node是哪个document的“片段”
   - `relationships`包含两部分
     - SOURCE Node（document）
     - Next Node
   
   - Prevous Node 和 Next Node
   
   ```python
   from llama_index.core import Document
   from llama_index.core.schema import TextNode
   from llama_index.core.node_parser import SentenceSplitter
   
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
   
   the_node()
   ```
   
   输出
   
   Node划分情况
   
   ```
   这是第一句。这是第二句。这是第三句。这是第四句。
   ===============================
   这是第四句。这是第五句。这是第六句。这是第七句。
   ===============================
   这是第七句。这是第八句。这是第九句。
   ===============================
   这是第九句。这是第十句。
   ===============================
   ```
   
   Node 信息打印
   
   ```bash
   Node ID:  ec2de07d-3371-400a-b971-e2d0f24925c1
   
   Node Relationships:  {
   <NodeRelationship.SOURCE: '1'>: RelatedNodeInfo(node_id='3a8eca19-6d19-4684-b53e-d37033a039d3', node_type=<ObjectType.DOCUMENT: '4'>, metadata={}, hash='5e7a226a0749dd110026172245ef35f96a9eccd132eae1bc3dfb68c88a8b2f5b'), 
   
   <NodeRelationship.NEXT: '3'>: RelatedNodeInfo(node_id='bd6690aa-7e09-49be-9f56-96479e57068f', node_type=<ObjectType.TEXT: '1'>, metadata={}, hash='3e785a9de7d7253b745c631969e56ede00121cfdaf8977d0c99f1691aeda5210')
   }
   
   Pre Node:  node_id='ec2de07d-3371-400a-b971-e2d0f24925c1' node_type=<ObjectType.TEXT: '1'> metadata={} hash='a73ed50709b2032bcae6d76dda92824b3403c75e99c9bcbacb807c2ee57446d8'
   
   Next Node:  node_id='a5a08a31-6e45-47d8-9605-35c91fbea1b3' node_type=<ObjectType.TEXT: '1'> metadata={} hash='8288ce88e1bce68a850cdcf6eae89e445335694eb72198b1758a24ff51d44d19'
   ```



## 3.2 SimpleDirectoryReader

Reader为实现对不同数据来源的数据载入，详细分类见[Module Guides](https://developers.llamaindex.ai/python/framework/module_guides/loading/connector/modules/)

- 此处只介绍最常用的[SimpleDirectoryReader](https://developers.llamaindex.ai/python/framework/module_guides/loading/simpledirectoryreader/)

注意`Reader.load_data()`的输出是`list[Document]`



SimpleDirectoryReader可针对多种文件类型

- .csv - comma-separated values
- .docx - Microsoft Word
- .epub - EPUB ebook format
- .hwp - Hangul Word Processor
- .ipynb - Jupyter Notebook
- .jpeg, .jpg - JPEG image
- .mbox - MBOX email archive
- .md - Markdown
- .mp3, .mp4 - audio and video
- .pdf - Portable Document Format
- .png - Portable Network Graphics
- .ppt, .pptm, .pptx - Microsoft PowerPoint




### 3.2.1 读取

1. 基础使用：读取本地文件

   ```python
   from llama_index.core import SimpleDirectoryReader
   
   reader = SimpleDirectoryReader(
       input_dir="path/to/directory", 
       recursive=True
   )
   documents = reader.load_data()
   ```

   注意`recursive=True`，否则只导入顶层文件

   

2. 限制模式

   ```python
   # 指定文件
   SimpleDirectoryReader(input_files=["path/to/file1", "path/to/file2"])
   
   # 排除文件
   SimpleDirectoryReader(
       input_dir="path/to/directory", exclude=["path/to/file1", "path/to/file2"]
   )
   
   # 指定类型
   SimpleDirectoryReader(
       input_dir="path/to/directory", required_exts=[".pdf", ".docx"]
   )
   ```

   

3. 可以用于直接读取支持多种协议的云盘

   > This can be any filesystem object that is implemented by the [`fsspec`](https://filesystem-spec.readthedocs.io/en/latest/) protocol. The `fsspec` protocol has open-source implementations for a variety of remote filesystems including [AWS S3](https://github.com/fsspec/s3fs), [Azure Blob & DataLake](https://github.com/fsspec/adlfs), [Google Drive](https://github.com/fsspec/gdrivefs), [SFTP](https://github.com/fsspec/sshfs), and [many others](https://github.com/fsspec/).

   以最为常用的`AWS S3`为例

   使用docker compose 启动
   
   ```yaml
   services:
     minio:
       image: minio/minio:latest
       container_name: minio
       ports:
         - "9000:9000"  # API端口
         - "9001:9001"  # 控制台端口
       environment:
         MINIO_ROOT_USER: minioadmin
         MINIO_ROOT_PASSWORD: minioadmin
       volumes:
         - ./db/minio_data:/data
       command: server /data --console-address ":9001"
   
   ```
   
   
   
   编写脚本
   
   ```python
   from s3fs import S3FileSystem
   from llama_index.core import SimpleDirectoryReader
   
   fs = S3FileSystem(
       key="minioadmin",
       secret="minioadmin",
       client_kwargs={
           "endpoint_url": "http://192.168.0.100:9000",
           "region_name": "cn-north-1",
           "verify": False,
           "use_ssl": False
       },
       config_kwargs={"s3": {"addressing_style": "path"}}
   )
   
   
   reader = SimpleDirectoryReader(
       input_dir="rag",            # bucket name
       fs=fs,
       recursive=True
   )
   
   documents = reader.load_data()
   
   print(documents)
   ```



### 3.2.2 metadata

1. 默认提取项

   > `SimpleDirectoryReader` will automatically attach a `metadata` dictionary to each `Document` object. By default, this dictionary has these items:
   >
   > - `file_path`: the full filesystem path to the file, including the file name (string)
   > - `file_name`: the file name, including suffix (string)
   > - `file_type`: the MIME type of the file, as guessed by [`mimetypes.guess_type()](https://docs.python.org/3/library/mimetypes.html#mimetypes.guess_type) (string)
   > - `file_size`: the size of the file, in bytes (integer)
   > - `creation_date`, `last_modified_date`, `last_accessed_date`: the creation, modification, and access dates for the file, normalized to the UTC timezone. See [Date and time metadata](https://developers.llamaindex.ai/python/framework/module_guides/loading/simpledirectoryreader/#date-and-time-metadata) below (string)

   

2. 定制生成的Document的metadata

   ```python
   from llama_index.core import SimpleDirectoryReader
   
   # 设置函数
   filename_fn = lambda filename: {"file_name": filename}
   
   # automatically sets the metadata of each document according to filename_fn
   documents = SimpleDirectoryReader(
       "./data", file_metadata=filename_fn
   ).load_data()
   ```




3. 框架集成了一些元信息提取器（[metadata extractor](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_metadata_extractor/)）
   - `SummaryExtractor` - automatically extracts a summary over a set of Nodes
   - `QuestionsAnsweredExtractor` - extracts a set of questions that each Node can answer
   - `TitleExtractor` - extracts a title over the context of each Node
   - `EntityExtractor` - extracts entities (i.e. names of places, people, things) mentioned in the content of each Node



## 3.3 Node Parser

### 3.3.1 介绍

1. Node Parser：将 `Document` 分成 `Node`

   > Node parsers are a simple abstraction that take a list of documents, and **chunk them into `Node` objects**, such that each node is a specific chunk of the parent document.

2. 基础使用

   ```python
   from llama_index.core import Document
   from llama_index.core.node_parser import SentenceSplitter
   
   node_parser = SentenceSplitter(chunk_size=1024, chunk_overlap=20)
   
   nodes = node_parser.get_nodes_from_documents(
       [Document(text="long text")], show_progress=False
   )
   ```

   

### 3.3.2 类型

（[Node Parser Modules | LlamaIndex Python Documentation](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules/)简化）

1. [File-Based](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules/#file-based-node-parsers)类

   - `HTMLNodeParser`
   - `JSONNodeParser`
   - `MarkdownNodeParser`

   推荐使用：`SimpleFileNodeParser`自动判别数据类型选取合适的Node Parser

2. [Text-Splitters](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules/#text-splitters) 类

   - `CodeSplitter`

   - `SentenceSplitter`：根据单词数量划分块，最常用

     ```python
         chunk_size: int = Field(
             default=DEFAULT_CHUNK_SIZE,
             description="The token chunk size for each chunk.",			# 每块大小
             gt=0,
         )
         chunk_overlap: int = Field(
             default=SENTENCE_CHUNK_OVERLAP,
             description="The token overlap of each chunk when splitting.",	# 块之间的重复
             ge=0,
         )
         # 划分重复部分时，句子的完整度 优先 指定overlap数量
     ```

     使用

     ```python
     from llama_index.core.node_parser import SentenceSplitter
     
     splitter = SentenceSplitter(
         chunk_size=1024,	# 每块大小
         chunk_overlap=20,	# 块之间的重复
     )
     nodes = splitter.get_nodes_from_documents(documents)
     ```
   
     
   
   - `TokenTextSplitter`：以token数量为单位进行划分

### 3.3.3 高级使用

1. 在构建索引时使用

   ```python
   from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
   from llama_index.core.node_parser import SentenceSplitter
   
   documents = SimpleDirectoryReader("./data").load_data()
   
   # global
   from llama_index.core import Settings
   
   Settings.text_splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=20)
   
   # per-index
   index = VectorStoreIndex.from_documents(
       documents,
       transformations=[SentenceSplitter(chunk_size=1024, chunk_overlap=20)],
   )
   ```

   

2. 在IngestionPipeline中使用

   ```python
   from llama_index.core import SimpleDirectoryReader
   from llama_index.core.ingestion import IngestionPipeline
   from llama_index.core.node_parser import TokenTextSplitter
   
   documents = SimpleDirectoryReader("./data").load_data()
   
   pipeline = IngestionPipeline(transformations=[TokenTextSplitter(), ...])
   
   nodes = pipeline.run(documents=documents)
   ```

   

## 3.4 Ingestion Pipeline

### 3.4.1 Transformations

1. A transformation is something that takes a list of **`Node` as an input, and returns a list of Node.**

   例如, 

   - [`TextSplitter`](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules#text-splitters)
   - [`NodeParser`](https://developers.llamaindex.ai/python/framework/module_guides/loading/node_parsers/modules)
   - [`MetadataExtractor`](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_metadata_extractor)
   - `Embeddings`model (check our [list of supported embeddings](https://developers.llamaindex.ai/python/framework/module_guides/models/embeddings#list-of-supported-embeddings))

   

2. Each component that implements the `Transformation` base class has both a synchronous `__call__()` definition and an async `acall()` definition.



3. 使用方式

   ```python
   from llama_index.core import VectorStoreIndex
   from llama_index.core.extractors import (
       TitleExtractor,
       QuestionsAnsweredExtractor,
   )
   from llama_index.core.ingestion import IngestionPipeline
   from llama_index.core.node_parser import TokenTextSplitter
   
   transformations = [
       TokenTextSplitter(chunk_size=512, chunk_overlap=128),
       TitleExtractor(nodes=5),
       QuestionsAnsweredExtractor(questions=3),
   ]
   
   index = VectorStoreIndex.from_documents(
       documents, transformations=transformations
   )
   ```



### 3.4.2 Pipeline

1. An `IngestionPipeline` uses a concept of `Transformations` that are applied to input data.

2. 使用方式

   ```python
   client = qdrant_client.QdrantClient(location=":memory:")
   vector_store = QdrantVectorStore(client=client, collection_name="test_store")
   
   pipeline = IngestionPipeline(
       transformations=[
           SentenceSplitter(chunk_size=25, chunk_overlap=0),
           TitleExtractor(),
           OpenAIEmbedding(),
       ],
       vector_store=vector_store,
   )
   
   # Ingest directly into a vector db
   pipeline.run(documents=[Document.example()])
   
   # Create your index
   from llama_index.core import VectorStoreIndex
   
   index = VectorStoreIndex.from_vector_store(vector_store)
   ```

3. 提供cache的存储与加载功能

   （存在些许bug）

4. 支持异步
5. 个人不建议使用pipeline，框架各模块已经高度集成化，均为手动定义流程更合适





# 4. Storing

1. LlamaIndex also supports swappable **storage components** that allows you to customize:

   - **Document stores**: **where ingested documents (i.e., `Node` objects) are stored**,
   - **Index stores**: where index metadata are stored,
   - **Vector stores**: where embedding vectors are stored.
   - **Property Graph stores**: where knowledge graphs are stored (i.e. for `PropertyGraphIndex`).
   - **Chat Stores**: where chat messages are stored and organized.

   The Document/Index stores rely on a common Key-Value store abstraction, which is also detailed below.

   注意：

   - **Document stores保存的并不是文件本身，是node，以及node和doc之间的关系**
   - 核心的是Document stores，Index stores，Vector stores



2. 前4类均提供默认的本地存储类，

   在构造StorageContext时，若不传入对应的对象，直接使用默认

   ```python
   docstore = docstore or SimpleDocumentStore()
   index_store = index_store or SimpleIndexStore()
   graph_store = graph_store or SimpleGraphStore()
   image_store = image_store or SimpleVectorStore()
   ```



3. LlamaIndex supports persisting data to any storage backend supported by [fsspec](https://filesystem-spec.readthedocs.io/en/latest/index.html). We have confirmed support for the following storage backends:

   - Local filesystem
   - AWS S3
   - Cloudflare R2

   ![img](images/LlamaIndex/storage.CHky3Ivr_2ghiKH.png)



4. **存储部分的最高管理层级是`StorageContext`**

   ```python
   from llama_index.core.storage.docstore import SimpleDocumentStore
   from llama_index.core.storage.index_store import SimpleIndexStore
   from llama_index.core.vector_stores import SimpleVectorStore
   from llama_index.core import StorageContext
   
   # create storage context using default stores
   storage_context = StorageContext.from_defaults(
       docstore=SimpleDocumentStore(),
       vector_store=SimpleVectorStore(),
       index_store=SimpleIndexStore(),
   )
   ```









## 4.1 Doc store

以官方推荐的mongodb为例

1. 安装

   ```
   pip install llama-index-storage-docstore-mongodb
   ```

2. 使用

   ```python
   from llama_index.storage.docstore.mongodb import MongoDocumentStore
   
   doc_mongodb_uri = f"mongodb://{user}:{password}@{host}:{port}/{database_name}?authSource=admin"
   document_store = MongoDocumentStore.from_uri(
       uri=doc_mongodb_uri,
       db_name=database_name,
       namespace="docstore"
   )
   ```

   注意：`namespace`是 `database_name` 下的collection的前缀名，与数据库无关，属于llamaindex自定义

   ![image-20260222164754377](images/LlamaIndex/image-20260222164754377.png)

   

3. 数据示例

   （`metadata`为用户自定义字段）

   mongodb中的docstore/ref_doc_info：当前一共有哪些doc，以及对应node

   ```
   {
     "_id": "d057c30f-77aa-42f0-928d-eec27be5cdf7",
     "metadata": {
       "file_path": "rag/1.txt",
       "status": "active"
     },
     "node_ids": [
       "74b6d637-2dc4-4f76-a959-f55294cc559b",
       "1a1653a7-5de8-41b5-8db6-2f48febadb7b"
     ]
   }
   ```

   

   mongodb中的docstore/metadata：当前有哪些node

   ```
   {
     "_id": "d057c30f-77aa-42f0-928d-eec27be5cdf7",
     "doc_hash": "87f34d8b4fb8e5daf17ffd2ca5718e5c25659397d132c8288659b7d8c47f5cfc"
   }
   {
     "_id": "74b6d637-2dc4-4f76-a959-f55294cc559b",
     "doc_hash": "302368e7fd103a7c6febcd1a4dcc4cda1a4cf1ea623f28d2b6cdbb977d631697",
     "ref_doc_id": "d057c30f-77aa-42f0-928d-eec27be5cdf7"
   }
   {
     "_id": "1a1653a7-5de8-41b5-8db6-2f48febadb7b",
     "doc_hash": "26e690f4853bd364792b361f4ebb0178927e881bc6b211640db7213982851de6",
     "ref_doc_id": "d057c30f-77aa-42f0-928d-eec27be5cdf7"
   }
   ```

   

   mongodb中的docstore/data：每个node具体保存的信息

   ```
   {
     "_id": "74b6d637-2dc4-4f76-a959-f55294cc559b",
     "__data__": {
       "id_": "74b6d637-2dc4-4f76-a959-f55294cc559b",
       "embedding": null,
       "metadata": {
         "file_path": "rag/1.txt",
         "status": "processing"
       },
       "excluded_embed_metadata_keys": [
         "file_name",
         "file_type",
         "file_size",
         "creation_date",
         "last_modified_date",
         "last_accessed_date"
       ],
       "excluded_llm_metadata_keys": [
         "file_name",
         "file_type",
         "file_size",
         "creation_date",
         "last_modified_date",
         "last_accessed_date"
       ],
       "relationships": {
         "1": {
           "node_id": "d057c30f-77aa-42f0-928d-eec27be5cdf7",
           "node_type": "4",
           "metadata": {
             "file_path": "rag/1.txt",
             "status": "processing"
           },
           "hash": "87f34d8b4fb8e5daf17ffd2ca5718e5c25659397d132c8288659b7d8c47f5cfc",
           "class_name": "RelatedNodeInfo"
         },
         "3": {
           "node_id": "1a1653a7-5de8-41b5-8db6-2f48febadb7b",
           "node_type": "1",
           "metadata": {},
           "hash": "3e573ded2151ddfa478d2d551c9ed8992ee7a1f9f48595b72f7d1f6b3e4e4fa2",
           "class_name": "RelatedNodeInfo"
         }
       },
       "metadata_template": "{key}: {value}",
       "metadata_separator": "\n",
       "text": "关于敏捷开发（Agile Development）理论，这是一个非常庞大且不断发展的体系。如果我们要梳理它的“代表作”，通常可以分为奠基经典、核心框架和工程实践三大类。\n\n基于我为你检索到的信息，以下是该领域最具权威性和代表性的书籍清单：\n\n📚 1. 奠基与核心理论（必读经典）\n如果你想理解敏捷的“为什么”和“是什么”，这两本书是绕不开的基石：\n\n《敏捷软件开发：原则、模式与实践》 (Agile Software Development: Principles, Patterns, and Practices)\n作者： Robert C. Martin (Uncle Bob)\n地位： 被誉为敏捷开发的“圣经”。这本书不仅阐述了敏捷的原则，还结合了面向对象设计的原则（SOLID原则）。\n核心内容： 它深入探讨了敏捷开发的核心理念、设计模式以及实际编程规范，强调了代码的整洁和可维护性。对于开发者和管理者来说，这是理解敏捷全貌的最佳起点。\n《敏捷宣言》 (Agile Manifesto)\n注意： 虽然它不是一本书，但它是所有敏捷理论的源头。由Kent Beck等17位软件开发领军人物于2001年签署，确立了“个体和互动、可工作的软件、客户合作、响应变化”四大价值观。\n🏗️ 2. 主流框架详解（Scrum与看板）\n在实际操作中，大多数团队使用的是 Scrum 或 看板。以下是这两个领域的权威著作：\n\n《Scrum指南》 (The Scrum Guide)\n作者： Ken Schwaber 和 Jeff Sutherland (Scrum的创始人)\n地位： 这是Scrum的“官方定义”，是最权威、最精简的入门必读。它定义了Scrum的角色（如Scrum Master、产品负责人）、事件（Sprint、站会）和工件（产品待办列表）。\n《SCRUM：用两倍速度做两倍工作》 (SCRUM: The Art of Doing Twice the Work in Half the Time)\n作者： Jeff Sutherland\n核心内容： 作者作为Scrum创始人，通过生动的商业案例讲述了Scrum方法的核心原理。书中强调了跨职能团队协作、每日立会以及MVP（最小可行产品）快速验证的理念，不仅适用于软件开发，还延伸到了其他行业。\n《看板方法：技术企业的敏捷管理》 (Kanban: Successful Evolutionary Change for Your Technology Business)\n作者： David J. Anderson\n核心内容： 详细介绍了看板方法的基本原理和实践。看板强调可视化工作流、限制在制品数量（WIP），非常适合那些流程变更阻力较大或维护工作较多的团队。\n💻 3.",
       "mimetype": "text/plain",
       "start_char_idx": 0,
       "end_char_idx": 1161,
       "metadata_seperator": "\n",
       "text_template": "{metadata_str}\n\n{content}",
       "class_name": "TextNode"
     },
     "__type__": "1"
   }
   ```

   

## 4.2 Vec store

- 支持的多种数据库类型以及特性对比：[Vector Store Options & Feature Support]([Vector Stores | LlamaIndex Python Documentation](https://developers.llamaindex.ai/python/framework/module_guides/storing/vector_stores/#vector-store-options--feature-support))

- 此处介绍基于Qdrant的用法：[Qdrant Vector Store | LlamaIndex Python Documentation](https://developers.llamaindex.ai/python/framework/integrations/vector_stores/qdrantindexdemo/)

  

1. 安装插件（可从 [llamahub](https://llamahub.ai/) 中找到：[LlamaIndex Vector_Stores Integration: Qdrant](https://llamahub.ai/l/vector_stores/llama-index-vector-stores-qdrant?from=vector_stores)）

   ```
   pip install llama-index-vector-stores-qdrant
   pip install qdrant-client
   ```

   

2. 同步使用

   ```python
   from llama_index.vector_stores.qdrant import QdrantVectorStore
   from qdrant_client import QdrantClient
   
   client = QdrantClient(
       host="<host>", 
       port="<port>"
   )
   vector_store = QdrantVectorStore(
       client=client, 
       collection_name=vector_config.collection_name
   )
   
   # NOTE: VERY IMPORTANT FOR THE INDEX STUCTURE CONSISTENCY
   vector_store.stores_text = False
   ```

   ==**要特别注意设置vector_store.stores_text = False，否则与SimpleXXXStore()中保存的数据结构不一致**==



3. 异步使用

   ```python
   from llama_index.vector_stores.qdrant import QdrantVectorStore
   from qdrant_client import AsyncQdrantClient, QdrantClient
   
   client = QdrantClient(
       host="<host>", 
       port="<port>"
   )
   
   aclient = AsyncQdrantClient(
       host="<host>", 
       port="<port>"
   )
   
   vector_store = QdrantVectorStore(
       collection_name="paul_graham",
       client=client,							# 注意要传两个
       aclient=aclient							# 注意要传两个
   )
   
   storage_context = StorageContext.from_defaults(vector_store=vector_store)
   index = VectorStoreIndex.from_documents(
       documents,
       storage_context=storage_context,
       use_async=True,							# 注意
   )
   ```



4. 单条数据payload示例：

   ```json
   {"file_path":"rag/1.txt","status":"processing","_node_content":"{\"id_\": \"74b6d637-2dc4-4f76-a959-f55294cc559b\", \"embedding\": null, \"metadata\": {\"file_path\": \"rag/1.txt\", \"status\": \"processing\"}, \"excluded_embed_metadata_keys\": [\"file_name\", \"file_type\", \"file_size\", \"creation_date\", \"last_modified_date\", \"last_accessed_date\"], \"excluded_llm_metadata_keys\": [\"file_name\", \"file_type\", \"file_size\", \"creation_date\", \"last_modified_date\", \"last_accessed_date\"], \"relationships\": {\"1\": {\"node_id\": \"d057c30f-77aa-42f0-928d-eec27be5cdf7\", \"node_type\": \"4\", \"metadata\": {\"file_path\": \"rag/1.txt\", \"status\": \"processing\"}, \"hash\": \"87f34d8b4fb8e5daf17ffd2ca5718e5c25659397d132c8288659b7d8c47f5cfc\", \"class_name\": \"RelatedNodeInfo\"}, \"3\": {\"node_id\": \"1a1653a7-5de8-41b5-8db6-2f48febadb7b\", \"node_type\": \"1\", \"metadata\": {}, \"hash\": \"3e573ded2151ddfa478d2d551c9ed8992ee7a1f9f48595b72f7d1f6b3e4e4fa2\", \"class_name\": \"RelatedNodeInfo\"}}, \"metadata_template\": \"{key}: {value}\", \"metadata_separator\": \"\\n\", \"text\": \"关于敏捷开发（Agile Development）理论，这是一个非常庞大且不断发展的体系。如果我们要梳理它的“代表作”，通常可以分为奠基经典、核心框架和工程实践三大类。\\n\\n基于我为你检索到的信息，以下是该领域最具权威性和代表性的书籍清单：\\n\\n📚 1. 奠基与核心理论（必读经典）\\n如果你想理解敏捷的“为什么”和“是什么”，这两本书是绕不开的基石：\\n\\n《敏捷软件开发：原则、模式与实践》 (Agile Software Development: Principles, Patterns, and Practices)\\n作者： Robert C. Martin (Uncle Bob)\\n地位： 被誉为敏捷开发的“圣经”。这本书不仅阐述了敏捷的原则，还结合了面向对象设计的原则（SOLID原则）。\\n核心内容： 它深入探讨了敏捷开发的核心理念、设计模式以及实际编程规范，强调了代码的整洁和可维护性。对于开发者和管理者来说，这是理解敏捷全貌的最佳起点。\\n《敏捷宣言》 (Agile Manifesto)\\n注意： 虽然它不是一本书，但它是所有敏捷理论的源头。由Kent Beck等17位软件开发领军人物于2001年签署，确立了“个体和互动、可工作的软件、客户合作、响应变化”四大价值观。\\n🏗️ 2. 主流框架详解（Scrum与看板）\\n在实际操作中，大多数团队使用的是 Scrum 或 看板。以下是这两个领域的权威著作：\\n\\n《Scrum指南》 (The Scrum Guide)\\n作者： Ken Schwaber 和 Jeff Sutherland (Scrum的创始人)\\n地位： 这是Scrum的“官方定义”，是最权威、最精简的入门必读。它定义了Scrum的角色（如Scrum Master、产品负责人）、事件（Sprint、站会）和工件（产品待办列表）。\\n《SCRUM：用两倍速度做两倍工作》 (SCRUM: The Art of Doing Twice the Work in Half the Time)\\n作者： Jeff Sutherland\\n核心内容： 作者作为Scrum创始人，通过生动的商业案例讲述了Scrum方法的核心原理。书中强调了跨职能团队协作、每日立会以及MVP（最小可行产品）快速验证的理念，不仅适用于软件开发，还延伸到了其他行业。\\n《看板方法：技术企业的敏捷管理》 (Kanban: Successful Evolutionary Change for Your Technology Business)\\n作者： David J. Anderson\\n核心内容： 详细介绍了看板方法的基本原理和实践。看板强调可视化工作流、限制在制品数量（WIP），非常适合那些流程变更阻力较大或维护工作较多的团队。\\n💻 3.\", \"mimetype\": \"text/plain\", \"start_char_idx\": 0, \"end_char_idx\": 1161, \"metadata_seperator\": \"\\n\", \"text_template\": \"{metadata_str}\\n\\n{content}\", \"class_name\": \"TextNode\"}","_node_type":"TextNode","document_id":"d057c30f-77aa-42f0-928d-eec27be5cdf7","doc_id":"d057c30f-77aa-42f0-928d-eec27be5cdf7","ref_doc_id":"d057c30f-77aa-42f0-928d-eec27be5cdf7"}
   ```

   

## 4.3 Index store

以官方推荐的mongodb为例

1. 安装

   ```
   pip install llama-index-storage-index-store-mongodb
   ```

2. 使用

   ```python
   from llama_index.storage.index_store.mongodb import MongoIndexStore
   from llama_index.core import VectorStoreIndex
   
   doc_mongodb_uri = f"mongodb://{user}:{password}@{host}:{port}/{database_name}?authSource=admin"
   
   index_store = MongoIndexStore.from_uri(
       uri=index_mongodb_uri,
       db_name=index_config.database,
       namespace="indexstore"
   )
   
   # create storage context
   storage_context = StorageContext.from_defaults(index_store=index_store)
   
   # build index
   index = VectorStoreIndex(nodes, storage_context=storage_context)
   ```

3. 数据示例

   mongodb中的indexstore：是指当前index中有哪些node

   ```json
   {
     "_id": "d67eebb0-d05d-4c19-a93a-99a0db4961aa",
     "__data__": "{\"index_id\": \"d67eebb0-d05d-4c19-a93a-99a0db4961aa\", \"summary\": null, \"nodes_dict\": {\"74b6d637-2dc4-4f76-a959-f55294cc559b\": \"74b6d637-2dc4-4f76-a959-f55294cc559b\", \"1a1653a7-5de8-41b5-8db6-2f48febadb7b\": \"1a1653a7-5de8-41b5-8db6-2f48febadb7b\"}, \"doc_id_dict\": {}, \"embeddings_dict\": {}}",
     "__type__": "vector_store"
   }
   ```

   

# 5. Indexing

- 关于Index的不同种类：[How Each Index Works]([How Each Index Works | LlamaIndex Python Documentation](https://developers.llamaindex.ai/python/framework/module_guides/indexing/index_guide/))

- 此处只讨论最符合RAG理念的[Vector Store Index](https://developers.llamaindex.ai/python/framework/module_guides/indexing/index_guide/#vector-store-index)

- 此外 [Tree Index](https://developers.llamaindex.ai/python/framework/module_guides/indexing/index_guide/#tree-index) 和 [Property Graph Index](https://developers.llamaindex.ai/python/framework/module_guides/indexing/index_guide/#property-graph-index) （知识图谱）值得关注



## 5.1 基础使用

1. 使用

   ```python
   from llama_index.core import VectorStoreIndex
   
   # 构建索引
   index = VectorStoreIndex.from_documents(
       documents,
       storage_context=storage_context
       # transformations=...
   )
   
   # 创建引擎
   retriever = index.as_retriever(similarity_top_k=1)
   query_engine = index.as_query_engine()
   
   # 使用
   result = retriever.retrieve("hello")
   result = query_engine.query("应该推荐那两本书？")
   ```

   

## 5.2 index 常用操作

1. insert

   > You can “insert” a new Document into any index data structure, after building the index initially. This document will be broken down into nodes and ingested into the index.
   >
   > For the vector store index, a new Document (and embeddings) is inserted into the underlying document/embedding store.

   ```python
   index.insert(document=doc)
   ```

   

2. Deletion

   > You can “delete” a Document from most index data structures by specifying a document_id. (**NOTE**: the tree index currently does not support deletion). All nodes corresponding to the document will be deleted.

   ```
   index.delete_ref_doc("doc_id_0", delete_from_docstore=True)
   ```

   

   

3. Document Tracking

   > Any index that uses the docstore (i.e. all indexes except for most vector store integrations), you can also see which documents you have inserted into the docstore.

   ```python
   print(index.ref_doc_info)
   """
   > {'doc_id_1': RefDocInfo(node_ids=['071a66a8-3c47-49ad-84fa-7010c6277479'], metadata={}),
      'doc_id_2': RefDocInfo(node_ids=['9563e84b-f934-41c3-acfd-22e88492c869'], metadata={}),
      'doc_id_0': RefDocInfo(node_ids=['b53e6c2f-16f7-4024-af4c-42890e945f36'], metadata={}),
      'doc_id_3': RefDocInfo(node_ids=['6bedb29f-15db-4c7c-9885-7490e10aa33f'], metadata={})}
   """
   ```

   

4. 注意：insert 和 delete 操作不能保证多数据库的一致性

   特别是 delete 操作，并发时将导致问题
   
   ```python
   # llama_index/core/indices/base.py
   class BaseIndex(Generic[IS], ABC):
               
       def insert(self, document: Document, **insert_kwargs: Any) -> None:
           """Insert a document."""
           with self._callback_manager.as_trace("insert"):
               nodes = run_transformations(
                   [document],
                   self._transformations,
                   show_progress=self._show_progress,
                   **insert_kwargs,
               )
   
               self.insert_nodes(nodes, **insert_kwargs)
               self.docstore.set_document_hash(document.id_, document.hash)
   ```
   
   ```python
   # llama_index/core/indices/vector_store/base.py
   class VectorStoreIndex(BaseIndex[IndexDict]):
       
       def insert_nodes(self, nodes: Sequence[BaseNode], **insert_kwargs: Any) -> None:
           """
           Insert nodes.
   
           NOTE: overrides BaseIndex.insert_nodes.
               VectorStoreIndex only stores nodes in document store
               if vector store does not store text
           """
           self._validate_serializable(nodes)
   
           with self._callback_manager.as_trace("insert_nodes"):
               self._insert(nodes, **insert_kwargs)
               self._storage_context.index_store.add_index_struct(self._index_struct)
               
       def _insert(self, nodes: Sequence[BaseNode], **insert_kwargs: Any) -> None:
           """Insert a document."""
           self._add_nodes_to_index(self._index_struct, nodes, **insert_kwargs)
           
       def _add_nodes_to_index(
           self,
           index_struct: IndexDict,
           nodes: Sequence[BaseNode],
           show_progress: bool = False,
           **insert_kwargs: Any,
       ) -> None:
           """Add document to index."""
           if not nodes:
               return
   
           for nodes_batch in iter_batch(nodes, self._insert_batch_size):
               nodes_batch = self._get_node_with_embedding(nodes_batch, show_progress)
               new_ids = self._vector_store.add(nodes_batch, **insert_kwargs)
   
               if not self._vector_store.stores_text or self._store_nodes_override:
                   # NOTE: if the vector store doesn't store text,
                   # we need to add the nodes to the index struct and document store
                   for node, new_id in zip(nodes_batch, new_ids):
                       # NOTE: remove embedding from node to avoid duplication
                       node_without_embedding = node.model_copy()
                       node_without_embedding.embedding = None
   
                       index_struct.add_node(node_without_embedding, text_id=new_id)
                       self._docstore.add_documents(
                           [node_without_embedding], allow_update=True
                       )
               else:
                   # NOTE: if the vector store keeps text,
                   # we only need to add image and index nodes
                   for node, new_id in zip(nodes_batch, new_ids):
                       if isinstance(node, (ImageNode, IndexNode)):
                           # NOTE: remove embedding from node to avoid duplication
                           node_without_embedding = node.model_copy()
                           node_without_embedding.embedding = None
   
                           index_struct.add_node(node_without_embedding, text_id=new_id)
                           self._docstore.add_documents(
                               [node_without_embedding], allow_update=True
                           )
                           
       def delete_ref_doc(
           self, ref_doc_id: str, delete_from_docstore: bool = False, **delete_kwargs: Any
       ) -> None:
           """Delete a document and it's nodes by using ref_doc_id."""
           self._vector_store.delete(ref_doc_id, **delete_kwargs)
           self._delete_from_index_struct(ref_doc_id)
           if delete_from_docstore:
               self._delete_from_docstore(ref_doc_id)
           self._storage_context.index_store.add_index_struct(self._index_struct)
   ```