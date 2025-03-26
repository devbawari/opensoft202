import logging
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from django.utils.timezone import now
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Employee, Award, DailyActivity, Mood
from .serializers import (
    EmployeeDashboardSerializer, SignupSerializer, LoginSerializer
)

# Setup logging
logger = logging.getLogger(__name__)

@api_view(['POST'])
def signup(request):
    logger.info("Received signup request with data: %s", request.data)
    
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        employee = serializer.save()
        return Response(
            {'message': 'Signup successful', 'employee_id': employee.employee_id},
            status=status.HTTP_201_CREATED
        )
    
    logger.error("Signup failed: %s", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_and_get_employee(request):
    logger.info("Login request received with data: %s", request.data)
    
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        logger.error("Login validation failed: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    employee = get_object_or_404(Employee, employee_id=serializer.validated_data['employee_id'])
    
    if not check_password(serializer.validated_data['password'], employee.password):
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def employee_dashboard(request, employee_id):
    logger.info("Fetching dashboard data for employee ID: %s", employee_id)

    employee = get_object_or_404(Employee, employee_id=employee_id)

    mood_history = list(Mood.objects.filter(employee=employee).values('Vibe_score', 'emotion_zone')) or [
        {"Vibe_score": 4, "emotion_zone": "Neutral Zone(OK)"}]
    
    activity = list(DailyActivity.objects.filter(employee=employee).values('date', 'meetings_attended', 'messages_sent')) or [
        {"date": now().isoformat(), "meetings_attended": 1, "messages_sent": 5}]
    
    rewards = list(Award.objects.filter(employee=employee).values('award_name', 'reward_points')) or [
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
