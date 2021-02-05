from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row
from django import forms

from app_vacancy.models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        exclude = ('vacancy', 'user')
        labels = {
            'written_username': 'Your first name and last name',
            'written_phone': 'Your phone number',
            'written_cover_letter': 'Text',
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.layout = Layout(
                Row(
                    Column('written_username'),
                ),
                Row(
                    Column('written_phone'),
                ),
                Row(
                    Column('written_cover_letter'),
                ),
            )
