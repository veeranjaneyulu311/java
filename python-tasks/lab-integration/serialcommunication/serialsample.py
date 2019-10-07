# You will need to know the number of the com port into which you have plugged your device,
# the device baud rate,
# number of bits in the data byte and parity
# If you have information about the Stop Bits then use it, otherwise set them to 2
import time
import serial




ser = serial.Serial(
    port='COM3',
    baudrate=9600,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,

)



'''
i=0
j=0
print(ser)
while True:
    i = i + 1
    print(ser.read(4),i)
    print("hi")
    time.sleep(10)
    j = j + 1
    print(ser.write('recieved'.encode()),j)
'''


print(ser)
while True:
    time.sleep(10)
    print(ser.read(10))
    print(ser.write('recieved'.encode()))


# def serial_ports():
#     """ Lists serial port names
#
#         :raises EnvironmentError:
#             On unsupported or unknown platforms
#         :returns:
#             A list of the serial ports available on the system
#     """
#     if sys.platform.startswith('win'):
#         ports = ['COM%s' % (i + 1) for i in range(256)]
#     elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
#         # this excludes your current terminal "/dev/tty"
#         ports = glob.glob('/dev/tty[A-Za-z]*')
#     elif sys.platform.startswith('darwin'):
#         ports = glob.glob('/dev/tty.*')
#     else:
#         raise EnvironmentError('Unsupported platform')
#
#     result = []
#     for port in ports:
#         try:
#             s = serial.Serial(port)
#             s.close()
#             result.append(port)
#         except (OSError, serial.SerialException):
#             pass
#     return result
#
#
# if __name__ == '__main__':
#     print(serial_ports())

