from django.db import models
import re,bcrypt
# Create your models here.
# User model - favorited(many to many), created(one to many) 
# preset model - favorited by(many to many), uploaded by(one to many)

class UserManager(models.Manager):
    def register_validator(self, post_data):
        errors = {}
        if len(post_data['username_form']) < 5: # username_form comes from html
            errors['username'] = 'Username must be 5 characters or more'#user_name comes from user dictionary

        for user in User.objects.all():
            if user.username == post_data['username_form']:
                errors['username'] = "Username already taken!"
        
        if len(post_data['email_form']) < 8: 
            errors['email'] = 'Email must be 8 characters or more'  

        if len(post_data['password_form']) < 8: 
            errors['password'] = 'Password must be 8 characters or more' 
            # this checks the passwords to make sure both are maching!!
        if(post_data['password_form'] != post_data['conPassword_form']):
            errors['conPassword'] = " Password doesn\'t match."
#this is to make sure the email is in a particular format  info@yahoo.com
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email_form']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email/password!"
            # this is to make sure there is no duplicate user 
        for user in User.objects.all():
            if user.email == post_data['email_form']:
                errors['email'] = "Invalid email address!"
        return errors # have to make sure u are returning errors!!!
    
    def login_validator(self, post_data):
        errors = {}
        user_list = User.objects.filter(email=post_data['log_email_form'])   # check the email is in the database
        if len(user_list) > 0 and bcrypt.checkpw(post_data['log_password_form'].encode(), user_list[0].password.encode()):
            print("password match")
        else:
            errors['login'] = "invalid email or password"
            print("failed login")
        return errors

    def patch_validator(self, post_data):
        errors = {}
        if len(post_data['patch_name_form']) < 3:
            errors['patch_name'] = 'Patch name must be 3 characters or more'
        return errors

class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =  models.DateTimeField(auto_now=True)
    objects = UserManager() #MAKE SURE ITS HERE

class Patch(models.Model):
    patch_name = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, related_name="patches", on_delete=models.CASCADE)
    saved_by = models.ManyToManyField(User, related_name="saved_patches")
    # osc 1
    oscillator1 = models.CharField(max_length=25)
    octave1 = models.DecimalField(max_digits=3, decimal_places=2)
    attackGain1 = models.DecimalField(max_digits=3, decimal_places=2)
    attackDur1 = models.DecimalField(max_digits=6, decimal_places=2)
    decayDur1 = models.DecimalField(max_digits=6, decimal_places=2)
    sustainGain1 = models.DecimalField(max_digits=3, decimal_places=2)
    sustainDur1 = models.DecimalField(max_digits=6, decimal_places=2)
    release1 = models.DecimalField(max_digits=3, decimal_places=2)
    # osc 2
    oscillator2 = models.CharField(max_length=25)
    octave2 = models.DecimalField(max_digits=3, decimal_places=2)
    attackGain2 = models.DecimalField(max_digits=3, decimal_places=2)
    attackDur2 = models.DecimalField(max_digits=6, decimal_places=2)
    decayDur2 = models.DecimalField(max_digits=6, decimal_places=2)
    sustainGain2 = models.DecimalField(max_digits=3, decimal_places=2)
    sustainDur2 = models.DecimalField(max_digits=6, decimal_places=2)
    release2 = models.DecimalField(max_digits=3, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =  models.DateTimeField(auto_now=True)
    objects = UserManager()