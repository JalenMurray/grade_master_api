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


class ClassView(View):
    def get(self, request, class_id):
        c = get_object_or_404(Class, id=class_id)
        assignment_types = c.assignment_types.all()
        data = {
            'class':{
                'id': c.id,
                'name': c.name,
                'semester': c.semester,
                'assignment_types': [
                    {'id': at.id, 'name': at.name, 'max_score': at.max_score} for at in assignment_types
                ]
            }
        }
        return JsonResponse(data)


class AssignmentTypeView(View):
    def get(self, request, at_id):
        at = get_object_or_404(AssignmentType, id=at_id)
        assignments = at.assignments.all()
        data = {
            'assignment_type': {
                'id': at.id,
                'name': at.name,
                'max_score': at.max_score,
                'assignments': [{'id': a.id, 'name': a.name, 'score': a.score, 'weight': a.weight} for a in assignments]
            }
        }
        return JsonResponse(data)

class AssignmentView(View):
    def get(self, request, a_id):
        a = get_object_or_404(Assignment, id=a_id)
        data = {
            'assignment': {
                'id': a.id,
                'name': a.name,
                'score': a.score,
                'weight': a.weight
            }
        }
        return JsonResponse(data)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'])
    def new(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class ClassViewSet(ModelViewSet):
    serializer_class = ClassSerializer
    queryset = Class.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(users__id=user_id)
        return queryset


class AssignmentViewSet(ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    @action(detail=True, methods=['post'])
    def new(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


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
