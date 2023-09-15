from rest_framework import serializers
from apps.store.models import Warehouse
# from apps.accounts.serializers import UserSerializer

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ('id',
                  'name',
                  'phone',
                  'email',
                  'country',
                  'city')

# class GetWarehouseSeralizer(serializers.ModelSerializer):
#     created_by = UserSerializer()
#     modified_by = UserSerializer()

#     class Meta:
#         model = Warehouse
#         fields = (
#             "created_by",
#             "modified_by",
#             "name",
#             "phone",
#             "email",
#             "country",
#             "city"
#         )