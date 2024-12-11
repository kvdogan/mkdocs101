from typing import Literal, LiteralString

from getpass4 import getpass


def _get_username_password() -> tuple[str, str]:
    """
    Keeping user input seperate from application logic for better testing

    Returns:
        tuple[str, str]: (username, password)
    """
    username = input("Type username: ")
    password = getpass("Type password: ")
    return username, password


def _set_authentication(
    trusted_connection: Literal["yes", "no", "test"] | LiteralString
) -> tuple[str, str]:
    """
    Set username and password for auth depending on three scenarios of:

    Args:
        trusted_connection (str): Options: 'yes', 'no', 'test'

    Raises:
        NotImplementedError: _description_

    Returns:
        tuple[str, str]: Return tuple of username and password.
    """
    trusted_connection = trusted_connection.lower()
    if trusted_connection == "test":
        username = "testuser"
        password = "testpwd"

    elif trusted_connection == "yes":
        username, password = "", ""
    elif trusted_connection == "no":
        username, password = _get_username_password()
    else:
        raise NotImplementedError()

    return username, password


def set_connection_string(
    server: str,
    instance: str,
    port: int | None,
    database: str,
    is_azure: bool,
    is_trusted_connection: Literal["yes", "no", "test"] | LiteralString,
) -> str:
    """Creates connection string for given database

    # PYODBC for DWH DB
    conn = set_connection_string(
        server="DWH-SQL-PROD",
        instance="XPERTBI",
        database="DM_MasterData",
        port=None,
        is_azure=False,
        is_trusted_connection="yes"
    )

    Args:
        server (str): _description_
        instance (str): _description_
        port (int): _description_
        database (str): _description_
        is_azure (bool): _description_
        is_trusted_connection (str): _description_

    Raises:
        NotImplementedError: _description_

    Returns:
        str: _description_
    """
    is_trusted_connection = is_trusted_connection.lower()
    username, password = _set_authentication(is_trusted_connection)
    if is_azure and is_trusted_connection == "yes":
        db_conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"Server={server}{',' + str(port) if type(port)==int else ''};"
            f"Database={database};"
            "Authentication=Active Directory Integrated;"
        )

    elif is_azure and (is_trusted_connection == "no" or is_trusted_connection == "test"):
        db_conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"Server={server}{',' + str(port) if type(port)==int else ''};"
            f"Database={database};"
            f"Uid={username};PWD={password};"
            "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30"
        )

    elif is_azure is False and is_trusted_connection == "yes":
        db_conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"Server={server}{chr(92) + instance if instance != '' else ''}"
            f"{',' + str(port) if type(port)==int else ''};"
            f"Database={database};"
            "Trusted_Connection=yes;"
        )

    elif is_azure is False and (
        is_trusted_connection == "no" or is_trusted_connection == "test"
    ):
        db_conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"Server={server}{chr(92) + instance if instance != '' else ''}"
            f"{',' + str(port) if type(port)==int else ''};"
            f"Database={database};"
            f"UID={username};PWD={password};"
        )

    else:
        raise NotImplementedError()

    return db_conn_str
