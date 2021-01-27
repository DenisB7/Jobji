from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms

from app_vacancy.models import Resume

STATUSES = (
    ('', '---------'),
    ('Не ищу работу', 'Не ищу работу'),
    ('Рассматриваю предложения', 'Рассматриваю предложения'),
    ('Ищу работу', 'Ищу работу'),
)

GRADES = (
    ('', '---------'),
    ('Стажер', 'Стажер'),
    ('Джуниор', 'Джуниор'),
    ('Миддл', 'Миддл'),
    ('Синьор', 'Синьор'),
    ('Лид', 'Лид'),
)


class MyResumeForm(forms.ModelForm):
    status = forms.ChoiceField(choices=STATUSES)
    grade = forms.ChoiceField(choices=GRADES)

    class Meta:
        model = Resume
        exclude = ('user',)
        labels = {
            'name': 'Имя',
            'surname': 'Фамилия',
            'status': 'Готовность к работе',
            'salary': 'Вознаграждение',
            'specialty': 'Специализация',
            'grade': 'Квалификация',
            'education': 'Образование',
            'experience': 'Опыт работы',
            'portfolio': 'Портфолио',
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
                Column(Submit('submit', 'Сохранить')),
            ),
        )
