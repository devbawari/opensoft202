from django.db import models

class Employee(models.Model):
    employee_id = models.CharField(max_length=20, unique=True)  # Unique Employee ID
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)  # Username added during signup
    password = models.CharField(max_length=128, blank=True, null=True)  # Hashed password stored here
    mentor_assigned = models.BooleanField(default=False)
    feedback_filled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employee_id} - {self.username or 'Not Signed Up'}"

class Award(models.Model):
    awards_choices=[
        ("Innovation Award","Innovation Award"),
        ("Leadership Excellence","Leadership Excellence"),
        ("best team player","best team player"),
        ("Star performer","Star Performer"),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='awards')
    award_name = models.CharField(max_length=255,choices=awards_choices,null=True)
    reward_points=models.IntegerField(default=0)

    def __str__(self):
        return f"Award {self.award_name} for {self.employee.username}"

class Leave(models.Model):
    leave_choices = [
        ("Sick Leave", "Sick Leave"),
        ("Casual Leave", "Casual Leave"),
        ("Unpaid Leave", "Unpaid Leave"),
        ("Annual Leave", "Annual Leave"),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves')
    start_date = models.DateField()
    end_date = models.DateField()
    no_of_leaves = models.IntegerField()
    leave_type = models.CharField(max_length=20, choices=leave_choices, null=True)

    def __str__(self):
        return f"Leave from {self.start_date} to {self.end_date} for {self.employee.username}"

class DailyActivity(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='daily_activities')
    date = models.DateField()
    meetings_attended = models.IntegerField()
    messages_sent = models.IntegerField()
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Activity on {self.date} for {self.employee.username}"

class Review_Performance(models.Model):
    choice_feed=[
      ("Meets Expectations","Meets Expectations"),
      ("Exceeds Expectations","Exceeds Expectations"),
      ("Needs Improvement","Needs Improvement"),
    ]
    choice_review=[
        ("Annual 2023","Annual 2023"),
        ("H2 2023","H2 2023"),
        ("H1 2023","H1 2023"),
        
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='review_performance')
    performance_rating=models.IntegerField()
    manager_feedback=models.CharField(choices=choice_feed,max_length=50)
    promotion_consideration=models.BooleanField()
    review_period=models.CharField(choices=choice_review,max_length=50)

    def __str__(self):
        return f"review for {self.employee.username}"
    

class Mood(models.Model):
    choice_emotion=[
      ("Sad Zone","Sad Zone"),
      ("Leaning to happy zone","Leaning to happy zone"),
      ("Neutral Zone(OK)","Neutral Zone(OK)"),
      ("Excited Zone","Excited Zone"),
      ("Frustrated Zone","Fruustrated Zone"),

    ]    

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='mood')
    Vibe_score=models.IntegerField()
    emotion_zone=models.CharField(choices=choice_emotion,max_length=200)

    def __str__(self):
        return f"mood for {self.employee.username}"

