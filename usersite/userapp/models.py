from django.db import models

# Create your models here.
class MyUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    dob = models.DateField()

    class LikesChocolate(models.TextChoices):
        LIKES = "L", "Likes Chocolate"
        DISLIKES = "D", "Dislikes Chocolate"
    likes_chocolate = models.CharField(
        max_length=1,
        choices=LikesChocolate,
        default=LikesChocolate.LIKES,
    )
    age_first_taste_chocolate = models.IntegerField(null=True)
