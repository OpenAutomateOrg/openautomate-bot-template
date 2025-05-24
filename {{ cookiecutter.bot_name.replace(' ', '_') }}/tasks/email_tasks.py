"""
Email Automation Tasks

Handle email sending, reading, and processing.
"""

from pathlib import Path
from . import log_task_start, log_task_complete, log_task_error

# Optional dependencies - will gracefully fail if not installed
try:
    import smtplib
    import imaplib
    import email
    from email.mime.text import MimeText
    from email.mime.multipart import MimeMultipart
    from email.mime.base import MimeBase
    from email import encoders
    HAS_EMAIL = True
except ImportError:
    HAS_EMAIL = False


def send_simple_email(logger, smtp_config, recipient, subject, message):
    """
    Send a simple text email.
    
    Args:
        logger: Logger instance
        smtp_config: SMTP configuration dict
        recipient: Email address to send to
        subject: Email subject
        message: Email message text
        
    Returns:
        bool: True if sent successfully
    """
    log_task_start(logger, "Send Email")
    
    if not HAS_EMAIL:
        error_msg = "Email libraries not available"
        log_task_error(logger, "Send Email", error_msg)
        raise ImportError(error_msg)
    
    try:
        logger.info(f"📧 Sending email to: {recipient}")
        
        # Create message
        msg = MimeText(message)
        msg['Subject'] = subject
        msg['From'] = smtp_config['from_email']
        msg['To'] = recipient
        
        # Send email
        with smtplib.SMTP(smtp_config['server'], smtp_config['port']) as server:
            server.starttls()
            server.login(smtp_config['username'], smtp_config['password'])
            server.send_message(msg)
        
        logger.info("✅ Email sent successfully")
        log_task_complete(logger, "Send Email", f"Sent to {recipient}")
        return True
        
    except Exception as e:
        log_task_error(logger, "Send Email", str(e))
        raise


def send_html_email(logger, smtp_config, recipient, subject, html_content, text_content=None):
    """
    Send an HTML email with optional text fallback.
    
    Args:
        logger: Logger instance
        smtp_config: SMTP configuration dict
        recipient: Email address to send to
        subject: Email subject
        html_content: HTML content
        text_content: Optional plain text fallback
        
    Returns:
        bool: True if sent successfully
    """
    log_task_start(logger, "Send HTML Email")
    
    if not HAS_EMAIL:
        error_msg = "Email libraries not available"
        log_task_error(logger, "Send HTML Email", error_msg)
        raise ImportError(error_msg)
    
    try:
        logger.info(f"📧 Sending HTML email to: {recipient}")
        
        # Create multipart message
        msg = MimeMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = smtp_config['from_email']
        msg['To'] = recipient
        
        # Add text part if provided
        if text_content:
            text_part = MimeText(text_content, 'plain')
            msg.attach(text_part)
        
        # Add HTML part
        html_part = MimeText(html_content, 'html')
        msg.attach(html_part)
        
        # Send email
        with smtplib.SMTP(smtp_config['server'], smtp_config['port']) as server:
            server.starttls()
            server.login(smtp_config['username'], smtp_config['password'])
            server.send_message(msg)
        
        logger.info("✅ HTML email sent successfully")
        log_task_complete(logger, "Send HTML Email", f"Sent to {recipient}")
        return True
        
    except Exception as e:
        log_task_error(logger, "Send HTML Email", str(e))
        raise


def send_email_with_attachment(logger, smtp_config, recipient, subject, message, attachment_path):
    """
    Send an email with a file attachment.
    
    Args:
        logger: Logger instance
        smtp_config: SMTP configuration dict
        recipient: Email address to send to
        subject: Email subject
        message: Email message text
        attachment_path: Path to file to attach
        
    Returns:
        bool: True if sent successfully
    """
    log_task_start(logger, "Send Email with Attachment")
    
    if not HAS_EMAIL:
        error_msg = "Email libraries not available"
        log_task_error(logger, "Send Email with Attachment", error_msg)
        raise ImportError(error_msg)
    
    try:
        attachment_file = Path(attachment_path)
        if not attachment_file.exists():
            raise FileNotFoundError(f"Attachment file not found: {attachment_path}")
        
        logger.info(f"📧 Sending email with attachment to: {recipient}")
        logger.info(f"📎 Attachment: {attachment_file.name}")
        
        # Create multipart message
        msg = MimeMultipart()
        msg['Subject'] = subject
        msg['From'] = smtp_config['from_email']
        msg['To'] = recipient
        
        # Add message body
        msg.attach(MimeText(message, 'plain'))
        
        # Add attachment
        with open(attachment_file, 'rb') as f:
            part = MimeBase('application', 'octet-stream')
            part.set_payload(f.read())
        
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {attachment_file.name}'
        )
        msg.attach(part)
        
        # Send email
        with smtplib.SMTP(smtp_config['server'], smtp_config['port']) as server:
            server.starttls()
            server.login(smtp_config['username'], smtp_config['password'])
            server.send_message(msg)
        
        logger.info("✅ Email with attachment sent successfully")
        log_task_complete(logger, "Send Email with Attachment", f"Sent to {recipient}")
        return True
        
    except Exception as e:
        log_task_error(logger, "Send Email with Attachment", str(e))
        raise


def send_report_email(logger, smtp_config, recipients, report_data):
    """
    Send a formatted automation report email.
    
    Args:
        logger: Logger instance
        smtp_config: SMTP configuration dict
        recipients: Email address or list of addresses
        report_data: Dictionary with report information
        
    Returns:
        int: Number of emails sent
    """
    log_task_start(logger, "Send Report Email")
    
    try:
        # Ensure recipients is a list
        if isinstance(recipients, str):
            recipients = [recipients]
        
        # Create report content
        subject = f"Automation Report - {report_data.get('bot_name', 'Unknown Bot')}"
        
        html_content = f"""
        <html>
        <body>
            <h2>🤖 Automation Report</h2>
            <p><strong>Bot:</strong> {report_data.get('bot_name', 'Unknown')}</p>
            <p><strong>Status:</strong> {'✅ Success' if report_data.get('success', False) else '❌ Failed'}</p>
            <p><strong>Execution Time:</strong> {report_data.get('execution_time', 0):.2f} seconds</p>
            
            <h3>📊 Results</h3>
            <ul>
        """
        
        # Add data items
        data = report_data.get('data', {})
        for key, value in data.items():
            html_content += f"<li><strong>{key.replace('_', ' ').title()}:</strong> {value}</li>"
        
        html_content += """
            </ul>
            
            <p><em>This is an automated report from the OpenAutomate platform.</em></p>
        </body>
        </html>
        """
        
        # Text fallback
        text_content = f"""
        Automation Report
        
        Bot: {report_data.get('bot_name', 'Unknown')}
        Status: {'Success' if report_data.get('success', False) else 'Failed'}
        Execution Time: {report_data.get('execution_time', 0):.2f} seconds
        
        Results:
        """
        
        for key, value in data.items():
            text_content += f"- {key.replace('_', ' ').title()}: {value}\n"
        
        text_content += "\nThis is an automated report from the OpenAutomate platform."
        
        # Send to each recipient
        sent_count = 0
        for recipient in recipients:
            try:
                send_html_email(logger, smtp_config, recipient, subject, html_content, text_content)
                sent_count += 1
            except Exception as e:
                logger.error(f"Failed to send report to {recipient}: {e}")
        
        log_task_complete(logger, "Send Report Email", f"Sent {sent_count}/{len(recipients)} reports")
        return sent_count
        
    except Exception as e:
        log_task_error(logger, "Send Report Email", str(e))
        raise


def check_inbox(logger, imap_config, folder='INBOX', limit=10):
    """
    Check email inbox for new messages.
    
    Args:
        logger: Logger instance
        imap_config: IMAP configuration dict
        folder: Email folder to check (default: INBOX)
        limit: Maximum number of emails to retrieve
        
    Returns:
        list: List of email information dictionaries
    """
    log_task_start(logger, "Check Inbox")
    
    if not HAS_EMAIL:
        error_msg = "Email libraries not available"
        log_task_error(logger, "Check Inbox", error_msg)
        raise ImportError(error_msg)
    
    try:
        logger.info(f"📬 Checking {folder} for new emails...")
        
        # Connect to IMAP server
        mail = imaplib.IMAP4_SSL(imap_config['server'], imap_config['port'])
        mail.login(imap_config['username'], imap_config['password'])
        mail.select(folder)
        
        # Search for emails
        status, messages = mail.search(None, 'ALL')
        email_ids = messages[0].split()
        
        # Get recent emails (limited)
        recent_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids
        
        emails = []
        for email_id in recent_ids:
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Extract email information
                    email_info = {
                        'id': email_id.decode(),
                        'subject': msg['subject'],
                        'from': msg['from'],
                        'date': msg['date'],
                        'body': get_email_body(msg)
                    }
                    emails.append(email_info)
        
        mail.close()
        mail.logout()
        
        logger.info(f"📧 Found {len(emails)} emails in {folder}")
        log_task_complete(logger, "Check Inbox", f"Retrieved {len(emails)} emails")
        
        return emails
        
    except Exception as e:
        log_task_error(logger, "Check Inbox", str(e))
        raise


def get_email_body(msg):
    """
    Extract the body text from an email message.
    
    Args:
        msg: Email message object
        
    Returns:
        str: Email body text
    """
    body = ""
    
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            
            if content_type == "text/plain" and "attachment" not in content_disposition:
                body = part.get_payload(decode=True).decode()
                break
    else:
        body = msg.get_payload(decode=True).decode()
    
    return body


def create_email_template(template_name, data):
    """
    Create an email from a template.
    
    Args:
        template_name: Name of the template
        data: Data to fill in the template
        
    Returns:
        tuple: (subject, html_content, text_content)
    """
    templates = {
        'welcome': {
            'subject': 'Welcome to {company_name}!',
            'html': '''
            <h2>Welcome {user_name}!</h2>
            <p>Thank you for joining {company_name}.</p>
            <p>Your account has been created successfully.</p>
            ''',
            'text': '''
            Welcome {user_name}!
            
            Thank you for joining {company_name}.
            Your account has been created successfully.
            '''
        },
        'notification': {
            'subject': 'Notification: {title}',
            'html': '''
            <h2>📢 {title}</h2>
            <p>{message}</p>
            <p><em>Sent at {timestamp}</em></p>
            ''',
            'text': '''
            {title}
            
            {message}
            
            Sent at {timestamp}
            '''
        }
    }
    
    if template_name not in templates:
        raise ValueError(f"Template '{template_name}' not found")
    
    template = templates[template_name]
    
    subject = template['subject'].format(**data)
    html_content = template['html'].format(**data)
    text_content = template['text'].format(**data)
    
    return subject, html_content, text_content 