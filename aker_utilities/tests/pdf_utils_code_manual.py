from aker_utilities.pdf_utils import PDFEditor


def test_split_in_two() -> None:
    print("Starting: test_split_in_two")
    doc = PDFEditor(r"__ref/pdf_utils/sample.pdf")
    split_page_no: int = int(doc.document.page_count / 2) + 1
    doc.split(split_page_no, save_as=r"__ref/pdf_utils/test_split_in_two.pdf")


def test_merge() -> None:
    print("Starting: test_merge")
    PDFEditor.merge(
        docpaths=[
            r"__ref/pdf_utils/test_split_in_two(1).pdf",
            r"__ref/pdf_utils/sample.pdf",
            r"__ref/pdf_utils/test_split_in_two.pdf",
        ],
        save_as=None,
    )


def test_merge_save_as() -> None:
    print("Starting: test_merge")
    PDFEditor.merge(
        docpaths=[
            r"__ref/pdf_utils/test_split_in_two(1).pdf",
            r"__ref/pdf_utils/sample.pdf",
            r"__ref/pdf_utils/test_split_in_two.pdf",
        ],
        save_as=r"__ref/pdf_utils/test_merge.pdf",
    )


def test_convert() -> None:
    print("Starting: test_convert")
    doc = PDFEditor(r"__ref/pdf_utils/sample.pdf")
    doc.convert_page(
        page_no=1,
        include_images=True,
        save_as=r"__ref/pdf_utils/test_convert_to_html.html",
    )


def test_delete() -> None:
    doc = PDFEditor(r"__ref/pdf_utils/sample.pdf")
    doc.delete(
        page_range=(1, 5), save_as=r"__ref/pdf_utils/test_delete_first_five_pages.pdf"
    )


def test_export_all_single_page_default_setup() -> None:
    print("Starting: test_export_all_single_page_default_setup")
    doc = PDFEditor(r"__ref/pdf_utils/sample.pdf")
    doc.export()


def test_export_range() -> None:
    print("Starting: test_export_range")
    doc = PDFEditor(r"__ref/pdf_utils/sample.pdf")
    doc.export(
        page_range=(1, 4),
        single_pages=False,
        save_as=r"__ref/pdf_utils/test_export_range.pdf",
    )


def test_export_arbitrary_pages() -> None:
    print("Starting: test_export_arbitrary_pages")
    doc = PDFEditor(r"__ref/pdf_utils/sample.pdf")
    doc.export(
        page_range=[1, 3, 5, 7, 9],
        single_pages=False,
        save_as=r"__ref/pdf_utils/test_export_arbitrary_pages.pdf",
    )


def test_export_range_as_single_pages() -> None:
    print("Starting: test_export_range_as_single_pages")
    doc = PDFEditor(r"__ref/pdf_utils/sample.pdf")
    doc.export(
        page_range=(1, 4),
        single_pages=True,
        save_as=r"__ref/pdf_utils/test_export_range_as_single_pages.pdf",
    )


def test_export_arbitrary_pages_as_single_pages() -> None:
    print("Starting: test_export_arbitrary_pages_as_single_pages")
    doc = PDFEditor(r"__ref/pdf_utils/sample.pdf")
    doc.export(
        page_range=[2, 4, 6, 8, 10],
        single_pages=True,
        save_as=r"__ref/pdf_utils/test_export_arbitrary_page_as_single_pgs.pdf",
    )


def test_insert_all_start() -> None:
    print("Starting: test_insert_all_start")
    doc = PDFEditor(r"__ref/pdf_utils/test_split_in_two.pdf")
    doc.insert(
        path_to_insert=r"__ref/pdf_utils/test_split_in_two(1).pdf",
        page_range=None,
        start_at=1,
        save=r"__ref/pdf_utils/test_insert_all_start.pdf",
    )


def test_insert_single_at_third_page() -> None:
    print("Starting: test_insert_single_at_third_page")
    doc = PDFEditor(r"__ref/pdf_utils/test_split_in_two.pdf")
    doc.insert(
        r"__ref/pdf_utils/test_split_in_two(1).pdf",
        page_range=(1, 1),
        start_at=3,
        save=r"__ref/pdf_utils/test_insert_single_to_third_page.pdf",
    )


def test_insert_reverse_end() -> None:
    print("Starting: test_insert_reverse_end")
    doc = PDFEditor(r"__ref/pdf_utils/test_split_in_two.pdf")
    doc.insert(
        r"__ref/pdf_utils/test_split_in_two(1).pdf",
        page_range=(3, 1),
        start_at=None,
        save=r"__ref/pdf_utils/test_insert_reverse_end.pdf",
    )


def test_rotate() -> None:
    print("Starting: test_rotate")
    doc = PDFEditor(r"__ref/pdf_utils/test_split_in_two.pdf")
    doc.rotate(
        pages=[1, 2],
        step=3,
        save_as=None,
    )


def test_rotate_save_as() -> None:
    print("Starting: test_rotate")
    doc = PDFEditor(r"__ref/pdf_utils/test_split_in_two.pdf")
    doc.rotate(
        pages=[1, 2],
        step=3,
        save_as=r"__ref/pdf_utils/test_rotate_page1_2_as_270.pdf",
    )


def test_rotate_all() -> None:
    print("Starting: test_rotate_all")
    doc = PDFEditor(r"__ref/pdf_utils/test_split_in_two.pdf")
    doc.rotate(None, step=1, save_as=r"__ref/pdf_utils/test_rotate_all_90.pdf")


def test_crop() -> None:
    print("Starting: test_crop")
    doc = PDFEditor(("__ref/pdf_utils/sample.pdf"))
    doc.crop(pages=None, cropbox=(0, 0, 300, 300), save_as=None)


# Ordering functions so that before insert and merge we split test document and have
# more than one document to manipulate
test_split_in_two()
test_merge()
test_merge_save_as()
test_convert()
test_delete()
test_export_range()
test_export_arbitrary_pages()
test_export_range_as_single_pages()
test_export_arbitrary_pages_as_single_pages()
test_insert_all_start()
test_insert_single_at_third_page()
test_insert_reverse_end()
test_rotate()
test_rotate_all()
test_crop()
