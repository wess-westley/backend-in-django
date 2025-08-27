from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, RegexValidator

# -----------------------------
# Contact / General Messages
# -----------------------------
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submission_type = models.CharField(max_length=20, default='general')  # Optional field like old model
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name}"


# -----------------------------
# Hire Requests
# -----------------------------
class HireRequest(models.Model):
    applicant_name = models.CharField(max_length=100)
    applicant_email = models.EmailField()
    applicant_phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{7,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    company_name = models.CharField(max_length=150)
    role = models.CharField(max_length=100)
    offered_salary = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(0)]
    )
    message = models.TextField(blank=True, null=True)  # Optional
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Hire request from {self.applicant_name} ({self.company_name})"


# -----------------------------
# Projects
# -----------------------------
class Project(models.Model):
    SOURCE_CHOICES = (
        ('MANUAL', 'Manual'),
        ('GITHUB', 'GitHub'),
    )

    title = models.CharField(max_length=100, validators=[MinLengthValidator(5)])
    description = models.TextField(validators=[MinLengthValidator(10)])
    tech_stack = models.CharField(max_length=200)
    github_url = models.URLField(blank=True, null=True)
    demo_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES, default='MANUAL')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# -----------------------------
# Quick Links
# -----------------------------
class QuickLink(models.Model):
    title = models.CharField(max_length=50)
    url = models.URLField()
    icon_class = models.CharField(max_length=50, blank=True)  # e.g., font-awesome icon
    color = models.CharField(max_length=20, default='#3498db')
    is_download = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
