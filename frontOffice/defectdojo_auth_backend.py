from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from . import views

UserModel = get_user_model()

class DefectDojoAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Authenticate with DefectDojo API
        login_success, token = views.authenticate_with_defectdojo(username, password)
        
        if login_success:
            # Check if the user already exists in the database
            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                # Create a new user if the user does not exist
                user = UserModel.objects.create_user(username=username, password=password)
            
            # Return the user object to indicate successful authentication
            return user
        
        # Return None if authentication fails
        return None

    def get_user(self, user_id):
        try:
            # Retrieve the user object based on user_id
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            # Return None if user_id does not exist
            return None
        
        return user
