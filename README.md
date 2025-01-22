![Qwiic SGP40 Python Package](docs/images/sgp40-gh-banner-py.png "qwiic SGP40 Python Package" )

# SparkFun Qwiic SGP40 - Python Package

![PyPi Version](https://img.shields.io/pypi/v/sparkfun_qwiic_sgp40)
![GitHub issues](https://img.shields.io/github/issues/sparkfun/qwiic_sgp40_py)
![License](https://img.shields.io/github/license/sparkfun/qwiic_sgp40_py)
![X](https://img.shields.io/twitter/follow/sparkfun)
[![API](https://img.shields.io/badge/API%20Reference-blue)](https://docs.sparkfun.com/qwiic_sgp40_py/classqwiic__sgp40_1_1qwiic__sgp40_1_1_qwiic_s_g_p40.html)

The SparkFun Qwiic SGP40 Air Quality Sensor Breakout Boards provide a simple and cost effective solution for adding air quality sensing to your project. Implementing a SparkFun Qwiic I2C interface, these sensors can be rapidly added to any project with boards that are part of the SparkFun Qwiic ecosystem.

This repository implements a Python package for the SparkFun Qwiic SGP40. This package works with Python, MicroPython and CircuitPython.

### Contents

* [About](#about-the-package)
* [Getting Started](#getting-started)
* [Installation](#installation)
* [Supported Platforms](#supported-platforms)
* [Documentation](https://docs.sparkfun.com/qwiic_sgp40_py/classqwiic__sgp40_1_1qwiic__sgp40_1_1_qwiic_s_g_p40.html)
* [Examples](#examples)

## About the Package

This python package enables the user to access the features of the SGP40 via a single Qwiic cable. This includes reading the volatile organic compound (VOC) index, perform a self-test, and more. The capabilities of the SGP40 are each demonstrated in the included examples.

New to qwiic? Take a look at the entire [SparkFun qwiic ecosystem](https://www.sparkfun.com/qwiic).

### Supported SparkFun Products

This Python package supports the following SparkFun qwiic products on Python, MicroPython and Circuit python. 

* [SparkFun Air Quality Sensor - SGP40](https://www.sparkfun.com/sparkfun-air-quality-sensor-sgp40-qwiic.html)

### Supported Platforms

| Python | Platform | Boards |
|--|--|--|
| Python | Linux | [Raspberry Pi](https://www.sparkfun.com/raspberry-pi-5-8gb.html) , [NVIDIA Jetson Orin Nano](https://www.sparkfun.com/nvidia-jetson-orin-nano-developer-kit.html) via the [SparkFun Qwiic SHIM](https://www.sparkfun.com/sparkfun-qwiic-shim-for-raspberry-pi.html) |
| MicroPython | Raspberry Pi - RP2, ESP32 | [SparkFun RP2040 Thing+](https://www.sparkfun.com/sparkfun-thing-plus-rp2040.html), [SparkFun RP2350 Thing+](https://www.sparkfun.com/sparkfun-thing-plus-rp2350.html), [SparkFun ESP32 Thing+](https://www.sparkfun.com/sparkfun-thing-plus-esp32-wroom-usb-c.html)
|CircuitPython | Raspberry Pi - RP2, ESP32 | [SparkFun RP2040 Thing+](https://www.sparkfun.com/sparkfun-thing-plus-rp2040.html), [SparkFun RP2350 Thing+](https://www.sparkfun.com/sparkfun-thing-plus-rp2350.html), [SparkFun ESP32 Thing+](https://www.sparkfun.com/sparkfun-thing-plus-esp32-wroom-usb-c.html)

> [!NOTE]
> The listed supported platforms and boards are the primary platform targets tested. It is fully expected that this package will work across a wide variety of Python enabled systems. 

## Installation 

The first step to using this package is installing it on your system. The install method depends on the python platform. The following sections outline installation on Python, MicroPython and CircuitPython.

### Python 

The package is primarily installed using the `pip` command, downloading the package from the Python Index - "PyPi". Note - the below instructions outline installation an Linux-based (Raspberry Pi) system.

#### PyPi Installation

The SparkFun Qwiic SGP40 Python package is part of the overall SparkFun Qwiic Python package which is hosted on PyPi. On systems that support PyPi installation via pip, this library is installed using the following commands

For all users (note: the user must have sudo privileges):
```sh
sudo pip install sparkfun-qwiic
```
For the current user:

```sh
pip install sparkfun-qwiic
```
---
---
> [!CAUTION]
> **TODO** Put together how this works with the new virtual environments used with the latest Python install
---
---
#### Local Installation
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
pip install sparkfun_qwiic_sgp40-<version>.tar.gz
```

### MicroPython Installation
If not already installed, follow the [instructions here](https://docs.micropython.org/en/latest/reference/mpremote.html) to install mpremote on your computer.

Connect a device with MicroPython installed to your computer and then install the package directly to your device with mpremote mip.
```sh
mpremote mip install github:sparkfun/qwiic_sgp40_py
```

### CircuitPython Installation
If not already installed, follow the [instructions here](https://docs.circuitpython.org/projects/circup/en/latest/#installation) to install CircUp on your computer.

Ensure that you have the latest version of the SparkFun Qwiic CircuitPython bundle. 
```sh
circup bundle-add sparkfun/Qwiic_Py
```

Finally, connect a device with CircuitPython installed to your computer and then install the package directly to your device with circup.
```sh
circup install --py qwiic_sgp40
```

Example Use
 ---------------
Below is a quickstart program to print Volatile Organic Compound (VOC) Index read from the SGP40.

See the examples directory for more detailed use examples and [examples/README.md](https://github.com/sparkfun/qwiic_sgp40_py/blob/main/examples/README.md) for a summary of the available examples.

```python
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
```

<p align="center">
<img src="https://cdn.sparkfun.com/assets/custom_pages/3/3/4/dark-logo-red-flame.png" alt="SparkFun - Start Something">
</p>
