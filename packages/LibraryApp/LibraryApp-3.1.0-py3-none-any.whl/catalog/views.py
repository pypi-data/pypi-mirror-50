# from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
# pg 43, use explicit relative imports
# instead of {from catalog.serializers import BookSerializer, AuthorSerializer}
from .serializers import BookSerializer, AuthorSerializer
from .models import Book
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import permission_required
from .forms import RenewBookForm
from rest_framework import viewsets
from .models import BookInstance

# views for the api


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


def index(request):
    """View function for home page of site."""
    return render(request, 'index.html',)


class BookListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Book
    paginate_by = 4


class BookDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Book


class AuthorListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Author
    paginate_by = 4


class AuthorDetailView(generic.DetailView):
    """Generic class-based detail view for an author."""
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(
            status__exact='o').order_by('due_back')
