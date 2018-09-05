import configparser
from email.message import EmailMessage
import smtplib
import urllib.request


def get_external_ip():
    return urllib.request.urlopen('http://ident.me').read().decode('utf8')


def check_and_notify():
    # Parse the config file
    config_filename = 'ipnotifier.ini'
    config = configparser.ConfigParser()
    config.read(config_filename)

    # Check if the IP has changed
    external_ip = get_external_ip()
    if config['ipnotifier']['current_ip'] != external_ip:
        # Update the config file
        config['ipnotifier']['current_ip'] = external_ip
        with open(config_filename, 'w') as configfile:
            config.write(configfile)

        # Prepare and send notification
        send_email_notification(config)


def send_email_notification(config):
    text_body = 'New IP address reported '\
                'from {}: {}'.format(config['ipnotifier']['location_name'],
                                     config['ipnotifier']['current_ip'])
    # Create the message
    msg = EmailMessage()
    msg.set_content(text_body)
    msg['Subject'] = 'IP Notifier Update'
    msg['From'] = config['email']['from_address']
    msg['To'] = config['email']['to_address']

    # Send the message
    s = smtplib.SMTP(config['email']['smtp_server'], int(config['email']['smtp_port']))
    s.starttls()
    s.login(config['email']['username'], config['email']['password'])
    s.send_message(msg)
    s.quit()


if __name__ == '__main__':
    check_and_notify()
