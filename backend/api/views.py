import json
# from django.http import JsonResponse, HttpResponse
from django.forms.models import model_to_dict

from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.models import Product
from products.serializers import ProductSerializer

@api_view(["POST"])
def api_home(request, *args, **kwargs):
  data = request.data
  serializer = ProductSerializer(data=request.data)
  if serializer.is_valid(raise_exception=True):
    return Response(serializer.data)
  return Response({"Invalid": "Not good data"}, status=400)
