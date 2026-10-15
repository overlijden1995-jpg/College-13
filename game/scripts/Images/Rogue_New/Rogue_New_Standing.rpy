# ============================================================
# New Rogue — Standing Sprite (Art Test Only)
# Completely separate layer system from the current Rogue.
# Layer order from the PSD (bottom-to-top), reworked 2026-10-02 with the
# artist's merged crossed-arm bases and descriptive head file names.
# ============================================================

# ── Store variable defaults (match PSD visible state) ─────

# Head
default _rn_face = "base"
default _rn_mouth = "smile"
default _rn_whites = "default"
default _rn_eyes = "default"
default _rn_brows = "sad"
default _rn_eyelids = "normal"
default _rn_blush = False

# Arms
default _rn_crossed = False
default _rn_right_arm = "idle"
default _rn_right_glove = True
default _rn_right_band = True
default _rn_right_vest = True
default _rn_left_arm = "idle"
default _rn_left_glove = True
default _rn_left_band = True
default _rn_left_vest = True

# Chest
# normal: top / bra / bikini / backing / bare
# crossed: empty / bra / bikini (merged bases) + bare or top drawn OVER the empty base
default _rn_chest = "top"
default _rn_pierced = False
default _rn_tape = False

# ChestClothes (vest overlay) — the model only ("vest" / "vest_short" / "none").
# The artist made two sizes of each: the "Clothed" cut for a covered chest and a slightly
# larger alt cut that covers the bare chest assets (prevents clipping). Picked automatically.
default _rn_vest = "vest_short"

# Body / Standing
default _rn_pubes = "tri"
default _rn_panties = "thong"
default _rn_skirt = "latex"
default _rn_feet = "boots_nosocks"
default _rn_legwear = "stockings"
default _rn_collar = True

# UI
default _rn_zoom = 1.0


init python:

    def _rn_chest_covered():
        """Her chest is inside a garment: the vest uses its 'Clothed' cut. Bare / empty /
        backing chest uses the larger alt cut the artist made against clipping."""
        return store._rn_chest in ("top", "bra", "bikini")


# ── Layeredimage ──────────────────────────────────────────
# First declared = backmost, last declared = frontmost.
#
# RightArm (back) → Standing → Chest → ChestClothes → LeftArm → Head (front)

layeredimage rogue_new standing:

    # ════════════════════════════════════════════════════════
    # RIGHT ARM (backmost — behind body)
    # Within each pose: base → glove → band → vest (back to front)
    # ════════════════════════════════════════════════════════

    # RArm Idle
    if not _rn_crossed and _rn_right_arm == "idle":
        "images/characters/Rogue_New/Standing/RightArm/RArmIdle/Rogue_StandingRArmIdle.PNG"
    if not _rn_crossed and _rn_right_arm == "idle" and _rn_right_glove:
        "images/characters/Rogue_New/Standing/RightArm/RArmIdle/Rogue_StandingRArmIdleGlove.PNG"
    if not _rn_crossed and _rn_right_arm == "idle" and _rn_right_band:
        "images/characters/Rogue_New/Standing/RightArm/RArmIdle/Rogue_StandingRArmIdleBand.PNG"
    if not _rn_crossed and _rn_right_arm == "idle" and _rn_right_vest:
        "images/characters/Rogue_New/Standing/RightArm/RArmIdle/RArmIdleVest.PNG"

    # RArm 1
    if not _rn_crossed and _rn_right_arm == "1":
        "images/characters/Rogue_New/Standing/RightArm/RArm1/Rogue_StandingRArm1.PNG"
    if not _rn_crossed and _rn_right_arm == "1" and _rn_right_glove:
        "images/characters/Rogue_New/Standing/RightArm/RArm1/Rogue_StandingRArm1Glove.PNG"
    if not _rn_crossed and _rn_right_arm == "1" and _rn_right_band:
        "images/characters/Rogue_New/Standing/RightArm/RArm1/Rogue_StandingRArm1Band.PNG"
    if not _rn_crossed and _rn_right_arm == "1" and _rn_right_vest:
        "images/characters/Rogue_New/Standing/RightArm/RArm1/Rogue_StandingRArm1Vest.PNG"

    # RArm 2
    if not _rn_crossed and _rn_right_arm == "2":
        "images/characters/Rogue_New/Standing/RightArm/RArm2/Rogue_StandingRArm2.PNG"
    if not _rn_crossed and _rn_right_arm == "2" and _rn_right_glove:
        "images/characters/Rogue_New/Standing/RightArm/RArm2/Rogue_StandingRArm2Glove.PNG"
    if not _rn_crossed and _rn_right_arm == "2" and _rn_right_band:
        "images/characters/Rogue_New/Standing/RightArm/RArm2/Rogue_StandingRArm1Band.PNG"
    if not _rn_crossed and _rn_right_arm == "2" and _rn_right_vest:
        "images/characters/Rogue_New/Standing/RightArm/RArm2/Rogue_StandingRArm1Vest.PNG"

    # ════════════════════════════════════════════════════════
    # STANDING (body + lower clothing)
    # PSD bottom→top: Body, Pubes, Panties, Skirts, Feet(Legs,Boots), Collar
    # ════════════════════════════════════════════════════════

    # Body base (backmost in Standing)
    always:
        "images/characters/Rogue_New/Standing/Standing/Rogue_StandingBodyFull.PNG"

    # Pubes
    if _rn_pubes == "bush":
        "images/characters/Rogue_New/Standing/Standing/Pubes/Rogue_StandingPubesBush.PNG"
    if _rn_pubes == "strip":
        "images/characters/Rogue_New/Standing/Standing/Pubes/Rogue_StandingPubesStrip.PNG"
    if _rn_pubes == "tri":
        "images/characters/Rogue_New/Standing/Standing/Pubes/Rogue_StandingPubesTri.PNG"

    # Panties (each piece also has its pulled-down state)
    if _rn_panties == "panties":
        "images/characters/Rogue_New/Standing/Standing/Panties/Rogue_StandingPanties.PNG"
    if _rn_panties == "panties_down":
        "images/characters/Rogue_New/Standing/Standing/Panties/Rogue_StandingPantiesDown.PNG"
    if _rn_panties == "thong":
        "images/characters/Rogue_New/Standing/Standing/Panties/Rogue_StandingThong.PNG"
    if _rn_panties == "thong_down":
        "images/characters/Rogue_New/Standing/Standing/Panties/Rogue_StandingThongDown.PNG"
    if _rn_panties == "bikini":
        "images/characters/Rogue_New/Standing/Standing/Panties/Rogue_StandingBikiniBottoms.PNG"
    if _rn_panties == "bikini_alt":
        "images/characters/Rogue_New/Standing/Standing/Panties/Rogue_StandingBikiniBottomsAlt.PNG"
    if _rn_panties == "bikini_down":
        "images/characters/Rogue_New/Standing/Standing/Panties/Rogue_StandingBikiniDown.PNG"

    # Skirts (each skirt also has its lifted "up" state)
    if _rn_skirt == "skirt":
        "images/characters/Rogue_New/Standing/Standing/Skirts/Rogue_StandingSkirt.PNG"
    if _rn_skirt == "skirt_up":
        "images/characters/Rogue_New/Standing/Standing/Skirts/Rogue_StandingSkirtUp.PNG"
    if _rn_skirt == "skirt2":
        "images/characters/Rogue_New/Standing/Standing/Skirts/Rogue_StandingSkirt2.PNG"
    if _rn_skirt == "skirt2_up":
        "images/characters/Rogue_New/Standing/Standing/Skirts/Rogue_StandingSkirt2Up.PNG"
    if _rn_skirt == "latex":
        "images/characters/Rogue_New/Standing/Standing/Skirts/Rogue_StandingLatex.PNG"
    if _rn_skirt == "latex_up":
        "images/characters/Rogue_New/Standing/Standing/Skirts/Rogue_StandingLatexUp.PNG"
    if _rn_skirt == "latex_see":
        "images/characters/Rogue_New/Standing/Standing/Skirts/Rogue_StandingLatexSeeThru.PNG"
    if _rn_skirt == "latex_see_up":
        "images/characters/Rogue_New/Standing/Standing/Skirts/Rogue_StandingLatexSeeThruUp.PNG"

    # Feet — Legwear (behind boots in Feet group)
    if _rn_legwear == "socks":
        "images/characters/Rogue_New/Standing/Standing/Feet/Legs/Rogue_StandingSocks.PNG"
    if _rn_legwear == "stockings":
        "images/characters/Rogue_New/Standing/Standing/Feet/Legs/Rogue_StandingStockings.PNG"

    # Feet — Boots (in front of legwear)
    if _rn_feet == "boots":
        "images/characters/Rogue_New/Standing/Standing/Feet/Rogue_StandingBoots.PNG"
    if _rn_feet == "boots_nosocks":
        "images/characters/Rogue_New/Standing/Standing/Feet/Rogue_StandingBootsNoSocks.PNG"

    # Collar (frontmost in Standing group)
    if _rn_collar:
        "images/characters/Rogue_New/Standing/Standing/Rogue_StandingCollar.PNG"

    # ════════════════════════════════════════════════════════
    # CHEST (in front of body)
    # Normal: one of top / bra / bikini / backing / bare (+pierced/+tape on bare).
    # Crossed (the artist's order): a merged BASE first — empty / bra / bikini —
    # then OVER it either the bare chest (needs the empty base, no top active)
    # or the crossed top. Tape sits on the bare chest.
    # ════════════════════════════════════════════════════════

    # Normal — garments / backing (backmost in Chest)
    if not _rn_crossed and _rn_chest == "top":
        "images/characters/Rogue_New/Standing/Chest/Rogue_StandingTop.PNG"
    if not _rn_crossed and _rn_chest == "bra":
        "images/characters/Rogue_New/Standing/Chest/Rogue_StandingBra.PNG"
    if not _rn_crossed and _rn_chest == "bikini":
        "images/characters/Rogue_New/Standing/Chest/Rogue_StandingBikini.PNG"
    if not _rn_crossed and _rn_chest == "backing":
        "images/characters/Rogue_New/Standing/Chest/Rogue_StandingBacking.PNG"

    # Normal — Bare: base → pierced → tape (back to front)
    if not _rn_crossed and _rn_chest == "bare":
        "images/characters/Rogue_New/Standing/Chest/Bare/Rogue_StandingChest.PNG"
    if not _rn_crossed and _rn_chest == "bare" and _rn_pierced:
        "images/characters/Rogue_New/Standing/Chest/Bare/Rogue_StandingChestPierced.PNG"
    if not _rn_crossed and _rn_chest == "bare" and _rn_tape:
        "images/characters/Rogue_New/Standing/Chest/Bare/Rogue_StandingChestTape.PNG"

    # Crossed — merged bases (arms included; "bare" and "top" sit on the empty base)
    if _rn_crossed and _rn_chest in ("empty", "bare", "top"):
        "images/characters/Rogue_New/Standing/Chest/Crossed/Rogue_StandingArmCrossedEmpty.PNG"
    if _rn_crossed and _rn_chest == "bra":
        "images/characters/Rogue_New/Standing/Chest/Crossed/Rogue_StandingArmsCrossedBra.PNG"
    if _rn_crossed and _rn_chest == "bikini":
        "images/characters/Rogue_New/Standing/Chest/Crossed/Rogue_StandingArmCrossedBikini.PNG"

    # Crossed — bare chest overlay: base → pierced → tape (needs the empty base, no top)
    if _rn_crossed and _rn_chest == "bare":
        "images/characters/Rogue_New/Standing/Chest/Crossed/Rogue_StandingArmCrossedNude.PNG"
    if _rn_crossed and _rn_chest == "bare" and _rn_pierced:
        "images/characters/Rogue_New/Standing/Chest/Crossed/Rogue_StandingArmCrossedNudePierced.PNG"
    if _rn_crossed and _rn_chest == "bare" and _rn_tape:
        "images/characters/Rogue_New/Standing/Chest/Crossed/Rogue_StandingCrossedChestTape.PNG"

    # Crossed — top overlay
    if _rn_crossed and _rn_chest == "top":
        "images/characters/Rogue_New/Standing/Chest/Crossed/Rogue_StandingCrossedTop.PNG"

    # ════════════════════════════════════════════════════════
    # CHEST CLOTHES (vests — in front of chest)
    # The cut follows the chest: covered chest = "Clothed" cut, otherwise the
    # Nude / larger alt cut that covers the bare chest (anti-clipping).
    # Crossed arms use the Crossed vests (sleeves drawn around the crossed
    # arms, hands left showing) and the crossed gloves cover those hands.
    # ════════════════════════════════════════════════════════

    if not _rn_crossed and _rn_vest == "vest" and _rn_chest_covered():
        "images/characters/Rogue_New/Standing/ChestClothes/Rogue_StandingVestClothed.PNG"
    if not _rn_crossed and _rn_vest == "vest" and not _rn_chest_covered():
        "images/characters/Rogue_New/Standing/ChestClothes/Rogue_StandingVest.PNG"
    if not _rn_crossed and _rn_vest == "vest_short" and _rn_chest_covered():
        "images/characters/Rogue_New/Standing/ChestClothes/Rogue_StandingVestShortClothed.PNG"
    if not _rn_crossed and _rn_vest == "vest_short" and not _rn_chest_covered():
        "images/characters/Rogue_New/Standing/ChestClothes/Rogue_StandingVestShort.PNG"

    if _rn_crossed and _rn_vest == "vest" and _rn_chest_covered():
        "images/characters/Rogue_New/Standing/ChestClothes/Rogue_StandingCrossedVestClothed.PNG"
    if _rn_crossed and _rn_vest == "vest" and not _rn_chest_covered():
        "images/characters/Rogue_New/Standing/ChestClothes/Rogue_StandingCrossedVestNude.PNG"
    if _rn_crossed and _rn_vest == "vest_short" and _rn_chest_covered():
        "images/characters/Rogue_New/Standing/ChestClothes/Rogue_StandingCrossedVestShortClothed.PNG"
    if _rn_crossed and _rn_vest == "vest_short" and not _rn_chest_covered():
        "images/characters/Rogue_New/Standing/ChestClothes/Rogue_StandingCrossedVestShortNude.PNG"

    # Crossed gloves — her hands sit in front of the crossed arms and the vest
    if _rn_crossed and (_rn_left_glove or _rn_right_glove):
        "images/characters/Rogue_New/Standing/Chest/Crossed/Rogue_StandingCrossedGloves.PNG"

    # ════════════════════════════════════════════════════════
    # LEFT ARM (in front of chest clothes)
    # Within each pose: base → glove → band → vest (back to front)
    # ════════════════════════════════════════════════════════

    # LArm Idle
    if not _rn_crossed and _rn_left_arm == "idle":
        "images/characters/Rogue_New/Standing/LeftArm/LArmIdle/Rogue_StandingLArmIdle.PNG"
    if not _rn_crossed and _rn_left_arm == "idle" and _rn_left_band:
        "images/characters/Rogue_New/Standing/LeftArm/LArmIdle/Rogue_StandingLArmIdleBand.PNG"
    if not _rn_crossed and _rn_left_arm == "idle" and _rn_left_glove:
        "images/characters/Rogue_New/Standing/LeftArm/LArmIdle/Rogue_StandingLArmIdleGlove.PNG"
    if not _rn_crossed and _rn_left_arm == "idle" and _rn_left_vest:
        "images/characters/Rogue_New/Standing/LeftArm/LArmIdle/LArmIdleVest.PNG"

    # LArm 1
    if not _rn_crossed and _rn_left_arm == "1":
        "images/characters/Rogue_New/Standing/LeftArm/LArm1/Rogue_StandingLArm1.PNG"
    if not _rn_crossed and _rn_left_arm == "1" and _rn_left_glove:
        "images/characters/Rogue_New/Standing/LeftArm/LArm1/Rogue_StandingLArm1Glove.PNG"
    if not _rn_crossed and _rn_left_arm == "1" and _rn_left_band:
        "images/characters/Rogue_New/Standing/LeftArm/LArm1/Rogue_StandingLArm1Band.PNG"
    if not _rn_crossed and _rn_left_arm == "1" and _rn_left_vest:
        "images/characters/Rogue_New/Standing/LeftArm/LArm1/Rogue_StandingLArm1Vest.PNG"

    # ════════════════════════════════════════════════════════
    # HEAD (frontmost — hair covers forehead, face overlaps collar)
    # PSD bottom→top: Face, Mouth, Whites, Eyes, Brows, EyeLids, Blush, Hair
    # (file names = the artist's debug names, 2026-10-02)
    # ════════════════════════════════════════════════════════

    # Face base (backmost in Head — skin with transparent areas for features)
    if _rn_face == "base":
        "images/characters/Rogue_New/Standing/Head/Face/Rogue_Headdown__Base.PNG"
    if _rn_face == "base_extend":
        "images/characters/Rogue_New/Standing/Head/Face/Rogue_Headdown__BaseExtend.PNG"

    # Mouth
    if _rn_mouth == "smile":
        "images/characters/Rogue_New/Standing/Head/Mouth/Rogue_Headdown_Mouth_Smile.PNG"
    if _rn_mouth == "grimace":
        "images/characters/Rogue_New/Standing/Head/Mouth/Rogue_Headdown_Mouth_Grimace.PNG"
    if _rn_mouth == "lipbite":
        "images/characters/Rogue_New/Standing/Head/Mouth/Rogue_Headdown_Mouth_Lipbite.PNG"
    if _rn_mouth == "sad":
        "images/characters/Rogue_New/Standing/Head/Mouth/Rogue_Headdown_Mouth_Sad.PNG"
    if _rn_mouth == "open":
        "images/characters/Rogue_New/Standing/Head/Mouth/Rogue_Headdown_Mouth_Open.PNG"
    if _rn_mouth == "tongue":
        "images/characters/Rogue_New/Standing/Head/Mouth/Rogue_Headdown_Mouth_Tongue.PNG"
    if _rn_mouth == "tongue2":
        "images/characters/Rogue_New/Standing/Head/Mouth/Rogue_Headdown_Mouth_Tongue2.PNG"

    # Eye whites
    if _rn_whites == "default":
        "images/characters/Rogue_New/Standing/Head/Whites/Rogue_EyeballDefault.PNG"
    if _rn_whites == "shocked":
        "images/characters/Rogue_New/Standing/Head/Whites/Rogue_EyeballShocked.PNG"

    # Eyes (iris)
    if _rn_eyes == "default":
        "images/characters/Rogue_New/Standing/Head/Eyes/Rogue_Headdown_Eyes.PNG"
    if _rn_eyes == "love":
        "images/characters/Rogue_New/Standing/Head/Eyes/Rogue_Headdown_EyesLove.PNG"

    # Brows
    if _rn_brows == "normal":
        "images/characters/Rogue_New/Standing/Head/Brows/Rogue_Headdown_BrowsNormal.PNG"
    if _rn_brows == "anger":
        "images/characters/Rogue_New/Standing/Head/Brows/Rogue_Headdown_BrowsAnger.PNG"
    if _rn_brows == "sad":
        "images/characters/Rogue_New/Standing/Head/Brows/Rogue_Headdown_BrowsSad.PNG"
    if _rn_brows == "confused":
        "images/characters/Rogue_New/Standing/Head/Brows/Rogue_Headdown_BrowsConfused.PNG"
    if _rn_brows == "shocked":
        "images/characters/Rogue_New/Standing/Head/Brows/Rogue_Headdown_BrowsShocked.PNG"

    # EyeLids
    if _rn_eyelids == "normal":
        "images/characters/Rogue_New/Standing/Head/EyeLids/Rogue_Headdown_EyeNormal.PNG"
    if _rn_eyelids == "shocked":
        "images/characters/Rogue_New/Standing/Head/EyeLids/Rogue_Headdown_EyeShocked.PNG"
    if _rn_eyelids == "sultry":
        "images/characters/Rogue_New/Standing/Head/EyeLids/Rogue_Headdown_EyeSultry.PNG"
    if _rn_eyelids == "closed":
        "images/characters/Rogue_New/Standing/Head/EyeLids/Rogue_Headdown_EyeClosed.PNG"
    if _rn_eyelids == "squint":
        "images/characters/Rogue_New/Standing/Head/EyeLids/Rogue_Headdown_EyeSquint.PNG"
    if _rn_eyelids == "squint2":
        "images/characters/Rogue_New/Standing/Head/EyeLids/Rogue_Headdown_EyeSquint2.PNG"

    # Blush
    if _rn_blush:
        "images/characters/Rogue_New/Standing/Head/Rogue_Headdown__Blush.PNG"

    # Hair (frontmost — covers forehead, falls over shoulders)
    always:
        "images/characters/Rogue_New/Standing/Head/Rogue_Headdown__Hair.PNG"
