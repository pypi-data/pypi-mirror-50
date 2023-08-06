from maya import cmds

import colorbleed.maya.lib as lib
import avalon.maya


class CreateRig(avalon.maya.Creator):
    """Artist-friendly rig with controls to direct motion"""

    label = "Rig"
    family = "colorbleed.rig"
    icon = "wheelchair"

    def process(self):

        with lib.undo_chunk():
            instance = super(CreateRig, self).process()

            self.log.info("Creating Rig instance set up ...")
            controls = cmds.sets(name="controls_SET", empty=True)
            pointcache = cmds.sets(name="out_SET", empty=True)
            cmds.sets([controls, pointcache], forceElement=instance)
