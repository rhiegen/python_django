from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=40)
    age = models.PositiveIntegerField()
    date_of_birth = models.DateField()

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.name} ({self.age})"
