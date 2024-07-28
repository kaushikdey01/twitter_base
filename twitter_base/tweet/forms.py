from django import forms
from .models import Tweet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# forms are made because the inputfields given by django are the only ones you want to use in your project



class TweetForm(forms.ModelForm):
    # meta class is mandatory, there's no other option
    class Meta:
        model = Tweet
        # fields is the array of fields  that you have used while making the models 
        fields = ['text','photo']
        

class UserRegistrationForm(UserCreationForm):
    # email = forms.EmailField()
    # class Meta:
    #     model = User
    #     fields = ('username', 'email', 'password1', 'password2') #using tuples here ause this is a built in forma that we're using for our work

    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            msg = 'A user with that email already exists.'
            self.add_error('email', msg)           
    
        return self.cleaned_data
        