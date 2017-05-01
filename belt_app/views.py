from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
	return render(request, 'index.html')

def createUser(request):
	if request.method != 'POST':
		return redirect('/')
	else:
		check = User.objects.validateUser(request.POST)
		if check[0] == False:
			for error in check[1]:
				messages.error(request, error)
			return redirect('/')
		else:
			hashed_pw = bcrypt.hashpw(request.POST.get('password').encode(), bcrypt.gensalt())
			user = User.objects.create(
				name = request.POST.get('name'),
				alias = request.POST.get('alias'),
				email = request.POST.get('email'),
				password = hashed_pw,
				birthday = request.POST.get('birthday')
				)
			request.session['user_id'] = user.id
			return redirect ('/quotes')

def login(request):
	if request.method != 'POST':
		return redirect('/')
	else:
		check = User.objects.loginUser(request.POST)
		if check['status'] == False:
			messages.error(request, check['message'])
			return redirect('/')
		else:
			request.session['user_id'] = check['user'].id
			return redirect('/quotes')

def currentUser(request):
	if 'user_id' in request.session:
		return User.objects.get(id=request.session['user_id'])

def logout(request):
	request.session.clear()
	return redirect('/')

def success(request):
	user = User.objects.filter(id = currentUser(request).id).first()
	favorites = user.fav_quotes.all()
	fav_ids = favorites.values_list("id", flat=True)
	other_quotes = Quote.objects.exclude(id__in = fav_ids)
	context = {
	'currentUser':currentUser(request),
	'favorites':favorites,
	'other_quotes': other_quotes
	}
	return render(request, 'success.html', context)

def createQuote(request):
		if request.method != 'POST':
			return redirect('/quotes')
		else:
			check = Quote.objects.validateQuote(request.POST)
			if check[0] == False:
				for error in check[1]:
					messages.error(request, error)
				return redirect('/quotes')
			else:
				Quote.objects.create(
					author = request.POST['author'],
					content = request.POST['content'],
					user = currentUser(request))
				return redirect('/quotes')

def favorite(request, id):
	this_quote = Quote.objects.filter(id = id).first()
	if this_quote:
		currentUser(request).fav_quotes.add(this_quote)
		return redirect('/quotes')

def remove(request, id):
	this_quote = Quote.objects.filter(id = id).first()
	if this_quote:
		currentUser(request).fav_quotes.remove(this_quote)
		return redirect('/quotes')

def showUser(request, id):
	user = User.objects.filter(id = id).first()
	quotes = Quote.objects.filter(user = user)
	count = len(quotes)
	context = {
	"user" :user,
	"quotes" :quotes,
	"count": count
	}
	return render (request, 'profile.html', context)
