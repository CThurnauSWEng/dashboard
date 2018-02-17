from __future__ import unicode_literals
from django.db import models

import re
import bcrypt

NAME_REGEX = re.compile(r'^[A-Za-z ]*$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

# model manager and validators 
class UserManager(models.Manager):
    def validate_registration_data(self, post_data):
        response = {
            'status' : True
        }
        errors = []

        if len(post_data['first_name']) < 3:
            errors.append("First name must be at least 3 characters long")

        if not re.match(NAME_REGEX, post_data['first_name']):
            errors.append('Name may only contain characters')

        if len(post_data['last_name']) < 3:
            errors.append("Last name must be at least 3 characters long")

        full_name = post_data['first_name'] + ' ' + post_data['last_name']

        if not re.match(NAME_REGEX, post_data['last_name']):
            errors.append('Name may only contain characters')

        # check emailness of email
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors.append("Invalid email")

        # does this email already exist?
        users = User.objects.filter(email = post_data['email'])
        if len(users) > 0:
            errors.append('This email is already in use')

        if len(post_data['password']) < 8:
            errors.append("Password must be at least 8 characters long")

        if post_data['password'] != post_data['pwd_confirm']:
            errors.append("Passwords do not match!")

        all_users = User.objects.all()
        if len(all_users) > 0:
            # not the first user
            user_level = 1
        else:
            user_level = 9

        if len(errors) > 0:
            response['status'] = False
            response['errors'] = errors
        else:
            hashedpwd = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

            user = User.objects.create(
                        email      = post_data['email'],
                        first_name = post_data['first_name'],
                        last_name  = post_data['last_name'],
                        full_name  = full_name,
                        password   = hashedpwd,
                        description= ' ',
                        user_level = user_level)

            response['user'] = user
            
        return response

    def validate_login_data(self, post_data):
        response = {
            'status' : True
        }
        errors = []
        hashedpwd = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

        user = User.objects.filter(email = post_data['email'])

        if len(user) > 0:
            # check this user's password
            user = user[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('username/password incorrect')
        else:
            errors.append('username/password incorrect')

        if len(errors) > 0:
            response['status'] = False
            response['errors'] = errors
        else:
            response['user'] = user
        return response

    def validate_edit_data(self, post_data):
        response = {
            'status' : True
        }
        errors = []

        this_user = User.objects.get(id=post_data['user_id'])

        if len(post_data['first_name']) < 3:
            errors.append("First name must be at least 3 characters long")

        if not re.match(NAME_REGEX, post_data['first_name']):
            errors.append('Name may only contain characters')

        this_user.first_name = post_data['first_name']

        if len(post_data['last_name']) < 3:
            errors.append("Last name must be at least 3 characters long")

        if not re.match(NAME_REGEX, post_data['last_name']):
            errors.append('Name may only contain characters')

        this_user.last_name = post_data['last_name']
        this_user.full_name = post_data['first_name'] + ' ' + post_data['last_name']

        # check emailness of email
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors.append("Invalid email")

        this_user.email = post_data['email']

        if (post_data['user_level'] != '1') & (post_data['user_level'] != '9'):
            print "post_data user_level", post_data['user_level']
            errors.append("Valid user levels: 1 for normal, 9 for admin")

        this_user.user_level = post_data['user_level']        

        if len(errors) > 0:
            response['status'] = False
            response['errors'] = errors
        else:
            this_user.save()

            response['user'] = this_user
            
        return response

    def validate_pwd_change(self, post_data):
        response = {
            'status' : True
        }
        errors = []

        if len(post_data['password']) < 8:
            errors.append("Password must be at least 8 characters long")

        if post_data['password'] != post_data['pwd_confirm']:
            errors.append("Passwords do not match!")

        # password is valid and matches pwd_confirm
        hashedpwd = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))
        
        this_user = User.objects.get(id=post_data['user_id'])
        this_user.password = hashedpwd

        if len(errors) > 0:
            response['status'] = False
            response['errors'] = errors
        else:
            this_user.save()
            response['user'] = this_user
            
        return response

    def validate_desc_change(self, post_data):
        response = {
            'status' : True
        }
        errors = []
        
        this_user = User.objects.get(id=post_data['user_id'])
        this_user.description = post_data['description']

        if len(errors) > 0:
            response['status'] = False
            response['errors'] = errors
        else:
            this_user.save()
            response['user'] = this_user
            
        return response


class MessageManager(models.Manager):
    def validate_message_data(self, post_data):
        response = {
            'status' : True
        }
        errors = []

        if len(post_data['content']) < 1:
            errors.append("Message must contain at least one character")

        to_user   = User.objects.get(id=post_data['msg_for'])
        from_user = User.objects.get(id=post_data['msg_from']) 

        if len(errors) > 0:
            response['status'] = False
            response['errors'] = errors
        else:
            message = Message.objects.create(
                content     = post_data['content'],
                to_user     = to_user,
                from_user   = from_user
            )

            response['message'] = message
            
        return response
        

class CommentManager(models.Manager):
    def validate_comment_data(self, post_data):
        response = {
            'status' : True
        }
        errors = []

        if len(post_data['content']) < 1:
            errors.append("Message must contain at least one character")

        to_msg   = Message.objects.get(id=post_data['to_msg'])
        from_user = User.objects.get(id=post_data['from_user']) 

        print "to_msg.content", to_msg.content
        print "from_user: ", from_user.full_name

        if len(errors) > 0:
            response['status'] = False
            response['errors'] = errors
        else:
            comment = Comment.objects.create(
                content     = post_data['content'],
                to_msg      = to_msg,
                from_user   = from_user
            )
            response['comment'] = comment
            
        return response


# Create your models here.
class User(models.Model):
    email       = models.CharField(max_length=255)
    first_name  = models.CharField(max_length=255)
    last_name   = models.CharField(max_length=255)
    full_name   = models.CharField(max_length=255)
    password    = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    user_level  = models.CharField(max_length=255)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now_add=True)
    objects     = UserManager()

class Message(models.Model):
    content     = models.TextField()
    to_user     = models.ForeignKey(User,related_name="messages_to")
    from_user   = models.ForeignKey(User,related_name="messages_from")
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now_add=True)
    objects     = MessageManager()

class Comment(models.Model):
    content     = models.TextField()
    to_msg      = models.ForeignKey(Message,related_name="comments")
    from_user   = models.ForeignKey(User,related_name="comments_from")
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now_add=True)
    objects     = CommentManager()


   