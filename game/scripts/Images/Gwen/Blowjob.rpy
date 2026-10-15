layeredimage gwen blowjob:

    # --------------------------------------------------------
    # Layer order (bottom -> top):
    # Legs -> Chest -> Torso -> Jaw -> Penis (mid) -> Head -> Mouth -> Eyes -> Brows
    # --------------------------------------------------------

    # LEGS
    group legs:
        attribute legs_base default:
            preg_art("gwen", "Blowjob/Legs.png")

    group legs_clothes:
        attribute legs_clothes_none default:
            Null()
        attribute legs_blue_skirt:
            preg_art("gwen", "Blowjob/Clothes/Legs/Blue Skirt/Blue Skirt.png")

    group legs_thighs:
        attribute legs_thighs_none default:
            Null()
        attribute legs_thigh_highs:
            "images/characters/Gwen/Blowjob/Clothes/Thigh Highs.png"

    group panties:
        attribute panties_none default:
            Null()
        attribute panties_purple:
            "images/characters/Gwen/Blowjob/Clothes/Panties/Purple Panties/Purple Panties.png"
        attribute panties_bikini:
            "images/characters/Gwen/Blowjob/Clothes/Panties/Black Bikini Bottom/Black bikini panties.png"

    group torso_corset:
        attribute torso_corset_none default:
            Null()
        attribute corset:
            "images/characters/Gwen/Blowjob/Clothes/Chest/Corset/Base.png"

    # --------------------------------------------------------
    # TORSO (ConditionSwitch: hand action + Over state)
    # --------------------------------------------------------
    group torso:
        attribute torso_auto default:
            ConditionSwitch(
                "bj_torso_type == 3",
                "images/characters/Gwen/Blowjob/BJ Torso 3.png",
                "bj_torso_type == 2 and store._bj_girl and store._bj_girl.Over",
                "images/characters/Gwen/Blowjob/Clothes/Over/Long Shirt/BJ Torso.png",
                "bj_torso_type == 2",
                "images/characters/Gwen/Blowjob/BJ Torso 2.png",
                True,
                "images/characters/Gwen/Blowjob/BJ Torso.png"
            )

    # --------------------------------------------------------
    # CHEST (BODY / PIERCING) — acima do torso
    # Corset hides naked chest; boobs_clothes shows corset overlay
    # --------------------------------------------------------
    # CHEST BODY — always visible
    group chest_body:
        attribute chest_none default:
            preg_art("gwen", "Blowjob/Gwen Chest.png")
        attribute chest_piercing:
            preg_art("gwen", "Blowjob/Gwen Chest Piercings.png")

    group boobs_clothes:
        attribute boobs_clothes_none default:
            Null()
        attribute boobs_clothes_1:
            preg_art("gwen", "Blowjob/Clothes/Chest/Corset/Cover.png")
        attribute boobs_clothes_2:
            preg_art("gwen", "Blowjob/Clothes/Chest/Corset/Cover.png")
        attribute boobs_bikini_top:
            preg_art("gwen", "Blowjob/Clothes/Chest/Black Bikini Top/Black bikini Top.png")
        attribute boobs_bikini_top_up:
            preg_art("gwen", "Blowjob/Clothes/Chest/Black Bikini Top/Black bikini Top Up.png")

    # MID (placeholder)
    group mid:
        attribute mid_none default:
            Null()

    group torso_arms:
        attribute torso_arms_none default:
            Null()
        attribute over_long_shirt:
            ConditionSwitch(
                "bj_torso_type == 3",
                "images/characters/Gwen/Blowjob/Clothes/Over/Long Shirt/BJ Torso 3 Long Shirt.png",
                "bj_torso_type == 2", Null(),
                True, "images/characters/Gwen/Blowjob/Clothes/Over/Long Shirt/BJ Body.png"
            )

    # --------------------------------------------------------
    # CUM BODY LAYERS (acima do corpo/roupas)
    # --------------------------------------------------------
    group cum_boobs:
        attribute cum_boobs_auto default:
            ConditionSwitch(
                "store._bj_girl and 'boobs' in getattr(store._bj_girl, 'Cum', [])",
                "images/characters/Gwen/Blowjob/Cum/Gwen BJ Boobs Cum.png",
                "True", Null()
            )

    # PENIS IS SHOWN SEPARATELY (CORNER, NO MOVEMENT)
    group penis_mid:
        attribute penis_mid default:
            Null()

    # FACE IS IN SEPARATE LAYER (blowjob_head)

layeredimage gwen blowjob_head:

    # HEAD
    group head:
        attribute head_base default:
            "images/characters/Gwen/Blowjob/Head/BJ Head.png"

    group cheeks:
        attribute cheeks_auto default:
            ConditionSwitch(
                "bj_cheeks", "images/characters/Gwen/Blowjob/Cheeks Sucking.png",
                "True",      Null()
            )

    # --------------------------------------------------------
    # BLUSH (acima da head, abaixo das expressions)
    # --------------------------------------------------------
    group blush:
        attribute blush_auto default:
            ConditionSwitch(
                "_gs('bj', 'blush', 0) == 2",
                "images/characters/Gwen/Blowjob/Head/Gwen BJ Face Blush 2.png",
                "_gs('bj', 'blush', 0) == 1",
                "images/characters/Gwen/Blowjob/Head/Gwen BJ Face Blush 1.png",
                "True", Null()
            )

    # CUM FACE / HEAD — movido para layers separados (bj_cum_face)
    # para ficar ACIMA do penis (zorder 10025) em vez de preso ao head (10015).

    # MOUTH
    # lick  -> mouth_tongue  (lingua, Jaw 1 fica visivel por baixo)
    # suck  -> mouth_sucking (default, speed-based)
    group mouth:
        attribute mouth_none:
            Null()
        attribute mouth_tongue:
            "images/characters/Gwen/Blowjob/Expressions/Mouth/Tongue.png"
        attribute mouth_sucking default:
            Null()  # handled by gwen bj_sucking_mouth (separate layer, zorder 10030)
        attribute mouth_normal:
            "images/characters/Gwen/Blowjob/Expressions/Mouth/Smile.png"
        attribute mouth_smile:
            "images/characters/Gwen/Blowjob/Expressions/Mouth/Smile.png"
        attribute mouth_happy:
            "images/characters/Gwen/Blowjob/Expressions/Mouth/Happy.png"
        attribute mouth_lipbite:
            "images/characters/Gwen/Blowjob/Expressions/Mouth/Lipbite.png"
        attribute mouth_sad:
            "images/characters/Gwen/Blowjob/Expressions/Mouth/Sad.png"
        attribute mouth_surprised:
            "images/characters/Gwen/Blowjob/Expressions/Mouth/Surprised.png"
        attribute mouth_angry:
            "images/characters/Gwen/Blowjob/Expressions/Mouth/Angry.png"
        attribute mouth_screaming:
            "images/characters/Gwen/Blowjob/Expressions/Mouth/Screamming.png"
        attribute mouth_scared:
            "images/characters/Gwen/Blowjob/Expressions/Mouth/Scared.png"

    # CUM MOUTH — movido para layer separado (bj_cum_face).

    # EYES — bj_blink fecha os olhos; bj_eyes escolhe a expressao
    group eyes:
        attribute eyes_auto default:
            ConditionSwitch(
                "store.hiding_face or bj_blink", "images/characters/Gwen/Blowjob/Expressions/Eyes/Closed.png",
                "bj_eyes == 'squint_2'",       "images/characters/Gwen/Blowjob/Expressions/Eyes/Squint 2.png",
                "bj_eyes == 'squint'",         "images/characters/Gwen/Blowjob/Expressions/Eyes/Squint.png",
                "bj_eyes == 'left_closed'",    "images/characters/Gwen/Blowjob/Expressions/Eyes/Left Closed.png",
                "bj_eyes == 'right_closed'",   "images/characters/Gwen/Blowjob/Expressions/Eyes/Right Closed.png",
                "bj_eyes == 'looking_left'",   "images/characters/Gwen/Blowjob/Expressions/Eyes/Looking Left.png",
                "bj_eyes == 'looking_right'",  "images/characters/Gwen/Blowjob/Expressions/Eyes/Looking Right.png",
                "bj_eyes == 'ahegao'",         "images/characters/Gwen/Blowjob/Expressions/Eyes/Ahegao.png",
                "bj_eyes == 'ahegao_2'",       "images/characters/Gwen/Blowjob/Expressions/Eyes/Ahegao 2.png",
                "bj_eyes == 'closed_happy'",   "images/characters/Gwen/Blowjob/Expressions/Eyes/Closed Happy.png",
                "bj_eyes == 'up_left_closed'", "images/characters/Gwen/Blowjob/Expressions/Eyes/Up Left Closed.png",
                "bj_eyes == 'up_right_closed'","images/characters/Gwen/Blowjob/Expressions/Eyes/Up Right Closed.png",
                "True",                        "images/characters/Gwen/Blowjob/Expressions/Eyes/Normal.png"
            )

    # BROWS — bj_brows (1-5) escolhe a sobrancelha
    group brows:
        attribute brows_auto default:
            ConditionSwitch(
                "bj_brows == 2", "images/characters/Gwen/Blowjob/Expressions/Brows/Sad.png",
                "bj_brows == 3", "images/characters/Gwen/Blowjob/Expressions/Brows/Perplexed.png",
                "bj_brows == 4", "images/characters/Gwen/Blowjob/Expressions/Brows/Perplexed 2.png",
                "bj_brows == 5", "images/characters/Gwen/Blowjob/Expressions/Brows/Angry.png",
                "True",          "images/characters/Gwen/Blowjob/Expressions/Brows/Normal.png"
            )

layeredimage gwen blowjob_jaw:

    # JAW (fixed)
    group jaw:
        attribute jaw_auto default:
            "images/characters/Gwen/Blowjob/Jaw 1.png"
        attribute jaw_1:
            "images/characters/Gwen/Blowjob/Jaw 1.png"
        attribute jaw_2:
            "images/characters/Gwen/Blowjob/Jaw 2.png"

image gwen bj_penis = ConditionSwitch(
    "store._bj_girl and 'penis' in getattr(store._bj_girl, 'Cum', [])",
    Composite(
        (1920, 1080),
        (0, 0), _p("BJ/BJ Penis.png"),
        (0, 0), "images/characters/Gwen/Blowjob/Cum/Gwen BJ Penis Cum.png",
    ),
    "True",
    _p("BJ/BJ Penis.png"),
)
image gwen bj_penis_guy = _p("BJ/BJ Penis Guy.png")
image gwen bj_arm = ConditionSwitch(
    "store._bj_girl and store._bj_girl.Over == 'long_shirt'",
    "images/characters/Gwen/Blowjob/Clothes/Over/Long Shirt/BJ Arm.png",
    True,
    "images/characters/Gwen/Blowjob/Arm Torso 2.png"
)
image gwen bj_hand           = "images/characters/Gwen/Blowjob/BJ Hand.png"
image gwen bj_forcing_hands_left  = _p("BJ/BJ Forcing Hands Left.png")
image gwen bj_forcing_hands_right = _p("BJ/BJ Forcing Hands Right.png")
image gwen bj_slap_right = _p("BJ/BJ Guy Hand Smack Right.png")
image gwen bj_slap_left  = _p("BJ/BJ Guy Hand Smack Left.png")

image gwen bj_hide_hand_left = ConditionSwitch(
    "store._bj_girl and store._bj_girl.Over == 'long_shirt'",
    Composite(
        (1920, 1080),
        (0, 0), "images/characters/Gwen/Blowjob/Hide Hand Left.png",
        (0, 0), "images/characters/Gwen/Blowjob/Clothes/Over/Long Shirt/Hide Hand Left.png",
    ),
    True,
    "images/characters/Gwen/Blowjob/Hide Hand Left.png"
)
image gwen bj_hide_hand_right = ConditionSwitch(
    "store._bj_girl and store._bj_girl.Over == 'long_shirt'",
    Composite(
        (1920, 1080),
        (0, 0), "images/characters/Gwen/Blowjob/Hide Hand Right.png",
        (0, 0), "images/characters/Gwen/Blowjob/Clothes/Over/Long Shirt/Hide Hand Right.png",
    ),
    True,
    "images/characters/Gwen/Blowjob/Hide Hand Right.png"
)

# Face cum layers — separados do blowjob_head para ficarem ACIMA do penis (zorder 10025).
# Cada sub-layer avalia independentemente via ConditionSwitch.
image gwen bj_cum_face = Composite(
    (1920, 1080),
    (0, 0), ConditionSwitch(
        "store._bj_girl and 'face' in getattr(store._bj_girl, 'Cum', [])",
        "images/characters/Gwen/Blowjob/Cum/Gwen BJ Face Cum.png",
        "True", Null()
    ),
    (0, 0), ConditionSwitch(
        "store._bj_girl and 'head' in getattr(store._bj_girl, 'Cum', [])",
        "images/characters/Gwen/Blowjob/Cum/Gwen BJ Head Cum.png",
        "True", Null()
    ),
)

# Mouth cum — layer separado abaixo do penis (zorder 9987)
image gwen bj_cum_mouth = ConditionSwitch(
    "store._bj_girl and 'mouth' in getattr(store._bj_girl, 'Cum', [])",
    "images/characters/Gwen/Blowjob/Cum/Gwen BJ Mouth Cum.png",
    "True", Null()
)

# Face cum 2 — parte do cum que fica ABAIXO do penis e ACIMA do jaw (zorder 9986).
image gwen bj_cum_face_under = ConditionSwitch(
    "store._bj_girl and 'face' in getattr(store._bj_girl, 'Cum', [])",
    "images/characters/Gwen/Blowjob/Cum/Gwen BJ Face Cum 2.png",
    "True", Null()
)

# Sucking mouth — layer separado mostrado pelo Core com zorder 10030 (acima de tudo)
image gwen bj_sucking_mouth = ConditionSwitch(
    "bj_speed <= 1", "images/characters/Gwen/Blowjob/Expressions/Mouth/Sucking 1.png",
    "bj_speed == 2", "images/characters/Gwen/Blowjob/Expressions/Mouth/Sucking 2.png",
    "bj_speed >= 3", "images/characters/Gwen/Blowjob/Expressions/Mouth/Sucking 3.png"
)

# Sucking below — lower lip/chin visible below penis during rise
image gwen bj_sucking_below = "images/characters/Gwen/Blowjob/Expressions/Mouth/Sucking Below.png"
