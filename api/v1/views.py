from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.serializers import AttackQueryParamsSerializer
from cloud.models import VirtualMachine
from cloud.services import build_request_stats_service


class AttackView(APIView):
    def get(self, request):
        serializer = AttackQueryParamsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        virtual_machines = VirtualMachine.objects.can_attack(
            serializer.validated_data.get("virtual_machine")
        ).all()

        return Response([virtual_machine.id for virtual_machine in virtual_machines])


class StatsView(APIView):
    def get(self, request):
        request_stats = build_request_stats_service()

        return Response(
            {
                "vm_count": VirtualMachine.objects.count(),
                "request_count": request_stats.get_request_count(),
                "average_request_time": request_stats.get_average_request_time(),
            }
        )
