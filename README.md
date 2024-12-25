# Static Site Generator

This is a static site generator, written in Python, that creates a static site from a collection of markdown files.

![Example Site](./docs/example-site.png)

## Setup & Usage

### Installation

This project uses Nix flakes. Nix _must_ be installed with the experimental-features `nix-command` and `flakes` enabled.

### Running the Generator

To build and serve the static site on `0.0.0.0:8888` (or whatever your loopback address is, on port `8888`):

```bash
nix run
```

### Developing with Nix

To enter a development shell with all the necessary dependencies available:

```bash
nix develop
```

Whilst developing using `nix develop`, there are several commands available:

- `build` - builds the static site
- `tests` - executes unit tests for the project
- `serve` - serves the site on port `8888`
- `format check` - checks code formatting using black
- `format fix` - fixes code formatting using black

## Project Structure

- Content you wish to serve is placed in the `content` directory. Each file in this directory will be a markdown file that will be converted to HTML. Content can be organized into subdirectories.
- Static content (images, CSS, etc.) is placed in the `static` directory. This content will be copied to the output directory as-is, using the existing directory structure.
- `template.html` is the template that will be used to render the content. Site generation will replace the `{{ Content }}` placeholder with the content of the markdown file, and the `{{ Title }}` placeholder with the Heading 1 from the file. **Note**: A missing Heading 1 will cause the page generation to fail.
- The `public` directory is where the generated site will be placed. This directory is _removed_ (if existing) and recreated upon each site generation.
- The `src` directory contains the source code for the static site generator, and is structured as follows:
  - `main.py` is the entry point. This file kicks off the site generation process.
  - `markdown_block_functions.py` contains functions for processing markdown block elements.
  - `markdown_conversion_functions.py` contains functions for converting markdown to HTML.
  - `markdown_inline_functions.py` contains functions for processing markdown inline elements.
  - `nodes_htmlnode.py` contains the `HTMLNode` class and child classes, which represent HTML elements.
  - `nodes_textnode.py` contains the `TextNode` class, which represents a text node.
  - `site_generation_functions.py` contains functions for generating the site.
- The `tests` directory contains unit tests for the project. Each test file corresponds to a source file.

---

This project was built as part of the Static Site Generator Course from [Boot.Dev](https://www.boot.dev/courses/build-static-site-generator-python)

