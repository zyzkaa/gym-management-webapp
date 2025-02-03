from django.forms.fields import Field

def delete_null_choice(choices: list[tuple[str, str]]) -> list[tuple[str, str]]:
    return [choice for choice in choices if choice[0]]
