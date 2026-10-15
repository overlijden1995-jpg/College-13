# TEMPORARY: Delete this file after running the game once.
# Clears the console history that causes a crash due to <string> text tag.
init -999 python:
    if hasattr(persistent, '_console_history'):
        persistent._console_history = []

# ============================================================
# TEST: Door open with girl behind it
# Call from console: renpy.call("test_door_open")
# ============================================================
label test_door_open:
    $ girl = _lookup_girl("gwen")
    scene bg gwenroom
    $ set_girl_sprite(girl.gid, pose="standing", at_list=[slot_door_open])
    show door_open zorder 151
    "You arrive at [girl.Name]'s room and find the door slightly open."
    "You peek inside..."
    hide door_open
    with dissolve
    $ set_girl_sprite(girl.gid, pose="standing")
    "You step inside."
    return
