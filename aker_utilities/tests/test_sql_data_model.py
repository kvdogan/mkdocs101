from pathlib import Path

import pytest

from aker_utilities.sql_data_model import SQLDataModel


def test_sqlite_successful_connection() -> None:
    sqlite_instance = SQLDataModel(
        provider="sqlite", database="__ref/sql_utils/sample.db"
    )
    assert isinstance(sqlite_instance, SQLDataModel)
    assert repr(sqlite_instance) == "SQLDataModel: sqlite/__ref/sql_utils/sample.db conn"


def test_mssql_successful_connection() -> None:
    mssql_instance = SQLDataModel(
        provider="mssql",
        server="DWH-SQL-PROD",
        instance="XPERTBI",
        database="DM_Synergi",
        # port=666,
        is_azure=False,
        is_trusted_connection="yes",
    )

    assert isinstance(mssql_instance, SQLDataModel)
    assert repr(mssql_instance) == "SQLDataModel: mssql/DWH-SQL-PROD/DM_Synergi conn"


def test_postresql_connection_not_implemented_error() -> None:
    with pytest.raises(NotImplementedError):
        SQLDataModel(
            provider="postgresql",
            database="XXX",
        )


def test_mssql_connection_value_error() -> None:
    with pytest.raises(ValueError):
        SQLDataModel(
            provider="mssql",
            database="DM_Synergi",
            # port=666,
            is_azure=False,
            is_trusted_connection="yes",
        )


def test_unknown_provider() -> None:
    with pytest.raises(NotImplementedError):
        SQLDataModel(
            provider="mysql",  # type: ignore
            database="DM_Synergi",
            # port=666,
            is_azure=False,
            is_trusted_connection="yes",
        )


def test_execute_query() -> None:
    sqlite_instance = SQLDataModel(
        provider="sqlite", database="__ref/sql_utils/sample.db"
    )

    assert sqlite_instance.execute_query(sql="SELECT * FROM genres") == [
        {"GenreId": 1, "Name": "Rock"},
        {"GenreId": 2, "Name": "Jazz"},
        {"GenreId": 3, "Name": "Metal"},
        {"GenreId": 4, "Name": "Alternative & Punk"},
        {"GenreId": 5, "Name": "Rock And Roll"},
        {"GenreId": 6, "Name": "Blues"},
        {"GenreId": 7, "Name": "Latin"},
        {"GenreId": 8, "Name": "Reggae"},
        {"GenreId": 9, "Name": "Pop"},
        {"GenreId": 10, "Name": "Soundtrack"},
        {"GenreId": 11, "Name": "Bossa Nova"},
        {"GenreId": 12, "Name": "Easy Listening"},
        {"GenreId": 13, "Name": "Heavy Metal"},
        {"GenreId": 14, "Name": "R&B/Soul"},
        {"GenreId": 15, "Name": "Electronica/Dance"},
        {"GenreId": 16, "Name": "World"},
        {"GenreId": 17, "Name": "Hip Hop/Rap"},
        {"GenreId": 18, "Name": "Science Fiction"},
        {"GenreId": 19, "Name": "TV Shows"},
        {"GenreId": 20, "Name": "Sci Fi & Fantasy"},
        {"GenreId": 21, "Name": "Drama"},
        {"GenreId": 22, "Name": "Comedy"},
        {"GenreId": 23, "Name": "Alternative"},
        {"GenreId": 24, "Name": "Classical"},
        {"GenreId": 25, "Name": "Opera"},
    ]


def test_mssql_table_list_with_regex_pattern() -> None:
    mssql_instance = SQLDataModel(
        provider="mssql",
        server="DWH-SQL-PROD",
        instance="XPERTBI",
        port=None,
        database="BI_DetNor_ODS",
        is_azure=False,
        is_trusted_connection="yes",
        options=None,
    )

    assert mssql_instance.get_tables(
        table_schemas=[
            "dbo",
        ],
        table_regex="^Synergi_3_1_Status((?!Transaction_XBI).)*$",
        tables_to_ignore=None,
    ) == [
        ("dbo", "Synergi_3_1_Status"),
        ("dbo", "Synergi_3_1_StatusDescription"),
    ]


def test_sqlite_table_list_without_regex_pattern() -> None:
    sqlite_instance = SQLDataModel(
        provider="sqlite", database="__ref/sql_utils/sample.db"
    )

    assert sqlite_instance.get_tables(table_regex=None) == [
        ("main", "albums"),
        ("main", "artists"),
        ("main", "customers"),
        ("main", "employees"),
        ("main", "genres"),
        ("main", "invoice_items"),
        ("main", "invoices"),
        ("main", "media_types"),
        ("main", "playlist_track"),
        ("main", "playlists"),
        ("main", "tracks"),
    ]


def test_sqlite_table_columns() -> None:
    sqlite_instance = SQLDataModel(
        provider="sqlite", database="__ref/sql_utils/sample.db"
    )

    assert (
        str(sqlite_instance.get_table_column_properties())
        == "{'albums': [{'name': 'AlbumId', 'type': INTEGER(), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 1}, {'name': 'Title', 'type': NVARCHAR(length=160), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'ArtistId', 'type': INTEGER(), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}], 'artists': [{'name': 'ArtistId', 'type': INTEGER(), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 1}, {'name': 'Name', 'type': NVARCHAR(length=120), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}], 'customers': [{'name': 'CustomerId', 'type': INTEGER(), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 1}, {'name': 'FirstName', 'type': NVARCHAR(length=40), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'LastName', 'type': NVARCHAR(length=20), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'Company', 'type': NVARCHAR(length=80), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'Address', 'type': NVARCHAR(length=70), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'City', 'type': NVARCHAR(length=40), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'State', 'type': NVARCHAR(length=40), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'Country', 'type': NVARCHAR(length=40), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'PostalCode', 'type': NVARCHAR(length=10), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'Phone', 'type': NVARCHAR(length=24), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'Fax', 'type': NVARCHAR(length=24), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'Email', 'type': NVARCHAR(length=60), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'SupportRepId', 'type': INTEGER(), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}], 'employees': [{'name': 'EmployeeId', 'type': INTEGER(), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 1}, {'name': 'LastName', 'type': NVARCHAR(length=20), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'FirstName', 'type': NVARCHAR(length=20), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'Title', 'type': NVARCHAR(length=30), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'ReportsTo', 'type': INTEGER(), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'BirthDate', 'type': DATETIME(), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'HireDate', 'type': DATETIME(), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'Address', 'type': NVARCHAR(length=70), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'City', 'type': NVARCHAR(length=40), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'State', 'type': NVARCHAR(length=40), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'Country', 'type': NVARCHAR(length=40), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'PostalCode', 'type': NVARCHAR(length=10), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'Phone', 'type': NVARCHAR(length=24), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'Fax', 'type': NVARCHAR(length=24), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'Email', 'type': NVARCHAR(length=60), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}], 'genres': [{'name': 'GenreId', 'type': INTEGER(), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 1}, {'name': 'Name', 'type': NVARCHAR(length=120), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}], 'invoice_items': [{'name': 'InvoiceLineId', 'type': INTEGER(), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 1}, {'name': 'InvoiceId', 'type': INTEGER(), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'TrackId', 'type': INTEGER(), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'UnitPrice', 'type': NUMERIC(precision=10, scale=2), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'Quantity', 'type': INTEGER(), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}], 'invoices': [{'name': 'InvoiceId', 'type': INTEGER(), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 1}, {'name': 'CustomerId', 'type': INTEGER(), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'InvoiceDate', 'type': DATETIME(), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'BillingAddress', 'type': NVARCHAR(length=70), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'BillingCity', 'type': NVARCHAR(length=40), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'BillingState', 'type': NVARCHAR(length=40), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'BillingCountry', 'type': NVARCHAR(length=40), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'BillingPostalCode', 'type': NVARCHAR(length=10), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'Total', 'type': NUMERIC(precision=10, scale=2), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}], 'media_types': [{'name': 'MediaTypeId', 'type': INTEGER(), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 1}, {'name': 'Name', 'type': NVARCHAR(length=120), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}], 'playlist_track': [{'name': 'PlaylistId', 'type': INTEGER(), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 1}, {'name': 'TrackId', 'type': INTEGER(), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 2}], 'playlists': [{'name': 'PlaylistId', 'type': INTEGER(), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 1}, {'name': 'Name', 'type': NVARCHAR(length=120), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}], 'tracks': [{'name': 'TrackId', 'type': INTEGER(), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 1}, {'name': 'Name', 'type': NVARCHAR(length=200), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'AlbumId', 'type': INTEGER(), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'MediaTypeId', 'type': INTEGER(), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'GenreId', 'type': INTEGER(), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'Composer', 'type': NVARCHAR(length=220), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'Milliseconds', 'type': INTEGER(), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'Bytes', 'type': INTEGER(), 'nullable': True, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}, {'name': 'UnitPrice', 'type': NUMERIC(precision=10, scale=2), 'nullable': False, 'default': None, 'autoincrement': 'auto', 'primary_key': 0}]}"
    )


def test_mssql_table_columns() -> None:
    mssql_instance = SQLDataModel(
        provider="mssql",
        server="DWH-SQL-PROD",
        instance="XPERTBI",
        port=None,
        database="BI_DetNor_ODS",
        is_azure=False,
        is_trusted_connection="yes",
        options=None,
    )

    assert (
        str(
            mssql_instance.get_table_column_properties(
                table_schemas=[
                    "dbo",
                ],
                table_regex="^Synergi_3_1_Status((?!Transaction_XBI).)*$",
            )
        )
        == "{'Synergi_3_1_Status': [{'name': 'Status_Id', 'type': INTEGER(), 'nullable': False, 'default': None, 'autoincrement': False}, {'name': 'UID_LastChanged', 'type': DATETIME(), 'nullable': False, 'default': None, 'autoincrement': False}, {'name': 'UID_Instance_Id', 'type': INTEGER(), 'nullable': False, 'default': None, 'autoincrement': False}, {'name': 'COLOUR', 'type': INTEGER(), 'nullable': True, 'default': None, 'autoincrement': False}, {'name': 'SEQUENCE', 'type': INTEGER(), 'nullable': True, 'default': None, 'autoincrement': False}, {'name': 'STATUS', 'type': INTEGER(), 'nullable': True, 'default': None, 'autoincrement': False}], 'Synergi_3_1_StatusDescription': [{'name': 'StatusDescription_Id', 'type': INTEGER(), 'nullable': False, 'default': None, 'autoincrement': False}, {'name': 'UID_LastChanged', 'type': DATETIME(), 'nullable': False, 'default': None, 'autoincrement': False}, {'name': 'UID_Instance_Id', 'type': INTEGER(), 'nullable': False, 'default': None, 'autoincrement': False}, {'name': 'Language_Id', 'type': INTEGER(), 'nullable': False, 'default': None, 'autoincrement': False}, {'name': 'Status_Id', 'type': INTEGER(), 'nullable': False, 'default': None, 'autoincrement': False}, {'name': 'DESCRIPTION', 'type': NVARCHAR(length=254), 'nullable': True, 'default': None, 'autoincrement': False}, {'name': 'LANGUAGE', 'type': INTEGER(), 'nullable': True, 'default': None, 'autoincrement': False}, {'name': 'STATUS', 'type': INTEGER(), 'nullable': True, 'default': None, 'autoincrement': False}]}"
    )


def test_sqlite_generate_orm_model() -> None:
    sqlite_instance = SQLDataModel(
        provider="sqlite", database="__ref/sql_utils/sample.db"
    )

    assert (
        sqlite_instance.generate_orm_model(
            gen_class="table", table_regex=None, output_folder=None
        )
        == "from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, MetaData, NVARCHAR, Numeric, Table\n\nmetadata = MetaData()\n\n\nt_artists = Table(\n    'artists', metadata,\n    Column('ArtistId', Integer, primary_key=True),\n    Column('Name', NVARCHAR(120)),\n    schema='main'\n)\n\nt_employees = Table(\n    'employees', metadata,\n    Column('EmployeeId', Integer, primary_key=True),\n    Column('LastName', NVARCHAR(20), nullable=False),\n    Column('FirstName', NVARCHAR(20), nullable=False),\n    Column('Title', NVARCHAR(30)),\n    Column('ReportsTo', ForeignKey('main.employees.EmployeeId'), index=True),\n    Column('BirthDate', DateTime),\n    Column('HireDate', DateTime),\n    Column('Address', NVARCHAR(70)),\n    Column('City', NVARCHAR(40)),\n    Column('State', NVARCHAR(40)),\n    Column('Country', NVARCHAR(40)),\n    Column('PostalCode', NVARCHAR(10)),\n    Column('Phone', NVARCHAR(24)),\n    Column('Fax', NVARCHAR(24)),\n    Column('Email', NVARCHAR(60)),\n    Index('IFK_EmployeeReportsTo', 'ReportsTo'),\n    schema='main'\n)\n\nt_genres = Table(\n    'genres', metadata,\n    Column('GenreId', Integer, primary_key=True),\n    Column('Name', NVARCHAR(120)),\n    schema='main'\n)\n\nt_media_types = Table(\n    'media_types', metadata,\n    Column('MediaTypeId', Integer, primary_key=True),\n    Column('Name', NVARCHAR(120)),\n    schema='main'\n)\n\nt_playlists = Table(\n    'playlists', metadata,\n    Column('PlaylistId', Integer, primary_key=True),\n    Column('Name', NVARCHAR(120)),\n    schema='main'\n)\n\nt_albums = Table(\n    'albums', metadata,\n    Column('AlbumId', Integer, primary_key=True),\n    Column('Title', NVARCHAR(160), nullable=False),\n    Column('ArtistId', ForeignKey('main.artists.ArtistId'), nullable=False, index=True),\n    Index('IFK_AlbumArtistId', 'ArtistId'),\n    schema='main'\n)\n\nt_customers = Table(\n    'customers', metadata,\n    Column('CustomerId', Integer, primary_key=True),\n    Column('FirstName', NVARCHAR(40), nullable=False),\n    Column('LastName', NVARCHAR(20), nullable=False),\n    Column('Company', NVARCHAR(80)),\n    Column('Address', NVARCHAR(70)),\n    Column('City', NVARCHAR(40)),\n    Column('State', NVARCHAR(40)),\n    Column('Country', NVARCHAR(40)),\n    Column('PostalCode', NVARCHAR(10)),\n    Column('Phone', NVARCHAR(24)),\n    Column('Fax', NVARCHAR(24)),\n    Column('Email', NVARCHAR(60), nullable=False),\n    Column('SupportRepId', ForeignKey('main.employees.EmployeeId'), index=True),\n    Index('IFK_CustomerSupportRepId', 'SupportRepId'),\n    schema='main'\n)\n\nt_invoices = Table(\n    'invoices', metadata,\n    Column('InvoiceId', Integer, primary_key=True),\n    Column('CustomerId', ForeignKey('main.customers.CustomerId'), nullable=False, index=True),\n    Column('InvoiceDate', DateTime, nullable=False),\n    Column('BillingAddress', NVARCHAR(70)),\n    Column('BillingCity', NVARCHAR(40)),\n    Column('BillingState', NVARCHAR(40)),\n    Column('BillingCountry', NVARCHAR(40)),\n    Column('BillingPostalCode', NVARCHAR(10)),\n    Column('Total', Numeric(10, 2), nullable=False),\n    Index('IFK_InvoiceCustomerId', 'CustomerId'),\n    schema='main'\n)\n\nt_tracks = Table(\n    'tracks', metadata,\n    Column('TrackId', Integer, primary_key=True),\n    Column('Name', NVARCHAR(200), nullable=False),\n    Column('AlbumId', ForeignKey('main.albums.AlbumId'), index=True),\n    Column('MediaTypeId', ForeignKey('main.media_types.MediaTypeId'), nullable=False, index=True),\n    Column('GenreId', ForeignKey('main.genres.GenreId'), index=True),\n    Column('Composer', NVARCHAR(220)),\n    Column('Milliseconds', Integer, nullable=False),\n    Column('Bytes', Integer),\n    Column('UnitPrice', Numeric(10, 2), nullable=False),\n    Index('IFK_TrackAlbumId', 'AlbumId'),\n    Index('IFK_TrackGenreId', 'GenreId'),\n    Index('IFK_TrackMediaTypeId', 'MediaTypeId'),\n    schema='main'\n)\n\nt_invoice_items = Table(\n    'invoice_items', metadata,\n    Column('InvoiceLineId', Integer, primary_key=True),\n    Column('InvoiceId', ForeignKey('main.invoices.InvoiceId'), nullable=False, index=True),\n    Column('TrackId', ForeignKey('main.tracks.TrackId'), nullable=False, index=True),\n    Column('UnitPrice', Numeric(10, 2), nullable=False),\n    Column('Quantity', Integer, nullable=False),\n    Index('IFK_InvoiceLineInvoiceId', 'InvoiceId'),\n    Index('IFK_InvoiceLineTrackId', 'TrackId'),\n    schema='main'\n)\n\nt_playlist_track = Table(\n    'playlist_track', metadata,\n    Column('PlaylistId', ForeignKey('main.playlists.PlaylistId'), primary_key=True, nullable=False),\n    Column('TrackId', ForeignKey('main.tracks.TrackId'), primary_key=True, nullable=False, index=True),\n    Index('IFK_PlaylistTrackTrackId', 'TrackId'),\n    schema='main'\n)\n"
    )


def test_mssql_generate_orm_model() -> None:
    mssql_instance = SQLDataModel(
        provider="mssql",
        server="DWH-SQL-PROD",
        instance="XPERTBI",
        port=None,
        database="BI_DetNor_ODS",
        is_azure=False,
        is_trusted_connection="yes",
        options=None,
    )

    assert (
        mssql_instance.generate_orm_model(
            gen_class="table",
            table_schemas=[
                "dbo",
            ],
            table_regex="^Synergi_3_1_Status((?!Transaction_XBI).)*$",
            output_folder=None,
        )
        == "from sqlalchemy import Column, DateTime, ForeignKeyConstraint, Integer, MetaData, PrimaryKeyConstraint, Table, Unicode\n\nmetadata = MetaData()\n\n\nt_Synergi_3_1_Language = Table(\n    'Synergi_3_1_Language', metadata,\n    Column('Language_Id', Integer),\n    Column('UID_LastChanged', DateTime, nullable=False),\n    Column('UID_Instance_Id', Integer, nullable=False),\n    Column('DESCRIPTION', Unicode(80)),\n    Column('FLG_ACTIVE', Integer),\n    Column('FLG_REGENERATE_INDEX', Integer),\n    Column('FLG_UNICODE', Integer),\n    Column('LANGUAGE', Integer),\n    Column('LANGUAGE_CODE_ISO', Unicode(9)),\n    Column('LOCALE_ID', Integer),\n    Column('UNICODE_MAX_LENGTH_PERCENT', Integer),\n    PrimaryKeyConstraint('Language_Id', name='PK_Synergi_3_1_Language'),\n    schema='dbo'\n)\n\nt_Synergi_3_1_Status = Table(\n    'Synergi_3_1_Status', metadata,\n    Column('Status_Id', Integer),\n    Column('UID_LastChanged', DateTime, nullable=False),\n    Column('UID_Instance_Id', Integer, nullable=False),\n    Column('COLOUR', Integer),\n    Column('SEQUENCE', Integer),\n    Column('STATUS', Integer),\n    PrimaryKeyConstraint('Status_Id', name='PK_Synergi_3_1_Status'),\n    schema='dbo'\n)\n\nt_Synergi_3_1_StatusDescription = Table(\n    'Synergi_3_1_StatusDescription', metadata,\n    Column('StatusDescription_Id', Integer),\n    Column('UID_LastChanged', DateTime, nullable=False),\n    Column('UID_Instance_Id', Integer, nullable=False),\n    Column('Language_Id', Integer, nullable=False),\n    Column('Status_Id', Integer, nullable=False),\n    Column('DESCRIPTION', Unicode(254)),\n    Column('LANGUAGE', Integer),\n    Column('STATUS', Integer),\n    ForeignKeyConstraint(['Language_Id'], ['dbo.Synergi_3_1_Language.Language_Id'], name='FK_Synergi_3_1_StatusDescription_Language_Id'),\n    ForeignKeyConstraint(['Status_Id'], ['dbo.Synergi_3_1_Status.Status_Id'], name='FK_Synergi_3_1_StatusDescription_Status_Id'),\n    PrimaryKeyConstraint('StatusDescription_Id', name='PK_Synergi_3_1_StatusDescription'),\n    schema='dbo'\n)\n"
    )


def test_sqlite_generate_orm_model_export_true() -> None:
    sqlite_instance = SQLDataModel(
        provider="sqlite", database="__ref/sql_utils/sample.db"
    )

    sqlite_instance.generate_orm_model(
        gen_class="table",
        output_folder=Path("aker_utilities", "tests", "data", "orm_exports"),
    )

    orm_path = Path(
        "aker_utilities",
        "tests",
        "data",
        "orm_exports",
        f"{Path(sqlite_instance.database).stem}.py",
    )

    assert orm_path.exists() is True

    orm_path.unlink()


def test_mssql_generate_orm_model_export_true() -> None:
    mssql_instance = SQLDataModel(
        provider="mssql",
        server="DWH-SQL-PROD",
        instance="XPERTBI",
        port=None,
        database="BI_DetNor_ODS",
        is_azure=False,
        is_trusted_connection="yes",
        options=None,
    )

    mssql_instance.generate_orm_model(
        gen_class="table",
        table_regex="^Synergi_3_1_Status((?!Transaction_XBI).)*$",
        output_folder=Path("aker_utilities", "tests", "data", "orm_exports"),
    )

    orm_path = Path(
        "aker_utilities",
        "tests",
        "data",
        "orm_exports",
        f"{mssql_instance.server}-{mssql_instance.database}.py",
    )

    assert orm_path.exists() is True

    orm_path.unlink()


def test_sqlite_generate_sql_ddl() -> None:
    sqlite_instance = SQLDataModel(
        provider="sqlite", database="__ref/sql_utils/sample.db"
    )

    assert (
        sqlite_instance.generate_sql_ddl(output_folder=None)
        == """\nCREATE TABLE main.albums (\n\t"AlbumId" INTEGER NOT NULL, \n\t"Title" NVARCHAR(160) NOT NULL, \n\t"ArtistId" INTEGER NOT NULL, \n\tPRIMARY KEY ("AlbumId"), \n\tFOREIGN KEY("ArtistId") REFERENCES artists ("ArtistId")\n)\n\n\nCREATE TABLE main.artists (\n\t"ArtistId" INTEGER NOT NULL, \n\t"Name" NVARCHAR(120), \n\tPRIMARY KEY ("ArtistId")\n)\n\n\nCREATE TABLE main.customers (\n\t"CustomerId" INTEGER NOT NULL, \n\t"FirstName" NVARCHAR(40) NOT NULL, \n\t"LastName" NVARCHAR(20) NOT NULL, \n\t"Company" NVARCHAR(80), \n\t"Address" NVARCHAR(70), \n\t"City" NVARCHAR(40), \n\t"State" NVARCHAR(40), \n\t"Country" NVARCHAR(40), \n\t"PostalCode" NVARCHAR(10), \n\t"Phone" NVARCHAR(24), \n\t"Fax" NVARCHAR(24), \n\t"Email" NVARCHAR(60) NOT NULL, \n\t"SupportRepId" INTEGER, \n\tPRIMARY KEY ("CustomerId"), \n\tFOREIGN KEY("SupportRepId") REFERENCES employees ("EmployeeId")\n)\n\n\nCREATE TABLE main.employees (\n\t"EmployeeId" INTEGER NOT NULL, \n\t"LastName" NVARCHAR(20) NOT NULL, \n\t"FirstName" NVARCHAR(20) NOT NULL, \n\t"Title" NVARCHAR(30), \n\t"ReportsTo" INTEGER, \n\t"BirthDate" DATETIME, \n\t"HireDate" DATETIME, \n\t"Address" NVARCHAR(70), \n\t"City" NVARCHAR(40), \n\t"State" NVARCHAR(40), \n\t"Country" NVARCHAR(40), \n\t"PostalCode" NVARCHAR(10), \n\t"Phone" NVARCHAR(24), \n\t"Fax" NVARCHAR(24), \n\t"Email" NVARCHAR(60), \n\tPRIMARY KEY ("EmployeeId"), \n\tFOREIGN KEY("ReportsTo") REFERENCES employees ("EmployeeId")\n)\n\n\nCREATE TABLE main.genres (\n\t"GenreId" INTEGER NOT NULL, \n\t"Name" NVARCHAR(120), \n\tPRIMARY KEY ("GenreId")\n)\n\n\nCREATE TABLE main.invoice_items (\n\t"InvoiceLineId" INTEGER NOT NULL, \n\t"InvoiceId" INTEGER NOT NULL, \n\t"TrackId" INTEGER NOT NULL, \n\t"UnitPrice" NUMERIC(10, 2) NOT NULL, \n\t"Quantity" INTEGER NOT NULL, \n\tPRIMARY KEY ("InvoiceLineId"), \n\tFOREIGN KEY("InvoiceId") REFERENCES invoices ("InvoiceId"), \n\tFOREIGN KEY("TrackId") REFERENCES tracks ("TrackId")\n)\n\n\nCREATE TABLE main.invoices (\n\t"InvoiceId" INTEGER NOT NULL, \n\t"CustomerId" INTEGER NOT NULL, \n\t"InvoiceDate" DATETIME NOT NULL, \n\t"BillingAddress" NVARCHAR(70), \n\t"BillingCity" NVARCHAR(40), \n\t"BillingState" NVARCHAR(40), \n\t"BillingCountry" NVARCHAR(40), \n\t"BillingPostalCode" NVARCHAR(10), \n\t"Total" NUMERIC(10, 2) NOT NULL, \n\tPRIMARY KEY ("InvoiceId"), \n\tFOREIGN KEY("CustomerId") REFERENCES customers ("CustomerId")\n)\n\n\nCREATE TABLE main.tracks (\n\t"TrackId" INTEGER NOT NULL, \n\t"Name" NVARCHAR(200) NOT NULL, \n\t"AlbumId" INTEGER, \n\t"MediaTypeId" INTEGER NOT NULL, \n\t"GenreId" INTEGER, \n\t"Composer" NVARCHAR(220), \n\t"Milliseconds" INTEGER NOT NULL, \n\t"Bytes" INTEGER, \n\t"UnitPrice" NUMERIC(10, 2) NOT NULL, \n\tPRIMARY KEY ("TrackId"), \n\tFOREIGN KEY("AlbumId") REFERENCES albums ("AlbumId"), \n\tFOREIGN KEY("GenreId") REFERENCES genres ("GenreId"), \n\tFOREIGN KEY("MediaTypeId") REFERENCES media_types ("MediaTypeId")\n)\n\n\nCREATE TABLE main.media_types (\n\t"MediaTypeId" INTEGER NOT NULL, \n\t"Name" NVARCHAR(120), \n\tPRIMARY KEY ("MediaTypeId")\n)\n\n\nCREATE TABLE main.playlist_track (\n\t"PlaylistId" INTEGER NOT NULL, \n\t"TrackId" INTEGER NOT NULL, \n\tPRIMARY KEY ("PlaylistId", "TrackId"), \n\tFOREIGN KEY("PlaylistId") REFERENCES playlists ("PlaylistId"), \n\tFOREIGN KEY("TrackId") REFERENCES tracks ("TrackId")\n)\n\n\nCREATE TABLE main.playlists (\n\t"PlaylistId" INTEGER NOT NULL, \n\t"Name" NVARCHAR(120), \n\tPRIMARY KEY ("PlaylistId")\n)\n\n"""
    )


def test_mssql_generate_sql_ddl() -> None:
    mssql_instance = SQLDataModel(
        provider="mssql",
        server="DWH-SQL-PROD",
        instance="XPERTBI",
        port=None,
        database="BI_DetNor_ODS",
        is_azure=False,
        is_trusted_connection="yes",
        options=None,
    )

    assert (
        mssql_instance.generate_sql_ddl(
            table_schemas=[
                "dbo",
            ],
            table_regex="^Synergi_3_1_Status((?!Transaction_XBI).)*$",
            output_folder=None,
        )
        == """\nCREATE TABLE dbo."Synergi_3_1_Status" (\n\t"Status_Id" INTEGER NOT NULL, \n\t"UID_LastChanged" DATETIME NOT NULL, \n\t"UID_Instance_Id" INTEGER NOT NULL, \n\t"COLOUR" INTEGER NULL, \n\t"SEQUENCE" INTEGER NULL, \n\t"STATUS" INTEGER NULL, \n\tCONSTRAINT "PK_Synergi_3_1_Status" PRIMARY KEY ("Status_Id")\n)\n\n\nCREATE TABLE dbo."Synergi_3_1_StatusDescription" (\n\t"StatusDescription_Id" INTEGER NOT NULL, \n\t"UID_LastChanged" DATETIME NOT NULL, \n\t"UID_Instance_Id" INTEGER NOT NULL, \n\t"Language_Id" INTEGER NOT NULL, \n\t"Status_Id" INTEGER NOT NULL, \n\t"DESCRIPTION" NVARCHAR(254) COLLATE Danish_Norwegian_CI_AS NULL, \n\t"LANGUAGE" INTEGER NULL, \n\t"STATUS" INTEGER NULL, \n\tCONSTRAINT "PK_Synergi_3_1_StatusDescription" PRIMARY KEY ("StatusDescription_Id"), \n\tCONSTRAINT "FK_Synergi_3_1_StatusDescription_Language_Id" FOREIGN KEY("Language_Id") REFERENCES dbo."Synergi_3_1_Language" ("Language_Id"), \n\tCONSTRAINT "FK_Synergi_3_1_StatusDescription_Status_Id" FOREIGN KEY("Status_Id") REFERENCES dbo."Synergi_3_1_Status" ("Status_Id")\n)\n\n\nCREATE TABLE dbo."Synergi_3_1_Language" (\n\t"Language_Id" INTEGER NOT NULL, \n\t"UID_LastChanged" DATETIME NOT NULL, \n\t"UID_Instance_Id" INTEGER NOT NULL, \n\t"DESCRIPTION" NVARCHAR(80) COLLATE Danish_Norwegian_CI_AS NULL, \n\t"FLG_ACTIVE" INTEGER NULL, \n\t"FLG_REGENERATE_INDEX" INTEGER NULL, \n\t"FLG_UNICODE" INTEGER NULL, \n\t"LANGUAGE" INTEGER NULL, \n\t"LANGUAGE_CODE_ISO" NVARCHAR(9) COLLATE Danish_Norwegian_CI_AS NULL, \n\t"LOCALE_ID" INTEGER NULL, \n\t"UNICODE_MAX_LENGTH_PERCENT" INTEGER NULL, \n\tCONSTRAINT "PK_Synergi_3_1_Language" PRIMARY KEY ("Language_Id")\n)\n\n"""
    )


def test_posgresql_generate_sql_ddl() -> None:
    ...
    pass


def test_sqlite_generate_sql_ddl_export_true() -> None:
    sqlite_instance = SQLDataModel(
        provider="sqlite", database="__ref/sql_utils/sample.db"
    )

    sqlite_instance.generate_sql_ddl(
        output_folder=Path("aker_utilities", "tests", "data", "ddl_exports")
    )

    ddl_path = Path(
        "aker_utilities",
        "tests",
        "data",
        "ddl_exports",
        f"{Path(sqlite_instance.database).stem}.sql",
    )

    assert ddl_path.exists() is True

    ddl_path.unlink()


def test_mssql_generate_sql_ddl_export_true() -> None:
    mssql_instance = SQLDataModel(
        provider="mssql",
        server="DWH-SQL-PROD",
        instance="XPERTBI",
        port=None,
        database="BI_DetNor_ODS",
        is_azure=False,
        is_trusted_connection="yes",
        options=None,
    )

    mssql_instance.generate_sql_ddl(
        table_regex="^Synergi_3_1_Status((?!Transaction_XBI).)*$",
        output_folder=Path("aker_utilities", "tests", "data", "ddl_exports"),
    )

    ddl_path = Path(
        "aker_utilities",
        "tests",
        "data",
        "ddl_exports",
        f"{mssql_instance.server}-{mssql_instance.database}.sql",
    )

    assert ddl_path.exists() is True

    ddl_path.unlink()
