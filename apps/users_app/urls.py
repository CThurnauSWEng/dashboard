from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^$', views.index),    
    url(r'^signin$', views.signin),     
    url(r'^register', views.register),     
    url(r'^logoff', views.logoff),     
    url(r'^profile', views.profile),     
    url(r'^dashboard', views.dashboard),     
    url(r'^add_user', views.add_user),     
    url(r'^edit/(?P<user_id>\d+)', views.edit_user),     
    url(r'^show/(?P<user_id>\d+)', views.show_user),     
    url(r'^process_login$', views.process_login),    
    url(r'^process_message$', views.process_message),    
    url(r'^process_comment$', views.process_comment),    
    url(r'^process_edit_info$', views.process_edit_info),    
    url(r'^process_pwd_change$', views.process_pwd_change),    
    url(r'^process_profile_edit_info$', views.process_profile_edit_info),    
    url(r'^process_profile_pwd_change$', views.process_profile_pwd_change),    
    url(r'^process_profile_desc_change$', views.process_profile_desc_change),    
    url(r'^process_register$', views.process_register)     
]
