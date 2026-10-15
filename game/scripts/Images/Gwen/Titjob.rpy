# ============================================================
# Gwen Titjob Layered Sprite
# ============================================================

image gwen titjob_penis = _p("TJ/TJ Penis.png")
image gwen tj_slap_right = _p("TJ/TJ Guy Hand Smack Right.png")
image gwen tj_slap_left  = _p("TJ/TJ Guy Hand Smack Left.png")
image gwen tj_grab_boobs_left  = _p("TJ/TJ Guy Hands Squeeze Left.png")
image gwen tj_grab_boobs_right = _p("TJ/TJ Guy Hands Squeeze Right.png")
image gwen tj_arms3_hands = "images/characters/Gwen/Titjob/Gwen TJ Arms 3 Naked Hands.png"
image gwen tj_bikini_top = preg_art("gwen", "Titjob/Clothes/Chest/Black Bikini Top/Black bikini Top.png")
image gwen tj_bikini_top_up = preg_art("gwen", "Titjob/Clothes/Chest/Black Bikini Top/Black bikini Top Up.png")
image gwen tj_bikini_top_fixed = preg_art("gwen", "Titjob/Clothes/Chest/Black Bikini Top/Black Bikini Fixed.png")

# Boobs base (nipples shown separately with extra movement)
image gwen titjob_boobs = preg_art("gwen", "Titjob/Gwen TJ Base Boobs.png")

# Boobs cum (separate layer so it can sit above bikini)
image gwen titjob_boobs_cum = ConditionSwitch(
    "store._titjob_girl and 'boobs' in getattr(store._titjob_girl, 'Cum', [])",
    "images/characters/Gwen/Titjob/Cum/Gwen TJ Boobs Cum.png",
    "True", Null()
)

# Nipples (piercing-aware, separate layer for extra jiggle)
image gwen titjob_nipples = ConditionSwitch(
    "store._titjob_girl and getattr(store._titjob_girl, 'Piercing', False)",
    preg_art("gwen", "Titjob/Gwen TJ Nipples Piercings.png"),
    "True",
    preg_art("gwen", "Titjob/Gwen TJ Nipples.png")
)

layeredimage gwen titjob:

    # 0. Torso (bottom)
    group torso:
        attribute torso_base default:
            "images/characters/Gwen/Titjob/Gwen TJ Torso.png"

    # 1. Chest Bottom (corset base band / bikini fixed band)
    group chest_base:
        attribute chest_base_none default:
            Null()
        attribute chest_base_on:
            "images/characters/Gwen/Titjob/Clothes/Chest/Corset/Base.png"
        attribute chest_base_bikini:
            preg_art("gwen", "Titjob/Clothes/Chest/Black Bikini Top/Black Bikini Fixed.png")

    # 2. Chest Up (corset base / bikini up)
    group corset_up:
        attribute corset_up_none default:
            Null()
        attribute corset_up_on:
            "images/characters/Gwen/Titjob/Clothes/Chest/Corset/Base.png"
        attribute corset_up_bikini:
            preg_art("gwen", "Titjob/Clothes/Chest/Black Bikini Top/Black bikini Top Up.png")

    # 3. Arms (pose 1/2/3, player-controlled)
    group arms:
        attribute arms_1 default:
            "images/characters/Gwen/Titjob/Gwen TJ Arms 1Naked.png"
        attribute arms_2:
            "images/characters/Gwen/Titjob/Gwen TJ Arms 2 Naked.png"
        attribute arms_3:
            "images/characters/Gwen/Titjob/Gwen TJ Arms 3 Naked.png"
        attribute arms_ls_1:
            "images/characters/Gwen/Titjob/Clothes/Over/Long Shirt/TJ Arms 1.png"
        attribute arms_ls_2:
            "images/characters/Gwen/Titjob/Clothes/Over/Long Shirt/TJ Arms 2.png"
        attribute arms_ls_3:
            "images/characters/Gwen/Titjob/Clothes/Over/Long Shirt/TJ Arms 3.png"
        attribute arms_none:
            Null()

    # 4. Penis (below boobs, shown separately)
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
                "images/characters/Gwen/Titjob/Cum/Gwen TJ Main Boobs Cum.png",
                "True", Null()
            )

    # 7. Cum - Shoulders
    group cum_shoulders:
        attribute cum_shoulders_auto default:
            ConditionSwitch(
                "store._titjob_girl and 'shoulders' in getattr(store._titjob_girl, 'Cum', [])",
                "images/characters/Gwen/Titjob/Cum/Gwen TJ Shoulders Cum.png",
                "True", Null()
            )

    # 8. Blush
    group blush:
        attribute blush_auto default:
            ConditionSwitch(
                "_gs('titjob', 'blush', 0) == 2",
                "images/characters/Gwen/Titjob/Head/Gwen TJ Blush 2.png",
                "_gs('titjob', 'blush', 0) == 1",
                "images/characters/Gwen/Titjob/Head/Gwen TJ Blush 1.png",
                "True", Null()
            )

    # 9. Mouth
    group mouth:
        attribute mouth_normal default:
            "images/characters/Gwen/Titjob/Expressions/Mouth/Normal.png"
        attribute mouth_laugh:
            "images/characters/Gwen/Titjob/Expressions/Mouth/Laugh.png"
        attribute mouth_sad:
            "images/characters/Gwen/Titjob/Expressions/Mouth/Sad.png"
        attribute mouth_surprised:
            "images/characters/Gwen/Titjob/Expressions/Mouth/Surprised.png"
        attribute mouth_lipbite:
            "images/characters/Gwen/Titjob/Expressions/Mouth/Lipbite.png"
        attribute mouth_ahegao:
            "images/characters/Gwen/Titjob/Expressions/Mouth/Ahegao.png"
        attribute mouth_open:
            "images/characters/Gwen/Titjob/Expressions/Mouth/Open.png"
        attribute mouth_kiss:
            "images/characters/Gwen/Titjob/Expressions/Mouth/Kiss.png"

    # 10. Eyes
    group eyes:
        attribute eyes_normal default:
            "images/characters/Gwen/Titjob/Expressions/Eyes/Normal.png"
        attribute eyes_sexy:
            "images/characters/Gwen/Titjob/Expressions/Eyes/Sexy.png"
        attribute eyes_closed:
            "images/characters/Gwen/Titjob/Expressions/Eyes/Closed.png"
        attribute eyes_squint:
            "images/characters/Gwen/Titjob/Expressions/Eyes/Squint.png"
        attribute eyes_blink_left:
            "images/characters/Gwen/Titjob/Expressions/Eyes/Blinking Left.png"
        attribute eyes_blink_right:
            "images/characters/Gwen/Titjob/Expressions/Eyes/Blinking Right.png"
        attribute eyes_looking_left:
            "images/characters/Gwen/Titjob/Expressions/Eyes/Looking Left.png"
        attribute eyes_looking_right:
            "images/characters/Gwen/Titjob/Expressions/Eyes/Looking Right.png"

    # 11. Brows
    group brows:
        attribute brows_normal default:
            "images/characters/Gwen/Titjob/Expressions/Brows/Normal.png"
        attribute brows_confused:
            "images/characters/Gwen/Titjob/Expressions/Brows/Confused.png"
        attribute brows_confused_2:
            "images/characters/Gwen/Titjob/Expressions/Brows/Confused 2.png"
        attribute brows_sad:
            "images/characters/Gwen/Titjob/Expressions/Brows/Sad.png"
        attribute brows_challenging:
            "images/characters/Gwen/Titjob/Expressions/Brows/Challenging.png"

    # 12. Cum - Face (on top of everything)
    group cum_face:
        attribute cum_face_auto default:
            ConditionSwitch(
                "store._titjob_girl and 'face' in getattr(store._titjob_girl, 'Cum', [])",
                "images/characters/Gwen/Titjob/Cum/Gwen TJ Face Cum.png",
                "True", Null()
            )
