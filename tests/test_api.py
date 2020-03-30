from django.urls import reverse

from tests import factories as f


class TestAttackView:
    def test_attack(self, api_client):
        tag_1 = f.VirtualMachineTag(name="tag1")
        tag_2 = f.VirtualMachineTag(name="tag2")
        tag_3 = f.VirtualMachineTag(name="tag3")
        vm_1 = f.VirtualMachineFactory.create(tags=[tag_1, tag_2])
        vm_2 = f.VirtualMachineFactory.create(tags=[tag_2, tag_3])
        f.FirewallRuleFactory.create(source_tag=tag_1, dest_tag=tag_3)

        url = reverse("api:v1:attack") + f"?vm_id={vm_2.id}"

        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 1
        assert vm_1.id in response.data


class TestStatsView:
    def test_stats(self, api_client, mocker, fake_redis):
        mocker.patch(
            "cloud.services.get_redis_connection", lambda *args, **kwargs: fake_redis
        )

        f.VirtualMachineFactory.create()
        f.VirtualMachineFactory.create()

        url = reverse("api:v1:stats")

        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data["vm_count"] == 2
        assert response.data["request_count"] == 0
        assert isinstance(response.data["average_request_time"], (int, float))

        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data["vm_count"] == 2
        assert response.data["request_count"] == 1
        assert isinstance(response.data["average_request_time"], (int, float))

    def test_stats__when_mocked(self, api_client, mocker):
        request_stats_service_mock = mocker.MagicMock()
        request_stats_service_mock.return_value.get_request_count.return_value = 3
        request_stats_service_mock.return_value.get_average_request_time.return_value = (
            0.35
        )
        mocker.patch(
            "api.v1.views.build_request_stats_service", request_stats_service_mock
        )

        f.VirtualMachineFactory.create()
        f.VirtualMachineFactory.create()

        url = reverse("api:v1:stats")

        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data["vm_count"] == 2
        assert response.data["request_count"] == 3
        assert response.data["average_request_time"] == 0.35
