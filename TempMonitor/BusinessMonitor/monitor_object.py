import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import logging
from time import sleep, time
import requests
import sys

_BUFF_SIZE = 10
_MIN_BAT_VOLTAGE = 0.85


def load_client_details(client_details_json_path):
    with open('../client_data/home.json') as f:
        return json.load(f)


class BusinessMonitor:
    def __init__(self, client_details_json_path=None):
        self.client_data = load_client_details(client_details_json_path)[0]
        self.client_data = self.client_data
        self.business_details = self.client_data['business_details']
        self.dev_id = self.client_data['dev_id']

        # self.cloud_server = self.client_data['cloud_server']
        # self.cloud_port = self.client_data['cloud_port']
        # self.app_id = self.client_data['app_id']
        # self.access_key = self.client_data['access_key']

        self.temperature_thresh = self.client_data['temperature_thresh']  # min_temp, max_temp
        self.temp_stabilization_thresh = self.client_data['temp_stabilization_thresh']

        self.temperature_history_buffer = []
        self.prev_temp = 0

        self.time_between_alerts = self.client_data['time_between_alerts_sec']
        self.last_email_sent_seconds = time()
        self.should_send_email = False

        self.min_battery_volt_alert = self.client_data['min_battery_volt_alert']
        self.log_level = self.client_data['log_level']
        self.debug_mode = self.client_data['debug_mode']

        # self.mqtt.client = self.connect_mqtt()
        # self.topic = f"{self.app_id}/devices/{self.dev_id}/up"
        self.init()
        self.listen()

    # Define event callbacks
    def on_disconnect(self, userdata, rc=0):
        logging.debug("Disconnected result code " + str(rc))
        self.mqtt_client.loop_stop()

    def on_connect(self, client, userdata, flags, rc):
        print("rc: " + str(rc))

    def on_message(self, client, obj, msg):
        # Assign data to variables
        payload_as_dict = json.loads(msg.payload.decode('ascii'))
        temperature_c = payload_as_dict['payload_fields']['TempC_DS']
        battery_voltage = payload_as_dict['payload_fields']['BatV']

        self.check_temperature(temperature_c)
        self.is_battery_low(battery_voltage)
        print(f'Temperature is: {temperature_c} Celsius')

    def init(self):
        self.mqtt_client.subscribe(self.topic, )

    def listen(self):
        while True:
            self.mqtt_client.loop()
            sleep(3)

    def send_note(self):
        report = dict()
        report['measured_temp'] = self.prev_temp
        try:
            requests.post('https://maker.ifttt.com/trigger/notify/with/key/zjH2Qk3YYziQ_hSqCYnVl', data=report)
        except:
            logging.warning('could not send notification')

    def check_temperature(self, curr_temp_c):
        if abs(curr_temp_c - self.temperature_history_buffer[-1]) > self.temp_stabilization_thresh:
            print('Waiting for temp to stabilize...')
            sys.stdout.flush()

        else:
            if self.temperature_thresh[0] <= curr_temp_c <= self.temperature_thresh[1]:
                print('business as usual')
                sys.stdout.flush()

            else:
                if self.should_send_email:
                    self.send_mail()
                print('Temperature is not within the thresholds!')
        self.prev_temp = curr_temp_c
        if self.temperature_history_buffer == _BUFF_SIZE:
            self.temperature_history_buffer.pop(0)
        self.temperature_history_buffer.append(curr_temp_c)

    def is_battery_low(self, battery_voltage):
        if battery_voltage < self.min_battery_volt_alert:
            if self.should_send_mail:
                self.send_mail(f'Battery is Low! {battery_voltage}V')
        else:
            return

    def should_send_mail(self):
        if time() - self.last_email_sent_seconds < self.time_between_alerts:
            return True
        else:
            return False
        
    def send_mail(self, additional_msg=None):
        """
        This function handles mail sending to the responsible personnel in the POC in case the watchdog detected failure in
        the system. the sending mail address in it's password are defined inside this function.
        :param curr_system: the current working system number
        :param additional_msg: Optional. Gives you the ability to apply custom message to mail.
        :return:
        """
        # set up the SMTP server
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login('saliniv0@gmail.com', '1f2c34vBoom')

        # For each contact, send the email:
        for ind, email in enumerate(self.business_details['contact_email']):
            msg = MIMEMultipart()  # create a message

            # setup the parameters of the message
            msg['From'] = 'saliniv0+temperature-alert@gmail.com'
            msg['To'] = email
            msg['Subject'] = f'Temperature on fridge Exceeds the threshold! now at {self.prev_temp} C'
            message = f"Hello {self.business_details['contact_name']},\n This is an automatic message from Temperature " \
                      f"watchdog.\n" \
                      f"The current temperature is: {self.prev_temp} .\n" \
                      f"Device ID : {self.dev_id}."
            if additional_msg is not None:
                message = message + "\n\n Note:\n" + additional_msg
            # add in the message body
            msg.attach(MIMEText(message, 'plain'))

            # send the message via the server set up earlier.
            s.send_message(msg)
            del msg

        # Terminate the SMTP session and close the connection
        s.quit()
        print('Warning email sent to user')


if __name__ == '__main__':
    # monitor = BusinessMonitor("eu.thethings.network", 1883, "temp_monitor_tester",
    #                           "ttn-account-v2.bznvspfhnrWpP1AkkHKw5bEsTJ-blN9Ywkx5IJQzOXY",
    #                           [-4, 50], dev_id="lht65279777", temp_stabilization_thresh=3,
    #                           debug_mode=True, min_battery_volt_alert=0.85)
    monitor = BusinessMonitor('client_data/home.json')
    print('done')
