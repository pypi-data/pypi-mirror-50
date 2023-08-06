import pyblish.api
import colorbleed.api


class ValidateBypassed(pyblish.api.InstancePlugin):
    """Validate all primitives build hierarchy from attribute when enabled.

    The name of the attribute must exist on the prims and have the same name
    as Build Hierarchy from Attribute's `Path Attribute` value on the Alembic
    ROP node whenever Build Hierarchy from Attribute is enabled.

    """

    order = colorbleed.api.ValidateContentsOrder - 0.1
    families = ["*"]
    hosts = ["houdini"]
    label = "Validate ROP Bypass"

    def process(self, instance):

        invalid = self.get_invalid(instance)
        if invalid:
            rop = invalid[0]
            raise RuntimeError(
                "ROP node %s is set to bypass, publishing cannot continue.." %
                rop.path()
            )

    @classmethod
    def get_invalid(cls, instance):

        rop = instance[0]
        if rop.isBypassed():
            return [rop]
