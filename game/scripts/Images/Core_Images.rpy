# ============================================================
# rod_handjob_core.rpy
# Generic optimized handjob animation system (no ConditionSwitch)
# ============================================================

init -5 python:
    # Per-Girl visual tuning ONLY (offset/zoom/zorder).
    # Assets/layers stay in each Girl's layeredimage.
    hj_cfg = {
        # "gwen": {"xoff": 200, "yoff": 800, "zoom": 0.60, "z": 150},
    }

    def get_hj_cfg(Girl):
        tag = getattr(Girl, "Name", "").lower()
        c = hj_cfg.get(tag, None)
        if not c:
            return {"xoff": 200, "yoff": 800, "zoom": 0.60, "z": 150}
        # Fill defaults if partial
        return {
            "xoff": c.get("xoff", 200),
            "yoff": c.get("yoff", 800),
            "zoom": c.get("zoom", 0.60),
            "z":    c.get("z", 150),
        }

    def girl_key(girl):
        """
        Returns a lowercase key based on girl.Name.
        Used to build image names like: '<key> handjob'
        """
        if girl and hasattr(girl, "Name") and girl.Name:
            return unicode(girl.Name).strip().lower()
        return "unknown"

    def _ssg(gid, key, default=None):
        return sprite_state.get(gid, {}).get(key, default)

    def _gs(scene_key, field, default=None):
        girl = getattr(store, "_%s_girl" % scene_key, None)
        if not girl:
            return default
        return sprite_state.get(girl.Id, {}).get(field, default)

    renpy._orig_ssg = _ssg
    renpy._orig_gs = _gs
    renpy.pure("_ssg")
    renpy.pure("_gs")

    def _hide_non_scene_girls(girl):
        _near = roster_get_near()
        _wr_gid = getattr(store, "_recording_watcher_gid", None)
        for _other in ALL_GIRLS:
            if _other is not girl and _other not in _near and _other.gid != _wr_gid:
                hide_girl_sprite(_other)

    def scene_show(name, at_list=None, tag=None, zorder=None, what=None):
        """renpy.show for a scene layer that can be still. Shown again with NO transform (an empty at_list), Ren'Py
        keeps the transform the tag is already running (config.keep_running_transform, scenelists.py), so a layer
        told to stop went on with its last motion: after his cum the "freeze" of Shion's doggy kept every layer
        thrusting at speed 4, and the cum drip, new and transform-less, stood still on a moving body (author,
        2026-10-11). A still layer is hidden first, so it really stops (RCG_CumAnim hides its layers by hand for the
        same reason)."""
        _tag = tag or name.split()[0]
        if not at_list:
            renpy.hide(_tag)
        _kw = {"at_list": at_list or [], "tag": _tag}
        if zorder is not None:
            _kw["zorder"] = zorder
        if what is not None:
            _kw["what"] = what
        renpy.show(name, **_kw)

    # (the 2026-10-10 scene-edge rollback barriers lived here for one day: the author rolled them back
    # on 2026-10-11, "como era antes"; the one wall left is after_load, script.rpy)

    def _clear_scene_refs(except_key=None):
        _SCENE_KEYS = ["cowgirl", "rcg", "hj", "bj", "titjob", "fn", "doggy", "laying", "scg", "srcg", "sdg", "ft", "rj"]
        for _k in _SCENE_KEYS:
            if _k != except_key:
                setattr(store, "_%s_girl" % _k, None)

    def _scene_blink_loop(girl, girl_var, blink_var, is_active_fn=None, cs_girls=None, blink_timing=(0.10, 0.18), running_var=None):
        import time as _time, random as _random

        def _is_active():
            if is_active_fn:
                return is_active_fn(girl)
            return getattr(store, girl_var) is girl

        _do_restart = cs_girls is None or girl.gid in cs_girls

        if running_var:
            setattr(store, running_var, True)

        try:
            while _is_active():
                _time.sleep(_random.uniform(3.0, 6.0))
                if not _is_active():
                    break
                setattr(store, blink_var, True)
                if _do_restart:
                    renpy.restart_interaction()
                _time.sleep(_random.uniform(*blink_timing))
                if not _is_active():
                    break
                setattr(store, blink_var, False)
                if _do_restart:
                    renpy.restart_interaction()
        finally:
            setattr(store, blink_var, False)
            if running_var:
                setattr(store, running_var, False)

    def _scene_cs_blink_loop(girl, girl_var, is_active_fn=None, blink_timing=(0.10, 0.18)):
        """Blink loop for ConditionSwitch girls — toggles sprite_state['eyes'] to 'eyes_blinking'."""
        import time as _time, random as _random

        def _is_active():
            if is_active_fn:
                return is_active_fn(girl)
            return getattr(store, girl_var) is girl

        try:
            while _is_active():
                _time.sleep(_random.uniform(3.0, 6.0))
                if not _is_active():
                    break
                _state = sprite_state.setdefault(girl.Id, {})
                _saved_eyes = _state.get("eyes", "eyes_normal")
                _state["eyes"] = "eyes_blinking"
                renpy.restart_interaction()
                _time.sleep(_random.uniform(*blink_timing))
                if not _is_active():
                    break
                if _state.get("eyes") == "eyes_blinking":
                    _state["eyes"] = _saved_eyes
                renpy.restart_interaction()
        finally:
            _state = sprite_state.get(girl.Id, {})
            if _state.get("eyes") == "eyes_blinking":
                _state["eyes"] = "eyes_normal"

    def _scene_expression_cycle(girl, girl_var, speed_var,
                                  eyes_by_speed, brows_by_speed, mouth_by_speed,
                                  is_active_fn=None, sleep_range=(7.0, 14.0),
                                  cs_girls=None, refresh_fn=None,
                                  guard_fn=None, pool_override_fn=None):
        def _is_active():
            if is_active_fn:
                return is_active_fn(girl)
            return getattr(store, girl_var) is girl

        _do_restart = cs_girls is None or girl.gid in cs_girls
        import time as _time

        while _is_active():
            _time.sleep(renpy.random.uniform(*sleep_range))
            if not _is_active():
                break
            if getattr(store, "_witness_expression_lock", False):
                continue
            if guard_fn and not guard_fn(girl):
                continue

            speed = getattr(store, speed_var, 0)

            eyes_pool = eyes_by_speed.get(speed, ["eyes_normal"])
            brows_pool = brows_by_speed.get(speed, ["brows_normal"])
            mouth_pool = mouth_by_speed.get(speed, ["mouth_normal"])

            if girl.has_trait("lesbian") and getattr(store, "_coercion_type", None):
                if speed <= 1:
                    eyes_pool = ["eyes_side", "eyes_side_2", "eyes_squint"]
                    brows_pool = ["brows_confused", "brows_sad"]
                    mouth_pool = ["mouth_serious", "mouth_normal", "mouth_sad"]
                else:
                    eyes_pool = ["eyes_squint", "eyes_side", "eyes_closed"]
                    brows_pool = ["brows_confused", "brows_surprised"]
                    mouth_pool = ["mouth_serious", "mouth_surprised", "mouth_normal"]

            if pool_override_fn:
                eyes_pool, brows_pool, mouth_pool = pool_override_fn(girl, speed, eyes_pool, brows_pool, mouth_pool)

            state = sprite_state.setdefault(girl.Id, {})
            state["eyes"] = renpy.random.choice(eyes_pool)
            state["brows"] = renpy.random.choice(brows_pool)
            state["mouth"] = renpy.random.choice(mouth_pool)

            if refresh_fn:
                refresh_fn(girl, state)
            elif _do_restart:
                renpy.restart_interaction()

    # ============================================================
    # EXPRESSION PRESET SYSTEM
    # ============================================================
    # Universal per-pose expression presets. Lookup chain:
    #   1. GIRL_POSE_EXPRESSIONS[gid][pose][expr]  (girl-specific override)
    #   2. POSE_EXPRESSIONS[pose][expr]             (universal pose default)
    #   3. POSE_EXPRESSIONS["standing"][expr]        (universal fallback)

    POSE_EXPRESSIONS = {
        "standing": {
            "normal":           {"eyes": "eyes_normal",      "brows": "brows_normal",    "mouth": "mouth_normal"},
            "happy":            {"eyes": "eyes_normal",      "brows": "brows_normal",    "mouth": "mouth_smile"},
            "laugh":            {"eyes": "eyes_normal",      "brows": "brows_normal",    "mouth": "mouth_laugh"},
            "surprised":        {"eyes": "eyes_surprised",   "brows": "brows_surprised", "mouth": "mouth_surprised"},
            "scared":           {"eyes": "eyes_surprised",   "brows": "brows_surprised", "mouth": "mouth_scared"},
            "angry":            {"eyes": "eyes_squint",      "brows": "brows_surprised", "mouth": "mouth_serious"},
            "sad":              {"eyes": "eyes_normal",      "brows": "brows_sad",       "mouth": "mouth_sad"},
            "sexy":             {"eyes": "eyes_normal",      "brows": "brows_normal",    "mouth": "mouth_smile"},
            "kissing":          {"eyes": "eyes_closed",      "brows": "brows_normal",    "mouth": "mouth_kissing"},
            "lewd":             {"eyes": "eyes_normal",      "brows": "brows_horny",     "mouth": "mouth_tongue"},
            "smug":             {"eyes": "eyes_normal",      "brows": "brows_horny",     "mouth": "mouth_lipbite"},
            "shy":              {"eyes": "eyes_squint",      "brows": "brows_confused",  "mouth": "mouth_smile"},
            "uncomfortable":    {"eyes": "eyes_squint",      "brows": "brows_confused",  "mouth": "mouth_surprised"},
            "lipbite":          {"eyes": "eyes_squint",      "brows": "brows_horny",     "mouth": "mouth_lipbite"},
            "pleasure":         {"eyes": "eyes_squint",      "brows": "brows_horny",     "mouth": "mouth_open_teeth"},
            "pleasure_intense": {"eyes": "eyes_squint_big",  "brows": "brows_horny",     "mouth": "mouth_tongue"},
            "disgusted":        {"eyes": "eyes_squint",      "brows": "brows_confused",  "mouth": "mouth_disgusted"},
            "closed_happy":     {"eyes": "eyes_closed",      "brows": "brows_normal",    "mouth": "mouth_smile"},
            "serious":          {"eyes": "eyes_normal",      "brows": "brows_normal",    "mouth": "mouth_serious"},
            "moaning":          {"eyes": "eyes_squint",      "brows": "brows_horny",     "mouth": "mouth_surprised"},
            "cumming":          {"eyes": "eyes_closed",      "brows": "brows_horny",     "mouth": "mouth_tongue"},
            "ahegao":           {"eyes": "eyes_surprised_2", "brows": "brows_surprised", "mouth": "mouth_tongue"},
            "ahegao_2":         {"eyes": "eyes_squint_big",  "brows": "brows_surprised", "mouth": "mouth_tongue"},
            "smile":            {"eyes": "eyes_normal",      "brows": "brows_normal",    "mouth": "mouth_smile"},
            "sly":              {"eyes": "eyes_squint",      "brows": "brows_confused",  "mouth": "mouth_smile"},
            "confused":         {"eyes": "eyes_normal",      "brows": "brows_confused",  "mouth": "mouth_serious"},
            "embarrassed":      {"eyes": "eyes_side",        "brows": "brows_confused",  "mouth": "mouth_smile"},
            "lusty":            {"eyes": "eyes_squint",      "brows": "brows_normal",    "mouth": "mouth_lipbite"},
            "smirk":            {"eyes": "eyes_normal",      "brows": "brows_confused",  "mouth": "mouth_smile"},
            "startled":         {"eyes": "eyes_surprised",   "brows": "brows_surprised", "mouth": "mouth_open_teeth"},
            "worried":          {"eyes": "eyes_side_2",      "brows": "brows_confused",  "mouth": "mouth_serious"},
            "nervous":          {"eyes": "eyes_side",        "brows": "brows_sad",       "mouth": "mouth_serious"},
            "grimace":          {"eyes": "eyes_normal",      "brows": "brows_normal",    "mouth": "mouth_disgusted"},
            "bemused":          {"eyes": "eyes_squint",      "brows": "brows_normal",    "mouth": "mouth_smile"},
            "perplexed":        {"eyes": "eyes_squint",      "brows": "brows_confused",  "mouth": "mouth_serious"},
            "neutral":          {"eyes": "eyes_normal",      "brows": "brows_normal",    "mouth": "mouth_normal"},
            "annoyed":          {"eyes": "eyes_side",        "brows": "brows_confused",  "mouth": "mouth_serious"},
            "thinking":         {"eyes": "eyes_side_2",      "brows": "brows_normal",    "mouth": "mouth_normal"},
            "surprise":         {"eyes": "eyes_surprised",   "brows": "brows_surprised", "mouth": "mouth_surprised"},
            "looking_down":     {"eyes": "eyes_looking_down","brows": "brows_normal",    "mouth": "mouth_normal"},
            "looking_left":     {"eyes": "eyes_looking_left","brows": "brows_normal",    "mouth": "mouth_normal"},
            "looking_right":    {"eyes": "eyes_looking_right","brows": "brows_normal",   "mouth": "mouth_normal"},
            "pleasure_mild":    {"eyes": "eyes_squint",      "brows": "brows_confused",  "mouth": "mouth_lipbite"},
        },

        "handjob": {
            "cumming":          {"eyes": "eyes_closed",      "brows": "brows_sad",       "mouth": "mouth_tongue"},
            "looking_down":     {"eyes": "eyes_side_2",      "brows": "brows_normal",    "mouth": "mouth_normal"},
            "looking_left":     {"eyes": "eyes_side",        "brows": "brows_normal",    "mouth": "mouth_normal"},
            "looking_right":    {"eyes": "eyes_looking_right","brows": "brows_normal",   "mouth": "mouth_normal"},
        },

        # The footjob head (Tenny/Footjob.rpy ft_head) has its own attribute set: without this block the standing
        # presets leak names its ConditionSwitch does not know (eyes_squint, brows_horny...) and the face stays
        # neutral through every tease and action
        "footjob": {
            "normal":           {"eyes": "eyes_normal",      "brows": "brows_normal",     "mouth": "mouth_normal"},
            "neutral":          {"eyes": "eyes_normal",      "brows": "brows_normal",     "mouth": "mouth_normal"},
            "happy":            {"eyes": "eyes_normal",      "brows": "brows_normal",     "mouth": "mouth_smile"},
            "smile":            {"eyes": "eyes_normal",      "brows": "brows_normal",     "mouth": "mouth_smile"},
            "laugh":            {"eyes": "eyes_normal",      "brows": "brows_normal",     "mouth": "mouth_laugh"},
            "surprised":        {"eyes": "eyes_up",          "brows": "brows_surprised",  "mouth": "mouth_moaning_2"},
            "surprise":         {"eyes": "eyes_up",          "brows": "brows_surprised",  "mouth": "mouth_moaning_2"},
            "startled":         {"eyes": "eyes_up_closed_surprised", "brows": "brows_surprised", "mouth": "mouth_moaning_2"},
            "scared":           {"eyes": "eyes_away",        "brows": "brows_scared",     "mouth": "mouth_scared"},
            "angry":            {"eyes": "eyes_normal",      "brows": "brows_angry",      "mouth": "mouth_angry"},
            "sad":              {"eyes": "eyes_away",        "brows": "brows_sad",        "mouth": "mouth_sad"},
            "sexy":             {"eyes": "eyes_sexy",        "brows": "brows_normal",     "mouth": "mouth_smile"},
            "kissing":          {"eyes": "eyes_closed",      "brows": "brows_normal",     "mouth": "mouth_kiss"},
            "lewd":             {"eyes": "eyes_sexy_2",      "brows": "brows_normal",     "mouth": "mouth_tongue"},
            "smug":             {"eyes": "eyes_sexy",        "brows": "brows_normal",     "mouth": "mouth_lipbite"},
            "shy":              {"eyes": "eyes_away",        "brows": "brows_sad",        "mouth": "mouth_smile"},
            "embarrassed":      {"eyes": "eyes_away",        "brows": "brows_confused",   "mouth": "mouth_smile"},
            "uncomfortable":    {"eyes": "eyes_side_2",      "brows": "brows_sad",        "mouth": "mouth_sad"},
            "lipbite":          {"eyes": "eyes_sexy",        "brows": "brows_normal",     "mouth": "mouth_lipbite"},
            "lusty":            {"eyes": "eyes_sexy_2",      "brows": "brows_normal",     "mouth": "mouth_lipbite"},
            "pleasure":         {"eyes": "eyes_bliss",       "brows": "brows_normal",     "mouth": "mouth_moaning"},
            "pleasure_mild":    {"eyes": "eyes_sexy",        "brows": "brows_confused",   "mouth": "mouth_lipbite"},
            "pleasure_intense": {"eyes": "eyes_ahegao",      "brows": "brows_surprised",  "mouth": "mouth_moaning_3"},
            "moaning":          {"eyes": "eyes_bliss",       "brows": "brows_surprised",  "mouth": "mouth_moaning"},
            "cumming":          {"eyes": "eyes_closed",      "brows": "brows_surprised",  "mouth": "mouth_moaning_3"},
            "ahegao":           {"eyes": "eyes_ahegao",      "brows": "brows_surprised",  "mouth": "mouth_tongue"},
            "ahegao_2":         {"eyes": "eyes_ahegao_2",    "brows": "brows_surprised",  "mouth": "mouth_tongue"},
            "disgusted":        {"eyes": "eyes_side_2",      "brows": "brows_angry",      "mouth": "mouth_sad"},
            "closed_happy":     {"eyes": "eyes_closed",      "brows": "brows_normal",     "mouth": "mouth_smile"},
            "serious":          {"eyes": "eyes_normal",      "brows": "brows_determined", "mouth": "mouth_normal"},
            "sly":              {"eyes": "eyes_sexy",        "brows": "brows_normal",     "mouth": "mouth_smile"},
            "confused":         {"eyes": "eyes_normal",      "brows": "brows_confused",   "mouth": "mouth_normal"},
            "smirk":            {"eyes": "eyes_normal",      "brows": "brows_confused",   "mouth": "mouth_smile"},
            "worried":          {"eyes": "eyes_side_2",      "brows": "brows_sad",        "mouth": "mouth_normal"},
            "nervous":          {"eyes": "eyes_side",        "brows": "brows_sad",        "mouth": "mouth_normal"},
            "grimace":          {"eyes": "eyes_normal",      "brows": "brows_angry",      "mouth": "mouth_sad"},
            "bemused":          {"eyes": "eyes_sexy",        "brows": "brows_normal",     "mouth": "mouth_smile"},
            "perplexed":        {"eyes": "eyes_normal",      "brows": "brows_perplexed_2","mouth": "mouth_normal"},
            "annoyed":          {"eyes": "eyes_side",        "brows": "brows_angry",      "mouth": "mouth_normal"},
            "thinking":         {"eyes": "eyes_up",          "brows": "brows_normal",     "mouth": "mouth_normal"},
            "looking_down":     {"eyes": "eyes_away",        "brows": "brows_normal",     "mouth": "mouth_normal"},
            "looking_left":     {"eyes": "eyes_side",        "brows": "brows_normal",     "mouth": "mouth_normal"},
            "looking_right":    {"eyes": "eyes_side_2",      "brows": "brows_normal",     "mouth": "mouth_normal"},
        },

        "blowjob": {
            "normal":           {"eyes": "eyes_normal",      "brows": "brows_normal",    "mouth": "mouth_tongue"},
            "happy":            {"eyes": "eyes_normal",      "brows": "brows_normal",    "mouth": "mouth_happy"},
            "kissing":          {"eyes": "eyes_closed",      "brows": "brows_normal",    "mouth": "mouth_lipbite"},
            "scared":           {"eyes": "eyes_surprised",   "brows": "brows_sad",       "mouth": "mouth_scared"},
            "angry":            {"eyes": "eyes_squint",      "brows": "brows_surprised", "mouth": "mouth_angry"},
            "sad":              {"eyes": "eyes_normal",      "brows": "brows_sad",       "mouth": "mouth_sad"},
            "sexy":             {"eyes": "eyes_normal",      "brows": "brows_normal",    "mouth": "mouth_lipbite"},
            "cumming":          {"eyes": "eyes_closed",      "brows": "brows_normal",    "mouth": "mouth_tongue"},
            "ahegao":           {"eyes": "eyes_surprised",   "brows": "brows_normal",    "mouth": "mouth_tongue"},
            "ahegao_2":         {"eyes": "eyes_squint_2",    "brows": "brows_surprised", "mouth": "mouth_tongue"},
            "lewd":             {"eyes": "eyes_normal",      "brows": "brows_normal",    "mouth": "mouth_tongue"},
            "smug":             {"eyes": "eyes_squint",      "brows": "brows_normal",    "mouth": "mouth_lipbite"},
            "shy":              {"eyes": "eyes_right_closed", "brows": "brows_sad",      "mouth": "mouth_smile"},
            "lipbite":          {"eyes": "eyes_squint",      "brows": "brows_normal",    "mouth": "mouth_lipbite"},
            "pleasure":         {"eyes": "eyes_squint",      "brows": "brows_confused",  "mouth": "mouth_happy"},
            "pleasure_intense": {"eyes": "eyes_squint_2",    "brows": "brows_surprised", "mouth": "mouth_tongue"},
            "disgusted":        {"eyes": "eyes_squint",      "brows": "brows_confused",  "mouth": "mouth_sad"},
            "closed_happy":     {"eyes": "eyes_closed_happy", "brows": "brows_normal",   "mouth": "mouth_lipbite"},
            "moaning":          {"eyes": "eyes_squint",      "brows": "brows_confused",  "mouth": "mouth_surprised"},
            "uncomfortable":    {"eyes": "eyes_squint_2",    "brows": "brows_sad",       "mouth": "mouth_sad"},
            "laugh":            {"eyes": "eyes_closed_happy", "brows": "brows_normal",   "mouth": "mouth_happy"},
            "surprised":        {"eyes": "eyes_normal",      "brows": "brows_surprised", "mouth": "mouth_surprised"},
            "serious":          {"eyes": "eyes_normal",      "brows": "brows_normal",    "mouth": "mouth_angry"},
            "smile":            {"eyes": "eyes_normal",      "brows": "brows_normal",    "mouth": "mouth_smile"},
            "sly":              {"eyes": "eyes_squint",      "brows": "brows_confused",  "mouth": "mouth_smile"},
            "confused":         {"eyes": "eyes_normal",      "brows": "brows_confused",  "mouth": "mouth_angry"},
            "embarrassed":      {"eyes": "eyes_looking_left","brows": "brows_confused",  "mouth": "mouth_smile"},
            "lusty":            {"eyes": "eyes_squint",      "brows": "brows_normal",    "mouth": "mouth_lipbite"},
            "smirk":            {"eyes": "eyes_normal",      "brows": "brows_confused",  "mouth": "mouth_smile"},
            "startled":         {"eyes": "eyes_normal",      "brows": "brows_surprised", "mouth": "mouth_happy"},
            "worried":          {"eyes": "eyes_looking_right","brows": "brows_confused",  "mouth": "mouth_angry"},
            "grimace":          {"eyes": "eyes_normal",      "brows": "brows_normal",    "mouth": "mouth_sad"},
            "bemused":          {"eyes": "eyes_squint",      "brows": "brows_normal",    "mouth": "mouth_smile"},
            "perplexed":        {"eyes": "eyes_squint",      "brows": "brows_confused",  "mouth": "mouth_angry"},
            "neutral":          {"eyes": "eyes_normal",      "brows": "brows_normal",    "mouth": "mouth_smile"},
            "surprise":         {"eyes": "eyes_normal",      "brows": "brows_surprised", "mouth": "mouth_surprised"},
            "looking_down":     {"eyes": "eyes_normal",      "brows": "brows_normal",    "mouth": "mouth_smile"},
            "looking_left":     {"eyes": "eyes_looking_left","brows": "brows_normal",    "mouth": "mouth_smile"},
            "looking_right":    {"eyes": "eyes_looking_right","brows": "brows_normal",   "mouth": "mouth_smile"},
        },

        "titjob": {
            "surprised":        {"eyes": "eyes_normal",      "brows": "brows_confused",  "mouth": "mouth_surprised"},
            "cumming":          {"eyes": "eyes_closed",      "brows": "brows_sad",       "mouth": "mouth_ahegao"},
            "ahegao":           {"eyes": "eyes_squint",      "brows": "brows_sad",       "mouth": "mouth_ahegao"},
            "ahegao_2":         {"eyes": "eyes_closed",      "brows": "brows_sad",       "mouth": "mouth_ahegao"},
            "looking_down":     {"eyes": "eyes_normal",      "brows": "brows_normal",    "mouth": "mouth_normal"},
            "looking_left":     {"eyes": "eyes_looking_left","brows": "brows_normal",    "mouth": "mouth_normal"},
            "looking_right":    {"eyes": "eyes_looking_right","brows": "brows_normal",   "mouth": "mouth_normal"},
        },

        "cowgirl": {
            "kissing":          {"eyes": "eyes_closed",      "brows": "brows_normal",    "mouth": "mouth_smile"},
            "sexy":             {"eyes": "eyes_normal",      "brows": "brows_horny",     "mouth": "mouth_tongue"},
            "cumming":          {"eyes": "eyes_closed",      "brows": "brows_horny",     "mouth": "mouth_tongue"},
            "ahegao":           {"eyes": "eyes_surprised",   "brows": "brows_horny",     "mouth": "mouth_tongue"},
            "ahegao_2":         {"eyes": "eyes_squint_big",  "brows": "brows_horny",     "mouth": "mouth_tongue"},
            "moaning":          {"eyes": "eyes_squint",      "brows": "brows_horny",     "mouth": "mouth_surprised"},
            "looking_down":     {"eyes": "eyes_side",        "brows": "brows_normal",    "mouth": "mouth_normal"},
            "looking_left":     {"eyes": "eyes_side",        "brows": "brows_normal",    "mouth": "mouth_normal"},
            "looking_right":    {"eyes": "eyes_side_2",      "brows": "brows_normal",    "mouth": "mouth_normal"},
        },

        "reverse_cowgirl": {
            "happy":            {"eyes": "eyes_looking_to_player", "brows": "brows_normal",    "mouth": "mouth_smile"},
            "scared":           {"eyes": "eyes_surprised",   "brows": "brows_surprised", "mouth": "mouth_scared"},
            "angry":            {"eyes": "eyes_looking_to_player", "brows": "brows_surprised", "mouth": "mouth_scared"},
            "sexy":             {"eyes": "eyes_looking_to_player", "brows": "brows_horny",     "mouth": "mouth_lipbite"},
            "kissing":          {"eyes": "eyes_closed",      "brows": "brows_normal",    "mouth": "mouth_kiss"},
            "cumming":          {"eyes": "eyes_closed",      "brows": "brows_horny",     "mouth": "mouth_tongue"},
            "ahegao":           {"eyes": "eyes_surprised",   "brows": "brows_surprised", "mouth": "mouth_tongue"},
            "ahegao_2":         {"eyes": "eyes_squint_2",    "brows": "brows_surprised", "mouth": "mouth_tongue"},
            "moaning":          {"eyes": "eyes_squint",      "brows": "brows_horny",     "mouth": "mouth_surprised"},
            "pleasure":         {"eyes": "eyes_looking_up",  "brows": "brows_horny",     "mouth": "mouth_tongue"},
            "lewd":             {"eyes": "eyes_looking_to_player", "brows": "brows_horny",     "mouth": "mouth_tongue"},
            "smug":             {"eyes": "eyes_looking_to_player", "brows": "brows_horny",     "mouth": "mouth_lipbite"},
            "shy":              {"eyes": "eyes_squint",      "brows": "brows_sad",       "mouth": "mouth_smile"},
            "uncomfortable":    {"eyes": "eyes_squint",      "brows": "brows_confused",  "mouth": "mouth_scared"},
            "looking_down":     {"eyes": "eyes_side",        "brows": "brows_normal",    "mouth": "mouth_normal"},
            "looking_left":     {"eyes": "eyes_side",        "brows": "brows_normal",    "mouth": "mouth_normal"},
            "looking_right":    {"eyes": "eyes_side_2",      "brows": "brows_normal",    "mouth": "mouth_normal"},
        },

        "doggy": {
            "normal":           {"eyes": "eyes_normal",            "brows": "brows_normal",    "mouth": "mouth_normal"},
            "happy":            {"eyes": "eyes_looking_to_player", "brows": "brows_normal",    "mouth": "mouth_smile"},
            "laugh":            {"eyes": "eyes_looking_to_player", "brows": "brows_normal",    "mouth": "mouth_laugh"},
            "surprised":        {"eyes": "eyes_looking_to_player", "brows": "brows_surprised", "mouth": "mouth_surprised"},
            "scared":           {"eyes": "eyes_looking_to_player", "brows": "brows_surprised", "mouth": "mouth_scared"},
            "angry":            {"eyes": "eyes_squint",            "brows": "brows_confused",  "mouth": "mouth_serious"},
            "sad":              {"eyes": "eyes_squint",            "brows": "brows_sad",       "mouth": "mouth_scared"},
            "sexy":             {"eyes": "eyes_looking_to_player", "brows": "brows_horny",     "mouth": "mouth_lipbite"},
            "kissing":          {"eyes": "eyes_closed",            "brows": "brows_normal",    "mouth": "mouth_kiss"},
            "lewd":             {"eyes": "eyes_looking_to_player", "brows": "brows_horny",     "mouth": "mouth_tongue"},
            "smug":             {"eyes": "eyes_looking_to_player", "brows": "brows_horny",     "mouth": "mouth_lipbite"},
            "shy":              {"eyes": "eyes_squint",            "brows": "brows_sad",       "mouth": "mouth_smile"},
            "uncomfortable":    {"eyes": "eyes_squint",            "brows": "brows_confused",  "mouth": "mouth_scared"},
            "lipbite":          {"eyes": "eyes_looking_to_player", "brows": "brows_horny",     "mouth": "mouth_lipbite"},
            "pleasure":         {"eyes": "eyes_looking_up",        "brows": "brows_horny",     "mouth": "mouth_tongue"},
            "pleasure_intense": {"eyes": "eyes_squint_big",        "brows": "brows_horny",     "mouth": "mouth_tongue"},
            "disgusted":        {"eyes": "eyes_squint",            "brows": "brows_confused",  "mouth": "mouth_disgusted"},
            "closed_happy":     {"eyes": "eyes_closed",            "brows": "brows_normal",    "mouth": "mouth_smile"},
            "serious":          {"eyes": "eyes_looking_to_player", "brows": "brows_normal",    "mouth": "mouth_serious"},
            "moaning":          {"eyes": "eyes_squint",            "brows": "brows_horny",     "mouth": "mouth_surprised"},
            "cumming":          {"eyes": "eyes_closed",            "brows": "brows_horny",     "mouth": "mouth_tongue"},
            "ahegao":           {"eyes": "eyes_surprised",         "brows": "brows_surprised", "mouth": "mouth_tongue"},
            "ahegao_2":         {"eyes": "eyes_squint",            "brows": "brows_horny",     "mouth": "mouth_tongue"},
            "looking_down":     {"eyes": "eyes_normal",            "brows": "brows_normal",    "mouth": "mouth_normal"},
            "looking_left":     {"eyes": "eyes_normal",            "brows": "brows_normal",    "mouth": "mouth_normal"},
            "looking_right":    {"eyes": "eyes_looking_to_player", "brows": "brows_normal",    "mouth": "mouth_normal"},
        },

        "laying_down": {
            "normal":           {"eyes": "eyes_normal",            "brows": "brows_normal",    "mouth": "mouth_normal"},
            "happy":            {"eyes": "eyes_looking_to_player", "brows": "brows_normal",    "mouth": "mouth_smile"},
            "laugh":            {"eyes": "eyes_looking_to_player", "brows": "brows_normal",    "mouth": "mouth_laugh"},
            "surprised":        {"eyes": "eyes_looking_to_player", "brows": "brows_surprised", "mouth": "mouth_surprised"},
            "scared":           {"eyes": "eyes_surprised",         "brows": "brows_scared",    "mouth": "mouth_scared"},
            "angry":            {"eyes": "eyes_squint",            "brows": "brows_angry",     "mouth": "mouth_angry"},
            "sad":              {"eyes": "eyes_squint",            "brows": "brows_sad",       "mouth": "mouth_sad"},
            "sexy":             {"eyes": "eyes_sexy",              "brows": "brows_horny",     "mouth": "mouth_lipbite"},
            "kissing":          {"eyes": "eyes_closed",            "brows": "brows_normal",    "mouth": "mouth_kiss"},
            "lewd":             {"eyes": "eyes_looking_to_player", "brows": "brows_horny",     "mouth": "mouth_tongue"},
            "smug":             {"eyes": "eyes_looking_to_player", "brows": "brows_horny",     "mouth": "mouth_lipbite"},
            "shy":              {"eyes": "eyes_side",              "brows": "brows_confused",   "mouth": "mouth_smile"},
            "uncomfortable":    {"eyes": "eyes_squint",            "brows": "brows_confused",   "mouth": "mouth_scared"},
            "lipbite":          {"eyes": "eyes_sexy",              "brows": "brows_horny",     "mouth": "mouth_lipbite"},
            "pleasure":         {"eyes": "eyes_looking_up",        "brows": "brows_horny",     "mouth": "mouth_moaning"},
            "pleasure_intense": {"eyes": "eyes_squint_2",          "brows": "brows_horny",     "mouth": "mouth_tongue"},
            "disgusted":        {"eyes": "eyes_squint",            "brows": "brows_confused",   "mouth": "mouth_sad"},
            "closed_happy":     {"eyes": "eyes_closed_happy",      "brows": "brows_normal",    "mouth": "mouth_smile"},
            "serious":          {"eyes": "eyes_looking_to_player", "brows": "brows_normal",    "mouth": "mouth_angry"},
            "moaning":          {"eyes": "eyes_squint",            "brows": "brows_horny",     "mouth": "mouth_moaning"},
            "cumming":          {"eyes": "eyes_closed",            "brows": "brows_horny",     "mouth": "mouth_tongue"},
            "ahegao":           {"eyes": "eyes_ahegao",            "brows": "brows_surprised", "mouth": "mouth_ahegao"},
            "ahegao_2":         {"eyes": "eyes_ahegao_2",          "brows": "brows_horny",     "mouth": "mouth_ahegao"},
            "smile":            {"eyes": "eyes_normal",            "brows": "brows_normal",    "mouth": "mouth_smile"},
            "sly":              {"eyes": "eyes_squint",            "brows": "brows_confused",   "mouth": "mouth_smile"},
            "confused":         {"eyes": "eyes_normal",            "brows": "brows_confused",   "mouth": "mouth_normal"},
            "embarrassed":      {"eyes": "eyes_side",              "brows": "brows_confused",   "mouth": "mouth_smile"},
            "lusty":            {"eyes": "eyes_squint",            "brows": "brows_horny",     "mouth": "mouth_lipbite"},
            "smirk":            {"eyes": "eyes_side",              "brows": "brows_confused",   "mouth": "mouth_smile"},
            "startled":         {"eyes": "eyes_surprised",         "brows": "brows_surprised", "mouth": "mouth_surprised"},
            "worried":          {"eyes": "eyes_side_2",            "brows": "brows_confused",   "mouth": "mouth_sad"},
            "nervous":          {"eyes": "eyes_side",              "brows": "brows_sad",       "mouth": "mouth_normal"},
            "grimace":          {"eyes": "eyes_normal",            "brows": "brows_normal",    "mouth": "mouth_sad"},
            "bemused":          {"eyes": "eyes_squint",            "brows": "brows_normal",    "mouth": "mouth_smile"},
            "perplexed":        {"eyes": "eyes_squint",            "brows": "brows_confused",   "mouth": "mouth_normal"},
            "neutral":          {"eyes": "eyes_normal",            "brows": "brows_normal",    "mouth": "mouth_normal"},
            "surprise":         {"eyes": "eyes_surprised",         "brows": "brows_surprised", "mouth": "mouth_surprised"},
            "looking_down":     {"eyes": "eyes_normal",            "brows": "brows_normal",    "mouth": "mouth_normal"},
            "looking_left":     {"eyes": "eyes_looking_left",      "brows": "brows_normal",    "mouth": "mouth_normal"},
            "looking_right":    {"eyes": "eyes_looking_right",     "brows": "brows_normal",    "mouth": "mouth_normal"},
            "pleasure_mild":    {"eyes": "eyes_squint",            "brows": "brows_confused",   "mouth": "mouth_lipbite"},
        },
    }

    _BJ_BROWS_MAP = {
        "gwen":  {"brows_normal": 1, "brows_sad": 2, "brows_confused": 3, "brows_surprised": 4, "brows_horny": 1, "brows_maniac": 5, "brows_up": 4, "brows_challenging": 3, "brows_confused_2": 3},
        "rogue": {"brows_normal": 1, "brows_sad": 2, "brows_confused": 3, "brows_surprised": 4, "brows_horny": 1, "brows_maniac": 5, "brows_up": 4, "brows_challenging": 3, "brows_confused_2": 3},
        "ntw":   {"brows_normal": 1, "brows_confused": 2, "brows_surprised": 3, "brows_sad": 4, "brows_horny": 1, "brows_maniac": 5, "brows_up": 3, "brows_challenging": 2, "brows_confused_2": 2},
        "tenny": {"brows_normal": 1, "brows_sad": 2, "brows_confused": 3, "brows_confused_2": 4, "brows_angry": 5, "brows_surprised": 4, "brows_horny": 1, "brows_maniac": 5, "brows_up": 4, "brows_challenging": 3, "brows_scared": 6},
        "shion": {"brows_normal": 1, "brows_sad": 2, "brows_confused": 3, "brows_confused_2": 4, "brows_angry": 5, "brows_surprised": 4, "brows_horny": 1, "brows_maniac": 5, "brows_up": 4, "brows_challenging": 6, "brows_worried": 7, "brows_scared": 7, "brows_determined": 6},
    }

    _POSE_ATTR_FALLBACK = {
        # Rimjob heads (Images/<Girl>/Rimjob.rpy): eyes normal / squint / surprised / side / wink / happy / closed /
        # ahegao, brows normal / angry / sad / surprised, no mouth (her mouth is on him)
        "rimjob": {
            "eyes_sexy":          "eyes_squint",
            "eyes_small":         "eyes_squint",
            "eyes_squint_big":    "eyes_squint",
            "eyes_closed_happy":  "eyes_happy",
            "eyes_bliss":         "eyes_closed",
            "eyes_ahegao_2":      "eyes_ahegao",
            "eyes_looking_left":  "eyes_side",
            "eyes_side_2":        "eyes_side",
            "eyes_side_squint":   "eyes_side",
            "eyes_scared":        "eyes_surprised",
            "brows_worried":      "brows_sad",
            "brows_scared":       "brows_sad",
            "brows_confused":     "brows_sad",
            "brows_confused_2":   "brows_sad",
            "brows_determined":   "brows_angry",
            "brows_challenging":  "brows_angry",
            "brows_up":           "brows_surprised",
            "brows_maniac":       "brows_surprised",
            "brows_horny":        "brows_normal",
        },
        "standing": {
            "brows_horny":      "brows_normal",
            "brows_up":         "brows_surprised",
            "brows_challenging":"brows_confused",
            "brows_confused_2": "brows_confused",
            "mouth_scared":     "mouth_surprised",
            "mouth_happy":      "mouth_smile",
            "mouth_angry":      "mouth_disgusted",
            "mouth_kiss":       "mouth_kissing",
            "mouth_ahegao":     "mouth_tongue",
            "mouth_open":       "mouth_open_teeth",
            "mouth_screaming":  "mouth_open_teeth",
            "eyes_looking_to_player": "eyes_normal",
            "eyes_looking_up":  "eyes_normal",
            "eyes_left_closed": "eyes_blinking_left",
            "eyes_right_closed":"eyes_blinking_right",
        },
        "handjob": {
            "eyes_sexy":        "eyes_normal",
            "eyes_looking_left":"eyes_side",
            "eyes_looking_down":"eyes_normal",
            "eyes_looking_down_2":"eyes_side_2",
            "eyes_small":       "eyes_squint",
            "eyes_side_squint": "eyes_side",
            "eyes_side_squint_2":"eyes_side_2",
            "eyes_scared":      "eyes_surprised",
            "eyes_blinking_left":"eyes_left_closed",
            "eyes_blinking_right":"eyes_right_closed",
            "eyes_closed_happy":"eyes_closed",
            "eyes_looking_to_player":"eyes_normal",
            "eyes_looking_up":  "eyes_normal",
            "brows_horny":      "brows_normal",
            "brows_maniac":     "brows_surprised",
            "brows_up":         "brows_surprised",
            "brows_challenging":"brows_confused",
            "brows_confused_2": "brows_confused",
            "mouth_lipbite":    "mouth_smile",
            "mouth_kissing":    "mouth_smile",
            "mouth_talking":    "mouth_smile",
            "mouth_scared":     "mouth_sad",
            "mouth_happy":      "mouth_smile",
            "mouth_angry":      "mouth_disgusted",
            "mouth_kiss":       "mouth_smile",
            "mouth_ahegao":     "mouth_tongue",
            "mouth_open":       "mouth_open_teeth",
            "mouth_screaming":  "mouth_open_teeth",
        },
        "blowjob": {
            "eyes_sexy":        "eyes_normal",
            "eyes_side":        "eyes_looking_left",
            "eyes_side_2":      "eyes_looking_right",
            "eyes_looking_down":"eyes_normal",
            "eyes_looking_down_2":"eyes_normal",
            "eyes_small":       "eyes_squint",
            "eyes_side_squint": "eyes_looking_left",
            "eyes_side_squint_2":"eyes_looking_right",
            "eyes_squint_big":  "eyes_squint_2",
            "eyes_surprised_2": "eyes_ahegao",
            "eyes_closed":      "eyes_closed_happy",
            "eyes_scared":      "eyes_normal",
            "eyes_looking_up":  "eyes_normal",
            "eyes_looking_to_player":"eyes_normal",
            "eyes_blinking_left":"eyes_left_closed",
            "eyes_blinking_right":"eyes_right_closed",
            "mouth_normal":     "mouth_smile",
            "mouth_laugh":      "mouth_happy",
            "mouth_kissing":    "mouth_lipbite",
            "mouth_disgusted":  "mouth_sad",
            "mouth_serious":    "mouth_angry",
            "mouth_open_teeth": "mouth_happy",
            "mouth_talking":    "mouth_smile",
            "mouth_sch":        "mouth_surprised",
            "mouth_kiss":       "mouth_lipbite",
            "mouth_ahegao":     "mouth_tongue",
            "mouth_open":       "mouth_happy",
            "mouth_screaming":  "mouth_scared",
        },
        "titjob": {
            "eyes_side":        "eyes_looking_left",
            "eyes_side_2":      "eyes_looking_right",
            "eyes_looking_down":"eyes_normal",
            "eyes_looking_down_2":"eyes_normal",
            "eyes_small":       "eyes_squint",
            "eyes_squint_2":    "eyes_squint",
            "eyes_squint_big":  "eyes_closed",
            "eyes_side_squint": "eyes_looking_left",
            "eyes_side_squint_2":"eyes_looking_right",
            "eyes_surprised":   "eyes_normal",
            "eyes_surprised_2": "eyes_normal",
            "eyes_left_closed": "eyes_blink_left",
            "eyes_right_closed":"eyes_blink_right",
            "eyes_scared":      "eyes_normal",
            "eyes_blinking_left":"eyes_blink_left",
            "eyes_blinking_right":"eyes_blink_right",
            "eyes_looking_to_player":"eyes_normal",
            "eyes_looking_up":  "eyes_normal",
            "eyes_closed_happy":"eyes_closed",
            "brows_horny":      "brows_normal",
            "brows_surprised":  "brows_confused",
            "brows_maniac":     "brows_confused_2",
            "brows_up":         "brows_confused",
            "mouth_smile":      "mouth_normal",
            "mouth_tongue":     "mouth_ahegao",
            "mouth_disgusted":  "mouth_sad",
            "mouth_serious":    "mouth_sad",
            "mouth_open_teeth": "mouth_open",
            "mouth_talking":    "mouth_normal",
            "mouth_kissing":    "mouth_kiss",
            "mouth_sch":        "mouth_surprised",
            "mouth_scared":     "mouth_sad",
            "mouth_happy":      "mouth_laugh",
            "mouth_angry":      "mouth_sad",
            "mouth_screaming":  "mouth_surprised",
        },
        "cowgirl": {
            "eyes_sexy":        "eyes_normal",
            "eyes_looking_left":"eyes_side",
            "eyes_looking_right":"eyes_side_2",
            "eyes_looking_down":"eyes_side",
            "eyes_looking_down_2":"eyes_side_2",
            "eyes_small":       "eyes_squint",
            "eyes_side_squint": "eyes_side",
            "eyes_side_squint_2":"eyes_side_2",
            "eyes_scared":      "eyes_surprised",
            "eyes_blinking_left":"eyes_left_closed",
            "eyes_blinking_right":"eyes_right_closed",
            "eyes_closed_happy":"eyes_closed",
            "eyes_looking_to_player":"eyes_normal",
            "eyes_looking_up":  "eyes_normal",
            "brows_sad":        "brows_confused",
            "brows_maniac":     "brows_surprised",
            "brows_up":         "brows_surprised",
            "brows_challenging":"brows_confused",
            "brows_confused_2": "brows_confused",
            "mouth_lipbite":    "mouth_smile",
            "mouth_sad":        "mouth_serious",
            "mouth_talking":    "mouth_smile",
            "mouth_scared":     "mouth_surprised",
            "mouth_happy":      "mouth_smile",
            "mouth_angry":      "mouth_disgusted",
            "mouth_kiss":       "mouth_kissing",
            "mouth_ahegao":     "mouth_tongue",
            "mouth_open":       "mouth_open_teeth",
            "mouth_screaming":  "mouth_open_teeth",
        },
        "reverse_cowgirl": {
            "eyes_sexy":        "eyes_normal",
            "eyes_squint_big":  "eyes_squint_2",
            "eyes_looking_left":"eyes_side",
            "eyes_looking_right":"eyes_side_2",
            "eyes_looking_down":"eyes_side",
            "eyes_looking_down_2":"eyes_side_2",
            "eyes_small":       "eyes_squint",
            "eyes_side_squint": "eyes_squint",
            "eyes_side_squint_2":"eyes_squint_2",
            "eyes_scared":      "eyes_surprised",
            "eyes_blinking_left":"eyes_left_closed",
            "eyes_blinking_right":"eyes_right_closed",
            "eyes_closed_happy":"eyes_closed",
            "brows_confused":   "brows_normal",
            "brows_maniac":     "brows_surprised",
            "brows_challenging":"brows_surprised",
            "brows_confused_2": "brows_normal",
            "mouth_laugh":      "mouth_smile",
            "mouth_sad":        "mouth_serious",
            "mouth_kissing":    "mouth_kiss",
            "mouth_talking":    "mouth_smile",
            "mouth_happy":      "mouth_smile",
            "mouth_angry":      "mouth_disgusted",
            "mouth_ahegao":     "mouth_tongue",
            "mouth_open":       "mouth_open_teeth",
            "mouth_screaming":  "mouth_open_teeth",
        },
        "doggy": {
            "eyes_sexy":        "eyes_normal",
            "eyes_squint_big":  "eyes_squint",
            "eyes_side":        "eyes_normal",
            "eyes_side_2":      "eyes_normal",
            "eyes_looking_left":"eyes_normal",
            "eyes_looking_right":"eyes_looking_to_player",
            "eyes_looking_down":"eyes_normal",
            "eyes_looking_down_2":"eyes_normal",
            "eyes_small":       "eyes_squint",
            "eyes_side_squint": "eyes_squint",
            "eyes_side_squint_2":"eyes_squint",
            "eyes_surprised_2": "eyes_surprised",
            "eyes_left_closed": "eyes_closed",
            "eyes_right_closed":"eyes_closed",
            "eyes_blinking_left":"eyes_closed",
            "eyes_blinking_right":"eyes_closed",
            "eyes_closed_happy":"eyes_closed",
            "eyes_scared":      "eyes_surprised",
            "brows_maniac":     "brows_surprised",
            "brows_up":         "brows_surprised",
            "brows_challenging":"brows_confused",
            "brows_confused_2": "brows_confused",
            "mouth_happy":      "mouth_smile",
            "mouth_kissing":    "mouth_kiss",
            "mouth_talking":    "mouth_smile",
            "mouth_angry":      "mouth_disgusted",
            "mouth_ahegao":     "mouth_tongue",
            "mouth_open":       "mouth_surprised",
            "mouth_screaming":  "mouth_surprised",
            "mouth_sch":        "mouth_surprised",
            "mouth_open_teeth": "mouth_surprised",
        },

        "laying_down": {
            "eyes_squint_big":  "eyes_squint",
            "eyes_small":       "eyes_squint",
            "eyes_side_squint": "eyes_squint",
            "eyes_side_squint_2":"eyes_squint_2",
            "eyes_scared":      "eyes_surprised",
            "eyes_looking_down":"eyes_normal",
            "eyes_looking_down_2":"eyes_side_2",
            "eyes_blinking_left":"eyes_left_closed",
            "eyes_blinking_right":"eyes_right_closed",
            "brows_up":         "brows_surprised",
            "brows_challenging":"brows_horny",
            "brows_confused_2": "brows_confused",
            "mouth_serious":    "mouth_normal",
            "mouth_disgusted":  "mouth_sad",
            "mouth_open_teeth": "mouth_moaning",
            "mouth_open":       "mouth_moaning",
            "mouth_kissing":    "mouth_kiss",
            "mouth_talking":    "mouth_smile",
            "mouth_sch":        "mouth_normal",
        },

        # Full Nelson head switches (Negasonic / Tenny FullNelson.rpy): standing names they don't know fall to
        # Normal. eyes_squint_big stays unmapped on purpose: the switch shows it as Closed.
        "full_nelson": {
            "eyes_surprised_2":   "eyes_ahegao",
            "eyes_looking_left":  "eyes_side",
            "eyes_looking_right": "eyes_side_2",
            "mouth_kissing":      "mouth_kiss",
            "mouth_disgusted":    "mouth_sad",
        },
    }

    def _apply_pose_fallback(pose, result):
        fb = _POSE_ATTR_FALLBACK.get(pose)
        if fb:
            for k in ("eyes", "brows", "mouth"):
                if k in result and result[k] in fb:
                    result[k] = fb[result[k]]

    def _detect_scene_pose(girl):
        if getattr(store, "_bj_girl", None) is girl:
            return "blowjob"
        if getattr(store, "_hj_girl", None) is girl:
            return "handjob"
        if getattr(store, "_titjob_girl", None) is girl:
            return "titjob"
        if getattr(store, "_cowgirl_girl", None) is girl or getattr(store, "_scg_girl", None) is girl:
            return "cowgirl"
        if getattr(store, "_rcg_girl", None) is girl or getattr(store, "_srcg_girl", None) is girl:
            return "reverse_cowgirl"
        if getattr(store, "_doggy_girl", None) is girl or getattr(store, "_sdg_girl", None) is girl:
            return "doggy"
        if getattr(store, "_fn_girl", None) is girl:
            return "full_nelson"
        if getattr(store, "_laying_girl", None) is girl:
            return "laying_down"
        if getattr(store, "_ft_girl", None) is girl:
            return "footjob"
        if getattr(store, "_rj_girl", None) is girl:
            return "rimjob"
        return "standing"

    def set_scene_expression(girl, expr_name, pose=None, eyes=None, brows=None, mouth=None, blush=None):
        """Universal expression setter. Replaces Face_Change and _bj_set_expression.

        expr_name: named preset ("happy", "scared", ...) or None for partial-only updates.
        Lookup: GIRL_POSE_EXPRESSIONS[gid][pose] -> POSE_EXPRESSIONS[pose] -> POSE_EXPRESSIONS["standing"]
        For BJ: translates to bj_eyes/bj_brows/bj_idle_mouth + re-shows head on mouth change.
        For sex scenes: updates sprite_state + blink-on-eye-change.
        For standing: updates sprite_state + re-shows sprite via set_girl_sprite.
        Returns the applied dict (keys present = values changed).
        """
        if getattr(store, "_phone_mode", False):
            return None

        if pose is None:
            pose = _detect_scene_pose(girl)

        if pose == "standing" and _girl_in_sex_scene(girl):
            import traceback as _tb
            _stack = "".join(_tb.format_stack())
            print("[BUG_TRACE] set_scene_expression detected pose=standing for %s while in sex scene! expr=%s\n%s" % (getattr(girl, "Id", "?"), expr_name, _stack))

        gid = getattr(girl, "Id", getattr(girl, "gid", ""))

        if expr_name is not None:
            expr = None
            if "GIRL_POSE_EXPRESSIONS" in dir(store):
                expr = GIRL_POSE_EXPRESSIONS.get(gid, {}).get(pose, {}).get(expr_name)
            if not expr:
                expr = POSE_EXPRESSIONS.get(pose, {}).get(expr_name)
            if not expr:
                expr = POSE_EXPRESSIONS.get("standing", {}).get(expr_name)
            if not expr:
                print("[EXPR] Unknown expression '%s' for %s/%s" % (expr_name, gid, pose))
                expr = {"eyes": "eyes_normal", "brows": "brows_normal", "mouth": "mouth_normal"}
            result = dict(expr)
            if hasattr(girl, "current_expression"):
                girl.current_expression = expr_name
        else:
            result = {}

        if eyes is not None:
            result["eyes"] = eyes
        if brows is not None:
            result["brows"] = brows
        if mouth is not None:
            result["mouth"] = mouth

        _apply_pose_fallback(pose, result)

        if not result and blush is None:
            return result

        if blush is not None:
            _st = sprite_state.setdefault(gid, {})
            _st["blush"] = _normalize_blush_value(blush)

        if pose == "blowjob":
            if "eyes" in result:
                _bj_e = result["eyes"].replace("eyes_", "") if result["eyes"].startswith("eyes_") else result["eyes"]
                store.bj_eyes = _bj_e
                store.bj_blink = False
            if "brows" in result:
                store.bj_brows = _BJ_BROWS_MAP.get(girl.gid, {}).get(result["brows"], 1)
            if "mouth" in result:
                _prev_mouth = getattr(store, "bj_idle_mouth", "")
                store.bj_idle_mouth = result["mouth"]
                if result["mouth"] != _prev_mouth:
                    _bj_variant = _bj_head_variant(gid)
                    if getattr(store, "bj_action", "") == "suck" and getattr(store, "bj_speed", 0) >= 1:
                        pass
                    elif _bj_variant == "head_base" and _gsc(gid, 'has_head_normal', False, pose='blowjob'):
                        # her working head has the mouth cut out and her jaw art is the open mouth: a face mouth
                        # on it = two mouths. Stored only: the next rest / line (head_normal) shows it.
                        print("[EXPR] %s (blowjob): mouth %s stored, not drawn on the cut-out working head" % (gid, result["mouth"]))
                    else:
                        _pov_bj = _gsc(gid, 'pov_overlay', False, pose='blowjob')
                        _bj_head_z = 10035 if _pov_bj else 10015
                        _bj_head_at = [bj_get_head_transform(0)] if _pov_bj else []
                        renpy.show(
                            "%s blowjob_head %s %s" % (girl.gid, _bj_variant, result["mouth"]),
                            tag="%s_bj_head" % girl.gid,
                            at_list=_bj_head_at,
                            zorder=_bj_head_z
                        )
            print("[EXPR] %s -> %s (blowjob): e=%s b=%s m=%s" % (gid, expr_name, result.get("eyes",""), result.get("brows",""), result.get("mouth","")))

        elif _girl_in_sex_scene(girl):
            state = sprite_state.setdefault(gid, {})
            _prev_eyes = state.get("eyes")
            for key in ("eyes", "brows", "mouth"):
                if key in result:
                    state[key] = result[key]
            _eyes_changed = "eyes" in result and result["eyes"] != _prev_eyes

            # Blink animation on eye change
            if _eyes_changed:
                if getattr(store, "_hj_girl", None) is girl:
                    store.hj_blink = True
                    renpy.restart_interaction()
                    import time
                    time.sleep(0.10)
                    store.hj_blink = False
                elif getattr(store, "_bj_girl", None) is girl:
                    store.bj_blink = True
                    renpy.restart_interaction()
                    import time
                    time.sleep(0.10)
                    store.bj_blink = False

            if _eyes_changed and getattr(store, "_laying_girl", None) is girl:
                try:
                    _tgt = state.get("eyes", "eyes_normal")
                    state["eyes"] = "eyes_closed"
                    _ld_refresh_expression(girl, state)
                    renpy.pause(0.12)
                    state["eyes"] = _tgt
                    _ld_refresh_expression(girl, state)
                except RENPY_FLOW_EXCEPTIONS:
                    raise   # rollback / load / quit are exceptions in Ren'Py: never swallow them
                except:
                    pass

            if _eyes_changed and getattr(store, "_rcg_girl", None) is girl and getattr(store, "_doggy_girl", None) is not girl and getattr(store, "_cowgirl_girl", None) is not girl:
                _cs_girls = getattr(store, "_RCG_CS_GIRLS", set())
                if gid in _cs_girls:
                    store.rcg_blink = True
                    renpy.restart_interaction()
                    renpy.pause(0.12)
                    store.rcg_blink = False
                    renpy.restart_interaction()
                else:
                    try:
                        _tgt = state.get("eyes", "eyes_normal")
                        state["eyes"] = "eyes_closed"
                        _attrs = _build_rcg_attributes(girl)
                        _img = "%s rcg" % gid
                        if _attrs:
                            _img += " " + " ".join(_attrs)
                        renpy.show(_img, tag=gid, zorder=9980)
                        renpy.restart_interaction()
                        renpy.pause(0.12)
                        state["eyes"] = _tgt
                        _attrs = _build_rcg_attributes(girl)
                        _img = "%s rcg" % gid
                        if _attrs:
                            _img += " " + " ".join(_attrs)
                        renpy.show(_img, tag=gid, zorder=9980)
                    except RENPY_FLOW_EXCEPTIONS:
                        raise   # rollback / load / quit are exceptions in Ren'Py: never swallow them
                    except:
                        pass

            # HJ/TJ/CG use static attributes — must re-show after ANY change
            if getattr(store, "_hj_girl", None) is girl:
                _hj_update_attrs(girl)
                _hj_show_sprite(girl)
            elif getattr(store, "_titjob_girl", None) is girl:
                _tj_attrs = _build_titjob_attributes(girl)
                _tj_img = "%s titjob" % gid
                if _tj_attrs:
                    _tj_img += " " + " ".join(_tj_attrs)
                _tj_spd = getattr(store, "titjob_speed", 0)
                _tj_tf = titjob_get_slot_transform(_tj_spd)
                _tj_boobs_tf = titjob_get_boobs_transform(_tj_spd)
                _tj_nipples_tf = titjob_get_nipples_transform(_tj_spd)
                _tj_boobs_at = [_tj_tf, _tj_boobs_tf]
                renpy.show(_tj_img, tag=gid, at_list=[_tj_tf], zorder=9980)
                renpy.show("%s titjob_boobs" % gid, tag="titjob_boobs", at_list=_tj_boobs_at, zorder=9982)
                renpy.show("%s titjob_nipples" % gid, tag="titjob_nipples", at_list=[_tj_tf, _tj_nipples_tf], zorder=9983)
                renpy.show("%s titjob_boobs_cum" % gid, tag="titjob_boobs_cum", at_list=_tj_boobs_at, zorder=9986)
                _tj_chest = girl.Chest
                if _tj_chest and _tj_chest != "corset":
                    _tj_top_img = "%s tj_%s" % (gid, _tj_chest)
                    _tj_top_up_img = "%s tj_%s_up" % (gid, _tj_chest)
                    if not girl.ChestUp and renpy.has_image(_tj_top_img):
                        renpy.show(_tj_top_img, tag="titjob_chest_top", at_list=_tj_boobs_at, zorder=9984)
                    elif girl.ChestUp and renpy.has_image(_tj_top_up_img):
                        renpy.show(_tj_top_up_img, tag="titjob_chest_top", at_list=_tj_boobs_at, zorder=9984)
                _tj_arms3 = "%s tj_arms3_hands" % gid
                if store.titjob_arms_pose == 3 and renpy.has_image(_tj_arms3):
                    renpy.show(_tj_arms3, tag="titjob_arms3_hands", at_list=[_tj_tf], zorder=10060)
                if store.titjob_grab:
                    _hand_disabled = getattr(store, "_player_hand_disabled", None)
                    _slap_hide = getattr(store, "_slap_hide_hand", None)
                    for _side in ("left", "right"):
                        _gb_img = "%s tj_grab_boobs_%s" % (gid, _side)
                        _gb_tag = "titjob_grab_%s" % _side
                        if _hand_disabled != _side and _slap_hide != _side and renpy.has_image(_gb_img):
                            renpy.show(_gb_img, tag=_gb_tag, at_list=_tj_boobs_at, zorder=10070)
            elif getattr(store, "_laying_girl", None) is girl:
                _ld_refresh_expression(girl, state)
            elif getattr(store, "_cowgirl_girl", None) is girl:
                _cg_attrs = _build_cowgirl_attributes(girl)
                if getattr(store, "hiding_face", False):
                    _hr = []
                    for _a in _cg_attrs:
                        if _a.startswith("eyes_"):
                            _hr.append("eyes_closed")
                        elif _a.startswith("arms_high_") and _a != "arms_high_none":
                            _hr.append("arms_high_none")
                        elif _a.startswith("arms_low_") and _a != "arms_low_none":
                            _hr.append("arms_low_none")
                        elif _a == "shoulder_left_on":
                            _hr.append("shoulder_left_none")
                        elif _a.startswith("masturbate_"):
                            _hr.append("masturbate_hand_none")
                        else:
                            _hr.append(_a)
                    _cg_attrs = _hr
                _cg_img = "%s cowgirl" % gid
                if _cg_attrs:
                    _cg_img += " " + " ".join(_cg_attrs)
                _cg_tf = cowgirl_slot_static if store._cg_force_static else cowgirl_slot_synced
                renpy.show(_cg_img, tag=gid, at_list=[_cg_tf], zorder=9980)

            renpy.restart_interaction()
            print("[EXPR] %s -> %s (%s): e=%s b=%s m=%s" % (gid, expr_name, pose, result.get("eyes",""), result.get("brows",""), result.get("mouth","")))

        else:
            _show = dict(result)
            if pose == "standing" and _show.get("eyes") == "eyes_closed":
                _show.pop("eyes")
            set_girl_sprite(girl, pose=pose, **_show)
            print("[EXPR] %s -> %s (%s): e=%s b=%s m=%s" % (gid, expr_name, pose, result.get("eyes",""), result.get("brows",""), result.get("mouth","")))

        return result

    def get_expression(expr_name, pose="standing", gid=None):
        """Lookup-only: returns {eyes, brows, mouth} without applying. For building pools or menus."""
        expr = None
        if gid and "GIRL_POSE_EXPRESSIONS" in dir(store):
            expr = GIRL_POSE_EXPRESSIONS.get(gid, {}).get(pose, {}).get(expr_name)
        if not expr:
            expr = POSE_EXPRESSIONS.get(pose, {}).get(expr_name)
        if not expr:
            expr = POSE_EXPRESSIONS.get("standing", {}).get(expr_name)
        return dict(expr) if expr else {"eyes": "eyes_normal", "brows": "brows_normal", "mouth": "mouth_normal"}

# --- Cum shake pair (called from all CumAnim/CumOutsideFreeze labels) ---

label _cum_punch_pair(shake_type="oral"):
    if shake_type == "oral":
        $ renpy.pause(0.50)
        show layer master at bj_slap_shake
        $ renpy.pause(0.20)
        show layer master
        $ renpy.pause(0.50)
        show layer master at bj_slap_shake
        $ renpy.pause(0.20)
        show layer master
    else:
        $ renpy.pause(0.35)
        show layer master at dg_cum_shake
        $ renpy.pause(0.15)
        show layer master
        $ renpy.pause(0.35)
        show layer master at dg_cum_shake
        $ renpy.pause(0.15)
        show layer master
    return

# --- Generic show/apply/hide ---

label Girl_Hide(Girl, hide_base=True):

    $ k = girl_key(Girl)

    python:
        for suf in [" standing", " sprite", " handjob", " blowjob", " sex"]:
            renpy.hide(k + suf)

        if hide_base:
            renpy.hide(k)

    return
