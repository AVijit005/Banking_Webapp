from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_dashboard_view_status_code(self):
        response = self.client.get(reverse('core:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_view_context_data(self):
        response = self.client.get(reverse('core:dashboard'))
        self.assertTrue('total_balance' in response.context)
        self.assertTrue('recent_transactions' in response.context)
        self.assertTrue('chart_labels' in response.context)
        self.assertTrue('chart_data' in response.context)
