import os

import avalon.maya
import colorbleed.api

from maya import cmds


class ExtractVRayProxy(colorbleed.api.Extractor):
    """Extract the content of the instance to a vrmesh file

    Things to pay attention to:
        - If animation is toggled, are the frames correct
        -
    """

    label = "VRay Proxy (.vrmesh)"
    hosts = ["maya"]
    families = ["colorbleed.vrayproxy"]

    def process(self, instance):

        staging_dir = self.staging_dir(instance)
        file_name = "{}.vrmesh".format(instance.name)
        file_path = os.path.join(staging_dir, file_name)

        anim_on = instance.data["animation"]
        if not anim_on:
            # Remove animation information because it is not required for
            # non-animated subsets
            instance.data.pop("startFrame", None)
            instance.data.pop("endFrame", None)

            start_frame = 1
            end_frame = 1
        else:
            start_frame = instance.data["startFrame"]
            end_frame = instance.data["endFrame"]

        vertex_colors = instance.data.get("vertexColors", False)

        # Write out vrmesh file
        self.log.info("Writing: '%s'" % file_path)
        with avalon.maya.maintained_selection():
            cmds.select(instance.data["setMembers"], noExpand=True)
            cmds.vrayCreateProxy(exportType=1,
                                 dir=staging_dir,
                                 fname=file_name,
                                 animOn=anim_on,
                                 animType=3,
                                 startFrame=start_frame,
                                 endFrame=end_frame,
                                 vertexColorsOn=vertex_colors,
                                 ignoreHiddenObjects=True,
                                 createProxyNode=False)

        if "files" not in instance.data:
            instance.data["files"] = list()

        instance.data["files"].append(file_name)

        self.log.info("Extracted instance '%s' to: %s"
                      % (instance.name, staging_dir))
