"""Generate the code reference pages."""

from pathlib import Path

import mkdocs_gen_files


# def generate_docstrings(source_folder: str):
#     nav = mkdocs_gen_files.Nav()
#     root = Path(__file__).parents[3]
#     src = Path(root, source_folder)
#     docs = Path(root, "site", "code")

#     docs.mkdir(exist_ok=True, parents=True)

#     for path in sorted(src.rglob("*.py")):
#         if path.parent.name == "tests":
#             continue

#         module_path = path.relative_to(src).with_suffix("")
#         doc_path = path.relative_to(src).with_suffix(".md")
#         full_doc_path = Path(docs, doc_path)

#         parts = tuple(module_path.parts)

#         if parts[-1] == "__init__":
#             # parts = parts[:-1]
#             continue
#         elif parts[-1] == "__main__":
#             continue

#         nav[parts] = doc_path.as_posix()

#         with mkdocs_gen_files.open(full_doc_path, "w") as fd:
#             identifier = ".".join((source_folder, ) + parts)
#             print("::: " + identifier, file=fd)

#         # mkdocs_gen_files.set_edit_path(full_doc_path, path.relative_to(root))
#         mkdocs_gen_files.set_edit_path(full_doc_path, Path("../", path))

#     with mkdocs_gen_files.open(Path(docs, "SUMMARY.md"), "w") as nav_file:
#         nav_file.writelines(nav.build_literate_nav())


# generate_docstrings(source_folder="aker_utilities")


"""Generate the code reference pages and navigation."""

# nav = mkdocs_gen_files.Nav()

root = Path(__file__).parents[3]
src = root / "aker_utilities"

for path in sorted(src.rglob("*.py")):
    if path.parent.name == "tests":
        continue

    module_path = path.relative_to(src).with_suffix("")
    doc_path = path.relative_to(src).with_suffix(".md")
    full_doc_path = Path("code-reference", doc_path)

    parts = tuple(module_path.parts)

    if parts[-1] == "__init__":
        # parts = parts[:-1]
        continue
    elif parts[-1] == "__main__":
        continue

    # nav[parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        ident = ".".join((src.name, ) + parts)
        fd.write(f"::: {ident}")

    mkdocs_gen_files.set_edit_path(full_doc_path, path.relative_to(root))

# with mkdocs_gen_files.open("code-reference/SUMMARY.md", "w") as nav_file:
#     nav_file.writelines(nav.build_literate_nav())