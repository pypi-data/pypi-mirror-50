from avalon import houdini


class CreatePointCache(houdini.Creator):
    """Alembic ROP to pointcache"""

    label = "Point Cache"
    family = "colorbleed.pointcache"
    icon = "gears"

    def __init__(self, *args, **kwargs):
        super(CreatePointCache, self).__init__(*args, **kwargs)

        # Remove the active, we are checking the bypass flag of the nodes
        self.data.pop("active", None)

        self.data.update({"node_type": "alembic"})

    def process(self):
        instance = super(CreatePointCache, self).process()

        parms = {"use_sop_path": True,  # Export single node from SOP Path
                 "build_from_path": True,  # Direct path of primitive in output
                 "path_attrib": "path",  # Pass path attribute for output
                 "prim_to_detail_pattern": "cbId",
                 "format": 2,  # Set format to Ogawa
                 "filename": "$HIP/pyblish/%s.abc" % self.name}

        if self.nodes:
            node = self.nodes[0]
            parms.update({"sop_path": node.path()})

        instance.setParms(parms)

        # Lock any parameters in this list
        to_lock = ["prim_to_detail_pattern"]
        for name in to_lock:
            parm = instance.parm(name)
            parm.lock(True)
