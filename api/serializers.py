from rest_framework import serializers
from .models import Formation,Profile,Subscribe

class FormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formation
        fields = '__all__'




class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name' ,'last_name' ,'email', 'password', 'numero_tel', 'address', 'niveau']  
        extra_kwargs = {
            'password': {'write_only': True},  
        }

    def create(self, validated_data):
        user = Profile.objects.create_user(**validated_data)
        return user
    

class SubscribeSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source = "formation.title" , read_only=True)
    localisation = serializers.CharField(source = "formation.localisation" , read_only=True)

    class Meta : 
        model = Subscribe 
        fields = ['id','profile','title','confirmed','localisation']