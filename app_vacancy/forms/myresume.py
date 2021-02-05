from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms

from app_vacancy.models import Resume

STATUSES = (
    ('', '---------'),
    ("Don't looking for job", "Don't looking for job"),
    ('Considering job offers', 'Considering job offers'),
    ('Looking for job', 'Looking for job'),
)

GRADES = (
    ('', '---------'),
    ('Intern/Trainee', 'Intern/Trainee'),
    ('Junior', 'Junior'),
    ('Middle', 'Middle'),
    ('Senior', 'Senior'),
    ('Lead', 'Lead'),
)


class MyResumeForm(forms.ModelForm):
    status = forms.ChoiceField(choices=STATUSES)
    grade = forms.ChoiceField(choices=GRADES)

    class Meta:
        model = Resume
        exclude = ('user',)
        labels = {
            'name': 'Name',
            'surname': 'Surname',
            'status': 'Status',
            'salary': 'Salary',
            'specialty': 'Specialization',
            'grade': 'Qualification',
            'education': 'Education',
            'experience': 'Experience',
            'portfolio': 'Portfolio',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name'),
                Column('surname'),
            ),
            Row(
                Column('status'),
                Column('salary'),
            ),
            Row(
                Column('specialty'),
                Column('grade'),
            ),
            Row(
                Column('education'),
            ),
            Row(
                Column('experience'),
            ),
            Row(
                Column('portfolio'),
            ),
            Row(
                Column(Submit('submit', 'Submit')),
            ),
        )
