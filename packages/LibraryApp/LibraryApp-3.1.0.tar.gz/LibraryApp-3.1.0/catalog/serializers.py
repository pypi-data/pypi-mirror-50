from rest_framework import serializers
from .models import Book, Author


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('title', 'author', 'summary', 'isbn',
                  'genre', 'language', )


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ('first_name', 'last_name', )
