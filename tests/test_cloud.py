from django.core.exceptions import ValidationError
import pytest

from cloud.models import VirtualMachine
from tests import factories as f


class TestVirtualMachineModel:
    @pytest.mark.parametrize(
        "id_", ["vm-a211de", "vm-c7bac01a07", "vm-c1e6285f", "vm-8d2d12765"]
    )
    def test_id__when_valid(self, id_):
        vm = f.VirtualMachineFactory.create(id=id_)
        vm.full_clean()

    @pytest.mark.parametrize("id_", ["1", "vm-"])
    def test_id__when_invalid(self, id_):
        with pytest.raises(ValidationError):
            vm = f.VirtualMachineFactory.create(id=id_)
            vm.full_clean()


class TestVirtualMachinQuerySet:
    def test_can_attack(self):
        tag_1 = f.VirtualMachineTag(name="tag1")
        tag_2 = f.VirtualMachineTag(name="tag2")
        tag_3 = f.VirtualMachineTag(name="tag3")
        tag_4 = f.VirtualMachineTag(name="tag4")
        tag_5 = f.VirtualMachineTag(name="tag5")
        tag_6 = f.VirtualMachineTag(name="tag6")
        tag_7 = f.VirtualMachineTag(name="tag7")
        tag_333 = f.VirtualMachineTag(name="tag333")
        vm_1 = f.VirtualMachineFactory.create(tags=[tag_1, tag_2, tag_3])
        vm_2 = f.VirtualMachineFactory.create(tags=[tag_4, tag_5])
        vm_3 = f.VirtualMachineFactory.create(tags=[tag_6])
        vm_4 = f.VirtualMachineFactory.create(tags=[tag_7])
        f.FirewallRuleFactory.create(source_tag=tag_1, dest_tag=tag_2)
        f.FirewallRuleFactory.create(source_tag=tag_4, dest_tag=tag_1)
        f.FirewallRuleFactory.create(source_tag=tag_5, dest_tag=tag_2)
        f.FirewallRuleFactory.create(source_tag=tag_6, dest_tag=tag_2)
        f.FirewallRuleFactory.create(source_tag=tag_7, dest_tag=tag_333)

        vms = VirtualMachine.objects.can_attack(vm_1)
        print(vms.query)
        assert vms.count() == 2
        assert vm_2 in vms
        assert vm_3 in vms
        assert vm_4 not in vms


class TestFirewallRuleModel:
    @pytest.mark.parametrize(
        "id_", ["fw-a211de", "fw-c7bac01a07", "fw-c1e6285f", "fw-8d2d12765"]
    )
    def test_id__when_valid(self, id_):
        vm = f.FirewallRuleFactory.create(id=id_)
        vm.full_clean()

    @pytest.mark.parametrize("id_", ["1", "fw-"])
    def test_id__when_invalid(self, id_):
        with pytest.raises(ValidationError):
            vm = f.FirewallRuleFactory.create(id=id_)
            vm.full_clean()
