from django.db import models
from string import ascii_uppercase
from random import choices


def generate_unique_code() -> str:
    """
    Generate a unique code for a new room.

    Returns:
        str: The unique code for the new room.
    """
    length: int = 6
    while True:
        code = ''.join(choices(ascii_uppercase, k=length))
        if Room.objects.filter(code=code).count() == 0:
            break
    return code

# Create your models here.

class Room(models.Model):
    code = models.CharField(max_length=8, default=generate_unique_code, unique=True)
    host = models.CharField(max_length=50, unique=True)
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)