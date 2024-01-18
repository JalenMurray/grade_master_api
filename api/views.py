from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status

from .models import User, Class, AssignmentType, Assignment, Semester
from .serializers import UserSerializer, ClassSerializer, AssignmentTypeSerializer, AssignmentSerializer,\
    SemesterSerializer


class CheckUserAPI(View):
    def post(self, request, *args, **kwargs):
        uid = self.request.POST.get('uid')
        auth = self.request.POST.get('auth')

        try:
            if auth:
                user = get_object_or_404(User, auth=auth)
            else:
                user = get_object_or_404(User, uid=uid)
            return JsonResponse({'exists': True, 'user': user})
        except User.DoesNotExist:
            return JsonResponse({'exists': False})
        return JsonResponse({'error': 'Invalid Request Method'}, status=400)


class UserList(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ClassList(ListCreateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class ClassDetail(RetrieveUpdateDestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class AssignmentTypeList(ListCreateAPIView):
    queryset = AssignmentType.objects.all()
    serializer_class = AssignmentTypeSerializer


class AssignmentTypeDetail(RetrieveUpdateDestroyAPIView):
    queryset = AssignmentType.objects.all()
    serializer_class = AssignmentTypeSerializer


class AssignmentList(ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer


class AssignmentDetail(RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer


class SemesterList(ListCreateAPIView):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer


class SemesterDetail(RetrieveUpdateDestroyAPIView):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
