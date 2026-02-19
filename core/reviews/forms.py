from django import forms
from .models import Review
# -------------------------------------------------------------------------------------------------
class SubmitReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['product', 'rating', 'comment']
        widgets = {
            'product': forms.HiddenInput(),
            'rating': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'required': True}),
        }

    def clean(self):
        cleaned_data = super().clean()
        rating = cleaned_data.get('rating')

        if rating is not None and (rating < 1 or rating > 5):
            raise forms.ValidationError('Rating must be between 1 and 5.')

        return cleaned_data
# -------------------------------------------------------------------------------------------------
class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['product', 'rating', 'comment']
        widgets = {
            'product': forms.HiddenInput(),
            'rating': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'required': True}),
        }
# -------------------------------------------------------------------------------------------------
