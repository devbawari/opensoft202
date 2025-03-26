from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Employee, Award, Leave, DailyActivity, Review_Performance, Mood

class EmployeeSerializer(serializers.ModelSerializer):
    awards = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['employee_id', 'username', 'mentor_assigned', 'feedback_filled', 'awards']

    def get_awards(self, obj):
        return [{'id': award.id, 'award_name': award.award_name, 'reward_points': award.reward_points} for award in obj.awards.all()]

class SignupSerializer(serializers.Serializer):
    employee_id = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate_employee_id(self, value):
        if not Employee.objects.filter(employee_id=value).exists():
            raise serializers.ValidationError("Employee ID not found in the database.")
        return value

    def create(self, validated_data):
        employee = Employee.objects.get(employee_id=validated_data['employee_id'])
        if employee.username:
            raise serializers.ValidationError("Employee is already signed up.")

        # Hash password before saving
        employee.username = validated_data['username']
        employee.password = make_password(validated_data['password'])
        employee.save()
        return employee

class LoginSerializer(serializers.Serializer):
    employee_id = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        fields = ['Vibe_score', 'emotion_zone']

class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ['award_name', 'reward_points']

class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = ['start_date', 'end_date', 'no_of_leaves', 'leave_type']

class DailyActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyActivity
        fields = ['date', 'meetings_attended', 'messages_sent', 'hours_worked']

class ReviewPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review_Performance
        fields = ['performance_rating', 'manager_feedback', 'promotion_consideration', 'review_period']

class EmployeeDashboardSerializer(serializers.ModelSerializer):
    mood = MoodSerializer(many=True, read_only=True)
    awards = AwardSerializer(many=True, read_only=True)
    leaves = LeaveSerializer(many=True, read_only=True)
    daily_activities = DailyActivitySerializer(many=True, read_only=True)
    review_performance = ReviewPerformanceSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = ['employee_id', 'username', 'mentor_assigned', 'feedback_filled', 'mood', 'awards', 'leaves', 'daily_activities', 'review_performance']
