from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError


class AppointmentModel(models.Model):
    """
    Appointment can be taken more than 5 times the user itself and get scheduled.If so user must be deprived of using this feature and only admin can make the appointment for the user
    """
    appointment_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    is_scheduled = models.BooleanField(default=False,null=True, blank=True)
    appointment_count = models.PositiveIntegerField()
    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = "Appointments"
    
    def validate_appointment_count(self):
        if self.is_scheduled:
            scheduled_appointments_count = AppointmentModel.objects.filter(user=self.user, is_scheduled=True).count()
            if scheduled_appointments_count >= 5:
                raise ValidationError("User has already scheduled 5 appointments.")
        if self.appointment_count > 5:
            raise ValidationError("Appointment count cannot exceed 5.")

    def save(self, *args, **kwargs):
        self.validate_appointment_count()  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} ==> {self.appointment_date}"

class KYC(models.Model):
    """
    KYC model keeps account of all objects created live or recorded.
    Online flow starts with taking appointment. On completing/saving the video recorded the KYC object is created. 
    If got interrupted, KYC object is not created.
    """
    kyc_type_choices = (
        ("Online", "Online"),
        ("Recorded", "Recorded"),
    )
    
    status_choices = (
        ("appointment_taken", "appointment_taken"),
        ("appointment_booked", "appointment_booked"),
        ("under_review", "under_review"),
        ("approved", "approved"),
        ("rejected", "rejected"),
        ("closed","closed"),   #"closed" due to discontinuation in recorded kyc verification method probably preferred offline verification.
        ("reverted", "reverted"),
    )

    application_id = models.UUIDField(max_length=30, unique=True)
    applicant_name = models.CharField(max_length=300)
    kyc_type = models.CharField(choices=kyc_type_choices, max_length=10)
    email = models.EmailField()
    booked_country = models.CharField(max_length=200, default="Nepal", null=True, blank=True)
    status = models.CharField(choices=status_choices, default="appointment_taken", max_length=20)
    
    online_appointment = models.ManyToManyField(AppointmentModel, on_delete=models.CASCADE,null=True,blank=True)
    scheduled_date = models.DateTimeField(null=True,blank=True)
    scheduled_remarks = models.TextField(null=True,blank=True) # if EMPLOYEE changed the appointment date then scheduled remarks must be provided 
    scheduled_at = models.DateTimeField(null=True, blank=True)
    scheduled_by = models.ForeignKey(User, related_name='scheduled_by', on_delete=models.SET_NULL, null=True)

    is_rebooked = models.BooleanField(default=False)


    reverted_count = models.PositiveIntegerField(default=0)
    
    close_remarks = models.TextField(null=True, blank=True)
    reject_remarks = models.TextField(null=True, blank=True)
    return_remarks = models.TextField(null=True, blank=True)
    repair_remarks = models.JSONField(null=True, blank=True)
   
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, related_name='approved_by', on_delete=models.SET_NULL, null=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    rejected_by = models.ForeignKey(User, related_name='rejected_by', on_delete=models.SET_NULL, null=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(User, related_name='verified_by', on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_online_to_live_converted = models.BooleanField(default=False)
    online_to_live_conversion_reason = models.TextField(null=True,blank=True)
    online_to_live_conversion_date = models.DateTimeField(null=True, blank=True)
    
    is_live_to_online_converted = models.BooleanField(default=False)
    live_to_online_conversion_date = models.DateTimeField(null=True, blank=True)
    live_to_online_conversion_reason = models.TextField(null=True,blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'KYC'
        verbose_name_plural = "KYC"

    

