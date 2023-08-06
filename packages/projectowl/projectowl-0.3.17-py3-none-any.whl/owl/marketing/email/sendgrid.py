"""API for sendgrid.

https://sendgrid.com/docs/API_Reference/api_v3.html
"""

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class SendGridAPI(object):
  def __init__(self, api_key):
    self.api_key = api_key

  def send_emails(self, sender, targets, template_id, contents={}):
    """Send email to targets.

    Args:
      sender: sender email.
      targets: list of target emails.
      template_id: id of sendgrid template.
      contents: dict of custom field name and value.
    """
    message = Mail(
        from_email=sender,
        to_emails=targets,
        subject='Sending with Twilio SendGrid is Fun',
        html_content=
        '<strong>and easy to do anywhere, even with Python</strong>')
    sg = SendGridAPIClient(self.api_key)
    response = sg.send(message)
    # succeed
    if 200 <= response.status_code < 300:
      return True
    else:
      raise Exception(response.body)