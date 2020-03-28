from django.core.validators import RegexValidator
from django.db import models


class VirtualMachineQuerySet(models.QuerySet):
    def can_attack(self, virtual_machine):
        return (
            self.exclude(id=virtual_machine.id)
            .filter(
                tags__in=models.Subquery(
                    FirewallRule.objects.filter(
                        dest_tag__in=virtual_machine.tags.all()
                    ).values("source_tag")
                )
            )
            .distinct()
        )


class VirtualMachineTag(models.Model):
    name = models.CharField(max_length=200, unique=True)


class VirtualMachine(models.Model):
    id = models.CharField(
        max_length=50, primary_key=True, validators=[RegexValidator(r"vm-\w+")]
    )
    name = models.CharField(max_length=200)
    tags = models.ManyToManyField(
        "VirtualMachineTag", related_name="virtual_machines", blank=True
    )

    objects = VirtualMachineQuerySet.as_manager()


class FirewallRule(models.Model):
    id = models.CharField(
        max_length=50, primary_key=True, validators=[RegexValidator(r"fw-\w+")]
    )
    source_tag = models.ForeignKey(
        "VirtualMachineTag",
        on_delete=models.CASCADE,
        related_name="source_firewall_rules",
    )
    dest_tag = models.ForeignKey(
        "VirtualMachineTag",
        on_delete=models.CASCADE,
        related_name="dest_firewall_rules",
    )
