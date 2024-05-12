from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.conf import settings



def send_email(subject, html_path, to_email, context, attachment_path=None):
    template = loader.get_template(html_path)
    html_content = template.render(context)

    msg = EmailMultiAlternatives(subject=subject, body=html_content, from_email=settings.DEFAULT_FROM_EMAIL, to=[to_email])
    msg.content_subtype = 'html'
    print(f'{subject}, {html_path}, {context}')
    if attachment_path:
        try:
            with open(attachment_path, 'rb') as attachment:
                msg.attach('attachment_name.txt', attachment.read(), 'text/csv')
        except Exception as e:
            print(f"Error attaching file: {e}")

    msg.send()