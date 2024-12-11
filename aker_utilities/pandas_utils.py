import datetime
import math
import pandas as pd

from aker_utilities.path_utils import checkfile


def dataframe_diff(df1, df2):
    """
    Give difference between two pandas dataframe.
             Date   Fruit   Num   Color
    9  2013-11-25  Orange   8.6  Orange
    8  2013-11-25   Apple  22.1     Red
    """
    df = pd.concat([df1, df2])
    df = df.reset_index(drop=True)

    # group by
    df_gpby = df.groupby(list(df.columns))

    # get index of unique records
    idx = [x[0] for x in df_gpby.groups.values() if len(x) == 1]

    # filter

    return df.reindex(idx)


def dataframe_countif(df, col):
    """
    :param df1: Dataframe
    :param col: Column to count
    """
    new_col = col + "_Count"
    df1 = df.copy()
    df1[new_col] = df1.groupby(col)[col].transform("count")
    return df1


def split_and_export_dataframe(
    df, nrows, sortby=None, output_name=None, export=True
) -> dict[str, pd.DataFrame] | None:
    """
    Split dataframe with given row numbers and return dict or export to csv

    Arguments:
        df {pd.DataFrame} -- Pandas dataframe
        nrows {int} --

    Keyword Arguments:
        sortby {string} --  (default: {None})
        output_name {string} --  (default: {None})
        export {bool} --

    Args:
        df (_type_): _description_
        nrows (_type_): Number of rows to split the database
        sortby (_type_, optional): Sort DataFrame before splitting. Defaults to None.
        output_name (_type_, optional): Output file name, Defaults to None equal to input
        export (bool, optional): Output file format, ';' seperated csv file'.
    """
    if sortby is not None:
        df.sort_values(by=sortby, inplace=True)

    n_iter = int(math.ceil(len(df) / nrows))

    if output_name is None:
        output_name = input("Please name the output file to save: ")

    split_dict = dict()

    for i in range(n_iter):
        split_dict[checkfile(f"{output_name}")] = df[nrows * i: nrows * i + nrows]

    if export:
        for key, value in split_dict.items():
            value.to_csv(checkfile(f"{key}.csv"), sep=";", index=False)
    else:
        return split_dict


def get_hierarchy_as_list(
    main_df,
    tag_list,
    lookup_for="children",
    exclude_list=None,
    sub_level=None,
    tag_column="Functional Location",
    parent_column="Superior functional location",
    print_details=True,
):
    r"""
    Retrieve parent tags or children tags as a dataframe for a given tag lists

    Arguments:
        main_df {pandas.Dataframe} -- Tag
        tag_list {list} -- Reference Tag list

    Keyword Arguments:
        lookup_for {str} -- Either 'children' or 'parents'. Defaults to 'children'
        exclude_list {list} -- List of tags that will be excluded from final output
        (default: {None})
        sub_level {int} -- Level of parent or children tags (default: {None})
        tag_column {str} -- Name of the tag in main_df (default: {'Functional Location'})
        parent_column {str} -- Name of the parent tag column in main_df
        (default: {'Superior functional location'})

    Returns:
        [pandas.Dataframe] -- [Output of desired list of parents or children]
    """
    if lookup_for == "children":
        tag_field = tag_column
        parent_field = parent_column
        sublevel_direction = lambda x: -abs(x)  # noqa: E731
    elif lookup_for == "parents":
        tag_field = parent_column
        parent_field = tag_column
        sublevel_direction = lambda x: abs(x)  # noqa: E731
    else:
        raise (
            AttributeError(
                "lookup_for keyword argument must be either 'parents' or 'children'"
            )
        )

    # Extracting initial dataframe as sublevel=0 from df['sap'] with initial taglist.
    df_out = main_df[main_df[tag_column].isin(tag_list)].copy()
    # assigning column values to empty dataframe with loc #10017
    df_out["Sublevel"] = 0
    tags = df_out[tag_field].tolist()

    if sub_level is not None:
        ctr = 1
        if print_details:
            print("Total number of tags: " + str(len(tags)) + " at level-" + str(ctr - 1))
        # Extracting all upto given sublevel starting from the initial taglist
        while ctr <= sub_level:
            df_temp = main_df[main_df[parent_field].isin(tags)].copy()
            # assigning column values to empty dataframe with loc #10017
            df_temp["Sublevel"] = sublevel_direction(ctr)
            df_out = df_out.append(df_temp)
            tags = df_temp[tag_field].tolist()
            if print_details:
                print("Total number of tags: " + str(len(tags)) + " at level-" + str(ctr))
            ctr += 1
    else:
        ctr = 1
        if print_details:
            print("Total number of tags: " + str(len(tags)) + " at level-" + str(ctr - 1))
        # Extracting all the sublevel starting from the initial taglist
        while len(tags) > 0:
            df_temp = main_df[main_df[parent_field].isin(tags)].copy()
            df_temp["Sublevel"] = sublevel_direction(ctr)
            df_out = df_out.append(df_temp)
            tags = df_temp[tag_field].tolist()
            if print_details:
                print("Total number of tags: " + str(len(tags)) + " at level-" + str(ctr))
            ctr += 1

    # Drop duplicates with the subset of Functional Location
    df_out = df_out.drop_duplicates(subset=[tag_column], keep="last")

    # Filtering out tags which already exist in AlignIT.
    if exclude_list:
        df_out = df_out[~df_out[tag_column].isin(exclude_list)]

    return df_out


def sort_groupby_hierarchical(
    orig_df: pd.DataFrame, export: bool = False
) -> pd.DataFrame:
    """
    Examines all the columns in dataframe and sort by number of unique values and group by
    in that order, so that it reprensents hierarchical model

    Args:
        orig_df (pd.DataFrame): _description_
    """
    df = orig_df.copy()
    df.fillna("NA", inplace=True)

    unique_values = dict()
    for col in df.columns.tolist():
        if not col.startswith("__"):
            unique_values[col] = len(df[col].unique().tolist())

    sorted_dict = dict(sorted(unique_values.items(), key=lambda item: item[1]))
    sorted_columns_list = [key for key in sorted_dict.keys()]

    df["fakecount"] = "NA"

    df = df.groupby(sorted_columns_list).count()

    if export:
        df.to_excel(
            f"{datetime.datetime.now().strftime('%Y-%m-%d--%H-%M-%S')}_export.xlsx"
        )

    return df
