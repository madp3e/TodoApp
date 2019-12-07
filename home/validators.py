from django.core.exceptions import ValidationError


ACCEPTED_EMAIL_DOMAIN = ["gmail.com",]
def validate_email(email):
    for domain_name in ACCEPTED_EMAIL_DOMAIN:
        if not domain_name in email:
            raise ValidationError("Email is invalid. Please enter a valid email")
    return email

