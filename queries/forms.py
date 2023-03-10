from django import forms
from django.forms import Form


class UploadFileForm(forms.Form):
    table_name = forms.CharField(max_length=50, help_text='Only letters, numbers and underscore.')
    file = forms.FileField(help_text='CSV file containing data for your table. CSV must contain header row.')
    # database =


class QueryAiCreateForm(Form):
    tables = forms.CharField(
        max_length=128,
        help_text='A comma- or space-delimited list of tables that hold the required data'
    )
    description = forms.CharField(
        max_length=128,
        help_text='Answers the question, what should the query find?  E.g. "Revenue by country for the past 30 days"'
    )