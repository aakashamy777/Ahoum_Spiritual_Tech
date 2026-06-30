import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit

class GoogleAuthView(APIView):
    permission_classes = [AllowAny]
    
    @method_decorator(ratelimit(key='ip', rate='5/m', block=True))
    def post(self, request):
        code = request.data.get('code')
        redirect_uri = request.data.get('redirect_uri')
        if not code:
            return Response({'error': 'No code provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            'code': code,
            'client_id': os.environ.get('GOOGLE_CLIENT_ID', ''),
            'client_secret': os.environ.get('GOOGLE_CLIENT_SECRET', ''),
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }
        res = requests.post(token_url, data=data)
        if res.status_code != 200:
            return Response({'error': 'Failed to exchange code for token', 'details': res.json()}, status=status.HTTP_400_BAD_REQUEST)
        
        token = res.json().get('access_token')
        
        # Verify token with Google
        response = requests.get(f'https://www.googleapis.com/oauth2/v3/userinfo?access_token={token}')
        if response.status_code != 200:
            return Response({'error': 'Invalid Google token'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_info = response.json()
        email = user_info.get('email')
        
        if not email:
            return Response({'error': 'Email not found in token'}, status=status.HTTP_400_BAD_REQUEST)
            
        user, created = User.objects.get_or_create(email=email, defaults={
            'username': email.split('@')[0],
            'first_name': user_info.get('given_name', ''),
            'last_name': user_info.get('family_name', ''),
            'avatar': user_info.get('picture', '')
        })
        
        tokens = get_tokens_for_user(user)
        return Response({
            **tokens,
            'user': UserSerializer(user).data
        })

class GithubAuthView(APIView):
    permission_classes = [AllowAny]
    
    @method_decorator(ratelimit(key='ip', rate='5/m', block=True))
    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response({'error': 'No code provided'}, status=status.HTTP_400_BAD_REQUEST)
            
        token_url = "https://github.com/login/oauth/access_token"
        data = {
            'client_id': os.environ.get('GITHUB_CLIENT_ID', ''),
            'client_secret': os.environ.get('GITHUB_CLIENT_SECRET', ''),
            'code': code
        }
        headers = {'Accept': 'application/json'}
        res = requests.post(token_url, data=data, headers=headers)
        if res.status_code != 200:
            return Response({'error': 'Failed to exchange code'}, status=status.HTTP_400_BAD_REQUEST)
            
        token = res.json().get('access_token')
        if not token:
            return Response({'error': 'Failed to get access token from Github', 'details': res.json()}, status=status.HTTP_400_BAD_REQUEST)
            
        headers = {'Authorization': f'token {token}'}
        response = requests.get('https://api.github.com/user', headers=headers)
        if response.status_code != 200:
            return Response({'error': 'Invalid Github token'}, status=status.HTTP_400_BAD_REQUEST)
            
        user_info = response.json()
        email = user_info.get('email')
        
        if not email:
            # GitHub email might be private, need to fetch from emails endpoint
            email_resp = requests.get('https://api.github.com/user/emails', headers=headers)
            if email_resp.status_code == 200:
                emails = email_resp.json()
                primary = next((e for e in emails if e.get('primary')), None)
                if primary:
                    email = primary.get('email')
                    
        if not email:
            return Response({'error': 'Could not get email from GitHub'}, status=status.HTTP_400_BAD_REQUEST)
            
        user, created = User.objects.get_or_create(email=email, defaults={
            'username': user_info.get('login', email.split('@')[0]),
            'first_name': user_info.get('name', '').split(' ')[0] if user_info.get('name') else '',
            'avatar': user_info.get('avatar_url', '')
        })
        
        tokens = get_tokens_for_user(user)
        return Response({
            **tokens,
            'user': UserSerializer(user).data
        })

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
        
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
