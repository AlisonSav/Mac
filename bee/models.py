from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=30)
    born_date = models.CharField(max_length=70)
    born_loc = models.CharField(max_length=50)
    about = models.TextField()

    def __str__(self):
        return f"Author: {self.name}, born: {self.born_date}"


class Quote(models.Model):
    quote = models.TextField(unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"Quote: {self.quote}, {self.author}"
