from app.clients.milvus_client import MILVUS_CLIENT
from pymilvus import DataType

schema = MILVUS_CLIENT.create_schema(
    auto_id=True,
    enable_dynamic_field=True,
)

schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=1536)
schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=10000)