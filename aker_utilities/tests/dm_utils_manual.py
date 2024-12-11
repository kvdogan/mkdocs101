from aker_utilities.graph_data_model import GraphqlDataModel
from pathlib import Path
from IO_utils import write_list_to_txt


gql = GraphqlDataModel(Path("__ref", "gql_utils", "advancedDB.gql"))
# gql.export_sql_dll(path=Path("__ref", "gql_utils", "advancedDB.sql"))

type_attr_dict = gql.type_fields
type_attr_dict = gql.export_type_fields(
    path=Path("__ref", "gql_utils", "advancedDB_type_attr.json")
)

attr_list = gql.get_type_attributes_only()
write_list_to_txt(
    attr_list, full_path_txt=Path("__ref", "gql_utils", "advancedDB_attributes.txt")
)

print("Paused")
