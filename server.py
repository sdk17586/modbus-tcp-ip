import sys
import logging
import threading
import time
from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock

sys.path.append('/usr/local/lib/python3.6/dist-packages')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('modbus_server.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0]*100),
    co=ModbusSequentialDataBlock(0, [0]*100),
    hr=ModbusSequentialDataBlock(0, [0]*100),
    ir=ModbusSequentialDataBlock(0, [0]*100)
)
context = ModbusServerContext(slaves=store, single=True)

def update_data(context):
    while True:
        try:
            logger.debug("update_data function is called")
            register = 0
            slave_id = 0x00
            values = context[slave_id].getValues(fx=3, address=register, count=1)
            logger.debug(f"Current register value: {values[0]}")
            print(f"Current register value: {values[0]}")
        except Exception as e:
            logger.exception("Error in update_data")
        time.sleep(1)

update_thread = threading.Thread(target=update_data, args=(context,))
update_thread.daemon = True
update_thread.start()

logger.info("Starting Modbus TCP Server on 192.168.50.2:5002")

StartTcpServer(context, address=("192.168.50.2", 5002))
