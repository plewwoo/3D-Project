from datetime import datetime, timezone, timedelta
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from backend.settings import MEDIA_ROOT
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, APIView
from rest_framework import status
import os
import sys
import jwt


class Token():

    def __init__(self):
        pass

    def get(self, username, password, expires, secret_key, app_id):
        result = {'success': False, 'message': None, 'data': None}
        try:
            user = authenticate(username=username, password=password)
            if user != None:
                encoded_data = {
                    'username': username,
                    'password': password,
                    'exp': expires,
                    'app_id': app_id
                }
                encoded_jwt = jwt.encode(
                    encoded_data, secret_key,  algorithm="HS256")
                result['success'] = True
                result['message'] = 'Get Token Success'
                result['data'] = {
                    'user_id': user.id,
                    'access_token': encoded_jwt,
                    'token_type': "Bearer",
                    'expires': expires,
                    'refresh_token': encoded_jwt,
                }
            else:
                result['message'] = 'Get Token Failed'
                result['data'] = 'invalid username or password'
        except Exception as ex:
            result['message'] = str(ex)

        return result

    def decode(self, token, expires, secret_key, app_id):
        result = {'success': False, 'message': None, 'data': None}
        try:
            decoded_jwt = jwt.decode(
                token, secret_key, algorithms="HS256")
            user = authenticate(
                username=decoded_jwt['username'], password=decoded_jwt['password'])
            if user != None:
                result['success'] = True
                result['message'] = 'Get Token Success'
                result['data'] = {
                    'user_id': user.id,
                    'access_token': token,
                    'token_type': "Bearer",
                    'expires': expires,
                    'refresh_token': token,
                }
            else:
                result['message'] = 'Get Token Failed'
                result['data'] = 'invalid username or password'
        except Exception as ex:
            print(ex)
            result['message'] = str(ex)

        return result


class Register(APIView):

    @staticmethod
    def get(request, *args, **kwargs):

        result = []

        user = User.objects.all()

        for u in user:
            result.append({
                'username': u.username,
                'password': u.password,
                'first_name': u.first_name,
                'last_name': u.last_name
            })

        return Response(result, status=status.HTTP_200_OK)

    @staticmethod
    def post(request, *args, **kwargs):

        result = {}
        http_status = None

        data = {
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'tel': request.data.get('tel'),
            'email': request.data.get('email'),
            'profile_pic': request.data.get('profile_pic'),
        }

        print(data)

        try:
            check_username = User.objects.filter(username=data['username'])
            if len(check_username) < 1:
                user = User()
                user.username = data['username']
                user.email = data['email']
                user.first_name = data['first_name']
                user.last_name = data['last_name']
                user.set_password(data['password'])
                user.save()

                profile = Profile()
                profile.user = User.objects.get(username=data['username'])
                profile.tel = data['tel']
                profile.save()

                result['success'] = True
                result['message'] = 'Register Success'
                result['data'] = {
                    'username': user.username,
                    'password': user.password,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
                http_status = status.HTTP_201_CREATED
            else:
                result['success'] = False
                result['message'] = 'Register Failed'
                result['data'] = "Found existing username, Please use new username"

                http_status = status.HTTP_302_FOUND

        except Exception as e:
            print(e)
            result['success'] = False
            result['message'] = 'Register Failed'
            result['data'] = str(e)
            http_status = status.HTTP_400_BAD_REQUEST

        return Response(result, status=http_status)


class Login(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        result = {}
        http_status = None

        data = {
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'expires': datetime.now(tz=timezone.utc) + timedelta(days=30),
            'secret_key': '0B8u9eVwsB',
            'app_id': '3DApp'
        }

        try:
            token_result = Token.get(
                request, data['username'], data['password'], data['expires'], data['secret_key'], data['app_id'])
            if token_result['success'] == True:
                result['success'] = True
                result['message'] = 'Login Success'
                result['data'] = {
                    'user_id': token_result['data']['user_id'],
                    'token_type': token_result['data']['token_type'],
                    'expires': token_result['data']['expires'],
                    'access_token': token_result['data']['access_token'],
                    'refresh_token': token_result['data']['refresh_token'],
                }
                http_status = status.HTTP_200_OK
            else:
                result['success'] = False
                result['message'] = 'Login Failed'
                result['data'] = "Not found existing user, Please try again"
                http_status = status.HTTP_401_UNAUTHORIZED
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(e)
            result['success'] = False
            result['message'] = 'Login Failed'
            result['data'] = str(e)
            http_status = status.HTTP_400_BAD_REQUEST

        return Response(result, status=http_status)


class CheckLogin(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        result = {}
        http_status = None

        data = {
            'user_id': request.data.get('user_id'),
            'token': request.data.get('token'),
            'expires': request.data.get('expires'),
            'secret_key': '0B8u9eVwsB',
            'app_id': '3DApp'
        }

        try:
            token_result = Token.decode(
                request, data['token'], data['expires'], data['secret_key'], data['app_id'])
            if token_result['success'] == True:
                result['success'] = True
                result['message'] = 'Login Success'
                result['data'] = {
                    'user_id': token_result['data']['user_id'],
                    'token_type': token_result['data']['token_type'],
                    'expires': token_result['data']['expires'],
                    'access_token': token_result['data']['access_token'],
                    'refresh_token': token_result['data']['refresh_token'],
                }
                http_status = status.HTTP_200_OK
            else:
                result['success'] = False
                result['message'] = 'Login Failed'
                result['data'] = "Not found existing user, Please try again"
                http_status = status.HTTP_401_UNAUTHORIZED
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(e)
            result['success'] = False
            result['message'] = 'Login Failed'
            result['data'] = str(e)
            http_status = status.HTTP_400_BAD_REQUEST

        return Response(result, status=http_status)


class UserProfile(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        try:
            result = {}
            user_id = kwargs.get('id', None)
            user = User.objects.get(id=user_id)
            if user != None:
                print(user)
                result['success'] = True
                result['message'] = 'Get user data success'
                result['data'] = {
                    'user_id': user.id,
                    'username': user.username
                }
            else:
                result['success'] = False
                result['message'] = 'Get user data failed'
                result['data'] = 'failed to get user data'

        except Exception as e:
            print(e)
            result['success'] = False
            result['message'] = 'Get user data failed'
            result['data'] = 'failed to get user data'

        return Response(result, status=status.HTTP_200_OK)


class UploadFile(APIView):

    def get(request, *args, **kwargs):
        result = {'success': True, 'message': ''}

        user_id = kwargs.get('id', None)

        model_list = []
        model = Models.objects.filter(user=user_id).order_by('-id')

        for m in model:
            model_list.append({
                'id': m.id,
                'name': m.name,
                'url': f'{m.model.url}.{m.extension}',
                'updated': m.upload_date
            })
        result['results'] = model_list
        http_status = status.HTTP_200_OK

        return Response(result, status=http_status)

    @staticmethod
    def post(request, *args, **kwargs):
        result = {'success': True, 'message': ''}

        data = {
            'user_id': request.data.get('user_id'),
            'file': request.FILES['file'],
            'file_name': request.data.get('file_name'),
        }

        http_status = status.HTTP_400_BAD_REQUEST

        try:
            if str(data['file_name']).split(".")[1] == 'glb':
                models = Models()
                models.user = User.objects.get(id=data['user_id'])
                models.name = str(data['file_name']).split(".")[0]
                models.model = request.FILES['file']
                models.extension = str(data['file_name']).split(".")[1]
                models.save()

                result['results'] = {
                    'id': models.id,
                    'name': str(data['file_name']).split(".")[0],
                    'url': f'{models.model.url}.{models.extension}',
                    'updated': models.upload_date
                }
                result['message'] = 'Upload File Success !!'

                http_status = status.HTTP_201_CREATED
            else:
                result['success'] = False
                result['message'] = 'File must be .glb'

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(e)
            result['success'] = False
            result['message'] = 'Login Failed'
            result['data'] = str(e)
            http_status = status.HTTP_400_BAD_REQUEST

        return Response(result, status=http_status)
