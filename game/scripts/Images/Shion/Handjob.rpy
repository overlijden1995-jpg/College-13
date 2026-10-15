layeredimage shion handjob:

    # --------------------------------------------------------
    # Layer order (bottom -> top):
    # Body -> Chest -> Clothes -> Cum -> Head -> Blush -> Expressions
    # --------------------------------------------------------

    # BODY (single composite -- no separate legs/pelvis/arms)
    always:
        "images/characters/Shion/Handjob/Body.png"

    # HEAD (above body, below chest/clothes). It used to go Null() on hiding_face, but her expression
    # and blush groups kept drawing: closed eyes and lips floating in the air (tester 2026-10-10).
    # Until her hide-face art exists (a hand over the face, or the head turned: artist's list), hiding
    # the face is the core's eyes-closed treatment with the head in place.
    always:
        "images/characters/Shion/Handjob/Head.png"

    # BELLY (pregnancy)
    always:
        preg_art("shion", "+Handjob/belly")

    # --------------------------------------------------------
    # CHEST
    # --------------------------------------------------------
    group chest_body:
        attribute chest_none default:
            preg_art("shion", "Handjob/Chest/Chest.png")
        attribute chest_piercing:
            preg_art("shion", "Handjob/Chest/Chest Piercing.png")
        attribute chest_hidden:
            Null()
        attribute chest_clothes:
            Null()

    # CHEST CLOTHING
    group chest_clothing:
        attribute chest_clothes_none default:
            Null()

    group boobs_clothes:
        attribute boobs_clothes_none default:
            Null()
        attribute boobs_bikini_top:
            preg_art("shion", "Handjob/Clothes/Bikini.png")
        attribute boobs_bra:
            preg_art("shion", "Handjob/Clothes/Bra.png")

    group shoes:
        attribute shoes_none default:
            Null()

    group panties:
        attribute panties_none default:
            Null()
        attribute panties_on:
            Null()
        attribute panties_bikini:
            Null()

    group legs_clothes:
        attribute legs_none default:
            Null()

    # COLLAR
    group collar:
        attribute collar_none default:
            Null()

    # MID CLOTHING
    group mid_clothing:
        attribute mid_none default:
            Null()
        attribute over_vest:
            "images/characters/Shion/Handjob/Clothes/Vest.png"

    # OVER CLOTHING
    group over:
        attribute over_none default:
            Null()
        attribute over_jacket:
            "images/characters/Shion/Handjob/Clothes/Jacket.png"

    # CUM BODY
    group cum_boobs:
        attribute cum_boobs_none default:
            ConditionSwitch(
                "store._hj_girl and 'boobs' in getattr(store._hj_girl, 'Cum', [])",
                "images/characters/Shion/Handjob/Cum/Boobs Cum.png",
                "True", Null()
            )
        attribute cum_boobs_on:
            "images/characters/Shion/Handjob/Cum/Boobs Cum.png"

    # BLUSH
    group blush:
        attribute blush_0 default:
            Null()
        attribute blush_1:
            "images/characters/Shion/Handjob/Head/Blush 1.png"
        attribute blush_2:
            "images/characters/Shion/Handjob/Head/Blush 2.png"

    # CUM FACE
    group cum_face:
        attribute cum_face_none default:
            ConditionSwitch(
                "store._hj_girl and 'face' in getattr(store._hj_girl, 'Cum', [])",
                "images/characters/Shion/Handjob/Cum/Face Cum.png",
                "True", Null()
            )
        attribute cum_face_on:
            "images/characters/Shion/Handjob/Cum/Face Cum.png"

    group cum_mouth:
        attribute cum_mouth_none default:
            Null()

    # BROWS
    group brows:
        attribute brows_normal default:
            "images/characters/Shion/Handjob/Expression/Brows/Normal.png"
        attribute brows_confused:
            "images/characters/Shion/Handjob/Expression/Brows/Perplexed.png"
        attribute brows_surprised:
            "images/characters/Shion/Handjob/Expression/Brows/Angry.png"
        attribute brows_sad:
            "images/characters/Shion/Handjob/Expression/Brows/Sad.png"
        attribute brows_rise:
            "images/characters/Shion/Handjob/Expression/Brows/Rise Right.png"
        attribute brows_sad_2:
            "images/characters/Shion/Handjob/Expression/Brows/Sad 2.png"

    # EYES
    group eyes:
        attribute eyes_normal default:
            ConditionSwitch(
                "hj_blink", "images/characters/Shion/Handjob/Expression/Eyes/Closed.png",
                "True", "images/characters/Shion/Handjob/Expression/Eyes/Normal.png",
            )
        attribute eyes_side:
            ConditionSwitch(
                "hj_blink", "images/characters/Shion/Handjob/Expression/Eyes/Closed.png",
                "True", "images/characters/Shion/Handjob/Expression/Eyes/Looking Left.png",
            )
        attribute eyes_side_2:
            ConditionSwitch(
                "hj_blink", "images/characters/Shion/Handjob/Expression/Eyes/Closed.png",
                "True", "images/characters/Shion/Handjob/Expression/Eyes/Looking Right.png",
            )
        attribute eyes_looking_right:
            ConditionSwitch(
                "hj_blink", "images/characters/Shion/Handjob/Expression/Eyes/Closed.png",
                "True", "images/characters/Shion/Handjob/Expression/Eyes/Looking Right.png",
            )
        attribute eyes_looking_down:
            ConditionSwitch(
                "hj_blink", "images/characters/Shion/Handjob/Expression/Eyes/Closed.png",
                "True", "images/characters/Shion/Handjob/Expression/Eyes/Looking Down.png",
            )
        attribute eyes_squint:
            ConditionSwitch(
                "hj_blink", "images/characters/Shion/Handjob/Expression/Eyes/Closed.png",
                "True", "images/characters/Shion/Handjob/Expression/Eyes/Squint.png",
            )
        attribute eyes_squint_big:
            ConditionSwitch(
                "hj_blink", "images/characters/Shion/Handjob/Expression/Eyes/Closed.png",
                "True", "images/characters/Shion/Handjob/Expression/Eyes/Squint Normal.png",
            )
        attribute eyes_surprised:
            ConditionSwitch(
                "hj_blink", "images/characters/Shion/Handjob/Expression/Eyes/Closed.png",
                "True", "images/characters/Shion/Handjob/Expression/Eyes/Surprised.png",
            )
        # aliases: the shared expression presets / cum faces ask for these (other girls have the art;
        # Shion's closest art stands in — "unknown attributes" wiped the scene otherwise, tester 2026-10-10)
        attribute eyes_surprised_2:
            ConditionSwitch(
                "hj_blink", "images/characters/Shion/Handjob/Expression/Eyes/Closed.png",
                "True", "images/characters/Shion/Handjob/Expression/Eyes/Surprised.png",
            )
        attribute eyes_squint_2:
            ConditionSwitch(
                "hj_blink", "images/characters/Shion/Handjob/Expression/Eyes/Closed.png",
                "True", "images/characters/Shion/Handjob/Expression/Eyes/Squint.png",
            )
        attribute eyes_closed:
            "images/characters/Shion/Handjob/Expression/Eyes/Closed.png"
        attribute eyes_left_closed:
            ConditionSwitch(
                "hj_blink", "images/characters/Shion/Handjob/Expression/Eyes/Closed.png",
                "True", "images/characters/Shion/Handjob/Expression/Eyes/Blink Left.png",
            )
        attribute eyes_right_closed:
            ConditionSwitch(
                "hj_blink", "images/characters/Shion/Handjob/Expression/Eyes/Closed.png",
                "True", "images/characters/Shion/Handjob/Expression/Eyes/Blink Right.png",
            )
        attribute eyes_closed_happy:
            "images/characters/Shion/Handjob/Expression/Eyes/Closed Happy.png"

    # MOUTH
    group mouth:
        attribute mouth_normal default:
            "images/characters/Shion/Handjob/Expression/Mouth/Normal.png"
        attribute mouth_smile:
            "images/characters/Shion/Handjob/Expression/Mouth/Laugh.png"
        attribute mouth_laugh:
            "images/characters/Shion/Handjob/Expression/Mouth/Laugh.png"
        attribute mouth_surprised:
            "images/characters/Shion/Handjob/Expression/Mouth/Surprised.png"
        attribute mouth_tongue:
            "images/characters/Shion/Handjob/Expression/Mouth/Tongue.png"
        attribute mouth_open_teeth:
            "images/characters/Shion/Handjob/Expression/Mouth/Surprised.png"
        attribute mouth_disgusted:
            "images/characters/Shion/Handjob/Expression/Mouth/Normal.png"
        attribute mouth_serious:
            "images/characters/Shion/Handjob/Expression/Mouth/Normal.png"
        attribute mouth_sad:
            "images/characters/Shion/Handjob/Expression/Mouth/Mouth Sad.png"
        attribute mouth_sch:
            "images/characters/Shion/Handjob/Expression/Mouth/Surprised.png"
        attribute mouth_lipbite:
            "images/characters/Shion/Handjob/Expression/Mouth/Lipbite.png"

# ============================================================
# STANDALONE IMAGES
# ============================================================

image shion hj_hand = "images/characters/Shion/Handjob/Hand.png"

image shion hj_palm = "images/characters/Shion/Handjob/Palm.png"

image shion hj_thumb = "images/characters/Shion/Handjob/Thumb.png"

image shion hj_penis = ConditionSwitch(
    "store._hj_girl and 'penis' in getattr(store._hj_girl, 'Cum', [])",
    Composite(
        (1920, 1080),
        (0, 0), _p("HJ/HJ Penis.png"),
        (0, 0), "images/characters/Shion/Handjob/Cum/Penis Cum.png",
    ),
    "True",
    _p("HJ/HJ Penis.png"),
)

image shion hj_slap_right = _p("HJ/Guy Hand Smack Right.png")
image shion hj_slap_left  = _p("HJ/Guy Hand Smack Left.png")
image shion hj_squeeze_left  = _p("HJ/Guy Hands Squeeze Left.png")
image shion hj_squeeze_right = _p("HJ/Guy Hands Squeeze Right.png")

# Her face cum lives INSIDE the layeredimage (group cum_face above: it moves with her body). The
# standalone copy the core also shows (slot transform) painted a SECOND facial floating in the air
# (tester 2026-10-10): Null keeps the core's show/hide calls harmless, the layeredimage does the work.
image shion hj_cum_face = Null()
image shion hj_cum_face_UNUSED = ConditionSwitch(
    "store._hj_girl and 'face' in getattr(store._hj_girl, 'Cum', [])",
    "images/characters/Shion/Handjob/Cum/Face Cum.png",
    "True", Null()
)

image shion hj_cum_hand = ConditionSwitch(
    "store._hj_girl and 'hand' in getattr(store._hj_girl, 'Cum', [])",
    "images/characters/Shion/Handjob/Cum/Hand Cum.png",
    "True", Null()
)

image shion hj_hand_squeeze = "images/characters/Shion/Handjob/Hand Squeeze.png"
