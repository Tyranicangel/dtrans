from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,renderer_classes
from rest_framework import permissions,viewsets,serializers,renderers,status
from core.models import Factor,Radiators,Vertical,Horizontal,Fins,Designs,Eddys
from core.iters import Iters
from core.multiiters import MultiIters
from users.models import User
import json
import time

# Create your views here.

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User

@api_view(['POST'])
@renderer_classes([renderers.JSONRenderer])
@permission_classes((permissions.IsAuthenticated, ))
def iterators(request, format=None):
	if(request.DATA.get('core')['coretype']=='stacked' and request.DATA.get('core')['num']=='Multi'):
		x=MultiIters()
	else:
		x=Iters()
	x.assign_data(request.DATA.get('basic'),request.DATA.get('core'),request.DATA.get('tapping'),request.DATA.get('lv'),request.DATA.get('hv'),request.DATA.get('cca'),request.DATA.get('cooling'),request.DATA.get('tank'),request.DATA.get('other'),request.DATA.get('check'),request.DATA.get('costing'),request.DATA.get('iters'))
	start = time.time()
	dat=x.run_thread()
	end = time.time()
	print end-start
	return Response([dat,x.counter])

@api_view(['GET'])
@renderer_classes([renderers.JSONRenderer])
@permission_classes((permissions.IsAuthenticated, ))
def root(request, format=None):
	x = {
	}
	return Response(x)

@api_view(['GET'])
@renderer_classes([renderers.JSONRenderer])
@permission_classes((permissions.IsAuthenticated, ))
def get_user_data(request, format=None):
	data = UserSerializer(request.user).data
	return Response(data, status=status.HTTP_200_OK)

class DesignSerializer(serializers.ModelSerializer):
	class Meta:
		model = Designs

class FactorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Factor

class RadiatorsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Radiators

class HorizontalSerializer(serializers.ModelSerializer):
	class Meta:
		model = Horizontal

class VerticalSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vertical

class FinsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Fins

class EddySerializer(serializers.ModelSerializer):
	class Meta:
		model = Eddys

class DesignViewSet(viewsets.ModelViewSet):
	"""
	This viewset automatically provides `list` and `detail` actions.
	"""
	queryset = Designs.objects.all()
	serializer_class = DesignSerializer
	permission_classes = (permissions.IsAuthenticated, )

class VerticalViewSet(viewsets.ModelViewSet):
	"""
	This viewset automatically provides `list` and `detail` actions.
	"""
	queryset = Vertical.objects.all()
	serializer_class = VerticalSerializer
	permission_classes = (permissions.IsAuthenticated, )

class HorizontalViewSet(viewsets.ModelViewSet):
	"""
	This viewset automatically provides `list` and `detail` actions.
	"""
	queryset = Horizontal.objects.all()
	serializer_class = HorizontalSerializer
	permission_classes = (permissions.IsAuthenticated, )

class FinsViewSet(viewsets.ModelViewSet):
	"""
	This viewset automatically provides `list` and `detail` actions.
	"""
	queryset = Fins.objects.all()
	serializer_class = FinsSerializer
	permission_classes = (permissions.IsAuthenticated, )

class RadiatorsViewSet(viewsets.ModelViewSet):
	"""
	This viewset automatically provides `list` and `detail` actions.
	"""
	queryset = Radiators.objects.all()
	serializer_class = RadiatorsSerializer
	permission_classes = (permissions.IsAuthenticated, )


class FactorViewSet(viewsets.ModelViewSet):
	"""
	This viewset automatically provides `list` and `detail` actions.
	"""
	queryset = Factor.objects.all()
	serializer_class = FactorSerializer
	permission_classes = (permissions.IsAuthenticated, )

class EddyViewSet(viewsets.ModelViewSet):
	"""
	This viewset automatically provides `list` and `detail` actions.
	"""
	queryset = Eddys.objects.all()
	serializer_class = EddySerializer
	permission_classes = (permissions.IsAuthenticated, )
