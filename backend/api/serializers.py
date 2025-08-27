from rest_framework import serializers
from .models import Project, ContactMessage, QuickLink, HireRequest

# -----------------------------
# Project Serializer
# -----------------------------
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


# -----------------------------
# Contact Message Serializer
# -----------------------------
class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'
        read_only_fields = ('created_at',)


# -----------------------------
# Quick Link Serializer
# -----------------------------
class QuickLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuickLink
        fields = '__all__'


# -----------------------------
# Hire Request Serializer
# -----------------------------
class HireRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HireRequest
        fields = '__all__'
        read_only_fields = ('created_at',)
