
from django.db.models import Q

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from .permissions import EmployeeManagementPermission

from .models import Employee, Department
from .serializers import (
    EmployeeSerializer,
    DepartmentSerializer
)


class EmployeeViewSet(viewsets.ModelViewSet):

    serializer_class = EmployeeSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [EmployeeManagementPermission]

    def get_queryset(self):

        queryset = Employee.objects.select_related(
            'department'
        ).all().order_by('-id')

        department = self.request.query_params.get(
            'department'
        )

        is_active = self.request.query_params.get(
            'is_active'
        )

        search = self.request.query_params.get(
            'search'
        )

        if department:
            queryset = queryset.filter(
                department_id=department
            )

        if is_active is not None:
            if is_active.lower() in ['true', 'false']:
                queryset = queryset.filter(
                    is_active=is_active.lower() == 'true'
                )

        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(designation__icontains=search)
            )

        return queryset


class DepartmentViewSet(viewsets.ModelViewSet):

    queryset = Department.objects.all().order_by('name')

    serializer_class = DepartmentSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [EmployeeManagementPermission]


# Create your views here.
