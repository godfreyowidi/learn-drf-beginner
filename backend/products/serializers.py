from rest_framework import serializers
from rest_framework.reverse import reverse
from api.serializers import UserPublicSerializer
from .models import Product
from . import validators


class ProductInlineSerializer(serializers.Serializer):
  url = serializers.HyperlinkedIdentityField(
    view_name='product_detail',
    lookup_field='pk',
    read_only=True
  )
  title = serializers.CharField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
  owner = UserPublicSerializer(source='user', read_only=True)
  edit_url = serializers.SerializerMethodField(read_only=True)
  url = serializers.HyperlinkedIdentityField(
    view_name='product_detail',
    lookup_field='pk'
  )
  title = serializers.CharField(validators=[validators.validate_title_no_hello, validators.unique_product_title])
  body = serializers.CharField(source='content')
  class Meta:
    model = Product
    fields = [
      'owner',
      'edit_url',
      'url',
      'pk',
      'title',
      'body',
      'price',
      'sale_price',
      'public',
      'path'
  ]

  def create(self, validated_data):
    # email = validated_data.pop('email')
    obj = super().create(validated_data)
    # print(email, obj)
    return obj

  def get_edit_url(self, obj):
    request = self.context.get('request')
    if request is None:
      return None
    return reverse("product_edit", kwargs={"pk": obj.pk}, request=request)

  def get_my_discount(self, obj):
    if not hasattr(obj, 'id'):
      return None
    if not isinstance(obj, Product):
      return None
    return obj.get_discount()