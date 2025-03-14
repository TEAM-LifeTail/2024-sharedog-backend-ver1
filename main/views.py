from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.viewsets import ViewSet
from .serializers import *
from rest_framework.permissions import AllowAny

# Create your views here.

class MainViewSet(ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        user = request.user  # 현재 로그인된 사용자
        region = request.query_params.get('region', None)
        context = {'request': request, 'region': region}
        serializer = MainSerializer(instance=user, context=context)
        return Response(serializer.data)