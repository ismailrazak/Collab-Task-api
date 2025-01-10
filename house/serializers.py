from rest_framework import serializers
from .models import House

class HouseSerializer(serializers.ModelSerializer):
    members = serializers.HyperlinkedRelatedField(read_only=True,many=True,view_name='user-detail')
    manager = serializers.HyperlinkedRelatedField(read_only=True,view_name='user-detail')
    tasklist = serializers.HyperlinkedRelatedField(many =True,read_only=True,view_name='tasklist-detail',source='task_lists')
    class Meta:
        model = House
        fields = ['id','url','name','image','created_on','description',
                  'manager','points','completed_tasks_count','not_completed_tasks_count'
                  ,'members','tasklist']
        read_only_fields = ['points','completed_tasks_count','not_completed_tasks_count']