from __future__ import print_function
import qwiic_sgp40
import time
import sys

def run_example():

	print("\nSparkFun Qwiic Air Quality Sensor - SGP40, Function Test\n")
	my_sgp40 = qwiic_sgp40.QwiicSGP40()
	
	# if my_sgp40.begin() == False:
		# print("\nThe Qwiic SGP40 isn't connected to the system. Please check your connection.", \
			# file=sys.stderr)
		# return
	
	print("\nSGP40 ready!")
	
	# if my_sgp40.measure_test() == 0:
		# print("\nSensor self-test passed!")
	# else:
		# print("\nSensor self-test failed.")
		
	#my_sgp40.soft_reset()
	my_sgp40.heater_off()
		
if __name__ == '__main__':
	try:
		run_example()
	except(KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Function Test")
		sys.exit(0)
