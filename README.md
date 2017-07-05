True Path
==========

*"Many are stubborn in pursuit of the path they have chosen, few in pursuit of the goal."* - Friedrich Nietzsche

A tool for checking website addresses' genuineness and safety.

In order to do so, program checks the use of HTTPS and a certificate correctness, whether the site is reachable and popular and if it's not marked by Google as unsafe.

## Installation

From GitHub:

`sudo pip3 install git+https://github.com/Peantab/true_path.git
`

From inside project's directory:

`sudo pip3 install .`

## API Key

The software is shipped without an API key. You are supposed to paste your own Google Safe Browsing API key into `api_key` file in package sources' directory. It should be the only content of this file.

## Usage

### As a stand-alone application

The software can be used as a stand-alone program, run from command-line like this:


`true_path https://www.example.com/eg?q=whatever`

or, if you want more information about tests:

`true_path https://www.example.com/eg?q=whatever -v`

You can always consult help with `true_path  --help`

### From within your Python script

After installation it's enough to use `import true_path`

API is described in notebook mentioned below.

### From Jupyter Notebook

Example notebook available in root folder of repo `TruePath.ipynb` serves as packages manual, you can make your own notebooks as well

## Tests

Tests in pytest can be run from within the root directory of the project with `python3 setup.py test` (or `python setup.py test`).