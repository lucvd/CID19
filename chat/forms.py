from django import forms


class MessageForm(forms.Form):
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={'width': "100%", 'cols': "80", 'rows': "2", }))
