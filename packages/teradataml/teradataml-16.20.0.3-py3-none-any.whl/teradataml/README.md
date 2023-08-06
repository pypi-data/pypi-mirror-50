## Teradata Python package for Advanced Analytics.

teradataml makes available to Python users a collection of analytic functions that reside on Teradata Vantage. This allows users to perform analytics on Teradata Vantage with no SQL coding. In addition, the teradataml library provides functions for scaling data manipulation and transformation, data filtering and sub-setting, and can be used in conjunction with other open-source python libraries. 

For community support, please visit the [Connectivity Forum](http://community.teradata.com/t5/Tools/bd-p/DevXToolsBoard).

For Teradata customer support, please visit [Teradata Access](https://access.teradata.com/).

Copyright 2019, Teradata. All Rights Reserved.

### Table of Contents
* [Release Notes](#release-notes)
* [Installation and Requirements](#installation-and-requirements)
* [Using the Teradata Python Package](#using-the-teradata-python-package)
* [Documentation](#documentation)
* [License](#license)

## Release Notes:
#### teradataml 16.20.00.03
* Fixed the garbage collection issue observed with `remove_context()` when context is created using a SQLAlchemy engine.
* Added 4 new NewSQL Engine analytic functions supported only on Vantage 1.1:
    * `Antiselect`, `Pack`, `StringSimilarity`, and `Unpack`.
* Updated the Machine Learning Engine `NGrams` function to work with Vantage 1.1.

#### teradataml 16.20.00.02
* Python version 3.4.x will no longer be supported. The Python versions supported are 3.5.x, 3.6.x, and 3.7.x.
* Major issue with the usage of formula argument in analytic functions with Python3.7 has been fixed, allowing this package to be used with Python3.7 or later.
* Configurable alias name support for analytic functions has been added.
* Support added to create_context (connect to Teradata Vantage) with different logon mechanisms.
    Logon mechanisms supported are: 'TD2', 'TDNEGO', 'LDAP' & 'KRB5'.
* copy_to_sql function and DataFrame 'to_sql' methods now provide following additional functionality:
    * Create Primary Time Index tables.
    * Create set/multiset tables.
* New DataFrame methods are added: 'median', 'var', 'squeeze', 'sort_index', 'concat'.
* DataFrame method 'join' is now updated to make use of ColumnExpressions (df.column_name) for the 'on' clause as opposed to strings.
* Series is supported as a first class object by calling squeeze on DataFrame.
    * Methods supported by teradataml Series are: 'head', 'unique', 'name', '\_\_repr__'.
    * Binary operations with teradataml Series is not yet supported. Try using Columns from teradataml.DataFrames.
* Sample datasets and commands to load the same have been provided in the function examples.
* New configuration property has been added 'column_casesenitive_handler'. Useful when one needs to play with case sensitive columns.

#### teradataml 16.20.00.01
* New support has been added for Linux distributions: Red Hat 7+, Ubuntu 16.04+, CentOS 7+, SLES12+.
* 16.20.00.01 now has over 100 analytic functions. These functions have been organized into their own packages for better control over which engine to execute the analytic function on. Due to these namespace changes, the old analytic functions have been deprecated and will be removed in a future release. See the Deprecations section in the Teradata Python Package User Guide for more information.
* New DataFrame methods `shape`, `iloc`, `describe`, `get_values`, `merge`, and `tail`.
* New Series methods for NA checking (`isnull`, `notnull`) and string processing (`lower`, `strip`, `contains`).

#### teradataml 16.20.00.00
* `teradataml 16.20.00.00` is the first release version. Please refer to the _Teradata Python Package User Guide_ for a list of Limitations and Usage Considerations.

## Installation and Requirements

### Package Requirements:
* Python 3.5 or later

Note: 32-bit Python is not supported.

### Minimum System Requirements:
* Windows 7 (64Bit) or later
* macOS 10.9 (64Bit) or later
* Red Hat 7 or later versions
* Ubuntu 16.04 or later versions
* CentOS 7 or later versions
* SLES 12 or later versions
* Teradata Vantage NewSQL Engine:
    * NewSQL Engine 16.20 Feature Update 1 or later

For a Teradata Vantage system with the ML Engine:
    * Teradata Machine Learning Engine 08.00.03.01 or later

### Installation

Use pip to install the Teradata Python Package for Advanced Analytics.

Platform       | Command
-------------- | ---
macOS/Linux    | `pip install teradataml`
Windows        | `py -3 -m pip install teradataml`

When upgrading to a new version of the Teradata Python Package, you may need to use pip install's `--no-cache-dir` option to force the download of the new version.

Platform       | Command
-------------- | ---
macOS/Linux    | `pip install --no-cache-dir -U teradataml`
Windows        | `py -3 -m pip install --no-cache-dir -U teradataml`

## Using the Teradata Python Package

Your Python script must import the `teradataml` package in order to use the Teradata Python Package:

```
>>> import teradataml as tdml
>>> from teradataml import create_context, remove_context
>>> create_context(host = 'hostname', username = 'user', password = 'password')
>>> df = tdml.DataFrame('iris')
>>> df

   SepalLength  SepalWidth  PetalLength  PetalWidth             Name
0          5.1         3.8          1.5         0.3      Iris-setosa
1          6.9         3.1          5.1         2.3   Iris-virginica
2          5.1         3.5          1.4         0.3      Iris-setosa
3          5.9         3.0          4.2         1.5  Iris-versicolor
4          6.0         2.9          4.5         1.5  Iris-versicolor
5          5.0         3.5          1.3         0.3      Iris-setosa
6          5.5         2.4          3.8         1.1  Iris-versicolor
7          6.9         3.2          5.7         2.3   Iris-virginica
8          4.4         3.0          1.3         0.2      Iris-setosa
9          5.8         2.7          5.1         1.9   Iris-virginica

>>> df = df.select(['Name', 'SepalLength', 'PetalLength'])
>>> df

              Name  SepalLength  PetalLength
0  Iris-versicolor          6.0          4.5
1  Iris-versicolor          5.5          3.8
2   Iris-virginica          6.9          5.7
3      Iris-setosa          5.1          1.4
4      Iris-setosa          5.1          1.5
5   Iris-virginica          5.8          5.1
6   Iris-virginica          6.9          5.1
7      Iris-setosa          5.1          1.4
8   Iris-virginica          7.7          6.7
9      Iris-setosa          5.0          1.3

>>> df = df[(df.Name == 'Iris-setosa') & (df.PetalLength > 1.5)]
>>> df

          Name  SepalLength  PetalLength
0  Iris-setosa          4.8          1.9
1  Iris-setosa          5.4          1.7
2  Iris-setosa          5.7          1.7
3  Iris-setosa          5.0          1.6
4  Iris-setosa          5.1          1.9
5  Iris-setosa          4.8          1.6
6  Iris-setosa          4.7          1.6
7  Iris-setosa          5.1          1.6
8  Iris-setosa          5.1          1.7
9  Iris-setosa          4.8          1.6
```

## Documentation

General product information, including installation instructions, is available in the [Teradata Documentation website](https://docs.teradata.com/)

## License

Use of the Teradata Python Package is governed by the *License Agreement for the Teradata Python Package for Advanced Analytics*. 
After installation, the `LICENSE` and `LICENSE-3RD-PARTY` files are located in the `teradataml` directory of the Python installation directory.
