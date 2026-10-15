# ============================================================
# Tenny Full Nelson Layered Sprite
# ============================================================
# Front-facing, held up by the player.
# Mirrors NTW structure — same layer order and tag pattern.

layeredimage tenny fn:

    # --- Torso (base body) ---
    group torso:
        attribute torso_base default:
            "images/characters/Tenny/Full Nelson/Torso.png"

    # --- Full belly (visual pregnancy stage 2): right above the torso, below the clothes ---
    # fn_during_pussy_fast carries it too (see that image).
    always:
        preg_belly("tenny", "+Full Nelson/belly")

    # --- Chest + Nipples: rendered as standalone with bounce transforms ---
    # See fn_chest_over / fn_nipples_over (shown by FN_ApplySpeed)

    # --- Clothes: White Top ---
    group white_top:
        attribute white_top_none default:
            Null()
        attribute white_top_up:
            preg_art("tenny", "Full Nelson/Clothes/White Top/White Top Up.png")
        attribute white_top_down:
            preg_art("tenny", "Full Nelson/Clothes/White Top/White Top Down.png")

    # --- Clothes: Striped Panties ---
    group striped_bottom:
        attribute striped_bottom_none default:
            Null()
        attribute striped_bottom_on:
            preg_art("tenny", "Full Nelson/Clothes/Striped Panties/Striped Bottom.png")

    # --- Clothes: Bikini Top ---
    group bikini_top:
        attribute bikini_top_none default:
            Null()
        attribute bikini_top_up:
            preg_art("tenny", "Full Nelson/Clothes/Bikini/Bikini Top Up.png")
        attribute bikini_top_down:
            preg_art("tenny", "Full Nelson/Clothes/Bikini/Bikini Top Dow.png")

    # --- Clothes: Bikini Bottom ---
    group bikini_bottom:
        attribute bikini_bottom_none default:
            Null()
        attribute bikini_bottom_on:
            preg_art("tenny", "Full Nelson/Clothes/Bikini/Bikini Bottom.png")

    # --- Head + Expressions: rendered as standalone with rotation transform ---
    # See fn_head_over layeredimage (shown by FN_ApplySpeed)


# ============================================================
# Head + Expressions (standalone layeredimage with rotation)
# ============================================================
layeredimage tenny fn_head_over:

    # --- Head ---
    always:
        "images/characters/Tenny/Full Nelson/Head/Head.png"

    # --- Blush ---
    always:
        ConditionSwitch(
            "_gs('fn', 'blush', 0) >= 2",
            "images/characters/Tenny/Full Nelson/Head/Blush 2.png",
            "_gs('fn', 'blush', 0) >= 1",
            "images/characters/Tenny/Full Nelson/Head/Blush 1.png",
            "True", Null()
        )

    # --- Mouth ---
    always:
        ConditionSwitch(
            "_gs('fn', 'mouth') == 'mouth_tongue'",
            "images/characters/Tenny/Full Nelson/Expression/Mouth/Tongue.png",
            "_gs('fn', 'mouth') == 'mouth_lipbite'",
            "images/characters/Tenny/Full Nelson/Expression/Mouth/Lipbite.png",
            "_gs('fn', 'mouth') == 'mouth_kiss'",
            "images/characters/Tenny/Full Nelson/Expression/Mouth/Kiss.png",
            "_gs('fn', 'mouth') == 'mouth_scared'",
            "images/characters/Tenny/Full Nelson/Expression/Mouth/Scared.png",
            "_gs('fn', 'mouth') == 'mouth_angry'",
            "images/characters/Tenny/Full Nelson/Expression/Mouth/Angry.png",
            "_gs('fn', 'mouth') == 'mouth_sad'",
            "images/characters/Tenny/Full Nelson/Expression/Mouth/Sad.png",
            "_gs('fn', 'mouth') == 'mouth_laugh'",
            "images/characters/Tenny/Full Nelson/Expression/Mouth/Laugh.png",
            "_gs('fn', 'mouth') == 'mouth_screaming'",
            "images/characters/Tenny/Full Nelson/Expression/Mouth/Screamming.png",
            "_gs('fn', 'mouth') in ('mouth_moaning_2', 'mouth_surprised', 'mouth_open_teeth', 'mouth_sch')",
            "images/characters/Tenny/Full Nelson/Expression/Mouth/Moaning 2.png",
            "_gs('fn', 'mouth') == 'mouth_moaning_3'",
            "images/characters/Tenny/Full Nelson/Expression/Mouth/Moaning 3.png",
            "_gs('fn', 'mouth') == 'mouth_smile'",
            "images/characters/Tenny/Full Nelson/Expression/Mouth/Smile.png",
            "_gs('fn', 'mouth') in ('mouth_moaning', 'mouth_serious')",
            "images/characters/Tenny/Full Nelson/Expression/Mouth/Moaning.png",
            "True",
            "images/characters/Tenny/Full Nelson/Expression/Mouth/Normal.png",
        )

    # --- Eyes ---
    always:
        ConditionSwitch(
            "getattr(store, 'fn_blink', False)",
            "images/characters/Tenny/Full Nelson/Expression/Eyes/Closed.png",
            "_gs('fn', 'eyes') == 'eyes_ahegao'",
            "images/characters/Tenny/Full Nelson/Expression/Eyes/Ahegao.png",
            "_gs('fn', 'eyes') == 'eyes_ahegao_2'",
            "images/characters/Tenny/Full Nelson/Expression/Eyes/Ahegao 2.png",
            "_gs('fn', 'eyes') == 'eyes_bliss'",
            "images/characters/Tenny/Full Nelson/Expression/Eyes/Bliss.png",
            "_gs('fn', 'eyes') == 'eyes_sexy'",
            "images/characters/Tenny/Full Nelson/Expression/Eyes/Sexy.png",
            "_gs('fn', 'eyes') == 'eyes_squint'",
            "images/characters/Tenny/Full Nelson/Expression/Eyes/Squint.png",
            "_gs('fn', 'eyes') == 'eyes_surprised'",
            "images/characters/Tenny/Full Nelson/Expression/Eyes/Surprised.png",
            "_gs('fn', 'eyes') == 'eyes_up'",
            "images/characters/Tenny/Full Nelson/Expression/Eyes/Up.png",
            "_gs('fn', 'eyes') == 'eyes_away'",
            "images/characters/Tenny/Full Nelson/Expression/Eyes/Away.png",
            "_gs('fn', 'eyes') == 'eyes_side'",
            "images/characters/Tenny/Full Nelson/Expression/Eyes/Looking Left.png",
            "_gs('fn', 'eyes') == 'eyes_side_2'",
            "images/characters/Tenny/Full Nelson/Expression/Eyes/Looking Right.png",
            "_gs('fn', 'eyes') == 'eyes_closed_happy'",
            "images/characters/Tenny/Full Nelson/Expression/Eyes/Closed Happy.png",
            "_gs('fn', 'eyes') == 'eyes_closed_left'",
            "images/characters/Tenny/Full Nelson/Expression/Eyes/Closed Left.png",
            "_gs('fn', 'eyes') == 'eyes_closed_right'",
            "images/characters/Tenny/Full Nelson/Expression/Eyes/Closed Right.png",
            "_gs('fn', 'eyes') == 'eyes_up_closed_left'",
            "images/characters/Tenny/Full Nelson/Expression/Eyes/Up Closed Left.png",
            "_gs('fn', 'eyes') == 'eyes_up_closed_right'",
            "images/characters/Tenny/Full Nelson/Expression/Eyes/Up Closed Right.png",
            "_gs('fn', 'eyes') in ('eyes_closed', 'eyes_squint_big', 'eyes_left_closed', 'eyes_right_closed')",
            "images/characters/Tenny/Full Nelson/Expression/Eyes/Closed.png",
            "True",
            "images/characters/Tenny/Full Nelson/Expression/Eyes/Normal.png",
        )

    # --- Brows ---
    always:
        ConditionSwitch(
            "_gs('fn', 'brows') == 'brows_angry'",
            "images/characters/Tenny/Full Nelson/Expression/Brows/Angry.png",
            "_gs('fn', 'brows') == 'brows_sad'",
            "images/characters/Tenny/Full Nelson/Expression/Brows/Sad.png",
            "_gs('fn', 'brows') == 'brows_scared'",
            "images/characters/Tenny/Full Nelson/Expression/Brows/Scared.png",
            "_gs('fn', 'brows') in ('brows_surprised', 'brows_confused')",
            "images/characters/Tenny/Full Nelson/Expression/Brows/Perplexed.png",
            "_gs('fn', 'brows') == 'brows_perplexed_2'",
            "images/characters/Tenny/Full Nelson/Expression/Brows/Perplexed 2.png",
            "_gs('fn', 'brows') == 'brows_horny'",
            "images/characters/Tenny/Full Nelson/Expression/Brows/Perplexed 2.png",
            "True",
            "images/characters/Tenny/Full Nelson/Expression/Brows/Normal.png",
        )


# ============================================================
# Standalone Full Nelson images
# ============================================================

# --- Chest Bounce (standalone above layeredimage) ---
image tenny fn_chest_over = preg_art("tenny", "Full Nelson/Chest.png")

# --- Nipples Bounce (standalone above chest) ---
image tenny fn_nipples_over = ConditionSwitch(
    "store._fn_girl and getattr(store._fn_girl, 'Piercing', False)",
    preg_art("tenny", "Full Nelson/Nipples Piercing.png"),
    "True",
    preg_art("tenny", "Full Nelson/Nipples.png"),
)

# --- Girl Arms (Layer 12 — bottom) ---
image tenny fn_arm_left = "images/characters/Tenny/Full Nelson/Arm Left 1.png"
image tenny fn_arm_right = "images/characters/Tenny/Full Nelson/Arm Right 1.png"

# --- Ass Base Safe (Layer 11) ---
image tenny fn_ass_safe = "images/characters/Tenny/Full Nelson/Ass Base Safe.png"

# --- Legs (Layer 10) ---
image tenny fn_shin_left = "images/characters/Tenny/Full Nelson/Shin Left.png"
image tenny fn_shin_right = "images/characters/Tenny/Full Nelson/Shin Right.png"
image tenny fn_thigh_left = "images/characters/Tenny/Full Nelson/Thigh Left.png"
image tenny fn_thigh_right = "images/characters/Tenny/Full Nelson/Thigh Right.png"

# --- Guy Arms (Layer 10 — above legs) ---
image tenny fn_guy_arm_left = _p("Full Nelson/FN Guy Arm Left Petite.png")
image tenny fn_guy_arm_right = _p("Full Nelson/FN Guy Arm Right Petite.png")

# --- Pelvis Base Safe (Layer 8) ---
image tenny fn_pelvis_safe = "images/characters/Tenny/Full Nelson/Pelvis Base Safe.png"

# --- Before Pussy (Layer 8 — clean state, no penetration) ---
image tenny fn_before_pussy = "images/characters/Tenny/Full Nelson/Before Pussy.png"

# --- During Pussy Below (Layer 8 — below penis during sex) ---
image tenny fn_during_pussy_below = "images/characters/Tenny/Full Nelson/During Pussy Below.png"

# --- During Pussy Fast (Layer 8 — above penis at fast speed) ---
# This layer redraws the lower torso ABOVE the layeredimage, so at fast speed it would cover the full
# belly: the part of the belly it hides rides on it (cropped at its top edge, so the tops that hang over
# the belly inside the layeredimage stay in front).
image tenny fn_during_pussy_fast = Composite(
    (1920, 1080),
    (0, 0), "images/characters/Tenny/Full Nelson/During Pussy Fast.png",
    (0, 519), preg_belly("tenny", "+Full Nelson/belly", window_top=519),
)

# --- Pussy Penis (Player) ---
image tenny fn_pussy_penis = _p("Full Nelson/FN Pussy Penis.png")

# --- Scrotum (Player — subtle zoom animation) ---
image tenny fn_scrotum = _p("Full Nelson/FN Scrotum.png")

# --- Before Ass (Layer 9 — clean state, no anal penetration) ---
image tenny fn_before_ass = "images/characters/Tenny/Full Nelson/Before Ass.png"

# --- During Anal Below (Layer 9 — below penis during anal) ---
image tenny fn_during_anal_below = "images/characters/Tenny/Full Nelson/During Anal Below.png"

# --- During Anal Fast (Layer 9 — above penis at fast anal speed) ---
image tenny fn_during_anal_fast = "images/characters/Tenny/Full Nelson/During Anal Fast.png"

# --- FN Legs (Player — below all other layers, moves with penis) ---
image tenny fn_legs = _p("Full Nelson/FN Legs.png")

# --- Cum Layers ---
image tenny fn_cum_penis = "images/characters/Tenny/Full Nelson/Cum/Cum Penis.png"
image tenny fn_cum_inside_pussy_2 = "images/characters/Tenny/Full Nelson/Cum/Cum Inside Pussy 2.png"
image tenny fn_cum_ass_inside = "images/characters/Tenny/Full Nelson/Cum/Cum Ass Inside.png"
image tenny fn_cum_boobs = "images/characters/Tenny/Full Nelson/Cum/Cum Boobs.png"
image tenny fn_cum_ass = "images/characters/Tenny/Full Nelson/Cum/Cum Ass.png"
image tenny fn_cum_face = "images/characters/Tenny/Full Nelson/Cum/Tenny Cum Face FN.png"

# --- Animated After Effects (31-frame loops) ---
image tenny fn_after_pussy_anim = DynamicDisplayable(_fn_effect_frame_anim, "After Pussy", "After Pussy")
image tenny fn_after_ass_anim = DynamicDisplayable(_fn_effect_frame_anim, "After Ass", "After Ass")
