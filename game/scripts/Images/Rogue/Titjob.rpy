# ============================================================
# Rogue Titjob Layered Sprite
# ============================================================
# Same structure as Gwen TJ. Arms 1/2/3 available.
# No Long Shirt variants.

image rogue titjob_penis = _p("TJ/TJ Penis.png")
image rogue tj_slap_right = _p("TJ/TJ Guy Hand Smack Right.png")
image rogue tj_slap_left  = _p("TJ/TJ Guy Hand Smack Left.png")
image rogue tj_grab_boobs_left  = Transform(_p("TJ/TJ Guy Hands Squeeze Left.png"), xoffset=8, yoffset=-8)
image rogue tj_grab_boobs_right = Transform(_p("TJ/TJ Guy Hands Squeeze Right.png"), xoffset=-8, yoffset=-8)

# Boobs base (nipples shown separately with extra movement)
image rogue titjob_boobs = preg_art("rogue", "Titjob/Rogue TJ Base Boobs.png")

# Boobs cum
image rogue titjob_boobs_cum = ConditionSwitch(
    "store._titjob_girl and 'boobs' in getattr(store._titjob_girl, 'Cum', [])",
    "images/characters/Rogue/Titjob/Cum/Rogue TJ Boobs Cum.png",
    "True", Null()
)

# Nipples (piercing-aware, separate layer for extra jiggle)
image rogue titjob_nipples = ConditionSwitch(
    "store._titjob_girl and getattr(store._titjob_girl, 'Piercing', False)",
    preg_art("rogue", "Titjob/Rogue TJ Nipples Piercings.png"),
    "True",
    preg_art("rogue", "Titjob/Rogue TJ Nipples.png")
)

# Arms 3 hands overlay (above boobs, shown by Core at zorder 10060)
image rogue tj_arms3_hands = "images/characters/Rogue/Titjob/Rogue TJ Arms 3 Naked Hands.png"

# Green Bikini Top standalone (referenced by Core_Titjob generic chest handling)
image rogue tj_bikini_top = preg_art("rogue", "Titjob/Clothes/Chest/Green Bikini Top/Green Bikini Top Down.png")
image rogue tj_bikini_top_up = "images/characters/Rogue/Titjob/Clothes/Chest/Green Bikini Top/Green Bikini Top Up.png"
image rogue tj_bikini_top_fixed = preg_art("rogue", "Titjob/Clothes/Chest/Green Bikini Top/Green Bikini Top Handle.png")

layeredimage rogue titjob:

    # 0. Torso (bottom)
    group torso:
        attribute torso_base default:
            "images/characters/Rogue/Titjob/Rogue TJ Torso.png"

    # 1. Chest Base (Crop Top base / Bikini fixed band, below boobs)
    group chest_base:
        attribute chest_base_none default:
            Null()
        attribute chest_base_on:
            "images/characters/Rogue/Titjob/Clothes/Chest/Crop Top/Base.png"
        attribute chest_base_bikini:
            preg_art("rogue", "Titjob/Clothes/Chest/Green Bikini Top/Green Bikini Top Handle.png")

    # 2. Corset Up (not used for Rogue, defined for system compatibility)
    group corset_up:
        attribute corset_up_none default:
            Null()

    # 3. Arms (pose 1/2/3, player-controlled)
    group arms:
        attribute arms_1 default:
            "images/characters/Rogue/Titjob/Rogue TJ Arms 1Naked.png"
        attribute arms_2:
            "images/characters/Rogue/Titjob/Rogue TJ Arms 2 Naked.png"
        attribute arms_3:
            "images/characters/Rogue/Titjob/Rogue TJ Arms 3 Naked.png"
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

    # 6. Cum - Main Boobs (on torso area)
    group cum_main_boobs:
        attribute cum_main_boobs_auto default:
            ConditionSwitch(
                "store._titjob_girl and 'boobs' in getattr(store._titjob_girl, 'Cum', [])",
                "images/characters/Rogue/Titjob/Cum/Rogue TJ Main Boobs Cum.png",
                "True", Null()
            )

    # 7. Cum - Shoulders
    group cum_shoulders:
        attribute cum_shoulders_auto default:
            ConditionSwitch(
                "store._titjob_girl and 'shoulders' in getattr(store._titjob_girl, 'Cum', [])",
                "images/characters/Rogue/Titjob/Cum/Rogue TJ Shoulders Cum.png",
                "True", Null()
            )

    # 8. Blush
    group blush:
        attribute blush_auto default:
            ConditionSwitch(
                "_gs('titjob', 'blush', 0) == 2",
                "images/characters/Rogue/Titjob/Head/Rogue TJ Blush 2.png",
                "_gs('titjob', 'blush', 0) == 1",
                "images/characters/Rogue/Titjob/Head/Rogue TJ Blush 1.png",
                "True", Null()
            )

    # 9. Mouth
    group mouth:
        attribute mouth_normal default:
            "images/characters/Rogue/Titjob/Expressions/Mouth/Normal.png"
        attribute mouth_laugh:
            "images/characters/Rogue/Titjob/Expressions/Mouth/Laugh.png"
        attribute mouth_sad:
            "images/characters/Rogue/Titjob/Expressions/Mouth/Sad.png"
        attribute mouth_surprised:
            "images/characters/Rogue/Titjob/Expressions/Mouth/Surprised.png"
        attribute mouth_lipbite:
            "images/characters/Rogue/Titjob/Expressions/Mouth/Lipbite.png"
        attribute mouth_ahegao:
            "images/characters/Rogue/Titjob/Expressions/Mouth/Ahegao.png"
        attribute mouth_open:
            "images/characters/Rogue/Titjob/Expressions/Mouth/Open.png"
        attribute mouth_kiss:
            "images/characters/Rogue/Titjob/Expressions/Mouth/Kiss.png"
        attribute mouth_angry:
            "images/characters/Rogue/Titjob/Expressions/Mouth/Angry.png"
        attribute mouth_scared:
            "images/characters/Rogue/Titjob/Expressions/Mouth/Screamming.png"
        attribute mouth_concerned:
            "images/characters/Rogue/Titjob/Expressions/Mouth/Concerned.png"

    # 10. Eyes
    group eyes:
        attribute eyes_normal default:
            "images/characters/Rogue/Titjob/Expressions/Eyes/Normal.png"
        attribute eyes_sexy:
            "images/characters/Rogue/Titjob/Expressions/Eyes/Sexy.png"
        attribute eyes_closed:
            "images/characters/Rogue/Titjob/Expressions/Eyes/Closed.png"
        attribute eyes_closed_happy:
            "images/characters/Rogue/Titjob/Expressions/Eyes/Closed Happy.png"
        attribute eyes_squint:
            "images/characters/Rogue/Titjob/Expressions/Eyes/Squint.png"
        attribute eyes_blink_left:
            "images/characters/Rogue/Titjob/Expressions/Eyes/Blinking Left.png"
        attribute eyes_blink_right:
            "images/characters/Rogue/Titjob/Expressions/Eyes/Blinking Right.png"
        attribute eyes_looking_left:
            "images/characters/Rogue/Titjob/Expressions/Eyes/Looking Left.png"
        attribute eyes_looking_right:
            "images/characters/Rogue/Titjob/Expressions/Eyes/Looking Right.png"
        attribute eyes_ahegao:
            "images/characters/Rogue/Titjob/Expressions/Eyes/Ahegao.png"
        attribute eyes_ahegao_2:
            "images/characters/Rogue/Titjob/Expressions/Eyes/Ahegao 2.png"
        attribute eyes_up_closed_left:
            "images/characters/Rogue/Titjob/Expressions/Eyes/Up Closed Left.png"
        attribute eyes_up_closed_right:
            "images/characters/Rogue/Titjob/Expressions/Eyes/Up Closed Right.png"

    # 11. Brows
    group brows:
        attribute brows_normal default:
            "images/characters/Rogue/Titjob/Expressions/Brows/Normal.png"
        attribute brows_confused:
            "images/characters/Rogue/Titjob/Expressions/Brows/Confused.png"
        attribute brows_confused_2:
            "images/characters/Rogue/Titjob/Expressions/Brows/Confused 2.png"
        attribute brows_sad:
            "images/characters/Rogue/Titjob/Expressions/Brows/Sad.png"
        attribute brows_sad_2:
            "images/characters/Rogue/Titjob/Expressions/Brows/Sad 2.png"
        attribute brows_challenging:
            "images/characters/Rogue/Titjob/Expressions/Brows/Challenging.png"
        attribute brows_concerned:
            "images/characters/Rogue/Titjob/Expressions/Brows/Concerned.png"

    # 12. Cum - Face
    group cum_face:
        attribute cum_face_auto default:
            ConditionSwitch(
                "store._titjob_girl and 'face' in getattr(store._titjob_girl, 'Cum', [])",
                "images/characters/Rogue/Titjob/Cum/Rogue TJ Face Cum.png",
                "True", Null()
            )
