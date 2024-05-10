from rest_framework.exceptions import ValidationError


class URLCheckValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = value.get(self.field)
        if url and 'www.youtube.com/' not in url:
            raise ValidationError('Можно вставлять только ссылки Youtube')
