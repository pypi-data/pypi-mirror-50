# pyoffice

## what is this?
example for best practices in python packaging.

## requirements
```
pip install -r requirements.txt
```

## install
to install PyOffice, do:

``` 
git clone https://github.com/mynameisvinn/PyOffice
cd PyOffice
python setup.py install
```
or, get it straight from pypi:
```
python -m pip install PyOffice
```
once installed, python search for pyoffice in `site-packages` folder, which isdefined in `.bash_profile`.

```
export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python2.7/site-packages
```

you can check python path from terminal:
```
env | grep PYTHONPATH
```

verify that install placed source code in the appropriate site-packages folder with:

```
cd /usr/local/lib/python2.7/site-packages
```
you should see "PyOffice" source code. other libraries (eg sklearn, scipy) reside in this folder too.

## usage

```
>>> from PyOffice import CalculatorProcessor
>>> my_calc = CalculatorProcessor()
>>> my_calc.add(2,3)
# 5
```

## create a pypi package

### package script
create setup.py, which will be the workhorse of pypi packaging, and then package script by

```
python setup.py sdist # creates dist folder, which stores tarred copy
```

### upload to pypi
assuming youve registered with pypi, do
```
python setup.py register # authenticate
python setup.py sdist upload # uploads entire file to pypi
```
you can view package at https://pypi.python.org/pypi/PyOffice/0.1.0

### install with pip
youve seen this a million times before:
```
python -m pip install PyOffice
```

## helpful links
* https://www.digitalocean.com/community/tutorials/how-to-package-and-distribute-python-applications