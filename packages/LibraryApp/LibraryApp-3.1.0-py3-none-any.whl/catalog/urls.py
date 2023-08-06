from django.urls import path, include
from rest_framework import routers
from . import views

# pg47 Use Underscores in URL Pattern Names Rather Than Dashes
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>',
         views.AuthorDetailView.as_view(), name='author-detail'),

]


urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(),
         name='my_borrowed'),
]


urlpatterns += [
    path('api/v1/books/', views.BookViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path('api/v1/authors/', views.AuthorViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
]

# router = routers.DefaultRouter()
# router.register(r'api/books', views.BookViewSet)
# router.register(r'api/authors', views.AuthorViewSet)

# urlpatterns += [
#     path('', include(router.urls)),
#     path(r'api/', include('rest_framework.urls', namespace='rest_framework'))

# ]
