from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ConnectionException
import time

plc_ip = "192.168.50.2"
plc_port = 5002

client = ModbusTcpClient(plc_ip, port=plc_port)

try:
    connection = client.connect()
    if connection:
        while True:  
            address = 0
            value = 1000
            result = client.write_register(address, value)
            
            if not result.isError():
                print("Data successfully written.")
            else:
                print("Failed to write data.")

            time.sleep(1)  
    else:
        print("Connection failed.")
except ConnectionException as ex:
    print(f"Connection Error: {ex}")
finally:
    client.close()
