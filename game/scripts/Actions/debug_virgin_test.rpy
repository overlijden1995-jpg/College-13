# ============================================================
# DEBUG: Virgin test setup
# Call from console: call debug_virgin_setup
# Sets Gwen as virgin with high enough stats to accept sex,
# teleports to her room, and opens the sex menu.
# ============================================================

label debug_virgin_setup:
    python:
        _gwen = GIRL_BY_ID.get("gwen") or GIRL_BY_ID.get("Gwen")

        # Ensure she has the virgin trait
        if not _gwen.has_trait("virgin"):
            _gwen.add_trait("virgin")

        # Stats high enough to accept everything
        _gwen.Love = max(_gwen.Love, 600)
        _gwen.Inbt = max(_gwen.Inbt, 600)
        _gwen.Obed = max(_gwen.Obed, 400)
        _gwen.Lust = 50
        _gwen.Temptation = 10

        # Intimacy flags: she's done everything up to this point
        if not hasattr(_gwen, "intimacy_flags"):
            _gwen.intimacy_flags = set()
        for _act in ("kiss", "hj", "bj", "tj", "masturbate", "rub", "tip"):
            _gwen.intimacy_flags.add(_act)

        # Sex acts counts (she's experienced with everything except penetration)
        if not hasattr(_gwen, "Sex_acts") or _gwen.Sex_acts is None:
            _gwen.Sex_acts = {k: 0 for k in _SEX_ACT_KEYS}
        _gwen.Sex_acts["kiss"] = max(_gwen.Sex_acts.get("kiss", 0), 5)
        _gwen.Sex_acts["hj"] = max(_gwen.Sex_acts.get("hj", 0), 3)
        _gwen.Sex_acts["bj"] = max(_gwen.Sex_acts.get("bj", 0), 3)
        _gwen.Sex_acts["tj"] = max(_gwen.Sex_acts.get("tj", 0), 2)
        _gwen.Sex_acts["rub"] = max(_gwen.Sex_acts.get("rub", 0), 2)
        _gwen.Sex_acts["tip"] = max(_gwen.Sex_acts.get("tip", 0), 2)

        # Clear cheat path blocks (no condom requirement, all stages passed)
        _gwen._cheat_broke = True
        _gwen._cheat_sex_stage = 3

        # Give player energy
        Player.energy = Player.energy_max

        # Move Gwen to player's location
        _gwen.loc = CurrentLocation
        _gwen.SpriteLoc = StageCenter

        # Show her
        set_girl_sprite(_gwen, pose="standing", at_list=[slot_center])
        store.CurrentGirl = _gwen

        _sync_girl(_gwen)

        debug_log("[DEBUG_VIRGIN] Setup complete:")
        debug_log("[DEBUG_VIRGIN] Love=%s Inbt=%s Obed=%s Lust=%s Tempt=%s" % (_gwen.Love, _gwen.Inbt, _gwen.Obed, _gwen.Lust, _gwen.Temptation))
        debug_log("[DEBUG_VIRGIN] virgin=%s intimacy=%s" % (_gwen.has_trait("virgin"), _gwen.intimacy_flags))
        debug_log("[DEBUG_VIRGIN] Sex_acts=%s" % str(_gwen.Sex_acts))

    "Gwen is ready. Virgin, high stats, all prior acts done. Choose Fuck her."

    call sex_menu(_gwen, CurrentLocation, TimeIndex) from _call_sex_menu_debug_virgin

    return
