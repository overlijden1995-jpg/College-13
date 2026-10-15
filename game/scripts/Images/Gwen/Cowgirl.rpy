# ============================================================
# Gwen Cowgirl Layered Sprite
# ============================================================

layeredimage gwen cowgirl:

    # 17. Guy (bottom — no longer used, kept for attribute compatibility)
    group guy:
        attribute guy_base default:
            Null()
        attribute guy_none:
            Null()

    # 16b. Arms Low (pose 2 below everything)
    group arms_low:
        attribute arms_low_none default:
            Null()
        attribute arms_low_2:
            "images/characters/Gwen/Cowgirl/Gwen Cowgirl Arms 2.png"

    # 16. Legs Bottom
    group legs_bottom:
        attribute legs_bottom_base default:
            "images/characters/Gwen/Cowgirl/Gwen Cowgirl Legs Bottom.png"
        attribute legs_bottom_none:
            Null()

    # 15. Panties Bottom (purple / bikini)
    group panties_bottom:
        attribute panties_bottom_none default:
            Null()
        attribute panties_bottom_1:
            "images/characters/Gwen/Cowgirl/Clothes/Panties/Purple Panties/Purple Panties.png"
        attribute panties_bottom_bikini:
            "images/characters/Gwen/Cowgirl/Clothes/Panties/Black Bikini Bottom/Black bikini panties.png"

    # 14. Penis
    group penis:
        attribute penis_none default:
            Null()
        attribute penis_on:
            _p("Cowgirl/Cowgirl Penis.png")

    # 13. Torso
    group torso:
        attribute torso_base default:
            preg_art("gwen", "Cowgirl/Gwen Cowgirl Torso.png")

    # 13b. Full belly (visual pregnancy stage 2): right above the torso, BELOW legs top / panties /
    # skirt / arms (the masturbation arm and the pulled-up skirt pass in front of it).
    always:
        preg_belly("gwen", "+Cowgirl/belly")

    # 12c. Shoulder Right (always visible)
    group shoulder_right:
        attribute shoulder_right_on default:
            ConditionSwitch(
                "store._cowgirl_girl and store._cowgirl_girl.Over == 'long_shirt'",
                "images/characters/Gwen/Cowgirl/Clothes/Over/Long Shirt/Gwen Shoulder Right Long Shirt.png",
                "True",
                "images/characters/Gwen/Cowgirl/Gwen Shoulder Right.png",
            )
        attribute shoulder_right_none:
            Null()

    # 12c. Shoulder Left (hidden during hide-face)
    group shoulder_left:
        attribute shoulder_left_on default:
            ConditionSwitch(
                "store._cowgirl_girl and store._cowgirl_girl.Over == 'long_shirt'",
                "images/characters/Gwen/Cowgirl/Clothes/Over/Long Shirt/Gwen Shoulder Left Long Shirt.png",
                "True",
                "images/characters/Gwen/Cowgirl/Gwen Shoulder Left.png",
            )
        attribute shoulder_left_none:
            Null()

    # 10. Legs Top
    group legs_top:
        attribute legs_top_base default:
            "images/characters/Gwen/Cowgirl/Gwen Cowgirl Legs Top.png"
        attribute legs_top_none:
            Null()

    # 11. Panties Top (purple / bikini — above legs so "down" state renders correctly)
    group panties_top:
        attribute panties_top_none default:
            Null()
        attribute panties_top_1:
            "images/characters/Gwen/Cowgirl/Clothes/Panties/Purple Panties/Purple Panties.png"
        attribute panties_top_2:
            "images/characters/Gwen/Cowgirl/Clothes/Panties/Purple Panties/Purple Panties Side Top.png"
        attribute panties_top_down:
            "images/characters/Gwen/Cowgirl/Clothes/Panties/Purple Panties/Purple Panties Down.png"
        attribute panties_top_bikini:
            "images/characters/Gwen/Cowgirl/Clothes/Panties/Black Bikini Bottom/Black bikini panties.png"
        attribute panties_top_bikini_side:
            "images/characters/Gwen/Cowgirl/Clothes/Panties/Black Bikini Bottom/Black bikini panties Side Top.png"
        attribute panties_top_bikini_down:
            "images/characters/Gwen/Cowgirl/Clothes/Panties/Black Bikini Bottom/Black bikini panties Down.png"

    # 9. Thigh-highs
    group thigh_highs:
        attribute thigh_highs_none default:
            Null()
        attribute thigh_highs_on:
            "images/characters/Gwen/Cowgirl/Clothes/Thigh Highs.png"

    # 9b. Skirt (pulled up around waist — top part only, bottom is standalone)
    group skirt:
        attribute skirt_none default:
            Null()
        attribute skirt_up:
            "images/characters/Gwen/Cowgirl/Clothes/Legs/Blue Skirt/Blue Skirt Up Top.png"

    # 12b. Torso Over (lowest priority — below arms, boobs and clothing)
    group torso_over:
        attribute torso_over_none default:
            Null()
        attribute torso_over_long_shirt:
            Null()

    # 8. Arms High (pose 1 above torso)
    group arms_high:
        attribute arms_high_none default:
            Null()
        attribute arms_high_1:
            "images/characters/Gwen/Cowgirl/Gwen Cowgirl Arms.png"
        attribute arms_high_clothed_1:
            "images/characters/Gwen/Cowgirl/Clothes/Over/Long Shirt/CG Arms 1.png"
        attribute arms_high_masturbate:
            "images/characters/Gwen/Cowgirl/Gwen Cowgirl Masturbation Naked.png"
        attribute arms_high_masturbate_ls:
            "images/characters/Gwen/Cowgirl/Clothes/Over/Long Shirt/CG Masturbation.png"

    # Masturbation hand overlay
    group masturbate_hand at cg_hand_rot:
        attribute masturbate_hand_none default:
            Null()
        attribute masturbate_hand_on:
            "images/characters/Gwen/Cowgirl/Gwen Masturbate Hand.png"

    # Cum on legs (below guy arms)
    group cum_legs:
        attribute cum_legs_auto default:
            ConditionSwitch(
                "store._cowgirl_girl and 'legs' in getattr(store._cowgirl_girl, 'Cum', [])",
                "images/characters/Gwen/Cowgirl/Cum/Gwen Cowgirl Legs Cum.png",
                "store._cowgirl_girl and 'dripping' in getattr(store._cowgirl_girl, 'Cum', []) and store._session_cum.get('inside', 0) >= 2",
                "images/characters/Gwen/Cowgirl/Cum/Gwen Cowgirl Legs Cum.png",
                "True", Null()
            )

    # Guy Arms — above cum, below boobs and clothing
    # Left/right arms now shown as standalone layers by COWGIRL_ApplySpeed
    group guy_arms:
        attribute guy_arms_on:
            Null()
        attribute guy_arms_none default:
            Null()

    # 12. Torso Clothing (higher priority)
    group torso_clothing:
        attribute torso_clothing_none default:
            Null()
        attribute torso_clothing_corset:
            preg_art("gwen", "Cowgirl/Clothes/Chest/Corset/Cover.png")
        attribute torso_clothing_corset_up:
            preg_art("gwen", "Cowgirl/Clothes/Chest/Corset/Base.png")

    # MID (placeholder)
    group mid:
        attribute mid_none default:
            Null()

    # 7. Boobs (standalone sprites only - animated via COWGIRL_ApplySpeed)
    group boobs:
        attribute boobs_none default:
            Null()
        attribute boobs_naked_1:
            preg_art("gwen", "Cowgirl/Gwen Cowgirl Boobs Base.png")
        attribute boobs_naked_2:
            preg_art("gwen", "Cowgirl/Gwen Cowgirl Boobs Base.png")
        attribute boobs_clothed_1:
            Null()
        attribute boobs_clothed_2:
            Null()

    # 5. Head
    group head at cg_head_rot:
        attribute head_base default:
            "images/characters/Gwen/Cowgirl/Head/Gwen Cowgirl Head.png"
        attribute head_base_bob:
            "images/characters/Gwen/Cowgirl/Head/Gwen Cowgirl Head.png"

    # 4b. Blush
    group blush at cg_head_rot:
        attribute blush_auto default:
            ConditionSwitch(
                "_gs('cowgirl', 'blush', 0) == 2",
                "images/characters/Gwen/Cowgirl/Head/Gwen Cowgirl Blush 2.png",
                "_gs('cowgirl', 'blush', 0) == 1",
                "images/characters/Gwen/Cowgirl/Head/Gwen Cowgirl Blush 1.png",
                "True", Null()
            )

    # 4. Mouth (1-7)
    group mouth at cg_head_rot:
        attribute mouth_normal default:
            "images/characters/Gwen/Cowgirl/Expressions/Mouth/Normal.png"
        attribute mouth_disgusted:
            "images/characters/Gwen/Cowgirl/Expressions/Mouth/Sad.png"
        attribute mouth_laugh:
            "images/characters/Gwen/Cowgirl/Expressions/Mouth/Laugh.png"
        attribute mouth_open_teeth:
            "images/characters/Gwen/Cowgirl/Expressions/Mouth/Moaning.png"
        attribute mouth_sch:
            "images/characters/Gwen/Cowgirl/Expressions/Mouth/Moaning 2.png"
        attribute mouth_serious:
            "images/characters/Gwen/Cowgirl/Expressions/Mouth/Moaning 3.png"
        attribute mouth_smile:
            "images/characters/Gwen/Cowgirl/Expressions/Mouth/Smile.png"
        attribute mouth_surprised:
            "images/characters/Gwen/Cowgirl/Expressions/Mouth/Moaning.png"
        attribute mouth_tongue:
            "images/characters/Gwen/Cowgirl/Expressions/Mouth/Tongue.png"
        attribute mouth_kissing:
            "images/characters/Gwen/Cowgirl/Expressions/Mouth/Kiss.png"

    # 3. Eyes (1-7)
    # Each attribute uses ConditionSwitch so the blink loop only needs to toggle
    # cg_blink — no renpy.show() call needed, slot_transform is never restarted.
    group eyes at cg_head_rot:
        attribute eyes_normal default:
            ConditionSwitch(
                "cg_blink", "images/characters/Gwen/Cowgirl/Expressions/Eyes/Closed.png",
                "True",     "images/characters/Gwen/Cowgirl/Expressions/Eyes/Normal.png"
            )
        attribute eyes_side:
            ConditionSwitch(
                "cg_blink", "images/characters/Gwen/Cowgirl/Expressions/Eyes/Closed.png",
                "True",     "images/characters/Gwen/Cowgirl/Expressions/Eyes/Away.png"
            )
        attribute eyes_side_2:
            ConditionSwitch(
                "cg_blink", "images/characters/Gwen/Cowgirl/Expressions/Eyes/Closed.png",
                "True",     "images/characters/Gwen/Cowgirl/Expressions/Eyes/Up.png"
            )
        attribute eyes_squint:
            ConditionSwitch(
                "cg_blink", "images/characters/Gwen/Cowgirl/Expressions/Eyes/Closed.png",
                "True",     "images/characters/Gwen/Cowgirl/Expressions/Eyes/Squint.png"
            )
        attribute eyes_squint_big:
            "images/characters/Gwen/Cowgirl/Expressions/Eyes/Bliss.png"
        attribute eyes_surprised:
            ConditionSwitch(
                "cg_blink", "images/characters/Gwen/Cowgirl/Expressions/Eyes/Closed.png",
                "True",     "images/characters/Gwen/Cowgirl/Expressions/Eyes/Surprised.png"
            )
        attribute eyes_surprised_2:
            ConditionSwitch(
                "cg_blink", "images/characters/Gwen/Cowgirl/Expressions/Eyes/Closed.png",
                "True",     "images/characters/Gwen/Cowgirl/Expressions/Eyes/Sexy.png"
            )
        attribute eyes_closed:
            "images/characters/Gwen/Cowgirl/Expressions/Eyes/Closed.png"
        attribute eyes_left_closed:
            "images/characters/Gwen/Cowgirl/Expressions/Eyes/Closed Left.png"
        attribute eyes_right_closed:
            "images/characters/Gwen/Cowgirl/Expressions/Eyes/Closed Right.png"
        attribute eyes_squint_2:
            ConditionSwitch(
                "cg_blink", "images/characters/Gwen/Cowgirl/Expressions/Eyes/Closed.png",
                "True",     "images/characters/Gwen/Cowgirl/Expressions/Eyes/Squint.png"
            )
        attribute eyes_ahegao:
            "images/characters/Gwen/Cowgirl/Expressions/Eyes/Ahegao.png"
        attribute eyes_ahegao_2:
            "images/characters/Gwen/Cowgirl/Expressions/Eyes/Ahegao 2.png"

    # 2. Eyebrows (1-5)
    group brows at cg_head_rot:
        attribute brows_normal default:
            "images/characters/Gwen/Cowgirl/Expressions/Brows/Normal.png"
        attribute brows_confused:
            "images/characters/Gwen/Cowgirl/Expressions/Brows/Sad.png"
        attribute brows_surprised:
            "images/characters/Gwen/Cowgirl/Expressions/Brows/Perplexed 1.png"
        attribute brows_horny:
            "images/characters/Gwen/Cowgirl/Expressions/Brows/Perplexed 2.png"

    # 0. Penis (optional, top)
    group penis_top:
        attribute penis_top_none default:
            Null()
        attribute penis_top_on:
            _p("Cowgirl/Cowgirl Penis Side.png")

image gwen cowgirl_penis = _p("Cowgirl/Cowgirl Penis.png")
image gwen cowgirl_penis_top = _p("Cowgirl/Cowgirl Penis Side.png")
image gwen cowgirl_guy_squeeze_left = _p("Cowgirl/Cowgirl Guy Hands Squeeze Left.png")
image gwen cowgirl_guy_squeeze_right = _p("Cowgirl/Cowgirl Guy Hands Squeeze Right.png")
image gwen cowgirl_guy_arms_left = _p("Cowgirl/Cowgirl Guy Arms Left.png")
image gwen cowgirl_guy_arms_right = _p("Cowgirl/Cowgirl Guy Arms Right.png")
image gwen cowgirl_pussy = "images/characters/Gwen/Cowgirl/Gwen Cowgirl Pussy.png"
image gwen cowgirl_legs_bottom = "images/characters/Gwen/Cowgirl/Gwen Cowgirl Legs Bottom.png"
image gwen cowgirl_skirt_bottom = "images/characters/Gwen/Cowgirl/Clothes/Legs/Blue Skirt/Blue Skirt Up Top Bottom.png"
image gwen cowgirl_panties_side_bottom = "images/characters/Gwen/Cowgirl/Clothes/Panties/Purple Panties/Purple Panties Side Bottom.png"
image gwen cowgirl_bikini_panties_side_bottom = "images/characters/Gwen/Cowgirl/Clothes/Panties/Black Bikini Bottom/Black bikini panties Side Bottom.png"
image gwen cowgirl_bikini_top = preg_art("gwen", "Cowgirl/Clothes/Chest/Black Bikini Top/Black bikini Top.png")
image gwen cowgirl_bikini_top_up = preg_art("gwen", "Cowgirl/Clothes/Chest/Black Bikini Top/Black bikini Top Up.png")
image gwen cowgirl_bikini_top_fixed = "images/characters/Gwen/Cowgirl/Clothes/Chest/Black Bikini Top/Black Bikini Top Fixed.png"
image gwen cowgirl_boobs_naked = preg_art("gwen", "Cowgirl/Gwen Cowgirl Boobs Base.png")
image gwen cowgirl_nipples = ConditionSwitch(
    "store._cowgirl_girl and getattr(store._cowgirl_girl, 'Piercing', False)",
    preg_art("gwen", "Cowgirl/Gwen Cowgirl Nipples Piercings.png"),
    "True",
    preg_art("gwen", "Cowgirl/Gwen Cowgirl Nipples.png")
)

# Cum layers (ConditionSwitch — auto-show when tag present in girl.Cum)
image gwen cowgirl_tummy_cum = ConditionSwitch(
    "store._cowgirl_girl and 'body' in getattr(store._cowgirl_girl, 'Cum', [])",
    "images/characters/Gwen/Cowgirl/Cum/Gwen Cowgirl Tummy Cum.png",
    "True", Null()
)
image gwen cowgirl_penis_cum = ConditionSwitch(
    "store._cowgirl_girl and 'body' in getattr(store._cowgirl_girl, 'Cum', [])",
    "images/characters/Gwen/Cowgirl/Cum/Gwen Cowgirl Penis Cum.png",
    "True", Null()
)
image gwen cowgirl_dripping_cum = ConditionSwitch(
    "store._cowgirl_girl and 'dripping' in getattr(store._cowgirl_girl, 'Cum', [])",
    "images/characters/Gwen/Cowgirl/Cum/Gwen Cowgirl Dripping Cum.png",
    "True", Null()
)
image gwen cowgirl_dripping_cum_2 = ConditionSwitch(
    "store._cowgirl_girl and 'dripping' in getattr(store._cowgirl_girl, 'Cum', []) and store._session_cum.get('inside', 0) >= 2",
    "images/characters/Gwen/Cowgirl/Cum/Gwen Cowgirl Dripping Cum 2.png",
    "True", Null()
)
image gwen cowgirl_legs_cum = ConditionSwitch(
    "store._cowgirl_girl and 'legs' in getattr(store._cowgirl_girl, 'Cum', [])",
    "images/characters/Gwen/Cowgirl/Cum/Gwen Cowgirl Legs Cum.png",
    "store._cowgirl_girl and 'dripping' in getattr(store._cowgirl_girl, 'Cum', []) and store._session_cum.get('inside', 0) >= 2",
    "images/characters/Gwen/Cowgirl/Cum/Gwen Cowgirl Legs Cum.png",
    "True", Null()
)
image gwen cowgirl_cum_face = ConditionSwitch(
    "store._cowgirl_girl and 'face' in getattr(store._cowgirl_girl, 'Cum', [])",
    "images/characters/Gwen/Cowgirl/Cum/Gwen Cowgirl Face.png",
    "True", Null()
)
image gwen cowgirl_hide_arm_left_1 = ConditionSwitch(
    "store._cowgirl_girl and store._cowgirl_girl.Over == 'long_shirt' and not store.cowgirl_masturbating",
    Composite(
        (1920, 1080),
        (0, 0), "images/characters/Gwen/Cowgirl/Hide Arm Left 1.png",
        (0, 0), "images/characters/Gwen/Cowgirl/Clothes/Over/Long Shirt/Hide Arm 1 Left Long Shirt.png",
    ),
    True,
    "images/characters/Gwen/Cowgirl/Hide Arm Left 1.png"
)
image gwen cowgirl_hide_arm_left_2 = "images/characters/Gwen/Cowgirl/Hide Arm Left 2.png"
image gwen cowgirl_hide_arm_left_2_over = ConditionSwitch(
    "store._cowgirl_girl and store._cowgirl_girl.Over == 'long_shirt'",
    "images/characters/Gwen/Cowgirl/Clothes/Over/Long Shirt/Hide Arm 2 Left Long Shirt.png",
    True,
    Null()
)
image gwen cowgirl_hide_arm_right = "images/characters/Gwen/Cowgirl/Hide Arm Right.png"
image gwen cowgirl_hide_arm_masturbate_right = ConditionSwitch(
    "store._cowgirl_girl and store._cowgirl_girl.Over == 'long_shirt'",
    Composite(
        (1920, 1080),
        (0, 0), "images/characters/Gwen/Cowgirl/Hide Arm Masturbate Right.png",
        (0, 0), "images/characters/Gwen/Cowgirl/Clothes/Over/Long Shirt/Hide Arm Masturbate Right Long Shirt.png",
    ),
    True,
    "images/characters/Gwen/Cowgirl/Hide Arm Masturbate Right.png"
)

image gwen cowgirl_slap_right = _p("Cowgirl/Cowgirl Guy Hand Smack Right.png")
image gwen cowgirl_slap_left  = _p("Cowgirl/Cowgirl Guy Hand Smack Left.png")
image gwen cowgirl_corset = preg_art("gwen", "Cowgirl/Clothes/Chest/Corset/Cover.png")
image gwen cowgirl_corset_up = preg_art("gwen", "Cowgirl/Clothes/Chest/Corset/Base.png")
image gwen cowgirl_shirt_top = Null()
image gwen cowgirl_masturbate_arm = "images/characters/Gwen/Cowgirl/Gwen Cowgirl Masturbation Naked.png"
image gwen cowgirl_masturbate_arm_ls = "images/characters/Gwen/Cowgirl/Clothes/Over/Long Shirt/CG Masturbation.png"
image gwen cowgirl_masturbate_hand = "images/characters/Gwen/Cowgirl/Gwen Masturbate Hand.png"
