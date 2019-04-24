from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from Ucook.models import Profile

class LoginForm(forms.Form):

    username = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'id': 'id_username'}))
    password = forms.CharField(max_length=200, widget = forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean();
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        user = authenticate(username = username, password = password)
        if not user:
            raise forms.ValidationError("Invalid username/password")
        return cleaned_data

class RegisterForm(forms.Form):
    username   = forms.CharField(max_length=20)
    password  = forms.CharField(max_length=200, label = 'Password', widget=forms.PasswordInput())
    confirm_password  = forms.CharField(max_length=200, label = 'Confirm', widget=forms.PasswordInput())
    email      = forms.CharField(max_length=50, widget=forms.EmailInput())
    # first_name = forms.CharField(max_length=20)
    # last_name  = forms.CharField(max_length=20)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password did not match.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact = username):
            raise forms.ValidationError("username is already taken.")

        return username



class EditForm(forms.Form):
    username   = forms.CharField(max_length=20)
    last_name  = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=20)
    email      = forms.CharField(max_length=50, widget=forms.EmailInput())


# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields =('text',)
#
#
# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields =('text',)


class HostPostForm(forms.Form):
    # hidden fields (for db)
    # host_postid
    # host_id
    # create_datetime
    # status (valid / invalid) / display (true or false)
    # guest_list
    content = forms.CharField()
    cuisine_type = forms.ChoiceField()
    event_date = forms.DateField()
    addr_street = forms.CharField()
    addr_apt = forms.CharField()
    addr_city = forms.CharField
    addr_state = forms.CharField()
    addr_country = forms.CharField()
    addr_zip = forms.CharField()
    max_guests = forms.IntegerField()


class GuestPostForm(forms.Form):
    # hidden fields (for db)
    # guest_postid
    # guest_id
    # create_datetime
    # status (valid / invalid) / display (true or false)
    # host_id
    content = forms.CharField()
    cuisine_type = forms.ChoiceField()
    preferred_date = forms.DateField()


class ReviewForm(forms.Form):
    # hidden fields (for db)
    # author_id / author_name
    # host_postid
    # recipient_id / recipient_name
    # create_datetime
    comment = forms.CharField()
    rating = forms.IntegerField()


MAX_UPLOAD_SIZE = 2500000
class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('profile_picture',)

    def clean_picture(self):
        picture = self.cleaned_data['profile_picture']
        if not picture:
            raise forms.ValidationError('You must upload a picture')
        if not picture.content_type or not picture.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture








