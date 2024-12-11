import collections
import os
import re
import warnings
from tkinter import Tk, filedialog, messagebox

import pandas as pd
import xlrd as xl
import xlsxwriter
from aker_utilities.path_utils import get_filepaths


def combine_multiple_csv_into_excel(full_path_to_folder, sep="\t", encoding="latin1"):
    r"""
    Combine csv files that can be converted to Dataframe and have same exact structure.
    :param full_path_to_folder:
    :param sep: Text separator, default is '\t'
    :param encoding: Text encoding, default is 'latin1'
    :return: excel file with one extra column showing the name of the file.
    """
    csv_files: list[str] = sorted(get_filepaths(full_path_to_folder))
    folder_name = os.path.split(full_path_to_folder)[
        1
    ]  # For folder location and folder name

    df_base = pd.read_csv(csv_files[0], sep=sep, encoding=encoding, low_memory=False)
    df_base["File_Name"] = os.path.splitext(os.path.split(csv_files[0])[1])[0]

    for i in csv_files[1:]:
        df_temp = pd.read_csv(i, sep=sep, encoding=encoding, low_memory=False)
        file_name = os.path.splitext(os.path.split(i)[1])[0]
        df_temp["File_Name"] = file_name

        df_base = pd.concat([df_base, df_temp])

    df_base.to_excel("{}\\{}.xlsx".format(full_path_to_folder, folder_name))


def split_worksheets(file: str) -> None:
    """
    :param file: Excel file to be split by its worksheets.
    :return:
    """
    dfs_to_split = pd.read_excel(io=file, sheet_name=None)
    # 'None' used as worksheet kwarg thus it could be read as Dataframe dict.
    dfs_to_split = collections.OrderedDict(sorted(dfs_to_split.items()))
    for k, v in dfs_to_split.items():
        export_file_name = os.path.join(os.path.split(file)[0], "{}.xlsx".format(k))
        writer = pd.ExcelWriter(export_file_name, engine="xlsxwriter")
        v.to_excel(excel_writer=writer, sheet_name=str(k), index=False)
        writer.close()


def convert_to_hyperlink(x):
    """
    Converts pandas column given in apply function to hyperlink for excel export

    Usage:
        df['Link'] = df['Link'].apply(convert_to_hyperlink)

    Returns:
        DataFrame -- Creates or modifies given DataFrame column
    """
    if "#" in x:
        return "'#' in file path is not allowed in Excel Hyperlinks"
    else:
        return f'=HYPERLINK("{x}", "Click to Open")'


def export_file_names(file_type=None, use_relative_path=True):
    """
    Walk through the folder structures and creates excel file with hyperlink.
    to every single file

    Keyword Arguments:
        file_type {string} -- File extension i.e. ".xls" (default: {None})
        use_relative_path {bool} -- Relative paths to selected folder (default: {True})
    """
    window = Tk()
    window.wm_withdraw()
    warnings.filterwarnings("ignore")  # xlsx writer hyperlink for 255+ char
    folder = filedialog.askdirectory(
        title="Please choose the folder to extract file names"
    )
    filenames = get_filepaths(folder)
    if file_type is None or not isinstance(file_type, str):
        filenames = [i for i in filenames if "$" not in i]
    else:
        filenames = [
            i for i in filenames if str(i).lower().endswith(file_type) and "$" not in i
        ]

    df = pd.DataFrame(data=filenames, columns=["Path"])
    df["FileName"] = df["Path"].apply(lambda x: os.path.split(x)[1])

    if use_relative_path:
        df["Link"] = df["Path"].apply(lambda x: os.path.relpath(x, folder))
    else:
        df["Link"] = df["Path"]

    df["Link"] = df["Link"].apply(convert_to_hyperlink)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(
        os.path.join(os.path.join(folder, "____Link2Files____.xlsx")),
        engine="xlsxwriter",
    )
    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name="Link2Files", index=False)
    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    worksheet = writer.sheets["Link2Files"]
    # Add some cell formats.
    custom_hyperlink_format = workbook.add_format(  # type: ignore
        {
            "font_color": "blue",
            # 'bold':       1,
            "underline": 1,
            "font_size": 12,
        }
    )
    # Note: It isn't possible to format any cells that already have a format such
    # as the index or headers or any cells that contain dates or datetimes.
    # Set the format but not the column width.
    worksheet.set_column("C:C", None, custom_hyperlink_format)
    # Close the Pandas Excel writer and output the Excel file.
    writer.close()

    messagebox.showinfo(title="Complete", message="Done!", detail="")


def outlined_hierarchy(
    txtfile,
    sysname="HVAC_sample",
    sysno="97_sample",
    wkbk="Outlined_Hierarchy_sample.xlsx",
    ws="Hierarchy",
):
    """
    Create a hierarchical structure from the given file by looking parent and child
    Arguments:
        txtfile {[type]} -- Structured txt file which is the output of hierarchy tree algo

    Keyword Arguments:
        sysname {str} -- Name of the system (default: {"HVAC_sample"})
        sysno {str} -- Number of the system (default: {"97_sample"})
        wkbk {str} -- Name for output file (default: {"Outlined_Hierarchy_sample.xlsx"})
        ws {str} -- Name for excel sheey (default: {"Hierarchy"})
    """
    ff = open(txtfile, "r", encoding="utf-8")
    rows = ff.readlines()
    ff.seek(0)
    ff.close()
    # Add workbook and worksheet
    wb = xlsxwriter.Workbook(wkbk)
    ws1 = wb.add_worksheet(ws)

    # Add a general format
    bold = wb.add_format({"bold": 1})
    level_text = wb.add_format({"bold": 1, "bg_color": "yellow"})

    # Freeze Top Pane
    ws1.freeze_panes(1, 0)

    # write the first row as heading (projects info and child tag levels)
    ws1.write(0, 0, "System: {}, System No:{}".format(sysname, sysno), bold)
    total_level = max(list(map(lambda x: x.count("|"), rows)))
    for i in range(2, total_level + 2):
        ws1.write(0, i - 1, "Level_{}".format(i), level_text)

    rowfor = 1
    colfor = 0
    while rowfor < len(rows):
        ws1.set_row(
            rowfor,
            None,
            None,
            {"level": colfor + rows[rowfor - 1].count("|"), "hidden": False},
        )
        rowfor += 1

    row = 1
    col = 0
    while row < len(rows):
        ws1.write(row, col + rows[row - 1].count("|"), rows[row - 1])
        row += 1
    wb.close()


def _get_cell_range(sheet_obj, start_row, start_col, end_row, end_col):
    """
    Get cell range in xlrd module as two level nested list.

    Arguments:
        sheet_obj {xlrd worksheet object} -- xlrd worksheet instance
        start_row {int} -- Number of start row
        start_col {int} -- Number of start column
        end_row {int} -- Number of last row
        end_col {int} -- Number of last column

    Returns:
        list -- Cell range as two level nested list
    """
    return [
        sheet_obj.row_slice(row, start_colx=start_col, end_colx=end_col + 1)
        for row in range(start_row, end_row + 1)
    ]


def _convert_empty_cells(sheet_obj, convert_to=None):
    """
    Create a list with all row numbers that contain data and loop through it.
    Create a list with all column numbers that contain data and loop through i

    Arguments:
        sheet_obj {xlrd worksheet object}

    Keyword Arguments:
        convert_to {str, int, None} -- (default: {None})
    """
    for r in range(0, sheet_obj.nrows):
        for c in range(0, sheet_obj.ncols):
            if sheet_obj.cell_type(r, c) == xl.XL_CELL_EMPTY:
                sheet_obj._cell_values[r][c] = convert_to


def _get_sheet_dimension(sheet_obj):
    """Return sheet dimension for quality validation issues

    Arguments:
        sheet_obj {xlrd worksheet object}

    Returns:
        dict -- Dictionary of 'spirname', 'maxcol', 'maxrow'
    """
    return {
        "spirname": sheet_obj.name,
        "maxcol": sheet_obj.ncols,
        "maxrow": sheet_obj.nrows,
    }
    # print(f"{spir_sheet.name}\tmaxCol: {spir_sheet.ncols}\tmaxRow: {spir_sheet.nrows}")


def _find_pattern(sheet_obj, pattern):
    """
    Finds given regex pattern

    Arguments:
        sheet_obj {xlrd worksheet object}
        pattern {string} -- Regex pattern

    Returns:
        list -- List of (row, col) tuples that match regex pattern
    """

    row_col_list = []
    for r in range(0, sheet_obj.nrows):
        for c in range(0, sheet_obj.ncols):
            if re.search(pattern, str(sheet_obj.cell_value(r, c))):
                row_col_list.append(sheet_obj.cell_value(r, c))

    return row_col_list

    # if len(set(row_col_list)) == 1:
    #     return row_col_list[0]
    # elif len(set(row_col_list)) > 1:
    #     return sheet_obj.cell_value(*cell_for_spir)
    # else:
    #     return "NO_SPIR_REF_FOUND"


def _get_horizontal_range(sheet_obj, row: int, start_col: int):
    """
    Find last filled cell in row, followed by two empty cell at least.
    start_col==1 because requires validation of "Tag No." text

    Arguments:
        sheet_obj {xlrd worksheet object}

    Keyword Arguments:
        row {int} -- First Tag cell row (default: {4})
        start_col {int} -- First Tag cell column (default: {1})

    Returns:
        dict -- Dictionary of 'tag' and 'last_cell'
    """
    if "tag" in sheet_obj.cell_value(row, start_col - 1).lower():
        ctr = 0
        cell_list = sheet_obj.row_slice(row, start_col)
        z = []
        while ctr < len(cell_list):
            if cell_list[ctr].value is not None:
                z.append(cell_list[ctr])
                ctr += 1
            elif cell_list[ctr].value is None and cell_list[ctr + 1].value is None:
                break
            else:
                z.append(cell_list[ctr])
                ctr += 1
        return {"tags": z[1:], "last_cell": (row, start_col + ctr - 1)}
    else:
        raise (ValueError("Check First Tag Cell in the SPIR"))


def read_excel_to_lol(fname, sheet_index=0):
    """
    Read excel file into lists of list.
    Make sure to indicate sheet index if it is not the first sheet
    """
    wb = xl.open_workbook(fname)
    sh = wb.sheet_by_index(sheet_index)
    return [sh.row_values(i) for i in range(sh.nrows)]
