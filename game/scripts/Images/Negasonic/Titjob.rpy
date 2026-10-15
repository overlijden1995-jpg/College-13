# ============================================================
# Negasonic (NTW) Titjob Layered Sprite
# ============================================================
# Body + Head split. Arms 2/3 only (no Arms 1).
# Boobs include nipples (no separate nipple layer).
# Piercings = full boobs replacement, not overlay.
# Clothes: Yellow Jacket (over), Yellow Bra (chest).
# Player Actions use shared Player/TJ/ assets.

image ntw titjob_penis = _p("TJ/TJ Penis.png")

# Player Actions — shared from Player/{skin}/TJ/
image ntw tj_slap_right = _p("TJ/TJ Guy Hand Smack Right.png")
image ntw tj_slap_left  = _p("TJ/TJ Guy Hand Smack Left.png")
image ntw tj_grab_boobs_left  = _p("TJ/TJ Guy Hands Squeeze Left.png")
image ntw tj_grab_boobs_right = _p("TJ/TJ Guy Hands Squeeze Right.png")

# Arms 3 hands overlay (above boobs, shown by Core at zorder 10060)
image ntw tj_arms3_hands = "images/characters/Negasonic/Titjob/Negasonic TJ Arms 3 Naked Hands.png"

# Boobs (nipples already included; piercing swaps entire image)
image ntw titjob_boobs = ConditionSwitch(
    "store._titjob_girl and getattr(store._titjob_girl, 'Piercing', False)",
    preg_art("ntw", "Titjob/Negasonic TJ Boobs Piercings.png"),
    "True",
    preg_art("ntw", "Titjob/Negasonic TJ Boobs.png"),
)

# Boobs cum (separate layer above bikini/bra)
image ntw titjob_boobs_cum = ConditionSwitch(
    "store._titjob_girl and 'boobs' in getattr(store._titjob_girl, 'Cum', [])",
    "images/characters/Negasonic/Titjob/Cum/Negasonic TJ Cum Boobs.png",
    "True", Null()
)

# Nipples: part of the boobs in the normal art (nothing to show). The bigger pregnancy breasts come as
# base + separate nipples, so from visual stage 1 this layer carries them (PREG_ART, preg_art.rpy).
image ntw titjob_nipples = ConditionSwitch(
    "store._titjob_girl and getattr(store._titjob_girl, 'Piercing', False)",
    preg_art("ntw", "+Titjob/nipples pierced"),
    "True",
    preg_art("ntw", "+Titjob/nipples"),
)

layeredimage ntw titjob:

    # 0. Torso + Head (bottom layers)
    group torso:
        attribute torso_base default:
            Composite(
                (1920, 1080),
                (0, 0), preg_art("ntw", "Titjob/Negasonic TJ Body.png"),
                (0, 0), "images/characters/Negasonic/Titjob/Negasonic TJ Head.png",
            )

    # 1. Chest Base (NTW has no under-boobs band)
    group chest_base:
        attribute chest_base_none default:
            Null()

    # 2. Corset Up (not applicable for NTW)
    group corset_up:
        attribute corset_up_none default:
            Null()

    # 3. Arms (2 positions: arms_2 default, arms_3 with hands overlay)
    group arms:
        attribute arms_1:
            Null()
        attribute arms_2 default:
            "images/characters/Negasonic/Titjob/Negasonic TJ Arms 2.png"
        attribute arms_3:
            "images/characters/Negasonic/Titjob/Negasonic TJ Arms 3 Naked.png"
        attribute arms_none:
            Null()

    # 4. Penis (shown separately)
    group penis:
        attribute penis_none default:
            Null()

    # 5. Boobs (shown separately via titjob_boobs)
    group boobs:
        attribute boobs_none default:
            Null()
        attribute boobs_naked:
            Null()

    # 6. Cum — Main Boobs (on torso area)
    group cum_main_boobs:
        attribute cum_main_boobs_auto default:
            ConditionSwitch(
                "store._titjob_girl and 'boobs' in getattr(store._titjob_girl, 'Cum', [])",
                "images/characters/Negasonic/Titjob/Cum/Negasonic TJ Cum Main.png",
                "True", Null()
            )

    # 7. Cum — Shoulders
    group cum_shoulders:
        attribute cum_shoulders_auto default:
            ConditionSwitch(
                "store._titjob_girl and 'shoulders' in getattr(store._titjob_girl, 'Cum', [])",
                "images/characters/Negasonic/Titjob/Cum/Negasonic TJ Cum Shoulders.png",
                "True", Null()
            )

    # 8. Blush
    group blush:
        attribute blush_auto default:
            ConditionSwitch(
                "_gs('titjob', 'blush', 0) == 2",
                "images/characters/Negasonic/Titjob/Head/Negasonic TJ Blush 2.png",
                "_gs('titjob', 'blush', 0) == 1",
                "images/characters/Negasonic/Titjob/Head/Negasonic TJ Blush 1.png",
                "True", Null()
            )

    # 9. Mouth
    group mouth:
        attribute mouth_normal default:
            "images/characters/Negasonic/Titjob/Expressions/Mouth/Normal.png"
        attribute mouth_laugh:
            "images/characters/Negasonic/Titjob/Expressions/Mouth/Laugh.png"
        attribute mouth_sad:
            "images/characters/Negasonic/Titjob/Expressions/Mouth/Sad.png"
        attribute mouth_surprised:
            "images/characters/Negasonic/Titjob/Expressions/Mouth/Screamming.png"
        attribute mouth_lipbite:
            "images/characters/Negasonic/Titjob/Expressions/Mouth/Lipbite.png"
        attribute mouth_ahegao:
            "images/characters/Negasonic/Titjob/Expressions/Mouth/Ahegao.png"
        attribute mouth_open:
            "images/characters/Negasonic/Titjob/Expressions/Mouth/Open.png"
        attribute mouth_kiss:
            "images/characters/Negasonic/Titjob/Expressions/Mouth/Kiss.png"
        attribute mouth_angry:
            "images/characters/Negasonic/Titjob/Expressions/Mouth/Angry.png"
        attribute mouth_concerned:
            "images/characters/Negasonic/Titjob/Expressions/Mouth/Concerned.png"
        attribute mouth_smile:
            "images/characters/Negasonic/Titjob/Expressions/Mouth/Smile.png"

    # 10. Eyes
    group eyes:
        attribute eyes_normal default:
            "images/characters/Negasonic/Titjob/Expressions/Eyes/Normal.png"
        attribute eyes_closed:
            "images/characters/Negasonic/Titjob/Expressions/Eyes/Closed.png"
        attribute eyes_closed_happy:
            "images/characters/Negasonic/Titjob/Expressions/Eyes/Closed Happy.png"
        attribute eyes_squint:
            "images/characters/Negasonic/Titjob/Expressions/Eyes/Squint.png"
        attribute eyes_blink_left:
            "images/characters/Negasonic/Titjob/Expressions/Eyes/Blinking Left.png"
        attribute eyes_blink_right:
            "images/characters/Negasonic/Titjob/Expressions/Eyes/Blinking Right.png"
        attribute eyes_looking_left:
            "images/characters/Negasonic/Titjob/Expressions/Eyes/Looking Left.png"
        attribute eyes_looking_right:
            "images/characters/Negasonic/Titjob/Expressions/Eyes/Looking Right.png"
        attribute eyes_looking_left_2:
            "images/characters/Negasonic/Titjob/Expressions/Eyes/Looking Left 2.png"
        attribute eyes_looking_right_2:
            "images/characters/Negasonic/Titjob/Expressions/Eyes/Looking Right 2.png"
        attribute eyes_surprised:
            "images/characters/Negasonic/Titjob/Expressions/Eyes/Surprised.png"
        attribute eyes_sexy:
            "images/characters/Negasonic/Titjob/Expressions/Eyes/Normal.png"

    # 11. Brows
    group brows:
        attribute brows_normal default:
            "images/characters/Negasonic/Titjob/Expressions/Brows/Normal.png"
        attribute brows_confused:
            "images/characters/Negasonic/Titjob/Expressions/Brows/Confused.png"
        attribute brows_confused_2:
            "images/characters/Negasonic/Titjob/Expressions/Brows/Confused 2.png"
        attribute brows_sad:
            "images/characters/Negasonic/Titjob/Expressions/Brows/Sad.png"
        attribute brows_sad_2:
            "images/characters/Negasonic/Titjob/Expressions/Brows/Sad 2.png"
        attribute brows_challenging:
            "images/characters/Negasonic/Titjob/Expressions/Brows/Challenging.png"

    # 12. Cum — Face (on top of everything)
    group cum_face:
        attribute cum_face_auto default:
            ConditionSwitch(
                "store._titjob_girl and 'face' in getattr(store._titjob_girl, 'Cum', [])",
                "images/characters/Negasonic/Titjob/Cum/Negasonic TJ Cum Face.png",
                "True", Null()
            )
