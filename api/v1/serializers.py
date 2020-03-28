from rest_framework import serializers

from cloud.models import VirtualMachine


class AttackQueryParamsSerializer(serializers.Serializer):
    vm_id = serializers.PrimaryKeyRelatedField(
        source="virtual_machine", queryset=VirtualMachine.objects.all()
    )
