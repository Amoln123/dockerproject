from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerializer

from .models import UserToken,User
from .database import get_db
from sqlalchemy import and_
from rest_framework.exceptions import ValidationError
import bcrypt

import os
from django.conf import settings
import jwt
from datetime import datetime, timedelta
import pytz



from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer




SECRET_KEY = 'RBACPROJECT'  # Make sure to keep this secret

db_generator = get_db()
db = next(db_generator)

class creatUser(APIView):

    renderer_classes = [JSONRenderer]  # Force JSON response

    def get(self, request):
        print("=======request=========", request)
        users = db.query(User).all()
        serializer = UserSerializer(users, many=True)
        return Response({
            "status": 200,
            "message": "Success",
            "response": {"users": serializer.data}
        }, status=status.HTTP_200_OK)

    def post(self, request):
        print("======request======", request.data)  # Use request.data to access data in the request

        serializer = UserSerializer(data=request.data)  # Assuming you have a UserSerializer
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            mobile = serializer.validated_data['mobile']
            plain_password  = serializer.validated_data['password']
            # Add any additional fields as necessary
            hashed_password = hash_password(plain_password)
            # Create a new User instance
            user = User(
                username=username,
                email=email,
                mobile=mobile,
                password=hashed_password,  # Ensure to hash the password before saving in production
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            return Response({"status": 200, "message": "User created successfully"}, status=status.HTTP_201_CREATED)

        return Response({"status": 400, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        print("=====email===",email)
        print("====password====",password)

        # Validate the email and password
        try:
            user = db.query(User).filter(User.email == email).one_or_none()  # Adjust based on your User model and ORM

            print("=======user======",user)
            if user is None or not verify_password(password, user.password):  # Ensure you have a check_password function
                return Response({"status": 400, "message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

            token = create_token(user.id)
            # Define the IST timezone
            ist = pytz.timezone('Asia/Kolkata')    
            # Get the current time in IST
            current_time_ist = datetime.now(ist)    
            # Calculate expiration time in IST (24 hours from now)
            expiration_time_ist = current_time_ist + timedelta(days=1)

            # Check if a token already exists for the user
            existing_token = db.query(UserToken).filter(UserToken.user_id == user.id).one_or_none()

            if existing_token:
                # Update the existing token
                existing_token.token = token
                existing_token.expires_on = expiration_time_ist
                db.commit()
                db.refresh(existing_token)  # Refresh the object to get the latest state
                user_token = existing_token
            else:
                # Create a new UserToken instance
                user_token = UserToken(user_id=user.id, token=token,expires_on=expiration_time_ist)
                db.add(user_token)
                db.commit()
                db.refresh(user_token)  # Refresh the object to get the latest state

            # Create JWT token
            # refresh = RefreshToken.for_user(user)
            return Response({
                "status": 200,
                "message": "Login successful",
                "refresh": str(token),
                "access": str(token),
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"status": 500, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def hash_password(plain_password: str) -> str:
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Verify the provided password against the hashed password
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))



def create_token(user_id):
    # Define the IST timezone
    ist = pytz.timezone('Asia/Kolkata')    
    # Get the current time in IST
    current_time_ist = datetime.now(ist)    
    # Calculate expiration time in IST (24 hours from now)
    expiration_time_ist = current_time_ist + timedelta(days=1)
    print("==================",expiration_time_ist)
    payload = {
        'user_id': user_id,
        'exp': expiration_time_ist,  # Token expiration time
        'iat': datetime.utcnow()  # Issued at time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    print("=========token=======",token)
    return token


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from sqlalchemy.orm import sessionmaker
# from your_model_file import User  # Make sure to import your User model here
# from your_serializer_file import UserSerializer  # Make sure to import your UserSerializer here
# from your_database_connection import engine  # Import your SQLAlchemy engine

# # Create a session factory
# Session = sessionmaker(bind=engine)

# class UserCreateView(APIView):

#     def post(self, request):
#         print("======request======", request.data)  # Use request.data to access data in the request

#         serializer = UserSerializer(data=request.data)  # Assuming you have a UserSerializer
#         if serializer.is_valid():
#             username = serializer.validated_data['username']
#             email = serializer.validated_data['email']
#             mobile = serializer.validated_data['mobile']
#             password = serializer.validated_data['password']
#             # Add any additional fields as necessary

#             # Create a new User instance
#             user = User(
#                 username=username,
#                 email=email,
#                 mobile=mobile,
#                 password=password,  # Ensure to hash the password before saving in production
#             )

#             # Create a new session to interact with the database
#             with Session() as session:
#                 session.add(user)
#                 session.commit()
#                 session.refresh(user)  # Refresh the instance to get the latest data from the database

#             return Response({"status": 200, "message": "User created successfully"}, status=status.HTTP_201_CREATED)

#         return Response({"status": 400, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)





