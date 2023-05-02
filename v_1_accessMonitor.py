import pyinotify
import re
import smtplib
from email.mime.text import MIMEText
import datetime

# Define the paths to the system log files
log_files = ['/var/log/auth.log', '/var/log/syslog']

# Define the regular expression pattern to search for
pattern = r'(Failed password|Invalid user)'

# Define the email settings
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'your-email@gmail.com'
smtp_password = 'your-email-password'
recipient = 'recipient-email@example.com'

# Define the function to send the email alert
def send_alert(message):
    msg = MIMEText(message)
    msg['From'] = smtp_username
    msg['To'] = recipient
    msg['Subject'] = 'Alert: Unauthorized Access Detected'
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(smtp_username, recipient, msg.as_string())
    server.quit()

# Define the function to handle file changes
def handle_event(event):
    if event.maskname == 'IN_MODIFY':
        for log_file in log_files:
            if event.pathname == log_file:
                with open(log_file) as f:
                    log_contents = f.read()
                    if re.search(pattern, log_contents):
                        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        message = f'Unauthorized access detected in {log_file} at {current_time}'
                        send_alert(message)

# Define the watch manager and notifier
wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(wm, default_proc_fun=handle_event)

# Add the log files to the watch list
for log_file in log_files:
    wm.add_watch(log_file, pyinotify.IN_MODIFY)

# Start the notifier
notifier.loop()

















# import pyinotify
# import re
# import smtplib
# from email.mime.text import MIMEText
# 
# # Define the path to the system log file
# log_file = '/var/log/auth.log'
# 
# # Define the regular expression pattern to search for
# pattern = r'(Failed password|Invalid user)'
# 
# # Define the email settings
# smtp_server = 'smtp.gmail.com'
# smtp_port = 587
# smtp_username = 'your-email@gmail.com'
# smtp_password = 'your-email-password'
# recipient = 'recipient-email@example.com'
# 
# # Define the function to send the email alert
# def send_alert(message):
#     msg = MIMEText(message)
#     msg['From'] = smtp_username
#     msg['To'] = recipient
#     msg['Subject'] = 'Alert: Unauthorized Access Detected'
#     server = smtplib.SMTP(smtp_server, smtp_port)
#     server.starttls()
#     server.login(smtp_username, smtp_password)
#     server.sendmail(smtp_username, recipient, msg.as_string())
#     server.quit()
# 
# # Define the function to handle file changes
# def handle_event(event):
#     if event.pathname == log_file and event.maskname == 'IN_MODIFY':
#         with open(log_file) as f:
#             log_contents = f.read()
#             if re.search(pattern, log_contents):
#                 send_alert('Unauthorized access detected in log file')
# 
# # Define the watch manager and notifier
# wm = pyinotify.WatchManager()
# notifier = pyinotify.Notifier(wm, default_proc_fun=handle_event)
# 
# # Add the log file to the watch list
# wm.add_watch(log_file, pyinotify.IN_MODIFY)
# 
# # Start the notifier
# notifier.loop()

