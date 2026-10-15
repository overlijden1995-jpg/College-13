# ============================================================
# Negasonic (NTW) RCG Layered Sprite
# ============================================================
# Same structure as Gwen/Rogue. No skirt, no thigh-highs, no collar.
# Default Uniform (yellow_jacket) as over. Yellow Panties only.
# Head 1 = looking at player, Head 2 = hiding face.

layeredimage ntw rcg:

    # --- Butt Bottom (gap between cheeks) ---
    group butt_bottom:
        attribute butt_bottom_base default:
            "images/characters/Negasonic/RCG/Butt Bottom.png"
        attribute butt_bottom_none:
            Null()

    # --- Torso overlay placeholder ---
    group torso_overlay:
        attribute torso_overlay_none default:
            Null()

    # --- Arms (below body when arms_1, standalone when arms_2) ---
    group arms:
        attribute arms_1 default:
            "images/characters/Negasonic/RCG/Arms 1.png"
        attribute arms_2:
            Null()
        attribute arms_ls_1:
            "images/characters/Negasonic/RCG/Clothes/Over/Default Uniform/Arms 1 Clothed.png"
        attribute arms_ls_2:
            Null()
        attribute arms_none:
            Null()

    # --- Body ---
    group body:
        attribute body_base default:
            "images/characters/Negasonic/RCG/Torso.png"

    # --- Butt Safe Layer ---
    group butt_safe:
        attribute butt_safe_on default:
            "images/characters/Negasonic/RCG/Ntw Butt Safe Layer.png"
        attribute butt_safe_none:
            Null()

    # --- Torso Clothing: Chest ---
    group torso_chest:
        attribute torso_chest_none default:
            Null()
        attribute torso_chest_bikini_top:
            "images/characters/Negasonic/RCG/Clothes/Chest/Pink Bikini Top/Pink Bikini Top.png"

    # --- Mid (placeholder) ---
    group mid:
        attribute mid_none default:
            Null()

    # --- Thigh Highs (NTW has none) ---
    group thigh_highs:
        attribute thigh_highs_none default:
            Null()

    # --- Head (Back = looking at player, Forward = hiding face) ---
    group head:
        attribute head_base default:
            ConditionSwitch(
                "store.hiding_face",
                "images/characters/Negasonic/RCG/Head/NTW Head RCG Forward.png",
                "True",
                "images/characters/Negasonic/RCG/Head/NTW Head RCG Back.png",
            )

    # --- Blush (hidden when facing forward) ---
    group blush:
        attribute blush_auto default:
            ConditionSwitch(
                "store.hiding_face", Null(),
                "_gs('rcg', 'blush', 0) == 2",
                "images/characters/Negasonic/RCG/Head/Blush 2.png",
                "_gs('rcg', 'blush', 0) == 1",
                "images/characters/Negasonic/RCG/Head/Blush 1.png",
                "True", Null()
            )

    # --- Mouth (hidden when facing forward) ---
    always:
        ConditionSwitch(
            "store.hiding_face", Null(),
            "_gs('rcg', 'mouth') == 'mouth_tongue'",
            "images/characters/Negasonic/RCG/Expressions/Mouth/Tongue.png",
            "_gs('rcg', 'mouth') == 'mouth_lipbite'",
            "images/characters/Negasonic/RCG/Expressions/Mouth/Lipbite.png",
            "_gs('rcg', 'mouth') == 'mouth_kiss'",
            "images/characters/Negasonic/RCG/Expressions/Mouth/Kiss.png",
            "_gs('rcg', 'mouth') == 'mouth_scared'",
            "images/characters/Negasonic/RCG/Expressions/Mouth/Scared.png",
            "_gs('rcg', 'mouth') in ('mouth_surprised', 'mouth_disgusted', 'mouth_open_teeth', 'mouth_sch', 'mouth_serious')",
            "images/characters/Negasonic/RCG/Expressions/Mouth/Moaning.png",
            "_gs('rcg', 'mouth') == 'mouth_smile'",
            "images/characters/Negasonic/RCG/Expressions/Mouth/Smile.png",
            "True",
            "images/characters/Negasonic/RCG/Expressions/Mouth/Normal.png",
        )

    # --- Eyes (hidden when facing forward) ---
    always:
        ConditionSwitch(
            "store.hiding_face", Null(),
            "getattr(store, 'rcg_blink', False)",
            "images/characters/Negasonic/RCG/Expressions/Eyes/Closed.png",
            "_gs('rcg', 'eyes') == 'eyes_side'",
            "images/characters/Negasonic/RCG/Expressions/Eyes/Looking Left.png",
            "_gs('rcg', 'eyes') == 'eyes_side_2'",
            "images/characters/Negasonic/RCG/Expressions/Eyes/Looking Right.png",
            "_gs('rcg', 'eyes') in ('eyes_squint', 'eyes_squint_2')",
            "images/characters/Negasonic/RCG/Expressions/Eyes/Blinking.png",
            "_gs('rcg', 'eyes') in ('eyes_squint_big', 'eyes_closed', 'eyes_left_closed', 'eyes_right_closed')",
            "images/characters/Negasonic/RCG/Expressions/Eyes/Closed.png",
            "_gs('rcg', 'eyes') == 'eyes_surprised'",
            "images/characters/Negasonic/RCG/Expressions/Eyes/Surprised.png",
            "_gs('rcg', 'eyes') == 'eyes_surprised_2'",
            "images/characters/Negasonic/RCG/Expressions/Eyes/Ahegao 2.png",
            "_gs('rcg', 'eyes') == 'eyes_looking_to_player'",
            "images/characters/Negasonic/RCG/Expressions/Eyes/Looking To Player.png",
            "_gs('rcg', 'eyes') == 'eyes_looking_up'",
            "images/characters/Negasonic/RCG/Expressions/Eyes/Looking Up.png",
            "True",
            "images/characters/Negasonic/RCG/Expressions/Eyes/Normal.png",
        )

    # --- Brows (hidden when facing forward) ---
    always:
        ConditionSwitch(
            "store.hiding_face", Null(),
            "_gs('rcg', 'brows') == 'brows_surprised'",
            "images/characters/Negasonic/RCG/Expressions/Eyebrows/Eyebrows Surprised.png",
            "_gs('rcg', 'brows') == 'brows_horny'",
            "images/characters/Negasonic/RCG/Expressions/Eyebrows/Horny.png",
            "_gs('rcg', 'brows') == 'brows_sad'",
            "images/characters/Negasonic/RCG/Expressions/Eyebrows/Eyebrows Sad.png",
            "_gs('rcg', 'brows') == 'brows_up'",
            "images/characters/Negasonic/RCG/Expressions/Eyebrows/Up.png",
            "True",
            "images/characters/Negasonic/RCG/Expressions/Eyebrows/Eyebrows Normal.png",
        )

    # --- Butt Top (skin overlay, below clothing) ---
    group butt_top:
        attribute butt_top_none default:
            Null()
        attribute butt_top_1:
            "images/characters/Negasonic/RCG/Top Butt 1.png"
        attribute butt_top_2:
            "images/characters/Negasonic/RCG/Top Butt 2.png"
        attribute butt_top_3:
            "images/characters/Negasonic/RCG/Top Butt 3.png"

    # --- Panties (yellow panties + pink bikini) ---
    group panties:
        attribute panties_none default:
            Null()
        attribute panties_1:
            "images/characters/Negasonic/RCG/Clothes/Panties/Yellow Panties/Panties 1.png"
        attribute panties_side:
            "images/characters/Negasonic/RCG/Clothes/Panties/Yellow Panties/Side Panties.png"
        attribute panties_down:
            "images/characters/Negasonic/RCG/Clothes/Panties/Yellow Panties/Panties Down.png"
        attribute panties_bikini_up:
            "images/characters/Negasonic/RCG/Clothes/Panties/Pink Bikini Bottom/Pink Bikini Panties Up.png"
        attribute panties_bikini_side:
            "images/characters/Negasonic/RCG/Clothes/Panties/Pink Bikini Bottom/Pink Bikini Panties Side.png"
        attribute panties_bikini_down:
            "images/characters/Negasonic/RCG/Clothes/Panties/Pink Bikini Bottom/Pink Bikini Panties Down.png"

    # --- Torso Over (Default Uniform — above panties so jacket covers them) ---
    # In sex/rub scenes, butt_clothed is a standalone layer (ApplySpeed handles it).
    # Outside scenes (ToD dare), include butt_clothed here so the full uniform shows.
    group torso_over:
        attribute torso_over_none default:
            Null()
        attribute torso_over_long_shirt:
            ConditionSwitch(
                "store.rcg_started or store.rcg_rub_mode",
                "images/characters/Negasonic/RCG/Clothes/Over/Default Uniform/Torso Clothed.png",
                "True",
                Composite(
                    (1920, 1080),
                    (0, 0), "images/characters/Negasonic/RCG/Clothes/Over/Default Uniform/Butt Clothed.png",
                    (0, 0), "images/characters/Negasonic/RCG/Clothes/Over/Default Uniform/Torso Clothed.png",
                ),
            )

    # --- Skirt (NTW has none) ---
    group skirt:
        attribute skirt_none default:
            Null()

    # --- Penis top (above clothing) ---
    group penis_top:
        attribute penis_top_none default:
            Null()
        attribute penis_top_on:
            _p("RCG/RCG Penis.png")

    # --- Collar (NTW has none) ---
    group collar:
        attribute collar_none default:
            Null()

# ============================================================
# Standalone RCG images
# ============================================================
image ntw rcg_penis = _p("RCG/RCG Penis.png")
image ntw rcg_butt_top_1 = "images/characters/Negasonic/RCG/Top Butt 1.png"
image ntw rcg_butt_top_2 = "images/characters/Negasonic/RCG/Top Butt 2.png"
image ntw rcg_butt_top_3 = "images/characters/Negasonic/RCG/Top Butt 3.png"
image ntw rcg_butt_gap = "images/characters/Negasonic/RCG/Butt Bottom.png"
image ntw rcg_arms_2 = "images/characters/Negasonic/RCG/Arms 2.png"
image ntw rcg_arms_ls_1 = "images/characters/Negasonic/RCG/Clothes/Over/Default Uniform/Arms 1 Clothed.png"
image ntw rcg_arms_ls_2 = "images/characters/Negasonic/RCG/Clothes/Over/Default Uniform/Arms 2 Clothed.png"
image ntw rcg_slap_right = _p("RCG/RCG Guy Hand Smack Right.png")
image ntw rcg_slap_left  = _p("RCG/RCG Guy Hand Smack Left.png")
image ntw rcg_grab_butt_left  = _p("RCG/RCG Guy Hand Squeeze Left.png")
image ntw rcg_grab_butt_right = _p("RCG/RCG Guy Hand Squeeze Right.png")
image ntw rcg_grab_butt = Composite(
    (1920, 1080),
    (0, 0), _p("RCG/RCG Guy Hand Squeeze Left.png"),
    (0, 0), _p("RCG/RCG Guy Hand Squeeze Right.png"),
)
image ntw rcg_rub_top = "images/characters/Negasonic/RCG/NTW RCG Top Butt Rubbing.png"
image ntw rcg_butt_clothed = "images/characters/Negasonic/RCG/Clothes/Over/Default Uniform/Butt Clothed.png"
# Standalone panties — named as: rcg_panties_{item_code}_{state}
image ntw rcg_panties_yellow_panties_full = "images/characters/Negasonic/RCG/Clothes/Panties/Yellow Panties/Panties 1.png"
image ntw rcg_panties_yellow_panties_side = "images/characters/Negasonic/RCG/Clothes/Panties/Yellow Panties/Side Panties.png"
image ntw rcg_panties_yellow_panties_down = "images/characters/Negasonic/RCG/Clothes/Panties/Yellow Panties/Panties Down.png"
# Pink Bikini standalone panties
image ntw rcg_panties_bikini_panties_full = "images/characters/Negasonic/RCG/Clothes/Panties/Pink Bikini Bottom/Pink Bikini Panties Up.png"
image ntw rcg_panties_bikini_panties_side = "images/characters/Negasonic/RCG/Clothes/Panties/Pink Bikini Bottom/Pink Bikini Panties Side.png"
image ntw rcg_panties_bikini_panties_side2 = "images/characters/Negasonic/RCG/Clothes/Panties/Pink Bikini Bottom/Pink Bikini Panties Side 2.png"
image ntw rcg_panties_bikini_panties_down = "images/characters/Negasonic/RCG/Clothes/Panties/Pink Bikini Bottom/Pink Bikini Panties Down.png"
image ntw rcg_butt_cum = ConditionSwitch(
    "store._rcg_girl and 'ass' in getattr(store._rcg_girl, 'Cum', [])",
    "images/characters/Negasonic/RCG/Cum/Negasonic RCG Butt Cum.png",
    "True", Null()
)
image ntw rcg_back_cum = ConditionSwitch(
    "store._rcg_girl and 'back' in getattr(store._rcg_girl, 'Cum', [])",
    "images/characters/Negasonic/RCG/Cum/Negasonic RCG Back Cum.png",
    "True", Null()
)
image ntw rcg_dripping_cum = ConditionSwitch(
    "store._rcg_girl and 'dripping' in getattr(store._rcg_girl, 'Cum', []) and store._session_cum.get('inside', 0) >= 2",
    "images/characters/Negasonic/RCG/Cum/Negasonic RCG Dripping Cum 2.png",
    "store._rcg_girl and 'dripping' in getattr(store._rcg_girl, 'Cum', [])",
    "images/characters/Negasonic/RCG/Cum/Negasonic RCG Dripping Cum 1.png",
    "True", Null()
)
image ntw rcg_penis_cum = ConditionSwitch(
    "store._rcg_girl and 'dripping' in getattr(store._rcg_girl, 'Cum', [])",
    "images/characters/Negasonic/RCG/Cum/Negasonic RCG Penis Cum.png",
    "True", Null()
)
image ntw rcg_cum_face = ConditionSwitch(
    "store._rcg_girl and 'face' in getattr(store._rcg_girl, 'Cum', []) and not store.hiding_face",
    "images/characters/Negasonic/RCG/Cum/Negasonic RCG Face Cum.png",
    "True", Null()
)
image ntw rcg_butt_blush = ConditionSwitch(
    "_gs('rcg', 'butt_blush', 0) >= 2",
    Composite(
        (1920, 1080),
        (0, 0), "images/characters/Negasonic/RCG/Butt Blush L 2.png",
        (0, 0), "images/characters/Negasonic/RCG/Butt Blush R 2.png",
    ),
    "_gs('rcg', 'butt_blush', 0) >= 1",
    Composite(
        (1920, 1080),
        (0, 0), "images/characters/Negasonic/RCG/Butt Blush L 1.png",
        (0, 0), "images/characters/Negasonic/RCG/Butt Blush R 1.png",
    ),
    "True", Null()
)
