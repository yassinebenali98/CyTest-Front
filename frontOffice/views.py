from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required



@login_required
def home_view(request):
    return render(request, 'frontOffice/dashboard.html')


class ExampleAPIView(APIView):
    def get(self, request):
        # Handle GET request and return a response
        data = {'message': 'This is a GET request'}
        return Response(data)

    def post(self, request):
        # Handle POST request and return a response
        data = {'message': 'This is a POST request'}
        return Response(data)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Use Django's login function to authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login the user and create a session
            login(request, user)
            return redirect('frontoffice:home')  # Replace 'home' with the URL name of your home page
        else:
            # Handle invalid credentials, display an error message, etc.
            pass
    
    return render(request, 'login.html')

def authenticate_with_defectdojo(username, password):
    base_url = 'http://127.0.0.1:9999/api/v2'
    login_url = base_url + '/api-token-auth/'

    payload = {
        'username': username,
        'password': password
    }

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    response = requests.post(login_url, json=payload, headers=headers)

    if response.status_code == 200:
        # Authentication successful
        token = response.json()['token']
        return True, token
    else:
        # Authentication failed
        return False, None
    
    
@login_required
def get_engagements(request):
    api_url = 'http://127.0.0.1:9999/api/v2/engagements/'
    token = request.session.get('token')  # Retrieve the token from the session using .get() method

    headers = {
        'Authorization': f'Token {token}'
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        engagements_data = response.json()
        return render(request, 'frontOffice/engagements.html', {'engagements': engagements_data['results']})
    else:
        error_message = "Failed to retrieve engagements."
        return render(request, 'error.html', {'error_message': error_message})