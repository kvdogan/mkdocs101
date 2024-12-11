from aker_utilities.cdf_utils import create_cognite_db_extractor_config


def test_create_cognite_db_extractor_config() -> None:
    config = {
        "cdf_prod_synergi": {
            "project": "akerbp",
            "destination": "synergi",
            "token_url": "https://login.microsoftonline.com/3b7e4170-8348-4aa4-bfae-06a3e1867469/oauth2/v2.0/token",
            "client_id": "7ed10d54-11dc-4102-ad65-dcef7ba7cf2d",
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

    assert str(create_cognite_db_extractor_config(
        user_config=config,
        dwh_config_key="ods_dm_synergi_prod",
        cdf_config_key="cdf_prod_synergi",
    )) == "{'version': '2.1.2', 'logger': {'file': {'level': 'INFO', 'path': 'logs\\\\info.log', 'retention': 7}}, 'cognite': {'project': 'akerbp', 'idp-authentication': {'token-url': 'https://login.microsoftonline.com/3b7e4170-8348-4aa4-bfae-06a3e1867469/oauth2/v2.0/token', 'client-id': '7ed10d54-11dc-4102-ad65-dcef7ba7cf2d', 'secret': None, 'scopes': ['https://api.cognitedata.com/.default']}}, 'extractor': {'state-store': {'local': {'path': 'state\\\\state-store.json', 'save-interval': 60}}}, 'databases': [{'name': 'BI_DetNor_ODS', 'connection-string': 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DWH-SQL-PROD;DATABASE=BI_DetNor_ODS;Trusted_Connection=yes'}, {'name': 'DM_Synergi', 'connection-string': 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DWH-SQL-PROD;DATABASE=DM_Synergi;Trusted_Connection=yes'}], 'queries': [{'name': 'Synergi_3_1_Status', 'database': 'BI_DetNor_ODS', 'query': 'SELECT *, CONVERT(VARCHAR(19), GETDATE(), 126) as _ingestionDT FROM Synergi_3_1_Status', 'primary-key': '{Status_Id}', 'destination-type': 'RAW', 'destination': {'database': 'synergi', 'table': 'Synergi_3_1_Status'}}, {'name': 'Synergi_3_1_StatusDescription', 'database': 'BI_DetNor_ODS', 'query': 'SELECT *, CONVERT(VARCHAR(19), GETDATE(), 126) as _ingestionDT FROM Synergi_3_1_StatusDescription', 'primary-key': '{StatusDescription_Id}', 'destination-type': 'RAW', 'destination': {'database': 'synergi', 'table': 'Synergi_3_1_StatusDescription'}}, {'name': 'Fact_HSSEQ_KPI_Actual', 'database': 'DM_Synergi', 'query': 'SELECT *, CONVERT(VARCHAR(19), GETDATE(), 126) as _ingestionDT FROM Fact_HSSEQ_KPI_Actual', 'primary-key': '{Fact_HSSEQ_KPI_Actual_Id}', 'destination-type': 'RAW', 'destination': {'database': 'synergi', 'table': 'Fact_HSSEQ_KPI_Actual'}}, {'name': 'KPI_HSE', 'database': 'DM_Synergi', 'query': 'SELECT *, CONVERT(VARCHAR(19), GETDATE(), 126) as _ingestionDT FROM KPI_HSE', 'primary-key': '{KPI_HSE_Id}', 'destination-type': 'RAW', 'destination': {'database': 'synergi', 'table': 'KPI_HSE'}}]}"
