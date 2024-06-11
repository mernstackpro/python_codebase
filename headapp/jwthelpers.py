from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from headapp.models import User


class TokenObtainPairView(APIView):
    def post(self,request):
        response = {'ok':False}
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            if username == None or password == None:
                response['details'] = 'fields_required_username_or_password'
                raise Exception('fields_required_username_or_password')
            if len(User.objects.filter(username=username)) != 1:
                response['details'] = 'user_not_found'
                raise Exception('user_not_found')
            user = authenticate(username=username,password=password)
            if user is not None :
                if user.role == 'request':
                    response['member'] = False
                    raise Exception('membership_request_pending')
                auth_tokens = get_tokens_for_user(user)
                for k,v in auth_tokens.items():response[k] = v
                response['ok'] = True
                response['lifetime'] = {'refresh':'365_days','access':'1_day'}
            else:response['details'] = 'password_not_valid'
        except Exception as e:print(e)
        return Response(response)
    

class TokenRefreshView(APIView):
    def post(self,request):
        response = {'ok':False}
        try:
            refresh_token = request.POST.get('refresh')
            if refresh_token is None:
                response['details'] = 'field_required_refresh'
                raise Exception('field_required_refresh')
            else:
                token_obj = RefreshToken(refresh_token)
                response['access'] = str(token_obj.access_token)
                response['ok'] = True
        except Exception as e:print(e)
        return Response(response)
    
    
class TokenVerifyView(APIView):
    def post(self,request):
        response = {'ok':False}
        if request.POST.get('token') is None:response['details'] = 'field_required_token'
        else:response['ok'] = verify_token(request.POST.get('token'))
        return Response(response) 



def verify_token(token:str)->bool:
    try:
        result = RefreshToken(token=token)
        return True
    except:
        try:
            result = AccessToken(token=token)
            return True
        except:
            return False
        
        
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }