from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_json_api import renderers, parsers
from .serializers import AccountSerializer
from .forms import RegistrationForm
from django.contrib.auth.models import User
from .permissions import HasAccess
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
# from django.shortcuts import render

# Create your views here.
class AccountViewSet(viewsets.ModelViewSet):
	# queryset = User.objects.all()
	serializer_class = AccountSerializer
	# authentication_classes = (JSONWebTokenAuthentication,)
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	# renderer_classes = (renderers.JSONRenderer,)
	# parser_classes = (parsers.JSONParser,)

	def get_queryset(self):
		return User.objects.filter(id=self.request.user.id)

	# def get_object(self):
	# 	return self.request.user

	# def get_permissions(self):
	# 	return (AllowAny() if self.request.method == 'POST' 
	# 		else HasAccess()),

	@require_http_methods(["POST"])
	@csrf_exempt
	def register(request):
	    """
	    API endpoint to register a new user.
	    """
	    try:
	        payload = json.loads(request.body.decode('utf-8'))
	    except ValueError:
	        return JsonResponse({"error": "Unable to parse request body"}, status=400)

	    form = RegistrationForm(payload)

	    if form.is_valid():
	        user = User.objects.create_user(form.cleaned_data["username"],
	                                        form.cleaned_data["email"],
	                                        form.cleaned_data["password"])
	        user.save()

	        return JsonResponse({"success": "User registered."}, status=201)

	    return HttpResponse(form.errors.as_json(), status=400, content_type="application/json")

# class AccountEditSet(viewsets.ModelViewSet):
# 	authentication_classes = (JSONWebTokenAuthentication,)
# 	permission_classes = (IsAuthenticated,)

# 	def post(self, request):
# 		obj = User.objects.get(id=request.user.id)
# 		serializer = AccountEditSerializer(obj, data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)