from django.contrib import admin
from .models import User, Credential  # Replace with your actual models

admin.site.register(User)
admin.site.register(Credential)
