from django.urls import path

from . import views

app_name = 'chat'
urlpatterns = [
    path('', views.index, name='overview'),
    path('<int:participationID>/<slug:conversationname>', views.detail, name='detail'),
    path('newMessage/user/<int:userID>/', views.newMessage, name='newMessage'),
    path('newMessage/project/<int:projectID>/', views.newMessage, name='newMessage'),
    path('sendMessage/', views.sendMessage, name="sendMessage"),
    path('sendMessage/<int:participationID>/', views.sendMessage, name="sendMessage"), # TODO check of da zo goe is met default participationID
    path('ajax/getNumberOfUnreadChats/', views.getNumberOfUnreadChats, name='getNumberOfUnreadChats'),
    path('ajax/updateLastRead/', views.updateLastRead, name='updateLastRead'),
]
