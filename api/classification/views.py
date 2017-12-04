from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.models import User, Group

from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from classification.serializers import JobSerializer
from classification.models import Job

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the classification index.")

class JobViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Job.objects.all().order_by('-created_at')
    serializer_class = JobSerializer

    @list_route(methods=['post', 'get'])
    def classify(self, request, pk=None):
        reference_number = request.POST['reference_number']
        content          = request.POST['content']
        job = Job(reference_number=reference_number, content=content)
        job.save()
        return Response(str(job.id))


