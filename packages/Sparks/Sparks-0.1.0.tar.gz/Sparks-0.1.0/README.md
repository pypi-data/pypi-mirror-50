# Sparks
<!-- insert badges here -->
Sparks is a minimal command-line tool to manage customizable project folders from templates.

## Features
* Simple command line usage thanks to [Click](https://click.palletsprojects.com).
* Customizable folder, files, and file contents thanks to [Jinja2](http://jinja.pocoo.org).

<!--
## Table of Contents
Optionally, include a table of contents in order to allow other people to quickly navigate especially long or detailed READMEs.
-->
## Installation
Run the following to install:
```bash
pip install sparks
```

## Usage

### Creating a new project
```bash
sparks create --help
Usage: sparks create [OPTIONS]

Options:
  --template TEXT  Template folder to generate from
  --output TEXT    Output folder to create files in
  --skip-prompt
  --help           Show this message and exit
```

<!--
## Contributing
For guidance on setting up a development environment and how to make a contribution to Sparks, see the [contributing guidelines](https://github.com/binaryart/sparks).
-->
<!--
## Credits
Include a section for credits in order to highlight and link to the authors of your project.
-->

## License
Sparks is released under the [MIT License](https://opensource.org/licenses/MIT).

