from maya import cmds

import pyblish.api
import colorbleed.api
import colorbleed.maya.action


class ValidateMeshLaminaFaces(pyblish.api.InstancePlugin):
    """Validate meshes don't have lamina faces.

    Lamina faces share all of their edges.

    """

    order = colorbleed.api.ValidateMeshOrder
    hosts = ['maya']
    families = ['colorbleed.model']
    category = 'geometry'
    version = (0, 1, 0)
    label = 'Mesh Lamina Faces'
    actions = [colorbleed.maya.action.SelectInvalidAction]

    @staticmethod
    def get_invalid(instance):
        meshes = cmds.ls(instance, type='mesh', long=True)
        invalid = [mesh for mesh in meshes if
                   cmds.polyInfo(mesh, laminaFaces=True)]

        return invalid

    def process(self, instance):
        """Process all the nodes in the instance 'objectSet'"""

        invalid = self.get_invalid(instance)

        if invalid:
            raise ValueError("Meshes found with lamina faces: "
                             "{0}".format(invalid))
