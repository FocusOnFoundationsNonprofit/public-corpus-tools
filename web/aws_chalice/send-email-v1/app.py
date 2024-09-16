from chalice import Chalice
import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import json
import base64

app = Chalice(app_name='send-email-v1')

ses_client = boto3.client('ses')
app.api.cors = True  # Enable CORS for all routes

@app.route('/send-email', methods=['POST'], cors=True)
def send_email():
    request = app.current_request
    json_body = request.json_body

    to_address = json_body['to_address']
    email_subject = json_body['email_subject']
    from_address = json_body['from_address']
    email_body_plain = json_body.get('email_body_plain', '')
    email_body_html = json_body.get('email_body_html', '')
    attachments = json_body.get('attachments', [])

    # Create MIME message
    msg = MIMEMultipart('mixed')
    msg['Subject'] = email_subject
    msg['From'] = from_address
    msg['To'] = to_address

    # Create a MIME part for the email body
    if email_body_html:
        msg_alternative = MIMEMultipart('alternative')
        msg.attach(msg_alternative)
        part1 = MIMEText(email_body_plain, 'plain')
        part2 = MIMEText(email_body_html, 'html')
        msg_alternative.attach(part1)
        msg_alternative.attach(part2)
    else:
        part1 = MIMEText(email_body_plain, 'plain')
        msg.attach(part1)

    # Attach files
    for attachment in attachments:
        filename = attachment['filename']
        file_content = base64.b64decode(attachment['content'])
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file_content)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={filename}')
        msg.attach(part)

    response = ses_client.send_raw_email(
        Source=msg['From'],
        Destinations=[msg['To']],
        RawMessage={
            'Data': msg.as_string()
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Email sent successfully!')
    }

# TO UPDATE
# cd /Users/randytrue/Documents/Code/corpus-tools/web/aws_chalice/send-email-v1
# chalice deploy

# - Lambda ARN: arn:aws:lambda:us-west-2:957789311461:function:send-email-v1-dev
# - Rest API URL: https://kllsn7lnqa.execute-api.us-west-2.amazonaws.com/api/

# TEST WITH CURL
'''
curl -X POST https://kllsn7lnqa.execute-api.us-west-2.amazonaws.com/api/send-email -H "Content-Type: application/json" -d '{"to_address": "randytrue@gmail.com", "email_subject": "CURL TEST of lambda function with SES Email", "from_address": "randy@floodlamp.bio", "email_body": "Here is the content of the email."}'
curl -X POST https://kllsn7lnqa.execute-api.us-west-2.amazonaws.com/api/send-email -H "Content-Type: application/json" -d '{"to_address": "randytrue@gmail.com", "email_subject": "CURL TEST of Lambda Function with SES Email", "from_address": "randy@floodlamp.bio", "email_body_plain": "Here is the plain text content of the email with headings, bold, italics, and a link.", "email_body_html": "<h1>Heading Level 1</h1><h2>Heading Level 2</h2><p>This is a <strong>bold</strong> text and this is an <em>italic</em> text.</p><p>Here is a link to <a href=\"https://example.com\">example.com</a>.</p>"}'
'''
