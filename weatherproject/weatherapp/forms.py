from django import forms
# from .models import EmailSubscription, Location

# class EmailSubscriptionForm(ModelForm):
#    class Meta:
#       model= EmailSubscription
#       fields= '__all__'


class EmailSubscriptionForm(forms.Form):
   email = forms.EmailField()
   location = forms.CharField(max_length=200)