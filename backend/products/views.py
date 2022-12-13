from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.mixins import (
  StaffEditorPermissionMixin,
  UserQuerySetMixin
)
from .models import Product
from .serializers import ProductSerializer

class ProductListCreateAPIView(
  # UserQuerySetMixin,
  StaffEditorPermissionMixin,
  generics.ListCreateAPIView
  ):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer

  def perform_create(self, serializer):
    title = serializer.validated_data.get('title')
    content = serializer.validated_data.get('content')
    email = serializer.validated_data.pop('email')
    if content is None:
      content = title
    serializer.save(user=self.request.user, content=content)

  # def get_queryset(self, *args, **kwargs):
  #   queryset = super().get_queryset(*args, **kwargs)
  #   request = self.request
  #   user = request.user
  #   if not user.is_authenticated:
  #     return Product.objects.none()
  #   # print(request.user)
  #   return queryset.filter(user=request.user)

product_list_create_view = ProductListCreateAPIView.as_view()

class ProductDetailAPIView(
  UserQuerySetMixin,
  StaffEditorPermissionMixin,
  generics.RetrieveAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer

product_detail_view = ProductDetailAPIView.as_view()

class ProductUpdateAPIView(
  UserQuerySetMixin,
  StaffEditorPermissionMixin,
  generics.UpdateAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  lookup_field = 'pk'

  def perform_update(self, serializer):
    instance = serializer.save()
    if not instance.content:
      instance.content = instance.title

product_update_view = ProductUpdateAPIView.as_view()

class ProductDeleteAPIView(
  UserQuerySetMixin,
  StaffEditorPermissionMixin,
  generics.DestroyAPIView):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  lookup_field = 'pk'

  def perform_destroy(self, instance):
    super().perform_destroy(instance)
product_destroy_view = ProductDeleteAPIView.as_view()

class ProductMixinView(
  mixins.ListModelMixin,
  mixins.RetrieveModelMixin,
  generics.GenericAPIView
):
  queryset = Product.objects.all()
  serializer_class = ProductSerializer
  lookup_field = 'pk'

  def get(self, request, *args, **kwargs):
    pk = kwargs.get("pk")
    if pk is not None:
      return self.retrieve(request, *args, **kwargs)
    return self.list(request, *args, **kwargs)


product_mixin_view = ProductMixinView.as_view()

@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
  method = request.method
  
  if method == "GET":
    if pk is not None:
      obj = get_object_or_404(Product, pk=pk)
      data = ProductSerializer(obj, many=False).data
      return Response(data)

    # List view
    queryset = Product.objects.all()
    data = ProductSerializer(queryset, many=True).data
    return Response(data)
  
  if method == "POST":
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      title = serializer.validated_data.get('title')
      content = serializer.validated_data.get('content')
      None
      if content is None:
        content = title
      serializer.save(content=content)
      return Response(serializer.data)
  return Response({"Invalid": "Not good data"}, status=400)