import json

from django.core.management.base import BaseCommand

from cloud.models import VirtualMachine, VirtualMachineTag, FirewallRule


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("input_path", type=str)

    def handle(self, *args, **options):
        VirtualMachineTag.objects.all().delete()
        VirtualMachine.objects.all().delete()
        FirewallRule.objects.all().delete()

        with open(options["input_path"]) as f:
            json_input = json.load(f)

            for vm_data in json_input.get("vms", []):
                virtual_machine = VirtualMachine.objects.create(
                    id=vm_data.get("vm_id"), name=vm_data.get("name"),
                )
                for tag_data in vm_data.get("tags", []):
                    tag, _ = VirtualMachineTag.objects.get_or_create(name=tag_data)
                    virtual_machine.tags.add(tag)

            for fw_data in json_input.get("fw_rules", []):
                source_tag, _ = VirtualMachineTag.objects.get_or_create(
                    name=fw_data.get("source_tag")
                )
                dest_tag, _ = VirtualMachineTag.objects.get_or_create(
                    name=fw_data.get("dest_tag")
                )
                FirewallRule.objects.create(
                    id=fw_data.get("fw_id"), source_tag=source_tag, dest_tag=dest_tag,
                )
