from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
	def validateUser(self, post):
		is_valid = True
		errors = []
		if len(post.get('name')) == 0:
			is_valid = False
			errors.append('Name field cannot be blank.')
		if len(post.get('alias')) == 0:
			is_valid = False
			errors.append('Alias field cannot be blank.')
		if  not re.search(r'\w+\@\w+.\w+', post.get('email')):
			is_valid = False
			errors.append('Email not valid')
		if len(post.get('password')) < 4:
			is_valid =False
			errors.append('Password field must be a minimum of 4 characters')
		if post.get('password') != post.get('pw_confirm'):
			is_valid = False
			errors.append('Passwords do not match')
		if post.get('birthday') == '':
			is_valid = False
			errors.append('Date of birth field cannot be empty')
		if len(post.get('birthday')) != 10:
			errors.append('Date of birth invalid')
		return (is_valid, errors)

	def loginUser(self, post):
		user = User.objects.filter(email = post.get('email')).first()
		if user and bcrypt.checkpw(post.get('password').encode(), user.password.encode()):
			return {'status': True, 'user':user}
		else:
			return{'status': False, 'message': 'invalid credentials'}

class User(models.Model):
	name = models.CharField(max_length = 255)
	alias= models.CharField(max_length = 255)
	email = models.CharField(max_length = 255)
	password = models.CharField(max_length = 255)
	birthday = models.DateField('birthday')
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

class QuoteManager(models.Manager):
	def validateQuote(self, post):
		is_valid = True
		errors =[]
		if len(post.get('author')) < 3:
			is_valid = False
			errors.append('Quoted by field must be a minimum of 3 characters.')
		if len(post.get('content')) < 10:
			is_valid = False
			errors.append('Quote must be a minimum of 10 characters.')
		return (is_valid, errors)

class Quote(models.Model):
	author = models.CharField(max_length = 255)
	content = models.TextField()
	favorite = models.ManyToManyField(User, related_name = "fav_quotes")
	user = models.ForeignKey(User, related_name = "quotes")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = QuoteManager()