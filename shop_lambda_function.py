from __future__ import print_function
import time
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Function to send email

def send_email(message):
    SENDER = "<ENTER A VERIFIED EMAIL>"  # Must be verified in AWS SES Email
    RECIPIENT = "<ENTER A VERIFIED EMAIL>"  # Must be verified in AWS SES Email

    # Replace with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"

    # The subject line for the email.
    SUBJECT = "This order is destined for shop1!!"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = f"""Hey Hi...\r\n
                 Here is an order:\n {message} \n
                 Thank you!"""
                 

    # The HTML body of the email.
    BODY_HTML = f"""
    <html>
    <head></head>
    <body>
        <h1>Hey Hi,</h1>
        <p>Here is an order:</p>
        <p><strong>{message}</strong></p>
        <p>Thank you!</p>
    </body>
    </html>
    """
    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=AWS_REGION)

    # Check if the configuration set is set or create it
    try:
        response = client.create_configuration_set(
            ConfigurationSet={
                'Name': 'my-config-set'
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConfigurationSetAlreadyExists':
            print("Configuration set already exists.")
        else:
            print(f"Error creating configuration set: {e.response['Error']['Message']}")
            return
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT
                },
            },
            Source=SENDER,
            ConfigurationSetName='my-config-set',
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:", response['MessageId'])


def lambda_handler(event, context):
    for record in event['Records']:
        payload = record["body"]
        print("Payload:", payload)
        send_email(payload)
    print("Shop1 processing complete")
    time.sleep(5)
