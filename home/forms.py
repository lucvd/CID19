import requests
from django import forms
from django.forms import formset_factory
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from django.forms import ModelForm
from PIL import Image

from ConnectID.choices import *

from home.models import Profile, Project


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ['headline', 'whyImHere', 'bio', 'typeOfUser', 'website', 'extraInfo']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['headline'].widget.attrs.update({'class': 'form-control'})
        self.fields['headline'].widget.attrs.update({'placeholder': 'You could write about your current job, special skills, achievements, ...'})
        self.fields['headline'].widget.attrs.update({'rows': '2'})
        self.fields['headline'].widget.attrs.update({'required': 'true'})
        self.fields['headline'].label = "Headline"
        self.fields['headline'].help_text = "The headline describes you in one or two short sentences. It could be your current job title, skills, ..."

        self.fields['whyImHere'].widget.attrs.update({'class': 'form-control'})
        self.fields['whyImHere'].widget.attrs.update({'placeholder': 'Help people understand what you are looking for and why you are using Connect-ID'})
        self.fields['whyImHere'].widget.attrs.update({'rows': '4'})
        self.fields['whyImHere'].label = "Why am I on this website?"
        self.fields['whyImHere'].help_text = "Explain why you are using this website and what you are looking for"

        self.fields['bio'].widget.attrs.update({'class': 'form-control'})
        self.fields['bio'].widget.attrs.update({'placeholder': 'Describe your history, education, professional history, past jobs, past projects, ...'})
        self.fields['bio'].widget.attrs.update({'rows': '8'})
        self.fields['bio'].label = "Bio"
        self.fields['bio'].help_text = "Longer description of yourself"

        self.fields['typeOfUser'].widget.attrs.update({'class': 'form-control'})
        self.fields['typeOfUser'].widget.attrs.update(
            {'placeholder': 'Choose the option that corresponds the most with you'})
        self.fields['typeOfUser'].widget.attrs.update({'rows': '8'})
        self.fields['typeOfUser'].label = "Type of user"

        self.fields['website'].widget.attrs.update({'class': 'form-control'})
        self.fields['website'].widget.attrs.update(
            {'placeholder': 'Insert your own personal website if you have one'})
        self.fields['website'].label = "Your personal website"

        self.fields['extraInfo'].widget.attrs.update({'class': 'form-control'})
        self.fields['extraInfo'].widget.attrs.update(
            {'placeholder': 'Explain other info about yourself'})
        self.fields['extraInfo'].widget.attrs.update({'rows': '6'})
        self.fields['extraInfo'].label = "Some other reason or extra info you would like to share"


class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = ['title', 'abstract', 'description', 'lookingFor', 'keywords', 'generalProjectType', 'projectType', 'projectStatus',
                  'projectWebsite', 'location', 'wiift', 'anonymity', 'visible']

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'A short but comprehensive project name'})
        self.fields['abstract'].widget.attrs.update({'placeholder': 'A short introduction to your project',
                                                     'rows': '2'})
        self.fields['description'].widget.attrs.update({'placeholder': 'A detailed description of the project',
                                                        'rows': '6'})

        self.fields['lookingFor'].label = 'What is your project looking for?'
        self.fields['lookingFor'].widget.attrs.update({'placeholder': 'Do you need someone with technical skills, or sales? Or do you just want to share your idea?',
                                                       'rows': '2'})

        self.fields['keywords'].widget.attrs.update({'placeholder': 'First one',
                                                     'name': forms.TextInput(attrs={
                                                        'class': 'form-control',
                                                        'placeholder': 'Enter keyword here'})
                                                    })
        self.fields['keywords'].label = 'Keyword'

        self.fields['generalProjectType'].label = 'Select a general type of project'

        self.fields['projectType'].label = 'Select more detailed your type of project'
        # TODO make the choices of projecttype change dynamically based on the chosen generalProjectType!
        # self.fields['projectType'] = forms.MultipleChoiceField(choices=[PROJECT_TYPES])

        self.fields['projectStatus'].widget.attrs.update({'placeholder': 'Status'})
        self.fields['projectStatus'].label = 'Select the status that your project is currently in'

        self.fields['projectWebsite'].widget.attrs.update({'placeholder': 'Fill in a website that tells more about your project',
                                                           'rows': '1'})
        self.fields['projectWebsite'].label = 'The website of your project'

        self.fields['location'].widget.attrs.update({'placeholder': 'Select your city'})
        self.fields['location'].label = 'Location'

        self.fields['wiift'].widget.attrs.update({'placeholder': 'Explain what other people can gain from your project',
                                                  'rows': '4'})
        self.fields['wiift'].label = 'What\'s in it for them'

        self.fields['anonymity'].label = 'Anonymous'
        self.fields['anonymity'].help_text = 'If your project is anonymous, no other user will see who submitted it.'

        self.fields['visible'].label = 'Publish'
        self.fields['visible'].help_text = 'Only when the project is published it will be visible to other users'


class LinkedInSignupForm(forms.Form):
    bio = forms.CharField(min_length=100, max_length=1000, label="Bio",
                          widget=forms.Textarea(attrs={
                              'placeholder': 'Introduce yourself'
                          }))

    def __init__(self, *args, **kwargs):
        super(LinkedInSignupForm, self).__init__(*args, **kwargs)
        self.fields['bio'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})

    def signup(self, request, user):
        user.profile.bio = self.cleaned_data['bio']
        user.username = user.email
        user.save()

        linkedinProfileFields = user.socialaccount_set.first().extra_data
        try:
            user.profile.linkedin = linkedinProfileFields['publicProfileUrl']
        except KeyError:
            print()
            # TODO log this?
        try:
            user.profile.linkedInProfilePictureURL = linkedinProfileFields['pictureUrls']['values'][0]
        except KeyError:
            print()
            # TODO log this?

        user.save()


class ProfilePictureForm(ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Profile
        fields = ('profilePicture',)

    def save(self, **kwargs):
        profile = super(ProfilePictureForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        # if the user chose the default picture, the profilePicture will be empty and must be set to the the default picture
        if not self.changed_data.__contains__('profilePicture'):
            from ConnectID.settings import BASE_DIR
            import os
            from django.core.files import File
            with open(os.path.join(BASE_DIR, 'home/static/home/img/default_profile_picture.jpg'),'rb') as f:
                defaultimage = File(f)
                profile.profilePicture.save("default.jpg", defaultimage, save=True)

        image = Image.open(profile.profilePicture)
        cropped_image = image.crop((x, y, w + x, h + y))
        resized_image = cropped_image.resize((300, 300), Image.ANTIALIAS)
        resized_image.save(profile.profilePicture.path)

        return profile
