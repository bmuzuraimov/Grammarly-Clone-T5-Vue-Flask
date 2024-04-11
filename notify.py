import resend
import os
import dotenv

dotenv.load_dotenv()

resend.api_key = os.getenv('RESEND_API_KEY')
from_email = os.getenv('FROM_EMAIL')
to_email = os.getenv('TO_EMAIL')

params = {
    'from': from_email,
    'to': [to_email],
    'subject': 'Training Progress',
    'html': '<h1>Training Completed</h1><p>Training has been completed successfully.</p>'
}
email = resend.Emails.send(params)