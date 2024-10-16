from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=100)
    mobile = serializers.CharField(max_length=15)
    password = serializers.CharField(max_length=255)

    def create(self, validated_data):
        # You could hash the password here if needed
        return validated_data  # Return the validated data for creating the user
