# app/forms.py
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1, 
        max_value=5,
        widget=forms.HiddenInput()
    )
    
    class Meta:
        model = Review
        fields = ['kindergarten', 'parent_name', 'parent_email', 'parent_phone', 'rating', 'comment']
        widgets = {
            'kindergarten': forms.HiddenInput(),
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Расскажите о вашем опыте...'}),
            'parent_email': forms.EmailInput(attrs={'placeholder': 'email@example.com'}),
            'parent_phone': forms.TextInput(attrs={'placeholder': '+7 (999) 123-45-67'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent_name'].widget.attrs.update({'placeholder': 'Ваше имя'})