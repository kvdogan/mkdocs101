---
title: Mkdocs Basics
---

# Admonitions

## Basic Admonition

??? note "Basic admonition"

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.

## Inline admonition

!!! info inline end "Lorem ipsum"

    Lorem ipsum dolor sit amet, consectetur
    adipiscing elit. Nulla et euismod nulla.
    Curabitur feugiat, tortor non consequat
    finibus, justo purus auctor massa, nec
    semper lorem quam in massa.

Lorem ipsum dolor sit amet,
consectetur adipiscing elit. Nulla et euismod nulla. Curabitur feugiat, tortor non
consequat finibus, justo purus auctor massa, nec semper lorem quam in massa.
This is an admonition comes to the end of line (inline) Lorem ipsum dolor sit amet,
consectetur adipiscing elit. Nulla et euismod nulla. Curabitur feugiat, tortor non
consequat finibus, justo purus auctor massa, nec semper lorem quam in massa.
This is an admonition comes to the end of line (inline) Lorem ipsum dolor sit amet,
consectetur adipiscing elit. Nulla et euismod nulla. Curabitur feugiat, tortor non
consequat finibus, justo purus auctor massa, nec semper lorem quam in massa.



!!! info inline "Lorem ipsum"

    Lorem ipsum dolor sit amet, consectetur
    adipiscing elit. Nulla et euismod nulla.
    Curabitur feugiat, tortor non consequat
    finibus, justo purus auctor massa, nec
    semper lorem quam in massa.

Dolor esse officia mollit aute veniam. Sit aute id cillum nisi minim adipisicing exercitation est proident sit. Cillum quis irure sit duis ullamco. Aliquip et magna nulla anim culpa velit dolore do cupidatat fugiat laborum magna. Commodo non non cupidatat fugiat laborum irure aliqua duis. Incididunt aliquip officia voluptate irure irure tempor reprehenderit velit nisi excepteur. Commodo commodo labore excepteur elit reprehenderit et.

[For more of admonitions...](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#inline-blocks-inline)



# Code blocks

``` py title="bubble_sort.py" linenums="1" hl_lines="2 3"
def bubble_sort(items):
    for i in range(len(items)):
        for j in range(len(items) - 1 - i):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
```

# Content tabs

=== "C"

    ``` c
    #include <stdio.h>

    int main(void) {
      printf("Hello world!\n");
      return 0;
    }
    ```

=== "C++"

    ``` c++
    #include <iostream>

    int main(void) {
      std::cout << "Hello world!" << std::endl;
      return 0;
    }
    ```

    # Diagrams


``` mermaid
graph LR
  A[Start] --> B{Error?};
  B -->|Yes| C[Hmm...];
  C --> D[Debug];
  D --> B;
  B ---->|No| E[Yay!];
```


# Formatting

- ==This was marked (highlight)==
- ^^This was inserted (underline)^^
- ~~This was deleted (strikethrough)~~

# Grids

<div class="grid cards" markdown>

-   :material-clock-fast:{ .lg .middle } __Set up in 5 minutes__

    ---

    Install [`mkdocs-material`](#) with [`pip`](#) and get up
    and running in minutes

    [:octicons-arrow-right-24: Getting started](#)

-   :fontawesome-brands-markdown:{ .lg .middle } __It's just Markdown__

    ---

    Focus on your content and generate a responsive and searchable static site

    [:octicons-arrow-right-24: Reference](#)

-   :material-format-font:{ .lg .middle } __Made to measure__

    ---

    Change the colors, fonts, language, icons, logo and more with a few lines

    [:octicons-arrow-right-24: Customization](#)

-   :material-scale-balance:{ .lg .middle } __Open Source, MIT__

    ---

    Material for MkDocs is licensed under MIT and available on [GitHub]

    [:octicons-arrow-right-24: License](#)

</div>


# Math

$$
\cos x=\sum_{k=0}^{\infty}\frac{(-1)^k}{(2k)!}x^{2k}
$$