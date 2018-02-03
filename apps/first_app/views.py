from django.shortcuts import render, redirect
from models import *
from django.contrib import messages


def flashErrors(request, errors):  
	for error in errors:
		messages.error(request, errors[error])

def index(request):
	return render(request, 'first_app/index.html')

def landing(request):
	id = request.session['user_id']
	context = {
		'items': Item.objects.exclude(wisher=User.objects.get(id=id)),
		'current_user': User.objects.get(id=id),
		'wishes': Item.objects.filter(wisher=User.objects.get(id=id))
	}
	return render(request, 'first_app/landing.html', context)


def show(request, id):
	context = {
		'item': Item.objects.get(id=id),
		'wishers': User.objects.filter(wished_for__id=id)

	}
	return render(request, 'first_app/show.html', context)


def add(request, id):

	want = Item.objects.get(id=id)
	user_id = request.session['user_id']
	want.wisher.add(User.objects.get(id=user_id))
	want.save()
	print want.wisher

	return redirect('/landing')

def create(request):
	current_user = User.objects.get(id=request.POST['poster'])

	Item.objects.create(product=request.POST['product'], poster=current_user)

	return redirect('/landing')

def new(request):
	id = request.session['user_id']
	context = {
		'current_user': User.objects.get(id=id)
	}

	return render(request, 'first_app/new.html', context)

def delete(request, id):
	Item.objects.get(id=id).delete()
	return redirect('/landing')



def register(request):
	if request.method == 'POST':
		errors = User.objects.validateRegister(request.POST)
		if not errors:
			user = User.objects.createUser(request.POST)
			request.session['user_id'] = user.id
			return redirect('/landing')

		flashErrors(request, errors)
	return redirect('/')

def login(request):
	if request.method == 'POST':
		errors = User.objects.validateLogin(request.POST)

		if not errors:
			user = User.objects.filter(username=request.POST['username']).first()

			if user:
				password = str(request.POST['password'])
				user_password = str(user.password)

				hashed_pw = bcrypt.hashpw(password, user_password)

				if hashed_pw == user.password:
					request.session['user_id'] = user.id  #if passwords match, make new session with users' id
					return redirect('/landing') 

				errors['password'] = 'Invalid account information' #passowrds don't match

		flashErrors(request, errors)
		return redirect('/')

def logout(request):
	if 'user_id' in request.session:
		request.session.pop('user_id')

	return redirect('/')




