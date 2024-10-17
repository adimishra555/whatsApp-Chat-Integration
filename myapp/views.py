# views.py
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Profile  
from .signals import send_whatsapp_message  

@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    phone_number = request.data.get('phone_number')

    if not username or not password or not phone_number:
        return Response({'error': 'Username, password, and phone number are required.', 'status': 'Error'})

    user, created = User.objects.get_or_create(username=username, defaults={'password': password})
    if created:
        Profile.objects.create(user=user, phone_number=phone_number)
    else:
        user.set_password(password)
        user.profile.phone_number = phone_number
        user.profile.save()
        user.save()

    send_whatsapp_message(
        phone_number=phone_number,
        message=f"Your account is successfully created. Now you can chat with us and provide more information about , {username}."
    )

    return Response({'message': 'User registered successfully.', 'status': True})

@api_view(['POST'])
def upload_product(request):
    user = request.user
    product_name = request.data.get('name')
    product_description = request.data.get('description')
    
    if not product_name or not product_description:
        return Response({'error': 'Product name and description are required.', 'status': 'Error'})
    
    product = Product.objects.create(user=user, name=product_name, description=product_description)
    return Response({'message': 'Product uploaded successfully.','status': True})
