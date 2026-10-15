layeredimage gwen handjob:

    # BASE (never moves)
    always:
        ConditionSwitch(
            "store.hiding_face",
            preg_art("gwen", "Handjob/Torso 2.png"),
            "True",
            preg_art("gwen", "Handjob/Torso Head.png")
        )

    # MID (placeholder)
    group mid:
        attribute mid_none default:
            Null()

    # OVER (below chest)
    group over:
        attribute over_none default:
            Null()
        attribute over_long_shirt:
            ConditionSwitch(
                "store.hiding_face",
                "images/characters/Gwen/Handjob/Clothes/Over/Long Shirt/HJ Torso 2 Long Shirt.png",
                "True",
                "images/characters/Gwen/Handjob/Clothes/Over/Long Shirt/HJ.png"
            )

    # --------------------------------------------------------
    # CORSET BOTTOM (abaixo do chest, visivel quando corset ativo)
    # --------------------------------------------------------
    group chest_base:
        attribute chest_base_none default:
            Null()
        attribute chest_base_on:
            preg_art("gwen", "Handjob/Clothes/Chest/Corset/Base.png")

    # --------------------------------------------------------
    # CHEST BODY — always visible (nude base)
    # --------------------------------------------------------
    group chest_body:
        attribute chest_none default:
            preg_art("gwen", "Handjob/Gwen Chest.png")
        attribute chest_piercing:
            preg_art("gwen", "Handjob/Gwen Chest Piercing.png")

    # CHEST CLOTHING — overlay on top of body
    group chest_clothing:
        attribute chest_clothes_none default:
            Null()
        attribute chest_corset:
            preg_art("gwen", "Handjob/Clothes/Chest/Corset/Cover.png")
        attribute chest_corset_down:
            Null()
        attribute chest_bikini_top:
            preg_art("gwen", "Handjob/Clothes/Chest/Black Bikini Top/Black bikini Top.png")
        attribute chest_bikini_top_up:
            preg_art("gwen", "Handjob/Clothes/Chest/Black Bikini Top/Black bikini Top Up.png")

    # COLLAR
    group collar:
        attribute collar_none default:
            Null()
        attribute collar_on:
            "images/characters/Gwen/Handjob/Clothes/Gwen HJ Collar.png"

    # --------------------------------------------------------
    # CUM BODY LAYERS (acima do corpo/roupas)
    # --------------------------------------------------------
    group cum_boobs:
        attribute cum_boobs_none default:
            Null()
        attribute cum_boobs_on:
            "images/characters/Gwen/Handjob/Cum/Gwen HJ Boobs Cum.png"

    # --------------------------------------------------------
    # BLUSH (acima do corpo, abaixo das expressions)
    # --------------------------------------------------------
    group blush:
        attribute blush_0 default:
            Null()
        attribute blush_1:
            "images/characters/Gwen/Handjob/Head/Gwen HJ Blush 1.png"
        attribute blush_2:
            "images/characters/Gwen/Handjob/Head/Gwen HJ Blush 2.png"

    # --------------------------------------------------------
    # CUM FACE (acima da head/blush)
    # --------------------------------------------------------
    group cum_face:
        attribute cum_face_none default:
            Null()
        attribute cum_face_on:
            "images/characters/Gwen/Handjob/Cum/Gwen HJ Face Cum.png"

    # BROWS
    group brows:
        attribute brows_normal default:
            "images/characters/Gwen/Handjob/Expressions/Brows/Normal.png"
        attribute brows_confused:
            "images/characters/Gwen/Handjob/Expressions/Brows/Perplexed.png"
        attribute brows_surprised:
            "images/characters/Gwen/Handjob/Expressions/Brows/Angry.png"
        attribute brows_sad:
            "images/characters/Gwen/Handjob/Expressions/Brows/Sad.png"

    # EYES (ConditionSwitch per attribute: hj_blink -> Closed.png)
    group eyes:
        attribute eyes_normal default:
            ConditionSwitch(
                "hj_blink", "images/characters/Gwen/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Gwen/Handjob/Expressions/Eyes/Normal.png",
            )
        attribute eyes_side:
            ConditionSwitch(
                "hj_blink", "images/characters/Gwen/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Gwen/Handjob/Expressions/Eyes/Looking Left.png",
            )
        attribute eyes_side_2:
            ConditionSwitch(
                "hj_blink", "images/characters/Gwen/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Gwen/Handjob/Expressions/Eyes/Looking Right.png",
            )
        attribute eyes_looking_right:
            ConditionSwitch(
                "hj_blink", "images/characters/Gwen/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Gwen/Handjob/Expressions/Eyes/Looking Right.png",
            )
        attribute eyes_squint:
            ConditionSwitch(
                "hj_blink", "images/characters/Gwen/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Gwen/Handjob/Expressions/Eyes/Squint.png",
            )
        attribute eyes_squint_big:
            ConditionSwitch(
                "hj_blink", "images/characters/Gwen/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Gwen/Handjob/Expressions/Eyes/Squint Normal.png",
            )
        attribute eyes_surprised:
            ConditionSwitch(
                "hj_blink", "images/characters/Gwen/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Gwen/Handjob/Expressions/Eyes/Surprised.png",
            )
        attribute eyes_surprised_2:
            ConditionSwitch(
                "hj_blink", "images/characters/Gwen/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Gwen/Handjob/Expressions/Eyes/Surprised.png",
            )
        attribute eyes_closed:
            "images/characters/Gwen/Handjob/Expressions/Eyes/Closed.png"
        attribute eyes_left_closed:
            ConditionSwitch(
                "hj_blink", "images/characters/Gwen/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Gwen/Handjob/Expressions/Eyes/Blink Left.png",
            )
        attribute eyes_right_closed:
            ConditionSwitch(
                "hj_blink", "images/characters/Gwen/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Gwen/Handjob/Expressions/Eyes/Blink Right.png",
            )
        attribute eyes_squint_2:
            ConditionSwitch(
                "hj_blink", "images/characters/Gwen/Handjob/Expressions/Eyes/Closed.png",
                "True", "images/characters/Gwen/Handjob/Expressions/Eyes/Squint Normal.png",
            )

    # MOUTH
    group mouth:
        attribute mouth_normal default:
            "images/characters/Gwen/Handjob/Expressions/Mouth/Normal.png"
        attribute mouth_smile:
            "images/characters/Gwen/Handjob/Expressions/Mouth/Lipbite.png"
        attribute mouth_laugh:
            "images/characters/Gwen/Handjob/Expressions/Mouth/Laugh.png"
        attribute mouth_surprised:
            "images/characters/Gwen/Handjob/Expressions/Mouth/Surprised.png"
        attribute mouth_tongue:
            "images/characters/Gwen/Handjob/Expressions/Mouth/Tongue.png"
        attribute mouth_open_teeth:
            "images/characters/Gwen/Handjob/Expressions/Mouth/Surprised.png"
        attribute mouth_disgusted:
            "images/characters/Gwen/Handjob/Expressions/Mouth/Surprised.png"
        attribute mouth_serious:
            "images/characters/Gwen/Handjob/Expressions/Mouth/Normal.png"
        attribute mouth_sad:
            "images/characters/Gwen/Handjob/Expressions/Mouth/Sad.png"
        attribute mouth_sch:
            "images/characters/Gwen/Handjob/Expressions/Mouth/Surprised.png"

image gwen hj_hide_hand = ConditionSwitch(
    "store._hj_girl and store._hj_girl.Over == 'long_shirt'",
    Composite(
        (1920, 1080),
        (0, 0), "images/characters/Gwen/Handjob/Hide Hand.png",
        (0, 0), "images/characters/Gwen/Handjob/Clothes/Over/Long Shirt/Long Shirt Hide Hand.png",
    ),
    True,
    "images/characters/Gwen/Handjob/Hide Hand.png"
)

image gwen hj_hand = "images/characters/Gwen/Handjob/Gwen Hand.png"
image gwen hj_palm  = "images/characters/Gwen/Handjob/Gwen HJ Palm.png"
image gwen hj_thumb = "images/characters/Gwen/Handjob/Gwen HJ Thumb.png"
image gwen hj_squeeze_left  = _p("HJ/Guy Hands Squeeze Left.png")
image gwen hj_squeeze_right = _p("HJ/Guy Hands Squeeze Right.png")
image gwen hj_slap_right = _p("HJ/Guy Hand Smack Right.png")
image gwen hj_slap_left  = _p("HJ/Guy Hand Smack Left.png")

image gwen hj_penis = ConditionSwitch(
    "store._hj_girl and 'penis' in getattr(store._hj_girl, 'Cum', [])",
    Composite(
        (1920, 1080),
        (0, 0), _p("HJ/HJ Penis.png"),
        (0, 15), "images/characters/Gwen/Handjob/Cum/Gwen HJ Penis Cum.png",
    ),
    "True",
    _p("HJ/HJ Penis.png"),
)
