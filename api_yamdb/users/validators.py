from django.core.validators import RegexValidator

# Валидация для username, допускающая только указанные символы.
username_validator = RegexValidator(
    regex=r'^[\w.@+-]+\Z',
    message='Допускаются только латинские буквы, цифры и символы @/./+/-/_'
)
