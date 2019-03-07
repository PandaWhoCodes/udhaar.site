import requests
from secrets import mailer_key

foorter_text = """


This email was sent by: 
"""


def send_mail(borrower, email_address, amount, lender_email, lender_name):
    """

    :param email_address: email address of the borrower
    :param name: name of the lender
    :param amount: amount
    :param borrower: name of the borrower
    :param lender_email: email address of the lender
    :return:
    """
    from_ = lender_name + " @ Udhaar Manager <noreply@mail.udhaar.site>"
    text = "Hey " + borrower + "! Just a gentle reminder, you still owe me Rs. " + str(
        amount) + foorter_text + " " + lender_email

    return requests.post(
        "https://api.mailgun.net/v3/mail.udhaar.site/messages",
        auth=("api", mailer_key),
        data={"from": from_,
              "to": email_address,
              "subject": "A gentle reminder from " + lender_name,
              "text": text})
