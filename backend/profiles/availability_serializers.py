from rest_framework import serializers
from .availability_models import Availability


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['id', 'available_from_month', 'available_from_year', 'employment_type', 'salary_min', 'salary_max', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_available_from_month(self, value):
        if value < 1 or value > 12:
            raise serializers.ValidationError("Month must be between 1 and 12")
        return value

    def validate_available_from_year(self, value):
        if value < 1900 or value > 2100:
            raise serializers.ValidationError("Year must be between 1900 and 2100")
        return value

    def validate(self, data):
        salary_min = data.get('salary_min')
        salary_max = data.get('salary_max')

        if salary_min is not None and salary_min < 0:
            raise serializers.ValidationError("Salary min cannot be negative")
        if salary_max is not None and salary_max < 0:
            raise serializers.ValidationError("Salary max cannot be negative")

        if salary_min is not None and salary_max is not None:
            if salary_max < salary_min:
                raise serializers.ValidationError("Salary max cannot be less than salary min")

        return data
