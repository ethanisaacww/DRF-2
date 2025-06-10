from django.shortcuts import render
from django.db import connection
from django.db import transaction
from django.db.models import Q
from .models import Product
from .serializer import ProductSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics, mixins, viewsets
from .object import Message
# Create your views here.

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def listproducts(request):
    query = Product.objects.all()
    serializer_class = ProductSerializer(query, many=True)
    context = {
        'serializer_class_data': serializer_class.data
    }
    return Response(serializer_class.data)
    # return render(request, 'product/list_products.html', {'products': })

@api_view(['GET','POST'])
def listmessages(request):
    message_obj = Message('ethan.wei@stratiphy.io', 'heehee')
    serializer_class = MessageSerializer(message_obj)
    return Response(serializer_class.data)

class ListProducts(APIView):

    def get(self, request):
        query = Product.objects.all()
        serializer_class = ProductSerializer(query, many=True)
        return Response(serializer_class.data)
    
    def post(self, request):
        serializer_obj = ProductSerializer(data=request.data)
        if serializer_obj.is_valid():
            product_saved = serializer_obj.save()
            return Response({"Success": "Product '{}' created successfully".format(product_saved.name)}, status=201)
        return Response(serializer_obj.errors, status=400)
        
class ProductDetailedView(APIView):

    def get(self, request, pid):
        product = Product.objects.filter(product_id=pid)
        serializer_class = ProductSerializer(product, many=True)
        return Response(serializer_class.data)
    
    def put(self, request, pid):
        product_obj = Product.objects.get(product_id=pid)
        serializer_obj = ProductSerializer(product_obj, data=request.data)
        if serializer_obj.is_valid():
            product_saved = serializer_obj.save()
            return Response({"Success": "Product '{}' updated successfully".format(product_saved.name)}, status=201)
        return Response(serializer_obj.errors, status=400)
    
    def delete(self, request, pid):
        product_obj = Product.objects.get(product_id=pid).delete()
        return Response({"Success": "Product '{}' deleted successfully".format(pid)}, status=200)
    
class ListProductsMixins(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class DetailedProductMixins(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.CreateModelMixin,
                            mixins.DestroyModelMixin,
                            generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
class ListProductsGeneric(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class DetailProductsGeneric(generics.RetrieveAPIView,
                            generics.UpdateAPIView,
                            generics.DestroyAPIView,):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class SpecialProductsGeneric(generics.ListCreateAPIView,
                             generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

### ORM ###

def product_list_(request):
    products = Product.objects.all()
    print(products)
    print(products.query)
    print(connection.queries)
    return render(request, 'output.html', {'products': products})

# or statement
def product_list_or(request):
    products = Product.objects.filter(~Q(name__startswith='iPhone') | Q(name__endswith='discounted') | Q(name__startswith='Pixel'))
    print(products)
    print(connection.queries)
    return render(request, 'output.html', {'products': products})

# and statement
def product_list_and(request):
    products = Product.objects.filter(product_id=1212) & Product.objects.filter(price=1099.99)
    print(products)
    print(connection.queries)
    return render(request, 'output.html', {'products': products})

def product_list(request):
    products = Product.objects.filter(Q(product_id=1212) & Q(price=1099.99))
    print(products)
    print(connection.queries)
    return render(request, 'output.html', {'products': products})

# def discount_products(request):
#     google = Product.objects.select_for_update().get(category=1)
#     apple = Product.objects.select_for_update().get(category=2)

#     # atomicity - execute commits at the same time, after making sure none fail
#     with transaction.atomic():
#         for product in google:
#             product.price = product.price * 0.9
#             product.save()
#         for product in apple:
#             product.price = product.price * 0.8
#             product.save()
#     return render(request, 'output.html', {'products': google | apple})