# ============================================================
# Shion Titjob Layered Sprite
# ============================================================

image shion titjob_penis = _p("TJ/TJ Penis.png")
image shion tj_slap_right = _p("TJ/TJ Guy Hand Smack Right.png")
image shion tj_slap_left  = _p("TJ/TJ Guy Hand Smack Left.png")
image shion tj_grab_boobs_left  = _p("TJ/TJ Guy Hands Squeeze Left.png")
image shion tj_grab_boobs_right = _p("TJ/TJ Guy Hands Squeeze Right.png")

# Boobs and nipples are shown separately above the layeredimage (Core_Titjob, z 9982 / 9983); XL from visual
# pregnancy stage 1 (preg_art.rpy).
image shion titjob_boobs = preg_art("shion", "Titjob/Chest/Chest.png")

image shion titjob_boobs_cum = ConditionSwitch(
    "store._titjob_girl and 'boobs' in getattr(store._titjob_girl, 'Cum', [])",
    "images/characters/Shion/Titjob/Cum/Cum Boobs.png",
    "True", Null()
)

image shion titjob_nipples = ConditionSwitch(
    "store._titjob_girl and getattr(store._titjob_girl, 'Piercing', False)",
    preg_art("shion", "Titjob/Chest/Nipples Piercing.png"),
    "True",
    preg_art("shion", "Titjob/Chest/Nipples.png")
)

# Her titjob is done in a bra / bikini top or bare (author's rule): the jacket and the vest come off at the launch
# (no "titjob" entry in the registry), their art in Titjob/Clothes (and the XL files in Titjob/Preg) is not drawn.
# The bra / bikini top are full cups drawn to the boobs: standalone ABOVE them (Core_Titjob "tj_<chest item>",
# z 9984, bouncing with them), nothing of them inside the layeredimage (registry: chest_base_none). No "_up"
# variant: pulled up, the Core hides the cups. No XL art for them yet.
image shion tj_bra = "images/characters/Shion/Titjob/Clothes/Bra.png"
image shion tj_bikini_top = "images/characters/Shion/Titjob/Clothes/Bikini.png"

image shion titjob_hair = "images/characters/Shion/Titjob/Hair.png"

layeredimage shion titjob:

    # 0. Hair (behind everything)
    always:
        "images/characters/Shion/Titjob/Hair.png"

    # 1. Torso (the belly at the bottom edge from visual stage 1)
    group torso:
        attribute torso_base default:
            preg_art("shion", "Titjob/Torso.png")

    # 2. Chest Bottom (nothing of hers goes under the boobs: tj_bra / tj_bikini_top above them)
    group chest_base:
        attribute chest_base_none default:
            Null()

    # 3. Chest Up
    group corset_up:
        attribute corset_up_none default:
            Null()

    # 4. Arms (pose 1/2/3), always bare
    group arms:
        attribute arms_1 default:
            "images/characters/Shion/Titjob/Arms 1.png"
        attribute arms_2:
            "images/characters/Shion/Titjob/Arms 2.png"
        attribute arms_3:
            "images/characters/Shion/Titjob/Arms 3.png"
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

    # 6. Cum - Main Boobs
    group cum_main_boobs:
        attribute cum_main_boobs_auto default:
            ConditionSwitch(
                "store._titjob_girl and 'boobs' in getattr(store._titjob_girl, 'Cum', [])",
                "images/characters/Shion/Titjob/Cum/Cum Boobs Main.png",
                "True", Null()
            )

    # 7. Cum - Shoulders
    group cum_shoulders:
        attribute cum_shoulders_auto default:
            ConditionSwitch(
                "store._titjob_girl and 'shoulders' in getattr(store._titjob_girl, 'Cum', [])",
                "images/characters/Shion/Titjob/Cum/Cum Shoulders.png",
                "True", Null()
            )

    # 8. Head
    always:
        "images/characters/Shion/Titjob/Head.png"

    # 9. Blush
    group blush:
        attribute blush_auto default:
            ConditionSwitch(
                "_gs('titjob', 'blush', 0) == 2",
                "images/characters/Shion/Titjob/Head/Blush 2.png",
                "_gs('titjob', 'blush', 0) == 1",
                "images/characters/Shion/Titjob/Head/Blush 1.png",
                "True", Null()
            )

    # 9. Mouth
    group mouth:
        attribute mouth_normal default:
            "images/characters/Shion/Titjob/Expression/Mouth/Normal.png"
        attribute mouth_laugh:
            "images/characters/Shion/Titjob/Expression/Mouth/Laugh.png"
        attribute mouth_sad:
            "images/characters/Shion/Titjob/Expression/Mouth/Sad.png"
        attribute mouth_surprised:
            "images/characters/Shion/Titjob/Expression/Mouth/Surprised.png"
        attribute mouth_lipbite:
            "images/characters/Shion/Titjob/Expression/Mouth/Lipbite.png"
        attribute mouth_ahegao:
            "images/characters/Shion/Titjob/Expression/Mouth/Ahegao.png"
        attribute mouth_open:
            "images/characters/Shion/Titjob/Expression/Mouth/Open.png"
        attribute mouth_kiss:
            "images/characters/Shion/Titjob/Expression/Mouth/Kiss.png"
        attribute mouth_angry:
            "images/characters/Shion/Titjob/Expression/Mouth/Angry.png"
        attribute mouth_smile:
            "images/characters/Shion/Titjob/Expression/Mouth/Smile.png"
        attribute mouth_screaming:
            "images/characters/Shion/Titjob/Expression/Mouth/Screaming.png"
        attribute mouth_concerned:
            "images/characters/Shion/Titjob/Expression/Mouth/Concerned.png"

    # 10. Eyes
    group eyes:
        attribute eyes_normal default:
            "images/characters/Shion/Titjob/Expression/Eyes/Normal.png"
        attribute eyes_sexy:
            "images/characters/Shion/Titjob/Expression/Eyes/Sexy.png"
        attribute eyes_closed:
            "images/characters/Shion/Titjob/Expression/Eyes/Closed.png"
        attribute eyes_squint:
            "images/characters/Shion/Titjob/Expression/Eyes/Squint.png"
        attribute eyes_squint_2:
            "images/characters/Shion/Titjob/Expression/Eyes/Squint 2.png"
        attribute eyes_blink_left:
            "images/characters/Shion/Titjob/Expression/Eyes/Blinking Left.png"
        attribute eyes_blink_right:
            "images/characters/Shion/Titjob/Expression/Eyes/Blinking Right.png"
        attribute eyes_looking_left:
            "images/characters/Shion/Titjob/Expression/Eyes/Looking Left.png"
        attribute eyes_looking_left_2:
            "images/characters/Shion/Titjob/Expression/Eyes/Looking Left 2.png"
        attribute eyes_looking_right:
            "images/characters/Shion/Titjob/Expression/Eyes/Looking Right.png"
        attribute eyes_looking_right_2:
            "images/characters/Shion/Titjob/Expression/Eyes/Looking Right 2.png"
        attribute eyes_ahegao:
            "images/characters/Shion/Titjob/Expression/Eyes/Ahegao.png"
        attribute eyes_ahegao_2:
            "images/characters/Shion/Titjob/Expression/Eyes/Ahegao 2.png"
        attribute eyes_closed_happy:
            "images/characters/Shion/Titjob/Expression/Eyes/Closed Happy.png"
        attribute eyes_surprised:
            "images/characters/Shion/Titjob/Expression/Eyes/Surprised.png"
        attribute eyes_up_closed_left:
            "images/characters/Shion/Titjob/Expression/Eyes/Up Closed Left.png"
        attribute eyes_up_closed_right:
            "images/characters/Shion/Titjob/Expression/Eyes/Up Closed Right.png"

    # 11. Brows
    group brows:
        attribute brows_normal default:
            "images/characters/Shion/Titjob/Expression/Brows/Normal.png"
        attribute brows_confused:
            "images/characters/Shion/Titjob/Expression/Brows/Confused.png"
        attribute brows_confused_2:
            "images/characters/Shion/Titjob/Expression/Brows/Confused 2.png"
        attribute brows_sad:
            "images/characters/Shion/Titjob/Expression/Brows/Sad.png"
        attribute brows_sad_2:
            "images/characters/Shion/Titjob/Expression/Brows/Sad 2.png"
        attribute brows_challenging:
            "images/characters/Shion/Titjob/Expression/Brows/Challenging.png"
        attribute brows_concerned:
            "images/characters/Shion/Titjob/Expression/Brows/Concerned.png"

    # 12. Cum - Face
    group cum_face:
        attribute cum_face_auto default:
            ConditionSwitch(
                "store._titjob_girl and 'face' in getattr(store._titjob_girl, 'Cum', [])",
                "images/characters/Shion/Titjob/Cum/Cum Face.png",
                "True", Null()
            )
