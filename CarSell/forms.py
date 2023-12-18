from .models import CarReview,Profilis
from django import forms
from django.contrib.auth.models import User

class CarReviewForm(forms.ModelForm):
    class Meta:
        model = CarReview

        fields = ('content', 'car', 'reviewer',)
        widgets = {'car': forms.HiddenInput(), 'reviewer': forms.HiddenInput()}


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['nuotrauka']