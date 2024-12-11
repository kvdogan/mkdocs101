echo -e "\nCLI Test for PDF_UTILs is getting started with TOC"
echo -e "##################################################"
pdf_tool --path="__ref\pdf_utils\sample.pdf" toc

echo -e "\nSPLIT test_split_in_two"
echo -e "##################################################"
pdf_tool split --path="__ref\pdf_utils\sample.pdf" --page=13 --save-as="__ref\pdf_utils\test_split_in_two.pdf"

echo -e "\nMERGE test_merge"
echo -e "##################################################"
pdf_tool merge --docpaths="['__ref/pdf_utils/test_split_in_two(1).pdf', '__ref/pdf_utils/sample.pdf', '__ref/pdf_utils/test_split_in_two.pdf']"

echo -e "\nMERGE test_merge_save_as"
echo -e "##################################################"
pdf_tool merge --docpaths="['__ref/pdf_utils/test_split_in_two(1).pdf', '__ref/pdf_utils/sample.pdf', '__ref/pdf_utils/test_split_in_two.pdf']"  --save-as="__ref/pdf_utils/test_merge.pdf"

echo -e "\nCONVERT test_convert"
echo -e "##################################################"
pdf_tool convert_page --path='__ref/pdf_utils/sample.pdf' --page-no=1 --save-as="__ref/pdf_utils/test_convert_to_html.html"

echo -e "\nDELETE test_delete"
echo -e "##################################################"
pdf_tool delete --path='__ref/pdf_utils/sample.pdf' --page-range="(1,5)" --save-as="__ref/pdf_utils/test_delete_first_five_page.pdf"

echo -e "\nEXPORT test_export_all_single_page_default_setup"
echo -e "##################################################"
pdf_tool export --path="__ref/pdf_utils/sample.pdf"

echo -e "\nEXPORT test_export_range"
echo -e "##################################################"
pdf_tool export --path="__ref/pdf_utils/sample.pdf" --page-range="(1, 4)" --single-pages=False --save-as="__ref/pdf_utils/test_export_range.pdf"

echo -e "\nEXPORT test_export_arbitrary_pages"
echo -e "##################################################"
pdf_tool export --path="__ref/pdf_utils/sample.pdf" --page-range="[1, 3, 5, 7, 9]"  --single-pages=False --save-as="__ref/pdf_utils/test_export_arbitrary_pages.pdf"

echo -e "\nEXPORT test_export_range_as_single_pages.pdf"
echo -e "##################################################"
pdf_tool export --path="__ref/pdf_utils/sample.pdf" --page-range="(1, 4)" --single-pages=True --save-as="__ref/pdf_utils/test_export_range_as_single_pages.pdf"

echo -e "\nEXPORT test_export_arbitrary_page_as_single_pgs.pdf"
echo -e "##################################################"
pdf_tool export --path="__ref/pdf_utils/sample.pdf" --page-range="[2, 4, 6, 8, 10]" --single-pages=True --save-as="__ref/pdf_utils/test_export_arbitrary_page_as_single_pgs.pdf"

echo -e "\nINSERT test_insert_all_start"
echo -e "##################################################"
pdf_tool insert --path="__ref/pdf_utils/test_split_in_two.pdf" --path_to_insert="__ref/pdf_utils/test_split_in_two(1).pdf" --start-at=1 --save="__ref/pdf_utils/test_insert_all_start.pdf"

echo -e "\nINSERT test_insert_single_to_third_page"
echo -e "##################################################"
pdf_tool insert --path="__ref/pdf_utils/test_split_in_two.pdf" --path_to_insert="__ref/pdf_utils/test_split_in_two(1).pdf" --page-range="(1, 1)" --start-at=3 --save="__ref/pdf_utils/test_insert_single_to_third_page.pdf"

echo -e "\nINSERT test_insert_all_start"
echo -e "##################################################"
pdf_tool insert --path="__ref/pdf_utils/test_split_in_two.pdf" --path_to_insert="__ref/pdf_utils/test_split_in_two(1).pdf" --page-range="(3, 1)" --save="__ref/pdf_utils/test_insert_reverse_end.pdf"

echo -e "\nROTATE test_rotate_page1_2_as_270"
echo -e "##################################################"
pdf_tool rotate --path="__ref/pdf_utils/test_split_in_two.pdf" --pages="[1,2]" --step=3 --save-as="__ref/pdf_utils/test_rotate_page1_2_as_270.pdf"

echo -e "\nROTATE test_rotate_all_90"
echo -e "##################################################"
pdf_tool rotate --path="__ref/pdf_utils/test_split_in_two.pdf" --step=1 --save-as="__ref/pdf_utils/test_rotate_all_90.pdf"

echo -e "\nCROP test_crop"
echo -e "##################################################"
pdf_tool crop --path="__ref/pdf_utils/sample.pdf" --cropbox="(0, 0, 300, 300)" --save-as="__ref/pdf_utils/test_crop_300_300.pdf"
