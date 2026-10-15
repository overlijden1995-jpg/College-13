# ============================================================
# Negasonic (NTW) Handjob Layered Sprite
# ============================================================
# Body/Face split (unlike Gwen/Rogue's combined Torso Head).
# Clothes: Yellow Jacket (over), Yellow Bra (chest).
# Player Actions use shared Player/HJ/ assets.

layeredimage ntw handjob:

    # BASE body (bottom layer — Torso 2 when hiding face)
    always:
        ConditionSwitch(
            "store.hiding_face",
            preg_art("ntw", "Handjob/Torso 2.png"),
            "True",
            preg_art("ntw", "Handjob/Negasonic HJ Body.png")
        )

    # CHEST BODY (boobs — above body)
    group chest_body:
        attribute chest_none default:
            preg_art("ntw", "Handjob/Negasonic HJ Boobs Naked.png")
        attribute chest_piercing:
            preg_art("ntw", "Handjob/Negasonic HJ Boobs Naked Piercings.png")

    # CHEST CLOTHING (Yellow Bra — above boobs, below jacket)
    group chest_clothing:
        attribute chest_clothes_none default:
            Null()
        attribute chest_corset:
            preg_art("ntw", "Handjob/Clothes/Chest/Yellow Bra/Yellow Bra.png")
        attribute chest_corset_up:
            preg_art("ntw", "Handjob/Clothes/Chest/Yellow Bra/Yellow Bra Up.png")
        attribute chest_corset_down:
            Null()
        attribute chest_bikini_top:
            preg_art("ntw", "Handjob/Clothes/Chest/Pink Bikini Top/Pink Bikini Top.png")
        attribute chest_bikini_top_up:
            preg_art("ntw", "Handjob/Clothes/Chest/Pink Bikini Top/Pink Bikini Top Up.png")

    # MID (placeholder)
    group mid:
        attribute mid_none default:
            Null()

    # OVER (Yellow Jacket — above bra, covers body+boobs)
    group over:
        attribute over_none default:
            Null()
        attribute over_long_shirt:
            ConditionSwitch(
                "store.hiding_face",
                Composite(
                    (480, 960),
                    (0, 0), preg_art("ntw", "Handjob/Clothes/Over/Yellow Jacket/Negasonic HJ Body Clothed 2.png"),
                    (0, 0), preg_art("ntw", "Handjob/Clothes/Over/Yellow Jacket/Negasonic HJ Boobs Clothed.png"),
                ),
                "True",
                Composite(
                    (480, 960),
                    (0, 0), preg_art("ntw", "Handjob/Clothes/Over/Yellow Jacket/Negasonic HJ Body Clothed.png"),
                    (0, 0), preg_art("ntw", "Handjob/Clothes/Over/Yellow Jacket/Negasonic HJ Boobs Clothed.png"),
                )
            )

    # FACE (above body and clothes — separate head layer)
    always:
        "images/characters/Negasonic/Handjob/Negasonic HJ Face.png"

    # COLLAR (NTW has none)
    group collar:
        attribute collar_none default:
            Null()
        attribute collar_on:
            Null()

    # CUM BOOBS
    group cum_boobs:
        attribute cum_boobs_none default:
            Null()
        attribute cum_boobs_on:
            "images/characters/Negasonic/Handjob/Cum/Negasonic HJ Boobs Cum.png"

    # BLUSH
    group blush:
        attribute blush_0 default:
            Null()
        attribute blush_1:
            "images/characters/Negasonic/Handjob/Head/Negasonic HJ Blush 1.png"
        attribute blush_2:
            "images/characters/Negasonic/Handjob/Head/Negasonic HJ Blush 2.png"

    # CUM FACE
    group cum_face:
        attribute cum_face_none default:
            Null()
        attribute cum_face_on:
            "images/characters/Negasonic/Handjob/Cum/Negasonic HJ Face Cum.png"

    # BROWS
    group brows:
        attribute brows_normal default:
            "images/characters/Negasonic/Handjob/Expressions/Brows/Normal.png"
        attribute brows_confused:
            "images/characters/Negasonic/Handjob/Expressions/Brows/Perplexed.png"
        attribute brows_surprised:
            "images/characters/Negasonic/Handjob/Expressions/Brows/Angry.png"
        attribute brows_sad:
            "images/characters/Negasonic/Handjob/Expressions/Brows/Sad.png"

    # EYES (ConditionSwitch: hj_blink -> Closed)
    group eyes:
        attribute eyes_normal default:
            ConditionSwitch(
                "hj_blink", "images/characters/Negasonic/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Negasonic/Handjob/Expressions/Eyes/Normal.png",
            )
        attribute eyes_side:
            ConditionSwitch(
                "hj_blink", "images/characters/Negasonic/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Negasonic/Handjob/Expressions/Eyes/Looking Left.png",
            )
        attribute eyes_side_2:
            ConditionSwitch(
                "hj_blink", "images/characters/Negasonic/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Negasonic/Handjob/Expressions/Eyes/Looking Right.png",
            )
        attribute eyes_looking_right:
            ConditionSwitch(
                "hj_blink", "images/characters/Negasonic/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Negasonic/Handjob/Expressions/Eyes/Looking Right.png",
            )
        attribute eyes_looking_down:
            ConditionSwitch(
                "hj_blink", "images/characters/Negasonic/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Negasonic/Handjob/Expressions/Eyes/Looking Down.png",
            )
        attribute eyes_squint:
            ConditionSwitch(
                "hj_blink", "images/characters/Negasonic/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Negasonic/Handjob/Expressions/Eyes/Squint.png",
            )
        attribute eyes_squint_big:
            ConditionSwitch(
                "hj_blink", "images/characters/Negasonic/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Negasonic/Handjob/Expressions/Eyes/Squint Normal.png",
            )
        attribute eyes_surprised:
            ConditionSwitch(
                "hj_blink", "images/characters/Negasonic/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Negasonic/Handjob/Expressions/Eyes/Surprised.png",
            )
        attribute eyes_surprised_2:
            ConditionSwitch(
                "hj_blink", "images/characters/Negasonic/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Negasonic/Handjob/Expressions/Eyes/Surprised.png",
            )
        attribute eyes_closed:
            "images/characters/Negasonic/Handjob/Expressions/Eyes/Closed.png"
        attribute eyes_closed_happy:
            "images/characters/Negasonic/Handjob/Expressions/Eyes/Closed Happy.png"
        attribute eyes_left_closed:
            ConditionSwitch(
                "hj_blink", "images/characters/Negasonic/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Negasonic/Handjob/Expressions/Eyes/Blink Left.png",
            )
        attribute eyes_right_closed:
            ConditionSwitch(
                "hj_blink", "images/characters/Negasonic/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Negasonic/Handjob/Expressions/Eyes/Blink Right.png",
            )
        attribute eyes_squint_2:
            ConditionSwitch(
                "hj_blink", "images/characters/Negasonic/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Negasonic/Handjob/Expressions/Eyes/Squint Normal.png",
            )

    # MOUTH
    group mouth:
        attribute mouth_normal default:
            "images/characters/Negasonic/Handjob/Expressions/Mouth/Normal.png"
        attribute mouth_smile:
            "images/characters/Negasonic/Handjob/Expressions/Mouth/Lipbite.png"
        attribute mouth_laugh:
            "images/characters/Negasonic/Handjob/Expressions/Mouth/Laugh.png"
        attribute mouth_surprised:
            "images/characters/Negasonic/Handjob/Expressions/Mouth/Surprised.png"
        attribute mouth_tongue:
            "images/characters/Negasonic/Handjob/Expressions/Mouth/Tongue.png"
        attribute mouth_open_teeth:
            "images/characters/Negasonic/Handjob/Expressions/Mouth/Surprised.png"
        attribute mouth_disgusted:
            "images/characters/Negasonic/Handjob/Expressions/Mouth/Surprised.png"
        attribute mouth_serious:
            "images/characters/Negasonic/Handjob/Expressions/Mouth/Normal.png"
        attribute mouth_sad:
            "images/characters/Negasonic/Handjob/Expressions/Mouth/Sad.png"
        attribute mouth_sch:
            "images/characters/Negasonic/Handjob/Expressions/Mouth/Surprised.png"

# ============================================================
# Standalone HJ images (used by Core_Handjob.rpy)
# ============================================================
image ntw hj_hide_hand = ConditionSwitch(
    "store._hj_girl and store._hj_girl.Over == 'yellow_jacket'",
    Composite(
        (1920, 1080),
        (0, 0), "images/characters/Negasonic/Handjob/Hide Hand.png",
        (0, 0), "images/characters/Negasonic/Handjob/Clothes/Over/Yellow Jacket/Yellow Jacket Hide Hand.png",
    ),
    True,
    "images/characters/Negasonic/Handjob/Hide Hand.png"
)

image ntw hj_hand = "images/characters/Negasonic/Handjob/Negasonic HJ Hand.png"
image ntw hj_palm = "images/characters/Negasonic/Handjob/Negasonic HJ Palm.png"
image ntw hj_thumb = "images/characters/Negasonic/Handjob/Negasonic HJ Thumb.png"

# Player Actions — shared from Player/{skin}/HJ/
image ntw hj_squeeze_left  = _p("HJ/Guy Hands Squeeze Left.png")
image ntw hj_squeeze_right = _p("HJ/Guy Hands Squeeze Right.png")
image ntw hj_slap_right = _p("HJ/Guy Hand Smack Right.png")
image ntw hj_slap_left  = _p("HJ/Guy Hand Smack Left.png")

# Penis — shared from Player/{skin}/HJ/, cum overlay per-girl
image ntw hj_penis = ConditionSwitch(
    "store._hj_girl and 'penis' in getattr(store._hj_girl, 'Cum', [])",
    Composite(
        (1920, 1080),
        (0, 0), _p("HJ/HJ Penis.png"),
        (0, 15), "images/characters/Negasonic/Handjob/Cum/Negasonic HJ Cum Penis.png",
    ),
    "True",
    _p("HJ/HJ Penis.png"),
)
