from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Message,Payment, contact, post_job, apply_job, report_job, Category,skilled_companies, skilled_individuals,skilled_individuals, Comments



class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True  
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=True 
    )

    
from django import forms
from django.contrib.auth.forms import PasswordResetForm

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    location_choices = [
    ('ashanti', 'Ashanti Region'),
    ('brong', 'Brong Region'),
    ('central', 'Central Region '),
    ('eastern', 'Eastern Region '),
    ('greater_accra', 'Greater Accra Region'),
    ('northern', 'Northern Region '),
    ('savannah', 'Savannah Region '),
    ('north_east', 'North-East Region '),
    ('upper_east', 'Upper East Region '),
    ('bono_east', 'Bono East Region '),
    ('ahafo', 'Ahafo Region '),
    ('oti', 'Oti Region '),
    ('volta', 'Volta Region'),
    ('western', 'Western Region'),
    ('western_north', 'Western North Region'),
    ('upper_west', 'Upper West Region '),
]
    location = forms.ChoiceField(choices=location_choices, widget=forms.Select(attrs={'class': 'form-control select2'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the default help text and validation message for the username field
        self.fields['username'].help_text = None




class PostJobForm(forms.ModelForm):
    class Meta:
        model = post_job
        
        fields = ['job_title','sex','region', 'job_description', 'responsibilities', 'location', 'company_address', 'company_number', 'company_email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class contactus(forms.ModelForm):
    class Meta:
        model = contact
        fields = '__all__'



class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        widgets={
            'message': forms.TextInput(attrs={'class': 'form-control'})
        }


class categoryform(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
        widgets ={
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add a category name'}),
        }



class post_job_form(forms.ModelForm):
    class Meta:
        model = post_job
        fields = ('company_name','sex', 'region','company_address','company_email' ,'company_number', 'job_title','job_description','responsibilities','qualifications','time', 'location','deadline','category','job_for','company_image')
        widgets={
            'region': forms.Select(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
             'company_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'company_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'company_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
             'job_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
             'responsibilities': forms.Textarea(attrs={'class': 'form-control'}),
            'qualifications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
           'time': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
           'deadline': forms.DateInput(attrs={'class': 'form-control','type': 'datetime-local'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'job_for': forms.Select(attrs={'class': 'form-control'}),
            'company_image': forms.FileInput(attrs={'class': 'form-control'}),
        }





class report_job_form(forms.ModelForm):
    class Meta:
        model = report_job
        exclude = ['user', 'posts']
        widgets = {
            'email_address': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact': forms.NumberInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def save(self, user, post, commit=True):
        report = super().save(commit=False)
        report.user = user
        report.posts = post
        if commit:
            report.save()
        return report

class apply_job_form(forms.ModelForm):
    class Meta:
        model = apply_job
        exclude = ['user', 'job', 'created_at']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'cv': forms.FileInput(attrs={'class': 'form-control-file'}),
            'information': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def save(self, user, job, commit=True):
        application = super().save(commit=False)
        application.user = user
        application.job = job
        if commit:
            application.save()
        return application

from .models import CompanyRating

class CompanyRatingForm(forms.ModelForm):
    class Meta:
        model = CompanyRating
        fields = ['rating']


from .models import CompanyProfile
class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['name', 'address', 'email', 'number', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['number'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})


from django import forms
from .models import skilled_companies

class skilled_company_form(forms.ModelForm):
    class Meta:
        model = skilled_companies
        exclude =['approved']
        widgets = {
'name': forms.TextInput(attrs={'class': 'form-control'}),
'region': forms.Select(attrs={'class': 'form-control'}),
'location': forms.TextInput(attrs={'class': 'form-control'}),
'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'email': forms.EmailInput(attrs={'class': 'form-control'}),
'services': forms.TextInput(attrs={'class': 'form-control'}),
'description': forms.Textarea(attrs={'class': 'form-control' , 'rows': 5}),
'availability': forms.Select(attrs={'class': 'form-control'}),
}


from django import forms
from .models import skilled_individuals

class skilled_individual_form(forms.ModelForm):
    class Meta:
        model = skilled_individuals
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'services': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'availability': forms.Select(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),  # Add sex field as a dropdown
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('email', 'amount')
        widgets = {
            'email': forms.EmailInput(attrs={'readonly': True, 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'readonly': True, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].initial = 20




from django import forms
from .models import skilled_companies, Comment,skilled_ind_Comment



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # Use the Comments model instead of Comment
        fields = ('name', 'email', 'body')
        widgets = {
'name': forms.TextInput(attrs={'class': 'form-control'}),
'email': forms.EmailInput(attrs={'class': 'form-control'}),
'body': forms.Textarea(attrs={'class': 'form-control' , 'rows': 5}),
}

class skilled_ind_Comment_form(forms.ModelForm):
    class Meta:
        model = skilled_ind_Comment  # Use the Comments model instead of Comment
        fields = ('name', 'email', 'body')
        widgets = {
'name': forms.TextInput(attrs={'class': 'form-control'}),
'email': forms.EmailInput(attrs={'class': 'form-control'}),
'body': forms.Textarea(attrs={'class': 'form-control' , 'rows': 5}),
}


class skilled_individual_form(forms.ModelForm):
    class Meta:
        model = skilled_individuals
        fields = ('name', 'location','region', 'phone_number', 'email', 'services', 'description', 'availability')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'services': forms.Textarea(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'availability': forms.Select(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
        }


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('name', 'email', 'body')
        widgets = {
'name': forms.TextInput(attrs={'class': 'form-control'}),
'email': forms.EmailInput(attrs={'class': 'form-control'}),
'body': forms.Textarea(attrs={'class': 'form-control' , 'rows': 5}),
}


from . models import MultipleImages
class MultipleImageForms(forms.ModelForm):
    class Meta:
        model = MultipleImages
        fields = ('images',)

from .models import MultipleImages  # Import the necessary model

class MultipleImagesForm(forms.ModelForm):
    class Meta:
        model = MultipleImages
        fields = ('images',)
    


