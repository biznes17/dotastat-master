from django import forms
from .models import Match


class MatchForm(forms.ModelForm):
	class Meta:
		model = Match
		fields = ['match_id']

	widgets = {
			'match_id': forms.TextInput(attrs={'class':'form-control'})
		}	