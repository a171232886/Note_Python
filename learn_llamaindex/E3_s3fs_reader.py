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