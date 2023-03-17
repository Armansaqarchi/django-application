from django.forms import ModelForm
from django import forms
from .models import Project, Review

#so we can create a model form based on model simply by extending the ModelForm class
class ProjectForm(ModelForm):
    class Meta:
        #2 things needed: model name and attributes needed to make a form from
        model = Project
        fields = ['title', 'description', 'demo_link', 'featured_image', 'vote_total', 'vote_ratio', 'tags']
        # to use different shapes of form( like using checkboxes )
        #  we can use widgets attribute which is in django forms

        widgets = {'tags' : forms.CheckboxSelectMultiple() ,
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        

        #to make some changes about fields
        for name, field in self.fields.items():
            field.widget.attrs.update({'class' : 'input'})
        

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            "value" : "select your vote here:",
            "body" : "Add your comment:"
        }
    
    def __init__(self, *args, **kwargs) -> None:
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class" : "input"})