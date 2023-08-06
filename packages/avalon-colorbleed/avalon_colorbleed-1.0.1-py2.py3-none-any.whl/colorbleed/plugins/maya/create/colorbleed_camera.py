import avalon.maya
from colorbleed.maya import lib


class CreateCamera(avalon.maya.Creator):
    """Single baked camera"""

    label = "Camera"
    family = "colorbleed.camera"
    icon = "video-camera"

    def __init__(self, *args, **kwargs):
        super(CreateCamera, self).__init__(*args, **kwargs)

        # get basic animation data : start / end / handles / steps
        animation_data = lib.collect_animation_data()
        for key, value in animation_data.items():
            self.data[key] = value

        # Bake to world space by default, when this is False it will also
        # include the parent hierarchy in the baked results
        self.data['bakeToWorldSpace'] = True

        # Apply Euler filter to rotations for alembic
        self.data["eulerFilter"] = True

