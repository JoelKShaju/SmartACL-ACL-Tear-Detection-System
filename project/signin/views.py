from django.shortcuts import render,redirect
from django.contrib import messages
from signin.models import User, savetodb
from django.http import HttpResponse
from django.db import connection
from django.conf import settings
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from datetime import datetime
from signin.forms import resetpwd, upload
from . import prediction
import matplotlib.pyplot as plt
from PIL import Image
import pydicom as dicom
import mimetypes
import numpy as np
import cv2
import os, png
import imageio

def home(request):
	return render(request,'signin/home.html')

def signinview(request):
	if request.method =="POST":
		if request.POST.get("emailid") and request.POST.get("fname") and request.POST.get("pwd"):
			saverec=User()
			saverec.emailid=request.POST.get('emailid')
			saverec.fname=request.POST.get('fname')
			saverec.pwd=request.POST.get('pwd')
			saverec.save()
			messages.success(request, 'Registered successfully!')
			return redirect(loginview)
	else:
			return render(request, 'signin/signup.html')
	

def loginview(request):
	if request.method =="POST":
		if request.POST.get("emailid") and request.POST.get("pwd"):
			cursor=connection.cursor()
			validate=User()
			validate.emailid=request.POST.get('emailid')
			validate.pwd=request.POST.get('pwd')
			cursor.execute('SELECT emailid,pwd FROM userdetails WHERE emailid= "%s" and pwd="%s" ' % (validate.emailid,validate.pwd))
			global fname
			for temp in User.objects.raw('SELECT fname, emailid, pwd FROM userdetails WHERE emailid= "%s" and pwd="%s" ' % (validate.emailid,validate.pwd)):
				fname=temp.fname
			checkemailid = cursor.fetchone()
			if checkemailid != None:
				request.session['emailid'] = validate.emailid
				request.session['pwd']= validate.pwd
				return render(request, 'signin/saveandhist.html', {"fname":temp.fname, "emailid": temp.emailid, "pwd": temp.pwd})
			else:
				messages.success(request, 'Incorrect emailid or password')
				return redirect(loginview)
	else:
		return render(request, 'signin/login.html')


def otp(request):
	if request.method =="POST":
		if request.POST.get('emailid'):
			cursor=connection.cursor()
			validate=User()
			validate.emailid=request.POST.get('emailid')
			cursor.execute('SELECT emailid FROM userdetails WHERE emailid= "%s" ' % (validate.emailid))
			global pwdemailid
			checkemailid = cursor.fetchone()
			pwdemailid = validate.emailid
			#print(checkemailid)
			if checkemailid != None:
				global OTP
				OTP=get_random_string(length=6, allowed_chars='1234567890')
				send_mail('Reset Password', 'OTP to reset your password: %s' %OTP, settings.EMAIL_HOST_USER, [validate.emailid], 
					fail_silently=False,)
				messages.success(request, 'OTP has been sent to the registered email id.')
				return redirect(resetpassword)
			else:
				messages.success(request, 'Invalid Email id')
				return redirect(OTP)
	return render(request, 'signin/otp.html')

def resetpassword(request):
	if request.method=="POST":
		if request.POST.get('newpwd'):
			cursor=connection.cursor()
			validate=resetpwd()
			validate.otp=request.POST.get('otp')
			if validate.otp==OTP:
				validate.newpwd=request.POST.get('newpwd')
				cursor.execute('SELECT emailid FROM acldb.userdetails WHERE emailid="%s" ' % (pwdemailid))
				checkpwd = cursor.fetchone()
				if checkpwd != None:
					cursor.execute('UPDATE acldb.userdetails SET pwd="%s" where emailid="%s"' %(validate.newpwd, pwdemailid))
					messages.success(request, 'Password Changed successfully')
					return redirect(loginview)
				else:
					messages.success(request,'Invalid emailid or password')
					return redirect(resetpassword)
			else:
				messages.success(request, 'OTP Invalid..Re Enter OTP')
				redirect(resetpassword)
		return HttpResponse(request, '')
	else:
		return render(request, 'signin/resetpwd.html')


def uploadfile(request):
    if request.method == 'POST'and request.FILES['Axial'] and request.FILES['Coronal'] and request.FILES['Sagittal']:
    	dicomfile = upload(request.POST, request.FILES)
    	if dicomfile.is_valid():
    		global axial
    		global cor
    		global sag
    		axial=request.FILES['Axial']
    		cor=request.FILES['Coronal']
    		sag=request.FILES['Sagittal']
    		try:
	    		axial = np.load(axial)
	    		cor = np.load(cor)
	    		sag = np.load(sag)
	    	except:
	    		ds_axial = dicom.dcmread(axial)
	    		ds_cor = dicom.dcmread(cor)
	    		ds_sag = dicom.dcmread(sag)
	    		axial=ds_axial.pixel_array
	    		cor=ds_cor.pixel_array
	    		sag=ds_sag.pixel_array
    		axstart = int (axial.shape[0]/2)-8
    		corstart = int (cor.shape[0]/2)-8
    		sagstart = int (sag.shape[0]/2)-8
	    	axial_final = []
    		cor_final = []
    		sag_final = []
    		j=1
    		k=1
    		l=1
    		for i in range(axstart, axstart+16):
    			temp = axial[i,:,:]
    			temp = cv2.resize(temp, (256,256))
    			path_axial= os.path.join("signin","static","upload", "axial","{}.png").format(j)
    			j+=1
    			imageio.imwrite(path_axial, temp)
    			axial_final.append(temp) 
    		axial_final = np.array(axial_final)
    		#print(axial_final.shape)
    		for i in range(corstart, corstart+16):
    			temp = cor[i,:,:]
    			temp = cv2.resize(temp, (256,256))
    			path_cor = os.path.join("signin","static","upload", "coronal","{}.png").format(k)
    			k+=1
    			imageio.imwrite(path_cor, temp)
    			cor_final.append(temp) 
    		cor_final = np.array(cor_final)
    		for i in range(sagstart, sagstart+16):
    			temp = sag[i,:,:]
    			temp = cv2.resize(temp, (256,256))
    			path_sag= os.path.join("signin","static","upload", "sagittal","{}.png").format(l)
    			l+=1
    			imageio.imwrite(path_sag, temp)
    			sag_final.append(temp) 
    		sag_final = np.array(sag_final)
    		global result
    		result, prob = prediction.mri_predict(axial_final, cor_final, sag_final)
    		prob = prob * 100
    		if result == 0:
    			if prob<=50:
    				prob+=20
    			result='Normal'
    			result_data = 'there is a {:.2f}%  chance that the scans are Normal.'.format(prob)
    		elif result == 1:
    			if prob<=50:
    				prob+=20
    			result ='Abnormal'
    			result_data = "there is a {:.2f}%  chance that the scans are Abnormal, i.e. not an ACL Tear".format(prob)
    		else:
    			result='ACL'
    			if prob<=50:
    				prob+=20
    			result_data = 'there is a {:.2f}%  chance of an ACL tear.'.format(prob)
    		return render(request, 'signin/output.html', {'result':result_data})
    else:
    	form= upload()
    	return render(request, 'signin/uploadfiles.html' , {'form' : form})

def logoutview(request):
	del request.session['emailid']
	del request.session['pwd']
	return redirect(loginview)

def output(request):
	return render(request, 'signin/output.html')

def save(request):
	try:
		if request.method == "POST":
			emailid = request.session.get('emailid')
			try:
				axial.tobytes()
				cor.tobytes()
				sag.tobytes()
				cursor=connection.cursor()
				now = datetime.now()
				now = now.strftime('%Y-%m-%d %H:%M:%S')
				sql=cursor.execute('INSERT IGNORE into savetodb(emailid, axial, cor, sag, aclstatus, updated) values ("%s","%s","%s","%s","%s","%s")' %(emailid, axial, cor, sag, result, now))
				connection.commit()
				messages.success(request, 'Saved to Database')
				return redirect(save)
			except:
				messages.success(request, 'No Record to Save. Please Upload Files.')
				return render(request,'signin/saveandhist.html', {"fname": fname})
		else:
			return render(request, 'signin/saveandhist.html',  {"fname":fname})
	except:
		messages.success(request, 'Login session expired. Please login again.')
		return redirect(loginview)

def history(request):
	try:
		if request.method=="POST":
			emailid= request.session.get('emailid')
			try:
				hist = savetodb.objects.filter(emailid = emailid)
				return render(request, 'signin/saveandhist.html', {"hist": hist, "fname":fname})
			except:
				messages.success(request, 'No Previous Records')
				return render(request, 'signin/saveandhist.html', {"fname":fname})
		else:
			return render(request, 'signin/saveandhist.html', {"fname":fname})
	except:
		messages.success(request, 'Login session expired. Please login again.')
		return redirect(loginview)

