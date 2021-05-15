from django import forms


class InvestmentsForm(forms.Form):
    FREQUENCY = (
        ('1', 'Annually'),
        ('12', 'Monthly'),
        ('52', 'Weekly'),
        ('365', 'Daily')
    )

    startingAmount = forms.IntegerField(widget=forms.NumberInput(
        attrs={'placeholder': '5000', 'class': 'form-item-input'}), label='Starting amount', required=True)
    additionalContribution = forms.IntegerField(widget=forms.NumberInput(
        attrs={'placeholder': '100', 'class': 'form-item-input'}), label='Additional contribution', required=True)
    additionalContributionFrequency = forms.ChoiceField(choices=FREQUENCY, widget=forms.Select(
        attrs={'class': 'form-item-input'}), label='Additional contribution frequency', required=True)
    rateOfReturn = forms.IntegerField(widget=forms.NumberInput(
        attrs={'placeholder': '7', 'class': 'form-item-input'}), label='Rate of return (%)', required=True)
    yearsToGrow = forms.IntegerField(widget=forms.NumberInput(
        attrs={'placeholder': '10', 'class': 'form-item-input'}), label='Years to grow', required=True)
