from rest_framework.serializers import ModelSerializer
from lib_mgmt_sys.models import Books

class BookSerializer(ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'