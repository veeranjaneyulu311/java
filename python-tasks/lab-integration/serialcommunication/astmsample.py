from typing import List

# from astm_serial.client import AstmConn
#
# astm = AstmConn(port='COM3', baudrate=9600, timeout=60)
#
# astm.send_string(string='1H|\^&|||HOST^P_1|||||BIOLIS NEO^SYSTEM1||P|1|20161019212729')

print(hex(sum(map(ord, 'test')) & 0xFF))
