from django.shortcuts import render
from django.contrib.auth import authenticate


from .models import Formation , Profile,Subscribe
from .serializers import FormationSerializer,ProfileSerializer,SubscribeSerializer

from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated


from rest_framework_simplejwt.tokens import RefreshToken






@api_view(['POST','GET'])
def get_Formations(request):
    #GET 
    if request.method == 'GET':
        formations = Formation.objects.all()
        serializer = FormationSerializer(formations,many=True)
        return Response(serializer.data)
    #POST
    if request.method == 'POST':
        serializer = FormationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.data, status= status.HTTP_400_BAD_REQUEST)



@api_view(['GET','PUT','DELETE'])
def get_Formation(request, id):
    
    try:
        formation = Formation.objects.get(pk=id)
    except Formation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # GET
    if request.method == 'GET':
        serializer = FormationSerializer(formation)
        return Response(serializer.data)
        
    # PUT
    elif request.method == 'PUT':
        serializer = FormationSerializer(formation, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    # DELETE
    if request.method == 'DELETE':
        formation.delete()
        


@api_view(['POST'])
def register_view(request):
    if request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = RefreshToken.for_user(user)
            return Response({
                'id':user.id,
                'refresh': str(tokens),
                'access': str(tokens.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    



@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(email=email, password=password)
        
        if user:
            tokens = RefreshToken.for_user(user)
            return Response({
                'id':user.id,
                'refresh': str(tokens),
                'access': str(tokens.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscribe(request, id):
    try:
        formation = Formation.objects.get(id=id)
        profile = Profile.objects.get(id=request.user.id)
        
        subscription, created = Subscribe.objects.get_or_create(formation=formation, profile=profile)
        
        if not created:
            return Response({'message': 'Already subscribed to this formation.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': 'Successfully subscribed to the formation.'}, status=status.HTTP_200_OK)
    except Formation.DoesNotExist:
        return Response({'message': 'Formation does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    except Profile.DoesNotExist:
        return Response({'message': 'Profile does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_formations(request):
    subscribes = Subscribe.objects.filter(profile = request.user.id)
    serializer = SubscribeSerializer(subscribes , many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def undo_subscribtion(request,id):
    try:
        subscribe = Subscribe.objects.get(pk=id)
        subscribe.delete()
        return Response("Deleted",status=status.HTTP_200_OK)
    except Subscribe.DoesNotExist:
        return Response({'message': 'Subscribtion does not exist.'}, status=status.HTTP_404_NOT_FOUND)
