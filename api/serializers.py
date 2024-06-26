from rest_framework import serializers
from .models import Users, Projects, Tasks, Comments

# users serializers
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=False)

    class Meta:
        model = Users
        fields = ['id', 'email', 'username', 'password', 'first_name', 'last_name', 'date_joined']
    
    def create(self, validated_data):
        user = Users.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

# projects serializers
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'name', 'description', 'owner', 'created_at']
        read_only_fields = ['owner']

# tasks serializers
class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = '__all__'
        read_only_fields = ('project',) 

    def create(self, validated_data):
        # Automatically set 'due_date' based on request data
        due_date_data = self.context['request'].data.get('due_date')
        if due_date_data:
            validated_data['due_date'] = due_date_data
        return super().create(validated_data)

# comments serializers
class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'
        read_only_fields = ['id', 'user', 'task', 'created_at']