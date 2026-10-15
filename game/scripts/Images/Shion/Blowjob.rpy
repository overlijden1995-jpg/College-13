layeredimage shion blowjob:

    # --------------------------------------------------------
    # Layer order (bottom -> top):
    # Legs -> Panties -> Body (Torso 1/2) -> Pants -> Chest -> Clothes -> Cum
    # --------------------------------------------------------

    # LEGS
    always:
        preg_art("shion", "Blowjob/Legs.png")

    group legs_clothes:
        attribute legs_none default:
            Null()

    group shoes:
        attribute shoes_none default:
            Null()

    group panties:
        attribute panties_none default:
            Null()
        attribute panties_bikini:
            "images/characters/Shion/Blowjob/Clothes/Bikini Bottom.png"
        attribute panties_on:
            "images/characters/Shion/Blowjob/Clothes/Panties.png"

    # TORSO (bj_torso_type 1/2)
    always:
        ConditionSwitch(
            "bj_torso_type == 2", "images/characters/Shion/Blowjob/Torso 2.png",
            "True", "images/characters/Shion/Blowjob/Torso 1.png"
        )

    # BELLY (pregnancy)
    always:
        preg_art("shion", "+Blowjob/preg")

    # PANTS (below chest: her chest/piercing renders above her pants)
    group pants:
        attribute pants_none default:
            Null()
        attribute pants_on:
            "images/characters/Shion/Blowjob/Clothes/Pants.png"

    # --------------------------------------------------------
    # CHEST
    # --------------------------------------------------------
    group chest_body:
        attribute chest_none default:
            preg_art("shion", "Blowjob/Chest/Chest.png")
        attribute chest_piercing:
            preg_art("shion", "Blowjob/Chest/Chest Piercing.png")
        attribute chest_hidden:
            Null()

    # CHEST CLOTHING
    group boobs_clothes:
        attribute boobs_clothes_none default:
            Null()
        attribute boobs_bikini_top:
            preg_art("shion", "Blowjob/Clothes/Bikini Top.png")
        attribute boobs_bra:
            preg_art("shion", "Blowjob/Clothes/Bra.png")

    # MID CLOTHING
    group mid_clothing:
        attribute mid_none default:
            Null()
        attribute over_vest:
            "images/characters/Shion/Blowjob/Clothes/Vest.png"

    # OVER CLOTHING
    group over:
        attribute over_none default:
            Null()
        attribute over_jacket_1:
            "images/characters/Shion/Blowjob/Clothes/Jacket 1.png"
        attribute over_jacket_2:
            "images/characters/Shion/Blowjob/Clothes/Jacket 2.png"

    # ARM CLOTHING
    group arm_clothing:
        attribute arm_clothing_none default:
            Null()
        attribute arm_clothing_on:
            "images/characters/Shion/Blowjob/Clothes/Arm Clothing.png"

    # --------------------------------------------------------
    # CUM BODY
    # --------------------------------------------------------
    group cum_boobs:
        attribute cum_boobs_auto default:
            ConditionSwitch(
                "store._bj_girl and 'boobs' in getattr(store._bj_girl, 'Cum', [])",
                "images/characters/Shion/Blowjob/Cum/Boobs Cum.png",
                "True", Null()
            )

    group cum_extra:
        attribute cum_extra_auto default:
            Null()

    group penis_mid:
        attribute penis_mid default:
            Null()

# ============================================================
# HEAD (separate layeredimage for bobbing)
# ============================================================
layeredimage shion blowjob_head:

    # HEAD. "Head Top" has the mouth cut out: the penis shows through it while she works (has_head_normal,
    # scene_config: speed 0, speaking and narration use the full "Head", head_normal, like Tenny). "Head Sucking" is
    # Head Top with the cheeks sucked in (bj_cheeks, the cycle thread of Core_Blowjob) where the other girls overlay
    # a "Cheeks Sucking" patch on a full head.
    group head:
        attribute head_base default:
            ConditionSwitch(
                "bj_cheeks", "images/characters/Shion/Blowjob/Head Sucking.png",
                "True",      "images/characters/Shion/Blowjob/Head Top.png",
            )
        attribute head_normal:
            "images/characters/Shion/Blowjob/Head.png"

    # BLUSH
    group blush:
        attribute blush_auto default:
            Null()

    # MOUTH
    group mouth:
        attribute mouth_none:
            Null()
        attribute mouth_tongue:
            "images/characters/Shion/Blowjob/Expression/Mouth/Tongue.png"
        attribute mouth_sucking default:
            Null()
        attribute mouth_smile:
            "images/characters/Shion/Blowjob/Expression/Mouth/Smile.png"
        attribute mouth_happy:
            "images/characters/Shion/Blowjob/Expression/Mouth/Happy.png"
        attribute mouth_lipbite:
            "images/characters/Shion/Blowjob/Expression/Mouth/Lipbite.png"
        attribute mouth_sad:
            "images/characters/Shion/Blowjob/Expression/Mouth/Sad.png"
        attribute mouth_surprised:
            "images/characters/Shion/Blowjob/Expression/Mouth/Surprised.png"
        attribute mouth_angry:
            "images/characters/Shion/Blowjob/Expression/Mouth/Angry.png"
        attribute mouth_screaming:
            "images/characters/Shion/Blowjob/Expression/Mouth/Screaming.png"
        attribute mouth_scared:
            "images/characters/Shion/Blowjob/Expression/Mouth/Scared.png"
        attribute mouth_kiss:
            "images/characters/Shion/Blowjob/Expression/Mouth/Kiss.png"
        attribute mouth_normal:
            "images/characters/Shion/Blowjob/Expression/Mouth/Normal.png"

    # EYES
    group eyes:
        attribute eyes_auto default:
            ConditionSwitch(
                "store.hiding_face or bj_blink", "images/characters/Shion/Blowjob/Expression/Eyes/Closed.png",
                "bj_eyes == 'squint_2'",         "images/characters/Shion/Blowjob/Expression/Eyes/Squint 2.png",
                "bj_eyes == 'squint'",           "images/characters/Shion/Blowjob/Expression/Eyes/Squint.png",
                "bj_eyes == 'left_closed'",      "images/characters/Shion/Blowjob/Expression/Eyes/Left Closed.png",
                "bj_eyes == 'right_closed'",     "images/characters/Shion/Blowjob/Expression/Eyes/Right Closed.png",
                "bj_eyes == 'looking_left'",     "images/characters/Shion/Blowjob/Expression/Eyes/Looking Left.png",
                "bj_eyes == 'looking_right'",    "images/characters/Shion/Blowjob/Expression/Eyes/Looking Right.png",
                "bj_eyes == 'looking_down'",     "images/characters/Shion/Blowjob/Expression/Eyes/Looking Down.png",
                "bj_eyes == 'looking_down_surprised'", "images/characters/Shion/Blowjob/Expression/Eyes/Looking Down Surprised.png",
                "bj_eyes == 'ahegao'",           "images/characters/Shion/Blowjob/Expression/Eyes/Ahegao.png",
                "bj_eyes == 'ahegao_2'",         "images/characters/Shion/Blowjob/Expression/Eyes/Ahegao 2.png",
                "bj_eyes == 'closed_happy'",     "images/characters/Shion/Blowjob/Expression/Eyes/Closed Happy.png",
                "bj_eyes == 'up_left_closed'",   "images/characters/Shion/Blowjob/Expression/Eyes/Up Left Closed.png",
                "bj_eyes == 'up_right_closed'",  "images/characters/Shion/Blowjob/Expression/Eyes/Up Right Closed.png",
                "bj_eyes == 'surprised'",        "images/characters/Shion/Blowjob/Expression/Eyes/Surprised.png",
                "True",                          "images/characters/Shion/Blowjob/Expression/Eyes/Normal.png"
            )

    # BROWS
    group brows:
        attribute brows_auto default:
            ConditionSwitch(
                "bj_brows == 2", "images/characters/Shion/Blowjob/Expression/Brows/Sad.png",
                "bj_brows == 3", "images/characters/Shion/Blowjob/Expression/Brows/Perplexed.png",
                "bj_brows == 4", "images/characters/Shion/Blowjob/Expression/Brows/Perplexed 2.png",
                "bj_brows == 5", "images/characters/Shion/Blowjob/Expression/Brows/Angry.png",
                "bj_brows == 6", "images/characters/Shion/Blowjob/Expression/Brows/Determined.png",
                "bj_brows == 7", "images/characters/Shion/Blowjob/Expression/Brows/Worried.png",
                "True",          "images/characters/Shion/Blowjob/Expression/Brows/Normal.png"
            )

# ============================================================
# JAW (separate -- follows head_transform)
# ============================================================
layeredimage shion blowjob_jaw:

    group jaw:
        attribute jaw_auto default:
            "images/characters/Shion/Blowjob/Jaw.png"
        attribute jaw_1:
            "images/characters/Shion/Blowjob/Jaw.png"
        attribute jaw_2:
            "images/characters/Shion/Blowjob/Jaw.png"

# ============================================================
# STANDALONE IMAGES
# ============================================================

# His side of the scene = Gwen's (author, 2026-10-05, for the tests): the standard BJ penis, penis-with-guy and
# forcing hands from Player/<skin>/BJ, no separate guy body (the POV "HJ BJ" set is Tenny's). The artist's
# Shion/Blowjob/Guy folder (Guy.png / Penis.png) is not drawn.
image shion bj_penis = _p("BJ/BJ Penis.png")
image shion bj_penis_guy = _p("BJ/BJ Penis Guy.png")

image shion bj_arm = "images/characters/Shion/Blowjob/Arm.png"

image shion bj_hand = "images/characters/Shion/Blowjob/Hand.png"

image shion bj_forcing_hands_left  = _p("BJ/BJ Forcing Hands Left.png")
image shion bj_forcing_hands_right = _p("BJ/BJ Forcing Hands Right.png")

image shion bj_slap_right = _p("BJ/BJ Guy Hand Smack Right.png")
image shion bj_slap_left  = _p("BJ/BJ Guy Hand Smack Left.png")

image shion bj_cum_face = ConditionSwitch(
    "store._bj_girl and 'face' in getattr(store._bj_girl, 'Cum', [])",
    "images/characters/Shion/Blowjob/Cum/Face Cum.png",
    "True", Null()
)

image shion bj_cum_mouth = ConditionSwitch(
    "store._bj_girl and 'mouth' in getattr(store._bj_girl, 'Cum', [])",
    "images/characters/Shion/Blowjob/Cum/Mouth Cum.png",
    "True", Null()
)

image shion bj_cum_head = ConditionSwitch(
    "store._bj_girl and 'head' in getattr(store._bj_girl, 'Cum', [])",
    "images/characters/Shion/Blowjob/Cum/Head Cum.png",
    "True", Null()
)

image shion bj_cum_penis = ConditionSwitch(
    "store._bj_girl and 'penis' in getattr(store._bj_girl, 'Cum', [])",
    "images/characters/Shion/Blowjob/Cum/Penis Cum.png",
    "True", Null()
)

image shion bj_sucking_mouth = ConditionSwitch(
    "bj_speed <= 1", "images/characters/Shion/Blowjob/Sucking Mouths/Sucking 1.png",
    "bj_speed == 2", "images/characters/Shion/Blowjob/Sucking Mouths/Sucking 2.png",
    "bj_speed >= 3", "images/characters/Shion/Blowjob/Sucking Mouths/Sucking 3.png"
)

image shion bj_sucking_below = "images/characters/Shion/Blowjob/Sucking Mouths/Sucking Below.png"

image shion bj_legs = "images/characters/Shion/Blowjob/Legs.png"
