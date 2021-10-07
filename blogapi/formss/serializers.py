from datetime import datetime
from django.contrib.auth.models import User, Group

from rest_framework import serializers

from .models import Blog, Blogs, Person, PersonDetails

class BlogSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField()
    blog = serializers.CharField()

    def create(self, validated_data):
        print("Creating blog", validated_data)
        return Blog.objects.create(**validated_data)



class UsersSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, required=True)

    def create(self, validated_data, password):
        print("Creating User")
        validated_data['is_staff']=True
        
        print('Serializers create data', validated_data, )
        user = User.objects.create_user(password=password, **validated_data)
        user.groups.set(Group.objects.all())
        print(user.id)
        
        return user


def positive_number(value):
    if value < 0:
        raise serializers.ValidationError('Negative age not possible.')

class DetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    gender = serializers.ChoiceField(choices=[('m', 'Male'), ('f', 'Female')])
    age = serializers.IntegerField(validators=[positive_number])
    dob = serializers.DateField()

    def create(self, validated_data):
        print(validated_data)
        validated_data['dob'] = validated_data['dob'].strftime('%Y-%m-%d')
        return PersonDetails.objects.create(**validated_data)


class PersonSerializer(serializers.Serializer):
    person = UsersSerializer()
    detail = DetailSerializer()

    class Meta:
        model = Person
        fields = ['person',  'detail', 'url']
    
    def create(self, validated_data):
        person=Person.objects.create(
            person=User.objects.get(id=validated_data['person']['id']), 
            detail=PersonDetails.objects.get(id=validated_data['detail']['id']))
        return person

class BlogsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    blog = BlogSerializer()
    person = PersonSerializer()

    class Meta:
        model = Blogs
        fields = ['id', 'blog', 'blog','person', '_date_created']


    def create(self, validated_data):
        print(validated_data)
        return Blogs.objects.create(
            blog=Blog.objects.get(id=validated_data['blog']),
            person=Person.objects.get(person__id=validated_data['person'])
        )._blog()
