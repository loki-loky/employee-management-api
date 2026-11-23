
from rest_framework import serializers
from .models import Employee, Department


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):

    department_name = serializers.CharField(
        source='department.name',
        read_only=True
    )

    class Meta:
        model = Employee

        fields = [
            'id',
            'employee_id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'designation',
            'department',
            'department_name',
            'date_of_joining',
            'salary',
            'is_active',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]
