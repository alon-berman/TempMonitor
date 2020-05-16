import time
import ttn



cert_path = r"C:\Users\Alon_Berman\Desktop\TempMonitor\temperature_monitor\certificate\cert.txt"
app_id = "temp_monitor_tester"
access_key = "ttn-account-v2.bznvspfhnrWpP1AkkHKw5bEsTJ-blN9Ywkx5IJQzOXY"

with open(cert_path) as cert:
    cert_data = cert.read()


def uplink_callback(msg, client):
    print("Received uplink from ", msg.dev_id)
    print(msg)


handler = ttn.HandlerClient(app_id, access_key)  #, cert_path=cert_path)
print(handler)
# # using mqtt client
# mqtt_client = handler.data()
# mqtt_client.set_uplink_callback(uplink_callback)
# print(handler)mqtt_client.connect()
# time.sleep(60)
# mqtt_client.close()
#
# # using application manager client
# app_client = handler.application()
# my_app = app_client.get()
# print(my_app)
# my_devices = app_client.devices()
# print(my_devices)