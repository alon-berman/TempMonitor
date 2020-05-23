import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from time import sleep, time
import sys

from CloudCommunication.CloudOperation import assign_cloud_object
from DataHandlers.DataFilter import json_filter

_BUFF_SIZE = 10
_MIN_BAT_VOLTAGE = 0.85


def load_client_details(client_details_json_path):
    with open(client_details_json_path) as f:
        return json.load(f)


class BusinessMonitor:
    """
    Each client of the service has this process running on server monitoring the temperature.

    """
    def __init__(self, device_ids, cloud_type, business_details, log_level, debug_mode):
        # Init parameters
        self.last_email_sent_seconds = time()
        self.should_send_email = False
        self.temperature_history_buffer = []
        self.prev_temp = None
        self.device_list = []

        # Client Data
        self.business_details = business_details
        self.device_ids = device_ids

        # Cloud Interface
        self.cloud_handler = assign_cloud_object(cloud_type)

        # Client-configured Parameters
        # self.temperature_thresh = temperature_thresh  # min_temp, max_temp
        # self.temp_stabilization_thresh = temp_stabilization_thresh
        # self.min_battery_volt_alert = min_battery_volt_alert
        # self.time_between_alerts = time_between_alerts_sec

        # Advanced
        self.log_level = log_level
        self.debug_mode = debug_mode

        self.prepare_run()
        self.monitor()

    def prepare_run(self):
        pass

    def monitor(self):
        while True:
            for device_id in self.device_ids:
                self.curr_temp_c_dict[device_id] = json_filter(self.cloud_handler.get_raw_data(),
                                                               "IMEI", device_id)[0]
                self.check_temperature()

    def check_temperature(self):
        # if abs(self. - self.temperature_history_buffer[-1]) > self.temp_stabilization_thresh:
        #     print('Waiting for temp to stabilize...')
        #     sys.stdout.flush()

        # else:
        if self.temperature_thresh[0] <= self.curr_temp_c_dict <= self.temperature_thresh[1]:
            print('business as usual')
            sys.stdout.flush()

        else:
            if self.should_send_email:
                self.send_mail()
            print('Temperature is not within the thresholds!')
        self.prev_temp = self.curr_temp_c_dict
        if self.temperature_history_buffer == _BUFF_SIZE:
            self.temperature_history_buffer.pop(0)
        self.temperature_history_buffer.append(self.curr_temp_c_dict)

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
    monitor = BusinessMonitor('ClientData/home.json')
    print('done')
