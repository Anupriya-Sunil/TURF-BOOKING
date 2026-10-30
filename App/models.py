from django.db import models


class Turf(models.Model):
    turf_name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='turf/', null=True, blank=True)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.turf_name

class Booking(models.Model):
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_amount = models.IntegerField()
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.customer_name

    

class UserCode(models.Model):
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE
    )
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.code


from django.contrib.auth.models import User

class Booking(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_amount = models.IntegerField()
    status = models.IntegerField(default=0)

