import json
import os

from graphql import GraphQLSchema, parse
from graphql.utilities import build_ast_schema, lexicographic_sort_schema, print_schema

GEN_TYPE_MAP = (
    ("id", "INT"),
    ("string", "VARCHAR"),
    ("int", "INT"),
    ("float", "FLOAT"),
    ("boolean", "BOOLEAN"),
    ("timestamp", "DATE"),
    ("int64", "BIGINT"),
    ("jsonobject", "JSON"),
    ("timeseries", "JSON"),
)

NULLABLILITY_MAP = (
    ("non_null_type", "NOT NULL"),
    ("named_type", "NULL"),
    ("list_type", "NULL"),
)


class GraphqlDataModel:
    """
    Using graphql-core library(https://github.com/graphql-python/graphql-core) parse funct
    Reason for feeding gen_type_mapping is keeping class loosely bound to different type
    of sql implementation
    """

    def __init__(
        self,
        path: os.PathLike,
        gen_type_mapping: tuple = GEN_TYPE_MAP,
        nullability_mapping: tuple = NULLABLILITY_MAP,
    ) -> None:
        self.path = path
        self.gen_type_mapping = dict(gen_type_mapping)
        self.nullability_mapping = dict(nullability_mapping)
        with open(path, "r") as gql:
            # Read as AST(abstract syntax trees)
            self.graphql_document = parse(gql.read())

        self.graphql_schema = build_ast_schema(self.graphql_document)
        self.graphql_dict = self.graphql_document.to_dict()

    def __str__(self) -> str:
        return f"GraphQL Parser for {self.path}"

    @property
    def datatype_mapping(self) -> dict:
        """
        Finding custom types implemented in the project and updating gen_type_mapping.

        Returns:
            dict: _description_
        """
        datatype_mapping = dict()
        datatype_mapping.update(self.gen_type_mapping)
        datatype_mapping.update(dict([(i.lower(), i) for i in self.types]))

        return datatype_mapping

    @property
    def type_fields(self) -> dict:
        # type_fields = [
        #     (i["name"]["value"], [j["name"]["value"] for j in i["fields"]])
        #     for i in self.graphql_dict["definitions"]
        #     if i["kind"] == "object_type_definition"
        # ]
        type_fields = [
            (
                i["name"]["value"],
                [
                    (
                        j["name"]["value"],
                        GraphqlDataModel._fetch_given_field_properties(j)[0],
                    )
                    for j in i["fields"]
                ],
            )
            for i in self.graphql_dict["definitions"]
            if i["kind"] == "object_type_definition"
        ]

        type_fields_dict = dict(type_fields)

        return type_fields_dict

    @property
    def interface_fields(self) -> dict:
        type_fields = [
            (i["name"]["value"], [j["name"]["value"] for j in i["fields"]])
            for i in self.graphql_dict["definitions"]
            if i["kind"] == "interface_type_definition"
        ]

        type_fields_dict = dict(type_fields)

        return type_fields_dict

    @property
    def types(self) -> list:
        return list(self.type_fields.keys())

    @property
    def interfaces(self) -> list:
        return list(self.interface_fields.keys())

    def _get_standard_datatype(self, datatype: str) -> str:
        try:
            std_type = self.datatype_mapping[datatype.lower()]
        except KeyError:
            std_type = "VARCHAR"

        return std_type

    def _get_nullability(self, null_option: str) -> str:
        try:
            nullable = self.nullability_mapping[null_option.lower()]
        except KeyError:
            nullable = "NULL"

        return nullable

    @staticmethod
    def _fetch_given_field_properties(field_object: dict) -> tuple:
        field_attrs = tuple()
        dt = ""
        try:
            dt = field_object["type"]["type"]["type"]["name"]["value"]
            if dt != "":
                field_attrs = (
                    dt,  # testTypeOne
                    field_object["type"]["kind"],  # not_null_type
                    field_object["type"]["type"]["kind"],  # list_type
                    field_object["type"]["type"]["type"]["kind"],  # named_type
                )
        except KeyError:
            try:
                dt = field_object["type"]["type"]["name"]["value"]
                if dt != "":
                    field_attrs = (
                        dt,  # string
                        field_object["type"]["kind"],  # list_type, not_null
                        field_object["type"]["type"]["kind"],  # named_type
                    )
            except KeyError:
                dt = field_object["type"]["name"]["value"]
                if dt != "":
                    field_attrs = (
                        dt,  # int
                        field_object["type"]["kind"],  # not_null_type, named
                    )

        return field_attrs

    def sort_schema(self) -> GraphQLSchema:
        """
        Sort Schema lexicographically based on type names

        Returns:
            GraphQLSchema: _description_
        """
        return lexicographic_sort_schema(self.graphql_schema)

    def export_graphql_ast(self, path: os.PathLike) -> None:
        """
        Export graphql query as AST(abstract syntax trees) json.

        Args:
            path (str): Pathlike object in json extension
        """
        with open(path, "w") as ff:
            ff.write(json.dumps(self.graphql_dict))

    def export_graphql_schema(
        self,
        path: os.PathLike,
        sort: bool = False,
    ) -> None:
        """
        Export graphql schema in SDL (Schema definition language) to gql file

        Args:
            path (str): Pathlike in gql extension
        """
        if sort:
            schema = self.sort_schema()
        else:
            schema = self.graphql_schema

        with open(path, "w") as ff:
            ff.write(print_schema(schema))

    def export_sql_dll(self, path: os.PathLike) -> None:
        # Creating table as per requirement
        type_fields = dict()
        for gql in self.graphql_dict["definitions"]:
            if gql["kind"] != "object_type_definition":
                continue

            # Get Table name
            table_name = gql["name"]["value"]
            type_fields[table_name] = []

            # Get fields with datatype_mapping, nullability_mapping and cardinality
            for field in gql["fields"]:
                field_parsed = GraphqlDataModel._fetch_given_field_properties(field)
                field_name = field["name"]["value"]
                field_type = self._get_standard_datatype(field_parsed[0])
                field_nullability = self._get_nullability(field_parsed[1])

                if field_parsed[0].lower() == "id":
                    type_fields[table_name] += [
                        (field_name, field_type, field_nullability, "PK")
                    ]

                elif field_type in self.types:
                    # Add FK: ForeignKey as 4th element in case of
                    # datatype exists in table list
                    type_fields[table_name] += [
                        (field_name, field_type, field_nullability, "FK")
                    ]
                else:
                    # NK: NoKey
                    type_fields[table_name] += [
                        (field_name, field_type, field_nullability, "NK")
                    ]

        # Construct SQL-DDL script with type_fields dictionary
        sql = ""

        for table, fields in type_fields.items():
            fields_str = ""
            constraint_str = ""
            for field in fields:
                if field[3] == "PK":
                    constraint_str = f"\tPRIMARY KEY ({fields[0][0]}),\n"
                if field[3] == "FK":
                    fields_str += f"\t{field[0]}\tINT\t{field[2]},\n"
                    ref = type_fields[field[1]][0][0]
                    constraint_str += (
                        f"\tFOREIGN KEY ({field[0]}) REFERENCES {field[1]} ({ref}),\n"
                    )
                else:
                    fields_str += f"\t{field[0]}\t{field[1]}\t{field[2]},\n"

            sql += f"CREATE TABLE {table}\n(\n{fields_str}{constraint_str});\n"

        with open(path, "w") as ff:
            ff.write(sql)

    def export_type_fields(self, path: os.PathLike) -> None:
        """
        This method converts graphql model into python dict like:
            { type_name: ["attrA", "attrB", ...] }

        Gets only types, ignores interfaces, however interface attributes exists in types.

        Args:
            path (os.PathLike | None, optional): If given and it is correct then exports
                                                 dict as json. Defaults to None.

        Example:
            >>> from pathlib import Path
            >>> gql = gql = GraphqlToSql(Path("__ref/gql_utils/advancedDB.gql"))
            >>> file_path = Path("__ref", "gql_utils", "advancedDB.json")
            >>> gql.export_type_fields(path=file_path)

        Returns:
            dict | None: _description_
        """
        with open(path, "w") as ff:
            json.dump(self.type_fields, ff)

    def get_type_attributes_only(self) -> list[str]:
        """
        Exports all unique attributes exists in the model

        Args:
            path (os.PathLike): _description_

        Example:
            >>> from pathlib import Path
            >>> gql = gql = GraphqlToSql(Path("__ref/gql_utils/iso.gql"))
            >>> file_path = Path("__ref", "gql_utils", "all_ISO_attributes.txt")
            >>> gql.export_all_attributes(path=file_path)
        """
        unique_type_fields = set([j for i in self.type_fields.values() for j in i])
        unique_interface_fields = set(
            [j for i in self.interface_fields.values() for j in i]
        )

        all_unique_fields = list(unique_type_fields.union(unique_interface_fields))

        return all_unique_fields
