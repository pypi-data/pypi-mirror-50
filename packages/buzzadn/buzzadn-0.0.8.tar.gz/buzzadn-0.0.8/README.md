# Buzzvil Adnetworks PyPI Package

## Requirements

```
python -m pip install twine
```

## Setup PyPI

Create a file in the home directory called ~/.pypirc with contents:

```
[distutils]
index-servers = pypi

[pypi]
repository = https://pypi.python.org/pypi
username = <PyPI username form 1password>
password = <PyPI password form 1password>
```

## Build and upload to PyPI

Open terminal window and change directory to /adserver/network/packages

Make changes and don't forget to upgrade the version in setup.py

```
python setup.py sdist 
python -m twine upload dist/* -r pypi
```

Don't forget to update services using this package

## References

- https://packaging.python.org/overview/
- https://github.com/bast/pypi-howto

python setup.py sdist upload -r buzzvil