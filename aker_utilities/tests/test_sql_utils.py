from unittest.mock import patch
from aker_utilities.sql_utils import (
    _set_authentication,
    set_connection_string,
)


def test_set_authentication_yes() -> None:
    assert _set_authentication(trusted_connection="yes") == ("", "")


def test_set_authentication_test() -> None:
    assert _set_authentication(trusted_connection="test") == ("testuser", "testpwd")


@patch(
    "aker_utilities.sql_utils._get_username_password",
    return_value=("testName", "testPassword"),
)
def test_answer(auth) -> None:
    assert _set_authentication("no") == ("testName", "testPassword")


def test_set_connection_string_is_azure_True_and_is_trusted_connection_Yes() -> None:
    assert (
        set_connection_string(
            server="tcp:myserver.database.windows.net", instance="",
            database="DM_MasterData", port=None,
            is_azure=True, is_trusted_connection="yes"
        ) == (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "Server=tcp:myserver.database.windows.net;"
            "Database=DM_MasterData;"
            "Authentication=Active Directory Integrated;"
        )
    )


def test_set_connection_string_is_azure_True_and_is_trusted_connection_Test() -> None:
    assert (
        set_connection_string(
            server="tcp:myserver.database.windows.net", instance="",
            database="DM_MasterData", port=666,
            is_azure=True, is_trusted_connection="test"
        ) == (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "Server=tcp:myserver.database.windows.net,666;"
            "Database=DM_MasterData;"
            "Uid=testuser;PWD=testpwd;"
            "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30"
        )
    )


@patch(
    "aker_utilities.sql_utils._get_username_password",
    return_value=("testName", "testPassword")
)
def test_set_connection_string_is_azure_True_and_is_trusted_connection_No(auth) -> None:
    assert (
        set_connection_string(
            server="tcp:myserver.database.windows.net", instance="",
            database="DM_MasterData", port=666,
            is_azure=True, is_trusted_connection="no"
        ) == (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "Server=tcp:myserver.database.windows.net,666;"
            "Database=DM_MasterData;"
            "Uid=testName;PWD=testPassword;"
            "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30"
        )
    )


def test_set_connection_string_is_azure_False_and_is_trusted_connection_Test() -> None:
    assert (
        set_connection_string(
            server="DWH-SQL-PROD", instance="XPERTBI", database="DM_MasterData",
            port=666, is_azure=False, is_trusted_connection="test"
        ) == (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "Server=DWH-SQL-PROD\\XPERTBI"
            ",666;"
            "Database=DM_MasterData;"
            "UID=testuser;PWD=testpwd;"
        )
    )


def test_set_connection_string_is_azure_False_and_is_trusted_connection_Yes() -> None:
    assert (
        set_connection_string(
            server="DWH-SQL-PROD", instance="XPERTBI", database="DM_MasterData",
            port=None, is_azure=False, is_trusted_connection="yes"
        ) == (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "Server=DWH-SQL-PROD\\XPERTBI;"
            "Database=DM_MasterData;"
            "Trusted_Connection=yes;"
        )
    )


@patch(
    "aker_utilities.sql_utils._get_username_password",
    return_value=("testName", "testPassword")
)
def test_set_connection_string_is_azure_False_and_is_trusted_connection_No(auth) -> None:
    assert (
        set_connection_string(
            server="DWH-SQL-PROD", instance="XPERTBI", database="DM_MasterData",
            port=666, is_azure=False, is_trusted_connection="no"
        ) == (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "Server=DWH-SQL-PROD\\XPERTBI"
            ",666;"
            "Database=DM_MasterData;"
            "UID=testName;PWD=testPassword;"
        )
    )
