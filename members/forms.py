from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Member, Family

class SignupForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.Roles.choices)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data.get('role')
        # If requesting super admin, set inactive for approval
        if user.role == User.Roles.SUPER_ADMIN:
            user.is_active = False
        if commit:
            user.save()
        return user

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name','last_name','dob','home_origin_district','home_origin_ta','home_origin_village',
                  'residential_home','homecell','ministry','picture','marital_status','employment_status','status','family']

class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ['family_name']