from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from cinema.models import Movie, Genre, Actor
from cinema.serializers import MovieSerializer


class MovieApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.genre = Genre.objects.create(name="Drama")
        self.actor = Actor.objects.create(first_name="Jack", last_name="Nicholson")

        self.movie1 = Movie.objects.create(
            title="Titanic",
            description="Titanic description",
            duration=200,
        )
        self.movie1.genres.add(self.genre)
        self.movie1.actors.add(self.actor)

        self.movie2 = Movie.objects.create(
            title="Batman",
            description="Batman description",
            duration=190,
        )

    def test_post_movies(self):
        payload = {
            "title": "Superman",
            "description": "Superman description",
            "duration": 170,
            "genres": [self.genre.id],  # Тепер серіалізатор буде валідним
            "actors": [self.actor.id],
        }
        response = self.client.post("/api/cinema/movies/", payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 3)
        self.assertTrue(Movie.objects.filter(title="Superman").exists())

    def test_put_movie(self):
        payload = {
            "title": "Watchman",
            "description": "Watchman description",
            "duration": 190,
            "genres": [self.genre.id],
            "actors": [self.actor.id],
        }
        response = self.client.put(f"/api/cinema/movies/{self.movie1.id}/", payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.movie1.refresh_from_db()

        self.assertEqual(self.movie1.title, "Watchman")
        self.assertEqual(self.movie1.duration, 190)

    def test_patch_movie(self):
        response = self.client.patch(
            f"/api/cinema/movies/{self.movie1.id}/",
            {"title": "Watchmen"}
        )
        self.movie1.refresh_from_db()
        self.assertEqual(self.movie1.title, "Watchmen")
        self.assertEqual(response.status_code, status.HTTP_200_OK)