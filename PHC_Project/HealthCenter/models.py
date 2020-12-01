from django.db import models


class Doctor(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    doctor_id = models.CharField(max_length=25, primary_key=True)
    name = models.CharField(max_length=40, null=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    position = models.CharField(max_length=25)
    phone = models.CharField(max_length=14)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=25)
    pincode = models.CharField(max_length=6, default=482005)

    def __str__(self):
        return self.name


class Beneficiary(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    POSITION_CHOICES = (
        ('S', 'Student'),
        ('F', 'Faculty'),
        ('W', 'Workers'),
        ('C', 'CareTaker'),
        ('G', 'Guards')
    )
    Beneficiary_id = models.CharField(max_length=25, primary_key=True)
    name = models.CharField(max_length=25, null=False)
    position = models.CharField(max_length=1, choices=POSITION_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    DOB = models.DateField(verbose_name="Date of Birth")
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=25)
    pincode = models.CharField(max_length=6, default=123456)

    def calculate_age(self):
        return date.today().year - self.DOB.year

    class Meta:
        ordering = ["name"]
        verbose_name_plural = 'Beneficiaries Register'

    def __str__(self):
        return self.Beneficiary_id + ' - ' + self.name


