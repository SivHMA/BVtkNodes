from .core import *
from . import favorites_data

# -----------------------------------------------------------------------------
# Favorites panel
# -----------------------------------------------------------------------------

# Favorites must be an array of (node.bl_idname, node.bl_label) tuples
favorites = favorites_data.favorites
favorites_file = favorites_data.__file__


class BVTK_PT_Favorites(bpy.types.Panel):
    """BVTK Favorites Panel"""

    bl_label = "Favorites"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Favorites"

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == "BVTK_NodeTreeType"

    def draw(self, context):
        global favorites
        active_node = context.active_node
        layout = self.layout
        # Button to add active node to favorites
        if active_node:
            add = layout.operator(
                "node.bvtk_update_favorites", icon="ZOOM_IN", text=active_node.bl_label
            )
            add.label = active_node.bl_label
            add.type = active_node.bl_idname
            layout.separator()
        # Favorites buttons
        for f in favorites:
            row = layout.row(align=True)
            remove = row.operator(
                "node.bvtk_update_favorites", icon="PANEL_CLOSE", text=""
            )
            remove.label = f[1]
            remove.type = f[0]
            remove.remove = True
            op = row.operator("node.add_node", text=f[1])
            op.type = f[0]
            op.use_transform = True


class BVTK_OT_UpdateFavorites(bpy.types.Operator):
    """Update favorites operator"""

    bl_idname = "node.bvtk_update_favorites"
    bl_label = "add/remove favorites"

    remove: bpy.props.BoolProperty(default=False)
    label: bpy.props.StringProperty()
    type: bpy.props.StringProperty()

    def execute(self, context):
        global favorites
        global favorites_file
        fav = (self.type, self.label)
        if self.remove:
            favorites.remove(fav)
        else:
            if fav in favorites:
                self.report({"INFO"}, "Already in favorites")
                return {"FINISHED"}
            favorites.append(fav)
        open(favorites_file, "w").write(
            "favorites = " + repr(favorites).replace("),", "),\n")
        )
        self.remove = False
        return {"FINISHED"}


add_ui_class(BVTK_PT_Favorites)
add_ui_class(BVTK_OT_UpdateFavorites)
