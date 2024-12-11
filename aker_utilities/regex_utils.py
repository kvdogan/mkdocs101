import re


def validate_email(email: str) -> bool | ValueError:
    """
    Ensure email is valid using regex pattern matching.

    Args:
        email (str): Email address to validate.

    Raises:
        ValueError: If email is not valid.

    Returns:
        bool | ValueError: True if email is valid, else raise ValueError.
    """
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')

    if email_pattern.match(email):
        return True
    else:
        raise ValueError(f"'{email}' is not a valid email address")


def regex_compile_match(pattern: str, string: str) -> bool:
    """
    To test regex compilation patterns and expected results in parametrized pytest func

    Args:
        string (_type_): _description_

    Returns:
        _type_: _description_
    """
    lookup_pattern = re.compile(pattern)

    if lookup_pattern.match(string):
        return True
    else:
        return False


def convert_to_snake_case(s: str) -> str:
    """
    Convert mixed case string to snake case.

    Args:
        s (str): Text to convert to snake case.

    Returns:
        str:
    """
    words = re.findall(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|_|\d|\W|$)|\d+', s)
    return '_'.join(map(str.lower, words))


def convert_to_camel_case(s: str) -> str:
    # Use regular expression substitution to replace underscores and hyphens with spaces,
    # then title case the string (capitalize the first letter of each word), and remove spaces
    s = re.sub(r"(_|-)+", " ", s).title().replace(" ", "")

    # Join the string, ensuring the first letter is lowercase
    return ''.join([s[0].lower(), s[1:]])


def get_dbname_by_regex(table_name: str) -> str | None:
    """
    Get cleaned dbname out of datawarehouse dbname as shown below.

    Example:
        ```python
        > get_dbname_by_regex("Synergi_3_1_ActionCategory")
        synergi

        > get_dbname_by_regex("SAP_SuccessFactors_1_1_WorkOrder")
        sap_successfactors

        > get_dbname_by_regex("cleanProd_temp")
        cleanprod_temp

        ```

    Args:
        table_name (str): _description_

    Returns:
        str | None: Silently failes by returning None if no match found.
    """
    return re.split(r"_\d", table_name, maxsplit=1)[0].lower()


def get_table_name_by_regex(table_name: str) -> str:
    """
    Get cleaned table name out of datawarehouse db table names as shown below.

    Example:
        ```python
        > get_table_name_by_regex("Synergi_3_1_ActionCategory")
        ActionCategory

        > get_table_name_by_regex("SAP_SuccessFactors_1_1_WorkOrder")
        WorkOrder

        > get_table_name_by_regex("cleanProd_temp")
        cleanProd_temp
        ```

    Args:
        table_name (str): _description_

    Returns:
        str: _description_
    """
    return re.split(r"\d_", table_name)[-1]
