from django import forms
from ckeditor.fields import RichTextField
from .models import Blog, Contact, BlogReport

#FOR REPORT POST 



class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            "name",
            "phone",
            "email",
            "message"
        ]


class TextForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, required=True)

class AddBlogForm(forms.ModelForm):
    description = RichTextField()
    tags = forms.CharField(max_length=255)  # Adjust the max_length as needed

    class Meta:
        model = Blog
        fields = ['title', 'description', 'category', 'tags', 'banner']


#for report blog 
class ReportForm(forms.ModelForm):
    class Meta:
        model = BlogReport
        fields = ['reason', 'status']
        widgets = {
            'status': forms.HiddenInput(), 
        }
  

class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))