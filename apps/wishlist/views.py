# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import bcrypt, re, datetime
from django.shortcuts import redirect, render
from django.contrib import messages

from models import *

# Create your views here.
def index(request):
	return redirect('/main')
	
def gateway(request):
	return render(request, 'wishlist/gateway.html')
	
def login(request):
	print "got here!"
	try:
		user = User.objects.get(email = request.POST['email'])
		hashed_password = user.password
		entered_password = request.POST['password']
		
		if bcrypt.checkpw(entered_password.encode(), hashed_password.encode()):
			request.session['id'] = user.id
			return redirect('/dashboard')
		else:		
			messages.add_message(request, messages.INFO, 'Invalid email or password. Please try again.')
			return redirect('/main')
	except:
		messages.add_message(request, messages.INFO, 'Invalid email or password. Please try again.')
		return redirect('/main')

def logout(request):
	del request.session['id']
	request.session.modified = True
	
	return redirect('/main')
		
def register(request):
	first_name = request.POST['first_name']
	last_name = request.POST['last_name']
	email = request.POST['email']
	birthday = request.POST['birthday']
	password = request.POST['password']	
	confirm_password = request.POST['confirm_password']	
	
	errors = 0

	if not re.match(r"^[a-zA-Z]+$", first_name) or len(first_name) < 2:
		messages.add_message(request, messages.INFO, "Invalid first_name.")
		errors += 1
	
	if not re.match(r"^[a-zA-Z]+$", last_name) or len(last_name) < 2:
		messages.add_message(request, messages.INFO, "Invalid last_name.")
		errors += 1
		
	if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
		flash("Invalid email.")
		errors += 1
		
	if password == "":
		messages.add_message(request, messages.INFO, "Password is not allowed to be empty.")
		errors += 1
	
	if len(password) < 8:
		messages.add_message(request, messages.INFO, "Password is too short.")
		errors += 1
	
	if password != confirm_password:
		messages.add_message(request, messages.INFO, "Passwords do not match.")
		errors += 1
		
	if datetime.datetime.strptime(birthday, '%Y-%m-%d') > datetime.datetime.today():
		messages.add_message(request, messages.INFO, "Birthday cannot be after today.")
		errors += 1
	
	hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
	
	if errors == 0:
		messages.add_message(request, messages.INFO, "Registration Successful! Please Log In.")
		User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hashed_password, birthday=birthday)
		user = User.objects.get(email = email)
		request.session['id'] = user.id
		return redirect('/dashboard')
	else:
		return redirect('/main')
	
def dashboard(request):
	return render(request, 'wishlist/dashboard.html')
	
def authsession(request):
	if request.session.get('id', None) is None:
		redirect('/')