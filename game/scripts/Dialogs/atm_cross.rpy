## atm_cross.rpy -- CROSS-GIRL ATM LINES (engine). Data lives in atm_cross_lines.rpy.
##
## Threesome: the player had anal with girl A, switched to girl B and asked B for a blowjob. It was in
## A's ass, not in B's, so every "my ass" pool of the same-girl ATM flow is wrong for B. This layer
## answers those moments in B's own style and by her traits, naming A through %(src)s.
##
##   _ATM_CROSS_LINES[gid or "_default"]["<moment>.<trait or _default>"] = [lines]
##   moments: ask_ok, ask_no (sex_menu), react (first taste, Core_Blowjob), moan (scene_pick_line),
##            entry (about to cum in her mouth), swallow_ok, swallow_no, after_swallow (Cum.rpy)
##   "<moment>.<trait>" + a _ATM_CROSS_HISTORY_SUFFIX suffix: lines added only when her own ATM history makes them true
##
## Cross is decided by store._atm_source_gid (every same-girl ATM entry point sets it to her own gid;
## only the sex_menu threesome path leaves another girl's gid there).

init python:

    # Her most telling trait wins: what disgusts her first, then what she enjoys
    _ATM_CROSS_TRAIT_PRIORITY = ("lesbian", "hate_cum", "anal_hater", "cum_slut", "anal_lover", "femdom", "submissive",
                                 "hardcore_sex", "cute_sex")
    # scene_pick_line() base key -> moment (blowjob scene only)
    _ATM_CROSS_KEY_MOMENT = {
        "moan.speed1": "moan",
        "moan.speed2": "moan",
        "moan.speed3": "moan",
        "atm_react": "react",
    }
    # Share (%) of those picks this layer takes over; the rest keep the regular (threesome...) pools
    _ATM_CROSS_MOMENT_CHANCE = {"moan": 50}
    # Pool suffix -> the ATM history it needs: True = she had an ATM of her own BEFORE this one ("I know that
    # taste"), False = she never had one ("I've never done anything like this"). "<moment>.<trait><suffix>" lines
    # join "<moment>.<trait>" only when that is true; the plain key keeps a line for both cases.
    _ATM_CROSS_HISTORY_SUFFIX = {".atm": True, ".first_atm": False}
    _atm_cross_last = {}   # gid -> last line, to avoid back-to-back repeats (not saved)

    def atm_cross_source(girl):
        """The OTHER girl whose ass it was just in, or None when this is not a cross-girl ATM."""
        _src = getattr(store, "_atm_source_gid", None)
        if girl is None or _src is None or _src == getattr(girl, "gid", None):
            return None
        return GIRL_BY_ID.get(_src)

    def atm_cross_line(girl, moment):
        """Translated line for this moment in HER style and by HER traits, or None (not cross / no pool)."""
        _src = atm_cross_source(girl)
        if _src is None:
            return None
        _all = globals().get("_ATM_CROSS_LINES", {})
        # an eager trait she is still discovering speaks only through its discovery keys (trait_line_keys): the
        # veteran pools here ("I never waste cum") are not her yet, so the next trait / _default answers
        _traits = [_k for _t in _ATM_CROSS_TRAIT_PRIORITY if girl.has_trait(_t) for _k in trait_line_keys(girl, _t)] + ["_default"]
        # ATMs of hers BEFORE this one: atm_register counts this one at her yes and marks the scene, so the mark
        # takes it back out (same rule as trait_is_first). It picks the history suffixes that are true for her.
        _atm_n = getattr(girl, "_atm_count", 0)
        _had_atm = _atm_n - (1 if _scene_act_marked(girl, "atm") else 0) > 0
        _sfx = [_s for _s, _needs in _ATM_CROSS_HISTORY_SUFFIX.items() if _needs == _had_atm]
        _pool, _found = None, None
        for _style in (girl.gid, "_default"):          # her own style first, whatever the trait
            _pools = _all.get(_style, {})
            for _t in _traits:
                _key = "%s.%s" % (moment, _t)
                # lines true whatever she did before + the ones her history makes true; none: the next trait answers
                _pool = list(_pools.get(_key, [])) + [_l for _s in _sfx for _l in _pools.get(_key + _s, [])]
                if _pool:
                    _found = _style + "/" + _key + "".join("+" + _s for _s in _sfx if _key + _s in _pools)
                    break
            if _pool:
                break
        if not _pool:
            print("[ATM_CROSS] %s: no pool for moment=%s traits=%s" % (girl.gid, moment, _traits))
            return None
        _last = _atm_cross_last.get(girl.gid)
        _line = renpy.random.choice([_l for _l in _pool if _l != _last] or list(_pool))
        _atm_cross_last[girl.gid] = _line
        print("[ATM_CROSS] %s <- %s: %s (atm_count=%d, had one before this=%s)" % (girl.gid, _src.gid, _found, _atm_n, _had_atm))
        # the matched trait pool spoke: live ATM commentary names her taste (she is doing it).
        # A refusal moment (ask_no / swallow_no) only reveals identity or control, never a preference.
        _dt = _t
        if _dt.endswith("_first"):
            _dt = _dt[:-6]
        elif _dt.endswith("_new"):
            _dt = _dt[:-4]
        if _dt != "_default":
            if moment in ("ask_no", "swallow_no") and _dt not in ("lesbian", "femdom", "submissive"):
                _dt = None
            if _dt and girl.has_trait(_dt) and hasattr(girl, "discover"):
                girl.discover("discovered_trait_%s" % _dt)
        return _tl(_line) % {"src": _src.Name}

    def atm_cross_override(girl, moment, fallback):
        """For the flows that pick from inline same-girl pools: the cross line when it applies, else `fallback`."""
        return atm_cross_line(girl, moment) or fallback

    def atm_cross_scene_line(key, scene, girl):
        """Hook for scene_pick_line(): a cross-girl line for this blowjob moment, or None."""
        if scene != "bj" or not getattr(store, "_atm_cum_in_mouth", False):
            return None
        _moment = _ATM_CROSS_KEY_MOMENT.get(key)
        if not _moment or atm_cross_source(girl) is None:
            return None
        if renpy.random.randint(1, 100) > _ATM_CROSS_MOMENT_CHANCE.get(_moment, 100):
            return None
        return atm_cross_line(girl, _moment)
