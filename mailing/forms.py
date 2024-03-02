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
        fields = ('name', 'letter', 'period', 'send_time', 'is_active', 'clients',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            from django.forms import CheckboxInput
            if isinstance(field.widget, CheckboxInput):

                field.widget.attrs['class'] = 'form-check'

            else:
                field.widget.attrs['class'] = 'form-control'


class LetterForm(forms.ModelForm):
    class Meta:
        model = Letter
        fields = ('name', 'title', 'text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

