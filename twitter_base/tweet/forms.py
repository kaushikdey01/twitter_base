from django import forms
from .models import Tweet
# forms are made because the inputfields given by django are the only ones you want to use in your project



class TweetForm(forms.ModelForm):
    # meta class is mandatory, there's no other option
    class Meta:
        model = Tweet
        # fields is the array of fields  that you have used while making the models 
        fields = ['text','photo']
        