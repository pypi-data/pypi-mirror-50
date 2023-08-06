from avalon import houdini


class CreateAlembicCamera(houdini.Creator):
    """Single baked camera from Alembic ROP"""

    label = "Camera (Abc)"
    family = "colorbleed.camera"
    icon = "camera"

    def __init__(self, *args, **kwargs):
        super(CreateAlembicCamera, self).__init__(*args, **kwargs)

        # Remove the active, we are checking the bypass flag of the nodes
        self.data.pop("active", None)

        # Set node type to create for output
        self.data.update({"node_type": "alembic"})

    def process(self):
        instance = super(CreateAlembicCamera, self).process()

        parms = {
            "filename": "$HIP/pyblish/%s.abc" % self.name,
            "use_sop_path": False
        }

        if self.nodes:
            node = self.nodes[0]
            path = node.path()

            # Split the node path into the first root and the remainder
            # So we can set the root and objects parameters correctly
            _, root, remainder = path.split("/", 2)
            parms.update({
                "root": "/" + root,
                "objects": remainder
            })

        instance.setParms(parms)

        # Lock the Use Sop Path setting so the
        # user doesn't accidentally enable it.
        instance.parm("use_sop_path").lock(True)
