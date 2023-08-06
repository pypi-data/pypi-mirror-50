from maya import cmds

import colorbleed.maya.lib as lib
import avalon.maya


class CreateYetiRig(avalon.maya.Creator):
    """Create a Yeti Rig"""

    label = "Yeti Rig"
    family = "colorbleed.yetiRig"
    icon = "usb"

    def process(self):

        with lib.undo_chunk():
            instance = super(CreateYetiRig, self).process()

            self.log.info("Creating Rig instance set up ...")
            input_meshes = cmds.sets(name="input_SET", empty=True)
            cmds.sets(input_meshes, forceElement=instance)
