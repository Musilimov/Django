from django.core.cache import cache
from django.test import TestCase
from students.models import Student

class CachingTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            name="John Doe",
            email="johndoe@example.com",
            dob="2000-01-01"
        )

    def test_cache_student(self):
        """Test that student data is cached."""
        cache.set(f"student_{self.student.id}", self.student)
        cached_student = cache.get(f"student_{self.student.id}")
        self.assertEqual(cached_student.name, "John Doe")

        # Ensure that fetching from the cache does not result in DB queries
        with self.assertNumQueries(0):
            cache.get(f"student_{self.student.id}")
