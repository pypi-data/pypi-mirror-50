import pyblish.api


class CollectFusionRenderMode(pyblish.api.InstancePlugin):
    """Collect current comp's render Mode

    Options:
        renderlocal
        deadline

    Note that this value is set for each comp separately. When you save the
    comp this information will be stored in that file. If for some reason the
    available tool does not visualize which render mode is set for the
    current comp, please run the following line in the console (Py2)

    comp.GetData("colorbleed.rendermode")

    This will return the name of the current render mode as seen above under
    Options.

    """

    order = pyblish.api.CollectorOrder + 0.4
    label = "Collect Render Mode"
    hosts = ["fusion"]
    families = ["colorbleed.saver"]

    def process(self, instance):
        """Collect all image sequence tools"""
        options = ["renderlocal", "deadline"]

        comp = instance.context.data.get("currentComp")
        if not comp:
            raise RuntimeError("No comp previously collected, unable to "
                               "retrieve Fusion version.")

        rendermode = comp.GetData("colorbleed.rendermode") or "renderlocal"
        assert rendermode in options, "Must be supported render mode"

        self.log.info("Render mode: {0}".format(rendermode))

        # Append family
        family = "colorbleed.saver.{0}".format(rendermode)
        instance.data["families"].append(family)
