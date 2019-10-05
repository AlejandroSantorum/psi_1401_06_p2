from django import forms
from django.contrib.auth.models import User
from rango.models import Page, Category, UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text='Please, enter category name')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category  # This associates the form with the model

        # This specifies which fields we want to use on the form
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
                            help_text='Please, enter page\'s title')
    url = forms.URLField(max_length=200,
                         help_text='Please, enter page\'s URL')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page

        # This specifies that we dont want to use category field,
        # its equivalent to fields = ('title', 'url', 'views')
        exclude = ('category',)

    def clean(self):
        cleaned_data = self.cleaned_data
        # Get will return None if no key is present on the dict
        # cleaned_data['url'] would raise KeyError instead
        url = cleaned_data.get('url')

        # Check if URL is well-formed and solve errors
        # Should check also https://
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

            return cleaned_data
