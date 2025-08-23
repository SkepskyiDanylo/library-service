import os

from django.test import TestCase


class TestConfiguration(TestCase):
    ENV_VARIABLES = [
        "BOT_TOKEN",
        "CHAT_ID",
        "CELERY_BROKER_URL",
        "STRIPE_API_KEY",
        "POSTGRES_PASSWORD",
        "POSTGRES_USER",
        "POSTGRES_DB",
        "POSTGRES_HOST",
        "POSTGRES_PORT",
    ]

    def test_check_env_configured(self):
        for var in self.ENV_VARIABLES:
            value = os.getenv(var, None)
            self.assertIsNotNone(value)
