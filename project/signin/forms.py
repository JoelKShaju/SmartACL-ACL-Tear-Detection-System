from django import forms

class resetpwd(forms.Form):
	emailid= forms.CharField(max_length=100)
	#pwd = forms.CharField(max_length=100)
	newpwd= forms.CharField(max_length=100)
	otp=forms.CharField(max_length=6)

class upload(forms.Form):
	Axial = forms.FileField()
	Coronal = forms.FileField()
	Sagittal = forms.FileField()

