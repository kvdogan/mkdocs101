import os
import re
from pathlib import Path
from typing import Literal
from urllib.parse import quote_plus

from sqlacodegen.generators import (
    DataclassGenerator,
    DeclarativeGenerator,
    TablesGenerator,
)
from sqlalchemy import MetaData, create_engine, dialects, inspect, text
from sqlalchemy.engine.mock import MockConnection
from sqlalchemy.schema import CreateTable

from aker_utilities.sql_utils import set_connection_string


class SQLDataModel:
    def __init__(
        self,
        provider: Literal["sqlite", "postgresql", "mssql"],
        database: str,
        server: str | None = None,
        instance: str | None = None,
        port: int | None = None,
        is_azure: bool = False,
        is_trusted_connection: Literal["yes", "no", "test"] = "yes",
        options: (
            Literal[
                "noindexes",
                "noconstraints",
                "nocomments",
                "use_inflect",
                "nojoined",
                "nobidi",
            ]
            | None
        ) = None,
    ) -> None:
        """
        Creates an SQL alchemy connection with expanded API.

        Args:
            provider (Literal["sqlite", "postgresql", "mssql"]): Database provider
            database (str): Database name or filepath for sqlite
            server (str | None, optional): ie. "DWH-SQL-PROD' Defaults to None for sqlite.
            instance (str | None, optional): ie. 'XPERTBI' Defaults to None.
            port (int | None, optional): ie. 666. Defaults to None.
            is_azure (bool, optional): Defaults to False.
            is_trusted_connection (Literal["yes", "no", "test"], optional): Def. to "yes"
            options (
                Literal[
                    "noindexes", "noconstraints", "nocomments", "use_inflect", "nojoined",
                    "nobidi"
                ] | None, optional): _description_. Defaults to None.

        Raises:
            NotImplementedError: _description_
            ValueError: Server and instance must be provided if provider is not sqlite.
        """
        self.provider = provider
        self.database = database
        self.server = server
        self.instance = instance
        self.port = port
        self.is_azure = is_azure
        self.is_trusted_connection = is_trusted_connection
        self.options = options

        # Connection
        if self.provider == "sqlite":
            self._db_engine = create_engine(f"sqlite:///{database}")
            self._inspect = inspect(self._db_engine)
        elif self.provider == "postgresql":
            raise NotImplementedError()
            # self._db_engine = create_engine(
            #     f'postgresql+psycopg2://{user}:{password}@{host}/{database}'
            # )
        elif self.provider == "mssql":
            if self.server is not None and self.instance is not None:
                connection_string = set_connection_string(
                    server=self.server,
                    instance=self.instance,
                    port=self.port,
                    database=self.database,
                    is_azure=self.is_azure,
                    is_trusted_connection=self.is_trusted_connection,
                )
                params = quote_plus(connection_string)
                self._db_engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
                self._inspect = inspect(self._db_engine)
            else:
                raise ValueError("Missing server and/or instanca name")
        else:
            raise NotImplementedError(
                f"Database connection for given provider: {provider}has not been "
                "implemented yet, feel free to implement or contact kvdogandev@gmail.com"
            )

    def execute_query(self, sql: str) -> list[dict[str, str]]:
        """
        Executes given sql query on the database and returns the result as a list of dict

        Args:
            sql (str): _description_

        Returns:
            list[dict[str, str]]: _description_
        """
        conn: MockConnection
        with self._db_engine.connect() as conn:  # type: ignore
            results = conn.execute(text(sql))
            return [row._mapping for row in results]

    def get_tables(
        self,
        table_schemas: list[str] | None = None,
        table_regex: str | None = None,
        tables_to_ignore: list[str] | None = None,
    ) -> list[tuple[str, str]]:
        """
        Get list of tables for db connection as a tuple of schema and table

        Args:
            table_schemas (list[str] | None, optional): _description_. Defaults to None.
            table_regex (str | None, optional): _description_. Defaults to None.
            tables_to_ignore (list[str] | None, optional): _description_. Defaults to None

        Returns:
            list[tuple[str, str]]: _description_
        """
        if table_schemas is None and self._inspect is not None:
            table_schemas = [self._inspect.default_schema_name]

        # Configure default regex pattern which matches everything
        if table_regex is None:
            table_regex = "(.*)"

        # Configure default tables_to_ignore and specific case for sqlite
        if tables_to_ignore is None:
            tables_to_ignore = []

        if self.provider == "sqlite":
            tables_to_ignore += ["sqlite_sequence", "sqlite_stat1"]

        table_list = []
        if self._inspect is not None:
            if table_schemas is not None:
                for schema in table_schemas:
                    # Get list of table names for given schema
                    tables_for_schema = self._inspect.get_table_names(schema=schema)
                    # Create a list of tuples[schema, table_name]
                    table_list += list(map(lambda x: (schema, x), tables_for_schema))

        table_pattern = re.compile(table_regex)

        tables = [
            (schema, table_name)
            for schema, table_name in table_list
            if table_pattern.match(table_name) and table_name not in tables_to_ignore
        ]

        return tables

    def get_table_column_properties(
        self,
        table_schemas: list[str] | None = None,
        table_regex: str | None = None,
        tables_to_ignore: list[str] | None = None,
    ) -> dict[str, list[dict[str, str]]]:
        """
        Returns dictionary with table name as key and list of dictionary of column
        properties as values

        Args:
            table_schemas (list[str] | None, optional): _description_. Defaults to None.
            table_regex (str | None, optional): _description_. Defaults to None.
            tables_to_ignore (list[str] | None, optional): _description_. Defaults to None

        Returns:
            dict[str, list[dict[str, str]]]: _description_
        """
        if table_schemas is None and self._inspect is not None:
            table_schemas = [self._inspect.default_schema_name]

        # Configure default regex pattern which matches everything
        if table_regex is None:
            table_regex = "(.*)"

        # Configure default tables_to_ignore and specific case for sqlite
        if tables_to_ignore is None:
            tables_to_ignore = []

        if self.provider == "sqlite":
            tables_to_ignore += ["sqlite_sequence", "sqlite_stat1"]

        tables = self.get_tables(table_schemas, table_regex, tables_to_ignore)

        column_table_dict = dict()
        if self._inspect is not None:
            for schema, table_name in tables:
                column_table_dict[table_name] = self._inspect.get_columns(
                    table_name, schema=schema
                )

        return column_table_dict

    def generate_orm_model(
        self,
        gen_class: Literal["table", "declarative", "dataclass"],
        table_schemas: list[str] | None = None,
        table_regex: str | None = None,
        tables_to_ignore: list[str] | None = None,
        output_folder: os.PathLike | None = None,
    ) -> str:
        """
        Generates ORM model for given database connection and exports to a file named with
        database name if output folder is provided.

        Example:

        ```python
        prod_bi_detnor_ods_synergi = SqlDataModel(
            provider="mssql",
            server="DWH-SQL-PROD",
            instance="XPERTBI",
            port=None,
            database="BI_DetNor_ODS",
            is_azure=False,
            is_trusted_connection="Yes",
            options=None,
        )

        prod_bi_detnor_ods_synergi.generate_orm_model(
            gen_class="table",
            output_folder=Path("TableGen_DWHPROD_BIDetNorODS_SynergiStatus.py")
        )
        ```
        Args:
            gen_class (Literal["table", "declarative", "dataclass"]): _description_
            table_schemas (list[str] | None, optional): _description_. Defaults to None.
            table_regex (str | None, optional): _description_. Defaults to None.
            tables_to_ignore (list[str] | None, optional): _description_. Defaults to None
            output_folder (os.PathLike | None, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        metadata = MetaData()

        if table_schemas is None and self._inspect is not None:
            table_schemas = [self._inspect.default_schema_name]

        # Configure default regex pattern which matches everything
        if table_regex is None:
            table_regex = "(.*)"

        # Configure default tables_to_ignore and specific case for sqlite
        if tables_to_ignore is None:
            tables_to_ignore = []

        if self.provider == "sqlite":
            tables_to_ignore += ["sqlite_sequence", "sqlite_stat1"]

        tables = [
            i[1] for i in self.get_tables(table_schemas, table_regex, tables_to_ignore)
        ]

        if table_schemas is not None:
            for sch in table_schemas:
                metadata.reflect(bind=self._db_engine, schema=sch, only=tables)

        gen_class_dict = {
            "table": TablesGenerator,
            "declarative": DeclarativeGenerator,
            "dataclass": DataclassGenerator,
        }

        gen = gen_class_dict[gen_class](
            metadata, self._db_engine, set(self.options or ())
        )

        orm_model = gen.generate()

        if isinstance(output_folder, os.PathLike):
            # Create folder structure first before exporting yaml to prevent os error
            if self.provider == "sqlite":
                export_path = Path(self.database).stem
            else:
                export_path = f"{self.server}-{self.database}".replace("/", "-").replace(
                    "\\", "-"
                )

            dm_export = Path(output_folder, f"{export_path}.py")
            dm_export.parent.mkdir(parents=True, exist_ok=True)

            with open(dm_export.absolute(), "w", encoding="utf-8") as ff:
                ff.write(orm_model)

        return orm_model

    def generate_sql_ddl(
        self,
        table_schemas: list[str] | None = None,
        table_regex: str | None = None,
        tables_to_ignore: list[str] | None = None,
        keep_brackets: bool = False,
        output_folder: os.PathLike | None = None,
    ) -> str:
        """
        Generates ORM model for given database connection and exports to a file named with
        database name if output folder is provided.

        Example:
        ```python
        prod_bi_detnor_ods_synergi = DbModel(
            provider="mssql",
            server="DWH-SQL-PROD",
            instance="XPERTBI",
            port=None,
            database="BI_DetNor_ODS",
            is_azure=False,
            is_trusted_connection="Yes",
            options=None,
            table_schemas=None,
            table_regex="^Synergi_3_1_Status((?!Transaction_XBI).)*$",
            tables_to_ignore=None
        )

        prod_bi_detnor_ods_synergi.generate_ddl(
            outputfile="DDL-DWH-PROD-BI_DetNorODS-Synergi_Status.sql"
        )
        ```

        Args:
            table_schemas (list[str] | None, optional): _description_. Defaults to None.
            table_regex (str | None, optional): _description_. Defaults to None.
            tables_to_ignore (list[str] | None, optional): _description_. Defaults to None
            keep_brackets (bool, optional): _description_. Defaults to False.
            export (bool, optional): _description_. Defaults to False.

        Returns:
            str: _description_
        """
        metadata = MetaData()

        if self.provider == "sqlite":
            db_dialect = dialects.sqlite.dialect()  # type: ignore
        elif self.provider == "postgresql":
            db_dialect = dialects.postgresql.dialect()  # type: ignore
        elif self.provider == "mssql":
            db_dialect = dialects.mssql.dialect()  # type: ignore

        if table_schemas is None and self._inspect is not None:
            table_schemas = [self._inspect.default_schema_name]

        # Configure default regex pattern which matches everything
        if table_regex is None:
            table_regex = "(.*)"

        # Configure default tables_to_ignore and specific case for sqlite
        if tables_to_ignore is None:
            tables_to_ignore = []

        if self.provider == "sqlite":
            tables_to_ignore += ["sqlite_sequence", "sqlite_stat1"]

        tables = [
            i[1] for i in self.get_tables(table_schemas, table_regex, tables_to_ignore)
        ]

        if table_schemas is not None:
            for sch in table_schemas:
                metadata.reflect(bind=self._db_engine, schema=sch, only=tables)

        tables_ddl = ""
        if isinstance(metadata.tables, dict):
            for table in metadata.tables.values():
                # Important dialect.mssql creates script with brackets which vuerd doesn't
                # handle, so that we must replace brackets with quotes same as postgresql
                # dialect, however postgresql dialect fails for some cases that is special
                # to mssql databases. Thus this is a temp solution.
                table_sql = str(
                    CreateTable(table).compile(dialect=db_dialect)  # type: ignore
                )
                if not keep_brackets:
                    table_sql = table_sql.replace("[", '"').replace("]", '"')

                tables_ddl += table_sql

        if isinstance(output_folder, os.PathLike):
            # Create folder structure first before exporting yaml to prevent os error
            if self.provider == "sqlite":
                export_path = Path(self.database).stem
            else:
                export_path = f"{self.server}-{self.database}".replace("/", "-").replace(
                    "\\", "-"
                )

            dm_export = Path(output_folder, f"{export_path}.sql")
            dm_export.parent.mkdir(parents=True, exist_ok=True)

            with open(dm_export.absolute(), "w", encoding="utf-8") as ff:
                ff.write(tables_ddl)

        return tables_ddl

    def generate_graphql_model(self, outputfile: Path) -> None:
        ...
        pass

    def __repr__(self) -> str:
        if self.provider == "sqlite":
            return f"SQLDataModel: {self.provider}/{self.database} conn"
        else:
            return f"SQLDataModel: {self.provider}/{self.server}/{self.database} conn"
