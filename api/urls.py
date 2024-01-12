from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import UserList, UserDetail, ClassList, ClassDetail, AssignmentTypeList, AssignmentTypeDetail,\
    AssignmentList, AssignmentDetail, SemesterList, SemesterDetail


urlpatterns = [
    path('users/', UserList.as_view(), name='users'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('semesters/', SemesterList.as_view(), name='semesters'),
    path('semesters/<int:pk>/', SemesterDetail.as_view(), name='semester_detail'),
    path('classes/', ClassList.as_view(), name='classes'),
    path('classes/<int:pk>/', ClassDetail.as_view(), name='class_detail'),
    path('assignment_types/', AssignmentTypeList.as_view(), name='assignment_types'),
    path('assignment_types/<int:pk>/', AssignmentTypeDetail.as_view(), name = 'assignment_type_detail'),
    path('assignments/', AssignmentList.as_view(), name = 'assignments'),
    path('assignments/<int:pk>/', AssignmentDetail.as_view(), name = 'assignment_detail'),

]

urlpatterns = format_suffix_patterns(urlpatterns)