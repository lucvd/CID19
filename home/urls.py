from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<int:userID>/<slug:slugName>/', views.profilepage, name='profile'),
    path('profile/edit', views.editprofilepage, name="editprofile"),
    path('profile/edit/picture', views.editprofilepicturepage, name="editprofilepicture"),
    path('profile', views.ownprofilepage, name='ownProfile'),

    path('logout', views.logout, name='logout'), # Logout should always be a POST request! https://stackoverflow.com/questions/3521290/logout-get-or-post
    path('login', views.login, name='login'),
    path('loginSuccess', views.loginSuccess, name="loginSuccess"),
    path('users', views.users, name='users'),

    path('projects/<int:projectID>/<slug:slugTitle>/', views.projectpage, name='project'),
    path('projects', views.projects, name='projects'),
    path('projects/edit/<int:projectID>/', views.editprojectpage, name='editproject'),
    path('projects/newproject/', views.newprojectpage, name='newproject'),

    path('feedback', views.feedback, name='feedback'),

    path('ajax/togglefavorite/', views.togglefavorite, name="togglefavorite"),
    path('ajax/deleteproject/<int:projectID>/', views.deleteproject, name="deleteproject"),
]
