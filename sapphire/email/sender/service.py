from facet import ServiceMixin

from sapphire.email.settings import EmailSettings


class EmailSenderService(ServiceMixin):
    TEMPLATES = ()

    def __init__(self):
        self._templates = {template.type: template for template in self.TEMPLATES}


def get_service(settings: EmailSettings) -> EmailSenderService:
    return EmailSenderService()
