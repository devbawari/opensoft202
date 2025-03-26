import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from .models import Employee
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Employee, Award, Leave, DailyActivity, Review_Performance, Mood
from .serializers import EmployeeDashboardSerializer,SignupSerializer, LoginSerializer,EmployeeSerializer
from django.utils.timezone import now
from rest_framework import status

@csrf_exempt  # Remove in production
@api_view(['POST'])
def signup(request):
    print(request.data)  # Debug
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        employee = serializer.save()
        return Response({'message': 'Signup successful', 'employee_id': employee.employee_id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_and_get_employee(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    employee = get_object_or_404(Employee, employee_id=serializer.validated_data['employee_id'])
    
    if not check_password(serializer.validated_data['password'], employee.password):
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    # Serialize employee data
    employee_data = EmployeeSerializer(employee).data
    return Response(employee_data)
@api_view(['GET'])
def employee_dashboard(request, employee_id):
    try:
        employee = Employee.objects.get(employee_id=employee_id)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=404)

    # Fetch mood history (Dummy if not available)
    mood_history = list(employee.mood.values('Vibe_score', 'emotion_zone')) or [
        {"Vibe_score": 4, "emotion_zone": "Neutral Zone(OK)"}]
    
    # Fetch activities (Dummy if not available)
    activity = list(employee.daily_activities.values('date', 'meetings_attended', 'messages_sent')) or [
        {"date": now().date(), "meetings_attended": 1, "messages_sent": 5}]
    
    # Fetch rewards (Dummy if not available)
    rewards = list(employee.awards.values('award_name', 'reward_points')) or [
        {"award_name": "Employee of the Month", "reward_points": 100}]
    
    # Fetch daily streak (Static for now)
    daily_streak = [1, -1, 1, 1, 0, 0, 0]
    
    # Fetch calendar events (Dummy if not available)
    calendar = [{"event": "Team Meeting", "date": "2025-03-24"}, {"event": "Performance Review", "date": "2025-03-25"}]

    # Fetch upcoming tasks (Dummy if not available)
    upcoming_tasks = [{"task": "Complete Survey", "due": "2025-03-23T18:00:00Z"}]

    data = {
        "mood_history": mood_history,
        "activity": activity,
        "rewards": rewards,
        "daily_streak": daily_streak,
        "calendar": calendar,
        "upcoming_tasks": upcoming_tasks,
    }

    return Response(data)
