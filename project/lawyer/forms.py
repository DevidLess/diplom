from django import forms
from .models import Review


# class ReviewForm(forms.ModelForm):
#     class Meta:
#         model = Review
#         fields = ['score', 'text']
#         widgets = {
#             'score': forms.NumberInput(attrs={
#                 'min': 1,
#                 'max': 5,
#                 'class': 'form-control',
#                 'placeholder': 'Оценка от 1 до 5',
#             }),
#             'text': forms.Textarea(attrs={
#                 'rows': 4,
#                 'class': 'form-control',
#                 'placeholder': 'Напишите ваш отзыв...',
#             }),
#         }


class ReviewForm(forms.ModelForm):
    score = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 6)],  # Оценки от 1 до 5
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Оценка"
    )

    class Meta:
        model = Review
        fields = ['score', 'text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Напишите ваш отзыв...',
            }),
        }
