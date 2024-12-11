from aker_utilities.regex_utils import (
    validate_email,
    regex_compile_match,
    convert_to_snake_case,
    get_dbname_by_regex,
    get_table_name_by_regex,
)
import pytest


@pytest.mark.parametrize(
    "test_email,expected",
    [
        ("veysel.dgn@gmail.com", True),
        ("123@123.com", True),
    ],
)
def test_validate_email(test_email, expected) -> None:
    assert validate_email(test_email) is expected


@pytest.mark.parametrize(
    "test_email,expected",
    [
        ("kvdogancom", ""),
        ("kvdogan###@gmail.com", ""),
    ],
)
def test_validate_email_raise_error(test_email, expected) -> None:
    with pytest.raises(ValueError, match=f"'{test_email}' is not a valid email address"):
        validate_email(test_email)


@pytest.mark.parametrize(
    "test_pattern, test_string, expected",
    [
        ("^Sy_3_1_((?!Transactions_XBI).)*$", "Sy_3_1_ABC", True),
        ("^Sy_3_1_((?!Transactions_XBI).)*$", "Sy_3_1_Transactions_", True),
        ("^Sy_3_1_((?!Transactions_XBI).)*$", "Sy_3_1_Transactions_XBI_ABC", False),
        (".*KPI_(HSE|Actual)$", "KPI_HSE", True),
        (".*KPI_(HSE|Actual)$", "Fact_HSSEQ_KPI_Actual", True),
        (".*KPI_(HSE|Actual)$", "Fact_HSSEQ_KPI_Actual_Inline", False),
    ],
)
def test_regex_compile_match(test_pattern, test_string, expected) -> None:
    assert regex_compile_match(test_pattern, test_string) is expected


@pytest.mark.parametrize(
    "test_string, expected_return",
    [
        ("UID_Last_Changed", "uid_last_changed"),
        ("ActionStatus_Id", "action_status_id"),
        ("camelCamelCase", "camel_camel_case"),
        ("PascalPascalCase", "pascal_pascal_case"),
        ("Camel2Camel2Case", "camel_2_camel_2_case"),
        ("getHTTPResponseCode", "get_http_response_code"),
        ("get200HTTPResponseCode", "get_200_http_response_code"),
        ("getHTTP200ResponseCode", "get_http_200_response_code"),
        ("HTTPResponseCode", "http_response_code"),
        ("ResponseHTTP", "response_http"),
        ("ResponseHTTP2", "response_http_2"),
        ("Fun?!awesome", "fun_awesome"),
        ("Fun?!Awesome", "fun_awesome"),
        ("10CoolDudes", "10_cool_dudes"),
        ("20coolDudes", "20_cool_dudes"),
    ],
)
def test_convert_to_snake_case(test_string, expected_return) -> None:
    assert convert_to_snake_case(test_string) == expected_return


@pytest.mark.parametrize(
    "dbname, expected_return",
    [
        ("Synergi_3_1_ActionCategory", "synergi"),
        ("SAP_SuccessFactors_1_1_WorkOrder", "sap_successfactors"),
        ("cleanProd_temp", "cleanprod_temp"),
    ],
)
def test_get_dbname_by_regex(dbname, expected_return) -> None:
    assert get_dbname_by_regex(dbname) == expected_return


@pytest.mark.parametrize(
    "table_name, expected_return",
    [
        ("Synergi_3_1_ActionCategory", "ActionCategory"),
        ("SAP_SuccessFactors_1_1_WorkOrder", "WorkOrder"),
        ("cleanProd_temp", "cleanProd_temp"),
    ],
)
def test_get_table_name_by_regex(table_name, expected_return) -> None:
    assert get_table_name_by_regex(table_name) == expected_return
