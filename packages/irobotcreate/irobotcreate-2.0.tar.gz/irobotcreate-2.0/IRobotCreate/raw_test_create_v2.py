import serial
import time

# create defaults to 115200 baud
#create = serial.Serial('COM6',115200)
create = serial.Serial('/dev/ttyUSB0',115200)

print("Sending OI START command (128). You should hear a high-pitch beep.")
create.write(b'\x80')
print("Sleeping 1 second (giving create time to change mode)")
time.sleep(1)

print("Sending SAFE MODE command (131).")
# Send SAFE MODE (131) or FULL MODE (132)
create.write(b'\x84')
print("Sleeping 1 second (giving create time to change mode)")
time.sleep(1)

print('Setting song 0 to three notes C,E,G.')
#                            C       E       G
create.write(b'\x8C\x00\x03\x48\x20\x4C\x20\x4F\x20')

print('Setting song 1 to three notes G,E,C.')
create.write(b'\x8C\x01\x03\x4F\x10\x4C\x10\x48\x10')

print('Playing song 0')
create.write(b'\x8D\x00')
print('Sleeping 3 seconds for song to play')
time.sleep(3)

print('Playing song 1')
create.write(b'\x8D\x01')
print('Sleeping 3 seconds for song to play')
time.sleep(3)


print('Setting LED digits')
create.write(b'\xA3\xFF\xFF\xFF\xFF')
time.sleep(10)


print('Sending OI START command (128) going back to passive mode.')
create.write(b'\x80')
print('Sleeping 1 second (giving create time to change mode)')
time.sleep(1)

"""
create.write(b'\x07')
ver = create.read(256)
print(ver)
"""

print("Sending STOP command (173). You should hear a low-pitch beep.")
create.write(b'\xAD')

print("Done")