# ============================================================
# NAME INPUT — Player chooses their character name
# ============================================================

default _name_input_text = ""
define _NAME_DEFAULT = "Rod"

screen name_input_screen():
    modal True
    zorder 200

    frame:
        style "SideMenuFrame"
        align (0.5, 0.2)
        xminimum 500
        xmaximum 500

        vbox:
            spacing 12
            xalign 0.5

            text _("What's your name?"):
                size 22
                color "#7dd3fc"
                font "fonts/WorkSans-Bold.ttf"
                outlines [(1, "#06101e", 0, 0)]
                xalign 0.5

            input:
                value VariableInputValue("_name_input_text")
                length 20
                color "#ffffff"
                size 24
                xalign 0.5

            # Error message if too short (but allow empty = default)
            if len(_name_input_text.strip()) > 0 and len(_name_input_text.strip()) < 3:
                text _("Name must be at least 3 characters."):
                    size 14
                    color "#f87171"
                    font "fonts/WorkSans-Medium.ttf"
                    outlines [(1, "#06101e", 0, 0)]
                    xalign 0.5

            # Hint that empty input uses default name
            if len(_name_input_text.strip()) == 0:
                text _("Leave empty for default: [_NAME_DEFAULT]"):
                    size 14
                    color "#94a3b8"
                    font "fonts/WorkSans-Medium.ttf"
                    outlines [(1, "#06101e", 0, 0)]
                    xalign 0.5

            textbutton _("Confirm"):
                style "SideMenuButton"
                text_style "SideMenuButtonText"
                xalign 0.5
                text_xalign 0.5
                text_text_align 0.5
                sensitive len(_name_input_text.strip()) >= 3 or len(_name_input_text.strip()) == 0
                action Return(_name_input_text.strip() if len(_name_input_text.strip()) >= 3 else _NAME_DEFAULT)

label name_input:

    scene black
    with fade

    $ _name_input_text = ""
    $ _player_name = renpy.call_screen("name_input_screen")

    $ Player.Name = _player_name

    "Alright, {b}[Player.Name]{/b}. Let's get started."

    return
