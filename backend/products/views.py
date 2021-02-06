from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *


class ProductView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializerResponse(products, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        product = request.data.get('product')
        serializer = ProductSerializerPostRequest(data=product)
        product_saved = None
        if serializer.is_valid(raise_exception=True):
            product_saved = serializer.save()
        newProduct = Product.objects.get(pk=product_saved.pk)
        response = ProductSerializerResponse(newProduct)
        return Response(response.data)

    def put(self, request, pk):
        saved_product = get_object_or_404(Product.objects.all(), pk=pk)
        data = request.data.get('product')
        serializer = ProductSerializerPostRequest(instance=saved_product, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_product = serializer.save()
        newProduct = Product.objects.get(pk=saved_product.pk)
        response = ProductSerializerResponse(newProduct)
        return Response(response.data)

    def delete(self, request, pk):
        product = get_object_or_404(Product.objects.all(), pk=pk)
        product.delete()
        response = ProductSerializerResponse(product)
        return Response(response.data, status=204)
# {
# "product": {
#             "name": "product123",
#             "price": 10000123,
#             "description": "product1233 is awesome"
#         }
# }
