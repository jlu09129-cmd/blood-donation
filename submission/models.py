from django.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator


# -------------------- USER MODEL --------------------
class User(models.Model):
    user_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveIntegerField(validators=[MinValueValidator(18)])
    blood_group = models.CharField(max_length=5)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, unique=True)
    last_donation_date = models.DateField(blank=True, null=True)
    availability = models.CharField(max_length=10, default='Yes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_id

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(age__gte=18),
                name='user_age_gte_18',
            ),
        ]


# -------------------- HEALTH STATUS MODEL --------------------
class HealthStatus(models.Model):
    healthstatus_id = models.CharField(max_length=10, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rh_factor = models.CharField(max_length=10, default='Yes')
    infection_screening = models.CharField(max_length=10, default='Yes')
    rbc_screening = models.CharField(max_length=10, default='Normal')
    bp_status = models.CharField(max_length=10, default='Yes')
    sugar = models.CharField(max_length=10, default='Yes')
    under_medication = models.CharField(max_length=10, default='Yes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.healthstatus_id


# -------------------- REQUEST MODEL --------------------
class Request(models.Model):
    request_id = models.CharField(max_length=10, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    blood_group = models.CharField(max_length=5)
    units_required = models.PositiveIntegerField()
    hospital_name = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15)
    request_date = models.DateField()
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.request_id
