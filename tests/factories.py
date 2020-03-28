import factory

from cloud.models import VirtualMachineTag, VirtualMachine, FirewallRule


class VirtualMachineTag(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"name-{n}")

    class Meta:
        model = VirtualMachineTag
        django_get_or_create = ("name",)


class VirtualMachineFactory(factory.DjangoModelFactory):
    id = factory.Sequence(lambda n: f"vm-{n}")
    name = factory.Sequence(lambda n: f"name-{n}")

    class Meta:
        model = VirtualMachine

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)


class FirewallRuleFactory(factory.DjangoModelFactory):
    id = factory.Sequence(lambda n: f"fw-{n}")
    source_tag = factory.SubFactory("tests.factories.VirtualMachineTag")
    dest_tag = factory.SubFactory("tests.factories.VirtualMachineTag")

    class Meta:
        model = FirewallRule
