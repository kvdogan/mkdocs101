import atexit
import json
import os
import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Literal

import pandas as pd
from cognite.client._cognite_client import CogniteClient
from cognite.client.config import ClientConfig
from cognite.client.credentials import OAuthClientCredentials, Token
from cognite.client.data_classes import TableList
from cognite.client.data_classes.data_modeling.views import ViewList
from cognite.client.data_classes.filters import Equals

# from cognite.client.data_classes import TransformationSchedule
from cognite.client.data_classes.transformations import (
    Transformation,
    TransformationList,
    common,
)
from cognite.client.data_classes.transformations.notifications import (
    TransformationNotification,
)
from msal import PublicClientApplication, SerializableTokenCache

from aker_utilities.api_extractor import Extractor
from aker_utilities.IO_utils import write_dict_to_yaml
from aker_utilities.regex_utils import get_table_name_by_regex, validate_email


class CDF:
    def __init__(
        self,
        client_name: str,
        project: Literal[
            "abp",
            "abp-dev",
            "abp-test",
            "akerbp",
            "akerbp-dev",
            "akerbp-test",
            "akerbp-sandbox",
        ],
        client_id: str,
        tenant_id: str,
        client_secret: str | None = None,
        port: int = 53000,
    ):
        """


        Args:
            client_name (str): _description_
            project (Literal["abp", "abp-dev", "abp-test", "akerbp", "akerbp-dev", "akerbp-test", "akerbp-sandbox"]): Should be one of the given AkerBP tenant
            client_id (str): Client ID for Azure AD
            tenant_id (str): Tenant ID for Azure AD
            client_secret (str | None, optional): For non interactive auth
            port (int, optional): Defaults to 53000.
        """
        self.client_name = client_name
        self.project = project
        self.port = port
        self.client = self._set_client_connection(
            client_name=self.client_name,
            project=self.project,
            client_id=client_id,
            tenant_id=tenant_id,
            client_secret=client_secret,
        )

    def _set_client_connection(
        self,
        client_name: str,
        project: str,
        client_id: str,
        tenant_id: str,
        client_secret: str | None = None,
    ) -> CogniteClient:

        ROOT_FOLDER = Path.cwd()
        TOKEN_FILENAME: str = "AUTH_CACHE.bin"
        TOKEN_CACHE_PATH = Path(ROOT_FOLDER, TOKEN_FILENAME)

        def _read_cached_credentials() -> dict:
            """Return stored 2FA credentials if we have them."""
            try:
                return json.loads(TOKEN_CACHE_PATH.read_text())
            except FileNotFoundError:
                return {}

        def _is_access_token_valid() -> bool:
            """Check if the token is still valid."""
            read_token = _read_cached_credentials()["AccessToken"]

            return datetime.now() < datetime.fromtimestamp(
                int(read_token[next(iter(read_token))]["expires_on"])
            )

        def _create_cache() -> SerializableTokenCache:
            """
            Reads cache and validates the access token. If the token is not valid, it will
            ask token interactively by default and at the end of the program it will save
            newly fetched token to the cache.

            Returns:
                SerializableTokenCache: _description_
            """
            cache = SerializableTokenCache()
            if TOKEN_CACHE_PATH.exists() and _is_access_token_valid():
                cache.deserialize(open(TOKEN_CACHE_PATH, "r").read())

            atexit.register(
                lambda: (
                    open(TOKEN_CACHE_PATH, "w").write(cache.serialize())
                    if cache.has_state_changed
                    else None
                )
            )
            return cache

        def _authenticate_azure(app) -> dict:
            # Firstly, check the cache to see if this end user has signed in before
            accounts = app.get_accounts()
            if accounts:
                creds = app.acquire_token_silent(SCOPES, account=accounts[0])
            else:
                # interactive login
                # Make sure you have http://localhost:port in Redirect URI
                # App Registration as type "Mobile and desktop applications"
                creds = app.acquire_token_interactive(
                    scopes=SCOPES,
                    port=self.port,
                )

            return creds

        def _get_token() -> Any:
            cred = _authenticate_azure(app)
            if cred is not None:
                # Setting environment variable "CDF_ACCESS_TOKEN" to access ToKen directly
                os.environ["CDF_ACCESS_TOKEN"] = cred["access_token"]
                return cred["access_token"]
            else:
                return None

        AUTHORITY_HOST_URI: str = "https://login.microsoftonline.com"
        AUTHORITY_URI: str = f"{AUTHORITY_HOST_URI}/{tenant_id}"

        # Set correct cluster for Google or Azure backend
        if project in ["akerbp", "akerbp-dev", "akerbp-test", "akerbp-sandbox"]:
            CDF_CLUSTER: str = "api"
        elif project in ["abp", "abp-dev", "abp-test"]:
            CDF_CLUSTER: str = "az-ams-sp-002"
        else:
            raise ValueError(
                "Check project name, must be one of the following projects: "
                "akerbp, akerbp-dev, akerbp-test, akerbp-sandbox, abp, abp-dev, abp-test"
            )

        BASE_URL: str = f"https://{CDF_CLUSTER}.cognitedata.com"
        SCOPES: list[str] = [f"https://{CDF_CLUSTER}.cognitedata.com/.default"]

        if client_secret is None:
            app = PublicClientApplication(
                client_id=client_id, authority=AUTHORITY_URI, token_cache=_create_cache()
            )

            config = ClientConfig(
                client_name=client_name,
                project=project,
                credentials=Token(_get_token),
                base_url=BASE_URL,
                timeout=300,
            )
        else:
            creds = OAuthClientCredentials(
                client_id=client_id,
                token_url=AUTHORITY_URI + "/oauth2/v2.0/token",
                scopes=SCOPES,
                client_secret=client_secret,
            )

            config = ClientConfig(
                client_name=client_name,
                project=project,
                credentials=creds,
                base_url=BASE_URL,
                timeout=300,
            )

        client = CogniteClient(config)

        return client

    def get_tables(self, db_name: str) -> list[str]:
        """
            List all the tables in alphetical order for the given database in CDF.

            Args:
                dbname (str): Name of the database i.e. e2e-maintenance-sap

            Raises:
                ValueError: _description_

            Returns:
                list[str]: _description_
        """
        # Get All tables for dbname="e2e-maintenance-sap",
        cdf_tables: TableList = self.client.raw.tables.list(db_name, limit=-1)
        cdf_table_names: list = [i.name for i in cdf_tables]
        return sorted(cdf_table_names)

    def get_records(
        self,
        db_name: str,
        table_name: str,
        min_last_updated_time: int | None = None,
        max_last_updated_time: int | None = None,
        columns: list[str] | None = None,
        limit: int | None = None,
    ) -> pd.DataFrame:
        """
        _summary_

        Args:
            db_name (str): _description_
            table_name (str): _description_
            min_last_updated_time (int | None, optional): _description_. Defaults to None.
            max_last_updated_time (int | None, optional): _description_. Defaults to None.
            columns (list[str] | None, optional): _description_. Defaults to None.
            limit (int | None, optional): _description_. Defaults to None.

        Returns:
            pd.DataFrame: _description_
        """
        print(f"\n{'# Fetching records from ' + table_name + ' ':->100}")
        records = self.client.raw.rows.retrieve_dataframe(
            db_name,
            table_name,
            min_last_updated_time,
            max_last_updated_time,
            columns,
            limit,
        )
        print(f"Rows -> {len(records):>8} fetched")

        return records

    def get_records_from_multiple_tables(
        self,
        db_name: str,
        tables: list[str] | None = None,
        min_last_updated_time: int | None = None,
        max_last_updated_time: int | None = None,
        columns: list[str] | None = None,
        limit: int | None = None,
    ) -> dict[str, pd.DataFrame]:
        """
        _summary_

        Args:
            db_name (str): _description_
            tables (list[str] | None, optional): _description_. Defaults to None.
            min_last_updated_time (int | None, optional): _description_. Defaults to None.
            max_last_updated_time (int | None, optional): _description_. Defaults to None.
            columns (list[str] | None, optional): _description_. Defaults to None.
            limit (int | None, optional): _description_. Defaults to None.

        Raises:
            TypeError: _description_

        Returns:
            dict[str, pd.DataFrame]: _description_
        """
        if tables is None:
            cdf_tables = self.get_tables(db_name=db_name)
        elif isinstance(tables, list):
            cdf_tables = tables
        else:
            raise TypeError("Check given tables, must be either one of list or None")

        # Get Table and column dictionary
        records_dict: dict[str, pd.DataFrame] = dict()

        for tbl in cdf_tables:
            records_dict[tbl] = self.get_records(
                db_name=db_name,
                table_name=tbl,
                min_last_updated_time=min_last_updated_time,
                max_last_updated_time=max_last_updated_time,
                columns=columns,
                limit=limit,
            )

        return records_dict

    def get_columns(self, db_name: str, table_name: str) -> list[str]:
        """
        _summary_

        Args:
            db_name (str): _description_
            table_name (str): _description_
        """
        records = self.get_records(db_name=db_name, table_name=table_name, limit=1)

        return sorted(records.columns.tolist(), key=str.casefold)

    def get_columns_from_multiple_tables(
        self, db_name: str, tables: list | None
    ) -> dict[str, list[str]]:
        """
        _summary_

        Args:
            db_name (str): _description_
            tables (str | list | None): _description_

        Raises:
            NameError: _description_

        Returns:
            dict[str, list[str]]: _description_
        """

        table_columns: dict[str, list[str]] = dict()

        if isinstance(tables, list):
            cdf_tables = tables

        elif tables is None:
            cdf_tables = self.get_tables(db_name=db_name)

        else:
            raise TypeError("Check given tables, must be either one of list or None")

        for tbl in cdf_tables:
            table_columns[tbl] = self.get_columns(db_name=db_name, table_name=tbl)

        return table_columns

    def delete_records(self, db_name: str, table_name: str, key: list[str]) -> None:
        """
        _summary_

        Args:
            db_name (str): _description_
            table_name (str): _description_
            key (list[str]): _description_
        """
        print(f"Deleting given records from {db_name}:{table_name} ...")
        self.client.raw.rows.delete(db_name=db_name, table_name=table_name, key=key)

    def delete_tables(self, db_name: str, tables: str | list[str] | None) -> None:
        """
        _summary_

        Args:
            db_name (str): _description_
            tables (str | list[str] | None): _description_

        Raises:
            NameError: _description_
        """
        if isinstance(tables, str):
            cdf_tables = [
                tables,
            ]
        elif isinstance(tables, list):
            cdf_tables = tables

        elif tables is None:
            cdf_tables = self.get_tables(db_name=db_name)

        else:
            raise NameError(
                "Check given tables, must be either one of string, list or None"
            )

        for i in enumerate(sorted(cdf_tables), start=1):
            print(f"{i[0]:>2} - {i[1]}")

        confirm = input(
            f"Total {len(cdf_tables)} tables shown above above will be deleted.."
            "Do you confirm?(yes/no) -> "
        )

        if confirm.lower() == "yes":
            self.client.raw.tables.delete(db_name, cdf_tables)
            print(f"{tables} deleted from {db_name}")
        else:
            print("Delete operation has been canceled!")

    def insert_records_into_raw(
        self,
        dbname: str,
        table_name: str,
        dataframe: pd.DataFrame,
        ensure_parent: bool = False,
    ) -> None:
        self.client.raw.rows.insert_dataframe(
            dbname, table_name, dataframe, ensure_parent
        )

    def get_stale_records(
        self,
        db_name: str,
        tables: list[str] | None,
        field: str,
        records_before: datetime,
        export_details: bool = False,
    ) -> dict[str, list[str | None]]:
        """
        This function is used to find stale records in a given list of tables in a given
        database. By stale records we mean records that are older than the latest record
        in the given table identified by _ingestionDT datetime field.

        Datetime filter for stale records is the older one among the max _ingestionDT and
        given records_before datetime argument. 6 hours of buffer is added to selection.

        Export details option is used to export all the keys with ingestionDT for each

        Args:
            db_name (str): _description_
            tables (list[str] | None): _description_
            field (str): _description_
            records_before (datetime): _description_
            export_details (bool, optional): _description_. Defaults to False.

        Returns:
            dict[str, list[str | None]]: _description_
        """

        table_keys_to_delete = dict()
        table_keys_with_ingestionDT = dict()

        if tables is None:
            list_of_tables = self.get_tables(db_name=db_name)
        else:
            list_of_tables = tables

        for table in sorted(list_of_tables):
            print(
                f"\n{table} analyze start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            rows = self.client.raw.rows.list(db_name, table, limit=None)

            max_ingestionDT = max(
                set(
                    [
                        datetime.fromisoformat(
                            i.columns.get(field, "1900-01-01T00:00:00")
                        )
                        for i in rows
                        if i.columns is not None
                    ]
                )
            )

            # Get desired datetime for making comparison, however if this is later than
            # max_ingestionDT, use max_ingestionDT to protect from deleting all records
            stale_record_dt_filter = min(records_before, max_ingestionDT) - timedelta(
                hours=6
            )

            keys_to_delete = [
                i.key
                for i in rows
                if i.columns is not None
                and datetime.fromisoformat(i.columns.get(field, "1900-01-01T00:00:00"))
                < stale_record_dt_filter
            ]

            if export_details:
                keys_to_delete_with_ingestionDT = [
                    " | ".join([str(i.key), i.columns.get(field, "1900-01-01T00:00:00")])
                    for i in rows
                    if i.columns is not None
                    and datetime.fromisoformat(
                        i.columns.get(field, "1900-01-01T00:00:00")
                    )
                    < stale_record_dt_filter
                ]

                table_keys_with_ingestionDT[table] = keys_to_delete_with_ingestionDT

            table_keys_to_delete[table] = keys_to_delete
            print(
                f"{table} analyze end  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Row Count:{len(rows)}"
            )

        with open(f"{db_name}_stale_records_{datetime.today().date()}.json", "w") as ff:
            json.dump(table_keys_to_delete, ff, indent=4)

        if export_details:
            with open(
                f"{db_name}_stale_records_{datetime.today().date()}_detailed.log", "w"
            ) as ff:
                json.dump(table_keys_with_ingestionDT, ff, indent=4)

        return table_keys_to_delete

    ######################################################################################
    # ## CDF transformations
    ######################################################################################
    def get_transformations(
        self, destination_type: str | None = None, owner: str | None = None
    ) -> TransformationList | list[Transformation]:
        """
        Get list of transformations based on destination_type and user email arguments

        Example:
            ```python
            tslist = get_transformations(
                destination_type="data_model_instances",
                owner="kahraman.v.dogan@akerbp.com"
            )
            ```

        Args:
            destination_type (str | None, optional): _description_. Defaults to None.
            owner (str | None, optional): _description_. Defaults to None.

        Returns:
            list: _description_
        """
        list_of_trans = self.client.transformations.list(limit=-1)

        if destination_type is not None:
            list_of_trans = [
                i
                for i in list_of_trans
                if i.destination.type == destination_type  # type: ignore
            ]

        if owner is not None:
            list_of_trans = [
                i for i in list_of_trans if i.owner["user"] == owner  # type: ignore
            ]

        return list_of_trans

    def create_model_transformation(
        self, list_of_transformation_dict: list[dict[str, Any]]
    ) -> None:
        """
        Create transformation for given list of transformation dictionaries

        Example:
            ```python
            list_of_transformation_dict = [
                dict(
                        space="E2E",
                        model="SAP",
                        type_name="Asset",
                        version="1",
                        trans_external_id="E2E:Asset_1",
                        trans_name="E2E:Asset_1",
                        query='''
                SELECT DISTINCT
                concat_ws(":", "E2E", "Asset", `flocMainAsset`) as `externalId`,
                string(`flocMainAsset`) as `flocMainAsset`
                FROM `e2e-maintenance-sap`.`functional-location-functional-location-metadata`;
                ''',
                        notification="kahraman.v.dogan@akerbp.com",
                        data_set_id=1613619045197736    # dataset:e2e-maintenance-sap
                    ),
            ]
            ```

        Args:
            model_transformation_list (list[dict[Any, Any]]): _description_

        """
        # TODO: Fix setting credentials upon creating transformation
        # credentials = common.OidcCredentials(
        #     client_id=os.getenv("TRANSFORMATIONS_CLIENT_ID"),
        #     client_secret=os.getenv("TRANSFORMATIONS_CLIENT_SECRET"),
        #     token_uri=os.getenv("TRANSFORMATIONS_TOKEN_URL"),
        #     cdf_project_name=os.getenv("TRANSFORMATIONS_CDF_PROJECT")
        # )
        transformations = list()
        for trans in list_of_transformation_dict:
            transformations.append(
                Transformation(
                    # external_id = "E2E:Asset_1"
                    external_id=trans["name"],
                    # name = "E2E:Asset_1"
                    name=trans["name"],
                    query=trans["query"],
                    destination=common.TransformationDestination.instances(
                        data_model=common.DataModelInfo(
                            space=trans["space"],  # E2E
                            external_id=trans["model"],  # SAP
                            version=trans["version"],  # 1
                            destination_type=trans["type_name"],  # Asset
                        ),
                        instance_space=trans["space"],  # E2E
                    ),
                    conflict_mode="upsert",
                    is_public=True,
                    ignore_null_fields=False,
                    data_set_id=int(trans["data_set_id"]),
                    # TODO: Fix setting credentials upon creating transformation
                    # has_source_oidc_credentials=True,
                    # source_oidc_credentials=credentials,
                    # has_destination_oidc_credentials=True,
                    # destination_oidc_credentials=credentials,
                    # TODO: Utilize Schedule automation
                    # schedule=TransformationSchedule(),
                )
            )

        self.client.transformations.create(transformations)

    def update_or_create_model_transformation(
        self,
        list_of_transformation_dict: list[dict[str, str]],
        create: bool = False,
    ) -> None:
        """
        Name must be set to new name to update, external_id must be existing name, after
        update external_id will be set as name, so both will be synced with given as name

        !!! Important
            Reason for using update_or_create_node_transformation rather than
            create_model_transformation upsert functionality is to be able to update
            external_id

        So that external_id and model_instance version are at par.

        Args:
            list_of_transformation_dict (list[dict[str, str]]): _description_

        """
        for trans in list_of_transformation_dict:
            transformation: Transformation | None = self.client.transformations.retrieve(
                external_id=trans["external_id"]
            )
            if transformation is not None:
                print(
                    f"Updating Transformation: {trans['external_id']} -> {trans['name']}"
                )
                transformation.name = trans["name"]
                transformation.external_id = trans["name"]
                transformation.query = trans["query"]

                try:
                    # Standardize transformation properties for node and edge
                    dest_type, dest_rel_from_type = trans["type_name"].split(".")
                except ValueError:
                    dest_type = trans["type_name"]
                    dest_rel_from_type = None

                transformation.destination = common.TransformationDestination.instances(
                    data_model=common.DataModelInfo(
                        space=trans["space"],  # E2E
                        external_id=trans["model"],  # SAP
                        version=trans["version"],  # 1
                        destination_type=dest_type,  # InspectionCode
                        destination_relationship_from_type=dest_rel_from_type,  # catalgPr
                    ),
                    instance_space=trans["space"],  # E2E
                )

                self.client.transformations.update(transformation)
            else:
                if create:
                    print(f"Creating Transformation: {trans['name']}")
                    self.create_model_transformation(
                        [
                            trans,
                        ],
                    )
                else:
                    print(f"Transformation: {trans['external_id']} not found, try create")

    def create_transformation_notifications(
        self, list_of_transformation_dict: list[dict[str, str]]
    ) -> None:
        """
        Creates transformation notifications for given list of transformation dictionaries

        Args:
            list_of_transformation_dict (list[dict[str, str]]): _description_
        """
        notifications_to_add: list = []
        for trans in list_of_transformation_dict:
            # Check if email is valid and no existing notification for that id and email
            if validate_email(trans["notification"]):
                existing_notification = self.client.transformations.notifications.list(
                    transformation_external_id=trans["external_id"],
                    destination=trans["notification"],
                )
                if len(existing_notification) == 0:
                    notifications_to_add.append(
                        (
                            trans["external_id"],
                            TransformationNotification(
                                transformation_external_id=trans["external_id"],
                                destination=trans["notification"],
                            ),
                        )
                    )

        for i in notifications_to_add:
            if isinstance(i[1], TransformationNotification):
                print(f"Subscribe '{i[1].destination}' to '{i[0]}'")
                self.client.transformations.notifications.create(i[1])

    def delete_transformation_notifications(
        self, list_of_transformation_dict: list[dict[str, str]]
    ) -> None:
        """
        Deletes transformation notifications for given list of transformation dictionaries

        Args:
            list_of_transformation_dict (list[dict[str, str]]): _description_
        """
        notifications_to_delete: list = []
        for trans in list_of_transformation_dict:
            if validate_email(trans["notification"]):
                existing_notification = self.client.transformations.notifications.list(
                    transformation_external_id=trans["external_id"],
                    destination=trans["notification"],
                )

                try:
                    notifications_to_delete.append(
                        (trans["external_id"], existing_notification[0])
                    )
                except IndexError:
                    notifications_to_delete.append(
                        (trans["external_id"], existing_notification)
                    )

        for i in notifications_to_delete:
            if isinstance(i[1], TransformationNotification):
                print(f"Unsubscribe '{i[1].destination}' from '{i[0]}'")
                self.client.transformations.notifications.delete(id=i[1].id)

    def run_transformation(
        self, list_of_transformation_dict: list[dict[str, str]]
    ) -> None:
        """
        Run transformation for given list of transformation dictionaries

        Args:
            list_of_transformation_dict (list[dict[str, str]]): _description_
        """
        for trans in list_of_transformation_dict:
            print(f"Running Transformation: {trans['external_id']}")
            self.client.transformations.run(
                transformation_external_id=trans["external_id"], wait=False
            )  # type:ignore

    # Getting multiple transformation schemas and output to a single json
    def get_transformation_schemas(
        self, list_of_transformation_dict: list[dict[str, str]]
    ) -> None:
        """
       Get transformation schemas for given list of transformation dictionaries

        Args:
            data_model_instances (list[tuple[str, str, str]]):
            [(model_id, space_id, instance_space_id), ... ]
        """
        with open("sample_json_schema.json", "w") as ff:
            json_output = dict()
            for trans in list_of_transformation_dict:
                res = self.client.transformations.schema.retrieve(
                    destination=common.TransformationDestination.instances(
                        data_model=common.DataModelInfo(
                            space=trans["space"],  # E2E
                            external_id=trans["model"],  # SAP
                            version=trans["version"],  # 1
                            destination_type=trans["type_name"],  # Asset
                        ),
                        instance_space=trans["space"],  # E2E
                    )
                )

                res_json = res.dump()

                for i in res_json:
                    i["type"] = i["type"].type

                json_output[trans["type_name"]] = res_json

            json.dump(json_output, ff)

    def get_transformation_preview(self, query: str) -> None:
        """
        Pay attention to array types because those can not be converted json,
        however in transformation itself you should not use to_json method unless
        you want json in the column value.

        Example:
            ```python
            query = '''
            Select
                concat_ws(':', 'sap', 'planningPlant', `plantPlanningPlant`) as `externalId`,
                string(`plantPlanningPlant`) as `plantPlanningPlant`,
                collect_set(`plantPlanningPlantDesc`)[0] as `plantPlanningPlantDesc`,
                to_json(collect_set(`plantSystemCondition`)) as `plantSystemCondition`,
                to_json(collect_set(`plantOperationalConsequence`)) as `plantOperationalCons`
            FROM `e2e-maintenance-sap`.`planning-plants-maintenance-ssd-codes`
            GROUP BY `plantPlanningPlant`;'''
            ```
        """
        res = self.client.transformations.preview(query=query)

        with open("preview_json.json", "w") as ff:
            json.dump(res.results, ff)

        print(res.results)

    ######################################################################################
    # ## Data modelling
    ######################################################################################
    def delete_instances_views_containers_for_given_model(
        self,
        space: str,
        model_name: str,
        list_of_views: list[str] | None,
        chunk_size: int = 100,
    ) -> None:
        """
        Clean up existing data model instances, views and containers for given model
        without leaving residues behind

        Args:
            space (str): Name of the model space
            model_name (str): Name of the model
            list_of_views (list[str] | None): List of views to be deleted
            chunk_size (int, optional): Defaults to 100.

        """
        # Models for the given space
        model_object = [
            i
            for i in self.client.data_modeling.data_models.list(space=space, limit=None)
            if i.external_id.lower() == model_name.lower()
        ]

        try:
            model_object = model_object[0]
            model = model_object.dump(camel_case=False)
        except IndexError:
            print(f"Model: {model_name} does not exist in {space}")
            return None

        # Instantiating Views for container and instance_type properties
        if model is not None:
            views = model["views"]
            view_ids = [(i["space"], i["external_id"], i["version"]) for i in views]
            try:
                view_list = self.client.data_modeling.views.retrieve(ids=view_ids)
                view_list = [view for view in view_list if view.external_id != "Metadata"]
            except Exception as e:
                print("Views: ", e)
                view_list = ViewList([])
        else:
            view_list = ViewList([])

        if list_of_views is not None and len(list_of_views) > 0:
            view_list = [i for i in view_list if i.external_id in list_of_views]

        delete_all_or_iterate = input(
            f"{[i.external_id for i in view_list]}"
            f"Would you like to delete ALL above views at once or LOOP through "
            f"selected views and corresponding instances view by view? (ALL | LOOP)?"
        )

        if len(view_list) == 0:
            print(f"Views: {list_of_views} do not exist in {space}")
            return None

        # Deleting instances from views in chunks
        for view in view_list:
            if delete_all_or_iterate.lower() != "all":
                confirm_delete_for_view = input(
                    f"Delete instances from view: {view.external_id}? (yes/n)"
                )
            else:
                confirm_delete_for_view = "yes"

            if confirm_delete_for_view.lower() == "yes":

                idx = 0
                ctr = chunk_size
                while ctr == chunk_size:
                    # Getting instances for that View
                    ins = self.client.data_modeling.instances.list(
                        sources=view,
                        limit=chunk_size,
                        filter=Equals(property=(view.used_for, "space"), value=space),
                    )

                    fetched_instances = len(ins)

                    if fetched_instances > 0:
                        print(
                            f"{view.used_for + '>' +space+ ':' + ins[0].external_id:<95}"
                            f"DEL: {view.used_for.capitalize()}: {idx}-{idx+chunk_size}",
                            end="\r",
                        )
                        self.client.data_modeling.instances.delete(ins.as_ids())
                        ctr = fetched_instances
                        idx += fetched_instances
                    else:
                        ctr = 0

                print(f"\n{idx:>8} {view.used_for}s deleted from {view.external_id }")

            else:
                print(f"\nView: {view.external_id } has been omitted from view list")
                view_list.remove(view)
                continue

        # Deleting Views
        try:
            view_ids = [i.as_id() for i in view_list]
            self.client.data_modeling.views.delete(view_ids)
            print(f"\nTotal number of views have been deleted: {len(view_list)}")
        except Exception as e:
            print("Views: ", e)

        # Deleting Containers
        try:
            container_ids = [(space, i.external_id) for i in view_list]
            container_list = self.client.data_modeling.containers.retrieve(
                ids=container_ids
            )
            self.client.data_modeling.containers.delete(container_list.as_ids())
            print(
                f"\nTotal number of containers have been deleted: {len(container_list)}"
            )
        except Exception as e:
            print("Containers: ", e)

        # Delete Models
        try:
            self.client.data_modeling.data_models.delete(model_object.as_id())
            print(f"\nModel: {model_name} has been deleted")
        except Exception as e:
            print("Model: ", e)

        print("#" * 90, "\n")

    def __str__(self) -> str:
        return (
            f"CDF extended SDK: {{ \n"
            f"    client: {self.client_name}\n"
            f"    project: {self.project}\n"
            f"}}\n"
        )

    def __repr__(self) -> str:
        return f"CDF extended SDK: '{self.client_name}' @ '{self.project}' project"


class PipelineToCDF(ABC):
    def __init__(
        self,
        source: Extractor | Path,
        endpoint: tuple[str, str, str] | None,
        uid_key_list: str | list[str] | None,
        cdf: CDF,
        cdf_db_name: str,
        cdf_table: str,
        limit: int | None = None,
    ) -> None:
        """
        Pipeline to CDF class to push data to CDF from different sources.

        Args:
            source (Extractor | Path): Path to the file or Extractor object
            endpoint (tuple[str, str, str] | None): Required if source is Extractor
            uid_key_list (str | list[str] | None): if None, a unique key will be generated
            cdf (CDF): CDF object
            cdf_db_name (str): CDF database name
            cdf_table (str): CDF table name
            limit (int, optional): Number of rows to read via Extractor. Defaults to 0.
        """
        self.source = source
        self.endpoint = endpoint
        self.cdf = cdf
        self.uid_key_list = uid_key_list
        self.cdf_db_name = cdf_db_name
        self.cdf_table = cdf_table
        self.limit = limit

    def get_data(self) -> None:
        if isinstance(self.source, Path):
            if self.source.suffix == ".csv":
                self.data = pd.read_csv(
                    self.source.absolute(), sep=";", encoding="latin-1"
                )
            elif self.source.suffix == ".xlsx":
                self.data = pd.read_excel(self.source.absolute())
            else:
                raise ValueError("File format not supported")
        elif isinstance(self.source, Extractor) and self.endpoint is not None:
            df = self.source.get_records(
                endpoint_tuple=self.endpoint,
                limit=self.limit,
            )
            self.data: pd.DataFrame = df
        else:
            raise ValueError("Invalid source type")

    def set_table_key(self) -> None | TypeError:
        if self.uid_key_list is None:
            self.data["rawKey"] = [str(uuid.uuid4()) for _ in range(len(self.data.index))]

        elif isinstance(self.uid_key_list, str):
            self.data["rawKey"] = self.data[self.uid_key_list].astype(str)
            self.data["rawKey"] = self.data[self.uid_key_list]

        elif isinstance(self.uid_key_list, list):
            self.data[self.uid_key_list] = self.data[self.uid_key_list].astype(str)
            self.data["rawKey"] = self.data[self.uid_key_list].apply(
                lambda row: "-".join(row.values.astype(str)), axis=1
            )
        else:
            raise TypeError("'uid_key_list' must be either one of types: None, list, str")

        self.data = self.data.set_index("rawKey")

    @abstractmethod
    def transform(self) -> None:
        pass

    @abstractmethod
    def validate(self) -> None:
        if self.uid_key_list is not None:
            assert len(self.data) == len(
                self.data.drop_duplicates(subset=self.uid_key_list)
            )

    def push_data(self) -> None:
        start_row: int = 0
        nrows: int = 100_000

        while start_row < len(self.data):
            self.cdf.insert_records_into_raw(
                dbname=self.cdf_db_name,
                table_name=self.cdf_table,
                dataframe=self.data[start_row : start_row + nrows],  # noqa: E203
                ensure_parent=True,
            )
            print(
                f"Rows -> {start_row:>7} : "
                f"{start_row + len(self.data[start_row: start_row + nrows]):<7}"
                f"pushed successfully"
            )

            start_row += nrows

        print("Data push has been completed!")

    def run_pipeline(self) -> None:
        self.get_data()
        self.transform()
        self.set_table_key()
        self.validate()
        self.push_data()

    def __str__(self) -> str:
        return f"PipelineToCDF from {self.source}"

    def __repr__(self) -> str:
        return f"PipelineToCDF from {self.source}"


def create_cognite_db_extractor_config(
    user_config: Path | dict[str, dict[str, Any]],
    dwh_config_key: str,
    cdf_config_key: str,
    export: bool = False,
) -> dict:
    from aker_utilities.sql_data_model import SQLDataModel

    """
    _summary_


    Args:
        user_config (Path | dict[str, dict[str, str]]): _description_
        config = {
            "cdf_prod_synergi": {
                "project": "akerbp",
                "destination": "synergi",
                "token_url": "https://login.microsoftonline.com/0-8348/oauth2/v2.0/token",
                "client_id": "xxxxx-xxxx-xxxx-xxxx-xxxxxxx",
                "scopes": ["https://api.cognitedata.com/.default"],
            },
            "ods_dm_synergi_prod": {
                "ods_prod_synergi": {
                    "dwh_server": "DWH-SQL-PROD",
                    "dwh_instance": "XPERTBI",
                    "database": "BI_DetNor_ODS",
                    "table_schema": ["dbo", ],
                    "table_regex": "^Synergi_3_1_Status((?!Transaction_XBI).)*$",
                    "expected_table_qty": 2,
                },
                "dm_prod_synergi": {
                    "dwh_server": "DWH-SQL-PROD",
                    "dwh_instance": "XPERTBI",
                    "database": "DM_Synergi",
                    "table_schema": ["dbo", ],
                    "table_regex": ".*KPI_(HSE|Actual)$",
                    "expected_table_qty": 2,
                },
            },
        }

        dwh_config_key (str): _description_
        cdf_config_key (str): _description_

    Raises:
        AssertionError: _description_

    Returns:
        dict: _description_
    """
    # Loading config
    if isinstance(user_config, Path):
        config: dict[str, dict[str, Any]] = json.load(user_config.open())
    else:
        config: dict[str, dict[str, Any]] = dict(user_config)

    # Creating Cognite dbExtractor config with YAML
    project, destination, token_url, client_id, scopes = config[cdf_config_key].values()

    extractor_config: dict = dict(
        version="2.1.2",
        # (Optional) Configure logging to standard out (console) and/or file. Level can
        # be DEBUG, INFO, WARNING or CRITICAL
        logger=dict(
            # # Logging to console/terminal. Remove or comment out to disable terminal
            # console=dict(
            #     level="INFO"
            # ),
            # Logging to file. Remove or comment out to disable file logging
            file=dict(
                level="INFO",
                path="logs\\info.log",
                # (Optional) Log retention (in days).
                retention=7,
            )
        ),
        cognite={
            # # (Optional) CDF deployment to target
            # "host": "https://api.cognitedata.com",
            "project": project,
            # (Either this or idp-authentication is required) API key to use for CDF auth
            "idp-authentication": {
                "token-url": token_url,
                "client-id": client_id,
                "secret": os.environ.get("OIDC_token"),
                "scopes": scopes,
            },
        },
        # (Optional) Extractor performance tuning.
        extractor={
            # # (Optional) Number of rows to fetch from sources before uploading
            # "upload-queue-size": 100_000,
            # (Optional) Where to store extraction states (progress) between runs.
            # Required for incremental load to work.
            "state-store": {
                "local": {"path": "state\\state-store.json", "save-interval": 60},
                # # Uncomment to use a RAW table for state storage
                # "raw": {
                #     # RAW database and table to use
                #     "database": "",
                #     "table": "",
                #     # (Optional) Upload interval (in seconds) for intermediate uploads.
                #     # A final upload will also be made on extractor shutdown.
                #     "upload-interval": 30
                # },
            },
            # # (Optional) Number of queries to execute in parallel
            # "parallelism": 4
        },
        databases=list(),
        queries=list(),
    )

    for key, value_dict in config[dwh_config_key].items():
        (
            dwh_server,
            dwh_instance,
            database,
            table_schema,
            table_regex,
            expected_table_qty,
        ) = value_dict.values()

        sql_data_model = SQLDataModel(
            provider="mssql",
            server=dwh_server,
            instance=dwh_instance,
            database=database,
        )

        table_list = sql_data_model.get_tables(
            table_schemas=table_schema,
            table_regex=table_regex,
        )

        try:
            assert len(table_list) == expected_table_qty
        except AssertionError:
            raise AssertionError(
                f"Expected table qty({expected_table_qty}) != " f"({len(table_list)})"
            )

        # Database section
        if isinstance(extractor_config["databases"], list):
            extractor_config["databases"].append(
                {
                    "name": database,
                    "connection-string": f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={dwh_server};"
                    f"DATABASE={database};"
                    f"Trusted_Connection=yes",
                }
            )

        # Queries section for each database config and filtered table
        # Get synergi table name and Id field as list of tuples
        # Logic between table and its primary id
        table_name_id_field: list[tuple[str, str]] = [
            (name, f"{get_table_name_by_regex(name)}_Id") for schema, name in table_list
        ]

        # Creating dynamic queries
        for table, id_field in table_name_id_field:
            temp_obj = {
                "name": table,
                "database": database,
                "query": "SELECT *, CONVERT(VARCHAR(19), GETDATE(), 126) as _ingestionDT "
                f"FROM {table}",
                "primary-key": f"{{{id_field}}}",
                "destination-type": "RAW",
                "destination": {"database": destination, "table": table},
            }

            if isinstance(extractor_config["queries"], list):
                extractor_config["queries"].append(temp_obj)

    if export:
        # Create folder structure first before exporting yaml to prevent os error
        info = Path("dist", "logs")
        state = Path("dist", "state", "state-store.json")

        info.mkdir(parents=True, exist_ok=True)
        state.parent.mkdir(parents=True, exist_ok=True)
        state.write_text("{}")

        write_dict_to_yaml(
            source_dict=extractor_config,
            export_path=Path(
                "dist", f"{dwh_config_key}_to_{cdf_config_key}_extractor_config.yml"
            ),
        )

    return extractor_config
