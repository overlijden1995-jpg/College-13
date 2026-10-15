# ============================================================
# Gwen RCG Layered Sprite
# ============================================================

layeredimage gwen rcg:

    # --- Butt Bottom (gap between cheeks, deepest layer) ---
    group butt_bottom:
        attribute butt_bottom_base default:
            "images/characters/Gwen/RCG/Gwen RCG Butt Gap.png"
        attribute butt_bottom_none:
            Null()

    # --- Torso (overlay placeholder) ---
    group torso_overlay:
        attribute torso_overlay_none default:
            Null()

    # --- Arms (below body when arms_1, above body when arms_2) ---
    group arms:
        attribute arms_1 default:
            "images/characters/Gwen/RCG/Gwen RCG Arms 1.png"
        attribute arms_2:
            Null()
        attribute arms_ls_1:
            "images/characters/Gwen/RCG/Clothes/Over/Long Shirt/DG Arms 1.png"
        attribute arms_ls_2:
            Null()
        attribute arms_none:
            Null()

    # --- Body ---
    group body:
        attribute body_base default:
            "images/characters/Gwen/RCG/Gwen RCG Body.png"

    # --- Butt Safe Layer (covers seams, above body/arms) ---
    group butt_safe:
        attribute butt_safe_on default:
            "images/characters/Gwen/RCG/Gwen Butt Safe Layer.png"
        attribute butt_safe_none:
            Null()

    # 6. Torso Clothing — chest (inner layer) below over (outer layer)
    group torso_chest:
        attribute torso_chest_none default:
            Null()
        attribute torso_chest_corset:
            "images/characters/Gwen/RCG/Clothes/Chest/Corset/Base.png"
        attribute torso_chest_bikini_top:
            "images/characters/Gwen/RCG/Clothes/Chest/Black Bikini Top/Black Bikini Top.png"

    # MID (placeholder)
    group mid:
        attribute mid_none default:
            Null()

    # 5. Thigh-highs
    group thigh_highs:
        attribute thigh_highs_none default:
            Null()
        attribute thigh_highs_on:
            "images/characters/Gwen/RCG/Clothes/Thigh Highs.png"

    # 3.5. Head (Back = looking at player, Forward = hiding face)
    group head:
        attribute head_base default:
            ConditionSwitch(
                "store.hiding_face",
                "images/characters/Gwen/RCG/Head/Gwen Head RCG Forward.png",
                "True",
                "images/characters/Gwen/RCG/Head/Gwen Head RCG Back.png",
            )

    # 3.4. Blush (hidden when facing forward)
    group blush:
        attribute blush_auto default:
            ConditionSwitch(
                "store.hiding_face", Null(),
                "_gs('rcg', 'blush', 0) == 2",
                "images/characters/Gwen/RCG/Head/Gwen RCG Blush 2.png",
                "_gs('rcg', 'blush', 0) == 1",
                "images/characters/Gwen/RCG/Head/Gwen RCG Blush 1.png",
                "True", Null()
            )

    # 3.3. Mouth (hidden when facing forward)
    always:
        ConditionSwitch(
            "store.hiding_face", Null(),
            "_gs('rcg', 'mouth') == 'mouth_tongue'",
            "images/characters/Gwen/RCG/Expressions/Mouth/Tongue.png",
            "_gs('rcg', 'mouth') == 'mouth_lipbite'",
            "images/characters/Gwen/RCG/Expressions/Mouth/Lipbite.png",
            "_gs('rcg', 'mouth') == 'mouth_kiss'",
            "images/characters/Gwen/RCG/Expressions/Mouth/Kiss.png",
            "_gs('rcg', 'mouth') == 'mouth_scared'",
            "images/characters/Gwen/RCG/Expressions/Mouth/Scared.png",
            "_gs('rcg', 'mouth') in ('mouth_surprised', 'mouth_disgusted', 'mouth_open_teeth', 'mouth_sch', 'mouth_serious')",
            "images/characters/Gwen/RCG/Expressions/Mouth/Moaning.png",
            "_gs('rcg', 'mouth') == 'mouth_smile'",
            "images/characters/Gwen/RCG/Expressions/Mouth/Smile.png",
            "True",
            "images/characters/Gwen/RCG/Expressions/Mouth/Normal.png",
        )

    # 7. Eyes (hidden when facing forward)
    always:
        ConditionSwitch(
            "store.hiding_face", Null(),
            "getattr(store, 'rcg_blink', False)",
            "images/characters/Gwen/RCG/Expressions/Eyes/Closed.png",
            "_gs('rcg', 'eyes') == 'eyes_side'",
            "images/characters/Gwen/RCG/Expressions/Eyes/Looking Left.png",
            "_gs('rcg', 'eyes') == 'eyes_side_2'",
            "images/characters/Gwen/RCG/Expressions/Eyes/Looking Right.png",
            "_gs('rcg', 'eyes') in ('eyes_squint', 'eyes_squint_2')",
            "images/characters/Gwen/RCG/Expressions/Eyes/Blinking.png",
            "_gs('rcg', 'eyes') in ('eyes_squint_big', 'eyes_closed', 'eyes_left_closed', 'eyes_right_closed')",
            "images/characters/Gwen/RCG/Expressions/Eyes/Closed.png",
            "_gs('rcg', 'eyes') in ('eyes_surprised', 'eyes_surprised_2')",
            "images/characters/Gwen/RCG/Expressions/Eyes/Ahegao.png",
            "_gs('rcg', 'eyes') == 'eyes_looking_to_player'",
            "images/characters/Gwen/RCG/Expressions/Eyes/Looking To Player.png",
            "_gs('rcg', 'eyes') == 'eyes_looking_up'",
            "images/characters/Gwen/RCG/Expressions/Eyes/Looking Up.png",
            "True",
            "images/characters/Gwen/RCG/Expressions/Eyes/Normal.png",
        )

    # 6. Eyebrows (hidden when facing forward)
    always:
        ConditionSwitch(
            "store.hiding_face", Null(),
            "_gs('rcg', 'brows') == 'brows_surprised'",
            "images/characters/Gwen/RCG/Expressions/Brows/Surprised.png",
            "_gs('rcg', 'brows') == 'brows_horny'",
            "images/characters/Gwen/RCG/Expressions/Brows/Horny.png",
            "_gs('rcg', 'brows') == 'brows_sad'",
            "images/characters/Gwen/RCG/Expressions/Brows/Sad.png",
            "_gs('rcg', 'brows') == 'brows_up'",
            "images/characters/Gwen/RCG/Expressions/Brows/Up.png",
            "True",
            "images/characters/Gwen/RCG/Expressions/Brows/Normal.png",
        )

    # --- BODY: Butt Top (skin overlay — below ALL clothing) ---
    group butt_top:
        attribute butt_top_none default:
            Null()
        attribute butt_top_1:
            "images/characters/Gwen/RCG/Gwen RCG Butt Top 1.png"
        attribute butt_top_2:
            "images/characters/Gwen/RCG/Gwen RCG Butt Top 2.png"
        attribute butt_top_3:
            "images/characters/Gwen/RCG/Gwen RCG Butt Top 3.png"

    # --- CLOTHING: Panties (above butt_top) ---
    group panties:
        attribute panties_none default:
            Null()
        attribute panties_1:
            "images/characters/Gwen/RCG/Clothes/Panties/Purple Panties/Purple Panties.png"
        attribute panties_side:
            "images/characters/Gwen/RCG/Clothes/Panties/Purple Panties/Purple Panties Side.png"
        attribute panties_down:
            "images/characters/Gwen/RCG/Clothes/Panties/Purple Panties/Purple Panties Down.png"
        attribute panties_bikini_up:
            "images/characters/Gwen/RCG/Clothes/Panties/Black Bikini Bottom/Black bikini panties Up.png"
        attribute panties_bikini_side:
            "images/characters/Gwen/RCG/Clothes/Panties/Black Bikini Bottom/Black bikini panties Side.png"
        attribute panties_bikini_down:
            "images/characters/Gwen/RCG/Clothes/Panties/Black Bikini Bottom/Black Bikini Panties Down.png"

    # --- CLOTHING: Over (above panties so jacket covers them) ---
    group torso_over:
        attribute torso_over_none default:
            Null()
        attribute torso_over_long_shirt:
            "images/characters/Gwen/RCG/Clothes/Over/Long Shirt/DG Body.png"

    # --- CLOTHING: Skirt (above panties) ---
    group skirt:
        attribute skirt_none default:
            Null()
        attribute skirt_on:
            "images/characters/Gwen/RCG/Clothes/Legs/Blue Skirt/Blue Skirt.png"
        attribute skirt_up:
            "images/characters/Gwen/RCG/Clothes/Legs/Blue Skirt/Blue Skirt Up.png"

    # --- Penis top (above clothing) ---
    group penis_top:
        attribute penis_top_none default:
            Null()
        attribute penis_top_on:
            _p("RCG/RCG Penis.png")

    # Collar (top priority, above everything)
    group collar:
        attribute collar_none default:
            Null()
        attribute collar_on:
            "images/characters/Gwen/RCG/Clothes/Collar.png"

image gwen rcg_penis = _p("RCG/RCG Penis.png")
image gwen rcg_butt_top_1 = "images/characters/Gwen/RCG/Gwen RCG Butt Top 1.png"
image gwen rcg_butt_top_2 = "images/characters/Gwen/RCG/Gwen RCG Butt Top 2.png"
image gwen rcg_butt_top_3 = "images/characters/Gwen/RCG/Gwen RCG Butt Top 3.png"
image gwen rcg_butt_gap = "images/characters/Gwen/RCG/Gwen RCG Butt Gap.png"
image gwen rcg_thigh_highs = "images/characters/Gwen/RCG/Clothes/Thigh Highs.png"
image gwen rcg_arms_2 = "images/characters/Gwen/RCG/Gwen RCG Arms 2.png"
image gwen rcg_arms_ls_2 = "images/characters/Gwen/RCG/Clothes/Over/Long Shirt/DG Arms 2.png"
image gwen rcg_slap_right = _p("RCG/RCG Guy Hand Smack Right.png")
image gwen rcg_slap_left  = _p("RCG/RCG Guy Hand Smack Left.png")
image gwen rcg_grab_butt_left  = _p("RCG/RCG Guy Hand Squeeze Left.png")
image gwen rcg_grab_butt_right = _p("RCG/RCG Guy Hand Squeeze Right.png")
image gwen rcg_grab_butt = Composite(
    (1920, 1080),
    (0, 0), _p("RCG/RCG Guy Hand Squeeze Left.png"),
    (0, 0), _p("RCG/RCG Guy Hand Squeeze Right.png"),
)
image gwen rcg_rub_top = "images/characters/Gwen/RCG/Gwen RCG Top Butt Rubbing.png"
image gwen rcg_skirt = "images/characters/Gwen/RCG/Clothes/Legs/Blue Skirt/Blue Skirt.png"
image gwen rcg_skirt_up = "images/characters/Gwen/RCG/Clothes/Legs/Blue Skirt/Blue Skirt Up.png"
# Standalone panties — named as: rcg_panties_{item_code}_{state}
# ApplySpeed builds: "%s rcg_panties_%s_%s" % (gid, girl.Panties, state)
image gwen rcg_panties_bikini_panties_full = "images/characters/Gwen/RCG/Clothes/Panties/Black Bikini Bottom/Black bikini panties Up.png"
image gwen rcg_panties_bikini_panties_side = "images/characters/Gwen/RCG/Clothes/Panties/Black Bikini Bottom/Black Bikini Panties Side 1.png"
image gwen rcg_panties_bikini_panties_side2 = "images/characters/Gwen/RCG/Clothes/Panties/Black Bikini Bottom/Black Bikini Panties Side 2.png"
image gwen rcg_panties_bikini_panties_down = "images/characters/Gwen/RCG/Clothes/Panties/Black Bikini Bottom/Black Bikini Panties Down.png"
image gwen rcg_panties_purple_full = "images/characters/Gwen/RCG/Clothes/Panties/Purple Panties/Purple Panties.png"
image gwen rcg_panties_purple_side = "images/characters/Gwen/RCG/Clothes/Panties/Purple Panties/Purple Panties Side Top.png"
image gwen rcg_panties_purple_side_bottom = "images/characters/Gwen/RCG/Clothes/Panties/Purple Panties/Purple Panties Side Bottom.png"
image gwen rcg_panties_purple_down = "images/characters/Gwen/RCG/Clothes/Panties/Purple Panties/Purple Panties Down.png"
image gwen rcg_butt_cum = ConditionSwitch(
    "store._rcg_girl and 'ass' in getattr(store._rcg_girl, 'Cum', [])",
    "images/characters/Gwen/RCG/Cum/Gwen RCG Butt Cum.png",
    "True", Null()
)
image gwen rcg_back_cum = ConditionSwitch(
    "store._rcg_girl and 'back' in getattr(store._rcg_girl, 'Cum', [])",
    "images/characters/Gwen/RCG/Cum/Gwen RCG Back Cum.png",
    "True", Null()
)
image gwen rcg_dripping_cum = ConditionSwitch(
    "store._rcg_girl and 'dripping' in getattr(store._rcg_girl, 'Cum', []) and store._session_cum.get('inside', 0) >= 2",
    "images/characters/Gwen/RCG/Cum/Gwen RCG Dripping Cum 2.png",
    "store._rcg_girl and 'dripping' in getattr(store._rcg_girl, 'Cum', [])",
    "images/characters/Gwen/RCG/Cum/Gwen RCG Dripping Cum 1.png",
    "True", Null()
)
image gwen rcg_penis_cum = ConditionSwitch(
    "store._rcg_girl and 'dripping' in getattr(store._rcg_girl, 'Cum', [])",
    "images/characters/Gwen/RCG/Cum/Gwen RCG Penis Cum.png",
    "True", Null()
)
image gwen rcg_cum_face = ConditionSwitch(
    "store._rcg_girl and 'face' in getattr(store._rcg_girl, 'Cum', []) and not store.hiding_face",
    "images/characters/Gwen/RCG/Cum/Gwen RCG Face Cum.png",
    "True", Null()
)
image gwen rcg_butt_blush = ConditionSwitch(
    "_gs('rcg', 'butt_blush', 0) >= 2",
    Composite(
        (1920, 1080),
        (0, 0), "images/characters/Gwen/RCG/Gwen RCG Butt Blush Left 2.png",
        (0, 0), "images/characters/Gwen/RCG/Gwen RCG Butt Blush Right 2.png",
    ),
    "_gs('rcg', 'butt_blush', 0) >= 1",
    Composite(
        (1920, 1080),
        (0, 0), "images/characters/Gwen/RCG/Gwen RCG Butt Blush Left 1.png",
        (0, 0), "images/characters/Gwen/RCG/Gwen RCG Butt Blush Right 1.png",
    ),
    "True", Null()
)
