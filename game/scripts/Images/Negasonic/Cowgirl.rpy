# ============================================================
# Negasonic (NTW) Cowgirl Layered Sprite
# ============================================================
# Same structure as Gwen/Rogue. No skirt, no thigh-highs.
# Default Uniform replaces Long Shirt. Yellow Panties + Pink Bikini.

layeredimage ntw cowgirl:

    # 17. Guy (bottom — placeholder for compatibility)
    group guy:
        attribute guy_base default:
            Null()
        attribute guy_none:
            Null()

    # 16b. Arms Low
    group arms_low:
        attribute arms_low_none default:
            Null()
        attribute arms_low_2:
            "images/characters/Negasonic/Cowgirl/Negasonic Cowgirl Arms 2.png"

    # 16. Legs Bottom
    group legs_bottom:
        attribute legs_bottom_base default:
            "images/characters/Negasonic/Cowgirl/Negasonic Cowgirl Legs Bottom.png"
        attribute legs_bottom_none:
            Null()

    # 15. Panties Bottom (yellow panties / pink bikini)
    group panties_bottom:
        attribute panties_bottom_none default:
            Null()
        attribute panties_bottom_1:
            "images/characters/Negasonic/Cowgirl/Clothes/Panties/Yellow Panties/Yellow Panties Bottom.png"
        attribute panties_bottom_bikini:
            "images/characters/Negasonic/Cowgirl/Clothes/Panties/Pink Bikini Bottom/Pink Bikini Panties Bottom.png"

    # 14. Penis
    group penis:
        attribute penis_none default:
            Null()
        attribute penis_on:
            _p("Cowgirl/Cowgirl Penis.png")

    # 13. Torso
    group torso:
        attribute torso_base default:
            preg_art("ntw", "Cowgirl/Negasonic Cowgirl Torso.png")

    # Full belly (visual pregnancy stage 2): right above the torso, BELOW legs top / panties / arms
    # (the masturbation arm passes in front of it).
    always:
        preg_belly("ntw", "+Cowgirl/belly")

    # 10. Legs Top
    group legs_top:
        attribute legs_top_base default:
            "images/characters/Negasonic/Cowgirl/Negasonic Cowgirl Legs Top.png"
        attribute legs_top_none:
            Null()

    # 11. Panties Top (yellow panties / pink bikini)
    group panties_top:
        attribute panties_top_none default:
            Null()
        attribute panties_top_1:
            "images/characters/Negasonic/Cowgirl/Clothes/Panties/Yellow Panties/Yellow Panties.png"
        attribute panties_top_2:
            "images/characters/Negasonic/Cowgirl/Clothes/Panties/Yellow Panties/Yellow Panties Side Top.png"
        attribute panties_top_down:
            "images/characters/Negasonic/Cowgirl/Clothes/Panties/Yellow Panties/Yellow Panties Down.png"
        attribute panties_top_bikini:
            "images/characters/Negasonic/Cowgirl/Clothes/Panties/Pink Bikini Bottom/Pink Bikini Panties Bottom.png"
        attribute panties_top_bikini_side:
            "images/characters/Negasonic/Cowgirl/Clothes/Panties/Pink Bikini Bottom/Pink Bikini Panties Side Top.png"
        attribute panties_top_bikini_down:
            "images/characters/Negasonic/Cowgirl/Clothes/Panties/Pink Bikini Bottom/Pink Bikini Panties Down.png"

    # 9. Thigh-highs (NTW has none)
    group thigh_highs:
        attribute thigh_highs_none default:
            Null()

    # 9b. Skirt (NTW has none)
    group skirt:
        attribute skirt_none default:
            Null()

    # 12b. Torso Over (NTW has none for cowgirl)
    group torso_over:
        attribute torso_over_none default:
            Null()

    # 12c. Shoulder Right (always visible)
    group shoulder_right:
        attribute shoulder_right_on default:
            "images/characters/Negasonic/Cowgirl/Negasonic Shoulder Right.png"
        attribute shoulder_right_none:
            Null()

    # 12c. Shoulder Left (hidden during hide-face)
    group shoulder_left:
        attribute shoulder_left_on default:
            "images/characters/Negasonic/Cowgirl/Negasonic Shoulder Left.png"
        attribute shoulder_left_none:
            Null()

    # 8. Arms High (pose 1 above torso)
    group arms_high:
        attribute arms_high_none default:
            Null()
        attribute arms_high_1:
            "images/characters/Negasonic/Cowgirl/Negasonic Cowgirl Arms.png"
        attribute arms_high_clothed_1:
            Null()
        attribute arms_high_masturbate:
            "images/characters/Negasonic/Cowgirl/Negasonic Cowgirl Masturbation Naked.png"
        attribute arms_high_masturbate_ls:
            Null()

    # Masturbation hand overlay
    group masturbate_hand at cg_hand_rot:
        attribute masturbate_hand_none default:
            Null()
        attribute masturbate_hand_on:
            "images/characters/Negasonic/Cowgirl/Negasonic Masturbate Hand.png"

    # Cum on legs
    group cum_legs:
        attribute cum_legs_auto default:
            ConditionSwitch(
                "store._cowgirl_girl and 'legs' in getattr(store._cowgirl_girl, 'Cum', [])",
                "images/characters/Negasonic/Cowgirl/Cum/Negasonic Cowgirl Legs Cum.png",
                "store._cowgirl_girl and 'dripping' in getattr(store._cowgirl_girl, 'Cum', []) and store._session_cum.get('inside', 0) >= 2",
                "images/characters/Negasonic/Cowgirl/Cum/Negasonic Cowgirl Legs Cum.png",
                "True", Null()
            )

    # Guy Arms (standalone — placeholder group)
    group guy_arms:
        attribute guy_arms_on:
            Null()
        attribute guy_arms_none default:
            Null()

    # 12. Torso Clothing (NTW has no corset — placeholder)
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
    group boobs:
        attribute boobs_none default:
            Null()
        attribute boobs_naked_1:
            preg_art("ntw", "Cowgirl/Negasonic Cowgirl Boobs Base.png")
        attribute boobs_naked_2:
            preg_art("ntw", "Cowgirl/Negasonic Cowgirl Boobs Base.png")
        attribute boobs_clothed_1:
            Null()
        attribute boobs_clothed_2:
            Null()

    # Collar (NTW has none)
    group collar:
        attribute collar_none default:
            Null()
        attribute collar_on:
            Null()

    # 5. Head
    group head at cg_head_rot:
        attribute head_base default:
            "images/characters/Negasonic/Cowgirl/Head/Negasonic Cowgirl Head.png"
        attribute head_base_bob:
            "images/characters/Negasonic/Cowgirl/Head/Negasonic Cowgirl Head.png"

    # 4b. Blush
    group blush at cg_head_rot:
        attribute blush_auto default:
            ConditionSwitch(
                "_gs('cowgirl', 'blush', 0) == 2",
                "images/characters/Negasonic/Cowgirl/Head/Negasonic Cowgirl Blush 2.png",
                "_gs('cowgirl', 'blush', 0) == 1",
                "images/characters/Negasonic/Cowgirl/Head/Negasonic Cowgirl Blush 1.png",
                "True", Null()
            )

    # 4. Mouth
    group mouth at cg_head_rot:
        attribute mouth_normal default:
            "images/characters/Negasonic/Cowgirl/Expressions/Mouth/Normal.png"
        attribute mouth_disgusted:
            "images/characters/Negasonic/Cowgirl/Expressions/Mouth/Sad.png"
        attribute mouth_laugh:
            "images/characters/Negasonic/Cowgirl/Expressions/Mouth/Laugh.png"
        attribute mouth_open_teeth:
            "images/characters/Negasonic/Cowgirl/Expressions/Mouth/Screamming.png"
        attribute mouth_sch:
            "images/characters/Negasonic/Cowgirl/Expressions/Mouth/Moaning 2.png"
        attribute mouth_serious:
            "images/characters/Negasonic/Cowgirl/Expressions/Mouth/Lipbite.png"
        attribute mouth_smile:
            "images/characters/Negasonic/Cowgirl/Expressions/Mouth/Smile.png"
        attribute mouth_surprised:
            "images/characters/Negasonic/Cowgirl/Expressions/Mouth/Moaning.png"
        attribute mouth_tongue:
            "images/characters/Negasonic/Cowgirl/Expressions/Mouth/Tongue.png"
        attribute mouth_kissing:
            "images/characters/Negasonic/Cowgirl/Expressions/Mouth/Kiss.png"

    # 3. Eyes (ConditionSwitch for blink)
    group eyes at cg_head_rot:
        attribute eyes_normal default:
            ConditionSwitch(
                "cg_blink", "images/characters/Negasonic/Cowgirl/Expressions/Eyes/Closed.png",
                "True",     "images/characters/Negasonic/Cowgirl/Expressions/Eyes/Normal.png"
            )
        attribute eyes_side:
            ConditionSwitch(
                "cg_blink", "images/characters/Negasonic/Cowgirl/Expressions/Eyes/Closed.png",
                "True",     "images/characters/Negasonic/Cowgirl/Expressions/Eyes/Away.png"
            )
        attribute eyes_side_2:
            ConditionSwitch(
                "cg_blink", "images/characters/Negasonic/Cowgirl/Expressions/Eyes/Closed.png",
                "True",     "images/characters/Negasonic/Cowgirl/Expressions/Eyes/Up.png"
            )
        attribute eyes_squint:
            ConditionSwitch(
                "cg_blink", "images/characters/Negasonic/Cowgirl/Expressions/Eyes/Closed.png",
                "True",     "images/characters/Negasonic/Cowgirl/Expressions/Eyes/Squint.png"
            )
        attribute eyes_squint_big:
            "images/characters/Negasonic/Cowgirl/Expressions/Eyes/Bliss.png"
        attribute eyes_surprised:
            ConditionSwitch(
                "cg_blink", "images/characters/Negasonic/Cowgirl/Expressions/Eyes/Closed.png",
                "True",     "images/characters/Negasonic/Cowgirl/Expressions/Eyes/Surprised.png"
            )
        attribute eyes_surprised_2:
            ConditionSwitch(
                "cg_blink", "images/characters/Negasonic/Cowgirl/Expressions/Eyes/Closed.png",
                "True",     "images/characters/Negasonic/Cowgirl/Expressions/Eyes/Sexy.png"
            )
        attribute eyes_closed:
            "images/characters/Negasonic/Cowgirl/Expressions/Eyes/Closed.png"
        attribute eyes_left_closed:
            "images/characters/Negasonic/Cowgirl/Expressions/Eyes/Closed Left.png"
        attribute eyes_right_closed:
            "images/characters/Negasonic/Cowgirl/Expressions/Eyes/Closed Right.png"
        attribute eyes_squint_2:
            ConditionSwitch(
                "cg_blink", "images/characters/Negasonic/Cowgirl/Expressions/Eyes/Closed.png",
                "True",     "images/characters/Negasonic/Cowgirl/Expressions/Eyes/Squint.png"
            )
        attribute eyes_ahegao:
            "images/characters/Negasonic/Cowgirl/Expressions/Eyes/Ahegao.png"
        attribute eyes_ahegao_2:
            "images/characters/Negasonic/Cowgirl/Expressions/Eyes/Ahegao 2.png"

    # 2. Eyebrows
    group brows at cg_head_rot:
        attribute brows_normal default:
            "images/characters/Negasonic/Cowgirl/Expressions/Brows/Normal.png"
        attribute brows_confused:
            "images/characters/Negasonic/Cowgirl/Expressions/Brows/Sad.png"
        attribute brows_surprised:
            "images/characters/Negasonic/Cowgirl/Expressions/Brows/Perplexed 1.png"
        attribute brows_horny:
            "images/characters/Negasonic/Cowgirl/Expressions/Brows/Perplexed 2.png"

    # 0. Penis (optional, top)
    group penis_top:
        attribute penis_top_none default:
            Null()
        attribute penis_top_on:
            _p("Cowgirl/Cowgirl Penis Side.png")

# ============================================================
# Standalone Cowgirl images
# ============================================================
image ntw cowgirl_penis = _p("Cowgirl/Cowgirl Penis.png")
image ntw cowgirl_penis_top = _p("Cowgirl/Cowgirl Penis Side.png")
image ntw cowgirl_guy_squeeze_left = _p("Cowgirl/Cowgirl Guy Hands Squeeze Left.png")
image ntw cowgirl_guy_squeeze_right = _p("Cowgirl/Cowgirl Guy Hands Squeeze Right.png")
image ntw cowgirl_guy_arms_left = _p("Cowgirl/Cowgirl Guy Arms Left.png")
image ntw cowgirl_guy_arms_right = _p("Cowgirl/Cowgirl Guy Arms Right.png")
image ntw cowgirl_pussy = "images/characters/Negasonic/Cowgirl/Negasonic Cowgirl Pussy.png"
image ntw cowgirl_legs_bottom = "images/characters/Negasonic/Cowgirl/Negasonic Cowgirl Legs Bottom.png"
image ntw cowgirl_panties_side_bottom = "images/characters/Negasonic/Cowgirl/Clothes/Panties/Yellow Panties/Yellow Panties Side Bottom.png"
image ntw cowgirl_bikini_panties_side_bottom = "images/characters/Negasonic/Cowgirl/Clothes/Panties/Pink Bikini Bottom/Pink Bikini Panties Side Bottom.png"
image ntw cowgirl_boobs_naked = preg_art("ntw", "Cowgirl/Negasonic Cowgirl Boobs Base.png")
image ntw cowgirl_nipples = ConditionSwitch(
    "store._cowgirl_girl and getattr(store._cowgirl_girl, 'Piercing', False)",
    preg_art("ntw", "Cowgirl/Negasonic Cowgirl Nipples Piercings.png"),
    "True",
    preg_art("ntw", "Cowgirl/Negasonic Cowgirl Nipples.png")
)

image ntw cowgirl_shirt_top = Null()
image ntw cowgirl_yellow_bra = preg_art("ntw", "Cowgirl/Clothes/Chest/Yellow Bra/Yellow Bra.png")
image ntw cowgirl_yellow_bra_up = preg_art("ntw", "Cowgirl/Clothes/Chest/Yellow Bra/Yellow Bra Up.png")
image ntw cowgirl_bikini_top = preg_art("ntw", "Cowgirl/Clothes/Chest/Pink Bikini Top/Pink Bikini Top.png")
image ntw cowgirl_bikini_top_up = preg_art("ntw", "Cowgirl/Clothes/Chest/Pink Bikini Top/Pink Bikini Top Up.png")
image ntw cowgirl_bikini_top_fixed = preg_art("ntw", "Cowgirl/Clothes/Chest/Pink Bikini Top/Pink Bikini Top Fixed.png")
image ntw cowgirl_masturbate_arm = "images/characters/Negasonic/Cowgirl/Negasonic Cowgirl Masturbation Naked.png"
image ntw cowgirl_masturbate_hand = "images/characters/Negasonic/Cowgirl/Negasonic Masturbate Hand.png"

image ntw cowgirl_hide_arm_left_1 = "images/characters/Negasonic/Cowgirl/Hide Arm Left 1.png"
image ntw cowgirl_hide_arm_left_2 = "images/characters/Negasonic/Cowgirl/Hide Arm Left 2.png"
image ntw cowgirl_hide_arm_right  = "images/characters/Negasonic/Cowgirl/Hide Arm Right.png"
image ntw cowgirl_hide_arm_masturbate_right = "images/characters/Negasonic/Cowgirl/Hide Arm Masturbate Right.png"

image ntw cowgirl_slap_right = _p("Cowgirl/Cowgirl Guy Hand Smack Right.png")
image ntw cowgirl_slap_left  = _p("Cowgirl/Cowgirl Guy Hand Smack Left.png")
image ntw cowgirl_penis_cum = ConditionSwitch(
    "store._cowgirl_girl and 'body' in getattr(store._cowgirl_girl, 'Cum', [])",
    "images/characters/Negasonic/Cowgirl/Cum/Negasonic Cowgirl Penis Cum.png",
    "True", Null()
)

image ntw cowgirl_tummy_cum = ConditionSwitch(
    "store._cowgirl_girl and 'body' in getattr(store._cowgirl_girl, 'Cum', [])",
    "images/characters/Negasonic/Cowgirl/Cum/Negasonic Cowgirl Tummy Cum.png",
    "True", Null()
)
image ntw cowgirl_dripping_cum = ConditionSwitch(
    "store._cowgirl_girl and 'dripping' in getattr(store._cowgirl_girl, 'Cum', [])",
    "images/characters/Negasonic/Cowgirl/Cum/Negasonic Cowgirl Dripping Cum.png",
    "True", Null()
)
image ntw cowgirl_dripping_cum_2 = ConditionSwitch(
    "store._cowgirl_girl and 'dripping' in getattr(store._cowgirl_girl, 'Cum', []) and store._session_cum.get('inside', 0) >= 2",
    "images/characters/Negasonic/Cowgirl/Cum/Negasonic Cowgirl Dripping Cum 2.png",
    "True", Null()
)
image ntw cowgirl_cum_face = ConditionSwitch(
    "store._cowgirl_girl and 'face' in getattr(store._cowgirl_girl, 'Cum', [])",
    "images/characters/Negasonic/Cowgirl/Cum/Negasonic Cowgirl Face.png",
    "True", Null()
)
image ntw cowgirl_legs_cum = ConditionSwitch(
    "store._cowgirl_girl and 'legs' in getattr(store._cowgirl_girl, 'Cum', [])",
    "images/characters/Negasonic/Cowgirl/Cum/Negasonic Cowgirl Legs Cum.png",
    "store._cowgirl_girl and 'dripping' in getattr(store._cowgirl_girl, 'Cum', []) and store._session_cum.get('inside', 0) >= 2",
    "images/characters/Negasonic/Cowgirl/Cum/Negasonic Cowgirl Legs Cum.png",
    "True", Null()
)
