from django import forms
from . import models

class NewClassify(forms.ModelForm):
    class Meta:
        model = models.Classified
        fields = ['types', 'article']

    def __init__(self, *args, **kwargs):
        super(NewClassify, self).__init__(*args, **kwargs)
        self.fields['types'].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields['types'].queryset = models.FakeType.objects.all()
        self.fields['article'].widget = forms.widgets.HiddenInput()
        self.fields['article'].required = True


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = models.Feedback
        fields = ['article', 'comment']

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['article'].widget = forms.widgets.HiddenInput()
        self.fields['article'].required = True
