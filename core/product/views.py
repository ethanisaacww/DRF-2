from django.shortcuts import render
from .models import Product
from .serializer import ProductSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
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
    
class ProductDetailedView(APIView):

    def get(self, request, pid):
        product = Product.objects.filter(product_id=pid)
        serializer_class = ProductSerializer(product)
        return Response(serializer_class.data)