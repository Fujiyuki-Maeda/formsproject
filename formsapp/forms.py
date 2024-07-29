from django import forms
from .models import Item
from phonenumber_field.formfields import PhoneNumberField
from django.core.validators import RegexValidator

class CSVUploadForm(forms.Form):
    file = forms.FileField(label='CSVファイル')

class JapanesePhoneNumberField(PhoneNumberField):
    def value_to_string(self, obj):
        phone_number = self.value_from_object(obj)
        if phone_number:
            return str(phone_number).replace('+81', '0')
        return ''
    
class ItemForm(forms.ModelForm):
    phone_number = JapanesePhoneNumberField(region='JP')
    
    class Meta:
        model = Item
        fields = ('member_no', 'id_number', 'name', 'furigana', 'gender', 'birth_year', 'birth_month', 'birth_day', 
                  'phone_number', 'zip_code', 'prefecture', 'city', 'address1', 'address2')
        widgets = {
            'member_no': forms.TextInput(attrs={'placeholder':'スタッフが入力します'}),
            'id_number': forms.RadioSelect(),
            'name': forms.TextInput(attrs={'placeholder':'記入例：下野戸大輔'}),
            'furigana': forms.TextInput(attrs={'placeholder':'記入例：シモノトダイスケ'}),
            'gender': forms.RadioSelect(),
            'birth_year': forms.NumberInput(attrs={'min':1900, 'placeholder':'西暦で入力してください 記入例：1995'}),
            'birth_month': forms.NumberInput(attrs={'min':1}),
            'birth_day': forms.NumberInput(attrs={'min':1}),
            'phone_number': forms.TextInput(),
            'zip_code': forms.TextInput(attrs={'class': 'p-postal-code', 'data-address': 'true'}),
            'prefecture': forms.TextInput(attrs={'class': 'p-region', 'data-address': 'true'}),
            'city': forms.TextInput(attrs={'class': 'p-locality', 'data-address': 'true'}),
            'address1': forms.TextInput(attrs={'class': 'p-street-address', 'data-address': 'true'}),
            'address2': forms.TextInput(attrs={'placeholder':'〇丁目 アパート名など'}),
        }
        validators = {
            'name': [RegexValidator(r'^[\u3040-\u309F]*$', 'Only full-width Hiragana characters are allowed.')],
            'furigana': [RegexValidator(r'^[\u30A0-\u30FF]*$', 'Only full-width Hiragana characters are allowed.')],
            'member_no': [RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')],
            'birth_year': [RegexValidator(r'^[0-9]*$', 'Only numeric characters are allowed.')],
            'birth_month': [RegexValidator(r'^[0-9]*$', 'Only numeric characters are allowed.')],
            'birth_day': [RegexValidator(r'^[0-9]*$', 'Only numeric characters are allowed.')],
            'phone_number': [RegexValidator(r'^[0-9]*$', 'Only numeric characters are allowed.')],
            'zip_code': [RegexValidator(r'^[0-9]*$', 'Only numeric characters are allowed.')],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['zip_code'].widget.attrs.update({'onkeyup': 'AjaxZip3.zip2addr(this,"","prefecture","city","address1");'})
