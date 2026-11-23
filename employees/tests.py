
from django.contrib.auth.models import User, Group

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from .models import Employee, Department


class EmployeeAPITestCase(APITestCase):

    def setUp(self):

        # 1. Create Admin group
        self.admin_group, created = Group.objects.get_or_create(
            name='Admin'
        )

        # 2. Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )

        # 3. Assign Admin role to test user
        self.user.groups.add(self.admin_group)

        # 4. Generate authentication token
        self.token = Token.objects.create(
            user=self.user
        )

        # 5. Authenticate API client
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token.key
        )

        # 6. Create test department
        self.department = Department.objects.create(
            name='IT',
            description='Information Technology'
        )

        # 7. Employee test data
        self.employee_data = {
            'employee_id': 'TEST001',
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'john.test@gmail.com',
            'phone': '9876543210',
            'designation': 'Software Developer',
            'department': self.department.id,
            'date_of_joining': '2025-08-07',
            'salary': '5000.00',
            'is_active': True
        }

        # 8. Create existing employee
        employee_model_data = self.employee_data.copy()
        employee_model_data['department'] = self.department

        self.employee = Employee.objects.create(
            **employee_model_data
        )

    # 1. Test employee creation
    def test_create_employee(self):

        data = self.employee_data.copy()

        data['employee_id'] = 'TEST002'
        data['email'] = 'jane.test@gmail.com'

        response = self.client.post(
            '/api/employees/',
            data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Employee.objects.count(),
            2
        )

    # 2. Test employee list
    def test_get_employee_list(self):

        response = self.client.get(
            '/api/employees/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data['count'],
            1
        )

    # 3. Test single employee retrieval
    def test_get_single_employee(self):

        response = self.client.get(
            f'/api/employees/{self.employee.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data['employee_id'],
            'TEST001'
        )

    # 4. Test complete employee update
    def test_update_employee(self):

        data = self.employee_data.copy()

        data['first_name'] = 'Updated'
        data['salary'] = '6500.00'

        response = self.client.put(
            f'/api/employees/{self.employee.id}/',
            data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.employee.refresh_from_db()

        self.assertEqual(
            self.employee.first_name,
            'Updated'
        )

        self.assertEqual(
            str(self.employee.salary),
            '6500.00'
        )

    # 5. Test partial employee update
    def test_partial_update_employee(self):

        data = {
            'designation': 'Technical Lead',
            'salary': '7500.00'
        }

        response = self.client.patch(
            f'/api/employees/{self.employee.id}/',
            data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.employee.refresh_from_db()

        self.assertEqual(
            self.employee.designation,
            'Technical Lead'
        )

    # 6. Test employee deletion
    def test_delete_employee(self):

        response = self.client.delete(
            f'/api/employees/{self.employee.id}/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Employee.objects.filter(
                id=self.employee.id
            ).exists()
        )

    # 7. Test department creation
    def test_create_department(self):

        data = {
            'name': 'HR',
            'description': 'Human Resources'
        }

        response = self.client.post(
            '/api/departments/',
            data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Department.objects.filter(
                name='HR'
            ).exists()
        )

    # 8. Test employee search
    def test_search_employee(self):

        response = self.client.get(
            '/api/employees/?search=John'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data['count'],
            1
        )

    # 9. Test department filter
    def test_filter_employee_by_department(self):

        response = self.client.get(
            f'/api/employees/?department={self.department.id}'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data['count'],
            1
        )

    # 10. Test active employee filter
    def test_filter_active_employees(self):

        response = self.client.get(
            '/api/employees/?is_active=true'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data['count'],
            1
        )

    # 11. Test unauthorized access
    def test_unauthorized_employee_access(self):

        self.client.credentials()

        response = self.client.get(
            '/api/employees/'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
