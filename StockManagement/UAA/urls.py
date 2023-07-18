
from django.urls import path, include
from . import views
urlpatterns = [

    path('', views.loginPage, name='loginPage'),
    path("logoutPage", views.logoutPage, name="logoutPage"),
    path('searchUserSelected', views.searchUserSelected, name = "searchUserSelected"),
    path('register', views.registerPage, name ='registerPage'),
    path('foggotenPassword', views.foggotenPassword, name= 'foggotenPassword'),
    path('opt_sent/<str:id>', views.opt_sent, name= 'opt_sent'),
    path('resend_password/<str:id>', views.resend_password, name= 'resend_password'),
    path('setting_password/<str:id>', views.setting_password, name= 'setting_password'),

    path('Admision_status', views.Admision_statusPage, name ='Admision_statusPage'),
    path('userProfile', views.userProfilePage, name ='userProfilePage'),
    path('updateStudent', views.updateStudent, name = 'updateStudent'),
    path('changePassword', views.changePassword, name = 'changePassword'),
    path('Dashboard', views.DashboardPage, name ='DashboardPage'),

    path('studentList', views.studentList, name ='studentlist'),
    path('AddTeacher', views.AddTeacher, name ='AddTeacher'),
    path('studentAdd', views.studentAdd, name ='studentAdd'),
    path('studentEdit/<str:id>', views.studentEdit, name ='studentEdit'),
    path('blockuser/<str:id>', views.blockuser, name ='blockuser'),

    path('manageroles', views.manageroles, name ='manageroles'),
    path('addroles', views.addroles, name ='addroles'),
    path('RemoveRole/<str:rid>/<str:pid>', views.RemoveRole, name ='RemoveRole'),
    path('AssignUserRole/<str:uid>', views.AssignUserRole, name ='AssignUserRole'),
    path('editroles/<str:id>', views.editroles, name ='editroles'),
    path('deleteroles/<str:id>', views.deleteroles, name ='deleteroles'),

]
