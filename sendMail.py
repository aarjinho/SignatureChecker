import smtplib
import ssl
from email.message import EmailMessage
import os
from datetime import datetime
from email.message import EmailMessage
import smtplib
import ssl



def sendPDF(teacherPath, email):
    # Get the current date and time
    now = datetime.now()

    # Define the format of the day and time in the file name
    day_format = "%A %d %B %Y"  # e.g. "jeudi 26 janvier"
    time_format = "%Hh%M"  # e.g. "10h00
    pdf_files = []

    # Iterate over all PDF files in the directory
    for file_name in os.listdir(teacherPath):
        if file_name.endswith(".pdf"):
            # Split the file name by underscore to separate the day and time
            parts = file_name.split("_")
            # Extract the day and time strings from the file name
            day_string = parts[1]
            day_string = day_string.replace("fevrier", "février").replace("aout", "août").replace("decembre", "décembre")
            time_string = parts[2][:-4]  # remove ".pdf" from the end of the string
            # Convert the day string to a datetime object
            day = datetime.strptime(day_string, day_format)
            # Convert the time string to a datetime object
            start_time, end_time = time_string.split(" - ")
            start_time = datetime.strptime(start_time, time_format)
            end_time = datetime.strptime(end_time, time_format)
            # Check if the day and time are in the past
            if day < now or (day == now and start_time < now):
                # The file is in the past, so do not add it to the list
                continue
            else:
                # The file is in the future, add it to the list
                pdf_files.append(teacherPath + "/"  + file_name)
    send_email(pdf_files, email)


def send_email(pdf_files, email):
    # Define email sender and receiver
    email_sender = 'signaturechecker@gmail.com'
    email_password = 'ifvolabkduxufibn'
    email_receiver = email

    # Set the subject and body of the email
    subject = 'Feuilles de présences'
    body = """"
    Bonjour, ci-joint les feuilles de présences pour vos prochaines séances de la semaine.



    Message généré automatiquement par SignatureChecker.
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject

    em.set_content(body)
    for pdf in pdf_files:

        with open(pdf, 'rb') as f:
            file_data = f.read()
            file_name = f.name.split("/")[-1]
        em.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)


    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
        print("Email sent to " + email_receiver)


