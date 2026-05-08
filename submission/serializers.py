from rest_framework import serializers
from .models import User, HealthStatus, Request


# -----------------------------
# User Serializer
# -----------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


# -----------------------------
# Health Status Serializer
# -----------------------------
class HealthStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthStatus
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


# -----------------------------
# Request Serializer
# -----------------------------
class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
