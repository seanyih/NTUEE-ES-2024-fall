# ble_scan_connect.py:
from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate
import time

class ScanDelegate(DefaultDelegate):
	def __init__(self):
		DefaultDelegate.__init__(self)
	def handleDiscovery(self, dev, isNewDev, isNewData):
		if isNewDev:
			print ("Discovered device", dev.addr)
		elif isNewData:
			print ("Received new data from", dev.addr)


		

#scan with timeout 10 sec.
scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)
n=0
addr = []

#print all device
for dev in devices:
	print ("%d: Device %s (%s), RSSI=%d dB" % (n, dev.addr, dev.addrType, dev.rssi))
	addr.append(dev.addr)
	n += 1
	for (adtype, desc, value) in dev.getScanData():
		print (" %s = %s" % (desc, value))

#select device to be connected
number = input('Enter your device number: ')
print('Device', number)
num = int(number)
print(addr[num])

#
print("Connecting...")
dev = Peripheral(addr[num], 'random')

#print all services and characteristics
print("Services...")
services = dev.getServices()
for svc in services:
	print("UUID:", svc.uuid)
	if(svc.uuid == "0000fff0-0000-1000-8000-00805f9b34fb"):
		des = svc.getDescriptors()
		print(des[0].uuid)
		print(des[1].uuid)
		des[1].write(b'x\01x\00')
	
print("Characteristics...")
characs = dev.getCharacteristics()
targetc = 0
for c in characs:
	print("Characteristic:", c.uuid)
	# if (c.supportsRead()):
	# print(str(c.read()))

	#our writing target: 0xFFF1
	if(c.uuid == "0000fff1-0000-1000-8000-00805f9b34fb"):
		#c.write(b'\xFF\xFF')
		targetc = c
	
notify = dev.waitForNotifications(30)
print(notify)



