from typing import Any
from pathlib import Path

import fire
import fitz

from aker_utilities.path_utils import checkfile, get_filepaths


class PDFEditor(object):
    def __init__(self, path: str | None) -> None:
        if path is None:
            self.path = Path("Empty_Binder.pdf")
            self.document = fitz.Document()
            self.document._newPage()
        else:
            self.path = Path(path)
            self.document = fitz.Document(self.path)

        self.folder = str(self.path.parent)
        self.file = self.path.name
        self.file_ext = self.path.suffix

    @property
    def toc(self) -> list[Any]:
        return fitz.utils.get_toc(self.document)

    @staticmethod
    def merge(
        docpaths: str | list[str],
        save_as: str | None = None,
        recursive_folder_scan: bool = False,
    ) -> None:
        """
        Merge given list of individual pdf paths or all documents in given folder path
        recursively or not recursively based on recursive_folder_scan argument.

        Args:
            docpaths (str | list[str]): Could be either folder
            save_as (str | None, optional): Saves into folder of first docpath or given
                                            string of folder path
            recursive (bool, optional): _description_. Defaults to False.
        """
        pdf = PDFEditor(path=None)

        if isinstance(docpaths, str):
            docpaths = get_filepaths(
                rootdir=docpaths, file_type=".pdf", recursive=recursive_folder_scan
            )
            folder_path = Path(str(docpaths)).parent
        elif isinstance(docpaths, list):
            folder_path = Path(str(docpaths[0])).parent

        for path in docpaths:
            pdf.insert(path, save=False)

        # Deleting Empty page created in the beginning for having file name as bookmark
        # when inserting documents without bookmarks.
        pdf.document.delete_page(0)

        if save_as is None:
            pdf.document.save(
                checkfile(Path(folder_path, "Binder.pdf").absolute()),
                garbage=4,
                deflate=1,
            )
        else:
            pdf.document.save(
                checkfile(Path(str(save_as)).absolute()), garbage=4, deflate=1
            )

    def convert_page(
        self,
        page_no: int,
        option: str = "html",
        sort: bool = True,
        include_images: bool = False,
        save_as: str | None = None,
    ) -> str | None:
        """Extract given pdf page as given format with or without images.

        Args:
            page_no (int): Page number as in pdf. (1-index)
            option (str, optional): Conversion format, ["html", "word"] Defaults to "html"
            sort (bool, optional): Fix the order of the document for auto generated PDFs
            include_images (bool, optional): _description_. Defaults to False.
            export_path (str, optional): In case of export. Defaults to None.

        Returns:
            str: _description_
        """
        # Getting Page Text as html without images with flag set to 2
        if include_images:
            page_html = self.document[int(page_no) - 1].get_text(  # type: ignore
                option=option, sort=sort
            )
        else:
            page_html = self.document[int(page_no) - 1].get_text(  # type: ignore
                option=option, sort=sort, flags=2
            )

        if isinstance(save_as, str):
            with open(checkfile(Path(save_as).absolute()), "w") as ff:
                ff.write(page_html)
        else:
            return page_html

    def delete(
        self,
        page_range: tuple[int, int] | list[int],
        save_as: str,
    ) -> None:
        """
        Delete pages out of given pdf page range and save_as with different name.
        If deleted page have bookmark, keep it, otherwise no bookmark.

        If page_range is:
        1. tuple of two int : Split page range either single pdfs or one pdf
        2. list of integers : Split given arbitrary page numbers either single pdfs
                              or one pdf
        3. None exports all thee page

        Args:
            page_range (tuple[int, int] | list[int] | None): 1-Index
            single_pages (bool, optional): _description_. Defaults to False.

        Example CLI:
        # Exports all pages as single page pdf
        >>> pdf_tool --path="./sample.pdf" delete

        """
        # Split given pages with start, end number either as single page pdfs or one pdf
        if isinstance(page_range, tuple) and len(page_range) == 2:
            start, end = page_range
            pages_to_delete = list(range(int(start), int(end) + 1))

        # Split arbitrary pages into either single page pdfs or one pdf
        elif isinstance(page_range, list) and len(page_range) != 0:
            pages_to_delete = [int(i) for i in page_range]
        else:
            raise ValueError(
                "page_range must be Tuple[start, end] or list[pages_to_extract]"
            )

        zero_index_pages = [i - 1 for i in pages_to_delete]
        self.document.delete_pages(zero_index_pages)

        toc = self.toc

        # In case of deleted document having no toc, insert name as toc
        if len(toc) != 0:
            # After Deletion cleans toc and flatten the structure due to complexity of
            # tracking level of bookmarks.
            toc = [[1, i[1], i[2]] for i in toc if i[2] > 0]

        # Setting cleaned toc
        self.document.set_toc(toc)  # type: ignore

        self.document.save(
            checkfile(Path(str(save_as)).absolute()), garbage=4, deflate=True
        )

    def export(
        self,
        page_range: tuple[int, int] | list[int] | None = None,
        single_pages: bool = True,
        save_as: str | None = None,
    ) -> None:
        """
        Export pages out of given pdf page range either as one pdf or many single page
        If exported page have bookmark, keep it, otherwise no bookmark.

        If page_range is:
        1. tuple of two int : Split page range either single pdfs or one pdf
        2. list of integers : Split given arbitrary page numbers either single pdfs
                              or one pdf
        3. None exports all thee page

        Args:
            page_range (tuple[int, int] | list[int] | None): 1-Index
            single_pages (bool, optional): _description_. Defaults to False.

        Example CLI:
        # Exports all pages as single page pdf
        >>> pdf_tool export --path="./sample.pdf"

        """
        # Split given pages with start, end number either as single page pdfs or one pdf
        if isinstance(page_range, tuple) and len(page_range) == 2:
            start, end = page_range
            pages_to_split = list(range(int(start), int(end) + 1))

        # Split arbitrary pages into either single page pdfs or one pdf
        elif isinstance(page_range, list) and len(page_range) != 0:
            pages_to_split = [int(i) for i in page_range]
        elif page_range is None:
            pages_to_split = list(range(1, self.document.page_count + 1))
        else:
            raise ValueError(
                "page_range must be Tuple[start, end] or list[pages_to_extract]"
            )

        if single_pages:
            for pageidx in pages_to_split:
                new_pdf = PDFEditor(path=None)
                new_pdf.insert(str(self.path), page_range=(pageidx, pageidx), save=False)

                # Delete created empty page
                new_pdf.document.delete_page(0)

                toc = new_pdf.toc

                # Setting cleaned toc
                new_pdf.document.set_toc(toc)  # type: ignore

                if save_as is None:
                    new_pdf.document.save(
                        checkfile(self.path.absolute()), garbage=4, deflate=1
                    )
                else:
                    new_pdf.document.save(
                        checkfile(Path(str(save_as)).absolute()), garbage=4, deflate=1
                    )

                new_pdf.document.close()
        else:
            all_pages = list(range(1, self.document.page_count + 1))
            pages_to_delete = list(set(all_pages).difference(set(pages_to_split)))

            zero_index_pages = [i - 1 for i in pages_to_delete]
            self.document.delete_pages(zero_index_pages)

            toc = self.toc

            # In case of inserted document having no toc, insert name as toc
            if len(toc) != 0:
                # After Deletion cleans toc and flatten the structure due to complexity of
                # tracking level of bookmarks.
                toc = [[1, i[1], i[2]] for i in toc if i[2] > 0]

            # Setting cleaned toc
            self.document.set_toc(toc)  # type: ignore

            if save_as is None:
                self.document.save(checkfile(self.path.absolute()), garbage=4, deflate=1)
            else:
                self.document.save(
                    checkfile(Path(str(save_as)).absolute()), garbage=4, deflate=1
                )

    def insert(
        self,
        path_to_insert: str,
        page_range: tuple[int, int] | None = None,
        start_at: int | None = None,
        rotate: int = 0,
        save: bool | str = False,
    ) -> fitz.Document | None:
        """
        Insert pdf, pages in any position, can also be used as append if start_at is not
        given (Append by default), smartly handles table of content

        Args:
            path_to_insert (str): PDF to copy from. Must be different object,
                           but may be same file.
            page_range (Tuple[int, int], optional): First source page to copy,
                                                    1-index, default 1.
                                                    Last source page to copy,
                                                    1-index, default last.
            start_at (int, optional): 1-index and it'll become this page number in target
            rotate (int, optional): rotate copied pages, default 0 is no change.
            save (str, optional): Defaults to False.
                                  True for overwriting original file
                                  False for returning document to keep in memory, no save
                                  Path string for writing in given path

        Copy sequence reversed if from_page > to_page.

        Returns:
            _type_: _description_
        """
        # Open file to insert
        # Saving TOC of file to insert
        path = Path(path_to_insert)
        doc2 = PDFEditor(path=path_to_insert)

        # Adjusting table of content aka. bookmarks in pdf however it is TOC in pymupdf
        # Saving initial TOC of original file
        toc1 = self.toc
        pcount = self.document.page_count

        # Extract from_page, to_page, page_count based on pages to insert for second file
        if page_range is None:
            start, end = (0, doc2.document.page_count - 1)  # 1-Index to Zero conversion
            pcount2 = doc2.document.page_count
        else:
            start, end = page_range
            # User inputs for page number are collected as 1-index but must be zero-index
            start = int(start) - 1
            end = int(end) - 1

            pcount2 = abs(end - start) + 1  # Calculate page count

            # Creating page number list in case of different page_range
            # Validation of input, make sure given page number is minimum 1 (1-index)
            if start < 0:
                start = 0

            if end < 0:
                end = 0

            # Document select method expects list of page numbers
            # In case range is single page
            if start == end:
                pages = [start]
            # In case of start > end meaning inserting in reverse order
            elif start > end:
                pages = list(range(end, start + 1))
            # All the other start < end cases
            else:
                pages = list(range(start, end + 1))  # Plus 1 because we want last page

            doc2_all_pages = list(range(0, doc2.document.page_count))
            pages_to_delete = list(set(doc2_all_pages).difference(set(pages)))
            doc2.document.delete_pages(pages_to_delete)

        toc2 = doc2.toc

        # In case of inserted document having no toc, insert name as toc
        if len(toc2) == 0:
            toc2 = [[1, path.stem, 1]]

        # After Deletion cleans toc and flatten the structure due to complexity of
        # tracking level of bookmarks.
        toc2 = [[1, i[1], i[2]] for i in toc2 if i[2] > 0]

        # Zero conversion for start_at
        if start_at is not None:
            start_at = int(start_at) - 1

        # Start at the end of first file, ie. appending to the end with no argument
        # In this case TOC page number of second file is increased by the first file
        if start_at is None or start_at >= pcount:
            # Zero-index conversion for start_at over total page number
            start_at = pcount
            # Increase page numbers in doc2 toc1 with doc1 page count
            for t in toc2:
                t[2] += pcount
        elif start_at == 0:
            # Increase page numbers in doc1 toc1 with original doc2 page count
            for t in toc1:
                t[2] += pcount2
        else:
            # In case of inserting pages in between,
            # Increase toc1 page number after start_at position by pcount2
            # Increase toc2 page numbers by start_at
            for t in toc1:
                if t[2] > start_at:
                    t[2] += pcount2
            for t in toc2:
                t[2] += start_at

        self.document.insert_pdf(
            doc2.document,  # cannot be the same object as doc1
            from_page=start,  # first page to copy, default: 0
            to_page=end,  # last page to copy, default: last page in 1-index
            start_at=start_at,  # type: ignore - target location in doc1, default: end
            rotate=rotate,  # rotate copied pages
            # TODO: Implement following arguments
            # links=links,                    # also copy links
            # annots=annots,                  # also copy annotations
            # show_progress=show_progress,    # message: Inserted 30 of 47 pages after int
            # final=final                     # the list of copied objects to be dropped
        )

        # Combine toc1 and toc2 and sort them based on page numbers
        combined_sorted_toc = toc1 + toc2
        combined_sorted_toc.sort(key=lambda x: x[2])

        self.document.set_toc(combined_sorted_toc)  # type: ignore

        doc2.document.close()

        if isinstance(save, str):
            self.document.save(checkfile(save), garbage=4, deflate=1)
        elif isinstance(save, bool) and save is True:
            self.document.save(checkfile(self.path.absolute()), garbage=4, deflate=1)
        elif isinstance(save, bool) and save is False:
            return self.document
        else:
            TypeError("'save' must be either 'path' to file or 'True' for overwriting")

    def rotate(
        self,
        pages: list[int] | None = None,
        step: int = 1,
        save_as: str | None = None,
    ) -> None:
        """
        Rotate given pages in steps of 90 degrees, negative sign for counter clockwise

        Args:
            pages (list[int], optional): Page numbers as in pdf. (1-index) Defaults to all
            step (int, optional): _description_. Defaults to 1.
            save_as (str, optional): _description_. Defaults to None.
        """
        if pages is None or pages == []:
            pages = list(range(self.document.page_count))
        else:
            pages = [int(i) - 1 for i in pages]

        # page_to_rotate = [0, ]
        for page in self.document:
            if page.number in pages and isinstance(step, int):
                # Rotate page clockwise 90 degrees and add to new pdf
                page.set_rotation(step * 90)

        if save_as is None:
            self.document.save(checkfile(self.path.absolute()), garbage=4, deflate=1)
        else:
            self.document.save(
                checkfile(Path(str(save_as)).absolute()), garbage=4, deflate=1
            )

    def split(self, page: int, save_as: str | None = None) -> None:
        """
        Split given pdf by the given page number as in pdf. Keeps toc in splitted document

        Args:
            page (int): Page number (incl) to split (1-index) as shown in pdf,
            save_as (str, optional): Custom fullpath. Defaults to same path as pdf
        """
        # Split pdf into two pdf with given page number (zero index) so that second file
        # starts with given page number
        # ie. Lets assume given page number is 10, total pno = 24
        split_gr1 = (0, int(page) - 1)  # [0, 9)
        split_gr2 = (int(page) - 1, self.document.page_count)  # [9, 24)
        toc = self.toc

        for split_range in [split_gr1, split_gr2]:
            new_pdf = fitz.Document()
            # to_page argument of insert_pdf is inclusive meaning
            # ie. page_to=8 includes page 9, [0, 8] or [9, 23]
            new_pdf.insert_pdf(
                self.document, from_page=split_range[0], to_page=split_range[1] - 1
            )
            # Adjusting page number of TOC based on split start page
            # Adding one because page is zero index put toc page number is not
            split_toc = [
                [t[0], t[1], t[2] - split_range[0]]
                for t in toc
                if t[2] in range(split_range[0] + 1, split_range[1] + 1)
            ]

            # If splited doc TOC hierarchy start from nested bookmarks (lvl2 or higher)
            # Create all hierarhcy level upwards as dummy TOC points addressing first page
            if len(split_toc) > 0 and split_toc[0][0] > 1:
                dummy_toc = []

                split_toc_original_page_no = [
                    split_toc[0][0],
                    split_toc[0][1],
                    split_toc[0][2] + split_range[0],
                ]
                split_toc_index_in_toc = toc.index(split_toc_original_page_no)

                index = split_toc_index_in_toc
                while toc[index][0] > 1:
                    if toc[index - 1][0] < toc[index][0]:
                        dummy_toc += [toc[index - 1]]
                        index -= 1
                    else:
                        index -= 1

                # Setting page number of parent toc element !, becasuse it is first page
                dummy_toc = [[i[0], i[1], 1] for i in dummy_toc]

                split_toc = dummy_toc + split_toc

            new_pdf.set_toc(split_toc)  # type: ignore
            if save_as is None:
                new_pdf.save(checkfile(self.path.absolute()), garbage=4, deflate=1)
            else:
                new_pdf.save(
                    checkfile(Path(str(save_as)).absolute()), garbage=4, deflate=1
                )

    def crop(
        self,
        cropbox: tuple[int, int, int, int],
        pages: list[int] | None = None,
        save_as: str | None = None,
    ) -> None:
        """
        Crops pages in given pdf with given crop box and saves as new pdf

        Args:
            pages (list[int] | None): Page numbers as in pdf. (1-index), def to all pages
            cropbox (tuple[int, int, int, int]): Corner coordinates of top_left and
                                                  bottom right of an crop-box rectangle.
            save_as (str | None): _description_
        """
        if pages is None or pages == []:
            pages = list(range(self.document.page_count))
        else:
            pages = [int(i) - 1 for i in pages]

        # page_to_rotate = [0, ]
        for page in self.document:
            if page.number in pages:
                # Rotate page clockwise 90 degrees and add to new pdf
                page.set_cropbox(fitz.Rect(*cropbox))

        if save_as is None:
            self.document.save(checkfile(self.path.absolute()), garbage=4, deflate=1)
        else:
            self.document.save(
                checkfile(Path(str(save_as)).absolute()), garbage=4, deflate=1
            )

    def __str__(self) -> str:
        return "PDFEditor({})".format(self.file)

    def __repr__(self) -> str:
        return "PDFEditor(file: {}, path: {})".format(self.file, self.path)


def main() -> None:
    fire.Fire(PDFEditor)


if __name__ == "__main__":
    # To be able to fix --help to show all the methods
    # https://github.com/google/python-fire/pull/364/commits/0e3d6827c74d9a43ee4367e2cf9c7d036828ac9e
    main()
