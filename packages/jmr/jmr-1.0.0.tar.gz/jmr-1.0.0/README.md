# jmr

![PyPI](https://img.shields.io/pypi/v/jmr.svg?style=flat-square)
![GitHub](https://img.shields.io/github/license/mashape/apistatus.svg?style=flat-square)

`jmr` is mappable JSON object.

## Installation

Using pip

```
$ pip install git+https://github.com/hinatades/jmr.git
```

or using pip with PyPI: https://pypi.python.org/pypi/jmr

```
$ pip install jmr
```

## Usage

```python
import jmr

json_data = {}
jmr = JSONMapper(json_data)
```

## Example

### map json keys with CSV

```python
new_input_data = jmr.map_keys_with_csv(
    'MAPPING_CSV_PATH',
    'MAPPING_PKL_PATH',
    [1, 0]
)
```

## Author

@hinatades (<hnttisk@gmail.com>)
