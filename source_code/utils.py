import customtkinter as ctk

def clear_frame(frame):
    """Removes all widgets from the given frame/window."""
    for widget in frame.winfo_children():
        widget.destroy()
