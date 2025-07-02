import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup

def read_mail():
    # Your Gmail credentials
    username = "mail4avvineeth@gmail.com"
    password = "wlsn owwh fqeh isgr"

    # Connect to Gmail's IMAP server
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(username, password)

    # Select the mailbox you want to access (e.g., "inbox")
    imap.select("inbox")

    # Search for the most recent 5 emails in the mailbox
    status, email_ids = imap.search(None, "ALL")
    email_id_list = email_ids[0].split()
    latest_email_ids = email_id_list[-10:]  # Get the latest 5 email IDs

    email_details = []  # List to store details of each email

    for email_id in latest_email_ids:
        # Fetch the email by ID
        status, msg_data = imap.fetch(email_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        # Extract email details (subject and sender)
        subject, encoding = decode_header(msg["Subject"])[0]
        sender, _ = decode_header(msg["From"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")
        if isinstance(sender, bytes):
            sender = sender.decode(encoding or "utf-8")

        # Extract email body
        email_body = ""
        email_body_html = ""

        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if "attachment" not in content_disposition:
                body = part.get_payload(decode=True)
                if body is not None:
                    if isinstance(body, bytes):
                        body = body.decode()

                    if content_type == "text/plain":
                        email_body += body
                    elif content_type == "text/html":
                        email_body_html += body

        # Remove HTML tags using BeautifulSoup
        soup = BeautifulSoup(email_body_html, "html.parser")
        email_body_text = soup.get_text()

        # Store details in a dictionary
        email_dict = {
            "Subject": subject,
            "From": sender,            
            "Body_Text": email_body_text,
            "body_html":email_body_html
        }

        email_details.append(email_dict)  # Append the dictionary to the list

    # Close the mailbox and logout
    imap.close()
    imap.logout()

    return email_details  # Return the list of email dictionaries
