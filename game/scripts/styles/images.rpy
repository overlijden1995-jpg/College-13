# =========================
# Gwen standing expressions
# =========================

# (gwen_pool_pos / rogue_left_pos voce pode manter se quiser pra cenas especificas)

transform gwen_pool_pos:
    xalign 0.7
    yalign 0.9

transform rogue_left_pos:
    xalign 0.2
    yalign 1.0

image black = Solid("#000")

image blackscreen:
    Solid("#000000")
    on show:
        alpha 1.0
        linear 0.4 alpha 1.0
    on hide:
        alpha 1.0
        linear 0.4 alpha 0.0

# Slots genéricos
transform slot_left:
    xalign StageLeft
    yalign 2.0
    yoffset 0

transform slot_center_left:
    xalign StageCenterLeft
    yalign 2.0
    yoffset 0

transform slot_center:
    xalign StageCenter
    yalign 2.0
    yoffset 0

transform slot_center_right:
    xalign StageCenterRight
    yalign 2.0
    yoffset 0

transform slot_right:
    xalign StageRight
    yalign 2.0
    yoffset 0

transform slide_out_right:
    yalign 2.0
    linear 0.5 xalign 1.3

transform slide_in_right:
    xalign 1.3
    yalign 2.0
    linear 0.5 xalign StageCenter

transform slot_door_open:
    xpos 0.5
    yalign 2.0

# Witness/intruder slide-in from screen edge
transform witness_enter_right:
    xalign 1.3
    yalign 2.0
    ease 0.6 xalign StageRight

transform witness_enter_left:
    xalign -0.3
    yalign 2.0
    ease 0.6 xalign StageLeft

transform witness_exit_right:
    ease 0.4 xalign 1.3

# A GIRL leaving the witness slot (set_girl_sprite hides her tag before showing, so an exit transform with no
# start position eased from xalign 0 / yalign 0: she jumped to the far left, a head higher, then walked out
# the right side; tester 2026-10-11). The witness slot is always StageRight (_safe_restore_slot).
transform witness_exit_right_from_slot:
    xalign StageRight
    yalign 2.0
    yoffset 0
    ease 0.4 xalign 1.3

transform witness_exit_left:
    ease 0.4 xalign -0.3

# Near/Far roster rotation animations
transform roster_slide_to_center:
    ease 0.4 xalign StageCenter

transform roster_slide_to_right:
    ease 0.4 xalign StageRight

transform roster_slide_to_offscreen:
    ease 0.4 xalign 1.3

transform roster_enter_from_left:
    xalign -0.3
    yalign 2.0
    ease 0.5 xalign StageLeft

init python:
    SPRITE_SLOTS = ["slot_left", "slot_right", "slot_center"]

    # Weekday names (Sun–Sat) — Day 1 = Sunday
    WEEKDAY_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    # Map time-of-day name -> icon file
    TIME_ICONS = {
        "Morning":   "images/menus/MorningIcon.png",
        "Afternoon": "images/menus/AfternoonIcon.png",
        "Evening":   "images/menus/EveningIcon.png",
        "Night":     "images/menus/NightIcon.png",   # your filename
    }

