from django.contrib import admin
from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static
from .import calendar_api

urlpatterns = [
   path('',views.login),
   path('dashboard',views.dashboard),
   path('doctor/',views.doctor),
   path('messages',views.messages1),
   path('signup',views.signup_detail),
   path('login_detail',views.login_detail),
   path('logout',views.logout),
   path('navbar',views.navbar),
   path('base',views.base),
   path('blog',views.blog),
   path('allblogs',views.allblogs),
   path('nodata',views.nodata),
   path('blogdata',views.NewBlog),
   path('blogdetail/<int:id>',views.blogdetail),
   path('draftblog',views.draftblog),
   path('patientdetail',views.patientdetail),
   path('post_list',views.post_list),
   path('filter_items',views.filter_items),
   path('drlist',views.drlist),
   path('bookappoint/<int:UserID>',views.bookappoint),
   path('bookappoint/appointmentdetail/<int:UserID>',views.appointmentdetail),
   path('appointdetail',views.appointdetail),
   path('errormsg',views.errormsg),
   path('drappoint',views.drappoint),
   # path('get_google_calendar_service',views.get_google_calendar_service),
   # path('bookappoint/book_appointment/<int:UserID>',views.book_appointment)
   path('get_googlecalendar',calendar_api.get_google_calendar_service),
   path('create_calendar_event',calendar_api.create_calendar_event),
#    path('chat/<int:recipient_id>/', views.chat, name='chat'),


   path('<str:RoomName>/', views.room, name='room'),
   path('checkview/<str:UserName>', views.checkview, name='checkview'),
   path('send', views.send, name='send'),
   path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
   
   
  
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                                 document_root=settings.MEDIA_ROOT)

