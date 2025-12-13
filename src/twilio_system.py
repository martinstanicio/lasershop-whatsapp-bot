import twilio.rest


class TwilioClient:
    def __init__(self, account_sid: str, auth_token: str, templates: dict[str, str]):
        self.client = twilio.rest.Client(account_sid, auth_token)
        self.templates = templates
