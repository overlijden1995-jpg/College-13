# ============================================================
# Rogue RCG Layered Sprite
# ============================================================
# Same structure as Gwen. No over, no panties down, no skirt up.

layeredimage rogue rcg:

    # --- Butt Bottom (gap between cheeks) ---
    group butt_bottom:
        attribute butt_bottom_base default:
            "images/characters/Rogue/RCG/Rogue RCG Butt Gap.png"
        attribute butt_bottom_none:
            Null()

    # --- Torso overlay placeholder ---
    group torso_overlay:
        attribute torso_overlay_none default:
            Null()

    # --- Arms (below body when arms_1, standalone when arms_2) ---
    group arms:
        attribute arms_1 default:
            "images/characters/Rogue/RCG/Rogue RCG Arms 1.png"
        attribute arms_2:
            Null()
        attribute arms_none:
            Null()

    # --- Body (above arms) ---
    group body:
        attribute body_base default:
            "images/characters/Rogue/RCG/Rogue RCG Body.png"

    # --- Butt Safe Layer ---
    group butt_safe:
        attribute butt_safe_on default:
            "images/characters/Rogue/RCG/Rogue Butt Safe Layer.png"
        attribute butt_safe_none:
            Null()

    # --- Torso Clothing: Chest (crop top bottom half, below arms) ---
    group torso_chest:
        attribute torso_chest_none default:
            Null()
        attribute torso_chest_corset:
            "images/characters/Rogue/RCG/Clothes/Chest/Top Crop/Rogue RCG Crop Bottom.png"
        attribute torso_chest_bikini_top:
            "images/characters/Rogue/RCG/Clothes/Chest/Green Bikini Top/Green Bikini Top.png"

    # --- Mid (placeholder) ---
    group mid:
        attribute mid_none default:
            Null()

    # --- Torso Over (not available for Rogue RCG) ---
    group torso_over:
        attribute torso_over_none default:
            Null()

    # --- Thigh Highs ---
    group thigh_highs:
        attribute thigh_highs_none default:
            Null()
        attribute thigh_highs_on:
            "images/characters/Rogue/RCG/Clothes/Rogue RCG Thigh Highs.png"

    # --- Head (Back = looking at player, Forward = hiding face) ---
    group head:
        attribute head_base default:
            ConditionSwitch(
                "store.hiding_face",
                "images/characters/Rogue/RCG/Head/Rogue Head RCG Forward.png",
                "True",
                "images/characters/Rogue/RCG/Head/Rogue Head RCG Back.png",
            )

    # --- Blush (hidden when facing forward) ---
    group blush:
        attribute blush_auto default:
            ConditionSwitch(
                "store.hiding_face", Null(),
                "_gs('rcg', 'blush', 0) == 2",
                "images/characters/Rogue/RCG/Head/Rogue RCG Blush 2.png",
                "_gs('rcg', 'blush', 0) == 1",
                "images/characters/Rogue/RCG/Head/Rogue RCG Blush 1.png",
                "True", Null()
            )

    # --- Mouth (hidden when facing forward) ---
    always:
        ConditionSwitch(
            "store.hiding_face", Null(),
            "_gs('rcg', 'mouth') == 'mouth_tongue'",
            "images/characters/Rogue/RCG/Expressions/Mouth/Tongue.png",
            "_gs('rcg', 'mouth') == 'mouth_lipbite'",
            "images/characters/Rogue/RCG/Expressions/Mouth/Lipbite.png",
            "_gs('rcg', 'mouth') == 'mouth_kiss'",
            "images/characters/Rogue/RCG/Expressions/Mouth/Kiss.png",
            "_gs('rcg', 'mouth') == 'mouth_scared'",
            "images/characters/Rogue/RCG/Expressions/Mouth/Scared.png",
            "_gs('rcg', 'mouth') in ('mouth_surprised', 'mouth_disgusted', 'mouth_open_teeth', 'mouth_sch', 'mouth_serious')",
            "images/characters/Rogue/RCG/Expressions/Mouth/Moaning.png",
            "_gs('rcg', 'mouth') == 'mouth_smile'",
            "images/characters/Rogue/RCG/Expressions/Mouth/Smile.png",
            "True",
            "images/characters/Rogue/RCG/Expressions/Mouth/Normal.png",
        )

    # --- Eyes (hidden when facing forward) ---
    always:
        ConditionSwitch(
            "store.hiding_face", Null(),
            "getattr(store, 'rcg_blink', False)",
            "images/characters/Rogue/RCG/Expressions/Eyes/Closed.png",
            "_gs('rcg', 'eyes') == 'eyes_side'",
            "images/characters/Rogue/RCG/Expressions/Eyes/Looking Right.png",
            "_gs('rcg', 'eyes') == 'eyes_side_2'",
            "images/characters/Rogue/RCG/Expressions/Eyes/Looking Up.png",
            "_gs('rcg', 'eyes') in ('eyes_squint', 'eyes_squint_2')",
            "images/characters/Rogue/RCG/Expressions/Eyes/Blinking.png",
            "_gs('rcg', 'eyes') in ('eyes_squint_big', 'eyes_closed', 'eyes_left_closed', 'eyes_right_closed')",
            "images/characters/Rogue/RCG/Expressions/Eyes/Closed.png",
            "_gs('rcg', 'eyes') in ('eyes_surprised', 'eyes_surprised_2')",
            "images/characters/Rogue/RCG/Expressions/Eyes/Ahegao.png",
            "_gs('rcg', 'eyes') == 'eyes_looking_to_player'",
            "images/characters/Rogue/RCG/Expressions/Eyes/Looking To Player.png",
            "_gs('rcg', 'eyes') == 'eyes_looking_up'",
            "images/characters/Rogue/RCG/Expressions/Eyes/Looking Up.png",
            "True",
            "images/characters/Rogue/RCG/Expressions/Eyes/Normal.png",
        )

    # --- Brows (hidden when facing forward) ---
    always:
        ConditionSwitch(
            "store.hiding_face", Null(),
            "_gs('rcg', 'brows') in ('brows_surprised', 'brows_up')",
            "images/characters/Rogue/RCG/Expressions/Brows/Surprised.png",
            "_gs('rcg', 'brows') == 'brows_horny'",
            "images/characters/Rogue/RCG/Expressions/Brows/Horny.png",
            "True",
            "images/characters/Rogue/RCG/Expressions/Brows/Normal.png",
        )

    # --- Butt Top (skin overlay, below clothing) ---
    group butt_top:
        attribute butt_top_none default:
            Null()
        attribute butt_top_1:
            "images/characters/Rogue/RCG/Rogue RCG Butt Top 1.png"
        attribute butt_top_2:
            "images/characters/Rogue/RCG/Rogue RCG Butt Top 2.png"
        attribute butt_top_3:
            "images/characters/Rogue/RCG/Rogue RCG Butt Top 3.png"

    # --- Panties (full + side) ---
    group panties:
        attribute panties_none default:
            Null()
        attribute panties_1:
            "images/characters/Rogue/RCG/Clothes/Panties/Green Panties/Green Panties.png"
        attribute panties_side:
            "images/characters/Rogue/RCG/Clothes/Panties/Green Panties/Green  Panties Side Top.png"
        attribute panties_down:
            "images/characters/Rogue/RCG/Clothes/Panties/Green Panties/Green Panties Down.png"
        attribute panties_bikini_up:
            "images/characters/Rogue/RCG/Clothes/Panties/Green Bikini Bottom/Green Bikini Bottom Up.png"
        attribute panties_bikini_side:
            "images/characters/Rogue/RCG/Clothes/Panties/Green Bikini Bottom/Green Bikini Bottom Side 1.png"
        attribute panties_bikini_down:
            "images/characters/Rogue/RCG/Clothes/Panties/Green Bikini Bottom/Green Bikini Bottom Down.png"

    # --- Skirt (only full state) ---
    group skirt:
        attribute skirt_none default:
            Null()
        attribute skirt_on:
            "images/characters/Rogue/RCG/Clothes/Legs/Black Skirt/Rogue RCG Skirt.png"
        attribute skirt_up:
            "images/characters/Rogue/RCG/Clothes/Legs/Black Skirt/Black Skirt Up.png"

    # --- Penis top ---
    group penis_top:
        attribute penis_top_none default:
            Null()
        attribute penis_top_on:
            _p("RCG/RCG Penis.png")

    # --- Collar ---
    group collar:
        attribute collar_none default:
            Null()
        attribute collar_on:
            "images/characters/Rogue/RCG/Clothes/Rogue RCG Collar.png"

# ============================================================
# Standalone RCG images
# ============================================================
image rogue rcg_penis = _p("RCG/RCG Penis.png")
image rogue rcg_butt_top_1 = "images/characters/Rogue/RCG/Rogue RCG Butt Top 1.png"
image rogue rcg_butt_top_2 = "images/characters/Rogue/RCG/Rogue RCG Butt Top 2.png"
image rogue rcg_butt_top_3 = "images/characters/Rogue/RCG/Rogue RCG Butt Top 3.png"
image rogue rcg_butt_gap = "images/characters/Rogue/RCG/Rogue RCG Butt Gap.png"
image rogue rcg_thigh_highs = "images/characters/Rogue/RCG/Clothes/Rogue RCG Thigh Highs.png"
# Arms 2 standalone: only the hands (above butt). Body of arm stays in layeredimage (below butt).
image rogue rcg_arms_2 = "images/characters/Rogue/RCG/Rogue RCG Arms 2.png"
# Crop top upper half (shown as standalone above arms)
image rogue rcg_crop_top = "images/characters/Rogue/RCG/Clothes/Chest/Top Crop/Rogue RCG Crop Top.png"
image rogue rcg_slap_right = _p("RCG/RCG Guy Hand Smack Right.png")
image rogue rcg_slap_left  = _p("RCG/RCG Guy Hand Smack Left.png")
image rogue rcg_grab_butt_left  = _p("RCG/RCG Guy Hand Squeeze Left.png")
image rogue rcg_grab_butt_right = _p("RCG/RCG Guy Hand Squeeze Right.png")
image rogue rcg_grab_butt = Composite(
    (1920, 1080),
    (0, 0), _p("RCG/RCG Guy Hand Squeeze Left.png"),
    (0, 0), _p("RCG/RCG Guy Hand Squeeze Right.png"),
)
image rogue rcg_rub_top    = "images/characters/Rogue/RCG/Rogue RCG Top Butt Rubbing.png"
image rogue rcg_skirt = "images/characters/Rogue/RCG/Clothes/Legs/Black Skirt/Rogue RCG Skirt.png"
image rogue rcg_skirt_up = "images/characters/Rogue/RCG/Clothes/Legs/Black Skirt/Black Skirt Up.png"
image rogue rcg_panties_purple_full = "images/characters/Rogue/RCG/Clothes/Panties/Green Panties/Green Panties.png"
image rogue rcg_panties_purple_side = "images/characters/Rogue/RCG/Clothes/Panties/Green Panties/Green  Panties Side Top.png"
image rogue rcg_panties_purple_side_bottom = "images/characters/Rogue/RCG/Clothes/Panties/Green Panties/Green Panties Side Bottom.png"
image rogue rcg_panties_purple_down = "images/characters/Rogue/RCG/Clothes/Panties/Green Panties/Green Panties Down.png"
# Green Bikini standalone layers
image rogue rcg_bikini_top = "images/characters/Rogue/RCG/Clothes/Chest/Green Bikini Top/Green Bikini Top.png"
image rogue rcg_panties_bikini_panties_full = "images/characters/Rogue/RCG/Clothes/Panties/Green Bikini Bottom/Green Bikini Bottom Up.png"
image rogue rcg_panties_bikini_panties_side = "images/characters/Rogue/RCG/Clothes/Panties/Green Bikini Bottom/Green Bikini Bottom Side 1.png"
image rogue rcg_panties_bikini_panties_side2 = "images/characters/Rogue/RCG/Clothes/Panties/Green Bikini Bottom/Green Bikini Bottom Side 2.png"
image rogue rcg_panties_bikini_panties_down = "images/characters/Rogue/RCG/Clothes/Panties/Green Bikini Bottom/Green Bikini Bottom Down.png"
image rogue rcg_butt_cum = ConditionSwitch(
    "store._rcg_girl and 'ass' in getattr(store._rcg_girl, 'Cum', [])",
    "images/characters/Rogue/RCG/Cum/Rogue RCG Butt Cum.png",
    "True", Null()
)
image rogue rcg_back_cum = ConditionSwitch(
    "store._rcg_girl and 'back' in getattr(store._rcg_girl, 'Cum', [])",
    "images/characters/Rogue/RCG/Cum/Rogue RCG Back Cum.png",
    "True", Null()
)
image rogue rcg_dripping_cum = ConditionSwitch(
    "store._rcg_girl and 'dripping' in getattr(store._rcg_girl, 'Cum', []) and store._session_cum.get('inside', 0) >= 2",
    "images/characters/Rogue/RCG/Cum/Rogue RCG Dripping Cum 2.png",
    "store._rcg_girl and 'dripping' in getattr(store._rcg_girl, 'Cum', [])",
    "images/characters/Rogue/RCG/Cum/Rogue RCG Dripping Cum 1.png",
    "True", Null()
)
image rogue rcg_penis_cum = ConditionSwitch(
    "store._rcg_girl and 'dripping' in getattr(store._rcg_girl, 'Cum', [])",
    "images/characters/Rogue/RCG/Cum/Rogue RCG Penis Cum.png",
    "True", Null()
)
image rogue rcg_cum_face = ConditionSwitch(
    "store._rcg_girl and 'face' in getattr(store._rcg_girl, 'Cum', []) and not store.hiding_face",
    "images/characters/Rogue/RCG/Cum/Rogue RCG Face Cum.png",
    "True", Null()
)
image rogue rcg_butt_blush = ConditionSwitch(
    "_gs('rcg', 'butt_blush', 0) >= 2",
    Composite(
        (1920, 1080),
        (0, 0), "images/characters/Rogue/RCG/Rogue RCG Butt Blush Left 2.png",
        (0, 0), "images/characters/Rogue/RCG/Rogue RCG Butt Blush Right 2.png",
    ),
    "_gs('rcg', 'butt_blush', 0) >= 1",
    Composite(
        (1920, 1080),
        (0, 0), "images/characters/Rogue/RCG/Rogue RCG Butt Blush Left 1.png",
        (0, 0), "images/characters/Rogue/RCG/Rogue RCG Butt Blush Right 1.png",
    ),
    "True", Null()
)
