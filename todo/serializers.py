from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User 


class TaskSerializer(serializers.ModelSerializer):
    # user = serializers.ForeignKey(User,on_delete=serializers.CASCADE, null=True,blank=True)
    Task = serializers.CharField(max_length=100,required=True)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Complete', 'Complete'),
        ('In-Progress','In-Progress')
        
       
    ]
    task_status = serializers.CharField(max_length=20)
    
    class Meta:
        model = Task
        fields= "__all__"    

        
 