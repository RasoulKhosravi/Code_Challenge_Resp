from rest_framework import status
from users.models import CustomUser as User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Task
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import Task  


class TaskAPITests(APITestCase):
    def setUp(self):
        # Create test users
        self.regular_user = User.objects.create_user(
            phone_number='09121234567', 
            password='testpass123'
        )
        self.staff_user = User.objects.create_user(
            phone_number='09919928825', 
            password='staffpass123', 
            is_staff=True
        )
        
        self.regular_user_task = Task.objects.create(
            user=self.regular_user, 
            title='Regular User Task', 
            status='In Progress'
        )
        self.another_user_task = Task.objects.create(
            user=User.objects.create_user(
                phone_number='09919928215', 
                password='anotherpass123'
            ), 
            title='Another User Task', 
            status='Completed'
        )

        self.regular_user_token = str(RefreshToken.for_user(self.regular_user).access_token)
        self.staff_user_token = str(RefreshToken.for_user(self.staff_user).access_token)

    def authenticate(self, user_token):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

    def test_create_task_authenticated(self):
        self.authenticate(self.regular_user_token)
        
        task_data = {
            'title': 'New Test Task',
            'status': 'Completed'
        }
        
        response = self.client.post(reverse('task_list'), task_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Test Task')
        self.assertEqual(response.data['user'], self.regular_user.id)

    def test_create_task_unauthenticated(self):
       
        task_data = {
            'title': 'Unauthorized Task',
            'status': 'In Progress'
        }
        
        response = self.client.post(reverse('task_list'), task_data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_tasks_authenticated(self):
        self.authenticate(self.regular_user_token)
        response = self.client.get(reverse('task_list'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Regular User Task')

        self.authenticate(self.staff_user_token)
        
        response = self.client.get(reverse('task_list'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 1)

    def test_retrieve_task_details(self):
        self.authenticate(self.regular_user_token)
        
        response = self.client.get(
            reverse('task_details', kwargs={'pk': self.regular_user_task.id})
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Regular User Task')

        response = self.client.get(
            reverse('task_details', kwargs={'pk': self.another_user_task.id})
        )
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_task(self):
        self.authenticate(self.regular_user_token)
        
        update_data = {
            'title': 'Updated Task Title',
            'status': 'Completed'
        }
        
        response = self.client.patch(
            reverse('task_details', kwargs={'pk': self.regular_user_task.id}),
            update_data
        )
        print("Update Task Response:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Task Title')
        self.assertEqual(response.data['status'], 'Completed')

    def test_delete_task(self):
        self.authenticate(self.regular_user_token)
        
        response = self.client.delete(
            reverse('task_details', kwargs={'pk': self.regular_user_task.id})
        )
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete(
            reverse('task_details', kwargs={'pk': self.another_user_task.id})
        )
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_user_permissions(self):
        
        self.authenticate(self.staff_user_token)
        
        response = self.client.get(
            reverse('task_details', kwargs={'pk': self.another_user_task.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

        update_data = {'title': 'Staff Updated Task'}
        response = self.client.patch(
            reverse('task_details', kwargs={'pk': self.another_user_task.id}),
            update_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.delete(
            reverse('task_details', kwargs={'pk': self.another_user_task.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)