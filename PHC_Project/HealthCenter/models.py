from django.db import models
from datetime import datetime
from django.utils import timezone
from django.db.models.signals import pre_delete
from django.dispatch import receiver


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

    class Meta:
        ordering = ["name"]
        verbose_name_plural = 'Beneficiaries Register'

    def __str__(self):
        return self.Beneficiary_id + ' - ' + self.name


class Medicines(models.Model):
    name = models.CharField(max_length=75, primary_key=True, verbose_name="Medicine Name")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'Medicines Register'

    def __str__(self):
        return self.name


# The field on the related object that the relation is to. By default, Django uses the primary key of the related
# object. If you reference a different field, that field must have unique=True.


class PatientEntry(models.Model):
    patient_no = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey(Beneficiary, to_field='Beneficiary_id', on_delete=models.CASCADE,
                                   related_name='patient_id')
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(editable=False)
    visit_date = models.DateTimeField(default=timezone.now, editable=False)

    def save(self, *args, **kwargs):
        self.age = date.today().year - self.patient_id.DOB.year
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Patients Entry Register'

    def __str__(self):
        return self.patient_id.Beneficiary_id + ' - ' + self.patient_id.name


class Prescription(models.Model):
    patient_no = models.ForeignKey(PatientEntry, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicines, on_delete=models.CASCADE, to_field="name")
    quantity = models.PositiveIntegerField(default=2)

    # If I am prescribing the medicines to a patient then that amount of particular medicine must be decreased in the stock.

    def save(self, *args, **kwargs):
        current = Medicines.objects.get(name=getattr(self.medicine, 'name'))
        current.stock -= self.quantity
        current.save()
        super().save(*args, **kwargs)



# update the medicines stock after deleting the prescribed medicines to a patient
@receiver(pre_delete, sender=Prescription)
def update_medicine_after_delete(sender, instance, using, **kwargs):
    current = Medicines.objects.get(name=getattr(instance.medicine, 'name'))
    current.stock += instance.quantity
    current.save()
