import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from Language.lang_handler import load_language

TEMPLATE_DICT = None

def send_mail(contact_name: str, contact_email: str, template: str, additional_msg=None, **kwargs):
    """
    This function handles mail sending to the responsible personnel in the POC in case the watchdog detected failure in
    the system. the sending mail address in it's password are defined inside this function.
    :param template: the msg template for each monitoring field (temperature, humidity etc)
    :param contact_name:
    :param contact_email:
    :param additional_msg: Optional. Gives you the ability to apply custom message to mail.
    :return:
    """
    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login('saliniv0@gmail.com', '1f2c3x4vBoom')

    # For each contact, send the email:
    for ind, email in enumerate(contact_email):
        msg = MIMEMultipart()  # create a message

        # setup the parameters of the message
        msg['From'] = 'saliniv0+temperature-alert@gmail.com'
        msg['To'] = email
        msg['Subject'] = TEMPLATE_DICT[template]["title"]
        message = \
            f"Hello {contact_name},\n This is an automatic message from Temperature Watchdog"

        message += TEMPLATE_DICT[template]["function"](**kwargs)  # this functions chooses template
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


def temperature_msg_template(device_id, previous_temp):
    return \
        f"The current temperature is: {previous_temp} .\n" \
        f"Device ID : {device_id}."


def prepare_template(lang):
    global TEMPLATE_DICT
    lang_dict = load_language(lang)
    TEMPLATE_DICT = {
            "temperature": {
                "title": lang_dict["email"]["title"],
                "function": temperature_msg_template
            }
    }

