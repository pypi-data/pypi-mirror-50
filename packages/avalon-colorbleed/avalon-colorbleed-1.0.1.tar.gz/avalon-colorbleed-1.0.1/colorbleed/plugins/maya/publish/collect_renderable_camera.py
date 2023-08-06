import pyblish.api

from maya import cmds

from colorbleed.maya import lib


class CollectRenderableCamera(pyblish.api.InstancePlugin):
    """Collect the renderable camera(s) for the render layer"""

    order = pyblish.api.CollectorOrder + 0.01
    label = "Collect Renderable Camera(s)"
    hosts = ["maya"]
    families = ["colorbleed.vrayscene",
                "colorbleed.renderlayer"]

    def process(self, instance):
        layer = instance.data["setMembers"]

        cameras = cmds.ls(type="camera", long=True)
        renderable = [c for c in cameras if
                      lib.get_attr_in_layer("%s.renderable" % c, layer=layer)]

        self.log.info("Found cameras %s: %s" % (len(renderable), renderable))

        instance.data["cameras"] = renderable
