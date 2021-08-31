from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone


class MyUserManager(BaseUserManager):
    def create_user(self, email, fullname,  date_of_birth, mobile, pan, address, city, state, date_of_issue,
                    password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=MyUserManager.normalize_email(email),
            fullname=fullname,
            date_of_birth=date_of_birth,
            mobile=mobile,
            pan=pan,
            address=address,
            city=city,
            state=state,
            date_of_issue=date_of_issue,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        u = self.create_user(username,
                             password=password
                             )
        u.is_admin = True
        u.save(using=self._db)
        return u


class MyUser(AbstractBaseUser):
    email = models.EmailField(
                        verbose_name='email address',
                        max_length=255,
                        unique=False,
                    )
    fullname = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    mobile = models.IntegerField()
    pan = models.CharField(max_length=50)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    date_of_issue = models.DateField(default=timezone.now())
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    # def get_full_name(self):
    #     # The user is identified by their email address
    #     return self.email
    #
    # def get_short_name(self):
    #     # The user is identified by their email address
    #     return self.email

    def __str__(self):
        return self.fullname + " | " + str(self.mobile) + " | " + str(self.date_of_issue)

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class InternalTeam(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    loan_amount = models.IntegerField()
    tenure_period = models.CharField(max_length=100)
    rate_of_interest = models.CharField(max_length=50)
    interest_amount = models.FloatField()
    amount_to_be_paid = models.FloatField()
    final_rate = models.FloatField()
    due_date = models.CharField(max_length=50)

    def __str__(self):
        return self.name + " | " + " amount to be paid: " + str(self.amount_to_be_paid) + " | on: " + str(self.due_date)
