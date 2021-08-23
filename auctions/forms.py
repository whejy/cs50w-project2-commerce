from django import forms
from .settings import STEP


class NewListForm(forms.Form):
    title = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
        'placeholder': 'Title', 'class': 'title'
        }), label=''
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
        'placeholder': 'Item description...'
        }),
        label=''
    )
    start_bid = forms.DecimalField(
        required=True,
        decimal_places=2,
        min_value=0.00,
        widget=forms.NumberInput(attrs={
        'value': '0.00', 'step': STEP
        }),
        label='Starting Bid $'
    )
    image = forms.URLField(
        required=False,
        label='Image URL'
    )
    category = forms.CharField(
        required=False
    )


class NewBidForm(forms.Form):
    bid = forms.DecimalField(
        required=False,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
        'step': STEP
        }),
        label='$'
    )        


class NewCommentForm(forms.Form):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
        'placeholder': 'Make a comment...'
        }),
        label=''
    )