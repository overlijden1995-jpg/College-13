# ============================================================
# Rogue Cowgirl Layered Sprite
# ============================================================
# Same structure as Gwen. No long shirt, no skirt.
# Crop Top replaces corset. Green Panties replaces purple.

layeredimage rogue cowgirl:

    # 17. Guy body (bottom - Rogue has no separate guy body, just arms above)
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
            "images/characters/Rogue/Cowgirl/Rogue Cowgirl Arms 2.png"

    # 16. Legs Bottom
    group legs_bottom:
        attribute legs_bottom_base default:
            "images/characters/Rogue/Cowgirl/Rogue Cowgirl Legs Bottom.png"
        attribute legs_bottom_none:
            Null()

    # 15. Panties Bottom (green panties / bikini)
    group panties_bottom:
        attribute panties_bottom_none default:
            Null()
        attribute panties_bottom_1:
            "images/characters/Rogue/Cowgirl/Clothes/Panties/Green Panties/Green Panties.png"
        attribute panties_bottom_bikini:
            "images/characters/Rogue/Cowgirl/Clothes/Panties/Green Bikini Bottom/Green Bikini.png"

    # 14. Penis
    group penis:
        attribute penis_none default:
            Null()
        attribute penis_on:
            _p("Cowgirl/Cowgirl Penis.png")

    # 13. Torso
    group torso:
        attribute torso_base default:
            preg_art("rogue", "Cowgirl/Rogue Cowgirl Torso.png")

    # Full belly (visual pregnancy stage 2): right above the torso, BELOW legs top / panties / arms
    # (the masturbation arm passes in front of it).
    always:
        preg_belly("rogue", "+Cowgirl/belly")

    # 12c. Shoulder Right (always visible)
    group shoulder_right:
        attribute shoulder_right_on default:
            "images/characters/Rogue/Cowgirl/Rogue Shoulder Right.png"
        attribute shoulder_right_none:
            Null()

    # 12c. Shoulder Left (hidden during hide-face)
    group shoulder_left:
        attribute shoulder_left_on default:
            "images/characters/Rogue/Cowgirl/Rogue Shoulder Left.png"
        attribute shoulder_left_none:
            Null()

    # 10. Legs Top
    group legs_top:
        attribute legs_top_base default:
            "images/characters/Rogue/Cowgirl/Rogue Cowgirl Legs Top.png"
        attribute legs_top_none:
            Null()

    # 11. Panties Top (green panties / bikini — above legs so "down" state renders correctly)
    group panties_top:
        attribute panties_top_none default:
            Null()
        attribute panties_top_1:
            "images/characters/Rogue/Cowgirl/Clothes/Panties/Green Panties/Green Panties.png"
        attribute panties_top_2:
            "images/characters/Rogue/Cowgirl/Clothes/Panties/Green Panties/Green Panties Side Top.png"
        attribute panties_top_down:
            "images/characters/Rogue/Cowgirl/Clothes/Panties/Green Panties/Green Panties Down.png"
        attribute panties_top_bikini:
            "images/characters/Rogue/Cowgirl/Clothes/Panties/Green Bikini Bottom/Green Bikini.png"
        attribute panties_top_bikini_side:
            "images/characters/Rogue/Cowgirl/Clothes/Panties/Green Bikini Bottom/Green Bikini Side Top.png"
        attribute panties_top_bikini_down:
            "images/characters/Rogue/Cowgirl/Clothes/Panties/Green Bikini Bottom/Green bikini panties Down.png"

    # 9. Thigh-highs
    group thigh_highs:
        attribute thigh_highs_none default:
            Null()
        attribute thigh_highs_on:
            "images/characters/Rogue/Cowgirl/Clothes/Rogue Cowgirl Thigh Highs.png"

    # 9b. Skirt (not available for Rogue)
    group skirt:
        attribute skirt_none default:
            Null()

    # 12b. Torso Over (not available for Rogue cowgirl)
    group torso_over:
        attribute torso_over_none default:
            Null()

    # 8. Arms High (pose 1 above torso)
    group arms_high:
        attribute arms_high_none default:
            Null()
        attribute arms_high_1:
            "images/characters/Rogue/Cowgirl/Rogue Cowgirl Arms.png"
        attribute arms_high_masturbate:
            "images/characters/Rogue/Cowgirl/Rogue Cowgirl Masturbation Naked.png"

    # Masturbation hand overlay
    group masturbate_hand at cg_hand_rot:
        attribute masturbate_hand_none default:
            Null()
        attribute masturbate_hand_on:
            "images/characters/Rogue/Cowgirl/Rogue Masturbate Hand.png"

    # Cum on legs
    group cum_legs:
        attribute cum_legs_auto default:
            ConditionSwitch(
                "store._cowgirl_girl and 'legs' in getattr(store._cowgirl_girl, 'Cum', [])",
                "images/characters/Rogue/Cowgirl/Cum/Rogue Cowgirl Legs Cum.png",
                "store._cowgirl_girl and 'dripping' in getattr(store._cowgirl_girl, 'Cum', []) and store._session_cum.get('inside', 0) >= 2",
                "images/characters/Rogue/Cowgirl/Cum/Rogue Cowgirl Legs Cum.png",
                "True", Null()
            )

    # Torso Clothing group (for registry compatibility)
    group torso_clothing:
        attribute torso_clothing_none default:
            Null()
        attribute torso_clothing_corset:
            Null()
        attribute torso_clothing_corset_up:
            Null()

    # MID (placeholder)
    group mid:
        attribute mid_none default:
            Null()

    # 7. Boobs (standalone sprites — animated via COWGIRL_ApplySpeed)
    # Chest clothing (Shirt, Shirt Bottom) handled entirely by Core standalone sprites.
    group boobs:
        attribute boobs_none default:
            Null()
        attribute boobs_naked_1:
            preg_art("rogue", "Cowgirl/Rogue Cowgirl Boobs Base.png")
        attribute boobs_naked_2:
            preg_art("rogue", "Cowgirl/Rogue Cowgirl Boobs Base.png")
        attribute boobs_clothed_1:
            Null()
        attribute boobs_clothed_2:
            Null()

    # Collar
    group collar:
        attribute collar_none default:
            Null()
        attribute collar_on:
            "images/characters/Rogue/Cowgirl/Clothes/Rogue Cowgirl Collar.png"

    # 5. Head
    group head at cg_head_rot:
        attribute head_base default:
            "images/characters/Rogue/Cowgirl/Head/Rogue Cowgirl Head.png"
        attribute head_base_bob:
            "images/characters/Rogue/Cowgirl/Head/Rogue Cowgirl Head.png"

    # 4b. Blush
    group blush at cg_head_rot:
        attribute blush_auto default:
            ConditionSwitch(
                "_gs('cowgirl', 'blush', 0) == 2",
                "images/characters/Rogue/Cowgirl/Head/Rogue Cowgirl Blush 2.png",
                "_gs('cowgirl', 'blush', 0) == 1",
                "images/characters/Rogue/Cowgirl/Head/Rogue Cowgirl Blush 1.png",
                "True", Null()
            )

    # 4. Mouth
    group mouth at cg_head_rot:
        attribute mouth_normal default:
            "images/characters/Rogue/Cowgirl/Expressions/Mouth/Normal.png"
        attribute mouth_disgusted:
            "images/characters/Rogue/Cowgirl/Expressions/Mouth/Sad.png"
        attribute mouth_laugh:
            "images/characters/Rogue/Cowgirl/Expressions/Mouth/Laugh.png"
        attribute mouth_open_teeth:
            "images/characters/Rogue/Cowgirl/Expressions/Mouth/Moaning.png"
        attribute mouth_sch:
            "images/characters/Rogue/Cowgirl/Expressions/Mouth/Moaning 2.png"
        attribute mouth_serious:
            "images/characters/Rogue/Cowgirl/Expressions/Mouth/Moaning 3.png"
        attribute mouth_smile:
            "images/characters/Rogue/Cowgirl/Expressions/Mouth/Smile.png"
        attribute mouth_surprised:
            "images/characters/Rogue/Cowgirl/Expressions/Mouth/Moaning.png"
        attribute mouth_tongue:
            "images/characters/Rogue/Cowgirl/Expressions/Mouth/Tongue.png"
        attribute mouth_kissing:
            "images/characters/Rogue/Cowgirl/Expressions/Mouth/Kiss.png"

    # 3. Eyes (ConditionSwitch for blink)
    group eyes at cg_head_rot:
        attribute eyes_normal default:
            ConditionSwitch(
                "cg_blink", "images/characters/Rogue/Cowgirl/Expressions/Eyes/Closed.png",
                "True",     "images/characters/Rogue/Cowgirl/Expressions/Eyes/Normal.png"
            )
        attribute eyes_side:
            ConditionSwitch(
                "cg_blink", "images/characters/Rogue/Cowgirl/Expressions/Eyes/Closed.png",
                "True",     "images/characters/Rogue/Cowgirl/Expressions/Eyes/Away.png"
            )
        attribute eyes_side_2:
            ConditionSwitch(
                "cg_blink", "images/characters/Rogue/Cowgirl/Expressions/Eyes/Closed.png",
                "True",     "images/characters/Rogue/Cowgirl/Expressions/Eyes/Up.png"
            )
        attribute eyes_squint:
            ConditionSwitch(
                "cg_blink", "images/characters/Rogue/Cowgirl/Expressions/Eyes/Closed.png",
                "True",     "images/characters/Rogue/Cowgirl/Expressions/Eyes/Squint.png"
            )
        attribute eyes_squint_big:
            "images/characters/Rogue/Cowgirl/Expressions/Eyes/Bliss.png"
        attribute eyes_surprised:
            ConditionSwitch(
                "cg_blink", "images/characters/Rogue/Cowgirl/Expressions/Eyes/Closed.png",
                "True",     "images/characters/Rogue/Cowgirl/Expressions/Eyes/Surprised.png"
            )
        attribute eyes_surprised_2:
            ConditionSwitch(
                "cg_blink", "images/characters/Rogue/Cowgirl/Expressions/Eyes/Closed.png",
                "True",     "images/characters/Rogue/Cowgirl/Expressions/Eyes/Sexy.png"
            )
        attribute eyes_closed:
            "images/characters/Rogue/Cowgirl/Expressions/Eyes/Closed.png"
        attribute eyes_left_closed:
            "images/characters/Rogue/Cowgirl/Expressions/Eyes/Closed Left.png"
        attribute eyes_right_closed:
            "images/characters/Rogue/Cowgirl/Expressions/Eyes/Closed Right.png"
        attribute eyes_squint_2:
            ConditionSwitch(
                "cg_blink", "images/characters/Rogue/Cowgirl/Expressions/Eyes/Closed.png",
                "True",     "images/characters/Rogue/Cowgirl/Expressions/Eyes/Squint.png"
            )
        attribute eyes_ahegao:
            "images/characters/Rogue/Cowgirl/Expressions/Eyes/Ahegao.png"
        attribute eyes_ahegao_2:
            "images/characters/Rogue/Cowgirl/Expressions/Eyes/Ahegao 2.png"

    # 2. Eyebrows
    group brows at cg_head_rot:
        attribute brows_normal default:
            "images/characters/Rogue/Cowgirl/Expressions/Brows/Normal.png"
        attribute brows_confused:
            "images/characters/Rogue/Cowgirl/Expressions/Brows/Sad.png"
        attribute brows_surprised:
            "images/characters/Rogue/Cowgirl/Expressions/Brows/Perplexed 1.png"
        attribute brows_horny:
            "images/characters/Rogue/Cowgirl/Expressions/Brows/Perplexed 2.png"

    # Guy Arms (above everything - head, expressions, etc.)
    # Left/right arms now shown as standalone layers by COWGIRL_ApplySpeed
    group guy_arms:
        attribute guy_arms_on:
            Null()
        attribute guy_arms_none default:
            Null()

    # 0. Penis (optional, top)
    group penis_top:
        attribute penis_top_none default:
            Null()
        attribute penis_top_on:
            _p("Cowgirl/Cowgirl Penis Side.png")

# ============================================================
# Standalone Cowgirl images
# ============================================================
image rogue cowgirl_penis = _p("Cowgirl/Cowgirl Penis.png")
image rogue cowgirl_penis_top = _p("Cowgirl/Cowgirl Penis Side.png")
image rogue cowgirl_guy_squeeze_left = Transform(_p("Cowgirl/Cowgirl Guy Hands Squeeze Left.png"), xoffset=20)
image rogue cowgirl_guy_squeeze_right = Transform(_p("Cowgirl/Cowgirl Guy Hands Squeeze Right.png"), xoffset=-20)
image rogue cowgirl_guy_arms_left = _p("Cowgirl/Cowgirl Guy Arms Left.png")
image rogue cowgirl_guy_arms_right = _p("Cowgirl/Cowgirl Guy Arms Right.png")
image rogue cowgirl_pussy = "images/characters/Rogue/Cowgirl/Rogue Cowgirl Pussy.png"
image rogue cowgirl_legs_bottom = "images/characters/Rogue/Cowgirl/Rogue Cowgirl Legs Bottom.png"
image rogue cowgirl_panties_side_bottom = "images/characters/Rogue/Cowgirl/Clothes/Panties/Green Panties/Green Panties Side Bottom.png"
image rogue cowgirl_bikini_panties_side_bottom = "images/characters/Rogue/Cowgirl/Clothes/Panties/Green Bikini Bottom/Green Bikini Side Bottom.png"
image rogue cowgirl_boobs_naked = preg_art("rogue", "Cowgirl/Rogue Cowgirl Boobs Base.png")
image rogue cowgirl_nipples = ConditionSwitch(
    "store._cowgirl_girl and getattr(store._cowgirl_girl, 'Piercing', False)",
    preg_art("rogue", "Cowgirl/Rogue Cowgirl Nipples Piercing.png"),
    "True",
    preg_art("rogue", "Cowgirl/Rogue Cowgirl Nipples.png")
)
# Crop Top standalone (referenced by Core_Cowgirl generic chest handling)
# Crop Top standalone: Shirt (full, above boobs)
image rogue cowgirl_crop_top = preg_art("rogue", "Cowgirl/Clothes/Chest/Top Crop/Rogue Cowgirl Shirt.png")
# Shirt Bottom (fixed layer, always visible when chest on, below boobs)
image rogue cowgirl_crop_top_fixed = "images/characters/Rogue/Cowgirl/Clothes/Chest/Top Crop/Rogue Cowgirl Shirt Bottom.png"
# Green Bikini Top standalone (referenced by Core_Cowgirl generic chest handling)
image rogue cowgirl_bikini_top = preg_art("rogue", "Cowgirl/Clothes/Chest/Green Bikini Top/Green bikini Top Down.png")
image rogue cowgirl_bikini_top_up = preg_art("rogue", "Cowgirl/Clothes/Chest/Green Bikini Top/Green bikini Top Up.png")
image rogue cowgirl_bikini_top_fixed = "images/characters/Rogue/Cowgirl/Clothes/Chest/Green Bikini Top/Green bikini Top handle.png"

# Cum layers
image rogue cowgirl_tummy_cum = ConditionSwitch(
    "store._cowgirl_girl and 'body' in getattr(store._cowgirl_girl, 'Cum', [])",
    "images/characters/Rogue/Cowgirl/Cum/Rogue Cowgirl Tummy Cum.png",
    "True", Null()
)
image rogue cowgirl_penis_cum = ConditionSwitch(
    "store._cowgirl_girl and 'body' in getattr(store._cowgirl_girl, 'Cum', [])",
    "images/characters/Rogue/Cowgirl/Cum/Rogue Cowgirl Penis Cum.png",
    "True", Null()
)
image rogue cowgirl_dripping_cum = ConditionSwitch(
    "store._cowgirl_girl and 'dripping' in getattr(store._cowgirl_girl, 'Cum', [])",
    "images/characters/Rogue/Cowgirl/Cum/Rogue Cowgirl Dripping Cum.png",
    "True", Null()
)
image rogue cowgirl_dripping_cum_2 = ConditionSwitch(
    "store._cowgirl_girl and 'dripping' in getattr(store._cowgirl_girl, 'Cum', []) and store._session_cum.get('inside', 0) >= 2",
    "images/characters/Rogue/Cowgirl/Cum/Rogue Cowgirl Dripping Cum 2.png",
    "True", Null()
)
image rogue cowgirl_legs_cum = ConditionSwitch(
    "store._cowgirl_girl and 'legs' in getattr(store._cowgirl_girl, 'Cum', [])",
    "images/characters/Rogue/Cowgirl/Cum/Rogue Cowgirl Legs Cum.png",
    "store._cowgirl_girl and 'dripping' in getattr(store._cowgirl_girl, 'Cum', []) and store._session_cum.get('inside', 0) >= 2",
    "images/characters/Rogue/Cowgirl/Cum/Rogue Cowgirl Legs Cum.png",
    "True", Null()
)
image rogue cowgirl_cum_face = ConditionSwitch(
    "store._cowgirl_girl and 'face' in getattr(store._cowgirl_girl, 'Cum', [])",
    "images/characters/Rogue/Cowgirl/Cum/Rogue Cowgirl Face.png",
    "True", Null()
)
image rogue cowgirl_hide_arm_left_1 = ConditionSwitch(
    "store._cowgirl_girl and store._cowgirl_girl.Over == 'long_shirt' and not store.cowgirl_masturbating",
    Composite(
        (1920, 1080),
        (0, 0), "images/characters/Rogue/Cowgirl/Hide Arm Left 1.png",
        (0, 0), preg_art("rogue", "Cowgirl/Clothes/Over/Mesh Top/Hide Arm 1 Left Mesh Top.png"),
    ),
    True,
    "images/characters/Rogue/Cowgirl/Hide Arm Left 1.png"
)
image rogue cowgirl_hide_arm_left_2 = "images/characters/Rogue/Cowgirl/Hide Arm Left 2.png"
image rogue cowgirl_hide_arm_left_2_over = ConditionSwitch(
    "store._cowgirl_girl and store._cowgirl_girl.Over == 'long_shirt'",
    "images/characters/Rogue/Cowgirl/Clothes/Over/Mesh Top/Hide Arm 2 Left Mesh Top.png",
    True,
    Null()
)
image rogue cowgirl_hide_arm_right = "images/characters/Rogue/Cowgirl/Hide Arm Right.png"
image rogue cowgirl_hide_arm_masturbate_right = "images/characters/Rogue/Cowgirl/Hide Arm Masturbate Right.png"

image rogue cowgirl_slap_right = _p("Cowgirl/Cowgirl Guy Hand Smack Right.png")
image rogue cowgirl_slap_left  = _p("Cowgirl/Cowgirl Guy Hand Smack Left.png")
image rogue cowgirl_masturbate_arm = "images/characters/Rogue/Cowgirl/Rogue Cowgirl Masturbation Naked.png"
image rogue cowgirl_masturbate_hand = "images/characters/Rogue/Cowgirl/Rogue Masturbate Hand.png"
