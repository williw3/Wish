from __future__ import unicode_literals

from django.db import models
import datetime
import re
import bcrypt

NAME_REGEX = re.compile(r"^[-a-zA-Z']+$")

class UserManager(models.Manager):
	def validateLogin(self, postData):
		errors = {}
		if len(postData['username']) < 3:
			errors['username'] = 'Must enter an username.'
		if len(postData['password']) < 8:
			errors['password'] = 'Password must contain at least 8 characters'
		return errors

	def validateRegister(self, postData):
		errors = {}
		if len(postData['name']) < 3:
			errors['name'] = 'Must enter a name'
		elif not NAME_REGEX.match(postData['name']):
			errors['name'] = 'name contains invalid characters'
		if len(postData['username']) < 3:
			errors['username'] = 'Must enter an username'
		if self.filter(username=postData['username']):
			errors['username'] ='username already in use'
		if len(postData['password']) < 8:
			errors['password'] = 'Password must contain at least 8 characters'
		elif not postData['password'] == postData['password_confirm']:
			errors['password'] = 'Passwords do not match'
		return errors

	def createUser(self, postData):
		password = str(postData['password'])
		hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())
		user = self.create(
			name=postData['name'], 
			username=postData['username'], 
			password=hashed_pw,
			hired=postData['hired']
			)

		return user

class User(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	hired = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()



class Item(models.Model):
	product = models.CharField(max_length=255)
	poster = models.ForeignKey(User, related_name='posted_item')
	wisher = models.ManyToManyField(User, related_name='wished_for')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

