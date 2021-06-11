#-----------------------------------------------------------------------------
# qwiic_sgp40.py
#
# Python library for the SparkFun Air Quality Sensor - SGP40 (Qwiic).
#   https://www.sparkfun.com/products/18345
#
#------------------------------------------------------------------------
#
# Written by Priyanka Makin @ SparkFun Electronics, June 2021
# This python module heavily is heavily based on the driver written by 
# DFRobot and leverages its VOC algorithm. It can be found here:
# https://github.com/DFRobot/DFRobot_SGP40/tree/master/Python/raspberrypi
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem 
#
# More information on qwiic is at https:// www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#==================================================================================
# Copyright (c) 2020 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#==================================================================================

"""
qwiic_sgp40
===========
Python module for the SparkFun Air Quality Sensor - SGP40 (Qwiic).

This package is a port of the existing [SparkFun SGP40 Arduino Library](https://github.com/sparkfun/SparkFun_SGP40_Arduino_Library) and is heavily based on the driver written by [DFRobot](https://github.com/DFRobot/DFRobot_SGP40/tree/master/Python/raspberrypi).

This package can be used in conjunction with the overall [SparkFun Qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)

New to qwiic? Take a look at the entire [SparkFun Qwiic Ecosystem](https://www.sparkfun.com/qwiic).
"""
# ----------------------------------------------------------------------

import math
import time
import qwiic_i2c
from DFRobot_SGP40_VOCAlgorithm import DFRobot_VOCAlgorithm

_DEFAULT_NAME = "Qwiic SGP40"

_AVAILABLE_I2C_ADDRESS = [0x59]

class QwiicSGP40(object):
  """
  QwiicSGP40
    
    :param address: The I2C address to use for the device.
                    If not provided, the default address is used.
    :param i2c_driver: An existing i2c driver object. If not provided a
                    a driver object is created.
    :return: The GPIO device object.
    :rtype: Object
  """
  # Constructor
  device_name = _DEFAULT_NAME
  available_addresses = _AVAILABLE_I2C_ADDRESS
  
  # SGP40 I2C commands
  #SGP40_MEASURE_RAW = [0x26, 0x0F]
  SGP40_MEASURE_RAW = 0x260F
  SGP40_MEASURE_TEST = [0x28, 0x0E]
  SGP40_HEATER_OFF = [0x36, 0x15]
  SGP40_SOFT_RESET = [0x00, 0x06]
  
  # SGP40 Measure Test Results
  SGP40_MEASURE_TEST_PASS = 0xD400
  SGP40_MEASURE_TEST_FAIL = 0x4B00
  
  DURATION_WAIT_MEASURE_TEST = 0.25
  DURATION_READ_RAW_VOC = 0.03
  
  # Constructor
  def __init__(self, address=None, i2c_driver=None):
    
    # Did the user specify an I2C address?
    self.address = address if address != None else self.available_addresses[0]
    
    # Load the I2C driver is one isn't provided
    if i2c_driver == None:
      self._i2c = qwiic_i2c.getI2CDriver()
      if self._i2c == None:
        print("Unable to load I2C driver for this platform.")
        return
    else:
      self._i2c = i2c_driver
        
    self.__my_vocalgorithm = DFRobot_VOCAlgorithm()
    self.__temperature_c = 0
    self.__relative_humidity = 0
    self.__rh = 0
    self.__temc = 0
    self.__rh_h = 0
    self.__rh_l = 0
    self.__temc_h = 0
    self.__temc_l = 0
    self.__temc__crc = 0
    self.__rh__crc = 0

  # --------------------------------------------------------------------
  # is_connected()
  #
  # Is an actual board connected to our sysem?
  def is_connected(self):
    """
      Determine if a Qwiic SGP40 device is connected to the system.
      
      :return: True if the device is connected, false otherwise.
      :rtype: bool
    """
    return qwiic_i2c.isDeviceConnected(self.address)

  # --------------------------------------------------------------------
  # begin()
  # 
  # Initialize I2C communication and wait through warm-up time.
  def begin(self, warm_up_time = 10):
    """
      Initialize the operation of the Qwiic SGP40 and wait through warm-
      up time. Run is_connected() and measure_test().
      
      :return: Returns true if the intialization was successful, false otherwise.
      :rtype: bool
    """
    if self.is_connected() == True:
      
      # # For debugging
      # print("\nSGP40 passed is_connected!")
      # return True 
      
      print("\nWaiting " + str(warm_up_time) + " seconds for the SGP40 to warm-up.")
      
      self.__my_vocalgorithm.vocalgorithm_init()
      start_time = int(time.time())
      while(int(time.time()) - start_time < warm_up_time):
        self.get_VOC_index()
      return self.measure_test()
    
    return False

  # --------------------------------------------------------------------
  # measure_test()
  #
  # Sensor runs chip self test
  def measure_test(self):
    """
      Sensor runs chip self test.
      
      :return: Returns 0 if the self-test succeeded and 1 if it failed.
      :rtype: int
    """
    self._i2c.writeWord(self.address, 0, self.SGP40_MEASURE_TEST)
    time.sleep(self.DURATION_WAIT_MEASURE_TEST)
    result = self._i2c.readWord(self.address, 0)
    if result == self.SGP40_MEASURE_TEST_PASS:
      return 0
    else:
      return 1

  # --------------------------------------------------------------------
  # soft_reset()
  #
  # Performs a soft reset
  def soft_reset(self):
    """
      Sensor reset
      
      :rtype: void - returns nothing
    """
    self._i2c.writeWord(self.address, 0, self.SGP40_SOFT_RESET)

  # --------------------------------------------------------------------
  # heater_off()
  #
  # Turns the heater off
  def heater_off(self):
    """
      Turns the hotplate off and puts sensor in idle mode.
      
      :rtype: void - returns nothing
    """
    self._i2c.writeWord(self.address, 0, self.SGP40_HEATER_OFF)

  # --------------------------------------------------------------------
  # measure_raw(SRAW_ticks, self.__relative_humidity, self.__temperature_c)
  #
  # The raw signal is returned in SRAW_ticks. The user can provide relative
  # humidity or temperature parameters if desired.
  def measure_raw(self, SRAW_ticks, __relative_humidity = 50, __temperature_c = 25):
    """
      Returns the raw data. See the SGP40 datasheet for more info.
      
      :param SRAW_ticks: variable to assign raw measurement to
      :param self.__relative_humidity: float relative humidity between 0 and 100%.
      :param self.__temperature_c: float temperature in celcius between -45 and 130 degrees.
      
      :return: 0 if CRC checks out, -1 otherwise
      :rtype: int
    """
    # Check boundaries of relative humidity and temperature
    if self.__relative_humidity < 0:
      self.__relative_humidity = 0
    if self.__relative_humidity > 100:
      self.__relative_humidity = 100
    if self.__temperature_c < -45:
      self.__temperature_c = -45
    if self.__temperature_c > 130:
      self.__temperature_c = 130
      
    # Calculate relative humidity and temperature ticks
    self.__rh = int(((self.__relative_humidity*65535)/100+0.5))
    self.__temc = int(((self.__temperature_c+45)*(65535/175)+0.5))
    # Break it into bytes and calculate CRC
    self.__rh_h = int(self.__rh)>>8
    self.__rh_l = int(self.__rh)&0xFF
    self.__rh__crc = self.__crc(self.__rh_h, self.__rh_l)
    self.__temc_h = int(self.__temc)>>8
    self.__temc_l = int(self.__temc)&0xFF
    self.__temc__crc = self.__crc(self.__temc_h, self.__temc_l)
    
    # TODO: figure out if this is right...
    self._i2c.writeWord(self.address, self.SGP40_MEASURE_RAW, 0)
    
    self._i2c.writeByte(self.address, 0, self.__rh_h)
    self._i2c.writeByte(self.address, 0, self.__rh_l)
    self._i2c.writeByte(self.address, 0, self.__rh__crc)
    
    self._i2c.writeByte(self.address, 0, self.__temc_h)
    self._i2c.writeByte(self.address, 0, self.__temc_l)
    self._i2c.writeByte(self.address, 0, self.__temc__crc)
    
    time.sleep(self.DURATION_READ_RAW_VOC)
    
    # Data is read back in 3 bytes: data (MSB) / data (LSB) / Cecksum
    result = self._i2c.readBlock(self.address, 0, 3)
    
    if self.__check_crc(result) == 0:
      SRAW_ticks = result[0] << 8 | result[1]
      return 0
    else:
      return -1
  
  # --------------------------------------------------------------------
  # __check__crc(raw)
  #
  # Verify the calibration value of the sensor
  def __check_crc(self, raw):
    """
      Verify the calibration value of the sensor
      
      :param raw: list parameter to check
      :return: -1 if the check failed, 0 if it succeeded
      :rtype: int
    """
    assert (len(raw) == 3)
    if self.__crc(raw[0], raw[1]) != raw[2]:
      return -1
    return 0
  
  # --------------------------------------------------------------------
  # __crc(data_1, data_2)
  #
  # CRC calculation
  def __crc(self, data_1, data_2):
    """
      CRC calculation
      
      :param data_1: high 8 bits of data
      :param data_2: low 8 bits of data
      :return: calibration value
      :rtype: int
    """
    crc = 0xff
    list = [data_1, data_2]
    for i in range(0, 2):
      crc = crc ^ list[i]
      for bit in range(0, 8):
        if (crc & 0x08):
          crc = ((crc << 1) ^ 0x31)
        else:
          crc = (crc << 1)
      crc = crc & 0xFF
      
  # --------------------------------------------------------------------
  # get_VOC_index(self.__relative_humidity, self.__tempertature_c)
  #
  # Get VOC index
  def get_VOC_index(self, __relative_humidity = 50, __temperature_c = 25):
    """
      Get VOC index
      
      :param self.__relative_humidity: float relative humidity between 0 and 100%.
      :param self.__temperature_c: float temperature in celcius between -45 and 130 degrees.
      
      :return: VOC index
      :rtype: int
    """
    raw = 0
    self.measure_raw(raw, self.__relative_humidity, self.__temperature_c)
    
    if raw < 0:
      return -1
    else:
      voc_index = self.__my_vocalgorithm.socalgorithm_process(raw)
      return voc_index 
