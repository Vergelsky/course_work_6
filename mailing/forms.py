from django import forms

from mailing.models import Client, Mailing, Letter


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingForm(forms.ModelForm):

    class Meta:
        model = Mailing
        fields = ('name', 'letter', 'start_date', 'finish_date', 'period', 'send_time', 'status', 'clients',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        from django.forms import CheckboxInput

        for field_name, field in self.fields.items():
            if isinstance(field.widget, CheckboxInput):
                field.widget.attrs['class'] = 'form-check'
            else:
                field.widget.attrs['class'] = 'form-control'

    def clean_finish_date(self):
        if self.cleaned_data.get('finish_date'):
            start_date = self.cleaned_data.get('start_date')
            finish_date = self.cleaned_data.get('finish_date')
            if finish_date > start_date:
                return finish_date
            else:
                raise forms.ValidationError('Начало рассылки должно быть позже чем конец!')



class LetterForm(forms.ModelForm):
    class Meta:
        model = Letter
        fields = ('name', 'title', 'text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

