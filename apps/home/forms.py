from django  import forms
from django import forms
from .models import *

class LogoForm(forms.ModelForm):
    class Meta:
        model = Logo
        fields = ('image',)

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name','address','city','state','country','phone','zipcode','subject','email','message',)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('name','phone','email','description',)

class CustomDesignForm(forms.Form):
    product = forms.CharField()
    design = forms.Textarea()



