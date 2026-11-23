
from django.contrib import admin
from .models import Employee, Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'created_at',
    )

    search_fields = ('name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        'employee_id',
        'first_name',
        'last_name',
        'email',
        'designation',
        'department',
        'salary',
        'is_active',
    )

    search_fields = (
        'employee_id',
        'first_name',
        'last_name',
        'email',
    )

    list_filter = (
        'department',
        'is_active',
    )


# Register your models here.
