import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.utils.timezone import now

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Employee, Award, Leave, DailyActivity, Review_Performance, Mood
from .serializers import EmployeeDashboardSerializer, SignupSerializer, LoginSerializer, EmployeeSerializer

# Set up logging for debugging
logger = logging.getLogger(__name__)
@csrf_exempt
@api_view(['POST'])
def signup(request):
    print("Received signup request with data:", request.data)  # Debugging step

    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        employee = serializer.save()
        return Response(
            {'message': 'Signup successful', 'employee_id': employee.employee_id},
            status=status.HTTP_201_CREATED
        )

    print("Signup failed with errors:", serializer.errors)  # Debugging step
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_and_get_employee(request):
    logger.info("Login request received with data: %s", request.data)
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        logger.error("Login validation failed: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    employee = get_object_or_404(Employee, employee_id=serializer.validated_data['employee_id'])
    print(f"Employee password in DB: {employee.password}")
    if not employee.password:  # If it's None, raise an error
        return Response({'error': 'Password not set for this employee'}, status=status.HTTP_400_BAD_REQUEST)

    if not check_password(serializer.validated_data['password'], employee.password):
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['GET'])
def employee_dashboard(request, employee_id):
    logger.info("Fetching dashboard data for employee ID: %s", employee_id)

    try:
        employee = Employee.objects.get(employee_id=employee_id)
    except Employee.DoesNotExist:
        logger.error("Employee not found with ID: %s", employee_id)
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

    mood_history = list(employee.mood.values('Vibe_score', 'emotion_zone')) or [
        {"Vibe_score": 4, "emotion_zone": "Neutral Zone(OK)"}]
    
    activity = list(employee.daily_activities.values('date', 'meetings_attended', 'messages_sent')) or [
        {"date": now().date(), "meetings_attended": 1, "messages_sent": 5}]
    
    rewards = list(employee.awards.values('award_name', 'reward_points')) or [
        {"award_name": "Employee of the Month", "reward_points": 100}]
    
    daily_streak = [1, -1, 1, 1, 0, 0, 0]

    calendar = [{"event": "Team Meeting", "date": "2025-03-24"}, {"event": "Performance Review", "date": "2025-03-25"}]

    upcoming_tasks = [{"task": "Complete Survey", "due": "2025-03-23T18:00:00Z"}]

    data = {
        "mood_history": mood_history,
        "activity": activity,
        "rewards": rewards,
        "daily_streak": daily_streak,
        "calendar": calendar,
        "upcoming_tasks": upcoming_tasks,
    }

    logger.info("Dashboard data successfully fetched for employee ID: %s", employee_id)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def home(request):
    return JsonResponse({'message': 'Welcome to the MyOpenSoft API!'})