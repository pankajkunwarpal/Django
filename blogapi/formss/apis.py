from django.core.exceptions import ObjectDoesNotExist
from django.db.models import query
from rest_framework import viewsets
from rest_framework.serializers import Serializer
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.authtoken.models import Token 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.status import HTTP_404_NOT_FOUND

from .models import Person, PersonDetails, Blog, Blogs
from .serializers import BlogsSerializer, BlogSerializer, PersonSerializer, UsersSerializer, DetailSerializer

from django.contrib.auth.models import User

# API classes

class BlogSerializerView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        print(request.data)
        try:
            post = BlogSerializer(data=request.data)
            if post.is_valid():
                dt = post.create(post.data)
            return Response(BlogSerializer(dt).data) 
        
        except Exception:
            return Response({ 'error': post.errors })

    def get(self, request, format=None):
            return Response(BlogSerializer(Blog.objects.all(), many=True).data)



class BlogsSerializerView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
  
    def get(self, request, format=None):
        print(request.COOKIES, request.user)
        # print(request.META)
        try:
            blogs = BlogsSerializer(Blogs.objects.filter(
                person__person=User.objects.get(username=request.user.username)
                ), many=True
            )
        except ObjectDoesNotExist:
            return Response({"Message": "User blogs doesn't exist"}, status=HTTP_404_NOT_FOUND)
        return Response(blogs.data)

    def post(self, request, format=None):
        print(request.data)
        try:
            Blog.objects.get(id=request.data['blog'])
            try:
                Person.objects.get(person__id=request.data['person'])
            except ObjectDoesNotExist:
                print("Error",  'Person doesn\'t exist')
                return Response({'error': "person with ID you provided does not exist."})
        except ObjectDoesNotExist:
            print("Error Blog does not exist.")
            return Response({'error': "blog with prvided id doesnot exist."})

        return Response(BlogsSerializer().create(request.data))


class PersonSerializerView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        print(request.user)
        try:
            person = PersonSerializer(
                {'person': User.objects.get(username=request.user.username), 
                'detail':PersonDetails.objects.get(id=Person.objects.get(person__username=request.user).detail.id)
                }
            )
        except ObjectDoesNotExist:
            return Response({'message': 'Person details not exist', 'error': PersonSerializer.errors}, status=HTTP_404_NOT_FOUND)

        return Response(person.data)

    def post(self, request, format=None):
        print("INSIDE POST")
        try:
            print(request.data, User.objects.get(id=request.data['person']), PersonDetails.objects.get(id=request.data['detail']))
            try:
                person = UsersSerializer(User.objects.get(id=request.data['person']))
                print(person.data)
            except User.DoesNotExist:
                return Response(person.errors)
            try:
                detail = DetailSerializer(PersonDetails.objects.get(id=request.data['detail']))
                print(detail.data)
            except PersonDetails.DoesNotExist:
                return Response(detail.errors)

            serializer = PersonSerializer(data={
                'person': person.data, 'detail': detail.data
            })
            serializer.initial_data['person']['password'] = "aszx"
            print(serializer.initial_data)

            print('Checking serializer')
            if serializer.is_valid():
                print('Validating person details')
                serializer.create(serializer.initial_data)
                print(serializer.data)
                return Response(serializer.data)
            return Response(serializer.errors)

        except User.DoesNotExist or PersonDetails.DoesNotExist:
            return Response({'error': serializer.errors})
    



class UserSerializerView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        print(request.user, request.user.id, request.data)
        try:
            serializer = UsersSerializer(User.objects.get(id=request.user.id))
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'message': 'User doesn\'t exist'})

    def delete(self,request, id=None):
        
        if id:
            try:
                User.objects.filter(id=request.user.id).delete()
                return Response({"message": 'User delete successful'})
                
            except User.DoesNotExist:
                return Response({'message': 'User doesn\'t exist'})


class CreateUserSerializerView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        print(request.data)
        serializer = UsersSerializer(data=request.data)
        print(serializer.is_valid(), )
        if serializer.is_valid():
            dt = serializer.create(serializer.data, request.data['password'])
            print(serializer.data)
            return Response(UsersSerializer(dt).data)        
        
        else:
            return Response({"message": 'Something went wrong'})

                

class PersonDetailSerializerView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def post(self, request, format=None):

        print(request.data)
        serializer = DetailSerializer(data=request.data)
        if serializer.is_valid():
            
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)        
        
        else:
            return Response({"message": 'Something went wrong', 'errors': serializer.errors})


    def get(self, request, format=None, id=None):
        print(id, request.data)
        try:
            serializer = DetailSerializer(PersonDetails.objects.get(id=request.data['id']))
            print(serializer.data)
            return Response(serializer.data)    
        except PersonDetails.DoesNotExist:
            return Response({'message': 'Details for this id does not exist.'})

    def delete(self, request, format=None):
        try:
            PersonDetails.objects.get(id=request.data['id']).delete()
            return Response({"message": "User detail deleted successfully."})
        except PersonDetails.DoesNotExist:
            return Response({"message": "User Detail with this id doesn't exist."})
        except Exception:
            return Response({'message': 'an error occured id field may not be provided.'})
        


#  For AuthToken 
# class AuthToken(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         print(created, token)
        
#         response = Response({
#             'Token': token.key,
#             'user_id': user.pk,
#             'email': user.email,
#             'date': token.created
#         })
#         response.set_cookie(key='Token', value=token.key)
#         return response