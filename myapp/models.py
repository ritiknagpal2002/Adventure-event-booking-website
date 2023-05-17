from django.contrib.auth.models import User
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings


class Client(User):
    IsAdmin = models.BooleanField(null=False)

    # PhoneNumber = models.PositiveIntegerField(null=False)
    class Meta:
        verbose_name = "Client"


class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} - {self.token}'

    def send_reset_email(self):
        subject = 'Reset your password'
        message = f'Click the following link to reset your password: http://127.0.0.1:8000/reset_password/{self.token}/'
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [self.user.email],
            fail_silently=False,
        )


class AdventureType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class Adventure(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.ForeignKey(AdventureType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CreateEvent(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    advanture = models.ForeignKey(Adventure, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='static/myapp/pics')
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    event_date = models.DateTimeField()

    def __str__(self):
        return self.name


class EventBooking(models.Model):
    event = models.ForeignKey(CreateEvent, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    number_of_people = models.IntegerField(default=1)
    total_amount_paid = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.user.username} booked {self.event.name}'

    def get_absolute_url(self):
        return reverse('event_booking_detail', args=[str(self.id)])
