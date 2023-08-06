from collections import defaultdict
import pyblish.api

from maya import cmds, mel
from avalon import maya as avalon
from colorbleed.maya import lib

# TODO : Publish of setdress: -unique namespace for all assets, VALIDATOR!


class CollectSetDress(pyblish.api.InstancePlugin):
    """Collect all relevant setdress items

    Collected data:

        * File name
        * Compatible loader
        * Matrix per instance
        * Namespace

    Note: GPU caches are currently not supported in the pipeline. There is no
    logic yet which supports the swapping of GPU cache to renderable objects.

    """

    order = pyblish.api.CollectorOrder + 0.49
    label = "Set Dress"
    families = ["colorbleed.setdress"]

    def process(self, instance):

        # Find containers
        containers = avalon.ls()

        # Get all content from the instance
        instance_lookup = set(cmds.ls(instance, type="transform", long=True))
        data = defaultdict(list)

        hierarchy_nodes = []
        for container in containers:

            root = lib.get_container_transforms(container, root=True)
            if not root or root not in instance_lookup:
                continue

            # Retrieve the hierarchy
            parent = cmds.listRelatives(root, parent=True, fullPath=True)[0]
            hierarchy_nodes.append(parent)

            # Temporary warning for GPU cache which are not supported yet
            loader = container["loader"]
            if loader == "GpuCacheLoader":
                self.log.warning("GPU Cache Loader is currently not supported"
                                 "in the pipeline, we will export it tho")

            # Gather info for new data entry
            representation_id = container["representation"]
            instance_data = {"loader": loader,
                             "parent": parent,
                             "namespace": container["namespace"]}

            # Check if matrix differs from default and store changes
            matrix_data = self.get_matrix_data(root)
            if matrix_data:
                instance_data["matrix"] = matrix_data

            data[representation_id].append(instance_data)

        instance.data["scenedata"] = dict(data)
        instance.data["hierarchy"] = list(set(hierarchy_nodes))

    def get_file_rule(self, rule):
        return mel.eval('workspace -query -fileRuleEntry "{}"'.format(rule))

    def get_matrix_data(self, node):
        """Get the matrix of all members when they are not default

        Each matrix which differs from the default will be stored in a
        dictionary

        Args:
            members (list): list of transform nmodes
        Returns:
            dict
        """

        matrix = cmds.xform(node, query=True, matrix=True)
        if matrix == lib.DEFAULT_MATRIX:
            return

        return matrix
