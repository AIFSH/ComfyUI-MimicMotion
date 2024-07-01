# Set the web directory, any .js file in that directory will be loaded by the frontend as a frontend extension
WEB_DIRECTORY = "./web"

from .nodes import MimicMotionNode, LoadVideo, PreViewVideo
# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "MimicMotionNode": MimicMotionNode,
    "LoadVideo": LoadVideo,
    "PreViewVideo": PreViewVideo
}
