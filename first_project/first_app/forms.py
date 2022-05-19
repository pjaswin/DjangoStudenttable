from django import forms

from first_app.models import Degree


class DegreeForm(forms.Form) :
    title = forms.CharField(label='Title', max_length=20)
    branch = forms.CharField(label='Branch', max_length=50)
    file = forms.FileField(label='Select a JSON file', help_text='(max. 2 mb)',required=False)

class StudentForm(forms.Form):
    degree= forms.ModelChoiceField(label='Degree',queryset=Degree.objects.all())
    roll_number=forms.CharField(label='Roll Number')
    name=forms.CharField(label="Name",max_length=30)
    year=forms.IntegerField(label="Year")
    dob=forms.DateField(label="Date of Birth")
    file = forms.FileField(label='Select a JSON file', help_text='(max. 2 mb)')

class Searchform(forms.Form):
    keywords=forms.CharField(label="Name",required=False)
    date1=forms.DateField(label="From",required=False)
    date2=forms.DateField(label="To",required=False)
    sort = forms.BooleanField(label="Sort",required=False)
    