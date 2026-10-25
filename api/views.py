from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from product.models import Product

from .pagination import ProductPagination, UserPagination
from .serializers import ProductSerializer, UserSerializer


class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        print('list: listar productos')
        products = Product.objects.order_by('id')
        paginator = ProductPagination()
        page = paginator.paginate_queryset(products, request, view=self)
        serializer = ProductSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        print('create: crear producto', request.data)
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        print(f'retrieve: consultar producto {pk}')
        product = get_object_or_404(Product, pk=pk)
        return Response(ProductSerializer(product).data)

    def update(self, request, pk=None):
        print(f'update: actualizar producto {pk}', request.data)
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        print(f'partial_update: actualizar parte del producto {pk}', request.data)
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        print(f'destroy: borrar producto {pk}')
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by('id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = UserPagination
