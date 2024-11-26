---
title: How-to-setup-mkdocs
author: Jon Steinar Folstad
date: 2024-11-06
---

# How to setup mkdocs with existing repository

We are using mkdocs with material plugin and installing material plugin will automatically install compatible versions of all dependencies: MkDocs, Markdown, Pygments and Python Markdown Extensions. Material for MkDocs always strives to support the latest versions, so there's no need to install those packages separately.

[mkdocs-material documentation >>>](https://squidfunk.github.io/mkdocs-material/getting-started/)

## Installation of dependencies via pip

`pip install mkdocs-material mkdocs-coverage mkdocstrings-python mkdocs-gen-files`

## Sample pyproject.toml

??? example "pyproject.toml"

    ```
    [tool.poetry]
    name = "mkdocs101"
    version = "0.1.0"
    description = "Test project for mkdocs documentation setup"
    authors = ["XYZ"]
    license = "MIT"
    readme = "README.md"

    [tool.poetry.dependencies]
    python = "^3.12"
    mkdocs-material = "^9.5.45"
    mkdocs-coverage = "^1.1.0"
    mkdocstrings-python = "^1.12.2"
    mkdocs-gen-files = "^0.5.0"

    [tool.poetry.group.dev.dependencies]
    black = "^24.10.0"
    flake8 = "^7.1.1"

    [build-system]
    requires = ["poetry-core"]
    build-backend = "poetry.core.masonry.api"
    ```

## Getting started with mkdocs

#### Alternative 1

!!! Warning

    Make sure no folder is named `docs` before running following command to prevent data loss

> `mkdocs new .` will create `docs` folder and `mkdocs.yaml` configuration file at root

Folder structure:
```
|   .gitignore
|   mkdocs.yml
|   poetry.lock
|   pyproject.toml
|   README.md
+---docs
        index.md
```        

#### Alternative 2 

In case of having a `docs` folder already in the repository

> `mkdocs new documentation` will nest `docs` folder and `mkdocs.yaml` under given folder name which is `documentation` in this case.

Folder structure:
```
|   .gitignore
|   poetry.lock
|   pyproject.toml
|   README.md
+---documentation
    |   mkdocs.yml
    +---docs
            index.md
```            

!!! info
    
    This guideline will follow the first alternative to create a new project, please remember to update paths with nested structure if second alternative was selected.

At this very stage a basic documentation site can be seen by running `mkdocs serve` command which will build and start hosting documentation as static html site in localhost.

## Extensions and Styling (Digipedia style)

Adding some useful extensions like admonition, katex, mermaid etc. and styling to meet digipedia look and feel by using following `mkdocs.yaml` config.

??? example "mkdocs.yaml"

    ```yaml
    site_name: AkerBP Project & Code Documentation
    site_url: https://mydomain.org/AkerBP
    repo_name: AkerBP/DataOps/dig-docs
    repo_url: https://dev.azure.com/akerbp/DataOps/_git/dig-docs


    theme:
    name: material
    # name: readthedocs
    favicon: assets/images/favicon.ico
    logo: assets/images/favicon.ico
    font:
        text: Lato
    palette:
        # Palette toggle for light mode
        - media: "(prefers-color-scheme: light)"
        scheme: default
        primary: akerbp
        accent: akerbp
        toggle:
            icon: material/weather-night
            name: Switch to dark mode

        # Palette toggle for dark mode
        - media: "(prefers-color-scheme: dark)"
        scheme: slate
        primary: akerbp
        accent: akerbp
        toggle:
            icon: material/weather-sunny
            name: Switch to light mode
    features:
        - navigation.footer
        # - navigation.tabs
        # - navigation.tabs.sticky
        - navigation.sections
        - navigation.indexes
        - content.action.edit
        - content.action.view
        - content.code.copy
        - toc.follow
        - toc.integrate   # Integrate outline on the right navigation bar into left panel

    icon:
        repo: fontawesome/brands/git-alt
        edit: material/pencil
        view: material/eye

    extra_javascript:
    - assets/javascripts/katex.js
    - https://unpkg.com/katex@0/dist/katex.min.js
    - https://unpkg.com/katex@0/dist/contrib/auto-render.min.js

    # Extra styling
    extra_css:
    - assets/stylesheets/extra.css
    - assets/stylesheets/img_carousel.css
    - https://unpkg.com/katex@0/dist/katex.min.css

    markdown_extensions:
    - admonition
    - attr_list
    - md_in_html
    - pymdownx.arithmatex:
        generic: true
    - pymdownx.blocks.caption
    - pymdownx.caret
    - pymdownx.details
    - pymdownx.emoji:
        emoji_index: !!python/name:material.extensions.emoji.twemoji
        emoji_generator: !!python/name:material.extensions.emoji.to_svg
    - pymdownx.highlight:
        anchor_linenums: true
        line_spans: __span
        pygments_lang_class: true
    - pymdownx.inlinehilite
    - pymdownx.mark
    - pymdownx.snippets
    - pymdownx.superfences:
        custom_fences:
            - name: mermaid
            class: mermaid
            format: !!python/name:pymdownx.superfences.fence_code_format
    - pymdownx.tabbed:
        alternate_style: true
    - pymdownx.tasklist:
        custom_checkbox: true
    - pymdownx.tilde
    - tables
    - toc:
        permalink: true
        permalink_title: "Direct link to this heading"
        slugify: !!python/object/apply:pymdownx.slugs.slugify
            kwds:
            case: lower
        toc_depth: 3
    ```

