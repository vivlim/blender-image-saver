bl_info = {
    "name": "Image Saver",
    "description": "Automatically saves any unsaved images when you save a .blend file.",
    "blender": (2, 80, 0), # bpy.context.blend_data appears to be added in 2.66.6
    "category": "User Interface",
    "version": (1, 0, 0),
    "author": "vivlim",
}

import bpy
from bpy.app.handlers import persistent

@persistent
def on_save_blend_file(_arg1, _arg2):
    print("Image Saver: .blend file was saved.")
    save_unsaved_images()
    
def register():
    print("Image Saver: registered add-on.")
    try:
        bpy.app.handlers.save_post.append(on_save_blend_file)
    except:
        print("Image Saver: Failed to register post-save handler")

def unregister():
    print("Image Saver: unregistered add-on.")
    try:
        bpy.app.handlers.save_post.remove(on_save_blend_file)
    except:
        print("Image Saver: Failed to unregister post-save handler")

def save_unsaved_images():
    popup = ModalPopup("Image Saver", "INFO")
    warning_msgs = []
    ok_msgs = []

    for (image_name, image_data) in bpy.context.blend_data.images.items():
        print(image_name)
        
        if image_data.is_dirty:
            print("image wasn't saved", image_name)
            if image_data.filepath == "": # It isn't set, this hasn't been saved before
                warning_msgs.append("'{}' has NOT been saved to disk yet.".format(image_name))
                
            else: # it's been saved, just save it
                image_data.save()
                ok_msgs.append("'{}' saved to {}".format(image_name, image_data.filepath))


    for msg in warning_msgs:
        popup.append_label(msg)
    for msg in ok_msgs:
        popup.append_label(msg)

    popup.show()

# Hacky way to show a notification popup since we aren't in the context of an Operator
class ModalPopup:
    def __init__(self, title, icon):
        self.title = title
        self.items = []
        self.icon = icon
        self.f = lambda menu, context: self._show_popup_inner(menu)
    def show(self):
        if self.items:
            bpy.context.window_manager.popup_menu(self.f, title=self.title, icon=self.icon)
    def append_label(self, text):
        self.items.append(lambda layout: layout.label(text=text))
    def _show_popup_inner(self, menu):
        for item in self.items:
            item(menu.layout)

# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()