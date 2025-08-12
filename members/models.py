from django.db import models
from django.contrib.auth.models import AbstractUser

class Homecell(models.Model):
    name = models.CharField(max_length=120)
    pastor = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL, related_name='pastored_homecells')

    def __str__(self):
        return self.name

class Ministry(models.Model):
    name = models.CharField(max_length=120)
    leader = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL, related_name='led_ministries')

    def __str__(self):
        return self.name

class Family(models.Model):
    family_name = models.CharField(max_length=200)

    def __str__(self):
        return self.family_name

class User(AbstractUser):
    class Roles(models.TextChoices):
        SUPER_ADMIN = 'super_admin', 'Super Admin'
        HOMECELL_PASTOR = 'homecell_pastor', 'Homecell Pastor'
        MINISTRY_LEADER = 'ministry_leader', 'Ministry Leader'

    role = models.CharField(max_length=30, choices=Roles.choices, default=Roles.HOMECELL_PASTOR)
    homecell = models.ForeignKey(Homecell, null=True, blank=True, on_delete=models.SET_NULL)
    ministry = models.ForeignKey(Ministry, null=True, blank=True, on_delete=models.SET_NULL)

    def is_super_admin(self):
        return self.role == self.Roles.SUPER_ADMIN

    def is_homecell_pastor(self):
        return self.role == self.Roles.HOMECELL_PASTOR

    def is_ministry_leader(self):
        return self.role == self.Roles.MINISTRY_LEADER

class Member(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('transferred', 'Transferred'),
        ('moved_away', 'Moved Away'),
        ('deceased', 'Deceased'),
    ]

    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    dob = models.DateField(null=True, blank=True)

    home_origin_district = models.CharField(max_length=120, blank=True)
    home_origin_ta = models.CharField(max_length=120, blank=True)
    home_origin_village = models.CharField(max_length=120, blank=True)

    residential_home = models.CharField(max_length=255, blank=True)

    homecell = models.ForeignKey(Homecell, null=True, blank=True, on_delete=models.SET_NULL)
    ministry = models.ForeignKey(Ministry, null=True, blank=True, on_delete=models.SET_NULL)

    picture = models.ImageField(upload_to='member_photos/', null=True, blank=True)
    marital_status = models.CharField(max_length=50, blank=True)
    employment_status = models.CharField(max_length=50, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    family = models.ForeignKey(Family, null=True, blank=True, on_delete=models.SET_NULL, related_name='members')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        from datetime import date
        if not self.dob:
            return None
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))