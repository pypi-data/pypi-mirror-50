from maya import cmds

import pyblish.api
import colorbleed.api
import colorbleed.maya.action


class ValidateMeshNonManifold(pyblish.api.Validator):
    """Ensure that meshes don't have non-manifold edges or vertices

    To debug the problem on the meshes you can use Maya's modeling
    tool: "Mesh > Cleanup..."

    """

    order = colorbleed.api.ValidateMeshOrder
    hosts = ['maya']
    families = ['colorbleed.model']
    label = 'Mesh Non-Manifold Vertices/Edges'
    actions = [colorbleed.maya.action.SelectInvalidAction]

    @staticmethod
    def get_invalid(instance):

        meshes = cmds.ls(instance, type='mesh', long=True)

        invalid = []
        for mesh in meshes:
            if (cmds.polyInfo(mesh, nonManifoldVertices=True) or
                    cmds.polyInfo(mesh, nonManifoldEdges=True)):
                invalid.append(mesh)

        return invalid

    def process(self, instance):
        """Process all the nodes in the instance 'objectSet'"""

        invalid = self.get_invalid(instance)

        if invalid:
            raise ValueError("Meshes found with non-manifold "
                             "edges/vertices: {0}".format(invalid))
