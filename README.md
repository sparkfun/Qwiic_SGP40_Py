Qwiic_SGP40_Py
===============

<p align="center">
   <img src="https://cdn.sparkfun.com/assets/custom_pages/2/7/2/qwiic-logo-registered.jpg"  width=200>  
   <img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"  width=240>   
</p>
<p align="center">
	<a href="https://pypi.org/project/sparkfun-qwiic-sgp40/" alt="Package">
		<img src="https://img.shields.io/pypi/pyversions/sparkfun-qwiic-sgp40.svg" /></a>
	<a href="https://github.com/sparkfun/Qwiic_SGP40_Py/issues" alt="Issues">
		<img src="https://img.shields.io/github/issues/sparkfun/Qwiic_SGP40_Py.svg" /></a>
	<a href="https://qwiic-sgp40-py.readthedocs.io/en/latest/?" alt="Documentation">
		<img src="https://readthedocs.org/projects/qwiic-sgp40-py/badge/?version=latest&style=flat" /></a>
	<a href="https://github.com/sparkfun/Qwiic_SGP40_Py/blob/master/LICENSE" alt="License">
		<img src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
	<a href="https://twitter.com/intent/follow?screen_name=sparkfun">
        	<img src="https://img.shields.io/twitter/follow/sparkfun.svg?style=social&logo=twitter"
           	 alt="follow on Twitter"></a>

</p>

<img src="https://cdn.sparkfun.com/assets/parts/1/7/6/8/0/18345-SparkFun_Air_Quality_Sensor_Breakout_-_SGP40__Qwiic_-01.jpg"  align="right" width=300 alt="SparkFun Qwiic RFID Reader">

Python module for the [SparkFun Qwiic Air Quality Sensor - SGP40](https://www.sparkfun.com/products/18345)

This python package is a port of the existing [SparkFun SGP40 Arduino Library](https://github.com/sparkfun/SparkFun_SGP40_Arduino_Library)

This package can be used in conjunction with the overall [SparkFun qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

## Contents

* [Supported Platforms](#supported-platforms)
* [Dependencies](#dependencies)
* [Installation](#installation)
* [Documentation](#documentation)
* [Example Use](#example-use)

Supported Platforms
--------------------
The Qwiic SGP40 Python package currently supports the following platforms:
* [Raspberry Pi](https://www.sparkfun.com/search/results?term=raspberry+pi)

Dependencies
--------------
This driver package depends on the qwiic I2C driver:
[Qwiic_I2C_Py](https://github.com/sparkfun/Qwiic_I2C_Py)

Documentation
-------------
The SparkFun Qwiic Sgp40 module documentation is hosted at [ReadTheDocs](https://qwiic-sgp40-py.readthedocs.io/en/latest/?)

Installation
---------------
### PyPi Installation

This repository is hosted on PyPi as the [sparkfun-qwiic-sgp40](https://pypi.org/project/sparkfun-qwiic-sgp40/) package. On systems that support PyPi installation via pip, this library is installed using the following commands

For all users (note: the user must have sudo privileges):
```sh
sudo pip install sparkfun-qwiic-sgp40
```
For the current user:

```sh
pip install sparkfun-qwiic-sgp40
```
To install, make sure the setuptools package is installed on the system.

Direct installation at the command line:
```sh
python setup.py install
```

To build a package for use with pip:
```sh
python setup.py sdist
 ```
A package file is built and placed in a subdirectory called dist. This package file can be installed using pip.
```sh
cd dist
pip install sparkfun-qwiic-sgp40-<version>.tar.gz
```

Example Use
 -------------
See the examples directory for more detailed use examples.

```python
from __future__ import print_function
import qwiic_sgp40
import time
import sys

def run_example():

	print("\nSparkFun Qwiic Air Quality Sensor - SGP40, Example 1\n")
	my_sgp40 = qwiic_sgp40.QwiicSGP40()
	
	if my_sgp40.begin() != 0:
		print("\nThe Qwiic SGP40 isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return
	
	print("\nSGP40 ready!")
	
	while True:
		
		print("\nVOC Index is: " + str(my_sgp40.get_VOC_index()))
		
		time.sleep(1)

if __name__ == '__main__':
	try:
		run_example()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)
```
<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
