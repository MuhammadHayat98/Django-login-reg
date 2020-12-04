from django.urls import path
from .views import BlogListView, BlogDetailView, BlogCreateView
from . import views

urlpatterns = [
    path('', BlogListView.as_view(), name="home"),
    path('blog/<int:pk>', BlogDetailView.as_view(), name="blog-detail"),
    path('blog/new/', BlogCreateView.as_view(), name="blog-create"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    # path('initdb/', views.userReturn, name="initdb"),
    # path('blog/', views.blogPage, name="blog"),
    path('followsWho/',views.followsWho, name="followsWho"),
    path('neverPosted/',views.neverPosted, name="neverPosted"),
    path('noNegativeComments/',views.noNegativeComments, name="noNegativeComments"),
    path('onDate/',views.onDate, name="onDate"),
    path('positive/',views.positive, name="positive"),
    path('someNegative/',views.someNegative, name="someNegative")
]