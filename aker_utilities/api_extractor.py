import json
from io import StringIO

import pandas as pd
import requests


class Extractor:
    def __init__(
        self,
        api_key: str,
        auth_keyword: str | None = None,
        data_keywords: list[str] | None = None,
        page_keywords: tuple[str, str] | None = None,
        is_odata: bool = False,
    ):
        """
        _summary_

        Args:
            api_key (str): _description_
            auth_keyword (str | None, optional): Defaults: "Ocp-Apim-Subscription-Key"
                Examples:
                "Ocp-Apim-Subscription-Key" for APIM,
                "Authorization" for SAP PRDFIORI

            data_keywords (list[str] | None, optional): Defaults: ["d", "results"]
            page_keywords (tuple[str, str] | None, optional): Defaults: ("$skip", "$top")
        """
        self.api_key = api_key

        if auth_keyword is None:
            self.auth_keyword = "Ocp-Apim-Subscription-Key"
        else:
            self.auth_keyword = auth_keyword

        if data_keywords is None:
            self.data_keywords = ["d", "results"]
        else:
            self.data_keywords = data_keywords

        if page_keywords is None:
            self.page_keywords = ("$skip", "$top")
        else:
            self.page_keywords = page_keywords

        self.is_odata = is_odata

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Cache-Control": "no-cache",
                self.auth_keyword: self.api_key,
                "Accept": "application/json",
            }
        )

    def get_records(
        self,
        endpoint_tuple: tuple[str, str, str],
        odata_query: str | None = None,
        limit: int | None = None,
    ) -> pd.DataFrame:
        """
        Return desired amount of records for given api endpoints.

        Args:
            endpoint_tuple (tuple[str, str, str]): _description_
            limit (int):  Default to 25 in SDK, set <= 0 for no limit

        ```
        APIM_SAP_ENDPOINTS: dict[str, tuple[str, str, str]] = dict(
            barrier_hierarchy_maintenance_get_barrier_hierarchies=(
                "https://gateway.api.akerbp.com/barrier-hierarchy-maintenance/v1/ZEAM...",
                "barrier-hierarchy-maintenance-get-barrier-hierarchies",
                "{baCharLvl1}-{baCharLvl2}-{baCharLvl3}-{baCharLvl4}-{baCharLvl5}",
            ),
            characteristics_maintenance_characteristics=(
                "https://gateway.api.akerbp.com/characteristics-maintenance/v1/ZEAM_C...",
                "characteristics-maintenance-characteristics",
                "{characteristic}-{characteristicValue}",
            ),
        ```
        Example:
            # For single table extraction
            >>> apim.get_records([APIM_SAP_ENDPOINTS["functional-location-object-type"]])

        Returns:
            dict[str, pd.DataFrame]: _description_
        """
        (api_domain, table_name, table_key) = endpoint_tuple
        (skip_keyword, top_keyword) = self.page_keywords

        print(f"\n{'# '+ table_name +' ':->100}")
        api_limit: int = 50_000
        temp_df: pd.DataFrame = pd.DataFrame()

        if limit is None or limit > api_limit:
            row_count: int = api_limit  # this is set to kick start while loop
            total_row_fetched: int = 0
            skip: int = 0
            while row_count == api_limit:
                if limit is not None and limit > 0:
                    top_n = min(api_limit, limit - total_row_fetched)
                else:
                    top_n = api_limit

                if self.is_odata and odata_query is not None:
                    url = (
                        f"{api_domain}?{skip_keyword}={skip}&{top_keyword}={top_n}"
                        f"&{odata_query}"
                    )
                else:
                    url = f"{api_domain}?{skip_keyword}={skip}&{top_keyword}={top_n}"

                temp = self.session.get(url)

                temp = temp.json()
                for key in self.data_keywords:
                    temp = temp[key]

                temp_df = pd.concat(
                    [
                        temp_df,
                        pd.read_json(StringIO(json.dumps(temp)), dtype=False),
                    ]
                )

                row_count = len(temp)
                print(f"Rows -> {skip:>8} : {skip + row_count:<8} fetched", end="\r")

                skip += row_count
                total_row_fetched += row_count
        else:
            if self.is_odata and odata_query is not None:
                url = f"{api_domain}?{top_keyword}={limit}&{odata_query}"
            else:
                url = f"{api_domain}?{top_keyword}={limit}"

            temp = self.session.get(url)

            temp = temp.json()
            for key in self.data_keywords:
                temp = temp[key]

            temp_df = pd.concat(
                [
                    temp_df,
                    pd.read_json(StringIO(json.dumps(temp)), dtype=False),
                ]
            )

            row_count = len(temp)
            print(f"Rows -> {'0':>8} : {row_count:<8} fetched", end="\r")

        # Make sure logging on console starts a new line for next print after execution
        print("\n")
        return temp_df

    def get_records_from_multiple_endpoints(
        self,
        list_of_endpoint_tuples: list[tuple[str, str, str]],
        list_of_odata_query: list[str] | None = None,
        limit: int | None = None,
    ) -> dict[str, pd.DataFrame]:
        """
        Return table records for given list of api endpoints in alphetical order.
        List

        Args:
            list_of_endpoint_tuples (list[tuple[str, str, str]]):
            limit: Default to 25 in SDK, set <= 0 for no limit

        Example:
            # For multiple table extraction
            >>> apim.get_records_from_multiple_endpoints(
            >>>    list(APIM_SAP_ENDPOINT.values()), limit=1
            >>> )

        Returns:
            dict[str, pd.DataFrame]: _description_
        """
        if list_of_odata_query is None:
            columns = ["" for i in list_of_endpoint_tuples]
            endpoint_query_pairs = list(zip(list_of_endpoint_tuples, columns))
        else:
            assert len(list_of_endpoint_tuples) == len(list_of_odata_query)
            endpoint_query_pairs = list(zip(list_of_endpoint_tuples, list_of_odata_query))

        # Get Table and column dictionary
        api_data_dict: dict[str, pd.DataFrame] = dict()
        for endpoint_tuple, odata_query in sorted(endpoint_query_pairs):
            temp_df = self.get_records(
                endpoint_tuple=endpoint_tuple, odata_query=odata_query, limit=limit
            )

            # table_name = api_endpoint[1]
            api_data_dict[endpoint_tuple[1]] = temp_df.astype(dtype=str)

        return api_data_dict

    def get_columns(
        self,
        endpoint_tuple: tuple[str, str, str],
    ) -> list[str]:
        """
        Return table columns for given list of api endpoints in alphabetical order.
        List

        Args:
            list_of_endpoint_tuples (list[tuple[str, str, str, str, str, str]]):
            List of values used for easy extraction from self.sap_endpoints dictionary,

        Example:
            # For single table extraction
            >>> apim.extract_columns_of_single_endpoint(
            >>>    [APIM_SAP_ENDPOINTS["functional_location_object_type"]]
            >>> )

        Returns:
            list[str]: _description_
        """
        tempdf = self.get_records(endpoint_tuple=endpoint_tuple, limit=1)

        return sorted(tempdf.columns.tolist(), key=str.casefold)

    def get_columns_from_multiple_endpoints(
        self,
        list_of_endpoint_tuples: list[tuple[str, str, str]],
    ) -> dict[str, list[str]]:
        """
        Return table columns for given list of api endpoints in alphabetical order.
        List

        Args:
            list_of_endpoint_tuples (list[tuple[str, str, str, str, str, str]]):
            List of values used for easy extraction from self.sap_endpoints dictionary,

        Example:
            # For multiple table extraction
            >>> apim.get_columns_from_multiple_endpoints(
            >>>     list(APIM_SAP_ENDPOINT.values())
            >>> )

        Returns:
            dict[str, list[str]]: _description_
        """
        col_dict: dict[str, list[str]] = dict()
        for endpoint_tuple in sorted(list_of_endpoint_tuples):
            # table_name = api_endpoint[1]
            col_dict[endpoint_tuple[1]] = self.get_columns(endpoint_tuple)

        return col_dict

    def __str__(self) -> str:
        return f"Generic API Extractor: {self.__class__.__name__}"

    def __repr__(self) -> str:
        return f"Generic API Extractor: {self.__class__.__name__}"
