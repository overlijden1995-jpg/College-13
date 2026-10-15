# ============================================================
# TRUTH OR DARE - DARE system
# Dare acceptance, strip penalty, dare menus, dare labels
# ============================================================

transform _tod_suck_lean:
    xalign 0.60
    yalign 2.0
    ease 0.5 yoffset 80
    block:
        ease 0.8 yoffset 70
        ease 0.8 yoffset 80
        repeat

init python:

    # ── Dare acceptance logic ──────────────────────────────

    def tod_girl_accepts_dare(girl, dare_difficulty):
        """Decide whether a girl accepts a dare.
        dare_difficulty is 1-10.
        If refusing would expose chest or panties, she's more likely to accept."""
        inbt = getattr(girl, "Inbt", 0)
        obed = getattr(girl, "Obed", 0)
        alc = tod_effective_alc(girl)   # bonus caps at the sweet-spot top

        # Base acceptance from Inbt (40%), Obed (30%), alcohol (6% per level) + 15% base
        acceptance = (inbt / 1000.0) * 0.4 + (obed / 1000.0) * 0.3 + alc * 0.06 + 0.15

        # Difficulty penalty
        acceptance -= dare_difficulty * 0.08

        # Harem night: girlfriends are comfortable with each other
        if getattr(store, "_hangout_is_harem_night", False):
            acceptance += 0.20

        # Trait modifiers
        if hasattr(girl, "has_trait"):
            if girl.has_trait("hardcore_sex"):
                acceptance += 0.15
            if girl.has_trait("cute_sex"):
                acceptance -= 0.10

        # Strip pressure: if refusing would expose chest/panties, prefer the dare
        strip_lvl = _tod_girl_strip_level(girl)
        if strip_lvl == 2:
            acceptance += 0.20  # rather do the dare than show boobs
        elif strip_lvl == 3:
            acceptance += 0.30  # really doesn't want to show everything
        elif strip_lvl >= 4:
            acceptance += 0.10  # already naked, less pressure either way

        # GF-awareness: target girl hesitates when player's GF is watching
        _gf_acc = _hangout_find_gf()
        if _gf_acc is not None and _gf_acc.gid != girl.gid:
            if not (hasattr(girl, "has_trait") and girl.has_trait("cheater")):
                _target_like_gf = girl.get_like_for(_gf_acc.gid)
                _gf_overruled = getattr(store, "_tod_gf_was_overruled", False)
                if _target_like_gf >= 750:
                    acceptance -= 0.30 if _gf_overruled else 0.15
                elif _target_like_gf >= 500:
                    acceptance -= 0.20 if _gf_overruled else 0.10
                elif _target_like_gf >= 250:
                    acceptance -= 0.05

        # BF-awareness: girl hesitates when her boyfriend is present and uncomfortable
        _h_npc_acc = getattr(store, "_h_npc", None)
        if _h_npc_acc and _npc_is_active() and _bf_is_gf(_h_npc_acc, girl):
            _npc_overruled = getattr(store, "_tod_npc_was_overruled", False)
            _npc_uneasy = getattr(store, "_tod_npc_was_uneasy", False)
            _loyalty = getattr(girl, "bf_loyalty", 500)

            if hasattr(girl, "has_trait") and girl.has_trait("cheater"):
                pass
            elif _npc_overruled:
                if _loyalty >= 700:
                    acceptance -= 0.25
                elif _loyalty >= 400:
                    acceptance -= 0.15
                else:
                    acceptance -= 0.05
            elif _npc_uneasy:
                if _loyalty >= 700:
                    acceptance -= 0.10
                elif _loyalty >= 400:
                    acceptance -= 0.05

        # Clamp
        acceptance = max(0.05, min(0.95, acceptance))
        return renpy.random.random() < acceptance

    # ── Sexuality gate for girl-girl dares ───────────────────

    GIRL_GIRL_DARES = {"kiss_girl", "suck_boobs", "spank_other"}

    def _tod_sexuality_blocks_dare(girl, dare_key):
        """Check if a girl's sexuality blocks a girl-girl dare.
        Returns True if she REFUSES (drinks double instead).
        Hetero firm (spectrum <26): refuses unless very drunk (6+).
        Party bi (26-40): refuses unless drunk (3+).
        Curious+ (41+): always accepts."""
        if dare_key not in GIRL_GIRL_DARES:
            return False
        spec = _effective_spectrum(girl)
        if spec >= 41:
            return False
        drunk = get_drunk(girl) if callable(globals().get("get_drunk")) else 0
        if spec >= 26:
            return drunk < 3
        return drunk < 6

    # ── Strip penalty for dare refusal ─────────────────────

    def tod_dare_strip_penalty(girl):
        """Advance the strip level for a girl who refuses a dare.
        Strips in order: Over -> Legs -> Chest -> Panties.
        Skips slots that are already empty.
        Returns (new_level, exposed_type, removed_name)."""
        key = "_hangout_strip_level_" + girl.gid
        level = getattr(store, key, 0)
        exposed = None
        removed_name = _tl(_("something"))

        # Try each slot in strict order, skip if already None
        if level <= 0 and getattr(girl, "Over", None) is not None:
            girl.Over = None
            girl.OverUp = False
            level = 1
            removed_name = _tl(_("jacket"))
        elif level <= 1 and getattr(girl, "Legs", None) is not None:
            girl.Legs = None
            girl.LegsDown = False
            level = 2
            removed_name = _tl(_("pants"))
        elif level <= 2 and getattr(girl, "Chest", None) is not None:
            girl.Chest = None
            girl.ChestUp = False
            level = 3
            exposed = "chest"
            removed_name = _tl(_("top"))
            girl.RegisterAction("player_saw_boobs")
        elif level <= 3 and getattr(girl, "Panties", None) is not None:
            girl.Panties = None
            girl.PantiesDown = False
            level = 4
            exposed = "panties"
            removed_name = _tl(_("panties"))
            girl.RegisterAction("player_saw_pussy")
        else:
            # Nothing left to remove, or all slots already None
            # Try to find anything still on
            if getattr(girl, "Over", None) is not None:
                girl.Over = None
                girl.OverUp = False
                removed_name = _tl(_("jacket"))
            elif getattr(girl, "Legs", None) is not None:
                girl.Legs = None
                girl.LegsDown = False
                removed_name = _tl(_("pants"))
            elif getattr(girl, "Chest", None) is not None:
                girl.Chest = None
                girl.ChestUp = False
                exposed = "chest"
                removed_name = _tl(_("top"))
                girl.RegisterAction("player_saw_boobs")
            elif getattr(girl, "Panties", None) is not None:
                girl.Panties = None
                girl.PantiesDown = False
                exposed = "panties"
                removed_name = _tl(_("panties"))
                girl.RegisterAction("player_saw_pussy")
            level = 4

        setattr(store, key, level)

        if exposed:
            for _w in _tod_other_girls(girl):
                if exposed == "chest":
                    set_scene_expression(_w, "surprised", blush=1)
                elif exposed == "panties":
                    set_scene_expression(_w, "surprised", blush=2)

        # Refresh sprite at static position (no slide-in animation)
        at_tf = Transform(xalign=_hangout_xalign_for(girl), yalign=2.0)
        set_girl_sprite(girl.gid, pose="standing", at_list=[at_tf])

        return (level, exposed, removed_name)

    # ── Harem night dialogue pools ────────────────────────
    _HAREM_GF_TEASE_LINES = [
        _("Don't hold back on my account~"),
        _("Ooh, lucky her. I'm next though, right?"),
        _("I'm watching every second of this. For research."),
        _("Jealous? Maybe. Turned on? Definitely."),
        _("Go ahead, babe. Just remember who's waiting at home."),
        _("She's blushing way more than I did~"),
        _("I dare you to do it better than you did with me."),
        _("This is way more fun when I'm not the one being embarrassed."),
    ]

    _HAREM_REFUSAL_TEASE_LINES = [
        _("I would have done it~"),
        _("Coward! I'll show you how it's done next round."),
        _("More drinks, less clothes... I like where this is going."),
        _("Seriously? That was an easy one!"),
    ]

    # ── Dare registries ────────────────────────────────────
    # (menu_label, dare_key, difficulty, needs_other)

    TOD_SAFE_DARES = [
        (_("Make a silly face"),       "silly_face",     1, False),
        (_("Sing a random song"),      "sing_song",      2, False),
        (_("Show your Flashgram page"),"show_flashgram", 2, False),
        (_("Do a chicken impression"), "chicken",        2, False),
        (_("Dance for us"),            "dance",          3, False),
    ]

    TOD_LEWD_DARES = [
        (_("Sit on {0}'s lap"),                    "sit_lap_player",     3, False),
        (_("Flash your boobs"),                    "flash_boobs",        3, False),
        (_("Take all your clothes off"),           "strip_all",          5, False),
        ("Kiss {0}",                            "kiss_player",        4, False),
        ("Kiss {other}",                        "kiss_girl",          5, True),
        ("Suck {other}'s boobs",                "suck_boobs",         6, True),
        (_("Let {0} slap your ass"),               "spank_player",       5, False),
        (_("Let {0} kiss your boobs"),             "kiss_boobs_player",  5, False),
        ("Slap {other}'s ass",                  "spank_other",        4, True),
        ("Give {0} a blowjob",                  "bj_player",          8, False),
        ("Give {0} a titjob",                   "tj_player",          7, False),
    ]

    # ── Cheat path / loyalty integration ──────────────────
    # Lewd dares done WITH the player map to the same act keys the 1:1 flow uses
    # (is_loyalty_blocked / mark_intimacy / sex_accept_with_temptation). Exposure dares
    # (flash, strip) and girl-girl dares are not cheating acts for the loyalty gate.
    TOD_DARE_CHEAT_ACT = {
        "sit_lap_player": "touch", "kiss_player": "kiss", "spank_player": "touch",
        "kiss_boobs_player": "touch", "bj_player": "bj", "tj_player": "tj",
    }
    # Player dares: key -> (act, who is the target: "her" = asker, "other" = the other girl)
    TOD_PDARE_CHEAT_ACT = {
        "p_lap_her": ("touch", "her"), "p_lap_other": ("touch", "other"),
        "p_kiss_her": ("kiss", "her"), "p_kiss_other": ("kiss", "other"),
        "p_spank_her": ("touch", "her"), "p_spank_other": ("touch", "other"),
        "p_kiss_boobs_her": ("touch", "her"), "p_kiss_boobs_other": ("touch", "other"),
    }
    # bf_loyalty lost when a girl with a partner does the act in a dare
    TOD_BF_LOYALTY_LOSS = {"touch": 3, "kiss": 5, "tj": 10, "bj": 15}

    def tod_loyalty_blocks_dare(girl, act):
        """Same loyalty gate as the 1:1 flow for a girl with a partner
        (temptation, drunk bonus, cheat heat, CheatMaxTier bypass, cheater trait).
        Returns the block reason, or None when she would go along with it."""
        if girl is None or not act:
            return None
        if not (hasattr(girl, "has_npc_partner") and girl.has_npc_partner()):
            return None
        if hasattr(girl, "has_trait") and girl.has_trait("lesbian"):
            return None
        blocked, reason = is_loyalty_blocked(girl, act)
        print("[TOD-LOYALTY] %s act=%s blocked=%s reason=%s" % (girl.gid, act, blocked, reason))
        return reason if blocked else None

    def tod_loyalty_blocks_player_dare(key, asker, other_girl):
        info = TOD_PDARE_CHEAT_ACT.get(key)
        if not info:
            return False
        target = asker if info[1] == "her" else other_girl
        return tod_loyalty_blocks_dare(target, info[0]) is not None

    def tod_register_cheat_act(girl, act):
        """After a lewd dare with the player: record it exactly like a 1:1 scene would, so the
        cheat path, intimacy gaps and financial gaps stay consistent with what happened."""
        mark_intimacy(girl, act)
        sex_accept_with_temptation(girl, act)
        if callable(globals().get("_is_on_cheat_path", None)) and _is_on_cheat_path(girl):
            _notify_cheat_heat(girl, "scene_%s" % act)
        if hasattr(girl, "has_npc_partner") and girl.has_npc_partner() and hasattr(girl, "change_bf_loyalty"):
            _loss = TOD_BF_LOYALTY_LOSS.get(act, 0)
            if _loss:
                girl.change_bf_loyalty(-_loss)
        print("[TOD-REGISTER] %s act=%s flags=%s stage=%s heat=%s bf_loyalty=%s" % (
            girl.gid, act, sorted(getattr(girl, "intimacy_flags", set())), getattr(girl, "_cheat_sex_stage", 0),
            getattr(girl, "_cheat_heat", 0), getattr(girl, "bf_loyalty", None)))

    # The forms _tod_format_dare_label rewrites to "my" / "me" BEFORE the lookup (the player asks, or the asking girl
    # is the {other}): never extracted from the labels, so they are listed here for the translation generator.
    _TOD_DARE_REWRITTEN_FORMS = (
        _("Sit on my lap"),
        _("Let me sit on your lap"),
        _("Let me slap your ass"),
        _("Let me kiss your boobs"),
    )

    def _tod_format_dare_label(label, other_girl=None, player_is_asker=False, translate=False, asker_girl=None):
        """Format a dare label by replacing placeholders with names.
        {0} = player, {other} = other girl, {asker} = asking girl.
        translate=True: translate template, then substitute names.
        translate=False: format English only, no translation.
        asker_girl: when girl asker IS the {other}, replace with me/my."""
        _pname = getattr(store.Player, "Name", "you")
        _self_ref = (asker_girl and other_girl and hasattr(asker_girl, 'gid')
                     and hasattr(other_girl, 'gid') and asker_girl.gid == other_girl.gid)
        if _self_ref:
            label = label.replace("{other}'s", "my").replace("{other}", "me")
        # the player asks: {0} is "my" / "me" BEFORE the lookup, whatever else the label holds (the rewritten form is
        # what gets translated, _TOD_DARE_REWRITTEN_FORMS). After it, an English word would land in a translated text
        if player_is_asker:
            label = label.replace("{0}'s", "my").replace("{0}", "me")
        txt = _tl(label) if translate else label
        if not player_is_asker:
            txt = txt.replace("{0}'s", _pname + "'s").replace("{0}", _pname)
        if other_girl and not _self_ref:
            txt = txt.replace("{other}'s", other_girl.Name + "'s").replace("{other}", other_girl.Name)
            txt = txt.replace("{asker}'s", other_girl.Name + "'s").replace("{asker}", other_girl.Name)
        return txt

    def _tod_filter_lewd_dares(girl):
        """Filter lewd dares based on the target girl's clothing state.
        - flash_boobs: hidden if chest already removed (Over+Chest gone)
        - strip_all: disabled (grayed) if already fully naked
        - kiss_boobs_player: hidden if chest already gone
        - suck_boobs: hidden if target chest already gone
        Returns (available, disabled) where each is list of (label, key, diff, needs_other)."""
        strip_lvl = _tod_girl_strip_level(girl)
        chest_gone = getattr(girl, "Chest", None) is None and getattr(girl, "Over", None) is None
        fully_naked = strip_lvl >= 4
        _has_other = _tod_other_girl(girl) is not None   # False in a 1-girl (girl+partner) hangout

        available = []
        disabled = []
        for entry in TOD_LEWD_DARES:
            _dl, _dk, _dd, _dno = entry
            if _dno and not _has_other:
                continue  # needs a second girl; not available with just one
            if _dk == "flash_boobs" and chest_gone:
                continue  # skip entirely, already showing
            if _dk == "strip_all" and fully_naked:
                disabled.append(entry)  # gray out
                continue
            available.append(entry)
        return (available, disabled)

    def _tod_lewd_chance(girl_or_alc, inbt=None):
        """Calculate lewd chance for a girl based on alcohol OR Inbt.
        Either one alone can push lewd chance high.
        Alcohol alone: alc 3 = 29%, alc 5 = 45%, alc 7 = 61%
        Inbt alone: 300 = 16%, 500 = 23%, 800 = 33%
        Both together cap fast.
        Base is 5% so first rounds without drinks stay safe.
        A femdom girl runs the game a little bolder: + TOD_FEMDOM_LEWD_BONUS x femdom_intensity."""
        _girl = None
        if inbt is None:
            _girl = girl_or_alc
            alc = tod_effective_alc(girl_or_alc)
            inbt = getattr(girl_or_alc, "Inbt", 0)
        else:
            alc = tod_effective_alc_val(girl_or_alc)
        # Each factor independently pushes toward lewd
        alc_factor = alc * 0.08    # 0-80%
        inbt_factor = (inbt / 1000.0) * 0.35  # 0-35%
        # Use the HIGHER of the two as base, plus a bonus from the other
        main = max(alc_factor, inbt_factor)
        bonus = min(alc_factor, inbt_factor) * 0.5
        chance = 0.05 + main + bonus
        if getattr(store, "_hangout_is_harem_night", False):
            chance += 0.15
        _fd = femdom_intensity(_girl) if hasattr(_girl, "has_trait") else 0.0
        if _fd:
            chance += TOD_FEMDOM_LEWD_BONUS * _fd
            print("[FEMDOM] %s: ToD lewd chance +%.3f (intensity %.1f)" % (_girl.gid, TOD_FEMDOM_LEWD_BONUS * _fd, _fd))
        return max(0.05, min(0.95, chance))

    # ── No-repeat tracking ─────────────────────────────────

    def tod_mark_used(key):
        """Mark a question or dare key as used this session."""
        used = getattr(store, "_tod_used_keys", set())
        used.add(key)
        store._tod_used_keys = used

    def tod_is_used(key):
        """Check if a question/dare was already used this session."""
        used = getattr(store, "_tod_used_keys", set())
        return key in used

    def tod_filter_unused(items, key_index=1):
        """Filter a list of tuples, removing items whose key (at key_index) was already used."""
        return [item for item in items if not tod_is_used(item[key_index])]

    # ── Escalation gates ─────────────────────────────────────
    # Minimum max_difficulty required before a dare can be auto-picked.
    # Prevents heavy dares from appearing before lighter ones are done.
    TOD_DARE_MIN_ESCALATION = {
        # --- Girl dares ---
        "sit_lap_player":     0,
        "flash_boobs":        2,
        "kiss_player":        0,
        "spank_other":        2,
        "kiss_girl":          3,
        "strip_all":          3,
        "spank_player":       3,
        "kiss_boobs_player":  4,
        "suck_boobs":         5,
        "tj_player":          6,
        "bj_player":          6,
        # --- Player dares ---
        "p_lap_her":          0,
        "p_lap_other":        0,
        "p_kiss_her":         0,
        "p_kiss_other":       3,
        "p_spank_her":        3,
        "p_spank_other":      3,
        "p_kiss_boobs_her":   4,
        "p_kiss_boobs_other": 4,
    }

    def _tod_filter_by_escalation(pool, key_index=1):
        """Remove dares whose min_escalation > current max difficulty."""
        cur = tod_get_max_difficulty()
        return [d for d in pool if TOD_DARE_MIN_ESCALATION.get(d[key_index], 0) <= cur]

    def _tod_other_girls(girl):
        """Return all hangout girls who are NOT the given girl."""
        return [g for g in _hangout_girls_list() if g.gid != girl.gid]

    def _tod_other_girl(girl):
        """Backward-compat: return ONE other girl (first in list), or None."""
        others = _tod_other_girls(girl)
        return others[0] if others else None

    # ── Escalation tracking ──────────────────────────────────

    def tod_get_max_difficulty():
        """Get the highest difficulty dare/question that has been done this session."""
        return getattr(store, "_tod_max_difficulty", 0)

    def tod_update_max_difficulty(diff):
        """Update the max difficulty tracker."""
        cur = getattr(store, "_tod_max_difficulty", 0)
        store._tod_max_difficulty = max(cur, int(diff))

    def _tod_pick_weighted_by_difficulty(pool, alc, inbt, min_diff=0):
        """Within a lewd pool, higher drunk/Inbt = prefer harder dares.
        Weights each dare by difficulty * boldness_factor.
        Items below min_diff are penalized (much less likely)."""
        boldness = 0.5 + (alc * 0.05) + (inbt / 1000.0) * 0.3
        weights = []
        for entry in pool:
            diff = entry[2]  # difficulty
            w = diff * boldness
            if diff < min_diff:
                w *= 0.3  # much less likely to go backwards
            weights.append(w)
        total = sum(weights)
        if total <= 0:
            return renpy.random.choice(pool)
        r = renpy.random.random() * total
        cumulative = 0
        for i, w in enumerate(weights):
            cumulative += w
            if r <= cumulative:
                return pool[i]
        return pool[-1]

    def tod_auto_pick_dare(girl, target, other_girl):
        """AI girl picks a dare for the target.
        girl = asker (determines lewd_chance, difficulty preference).
        target = who receives the dare (determines clothing filter).
        Filters out unavailable dares based on clothing.
        Also filters dares the GF would block (so she doesn't propose then deny).
        Higher drunk/Inbt = more lewd and harder dares."""
        alc = hangout_get_alcohol(girl)
        inbt = getattr(girl, "Inbt", 0)
        lewd_chance = _tod_lewd_chance(girl)
        _min_d = tod_get_max_difficulty()

        if renpy.random.random() < lewd_chance:
            available, _discard_disabled = _tod_filter_lewd_dares(target)
            available = tod_filter_unused(available)
            available = _tod_filter_by_escalation(available)
            available = tod_gf_filter_dares(available)  # Don't propose what GF would block
            if available:
                pick = _tod_pick_weighted_by_difficulty(available, alc, inbt, min_diff=_min_d)
                return (pick[1], pick[2], pick[3])
        # Fallback to safe
        safe_pool = tod_filter_unused(TOD_SAFE_DARES)
        if not safe_pool:
            safe_pool = list(TOD_SAFE_DARES)
        pick = renpy.random.choice(safe_pool)
        return (pick[1], pick[2], pick[3])

    # ── GF Jealousy Check ─────────────────────────────────

    def tod_gf_would_block(dare_key, target_girl=None, asker=None):
        """Quick check: would the GF block this dare key?
        Used to filter dares BEFORE proposing them (so GF doesn't propose then block).
        asker: for player dares, the girl who proposed the dare (determines who '_her' targets).
        Returns True if GF would block it."""
        blocked, gf = tod_gf_blocks_dare(dare_key, target_girl, asker=asker)
        return blocked

    def _hangout_find_gf():
        """Find the player's GF among present hangout girls, or None."""
        for g in _hangout_girls_list():
            if hasattr(g, "is_dating_player") and g.is_dating_player():
                return g
        return None

    def tod_gf_filter_dares(dare_list, key_index=1):
        """No longer filters by GF — tolerance check happens after selection.
        Kept for API compatibility."""
        return dare_list

    def tod_gf_blocks_dare(dare_key, target_girl, asker=None):
        """Check if the player's GF (if present) blocks a lewd dare.
        Returns (blocks, gf_girl) tuple.
        blocks = True if GF prevents the dare.
        gf_girl = the GF object or None.
        asker: for player dares, the girl who proposed the dare.
               '_her' keys (p_kiss_her etc.) target the asker, not necessarily the GF.

        Lewd player dares that involve OTHER girls (not the GF herself) are blocked
        unless GF is drunk enough (alcohol >= 7).
        Safe dares are never blocked.
        """
        gf = _hangout_find_gf()

        if gf is None:
            return (False, None)

        # Poly GF never blocks lewd dares
        if gf.has_trait("polyamorous"):
            return (False, gf)

        # Harem-exempt target: GF accepts this girl
        if target_girl is not None and is_harem_exempt(gf, target_girl):
            return (False, gf)

        # Safe dares are fine
        safe_keys = set(d[1] for d in TOD_SAFE_DARES)
        # Also safe: player safe dares
        safe_keys.add("show_penis")
        safe_keys.add("p_silly_face")
        safe_keys.add("p_sing_song")
        safe_keys.add("p_show_flashgram")
        safe_keys.add("p_chicken")
        safe_keys.add("p_dance")
        if dare_key in safe_keys:
            return (False, gf)

        # Dares involving the GF herself are fine — but only if the asker IS the GF
        _her_keys = {"p_kiss_her", "p_spank_her", "p_kiss_boobs_her", "p_bj_from_her"}
        if dare_key in _her_keys:
            if asker is not None and asker.gid == gf.gid:
                return (False, gf)
            # asker is another girl — '_her' targets HER, not the GF; fall through to drunk check

        # Lewd dares with OTHER girl are blocked unless GF is drunk enough
        gf_alc = hangout_get_alcohol(gf)
        if gf_alc >= 7:
            return (False, gf)

        return (True, gf)

    # ── GF Tolerance System ─────────────────────────────────

    def _tod_gf_tolerance(gf, target, dare_diff):
        """Calculate GF tolerance for a lewd dare involving target girl.
        Returns "accepts", "reluctant", or "objects".
        Uses alcohol + Girl_like toward target to determine threshold."""
        if gf.has_trait("polyamorous"):
            return "accepts"
        if target is not None and is_harem_exempt(gf, target):
            return "accepts"
        if getattr(store, "_hangout_is_harem_night", False):
            return "accepts"

        alc = hangout_get_alcohol(gf)
        like = gf.get_like_for(target.gid) if target is not None else 0

        # Girl_like tiers reduce alcohol threshold needed
        like_bonus = int(like / 250)  # 0-4
        base_threshold = max(3, 7 - like_bonus)

        # Dare difficulty: easy (3-4) = -1, hard (7-8) = +1
        if dare_diff <= 4:
            threshold = max(2, base_threshold - 1)
        elif dare_diff >= 7:
            threshold = min(9, base_threshold + 1)
        else:
            threshold = base_threshold

        # Cheater GF is more tolerant
        if gf.has_trait("cheater"):
            threshold = max(1, threshold - 2)

        print("[TOD-GF-TOL] gf=%s target=%s diff=%d like=%d alc=%d threshold=%d" % (
            gf.gid, target.gid if target else "?", dare_diff, like, alc, threshold))

        if alc >= threshold:
            return "accepts"
        elif alc >= threshold - 2:
            return "reluctant"
        else:
            return "objects"

    # ── NPC Boyfriend Tolerance System ────────────────────

    def _tod_npc_tolerance(npc, girl, dare_diff):
        """Calculate NPC boyfriend tolerance for a lewd dare involving his girlfriend.
        Returns "ignores", "uneasy", or "protests".
        Uses NPC alcohol + friendship + love + traits to determine threshold."""
        if _npc_is_ntr(npc) and getattr(girl, "_ntr_boundary_discovered", False):
            return "ignores"

        alc = get_drunk(npc) if callable(globals().get("get_drunk")) else 0
        friend = getattr(npc, "friendship_with_player", 200)
        love = getattr(npc, "love_for_girl", 750)

        # Friendship REDUCES threshold (friendlier = more tolerant)
        friend_bonus = 0
        if friend >= 750:
            friend_bonus = 2
        elif friend >= 500:
            friend_bonus = 1
        elif friend < 200:
            friend_bonus = -1
        base_threshold = max(3, 7 - friend_bonus)

        # Love INCREASES threshold (more love = more protective)
        if love >= 700:
            base_threshold = min(9, base_threshold + 1)

        # Dare difficulty: easy (3-4) = -1, hard (7-8) = +1
        if dare_diff <= 4:
            threshold = max(2, base_threshold - 1)
        elif dare_diff >= 7:
            threshold = min(9, base_threshold + 1)
        else:
            threshold = base_threshold

        # NPC traits
        if hasattr(npc, "has_trait"):
            if npc.has_trait("voyeur"):
                threshold = max(1, threshold - 2)
            if npc.has_trait("proud"):
                threshold = min(9, threshold + 1)

        # NTR active but NOT discovered: lower threshold
        if _npc_is_ntr(npc) if callable(globals().get("_npc_is_ntr")) else False:
            threshold = max(2, threshold - 2)

        print("[TOD-NPC-TOL] npc=%s girl=%s diff=%d friend=%d love=%d alc=%.1f threshold=%d" % (
            getattr(npc, "Name", "?"), girl.gid, dare_diff, friend, love, alc, threshold))

        if alc >= threshold:
            return "ignores"
        elif alc >= threshold - 2:
            return "uneasy"
        else:
            return "protests"

    def _tod_is_safe_dare(dare_key):
        """Check if a dare key is safe (non-lewd)."""
        _safe = set(d[1] for d in TOD_SAFE_DARES)
        _safe.update({"show_penis", "p_silly_face", "p_sing_song", "p_show_flashgram", "p_chicken", "p_dance"})
        return dare_key in _safe

    def _tod_gf_dare_target(dare_key, asker, other_girl, gf):
        """Determine who the lewd dare targets (for GF tolerance check).
        Returns the target girl, or None if the dare targets the GF herself."""
        _her_keys = {"p_kiss_her", "p_spank_her", "p_kiss_boobs_her", "p_bj_from_her", "p_lap_her"}
        if dare_key in _her_keys:
            if asker is not None and gf is not None and asker.gid == gf.gid:
                return None  # dare targets GF herself, no jealousy
            return asker  # '_her' targets the asker, who is NOT the GF
        _other_keys = {"p_kiss_other", "p_spank_other", "p_kiss_boobs_other", "p_lap_other"}
        if dare_key in _other_keys:
            if other_girl is not None and gf is not None and other_girl.gid == gf.gid:
                return None  # dare targets GF herself, no jealousy
            return other_girl
        # Girl dares (lewd): target is the dared girl, GF watches
        _girl_lewd = set(d[1] for d in TOD_LEWD_DARES)
        if dare_key in _girl_lewd:
            return None  # handled separately in girl dare flow
        return other_girl

    # ── GF Tolerance Dialogue Pools ──────────────────────

    _GF_RELUCTANT_LINES = [
        _("I don't love this, but... fine. It's just a game."),
        _("Really? ...Okay. But I'm keeping score."),
        _("If you insist. Just don't make it weird."),
        _("You're not going to accept that one, right?"),
    ]

    _GF_OBJECTS_LINES = [
        _("Excuse me? You are NOT doing that."),
        _("No. Absolutely not. I'm right here."),
        _("Are you serious right now? I'm your girlfriend!"),
        _("That's not happening. Pick something else."),
    ]

    _GF_OVERRULED_LINES = [
        _("Wow. Okay. Good to know where I stand."),
        _("You know what? Fine. Do whatever you want."),
        _("I can't believe you're actually doing this to me."),
        _("Don't talk to me after this. Just... don't."),
    ]

    _GF_IS_TARGET_LINES = [
        _("With my own boyfriend? That's barely even a dare!"),
        _("Oh no, something with my boyfriend. How terrible."),
        _("You really thought this would bother me? He's MY boyfriend."),
        _("Best dare ever. Thanks for the excuse~"),
    ]

    _TARGET_GF_HESITATION_LINES = [
        _("I can't do that... she's right there watching us."),
        _("This is awkward with her sitting here..."),
        _("Sorry, but she's your girlfriend. I don't want drama."),
        _("Maybe pick something else? I don't want to cause problems."),
    ]

    # Girl's surprise when GF dares her to do something with the player
    _GF_ASKER_TARGET_SURPRISE_LIGHT = [
        _("Wait... aren't you two together?"),
        _("Are you sure about that? He's your boyfriend."),
        _("You're daring me to do that with YOUR boyfriend?"),
    ]
    _GF_ASKER_TARGET_SURPRISE_HEAVY = [
        _("You want ME to do THAT? With your boyfriend?!"),
        _("Are you serious right now? He's YOUR boyfriend!"),
        _("Girl, are you sure?! That's your man!"),
    ]

    # GF's playful dismissal after target's surprise
    _GF_ASKER_DISMISS_LIGHT = [
        _("It's just a dare! Relax~"),
        _("It's a game! Besides, I'm right here."),
        _("Oh please, it's nothing. Go ahead."),
    ]
    _GF_ASKER_DISMISS_HEAVY = [
        _("I said what I said. A dare is a dare~"),
        _("If I'm the one asking, it's fine. Go ahead."),
        _("I can handle it. Don't chicken out on my dare!"),
    ]

    # ── NPC Boyfriend Tolerance Dialogue Pools ─────────────

    _NPC_UNEASY_LINES = [
        _("I guess it's just a game... right?"),
        _("This is fine. Everything's fine."),
        _("You guys are really pushing it with these dares."),
        _("I'm not sure I like where this is going."),
    ]

    _NPC_PROTEST_LINES = [
        _("Whoa, hold on. That's my girlfriend."),
        _("No way. That's too far. She's with me."),
        _("Are you serious? She's MY girlfriend, man."),
        _("I don't think so. Not with her."),
    ]

    _NPC_BACKED_OFF_LINES = [
        _("...Thanks. I appreciate that."),
        _("Good call. Let's keep it fun."),
        _("Yeah, let's move on to something else."),
    ]

    _NPC_OVERRULED_LINES = [
        _("Seriously? You're just going to ignore me?"),
        _("...Wow. Okay."),
        _("I can't believe this."),
        _("Fine. Whatever."),
    ]

    _GIRL_BF_REASSURE_LINES = [
        _("It's just a game, %(pl)s. Don't worry."),
        _("Relax, %(pn)s. It doesn't mean anything."),
        _("%(Pn)s, look at me. It's fine, okay?"),
        _("Babe, it's Truth or Dare. Calm down."),
    ]

    _GIRL_BF_REFUSE_LINES = [
        _("Sorry, but my %(pl)s is right there. I can't."),
        _("Not with %(pn)s watching... I'd feel awful."),
        _("I want to, but... %(pp)s'd be so hurt."),
        _("%(Pn)s is already uncomfortable. I'll pass."),
    ]

    _OTHER_GIRL_NPC_COMMENT_UNEASY = [
        _("Ooh, someone's not happy..."),
        _("I think you should check on your %(pl)s."),
        _("%(Pp)s looks a little tense over there."),
    ]

    _OTHER_GIRL_NPC_COMMENT_PROTEST = [
        _("Wow, %(pp)s is NOT okay with this."),
        _("Poor thing. %(Pp)s looks like %(pp)s is about to explode."),
        _("Maybe we should pick something else?"),
    ]

    # ── Player Dare Registries ────────────────────────────

    # Player safe dares
    TOD_PLAYER_SAFE_DARES = [
        (_("Make a silly face"),        "p_silly_face",     1),
        (_("Sing a random song"),       "p_sing_song",      2),
        (_("Show your Flashgram page"), "p_show_flashgram", 2),
        (_("Do a chicken impression"),  "p_chicken",        2),
        (_("Dance for us"),             "p_dance",          3),
        (_("Show your... equipment"),   "show_penis",       4),
    ]

    # Player lewd dares - {asker} = girl who asked, {other} = the other girl
    TOD_PLAYER_LEWD_DARES = [
        (_("Let {asker} sit on your lap"),  "p_lap_her",         3),
        (_("Let {other} sit on your lap"),  "p_lap_other",       4),
        ("Kiss {asker}",                  "p_kiss_her",        4),
        ("Kiss {other}",                  "p_kiss_other",      5),
        ("Slap {asker}'s ass",           "p_spank_her",       4),
        ("Slap {other}'s ass",           "p_spank_other",     5),
        ("Kiss {asker}'s boobs",         "p_kiss_boobs_her",  5),
        ("Kiss {other}'s boobs",         "p_kiss_boobs_other",6),
    ]

    # femdom (docs/plan_femdom.md 7): the dares she gives HIM that put him at her service (her lap, her kiss, her
    # boobs) are orders; she prefers them with TOD_FEMDOM_COMMAND_CHANCE x femdom_intensity (Gwen 0.45, Rogue 0.41,
    # Tenny 0.54, NTW / Shion 0.68). Slapping her ass stays the hardcore preference: slaps are hardcore (D3).
    # Her lewd chance (_tod_lewd_chance) gets + TOD_FEMDOM_LEWD_BONUS x intensity.
    TOD_FEMDOM_COMMAND_DARES = ("p_lap_her", "p_kiss_her", "p_kiss_boobs_her")
    TOD_FEMDOM_COMMAND_CHANCE = 0.45
    TOD_FEMDOM_LEWD_BONUS = 0.05

    # ── Auto-pick Player Dare ─────────────────────────────

    def tod_auto_pick_player_dare(asker, other_girl):
        """Girl auto-picks a dare for the player.
        Higher drunk/Inbt = more lewd and harder dares. Traits influence choice.
        GF won't propose dares she would block."""
        alc = hangout_get_alcohol(asker)
        inbt = getattr(asker, "Inbt", 0)
        lewd_chance = _tod_lewd_chance(asker)
        _min_d = tod_get_max_difficulty()

        is_voyeur = hasattr(asker, "has_trait") and asker.has_trait("voyeur")
        is_hardcore = hasattr(asker, "has_trait") and asker.has_trait("hardcore_sex")

        if renpy.random.random() < lewd_chance:
            pool = tod_filter_unused(TOD_PLAYER_LEWD_DARES)
            if not pool:
                pool = list(TOD_PLAYER_LEWD_DARES)
            if other_girl is None:
                pool = [d for d in pool if "other" not in d[1]]
            # Filter by escalation gates (GF tolerance checked after selection)
            pool = _tod_filter_by_escalation(pool)
            # A girl with a partner will not propose a dare her loyalty would make her refuse
            pool = [d for d in pool if not tod_loyalty_blocks_player_dare(d[1], asker, other_girl)]
            if not pool:
                # All lewd dares blocked/gated, fall through to safe
                pass
            else:
                # Voyeur prefers dares involving other girl
                if is_voyeur:
                    other_dares = [d for d in pool if "other" in d[1]]
                    if other_dares and renpy.random.random() < 0.6:
                        pick = _tod_pick_weighted_by_difficulty(other_dares, alc, inbt, min_diff=_min_d)
                        return (pick[1], pick[2])
                # Femdom prefers the dares that put him at her service (x her intensity)
                _fd = femdom_intensity(asker) if hasattr(asker, "has_trait") else 0.0
                if _fd:
                    cmd_dares = [d for d in pool if d[1] in TOD_FEMDOM_COMMAND_DARES]
                    _fd_chance = min(0.9, TOD_FEMDOM_COMMAND_CHANCE * _fd)
                    if cmd_dares and renpy.random.random() < _fd_chance:
                        pick = _tod_pick_weighted_by_difficulty(cmd_dares, alc, inbt, min_diff=_min_d)
                        print("[FEMDOM] %s gives the player a commanding dare: %s (chance %.2f)" % (asker.gid, pick[1], _fd_chance))
                        return (pick[1], pick[2])
                # Hardcore prefers spank
                if is_hardcore:
                    spank_dares = [d for d in pool if "spank" in d[1] and "her" in d[1]]
                    if spank_dares and renpy.random.random() < 0.5:
                        pick = _tod_pick_weighted_by_difficulty(spank_dares, alc, inbt, min_diff=_min_d)
                        return (pick[1], pick[2])
                pick = _tod_pick_weighted_by_difficulty(pool, alc, inbt, min_diff=_min_d)
                return (pick[1], pick[2])
        # Fallback to safe
        safe_pool = tod_filter_unused(TOD_PLAYER_SAFE_DARES)
        if not safe_pool:
            safe_pool = list(TOD_PLAYER_SAFE_DARES)
        pick = renpy.random.choice(safe_pool)
        return (pick[1], pick[2])

    # ── Player Dare Refusal ───────────────────────────────

    def tod_player_dare_refuse():
        """Player refuses a dare. Just drinks penalty, no strip sprites."""
        tod_drink_player(2)


# ============================================================
# MAIN DARE FLOW
# ============================================================

label hangout_tod_dare(girl, asker):
    python:
        store._h_npc = getattr(store, "_hangout_partner_npc", None)
        print("[TOD_DARE] girl=%s asker=%s _h_npc=%s _hangout_partner_npc=%s girls=%s" % (
            girl.gid, asker, store._h_npc,
            getattr(store, "_hangout_partner_npc", "MISSING"),
            [g.gid for g in _hangout_girls_list()]))
        _dare_others = _tod_other_girls(girl)
        _dare_other = _dare_others[0] if _dare_others else None

    if asker == "player":
        # Player picks dare category, then specific dare
        $ _dare_was_lewd = False
        label .dare_pick_category:
        menu:
            "Pick a dare category:"

            "Safe dares":
                python:
                    _dare_was_lewd = False
                    _d_choices = []
                    for _dl, _dk, _dd, _dno in TOD_SAFE_DARES:
                        if tod_is_used(_dk):
                            continue
                        if _dno and len(_dare_others) > 1:
                            for _dtarget in _dare_others:
                                _formatted = _tod_format_dare_label(_dl, _dtarget, player_is_asker=True, translate=True)
                                _d_choices.append((_formatted, (_dk, _dd, _dno, _dtarget)))
                        else:
                            _formatted = _tod_format_dare_label(_dl, _dare_other, player_is_asker=True, translate=True)
                            _d_choices.append((_formatted, (_dk, _dd, _dno)))
                    if not _d_choices:
                        Narration(_("All safe dares have been done already."))
                        _chosen_dare = None
                    else:
                        _d_choices.append((_("Back"), "_back"))
                        _chosen_dare = renpy.display_menu(_d_choices)

            "Lewd dares":
                python:
                    _dare_was_lewd = True
                    _d_avail, _d_disabled = _tod_filter_lewd_dares(girl)
                    _d_choices = []
                    for _dl, _dk, _dd, _dno in _d_avail:
                        if tod_is_used(_dk):
                            continue
                        if _dno and len(_dare_others) > 1:
                            for _dtarget in _dare_others:
                                _formatted = _tod_format_dare_label(_dl, _dtarget, player_is_asker=True, translate=True)
                                _d_choices.append((_formatted, (_dk, _dd, _dno, _dtarget)))
                        else:
                            _formatted = _tod_format_dare_label(_dl, _dare_other, player_is_asker=True, translate=True)
                            _d_choices.append((_formatted, (_dk, _dd, _dno)))
                    for _dl, _dk, _dd, _dno in _d_disabled:
                        _formatted = _tod_format_dare_label(_dl, _dare_other, player_is_asker=True, translate=True) + " " + _tl(_("(already naked)"))
                        _d_choices.append(("!disabled!" + _formatted, None))
                    if not _d_choices:
                        Narration(_("All lewd dares have been done already."))
                        _chosen_dare = None
                    else:
                        _d_choices.append((_("Back"), "_back"))
                        _chosen_dare = renpy.display_menu(_d_choices)

        if _chosen_dare == "_back":
            jump .dare_pick_category

        if _chosen_dare is None:
            return

        python:
            if len(_chosen_dare) == 4:
                _dare_key, _dare_diff, _dare_needs_other, _dare_other = _chosen_dare
            else:
                _dare_key, _dare_diff, _dare_needs_other = _chosen_dare

    else:
        # Girl auto-picks a dare
        python:
            if _dare_others and len(_dare_others) > 1:
                _dare_other = renpy.random.choice(_dare_others)
            _dare_key, _dare_diff, _dare_needs_other = tod_auto_pick_dare(asker, girl, _dare_other)
            _dare_label_text = None
            # Find the label for narration
            for _dl, _dk, _dd, _dno in TOD_SAFE_DARES + TOD_LEWD_DARES:
                if _dk == _dare_key:
                    _dare_label_text = _tod_format_dare_label(_dl, _dare_other, translate=True, asker_girl=asker)
                    break
            if _dare_label_text:
                set_scene_expression(asker, "smirk")
                Say_Line(asker, _dare_label_text + "!")

    # GF tolerance check for girl dares (when dare involves the player)
    python:
        store._tod_gf_was_overruled = False
        _gd_gf = _hangout_find_gf()
        _gd_gf_tolerance = "accepts"
        _GIRL_DARE_PLAYER_KEYS = {"sit_lap_player", "kiss_player", "spank_player",
                                   "kiss_boobs_player", "bj_player", "tj_player",
                                   "flash_boobs", "strip_all"}
        if _gd_gf is not None and _dare_key in _GIRL_DARE_PLAYER_KEYS and _gd_gf.gid != girl.gid and (asker == "player" or _gd_gf.gid != asker.gid):
            _gd_gf_tolerance = _tod_gf_tolerance(_gd_gf, girl, _dare_diff)
            print("[TOD-GD-GF] dare=%s girl=%s tolerance=%s" % (_dare_key, girl.gid, _gd_gf_tolerance))

    if _gd_gf_tolerance == "reluctant":
        python:
            Change_Status(_gd_gf, "Love", -5)
        $ set_scene_expression(_gd_gf, "worried")
        $ Say_Line(_gd_gf, renpy.random.choice(_GF_RELUCTANT_LINES))

    elif _gd_gf_tolerance == "objects":
        $ set_scene_expression(_gd_gf, "angry")
        $ Say_Line(_gd_gf, renpy.random.choice(_GF_OBJECTS_LINES))

        menu:
            "What do you do?"

            "Reconsider":
                $ Narration(_("You step in and cancel the dare."))
                return

            "Do it anyway":
                python:
                    _gd_love_pen = -(10 + _dare_diff * 2)
                    Change_Status(_gd_gf, "Love", _gd_love_pen)
                    Change_Status(_gd_gf, "Obed", 5)
                    _gd_like_pen_gf = -(15 + _dare_diff * 5)
                    _gd_like_pen_target = -(10 + _dare_diff * 3)
                    _gd_gf.add_like_for(girl.gid, _gd_like_pen_gf)
                    girl.add_like_for(_gd_gf.gid, _gd_like_pen_target)
                    print("[TOD-GD-GF-OVERRULED] Love %d, GF->girl like %d, girl->GF like %d" % (
                        _gd_love_pen, _gd_like_pen_gf, _gd_like_pen_target))
                    store._tod_gf_was_overruled = True
                $ set_scene_expression(_gd_gf, "sad")
                $ Say_Line(_gd_gf, renpy.random.choice(_GF_OVERRULED_LINES))

    # Mini-interaction: GF dares a girl to do something with her boyfriend
    python:
        _gf_is_asker_interaction = False
        if _gd_gf is not None and asker != "player" and _gd_gf.gid == asker.gid and _gd_gf.gid != girl.gid:
            _PLAYER_CONTACT_KEYS = {"kiss_player", "spank_player", "kiss_boobs_player",
                                     "bj_player", "tj_player", "sit_lap_player"}
            if _dare_key in _PLAYER_CONTACT_KEYS:
                _gf_is_asker_interaction = True
                _is_heavy_dare = _dare_key in {"bj_player", "tj_player", "kiss_boobs_player"}

    if _gf_is_asker_interaction:
        if _is_heavy_dare:
            $ set_scene_expression(girl, "surprised")
            $ Say_Line(girl, renpy.random.choice(_GF_ASKER_TARGET_SURPRISE_HEAVY))
            $ set_scene_expression(_gd_gf, "smirk")
            $ Say_Line(_gd_gf, renpy.random.choice(_GF_ASKER_DISMISS_HEAVY))
        else:
            $ set_scene_expression(girl, "confused")
            $ Say_Line(girl, renpy.random.choice(_GF_ASKER_TARGET_SURPRISE_LIGHT))
            $ set_scene_expression(_gd_gf, "happy")
            $ Say_Line(_gd_gf, renpy.random.choice(_GF_ASKER_DISMISS_LIGHT))

    # Sexuality gate: hetero girls refuse girl-girl dares and drink double
    if _tod_sexuality_blocks_dare(girl, _dare_key):
        python:
            _spec = _effective_spectrum(girl)
            _gn = girl.Name
            if _spec <= 25:
                _sex_ref_lines = [
                    _("Do that with a girl? No thanks. Not my thing."),
                    _("That's a hard no. I'm not into girls."),
                    _("I'll pass on that one. Girls aren't really my thing."),
                ]
            else:
                _sex_ref_lines = [
                    _("Maybe if I had a few more drinks... but not like this."),
                    _("I'm not drunk enough for that. Ask me later."),
                    _("Hmm... no. Not right now. I'd need more liquid courage."),
                ]
        $ set_scene_expression(girl, "uncomfortable")
        $ Say_Line(girl, renpy.random.choice(_sex_ref_lines))
        $ Narration(_("[_gn] takes a long sip from her drink instead."))
        $ tod_drink(girl, 2)
        return

    # NPC boyfriend tolerance check BEFORE the girl decides
    python:
        store._tod_npc_was_overruled = False
        store._tod_npc_was_uneasy = False
        _npc_protested_dare = False
        _npc_tol_result = "ignores"
        _npc_pd = getattr(store, "_h_npc", None)
        if _npc_pd and _npc_is_active():
            _lewd_keys_pd = set(d[1] for d in TOD_LEWD_DARES)
            _is_lewd_pd = _dare_key in _lewd_keys_pd
            if _is_lewd_pd and _bf_is_gf(_npc_pd, girl):
                _npc_tol_result = _tod_npc_tolerance(_npc_pd, girl, _dare_diff)

    if _npc_tol_result == "uneasy":
        $ _npc_pd.show_sprite(_hangout_npc_pos())
        $ Character(_npc_pd.Name, color=_npc_pd.color)(_tl(renpy.random.choice(_NPC_UNEASY_LINES)))
        python:
            Change_NPC_Status(_npc_pd, "suspicion", 5)
            Change_NPC_Status(_npc_pd, "friendship_with_player", -3)
            store._tod_npc_was_uneasy = True
            _npc_protested_dare = True
            print("[TOD-NPC-TOL] uneasy: susp+5 fr-3")

        # Another girl comments on the NPC's discomfort
        python:
            _npc_comment_girls = [g for g in _hangout_girls_list() if g.gid != girl.gid]
        if _npc_comment_girls:
            $ _npc_commenter = renpy.random.choice(_npc_comment_girls)
            $ set_scene_expression(_npc_commenter, "bemused")
            $ Say_Line(_npc_commenter, _format_partner_line(girl, renpy.random.choice(_OTHER_GIRL_NPC_COMMENT_UNEASY)))   # the partner may be a girlfriend

    elif _npc_tol_result == "protests":
        $ _npc_pd.show_sprite(_hangout_npc_pos())
        $ Character(_npc_pd.Name, color=_npc_pd.color)(_tl(renpy.random.choice(_NPC_PROTEST_LINES)))

        # Another girl comments on the NPC's protest
        python:
            _npc_comment_girls = [g for g in _hangout_girls_list() if g.gid != girl.gid]
        if _npc_comment_girls:
            $ _npc_commenter = renpy.random.choice(_npc_comment_girls)
            $ set_scene_expression(_npc_commenter, "worried")
            $ Say_Line(_npc_commenter, _format_partner_line(girl, renpy.random.choice(_OTHER_GIRL_NPC_COMMENT_PROTEST)))

        if asker == "player":
            $ _tod_npc_ignore_lbl = _npc_menu_caption(_npc_pd, "ignore")   # "Ignore him" / "Ignore her"
            menu:
                "What do you do?"

                "Back off":
                    python:
                        Change_NPC_Status(_npc_pd, "friendship_with_player", 5)
                        print("[TOD-NPC-TOL] player backed off: fr+5")
                    $ Character(_npc_pd.Name, color=_npc_pd.color)(_tl(renpy.random.choice(_NPC_BACKED_OFF_LINES)))
                    return

                "[_tod_npc_ignore_lbl]":
                    python:
                        _npc_fr_loss = -(10 + _dare_diff)
                        _npc_susp_gain = 10 + _dare_diff
                        Change_NPC_Status(_npc_pd, "friendship_with_player", _npc_fr_loss)
                        Change_NPC_Status(_npc_pd, "suspicion", _npc_susp_gain)
                        Change_NPC_Status(_npc_pd, "love_for_girl", -5)
                        store._tod_npc_was_overruled = True
                        _npc_protested_dare = True
                        print("[TOD-NPC-TOL] player ignored: fr%d susp+%d love-5" % (_npc_fr_loss, _npc_susp_gain))
                    $ Character(_npc_pd.Name, color=_npc_pd.color)(_tl(renpy.random.choice(_NPC_OVERRULED_LINES)))
        else:
            # Girl-picked dare: no player menu, just stat penalties
            python:
                Change_NPC_Status(_npc_pd, "suspicion", 10)
                Change_NPC_Status(_npc_pd, "friendship_with_player", -5)
                _npc_protested_dare = True
                print("[TOD-NPC-TOL] girl dare protest: susp+10 fr-5")

    # Loyalty gate (girl with a partner): same rule as the 1:1 flow, before the dare roll
    $ _tod_loyal_reason = tod_loyalty_blocks_dare(girl, TOD_DARE_CHEAT_ACT.get(_dare_key))
    if _tod_loyal_reason:
        $ provoke(girl, 1)

    # Check if girl accepts the dare
    if _tod_loyal_reason is None and tod_girl_accepts_dare(girl, _dare_diff):
        python:
            _alc_acc = hangout_get_alcohol(girl)
            _has_bf_acc = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
            _is_cheater_acc = hasattr(girl, "has_trait") and girl.has_trait("cheater")
            _is_les_acc = hasattr(girl, "has_trait") and girl.has_trait("lesbian")
            _lewd_keys_acc = set(d[1] for d in TOD_LEWD_DARES)
            _is_lewd_acc = _dare_key in _lewd_keys_acc
            _acc_expr = "normal"
            _acc_blush = None
            _tod_disc_trait = None

            # ---- NPC IS PRESENT and is HER partner ----
            if _is_lewd_acc and _has_bf_acc and _npc_is_active() and _bf_is_gf(store._h_npc, girl):
                _npc_ntr_acc = _npc_is_ntr(store._h_npc) if callable(globals().get("_npc_is_ntr")) else False
                _ntr_disc_acc = getattr(girl, "_ntr_boundary_discovered", False)

                if _is_les_acc:
                    _acc_expr = "looking_right"
                    _tod_disc_trait = "lesbian"
                    _acc_lines = [
                        _("Great, my girlfriend gets to watch me do this with a guy..."),
                        _("%(Pp)s is right there. And I'm doing this with a MAN. Wonderful."),
                        _("Sorry, %(pl)s. A dare is a dare. Don't look at me like that."),
                    ]
                elif _is_cheater_acc:
                    _acc_expr = "smirk"
                    _tod_disc_trait = "cheater"
                    _acc_lines = [
                        _("Right in front of %(po)s? Even better."),
                        _("%(Pp)s can watch. Maybe %(pp)s will learn something."),
                        _("Oh, %(pp)s is watching? Good. Let %(po)s see what %(pp)s is missing."),
                    ]
                elif _npc_ntr_acc and _ntr_disc_acc:
                    _acc_expr = "shy"
                    _acc_blush = "1"
                    _acc_lines = [
                        _("%(Pp)s doesn't mind. Right, babe?"),
                        _("It's fine, %(pp)s is into this kind of thing. ...Right?"),
                        _("%(Pp)s said %(pp)s is okay with it. So... here goes."),
                    ]
                elif _npc_ntr_acc:
                    _acc_expr = "embarrassed"
                    _acc_blush = "1"
                    _acc_lines = [
                        _("Babe, you're really not going to say anything? Not even a little jealous?"),
                        _("Wait, %(pl)s... you're just gonna sit there? Okay then."),
                        _("Seriously, %(pl)s? No reaction at all? ...Fine, I guess I'm doing this."),
                    ]
                elif _alc_acc >= 5:
                    _acc_expr = "happy"
                    _acc_blush = "1"
                    _acc_lines = [
                        _("%(Pp)s is watching? So what. I'm drunk enough not to care."),
                        _("Sorry babe, the drinks made me do it. Don't be mad."),
                        _("I know %(pp)s is right there but honestly? Too drunk to care."),
                    ]
                else:
                    _acc_expr = "looking_left"
                    _acc_blush = "1"
                    _acc_lines = [
                        _("It's just a dare, %(pl)s. It doesn't count. Don't make this weird."),
                        _("Everyone's right here, %(pl)s. It's not like I'm sneaking around. It's just a game."),
                        _("Relax, babe. We're all playing together. This doesn't mean anything."),
                        _("Look, we're doing it right in front of you. If it was real, I'd be hiding it."),
                    ]

            # ---- NPC IS ABSENT (she references him) ----
            elif _is_lewd_acc and _is_les_acc and _has_bf_acc:
                _acc_expr = "looking_right"
                _tod_disc_trait = "lesbian"
                _acc_lines = [
                    _("My %(pl)s would hate this... and doing it with a GUY? Ugh."),
                    _("%(Pp)s would lose it. But fine, a dare is a dare."),
                    _("If my %(pl)s finds out about this... whatever. Let's go."),
                ]
            elif _is_lewd_acc and _is_cheater_acc and _has_bf_acc:
                _acc_expr = "smirk"
                _tod_disc_trait = "cheater"
                _acc_lines = [
                    _("My %(pl)s doesn't need to know everything. I'm in."),
                    _("What %(pp)s doesn't know won't hurt %(po)s. Let's go."),
                    _("Relax, it's just a game. My %(pl)s would understand... actually, no. But who cares?"),
                    _("A dare is a dare. And honestly? This sounds fun."),
                    _("My %(pl)s is so boring compared to this. Count me in."),
                ]
            elif _is_lewd_acc and _has_bf_acc:
                if _alc_acc >= 5:
                    _acc_expr = "happy"
                    _acc_blush = "1"
                    _acc_lines = [
                        _("I have a %(pl)s... but I'm too drunk to care right now."),
                        _("My %(pl)s would kill me... oh well. Liquid courage!"),
                        _("The drinks are making me forget I'm taken. Fine, I'll do it."),
                    ]
                else:
                    _acc_expr = "looking_left"
                    _acc_blush = "1"
                    _acc_lines = [
                        _("I... I have a %(pl)s, but... it's just a dare, right?"),
                        _("My %(pl)s can never find out about this. Fine."),
                        _("This is just a game... it doesn't count. That's what I'm telling myself."),
                        _("God, %(pp)s would be so mad if %(pp)s knew... but okay."),
                        _("It's a dare. It means nothing. ...Right?"),
                    ]
            elif _is_lewd_acc and _is_cheater_acc:
                _acc_expr = "smirk"
                # no discover: these lines are plain eagerness, they never name cheating
                _acc_lines = [
                    _("Oh, this should be fun. I'm in."),
                    _("You don't have to ask me twice."),
                    _("Finally, something interesting. Let's do it."),
                    _("I was hoping for something bold. Bring it on."),
                ]
            elif _alc_acc >= 7:
                _acc_expr = "happy"
                _acc_blush = "1"
                _acc_lines = [
                    _("Pfft, sure! I'll do anything right now!"),
                    _("Whatever! I'm too drunk to care. Let's go!"),
                    _("Haha, fine! The drinks are making me brave!"),
                ]
            elif _alc_acc >= 4:
                _acc_expr = "looking_left"
                _acc_blush = "1"
                _acc_lines = [
                    _("Okay... the alcohol is giving me courage. Let's do this."),
                    _("Fine, I'll do it. Blame the drinks."),
                    _("Alright, watch me. Liquid courage engaged."),
                ]
            elif _is_lewd_acc and hasattr(girl, "is_dating_player") and girl.is_dating_player():
                _GIRL_DARE_PLAYER_KEYS_ACC = {"sit_lap_player", "kiss_player", "spank_player", "kiss_boobs_player", "bj_player", "tj_player"}
                if _dare_key in _GIRL_DARE_PLAYER_KEYS_ACC:
                    _acc_expr = "happy"
                    _acc_lines = [
                        _("With my boyfriend? Easy."),
                        _("Fine, but only because it's you~"),
                        _("A dare to do something with my own boyfriend? Wow, how hard."),
                    ]
                else:
                    _acc_expr = "looking_left"
                    _acc_blush = "1"
                    _acc_lines = [
                        _("Fine... but don't look at me like that, babe. It's just a game."),
                        _("Okay, but this stays in this room. Got it?"),
                        _("Alright... babe, stop judging. It's a dare."),
                    ]
            else:
                _acc_expr = "normal"
                _acc_lines = [
                    _("Fine, I'll do it."),
                    _("Okay, okay... here goes."),
                    _("You asked for it."),
                    _("Alright, watch me."),
                    _("Challenge accepted."),
                ]
        $ set_scene_expression(girl, _acc_expr, blush=_acc_blush)
        $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice(_acc_lines)))
        if _tod_disc_trait:
            $ girl.discover("discovered_trait_%s" % _tod_disc_trait)

        # Girl reassures her BF before accepting (when he was uneasy or protested)
        python:
            _bf_reassure = (_is_lewd_acc and _has_bf_acc and _npc_is_active()
                            and _bf_is_gf(store._h_npc, girl)
                            and (getattr(store, "_tod_npc_was_uneasy", False) or getattr(store, "_tod_npc_was_overruled", False))
                            and not _is_cheater_acc and not _is_les_acc)
        if _bf_reassure:
            $ set_scene_expression(girl, "looking_left")
            $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice(_GIRL_BF_REASSURE_LINES)))

        # Her partner reacts to a lewd dare. If he's PRESENT (girl+partner
        # hangout) HE reacts himself; otherwise the other girl comments.
        $ print("[DEBUG NPC REACT] _is_lewd_acc=%s _has_bf_acc=%s _h_npc=%s dare_diff=%s" % (_is_lewd_acc, _has_bf_acc, store._h_npc, _dare_diff))
        if _is_lewd_acc and _has_bf_acc and _npc_is_active() and _bf_is_gf(store._h_npc, girl):
            $ print("[DEBUG NPC REACT] INSIDE IF — NPC Name=%s, color=%s" % (store._h_npc.Name, store._h_npc.color))
            python:
                _npc_watch_raw = _tod_partner_watch_line(store._h_npc, girl, _dare_diff)
                _npc_watch_tl = _tl(_npc_watch_raw)
                _npc_watch_fmt = _format_npc_line(store._h_npc, _npc_watch_tl, girl)
                print("[DEBUG NPC REACT] raw=%s tl=%s fmt=%s" % (_npc_watch_raw, _npc_watch_tl, _npc_watch_fmt))
            $ store._h_npc.show_sprite(_hangout_npc_pos())
            $ Character(store._h_npc.Name, color=store._h_npc.color)(_npc_watch_fmt)

            # Player reassures the NPC (non-NTR only)
            python:
                _npc_d = store._h_npc
                _npc_is_ntr_here = _npc_is_ntr(_npc_d) if callable(globals().get("_npc_is_ntr")) else False
                _npc_discovered = getattr(_npc_d, "_ntr_boundary_discovered", False)
            if not _npc_is_ntr_here:
                $ Say_Player(_tl(renpy.random.choice([
                    _("Relax. It's just a game. Nobody's cheating here."),
                    _("Hey, it's Truth or Dare. We're all just playing. It doesn't mean anything."),
                    _("Come on, we're doing it right here in front of everyone. It's just a dare."),
                ])))
            python:
                if not _npc_discovered:
                    _npc_alc_post = get_drunk(_npc_d) if callable(globals().get("get_drunk")) else 0
                    _penalty_mult = 1.0
                    if _npc_protested_dare:
                        _penalty_mult *= 0.5
                    if _npc_alc_post >= 9:
                        _penalty_mult *= 0.25
                    elif _npc_alc_post >= 5:
                        _penalty_mult *= 0.5
                    if _dare_diff >= 6:
                        Change_NPC_Status(_npc_d, "friendship_with_player", int(-30 * _penalty_mult))
                        Change_NPC_Status(_npc_d, "suspicion", int(20 * _penalty_mult))
                    elif _dare_diff >= 4:
                        Change_NPC_Status(_npc_d, "friendship_with_player", int(-15 * _penalty_mult))
                        Change_NPC_Status(_npc_d, "suspicion", int(10 * _penalty_mult))
                    else:
                        Change_NPC_Status(_npc_d, "friendship_with_player", int(-5 * _penalty_mult))
                    print("[TOD-DARE-NPC] diff=%d mult=%.2f protested=%s alc=%.1f" % (_dare_diff, _penalty_mult, _npc_protested_dare, _npc_alc_post))
        elif _is_lewd_acc and _has_bf_acc:
            python:
                _bf_watcher = _tod_other_girl(girl)
                _watcher_cheater = hasattr(_bf_watcher, "has_trait") and _bf_watcher.has_trait("cheater")
                _watcher_cute = hasattr(_bf_watcher, "has_trait") and _bf_watcher.has_trait("cute_sex")
                _watcher_hardcore = hasattr(_bf_watcher, "has_trait") and _bf_watcher.has_trait("hardcore_sex")
                _w_expr = "surprised"

                if _watcher_cheater:
                    _w_expr = "smug"
                    _w_bf_lines = [
                        _("Your %(pl)s doesn't need to know everything, girl."),
                        _("Live a little! %(Pp)s is not here, is %(pp)s?"),
                        _("What happens in Truth or Dare stays in Truth or Dare~"),
                        _("Relax. It's a game. No one's going to tell %(po)s."),
                    ]
                elif _watcher_hardcore:
                    _w_expr = "sly"
                    _w_bf_lines = [
                        _("Wait, you're actually doing this? What about your %(pl)s?"),
                        _("Bold move with a %(pl)s at home. I respect it."),
                        _("Your %(pl)s doesn't know what %(pp)s is missing. Go for it."),
                    ]
                elif _watcher_cute:
                    _w_expr = "worried"
                    _w_bf_lines = [
                        _("Are you sure about this? You have a %(pl)s..."),
                        _("Oh my god, your %(pl)s... is this okay?!"),
                        _("Girl... what about your %(pl)s? I feel bad just watching..."),
                        _("I would NEVER do this if I had a %(pl)s... but that's just me."),
                    ]
                else:
                    _w_bf_lines = [
                        _("Wait... aren't you with someone? Are you really doing this?"),
                        _("What about your %(pl)s? Are you sure?"),
                        _("Girl... your %(pl)s. Just saying."),
                        _("If your %(pl)s could see this right now..."),
                        _("You have a %(pl)s! Are you serious right now?"),
                    ]
            if _bf_watcher:
                $ set_scene_expression(_bf_watcher, _w_expr)
                $ Say_Line(_bf_watcher, _format_partner_line(girl, renpy.random.choice(_w_bf_lines)))
    else:
        # Context-aware refusal based on why she's refusing
        python:
            _gn = girl.Name
            _alc_ref = hangout_get_alcohol(girl)
            _inbt_ref = getattr(girl, "Inbt", 0)
            _has_bf_ref = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
            _is_cute_ref = hasattr(girl, "has_trait") and girl.has_trait("cute_sex")
            _is_cheater_ref = hasattr(girl, "has_trait") and girl.has_trait("cheater")
            _is_les_ref = hasattr(girl, "has_trait") and girl.has_trait("lesbian")
            _lewd_keys_ref = set(d[1] for d in TOD_LEWD_DARES)
            _is_lewd_ref = _dare_key in _lewd_keys_ref
            _strip_lvl_ref = _tod_girl_strip_level(girl)
            _ref_expr = "serious" if _is_les_ref else "angry"
            _ref_blush = None

            _ref_lines = []
            _is_gf_refusing = hasattr(girl, "is_dating_player") and girl.is_dating_player()

            _is_player_dare = "player" in _dare_key
            if _is_lewd_ref and _is_les_ref and _is_player_dare:
                _ref_expr = "serious"
                _ref_lines.extend([
                    _("I'm a lesbian. I'm not doing that with a guy."),
                    _("That involves a man. Hard pass."),
                    _("Not happening. I'm into girls, remember?"),
                ])

            # Boyfriend-related refusals (cheaters never refuse because of BF)
            _bf_here_ref = _has_bf_ref and _npc_is_active() and _bf_is_gf(store._h_npc, girl)
            if _has_bf_ref and (_dare_diff >= 4 or _tod_loyal_reason) and not _is_cheater_ref:
                _ref_expr = "angry"
                if _bf_here_ref:
                    _npc_name_ref = store._h_npc.Name if store._h_npc else "babe"
                    _ref_lines.extend([
                        _("You've got some nerve suggesting that with %(po)s RIGHT HERE. %(Pp)s is sitting right there!"),
                        _tl(_("Are you serious?! %(Pp)s is in the room! You're not even going to say anything, {npc}?")).replace("{npc}", _npc_name_ref),
                        _("You really just said that in front of my %(pl)s. Wow. No."),
                        _("My %(pl)s is literally watching. What is wrong with you?"),
                    ])
                else:
                    _ref_lines.extend([
                        _("I have a %(pl)s. I can't do that."),
                        _("My %(pl)s would lose it if %(pp)s found out. No."),
                        _("I'm taken. That crosses a line for me."),
                        _("No. I'm in a relationship. That's not happening."),
                        _("My %(pl)s trusts me. I'm not breaking that trust for a dare."),
                        _("Do you know how guilty I'd feel? I have a %(pl)s."),
                    ])

            # Too sober refusals (hint: more drinks would help)
            if _alc_ref < 4:
                if _ref_expr == "serious":
                    _ref_expr = "looking_right"
                if _is_gf_refusing and _is_player_dare:
                    _ref_lines.extend([
                        _("Not sober enough for this kind of dare in public."),
                        _("I need a few more drinks before doing that in front of everyone."),
                        _("Maybe after a few more. I'm not drunk enough for a show."),
                    ])
                else:
                    _ref_lines.extend([
                        _("I'm way too sober for that. Ask me after a few more drinks."),
                        _("Maybe if I was more drunk... but not right now."),
                        _("I need at least three more drinks before I'd even consider that."),
                    ])

            # Too shy / low Inbt refusals (hint: needs more comfort)
            if _inbt_ref < 300:
                if _ref_expr == "serious":
                    _ref_expr = "shy"
                    _ref_blush = "1"
                if _is_gf_refusing and _is_player_dare:
                    _ref_lines.extend([
                        _("With you, sure, but not in front of everyone!"),
                        _("Babe, no! There are people watching!"),
                        _("I'm your girlfriend, not your show pony. Not here."),
                    ])
                elif _is_gf_refusing:
                    _ref_lines.extend([
                        _("I'm not doing that in front of my boyfriend. No way."),
                        _("That's way too much with him right here watching."),
                        _("My boyfriend is right there. I can't do that."),
                    ])
                else:
                    _ref_lines.extend([
                        _("That's too much for me. I barely know you guys like that."),
                        _("I'm not comfortable enough for something like that... not yet."),
                        _("Maybe someday, but tonight? No way."),
                    ])

            # Cute trait specific
            if _is_cute_ref:
                _ref_expr = "embarrassed"
                _ref_blush = "2"
                _ref_lines.extend([
                    _("That's way too embarrassing! I could never..."),
                    _("My heart can't handle that kind of thing!"),
                    _("You're trying to kill me with embarrassment, aren't you?"),
                ])

            # About to lose more clothes (hint: strip pressure)
            if _strip_lvl_ref >= 2:
                if _ref_expr == "serious":
                    _ref_expr = "angry"
                _ref_blush = "1"
                _ref_lines.extend([
                    _("I'm already half naked! I'm not doing that on top of it!"),
                    _("I've lost enough clothes tonight. But still no."),
                ])

            # GF-awareness refusal (player's GF is present and girl cares about her)
            _gf_ref = _hangout_find_gf()
            if _gf_ref and _gf_ref.gid != girl.gid and not _is_cheater_ref:
                _like_gf_ref = girl.get_like_for(_gf_ref.gid)
                if _like_gf_ref >= 500:
                    _ref_lines.extend(_TARGET_GF_HESITATION_LINES)

            # BF-awareness refusal (her boyfriend is uncomfortable/protested)
            if _bf_here_ref and not _is_cheater_ref:
                _npc_was_upset = getattr(store, "_tod_npc_was_overruled", False) or getattr(store, "_tod_npc_was_uneasy", False)
                if _npc_was_upset:
                    _ref_lines.extend(_GIRL_BF_REFUSE_LINES)

            # High difficulty generic
            if _dare_diff >= 7:
                if _ref_expr == "serious":
                    _ref_expr = "angry"
                _ref_lines.extend([
                    _("Are you insane? That's way too extreme."),
                    _("Absolutely not. That's crossing every line there is."),
                ])

            # Fallback
            if not _ref_lines:
                if _is_gf_refusing and _is_player_dare:
                    _ref_lines = [
                        _("Not here, babe. Maybe later when we're alone."),
                        _("I love you, but no. Not with everyone watching."),
                        _("That's a private thing. Not doing it here."),
                    ]
                elif _is_gf_refusing:
                    _ref_lines = [
                        _("Not with my boyfriend right there. Sorry."),
                        _("Babe, tell them I don't have to do this."),
                        _("No. Not happening. Not in front of him."),
                    ]
                else:
                    _ref_lines = [
                        _("No way. Absolutely not."),
                        _("I'm not doing that."),
                        _("Pass. Hard pass."),
                        _("Nope, not happening."),
                    ]

        $ set_scene_expression(girl, _ref_expr, blush=_ref_blush)
        $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice(_ref_lines)))
        $ _gn = girl.Name
        python:
            _strip_lvl, _d_exposed, _removed = tod_dare_strip_penalty(girl)
        $ Narration(_("[_gn] refuses the dare. As penalty, she drinks and takes off her [_removed]."))
        $ tod_drink(girl, 2)
        if _d_exposed == "chest":
            $ set_scene_expression(girl, "embarrassed", blush="2")
            $ Say_Line(girl, renpy.random.choice([
                _("Don't you dare look!"),
                _("I can't believe I'm showing these..."),
                _("I should have just done the dare..."),
            ]))
            $ Say_Player(renpy.random.choice([
                _("I'm definitely looking."),
                _("Maybe you should have done the dare instead~"),
                _("Worth it."),
            ]))
            python:
                Change_Status(girl, "Inbt", 15)
        elif _d_exposed == "panties":
            $ set_scene_expression(girl, "embarrassed", blush="2")
            $ Say_Line(girl, renpy.random.choice([
                _("Everything is out now! Are you all happy?!"),
                _("I'm completely naked... I can't believe this..."),
                _("This is the most embarrassing night of my life..."),
            ]))
            $ Say_Player(renpy.random.choice([
                _("You look incredible. Nothing to be embarrassed about."),
                _("Now THAT is a view."),
                _("You should have just done the dare, but I'm not complaining."),
            ]))
            python:
                Change_Status(girl, "Inbt", 25)
                Change_Status(girl, "Obed", 10)
        elif _strip_lvl <= 2:
            $ set_scene_expression(girl, "uncomfortable")
            $ Say_Line(girl, renpy.random.choice([_("Fine, whatever. It's just clothes."), _("There, happy?"), _("This is so embarrassing...")]))
        else:
            $ set_scene_expression(girl, "embarrassed", blush="1")
            $ Say_Line(girl, renpy.random.choice([_("Don't stare!"), _("I can't believe I'm doing this..."), _("This game is insane...")]))

        # Harem night: other GF teases the one who refused
        if store._hangout_is_harem_night:
            python:
                _ref_others = [_rg for _rg in _hangout_girls_list() if _rg != girl]
            if _ref_others:
                $ set_scene_expression(_ref_others[0], "smirk")
                $ Say_Line(_ref_others[0], _tl(renpy.random.choice(_HAREM_REFUSAL_TEASE_LINES)))

        # NPC boyfriend reacts to the player even SUGGESTING a lewd dare (skip if tolerance system already fired)
        if _is_lewd_ref and _has_bf_ref and asker == "player" and _dare_diff >= 4 and _npc_is_active() and _bf_is_gf(store._h_npc, girl) and not _npc_protested_dare:
            python:
                _npc_rf = store._h_npc
                _npc_ntr_rf = _npc_is_ntr(_npc_rf) if callable(globals().get("_npc_is_ntr")) else False
                _npc_disc_rf = getattr(girl, "_ntr_boundary_discovered", False)

            if _npc_disc_rf:
                pass
            elif _npc_ntr_rf:
                $ Character(store._h_npc.Name, color=store._h_npc.color)(_tl(renpy.random.choice([
                    _("At least she said no... that's good. Right? Yeah. Good."),
                    _("She refused. Obviously. I mean... of course she would. ...Right."),
                ])))
            elif _dare_diff >= 7:
                $ Character(store._h_npc.Name, color=store._h_npc.color)(_tl(renpy.random.choice([
                    _("What the FUCK?! You seriously asked her to do THAT?!"),
                    _("Are you out of your mind?! That's my girlfriend!"),
                    _("I don't care if it's a game, you don't ask someone's girlfriend to do THAT!"),
                ])))
                python:
                    Change_NPC_Status(_npc_rf, "friendship_with_player", -15)
                    Change_NPC_Status(_npc_rf, "suspicion", 10)
                    print("[TOD-DARE-REFUSE-NPC] diff=%d heavy: fr -15, susp +10" % _dare_diff)
            elif _dare_diff >= 5:
                $ Character(store._h_npc.Name, color=store._h_npc.color)(_tl(renpy.random.choice([
                    _("Seriously? You think that's okay to even suggest?"),
                    _("What kind of dare is that?! She's MY girlfriend, dude."),
                    _("Watch yourself. That was way out of line."),
                ])))
                python:
                    Change_NPC_Status(_npc_rf, "friendship_with_player", -10)
                    print("[TOD-DARE-REFUSE-NPC] diff=%d medium: fr -10" % _dare_diff)
            else:
                $ Character(store._h_npc.Name, color=store._h_npc.color)(_tl(renpy.random.choice([
                    _("Hey. Watch it, man. That's my girlfriend."),
                    _("Not cool, dude. She's taken."),
                ])))
                python:
                    Change_NPC_Status(_npc_rf, "friendship_with_player", -5)
                    print("[TOD-DARE-REFUSE-NPC] diff=%d low: fr -5" % _dare_diff)

        return

    # Dispatch to the correct dare label
    if _dare_key == "sit_lap_player":
        call tod_dare_sit_lap(girl) from _call_tod_dare_sit_lap
    elif _dare_key == "silly_face":
        call tod_dare_silly_face(girl) from _call_tod_dare_silly_face
    elif _dare_key == "sing_song":
        call tod_dare_sing_song(girl) from _call_tod_dare_sing_song
    elif _dare_key == "show_flashgram":
        call tod_dare_show_flashgram(girl) from _call_tod_dare_show_flashgram
    elif _dare_key == "chicken":
        call tod_dare_chicken(girl) from _call_tod_dare_chicken
    elif _dare_key == "dance":
        call tod_dare_dance(girl) from _call_tod_dare_dance
    elif _dare_key == "flash_boobs":
        call tod_dare_flash_boobs(girl) from _call_tod_dare_flash_boobs
    elif _dare_key == "strip_all":
        call tod_dare_strip_all(girl) from _call_tod_dare_strip_all
    elif _dare_key == "kiss_player":
        call tod_dare_kiss_player(girl) from _call_tod_dare_kiss_player
    elif _dare_key == "kiss_girl":
        call tod_dare_kiss_girl(girl, _dare_other) from _call_tod_dare_kiss_girl
    elif _dare_key == "suck_boobs":
        call tod_dare_suck_boobs(girl, _dare_other) from _call_tod_dare_suck_boobs
    elif _dare_key == "spank_player":
        call tod_dare_spank_player(girl) from _call_tod_dare_spank_player
    elif _dare_key == "kiss_boobs_player":
        call tod_dare_kiss_boobs_player(girl) from _call_tod_dare_kiss_boobs_player
    elif _dare_key == "spank_other":
        call tod_dare_spank_other(girl, _dare_other) from _call_tod_dare_spank_other
    elif _dare_key == "bj_player":
        call tod_dare_bj_player(girl) from _call_tod_dare_bj_player
    elif _dare_key == "tj_player":
        call tod_dare_tj_player(girl) from _call_tod_dare_tj_player

    # Mark dare as used and update escalation tracker
    python:
        tod_mark_used(_dare_key)
        tod_update_max_difficulty(_dare_diff)

    return


# ============================================================
# NPC BOYFRIEND REACTION (reusable for any dare with BF present)
# ============================================================
label _tod_npc_react_dare(girl, dare_diff):
    python:
        _npc_r = store._h_npc
        _bf_here_r = (hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
                      and _npc_is_active() and _bf_is_gf(_npc_r, girl))
    if _bf_here_r:
        python:
            _npc_watch_raw = _tod_partner_watch_line(_npc_r, girl, dare_diff)
            _npc_watch_tl = _tl(_npc_watch_raw)
            _npc_watch_fmt = _format_npc_line(_npc_r, _npc_watch_tl, girl)
        $ _npc_r.show_sprite(_hangout_npc_pos())
        $ Character(_npc_r.Name, color=_npc_r.color)(_npc_watch_fmt)
    return


# ============================================================
# PLAYER DARE FLOW (when bottle lands on player and he picks dare)
# ============================================================
label hangout_tod_player_dare(asker):
    python:
        _pd_others = _tod_other_girls(asker)
        _pd_other = renpy.random.choice(_pd_others) if _pd_others else None

    # Girl auto-picks a dare for the player
    python:
        _pd_key, _pd_diff = tod_auto_pick_player_dare(asker, _pd_other)
        # Find the label text
        _pd_label = None
        for _pdl, _pdk, _pdd in TOD_PLAYER_SAFE_DARES + TOD_PLAYER_LEWD_DARES:
            if _pdk == _pd_key:
                _pd_en = _pdl.replace("{asker}'s", "my").replace("{asker}", "me")
                _pd_tpl = _tl(_pd_en)
                if _pd_other is not None:
                    _pd_label = _pd_tpl.replace("{other}'s", _pd_other.Name + _tl("'s")).replace("{other}", _pd_other.Name)
                else:
                    _pd_label = _pd_tpl
                break
        # a veteran femdom does not dare him to serve her, she tells him to (docs/plan_femdom.md 7)
        _pd_order = _pd_key in TOD_FEMDOM_COMMAND_DARES and trait_is_veteran(asker, "femdom")
        if _pd_label and _pd_order:
            set_scene_expression(asker, "smug")
            Say_Line(asker, _tl(_("This isn't a dare. It's an order.")) + " " + _pd_label + ".")
            print("[FEMDOM] %s gives the player an order, not a dare: %s" % (asker.gid, _pd_key))
        elif _pd_label:
            set_scene_expression(asker, "smirk")
            Say_Line(asker, _tl(_("I dare you to...")) + " " + _pd_label + "!")

    # GF tolerance check (replaces binary blocking)
    python:
        store._tod_gf_was_overruled = False
        _pd_gf = _hangout_find_gf()
        _pd_gf_tolerance = "accepts"
        if _pd_gf is not None and not _tod_is_safe_dare(_pd_key):
            _pd_gf_target = _tod_gf_dare_target(_pd_key, asker, _pd_other, _pd_gf)
            if _pd_gf_target is not None:
                _pd_gf_tolerance = _tod_gf_tolerance(_pd_gf, _pd_gf_target, _pd_diff)
                print("[TOD-PD-GF] key=%s target=%s tolerance=%s" % (_pd_key, _pd_gf_target.gid, _pd_gf_tolerance))

    if _pd_gf_tolerance == "reluctant":
        python:
            Change_Status(_pd_gf, "Love", -5)
        $ set_scene_expression(_pd_gf, "worried")
        $ Say_Line(_pd_gf, renpy.random.choice(_GF_RELUCTANT_LINES))

    elif _pd_gf_tolerance == "objects":
        $ set_scene_expression(_pd_gf, "angry")
        $ Say_Line(_pd_gf, renpy.random.choice(_GF_OBJECTS_LINES))

        menu:
            "What do you do?"

            "Reconsider":
                $ Narration(_("You decide it's not worth the argument."))
                return

            "Do it anyway":
                python:
                    _gf_love_penalty = -(10 + _pd_diff * 2)
                    Change_Status(_pd_gf, "Love", _gf_love_penalty)
                    Change_Status(_pd_gf, "Obed", 5)
                    if _pd_gf_target is not None:
                        _gf_like_penalty = -(15 + _pd_diff * 5)
                        _target_like_penalty = -(10 + _pd_diff * 3)
                        _pd_gf.add_like_for(_pd_gf_target.gid, _gf_like_penalty)
                        _pd_gf_target.add_like_for(_pd_gf.gid, _target_like_penalty)
                        print("[TOD-PD-GF-OVERRULED] Love %d, GF->target like %d, target->GF like %d" % (
                            _gf_love_penalty, _gf_like_penalty, _target_like_penalty))
                    store._tod_gf_was_overruled = True
                $ set_scene_expression(_pd_gf, "sad")
                $ Say_Line(_pd_gf, renpy.random.choice(_GF_OVERRULED_LINES))

    # NPC boyfriend tolerance check for player dares
    python:
        store._tod_npc_was_overruled = False
        store._tod_npc_was_uneasy = False
        _pd_npc = getattr(store, "_h_npc", None)
        _pd_npc_tol = "ignores"
        _pd_npc_target = None
        if _pd_npc and _npc_is_active() and not _tod_is_safe_dare(_pd_key):
            _her_keys_pd = {"p_kiss_her", "p_spank_her", "p_kiss_boobs_her", "p_bj_from_her", "p_lap_her"}
            _other_keys_pd = {"p_kiss_other", "p_spank_other", "p_kiss_boobs_other", "p_lap_other"}
            if _pd_key in _her_keys_pd and _bf_is_gf(_pd_npc, asker):
                _pd_npc_target = asker
            elif _pd_key in _other_keys_pd and _pd_other is not None and _bf_is_gf(_pd_npc, _pd_other):
                _pd_npc_target = _pd_other
            if _pd_npc_target is not None:
                _pd_npc_tol = _tod_npc_tolerance(_pd_npc, _pd_npc_target, _pd_diff)
                print("[TOD-PD-NPC] key=%s target=%s tolerance=%s" % (_pd_key, _pd_npc_target.gid, _pd_npc_tol))

    if _pd_npc_tol == "uneasy":
        $ _pd_npc.show_sprite(_hangout_npc_pos())
        $ Character(_pd_npc.Name, color=_pd_npc.color)(_tl(renpy.random.choice(_NPC_UNEASY_LINES)))
        python:
            Change_NPC_Status(_pd_npc, "suspicion", 5)
            Change_NPC_Status(_pd_npc, "friendship_with_player", -3)
            store._tod_npc_was_uneasy = True
            print("[TOD-PD-NPC] uneasy: susp+5 fr-3")

    elif _pd_npc_tol == "protests":
        $ _pd_npc.show_sprite(_hangout_npc_pos())
        $ Character(_pd_npc.Name, color=_pd_npc.color)(_tl(renpy.random.choice(_NPC_PROTEST_LINES)))

        $ _tod_npc_ignore_lbl = _npc_menu_caption(_pd_npc, "ignore")   # "Ignore him" / "Ignore her"
        menu:
            "What do you do?"

            "Back off":
                python:
                    Change_NPC_Status(_pd_npc, "friendship_with_player", 5)
                    print("[TOD-PD-NPC] backed off: fr+5")
                $ Character(_pd_npc.Name, color=_pd_npc.color)(_tl(renpy.random.choice(_NPC_BACKED_OFF_LINES)))
                return

            "[_tod_npc_ignore_lbl]":
                python:
                    _pd_npc_fr_loss = -(10 + _pd_diff)
                    _pd_npc_susp_gain = 10 + _pd_diff
                    Change_NPC_Status(_pd_npc, "friendship_with_player", _pd_npc_fr_loss)
                    Change_NPC_Status(_pd_npc, "suspicion", _pd_npc_susp_gain)
                    Change_NPC_Status(_pd_npc, "love_for_girl", -5)
                    store._tod_npc_was_overruled = True
                    print("[TOD-PD-NPC] ignored: fr%d susp+%d love-5" % (_pd_npc_fr_loss, _pd_npc_susp_gain))
                $ Character(_pd_npc.Name, color=_pd_npc.color)(_tl(renpy.random.choice(_NPC_OVERRULED_LINES)))

    # Target girl with a partner: her loyalty can veto the dare (same gate as 1:1)
    python:
        _pd_act_info = TOD_PDARE_CHEAT_ACT.get(_pd_key)
        _pd_loyal_target = None
        _pd_loyal_reason = None
        if _pd_act_info:
            _pd_loyal_target = asker if _pd_act_info[1] == "her" else _pd_other
            _pd_loyal_reason = tod_loyalty_blocks_dare(_pd_loyal_target, _pd_act_info[0])
    if _pd_loyal_reason and _pd_loyal_target is not None:
        $ set_scene_expression(_pd_loyal_target, "serious")
        $ Say_Line(_pd_loyal_target, _format_partner_line(_pd_loyal_target, renpy.random.choice([
            _("Wait, no. I have %(pl)s. Pick something else."),
            _("I'm taken. That one's off the table."),
            _("Not that. My %(pl)s would never forgive me."),
        ])))
        $ provoke(_pd_loyal_target, 1)
        $ Narration(_("She shakes her head. The dare is cancelled."))
        return

    # Player can refuse the dare
    menu:
        "Do you accept the dare?"

        "Accept":
            pass

        "Refuse (drink 2 doses as penalty)":
            $ tod_player_dare_refuse()
            python:
                _p_alc = hangout_get_player_alcohol()
            $ Narration(_("You down your penalty drinks. Your head swims a little."))
            # a veteran femdom takes it as a refused order; the drinks are the game's penalty, so no stat here
            if trait_is_veteran(asker, "femdom"):
                $ print("[FEMDOM] %s: the player refused her dare %s" % (asker.gid, _pd_key))
                $ set_scene_expression(asker, "annoyed")
                $ Say_Line(asker, renpy.random.choice([
                    _("You don't say no to me. Drink. All of it."),
                    _("Refusing me? Bold. Drink up, and remember this."),
                    _("Wrong answer. Next time you do what I say."),
                ]))
                return
            $ set_scene_expression(asker, "bemused")
            $ Say_Line(asker, renpy.random.choice([
                _("Coward!"),
                _("Boo! You're no fun."),
                _("Weak! I expected more from you."),
                _("Lame! But more drinks for you, I guess."),
            ]))
            return

    # GF watching reaction (only if tolerance was "accepts" — reluctant/objects already reacted above)
    python:
        _is_safe_pd = _tod_is_safe_dare(_pd_key)
        _her_player_keys = {"p_kiss_her", "p_spank_her", "p_kiss_boobs_her", "p_lap_her"}
        _other_player_keys = {"p_kiss_other", "p_spank_other", "p_kiss_boobs_other", "p_lap_other"}
        _is_gf_target_pd = False
        if _pd_gf is not None:
            if _pd_key in _her_player_keys and asker.gid == _pd_gf.gid:
                _is_gf_target_pd = True
            elif _pd_key in _other_player_keys and _pd_other is not None and _pd_other.gid == _pd_gf.gid:
                _is_gf_target_pd = True

    # GF is the dare target — playful reaction (kiss MY boyfriend? easy!)
    if _is_gf_target_pd and _pd_gf is not None:
        $ set_scene_expression(_pd_gf, "happy")
        $ Say_Line(_pd_gf, renpy.random.choice(_GF_IS_TARGET_LINES))

    elif _pd_gf is not None and not _is_safe_pd and not _is_gf_target_pd and _pd_gf_tolerance == "accepts":
        if store._hangout_is_harem_night:
            $ set_scene_expression(_pd_gf, "sly")
            $ Say_Line(_pd_gf, _tl(renpy.random.choice(_HAREM_GF_TEASE_LINES)))
        elif _pd_gf.gid == asker.gid:
            $ set_scene_expression(_pd_gf, "looking_left")
            $ Say_Line(_pd_gf, renpy.random.choice([
                _("I asked for it... doesn't mean I like watching it."),
                _("It was MY dare. I can handle it. ...Probably."),
                _("Just get it over with. I'm the one who said it."),
            ]))
        else:
            python:
                Change_Status(_pd_gf, "Love", -5)
            $ set_scene_expression(_pd_gf, "looking_left")
            $ Say_Line(_pd_gf, renpy.random.choice([
                _("I can't believe you're actually doing this..."),
                _("I'm watching. Don't enjoy it too much."),
                _("Fine. Whatever. It's just a game..."),
            ]))

    # Other girl comments on BF situation for player lewd dares
    python:
        # Determine the target girl for the dare
        _her_keys = {"p_kiss_her", "p_spank_her", "p_kiss_boobs_her", "p_lap_her"}
        _other_keys = {"p_kiss_other", "p_spank_other", "p_kiss_boobs_other", "p_lap_other"}
        if _pd_key in _her_keys:
            _pd_target = asker
            _pd_commenter = _pd_other
        elif _pd_key in _other_keys:
            _pd_target = _pd_other
            _pd_commenter = asker
        else:
            _pd_target = None
            _pd_commenter = None

        _pd_target_bf = _pd_target is not None and hasattr(_pd_target, "has_npc_partner") and _pd_target.has_npc_partner()
        _pd_target_cheater = _pd_target is not None and hasattr(_pd_target, "has_trait") and _pd_target.has_trait("cheater")
        if store._hangout_is_harem_night:
            _pd_target_bf = False

    if _pd_target_bf and _pd_commenter is not None and not _is_safe_pd:
        python:
            _npc_present_pd = _npc_is_active() and store._h_npc is not None and _bf_is_gf(store._h_npc, _pd_target)
            _cm_cheater = hasattr(_pd_commenter, "has_trait") and _pd_commenter.has_trait("cheater")
            _cm_cute = hasattr(_pd_commenter, "has_trait") and _pd_commenter.has_trait("cute_sex")
            _cm_expr = "surprised"
            _gf_dared = _pd_key in _her_keys

            if _pd_target_cheater:
                _pd_bf_comment = None
            elif _npc_present_pd:
                # NPC is RIGHT HERE — acknowledge his presence
                _npc_n_pd = store._h_npc.Name
                if _gf_dared:
                    # The GF herself dared the player — commenter addresses the NPC
                    if _cm_cheater:
                        _cm_expr = "smug"
                        _pd_bf_comment = _tl(renpy.random.choice([
                            _("{npc}... you're just gonna sit there? This is gold."),
                            _("I love that {npc} has a front row seat for this~"),
                        ])).replace("{npc}", _npc_n_pd)
                    elif _cm_cute:
                        _cm_expr = "worried"
                        _pd_bf_comment = _tl(renpy.random.choice([
                            _("{npc}... she just dared him herself... are you okay?"),
                            _("I feel so bad... {npc} is right there watching this..."),
                        ])).replace("{npc}", _npc_n_pd)
                    else:
                        _pd_bf_comment = _tl(renpy.random.choice([
                            _("{npc}... you're okay with this? Wow."),
                            _("Is nobody going to mention that {npc} is sitting RIGHT there?"),
                            _("She dared him herself? With {npc} watching? That's bold."),
                        ])).replace("{npc}", _npc_n_pd)
                else:
                    # Commenter IS the asker — she made the dare, lines reflect ownership
                    if _cm_cheater:
                        _cm_expr = "smug"
                        _pd_bf_comment = _tl(renpy.random.choice([
                            _("Yeah, I said it. {npc} can deal with it."),
                            _("{npc} can watch. Makes it more fun."),
                        ])).replace("{npc}", _npc_n_pd)
                    elif _cm_cute:
                        _cm_expr = "worried"
                        _pd_bf_comment = _tl(renpy.random.choice([
                            _("I know, I know... I shouldn't have... {npc} is right there..."),
                            _("I didn't think this through... {npc} is watching..."),
                        ])).replace("{npc}", _npc_n_pd)
                    else:
                        _pd_bf_comment = _tl(renpy.random.choice([
                            _("I know what I said. {npc} can watch if %(pp)s wants."),
                            _("{npc} is right there, you know. Right THERE."),
                            _("You're doing this with {npc} watching? That takes nerve."),
                        ])).replace("{npc}", _npc_n_pd)
            elif _cm_cheater:
                # NPC NOT present — existing absent-boyfriend lines
                _cm_expr = "smug"
                _pd_bf_comment = renpy.random.choice([
                    _("Don't worry about her %(pl)s. %(Pp)s'll survive."),
                    _("Her %(pl)s doesn't own her. Go ahead."),
                    _("A dare is a dare. Her %(pl)s isn't here to complain."),
                ])
            elif _cm_cute:
                _cm_expr = "worried"
                _pd_bf_comment = renpy.random.choice([
                    _("Um... she has a %(pl)s, you know. Are you both okay with this?"),
                    _("This feels wrong... she's with someone..."),
                    _("I can't watch. She has a %(pl)s!"),
                ])
            else:
                _pd_bf_comment = renpy.random.choice([
                    _("She has a %(pl)s, you know. Just saying."),
                    _("Her %(pl)s is going to love hearing about this one."),
                    _("Are you seriously doing this? She's taken."),
                    _("What about her %(pl)s? No one cares, apparently."),
                ])

        if _pd_bf_comment is not None:
            $ set_scene_expression(_pd_commenter, _cm_expr)
            $ Say_Line(_pd_commenter, _format_partner_line(_pd_target, _pd_bf_comment))

    # Dispatch to specific player dare labels
    if _pd_key == "p_lap_her":
        call tod_pdare_lap(asker) from _call_tod_pdare_lap_her
    elif _pd_key == "p_lap_other":
        call tod_pdare_lap(_pd_other) from _call_tod_pdare_lap_other
    elif _pd_key == "p_silly_face":
        call tod_pdare_silly_face from _call_tod_pdare_silly
    elif _pd_key == "p_sing_song":
        call tod_pdare_sing from _call_tod_pdare_sing
    elif _pd_key == "p_show_flashgram":
        call tod_pdare_flashgram(_hangout_girls_list()) from _call_tod_pdare_flash
    elif _pd_key == "p_chicken":
        call tod_pdare_chicken from _call_tod_pdare_chicken
    elif _pd_key == "p_dance":
        call tod_pdare_dance(_hangout_girls_list()) from _call_tod_pdare_dance
    elif _pd_key == "show_penis":
        call tod_pdare_show_penis(_hangout_girls_list(), asker) from _call_tod_pdare_penis
    elif _pd_key == "p_kiss_her":
        call tod_pdare_kiss(asker) from _call_tod_pdare_kiss_her
    elif _pd_key == "p_kiss_other":
        call tod_pdare_kiss(_pd_other) from _call_tod_pdare_kiss_other
    elif _pd_key == "p_spank_her":
        call tod_pdare_spank(asker) from _call_tod_pdare_spank_her
    elif _pd_key == "p_spank_other":
        call tod_pdare_spank(_pd_other) from _call_tod_pdare_spank_other
    elif _pd_key == "p_kiss_boobs_her":
        call tod_pdare_kiss_boobs(asker) from _call_tod_pdare_kboobs_her
    elif _pd_key == "p_kiss_boobs_other":
        call tod_pdare_kiss_boobs(_pd_other) from _call_tod_pdare_kboobs_other

    # Mark player dare as used and update escalation tracker
    python:
        tod_mark_used(_pd_key)
        tod_update_max_difficulty(_pd_diff)

    return


# ============================================================
# PLAYER SAFE DARES
# ============================================================

# --- Player Silly Face ---
label tod_pdare_silly_face:
    $ Say_Player(renpy.random.choice([_("Alright, check this out."), _("Prepare yourselves."), _("You asked for it...")]))
    $ Narration(_("You cross your eyes, puff out your cheeks, and stick your tongue out sideways."))
    python:
        _sf_pools = [
            ("laugh", [
                _("Oh my God, what IS that face?!"),
                _("That's horrifying. I love it."),
                _("Please never do that again."),
            ]),
            ("bemused", [
                _("I think I just lost my appetite."),
                _("That was actually impressive. In a bad way."),
                _("You look like a cartoon character having a stroke."),
            ]),
            ("laugh", [
                _("I can't unsee that. It's burned into my brain."),
                _("Do it again! No, actually, don't."),
                _("That face should be illegal."),
            ]),
        ]
        for _si, _sg in enumerate(_hangout_girls_list()):
            Change_Status(_sg, "Inbt", 10)
            _se, _sp = _sf_pools[min(_si, len(_sf_pools) - 1)]
            set_scene_expression(_sg, _se)
            Say_Line(_sg, renpy.random.choice(_sp))
    return


# --- Player Sing ---
label tod_pdare_sing:
    $ Say_Player(renpy.random.choice([_("Fine, but no judging."), _("I'm warning you, this won't be pretty."), _("My singing career starts now.")]))
    python:
        _sing_bits = [
            _("You belt out a pop song so off-key that everyone winces at the same time."),
            _("You attempt a love ballad. The words are wrong, the pitch is wrong, everything is wrong."),
            _("You rap the first thing that comes to mind. It's awful. You forget the beat halfway through."),
        ]
        Narration(renpy.random.choice(_sing_bits))
    python:
        _sing_pools = [
            ("grimace", [
                _("That was... something."),
                _("My ears are bleeding. Literally bleeding."),
                _("Don't quit your day job. Please."),
            ]),
            ("laugh", [
                _("I've heard cats fight that sounded better."),
                _("Encore! Just kidding. Never again."),
                _("Points for confidence, though."),
            ]),
            ("bemused", [
                _("Was that supposed to be a song?"),
                _("I need a moment to recover from that."),
                _("At least you committed to it."),
            ]),
        ]
        for _si, _sg in enumerate(_hangout_girls_list()):
            Change_Status(_sg, "Inbt", 10)
            _se, _sp = _sing_pools[min(_si, len(_sing_pools) - 1)]
            set_scene_expression(_sg, _se)
            Say_Line(_sg, renpy.random.choice(_sp))
    return


# --- Player Show Flashgram ---
label tod_pdare_flashgram(girls):
    $ Say_Player(renpy.random.choice([_("Okay, fine. Here's my phone."), _("Don't scroll too far..."), _("You asked for this.")]))
    $ Narration(_("You hand over your phone with your Flashgram page open."))
    python:
        _flash_content = renpy.random.choice(["music", "memes", "gothic_bikini"])

    python:
        _fg_music = [
            ("happy", [
                _("Oh, you're a music nerd? That's actually cool."),
                _("Nice taste. Well, some of it."),
                _("These playlists are... interesting."),
            ]),
            ("surprised", [
                _("I didn't expect that. Not bad."),
                _("Send me that playlist later."),
                _("At least it's not something embarrassing."),
            ]),
            ("happy", [
                _("I know some of these artists!"),
                _("Your music taste is better than I expected."),
            ]),
        ]
        _fg_memes = [
            ("bemused", [
                _("This is your entire feed? Just memes?"),
                _("Okay, that one's actually funny."),
                _("You're a meme hoarder. Noted."),
            ]),
            ("laugh", [
                _("A man of culture, I see."),
                _("Some of these are ancient. Like, fossil-level old."),
                _("Send me that one. No, the other one. That one."),
            ]),
            ("laugh", [
                _("I'm saving this one for later."),
                _("Your meme game is top tier, I'll admit."),
            ]),
        ]
        _fg_goth = [
            ("surprised", [
                _("So THAT'S your type, huh?"),
                _("Wow. Okay. You like them... alternative."),
                _("That's... a lot of gothic cleavage."),
            ]),
            ("smirk", [
                _("Should I be wearing more black eyeliner?"),
                _("I mean... they're hot, I'll give you that."),
                _("This explains so much about you."),
            ]),
            ("surprised", [
                _("I see the pattern here..."),
                _("You really have a type, don't you?"),
            ]),
        ]

    if _flash_content == "music":
        $ Narration(_("Your feed is full of music playlists and concert clips."))
        python:
            for _fi, _fg in enumerate(girls):
                if _fg:
                    _fe, _fp = _fg_music[min(_fi, len(_fg_music) - 1)]
                    set_scene_expression(_fg, _fe)
                    Say_Line(_fg, renpy.random.choice(_fp))
                    Change_Status(_fg, "Inbt", 10)

    elif _flash_content == "memes":
        $ Narration(_("Your feed is nothing but memes. Page after page of memes."))
        python:
            for _fi, _fg in enumerate(girls):
                if _fg:
                    _fe, _fp = _fg_memes[min(_fi, len(_fg_memes) - 1)]
                    set_scene_expression(_fg, _fe)
                    Say_Line(_fg, renpy.random.choice(_fp))
                    Change_Status(_fg, "Inbt", 10)

    else:
        $ Narration(_("Your feed is full of gothic girls posing in bikinis. Dark makeup, pale skin, lots of lace."))
        python:
            for _fi, _fg in enumerate(girls):
                if _fg:
                    _fe, _fp = _fg_goth[min(_fi, len(_fg_goth) - 1)]
                    set_scene_expression(_fg, _fe, blush=1)
                    Say_Line(_fg, renpy.random.choice(_fp))
                    Change_Status(_fg, "Inbt", 20)
                    Change_Status(_fg, "Obed", 10)

    return


# --- Player Chicken ---
label tod_pdare_chicken:
    $ Say_Player(renpy.random.choice([_("I'm going to regret this."), _("Full commitment. Here we go."), _("Bawk bawk.")]))
    $ Narration(_("You stand up, tuck your hands under your armpits, and start clucking and strutting around the room."))
    python:
        _ck_pools = [
            ("laugh", [
                _("Oh my God, stop! I'm going to die laughing!"),
                _("That's the most committed chicken I've ever seen."),
                _("The head bobbing is killing me!"),
            ]),
            ("bemused", [
                _("I think he's actually part chicken."),
                _("Please sit down. My stomach hurts from laughing."),
                _("That was... disturbingly realistic."),
            ]),
            ("laugh", [
                _("The clucking! I can't breathe!"),
                _("I'm never going to forget this image."),
                _("Someone record this, please!"),
            ]),
        ]
        for _si, _sg in enumerate(_hangout_girls_list()):
            Change_Status(_sg, "Inbt", 10)
            _se, _sp = _ck_pools[min(_si, len(_ck_pools) - 1)]
            set_scene_expression(_sg, _se)
            Say_Line(_sg, renpy.random.choice(_sp))
    return


# --- Player Dance ---
label tod_pdare_dance(girls):
    $ Say_Player(renpy.random.choice([_("Time to show you my moves."), _("No music? No problem."), _("Watch and learn.")]))
    python:
        _dance_bits = [
            _("You bust out some moves that are equal parts confident and terrible. It's mesmerizing."),
            _("You do a slow body roll that's either incredibly smooth or incredibly awkward. Hard to tell."),
            _("You attempt a breakdance move, nearly fall, then recover with a dramatic spin."),
        ]
        Narration(renpy.random.choice(_dance_bits))
    python:
        _dn_pools = [
            ("surprised", [
                _("That was... actually not terrible?"),
                _("I'm impressed. And confused. But mostly impressed."),
                _("Okay, you've got rhythm. I'll give you that."),
            ]),
            ("happy", [
                _("More! Do the spin thing again!"),
                _("I need to record this next time."),
                _("Seven out of ten. Would watch again."),
            ]),
            ("laugh", [
                _("I want to learn that move!"),
                _("That was honestly entertaining."),
                _("You should do this more often."),
            ]),
        ]
        for _di, _dg in enumerate(girls):
            if _dg:
                Change_Status(_dg, "Inbt", 15)
                _de, _dp = _dn_pools[min(_di, len(_dn_pools) - 1)]
                set_scene_expression(_dg, _de)
                Say_Line(_dg, renpy.random.choice(_dp))
    return


# --- Player Show Penis ---
label tod_pdare_show_penis(girls, asker=None):
    $ Narration(_("You take a breath, pull down your pants, and show everything."))
    python:
        for _g in girls:
            if _g:
                _g.RegisterAction("girl_saw_penis")
    pause 1.0

    python:
        _sp_very = [
            [
                _("Oh my god... that is NOT what I was expecting."),
                _("Holy... that's... wow. That's big."),
                _("I... okay. I need a second. That's huge."),
            ],
            [
                _("Are you serious right now?! That thing is massive!"),
                _("I... can't stop staring. Sorry. Wow."),
                _("That is... way bigger than I imagined. Like, way bigger."),
            ],
            [
                _("Wait, THAT'S what you've been hiding?!"),
                _("I'm speechless. Genuinely speechless."),
            ],
        ]
        _sp_good = [
            [
                _("Oh! That's... bigger than I thought it would be."),
                _("Well, someone's been hiding something. Not bad at all."),
                _("Okay, I'm surprised. In a good way."),
            ],
            [
                _("Huh. That's actually impressive."),
                _("Wow, okay. I was not expecting that size."),
                _("Not bad... not bad at all."),
            ],
            [
                _("Color me impressed."),
                _("Okay, I see you. Not bad at all."),
            ],
        ]
        _sp_ok = [
            [
                _("Oh! Well... that's a surprise."),
                _("Bigger than I expected, honestly."),
                _("Huh. You've been holding out on us."),
            ],
            [
                _("Wait, that's actually pretty nice."),
                _("Not gonna lie, I'm pleasantly surprised."),
                _("Okay, respect. That's more than I thought."),
            ],
            [
                _("Well, that was unexpected."),
                _("Pleasantly surprised over here."),
            ],
        ]

        # Asker-specific pools: she dared it, so she's smug, not surprised
        _sp_asker_very = [
            _("See? I knew you had something special hiding in there."),
            _("Damn. Good dare on my part."),
            _("Well well well... I was right to be curious."),
        ]
        _sp_asker_good = [
            _("Ha! Not bad at all. I knew it was worth asking."),
            _("See? That wasn't so hard. And honestly? Impressive."),
            _("I pick good dares, don't I?"),
        ]
        _sp_asker_ok = [
            _("There you go! That wasn't so bad, was it?"),
            _("Ha! You actually did it. Respect."),
            _("See? Nothing to be shy about."),
        ]

        if Player.attractiveness >= 76:
            _sp_pools, _sp_blush, _sp_inbt = _sp_very, "2", 25
            _sp_asker_pool = _sp_asker_very
        elif Player.attractiveness >= 26:
            _sp_pools, _sp_blush, _sp_inbt = _sp_good, "1", 20
            _sp_asker_pool = _sp_asker_good
        else:
            _sp_pools, _sp_blush, _sp_inbt = _sp_ok, None, 15
            _sp_asker_pool = _sp_asker_ok

        # Check which girls have already seen the player's penis via sex acts
        # acts only: every position already counts as "sex" (or "anal") in Sex_acts
        _PENIS_SEEN_ACTS = ("hj", "bj", "tj", "sex", "anal")
        _sp_has_seen = {}
        for _pg in girls:
            if _pg:
                _pg_acts = getattr(_pg, "Sex_acts", {}) or {}
                _sp_has_seen[_pg.gid] = any(_pg_acts.get(k, 0) > 0 for k in _PENIS_SEEN_ACTS)

        _sp_seen_lines = [
            _("Mm, that's familiar. No surprises here."),
            _("I've already had a good look at that. Still nice though."),
            _("Nothing new for me. But enjoy the show, girls."),
            _("I've seen it before. Still not bad."),
        ]
        _sp_asker_seen_lines = [
            _("I've already had a personal viewing. This dare was for THEM."),
            _("Old news for me. Let's see how the others handle it."),
            _("I already know what you're packing. Show the rest of the class."),
        ]

        # Player's GF — possessive when she's seen it, indignant when she hasn't
        _sp_gf_seen_lines = [
            _("That's mine, girls. Look all you want."),
            _("I know every inch of that. Trust me, the rest matches."),
            _("Ha. It's even better in private."),
            _("I've had the full tour already. Enjoy the preview."),
        ]
        _sp_gf_asker_seen_lines = [
            _("I know exactly what I dared you to show. And I'm proud of it."),
            _("This was for their benefit, not mine. I've had the VIP experience."),
            _("Come on, girls. I dared him for a reason. Feast your eyes."),
        ]
        _sp_gf_first_lines = [
            _("I'm your girlfriend and THIS is how I find out?!"),
            _("Seriously?! Everyone gets to see this before I do properly?!"),
            _("I can't believe my own boyfriend is... okay, I'm looking."),
            _("This is so embarrassing... but also not bad at all."),
        ]
        _sp_gf_asker_first_lines = [
            _("I had to know what my boyfriend was hiding! No regrets."),
            _("I dared my own boyfriend to show everyone. And... wow."),
        ]

        # Girl with NPC boyfriend present — uncomfortable, or hiding familiarity
        _sp_bf_here_first_lines = [
            _("I... that's, um, unexpected."),
            _("Oh. That's... interesting. I guess."),
            _("I shouldn't be staring at that."),
        ]
        _sp_bf_here_seen_lines = [
            _("Oh. Yeah. Surprising. Very surprising."),
            _("Hm. That's... I wouldn't know anything about that."),
            _("I mean... it's just a dare. Nothing special."),
        ]

        _h_npc_sp = getattr(store, "_h_npc", None)
        for _pi, _pg in enumerate(girls):
            if _pg:
                _is_asker_sp = asker is not None and _pg.gid == asker.gid
                _seen_before = _sp_has_seen.get(_pg.gid, False)
                _is_player_gf = hasattr(_pg, "is_dating_player") and _pg.is_dating_player()
                _bf_here_sp = (_h_npc_sp is not None and _npc_is_active()
                               and hasattr(_pg, "has_npc_partner") and _pg.has_npc_partner()
                               and _bf_is_gf(_h_npc_sp, _pg))

                # Priority 1: Player's GF
                if _is_player_gf and _is_asker_sp and _seen_before:
                    set_scene_expression(_pg, "smug")
                    Say_Line(_pg, renpy.random.choice(_sp_gf_asker_seen_lines))
                elif _is_player_gf and _is_asker_sp:
                    set_scene_expression(_pg, "smug", blush="1")
                    Say_Line(_pg, renpy.random.choice(_sp_gf_asker_first_lines))
                elif _is_player_gf and _seen_before:
                    set_scene_expression(_pg, "smug")
                    Say_Line(_pg, renpy.random.choice(_sp_gf_seen_lines))
                elif _is_player_gf:
                    set_scene_expression(_pg, "surprised", blush="2")
                    Say_Line(_pg, renpy.random.choice(_sp_gf_first_lines))

                # Priority 2: Girl whose NPC BF is watching
                elif _bf_here_sp and _seen_before:
                    set_scene_expression(_pg, "looking_left")
                    Say_Line(_pg, renpy.random.choice(_sp_bf_here_seen_lines))
                elif _bf_here_sp:
                    set_scene_expression(_pg, "looking_left", blush="1")
                    Say_Line(_pg, renpy.random.choice(_sp_bf_here_first_lines))

                # Priority 3: Generic — asker/seen/first time
                elif _is_asker_sp and _seen_before:
                    set_scene_expression(_pg, "smug")
                    Say_Line(_pg, renpy.random.choice(_sp_asker_seen_lines))
                elif _is_asker_sp:
                    set_scene_expression(_pg, "smug", blush=_sp_blush)
                    Say_Line(_pg, renpy.random.choice(_sp_asker_pool))
                elif _seen_before:
                    set_scene_expression(_pg, "smirk")
                    Say_Line(_pg, renpy.random.choice(_sp_seen_lines))
                else:
                    _pp = _sp_pools[min(_pi, len(_sp_pools) - 1)]
                    if _sp_blush:
                        set_scene_expression(_pg, "surprised", blush=_sp_blush)
                    else:
                        set_scene_expression(_pg, "surprised")
                    Say_Line(_pg, renpy.random.choice(_pp))
                Change_Status(_pg, "Inbt", _sp_inbt)

    # Trait-based extra reactions
    python:
        _sp_hc_lines = [
            _("Keep it out a little longer. I want a better look."),
            _("Mm. I could work with that."),
            _("Not bad. I'd like to see it in action."),
            _("Nice. Don't be shy now."),
            _("I appreciate a man who's not afraid to show off."),
            _("That's brave. I like brave."),
        ]
        _sp_cute_lines = [
            _("Oh gosh... okay, I'm looking away now!"),
            _("I can't believe I just saw that..."),
            _("My face is so red right now..."),
            _("Please put it away! I'm dying over here!"),
            _("I... I wasn't ready for that!"),
            _("Why am I so flustered right now..."),
        ]
        _sp_asker_hc_lines = [
            _("Best dare I've ever given, honestly."),
            _("See? This is why I love this game."),
            _("I knew asking would be worth it."),
        ]
        _sp_asker_cute_lines = [
            _("Okay, it's... bigger than I expected. But I'm not looking away."),
            _("I dared you, so I'm owning it. Even if my face is red."),
            _("I asked for it, and I got it... and I'm not complaining."),
        ]
        _sp_hc_seen_lines = [
            _("Oh, I know that one well. Trust me, it performs."),
            _("I've had hands-on experience. Still love the view."),
            _("Nothing I haven't enjoyed up close already."),
        ]
        _sp_cute_seen_lines = [
            _("I've seen it before, but it still makes me blush..."),
            _("I already know what's there, but... I can't help looking away."),
            _("I've seen it! But it's still embarrassing in front of everyone..."),
        ]
        _h_npc_tr = getattr(store, "_h_npc", None)
        for _pg in girls:
            if _pg and hasattr(_pg, "has_trait"):
                _is_asker = asker is not None and _pg.gid == asker.gid
                _seen_before = _sp_has_seen.get(_pg.gid, False)
                _bf_here_tr = (_h_npc_tr is not None and _npc_is_active()
                               and hasattr(_pg, "has_npc_partner") and _pg.has_npc_partner()
                               and _bf_is_gf(_h_npc_tr, _pg))
                if _pg.has_trait("hardcore_sex"):
                    set_scene_expression(_pg, "smirk")
                    if _seen_before and not _bf_here_tr:
                        Say_Line(_pg, renpy.random.choice(_sp_hc_seen_lines))
                    elif not _seen_before:
                        Say_Line(_pg, renpy.random.choice(_sp_asker_hc_lines if _is_asker else _sp_hc_lines))
                elif _pg.has_trait("cute_sex"):
                    set_scene_expression(_pg, "embarrassed", blush="2")
                    if _seen_before and not _bf_here_tr:
                        Say_Line(_pg, renpy.random.choice(_sp_cute_seen_lines))
                    elif not _seen_before:
                        Say_Line(_pg, renpy.random.choice(_sp_asker_cute_lines if _is_asker else _sp_cute_lines))

    # GF suspicion: she notices another girl wasn't surprised
    python:
        _gf_sp = _hangout_find_gf()
        _sp_suspicious_target = None
        if _gf_sp:
            for _pg in girls:
                if _pg and _pg.gid != _gf_sp.gid and _sp_has_seen.get(_pg.gid, False):
                    if not girl_knows_with_player(_gf_sp, _pg):
                        _sp_suspicious_target = _pg
                        break
        if _sp_suspicious_target:
            set_scene_expression(_gf_sp, "serious")
            _sp_susp_line = renpy.random.choice([
                _("Wait... how come %(name)s wasn't even surprised?"),
                _("Hold on. %(name)s looked way too calm about that."),
                _("%(name)s didn't flinch at all. Should I be worried?"),
                _("Why does %(name)s look like she's already seen it?"),
            ]) % {"name": _sp_suspicious_target.Name}
            Say_Line(_gf_sp, _sp_susp_line)
            print("[TOD-SHOW-PENIS] GF %s suspicious of %s" % (_gf_sp.gid, _sp_suspicious_target.gid))

    $ Narration(_("You pull your pants back up."))
    return


# ============================================================
# PLAYER LEWD DARES
# ============================================================

# --- Player Kiss (target girl) ---
label tod_pdare_kiss(girl):
    $ _gn = girl.Name
    $ set_girl_sprite(girl.gid, pose="standing", zorder=10)
    python:
        _has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _bf_here = _has_bf and _npc_is_active() and _bf_is_gf(store._h_npc, girl)
        _is_cute = hasattr(girl, "has_trait") and girl.has_trait("cute_sex")
        _is_hardcore = hasattr(girl, "has_trait") and girl.has_trait("hardcore_sex")
        _is_gf = hasattr(girl, "is_dating_player") and girl.is_dating_player()

    # Approach
    $ Say_Player(renpy.random.choice([
        _("Alright, [_gn]. Come here."),
        _("A dare's a dare. Ready?"),
        _("Don't make it weird..."),
    ]))

    if _is_gf:
        $ set_scene_expression(girl, "smirk", blush="1")
        $ Say_Line(girl, renpy.random.choice([
            _("Kissing my own boyfriend? That's not even a real dare."),
            _("Come here, babe. This one's easy."),
            _("Finally, a dare I actually want to do."),
        ]))
    elif _bf_here:
        $ set_scene_expression(girl, "looking_left", blush="1")
        $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice([
            _("You're really making me do this in front of %(po)s..."),
            _("%(Pp)s is right there... one quick kiss. That's it."),
            _("Sorry, %(pl)s... it's just a dare. Please don't be mad."),
        ])))
    elif _has_bf:
        $ set_scene_expression(girl, "looking_left", blush="1")
        $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice([
            _("I have %(pl)s, you know... but fine. It's just a dare."),
            _("This means nothing. %(Pp)s would kill you if %(pp)s knew."),
            _("One quick kiss. That's it. I'm taken, remember?"),
        ])))
    elif _is_cute:
        $ set_scene_expression(girl, "shy", blush="1")
        $ Say_Line(girl, renpy.random.choice([
            _("W-wait, already? I'm not ready..."),
            _("Close your eyes first... please..."),
            _("My heart is pounding so fast right now..."),
        ]))
    elif _is_hardcore:
        $ set_scene_expression(girl, "smirk")
        $ Say_Line(girl, renpy.random.choice([
            _("Come on then. Don't be gentle."),
            _("Finally, something interesting. Get over here."),
            _("Make it a good one or don't bother."),
        ]))
    else:
        $ set_scene_expression(girl, "looking_left")
        $ Say_Line(girl, renpy.random.choice([
            _("Okay... just a quick one."),
            _("Fine. But don't get any ideas."),
            _("Alright, let's do this before I change my mind."),
        ]))

    call KISS_Launch(girl) from _call_KISS_Launch_pdare
    $ Narration(_("You lean in. Your lips meet hers."))
    call KISS_Smooch(girl) from _call_KISS_Smooch_pdare
    # intimacy/Sex_acts/cheat registration happens once, in tod_register_cheat_act below
    $ girl.set_flag("tod_kiss_done", True)
    $ Narration(_("The kiss is brief but electric."))
    call KISS_End(girl) from _call_KISS_End_pdare
    $ set_girl_sprite(girl.gid, pose="standing", at_list=[_hangout_pos_for(girl)], zorder=0)

    # Reaction
    if _is_gf:
        $ set_scene_expression(girl, "smirk", blush="1")
        $ Say_Line(girl, renpy.random.choice([
            _("Mm. I could do that all day."),
            _("See? That's how a real kiss feels."),
            _("I don't need a dare to kiss you, babe."),
        ]))
    elif _is_cute:
        $ set_scene_expression(girl, "embarrassed", blush="2")
        $ Say_Line(girl, renpy.random.choice([
            _("That was... um... okay, moving on!"),
            _("My face is burning... don't look at me!"),
            _("I... I need a second..."),
        ]))
    elif _is_hardcore:
        $ set_scene_expression(girl, "smirk")
        $ Say_Line(girl, renpy.random.choice([
            _("Not bad. Could've been longer, though."),
            _("Mm. You're a decent kisser."),
            _("That's it? I expected more fire."),
        ]))
    else:
        $ set_scene_expression(girl, "looking_left")
        $ Say_Line(girl, renpy.random.choice([
            _("...Okay. That happened. Moving on."),
            _("That wasn't as weird as I thought it'd be."),
            _("Don't let it go to your head."),
        ]))

    python:
        Change_Status(girl, "Love", 15)
        Change_Status(girl, "Inbt", 10)
        tod_register_cheat_act(girl, "kiss")

    # GF watches player kiss another girl
    python:
        _kiss_gf_w = _hangout_find_gf()
        _kiss_gf_watching = _kiss_gf_w is not None and _kiss_gf_w.gid != girl.gid
    if _kiss_gf_watching:
        if store._hangout_is_harem_night:
            $ set_scene_expression(_kiss_gf_w, "sly")
            $ Say_Line(_kiss_gf_w, _tl(renpy.random.choice(_HAREM_GF_TEASE_LINES)))
        else:
            python:
                Change_Status(_kiss_gf_w, "Love", -10)
                Change_Status(_kiss_gf_w, "Obed", 5)
            $ set_scene_expression(_kiss_gf_w, "serious")
            $ Say_Line(_kiss_gf_w, renpy.random.choice([
                _("You just kissed another girl. In front of me."),
                _("I'm sitting right here, you know."),
                _("'Just a dare,' right? Sure looked like more than that."),
                _("Cool. Great. Love that for me."),
            ]))

    call _tod_npc_react_dare(girl, 4) from _call_npc_react_pdare_kiss
    return


# --- Player Spank (target girl) ---
label tod_pdare_spank(girl):
    $ _gn = girl.Name
    python:
        _has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _bf_here = _has_bf and _npc_is_active() and _bf_is_gf(store._h_npc, girl)
        _is_cute = hasattr(girl, "has_trait") and girl.has_trait("cute_sex")
        _is_hardcore = hasattr(girl, "has_trait") and girl.has_trait("hardcore_sex")
        _is_gf = hasattr(girl, "is_dating_player") and girl.is_dating_player()

    if _is_gf:
        $ set_scene_expression(girl, "smirk", blush="1")
        $ Say_Line(girl, renpy.random.choice([
            _("Spanking your own girlfriend in front of everyone? You're bold."),
            _("Go ahead, babe. I know you've been wanting to."),
            _("My boyfriend is spanking me as a dare. This is my life now."),
        ]))
    elif _bf_here:
        $ set_scene_expression(girl, "looking_left", blush="1")
        $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice([
            _("%(Pp)s is literally right there... this is so embarrassing."),
            _("This is so wrong... but it's just a dare, right?"),
            _("I'm sorry, %(pl)s... don't look at me like that."),
        ])))
    elif _has_bf:
        $ set_scene_expression(girl, "looking_left", blush="1")
        $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice([
            _("%(Pp)s would lose %(poss)s mind if %(pp)s saw this..."),
            _("Fine. But if %(pl)s asks, this never happened."),
        ])))
    else:
        $ set_scene_expression(girl, "looking_right")
        $ Say_Line(girl, renpy.random.choice([
            _("You want to slap MY ass? Bold move."),
            _("One slap. That's it. Don't get carried away."),
            _("Fine. But I'm slapping you back if you go too hard."),
        ]))

    # Girl goes to rear pose (RCG or LD) -- hide other girls so they don't overlap
    python:
        _spank_slot = _hangout_pos_for(girl)
        _spank_pose = _rear_pose_for(girl)
        _spank_others = _tod_other_girls(girl)
        for _so in _spank_others:
            renpy.hide(_so.gid)
    python:
        print("[SPANK_DEBUG] pdare_spank: gid=%s pose=%s clothes=%s clothes_state=%s" % (girl.gid, _spank_pose, str(girl.clothes), str(girl.clothes_state)))
        if _spank_pose == "reverse_cowgirl":
            _dbg_attrs = _build_rcg_attributes(girl)
            print("[SPANK_DEBUG] pdare_spank: rcg_attrs=%s" % str(_dbg_attrs))
    if _spank_pose == "laying_down":
        $ _ld_show_rear_preview(girl)
    else:
        $ set_girl_sprite(girl.gid, pose=_spank_pose, at_list=[slot_center])
    python:
        _dbg_showing = []
        _dbg_match = girl.gid
        for _dtag in renpy.get_showing_tags("master"):
            _dtag_str = str(_dtag)
            if _dbg_match in _dtag_str or "rcg" in _dtag_str or "laying" in _dtag_str:
                _dbg_showing.append(_dtag_str)
        print("[SPANK_DEBUG] pdare_spank: showing_tags=%s" % str(_dbg_showing))
    $ Narration(_("[_gn] bends over."))
    $ Say_Player(_("Here goes..."))
    $ slap_crack()   # the shared crack (SubEvents.rpy): this dare landed mute until 2026-10-10
    call Punch from _call_Punch_pdare_spank

    if _spank_pose == "laying_down":
        $ _hide_scene_layers("laying_down")

    if _is_gf:
        $ set_scene_expression(girl, "smirk", blush="1")
        $ Say_Line(girl, renpy.random.choice([
            _("You enjoyed that way too much, babe."),
            _("Not bad. But I know you can do better."),
            _("That's what I get for dating you, I guess."),
        ]))
    elif _is_hardcore:
        $ set_scene_expression(girl, "smirk")
        $ Say_Line(girl, renpy.random.choice([
            _("Harder next time."),
            _("That's all you've got? Come on."),
            _("Mm... not bad. Do it again."),
        ]))
    elif _is_cute:
        $ set_scene_expression(girl, "embarrassed", blush="1")
        $ Say_Line(girl, renpy.random.choice([
            _("OW! That hurt!"),
            _("Ahh! You didn't have to hit so hard!"),
            _("That stings! You're mean..."),
        ]))
    else:
        $ set_scene_expression(girl, "looking_left")
        $ Say_Line(girl, renpy.random.choice([
            _("Hey! Watch the force!"),
            _("Okay, okay, dare completed! Hands off!"),
            _("My butt is going to be red for hours..."),
        ]))

    python:
        Change_Status(girl, "Obed", 15)
        Change_Status(girl, "Inbt", 10)
        tod_register_cheat_act(girl, "touch")
        # her spank record (spank_note): the smirking answers above (girlfriend, hardcore) enjoyed it, the others complain
        spank_note(girl, _is_gf or _is_hardcore, "tod_player_dare")

    # Return to standing and restore other girls
    $ set_girl_sprite(girl.gid, pose="standing", at_list=[_spank_slot])
    python:
        for _so in _spank_others:
            set_girl_sprite(_so.gid, pose="standing", at_list=[_hangout_pos_for(_so)])

    # GF watches player spank another girl
    python:
        _spk_gf_w = _hangout_find_gf()
        _spk_gf_watching = _spk_gf_w is not None and _spk_gf_w.gid != girl.gid
    if _spk_gf_watching:
        if store._hangout_is_harem_night:
            $ set_scene_expression(_spk_gf_w, "sly")
            $ Say_Line(_spk_gf_w, _tl(renpy.random.choice(_HAREM_GF_TEASE_LINES)))
        else:
            python:
                Change_Status(_spk_gf_w, "Love", -10)
                Change_Status(_spk_gf_w, "Obed", 5)
            $ set_scene_expression(_spk_gf_w, "serious")
            $ Say_Line(_spk_gf_w, renpy.random.choice([
                _("You just slapped her ass. Right in front of me."),
                _("Oh, smacking other girls now? Having fun?"),
                _("I saw that, you know. I'm RIGHT here."),
            ]))

    call _tod_npc_react_dare(girl, 5) from _call_npc_react_pdare_spank
    return


# --- Player Kiss Boobs (target girl) ---
label tod_pdare_kiss_boobs(girl):
    $ _gn = girl.Name
    $ set_girl_sprite(girl.gid, pose="standing", zorder=10)
    python:
        _has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _bf_here = _has_bf and _npc_is_active() and _bf_is_gf(store._h_npc, girl)
        _is_cute = hasattr(girl, "has_trait") and girl.has_trait("cute_sex")
        _is_hardcore = hasattr(girl, "has_trait") and girl.has_trait("hardcore_sex")
        _is_gf = hasattr(girl, "is_dating_player") and girl.is_dating_player()

    if _is_gf:
        $ set_scene_expression(girl, "smirk", blush="1")
        $ Say_Line(girl, renpy.random.choice([
            _("Kissing your girlfriend's boobs in front of everyone? Bold."),
            _("You already do this at home. But fine, show them how it's done."),
            _("Nothing you haven't done before... just with an audience this time."),
        ]))
    elif _bf_here:
        $ set_scene_expression(girl, "looking_left", blush="2")
        $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice([
            _("This is way beyond 'just a dare'... and %(pp)s is watching..."),
            _("%(Pp)s is right there and you want to kiss my boobs? God..."),
            _("I can't believe I'm letting you do this with %(po)s sitting right there."),
        ])))
    elif _has_bf:
        $ set_scene_expression(girl, "looking_left", blush="1")
        $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice([
            _("This is way beyond 'just a dare'... but fine."),
            _("If %(pl)s ever finds out about this..."),
            _("I can't believe I'm letting you do this. A dare is a dare, I guess."),
        ])))
    elif _is_cute:
        $ set_scene_expression(girl, "shy", blush="2")
        $ Say_Line(girl, renpy.random.choice([
            _("Y-you're really going to... okay, don't stare too much..."),
            _("I'm so embarrassed right now... just be gentle."),
            _("Promise you'll be quick about it..."),
        ]))
    elif _is_hardcore:
        $ set_scene_expression(girl, "smirk")
        $ Say_Line(girl, renpy.random.choice([
            _("Go ahead. I don't mind."),
            _("Take your time. I'm not shy."),
            _("Show me what you've got, big boy."),
        ]))
    else:
        $ set_scene_expression(girl, "embarrassed", blush="1")
        $ Say_Line(girl, renpy.random.choice([
            _("Okay, but make it quick. This is embarrassing enough."),
            _("Fine... but if you drool, we're done."),
            _("Just... be respectful about it, okay?"),
        ]))

    $ girl.Outfit_Change(over="none", mid="none", chest_up=True, refresh=False)
    $ set_girl_sprite(girl.gid, pose="standing", at_list=[_hangout_pos_for(girl)])
    $ girl.RegisterAction("player_saw_boobs")
    $ Narration(_("[_gn] lifts her top. You lean in and press your lips gently against her skin."))
    pause 1.0

    if _is_gf:
        $ set_scene_expression(girl, "pleasure", blush="1")
        $ Say_Line(girl, renpy.random.choice([
            _("You took your time with that, babe..."),
            _("Same as always. Except with people watching."),
            _("Nothing new for us. But the audience is new."),
        ]))
    elif _is_cute:
        $ set_scene_expression(girl, "embarrassed", blush="2")
        $ Say_Line(girl, renpy.random.choice([
            _("O-okay, that's enough! Stop!"),
            _("Your lips are so warm... I mean, stop that!"),
            _("I'm going to faint..."),
        ]))
    elif _is_hardcore:
        $ set_scene_expression(girl, "smirk", blush="1")
        $ Say_Line(girl, renpy.random.choice([
            _("Mm, you can keep going if you want."),
            _("Not bad. You've got soft lips."),
            _("That tickles... in a good way."),
        ]))
    else:
        $ set_scene_expression(girl, "shy", blush="1")
        $ Say_Line(girl, renpy.random.choice([
            _("Okay... that's enough. Dare completed."),
            _("Your lips are warm... anyway, moving on!"),
            _("That was... not as bad as I thought."),
        ]))

    python:
        Change_Status(girl, "Inbt", 20)
        Change_Status(girl, "Love", 15)
        tod_register_cheat_act(girl, "touch")

    # GF watches player kiss another girl's boobs
    python:
        _kb_gf_w = _hangout_find_gf()
        _kb_gf_watching = _kb_gf_w is not None and _kb_gf_w.gid != girl.gid
    if _kb_gf_watching:
        if store._hangout_is_harem_night:
            $ set_scene_expression(_kb_gf_w, "sly")
            $ Say_Line(_kb_gf_w, _tl(renpy.random.choice(_HAREM_GF_TEASE_LINES)))
        else:
            python:
                Change_Status(_kb_gf_w, "Love", -15)
                Change_Status(_kb_gf_w, "Obed", 5)
            $ set_scene_expression(_kb_gf_w, "serious")
            $ Say_Line(_kb_gf_w, renpy.random.choice([
                _("You're kissing HER boobs? In front of me?"),
                _("That was way more than 'just a dare.' I saw how long that lasted."),
                _("So that's how it is? Right in front of your girlfriend?"),
            ]))

    $ set_girl_sprite(girl.gid, pose="standing", zorder=0)
    call _tod_npc_react_dare(girl, 5) from _call_npc_react_pdare_kboobs
    return


# --- Player Dare: Girl sits on lap (difficulty 3-4) ---
label tod_pdare_lap(girl):
    $ _gn = girl.Name
    $ set_girl_sprite(girl.gid, pose="standing", zorder=10)
    python:
        _has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _bf_here = _has_bf and _npc_is_active() and _bf_is_gf(store._h_npc, girl)
        _is_cute = hasattr(girl, "has_trait") and girl.has_trait("cute_sex")
        _is_hardcore = hasattr(girl, "has_trait") and girl.has_trait("hardcore_sex")
        _is_gf = hasattr(girl, "is_dating_player") and girl.is_dating_player()

    if _is_gf:
        $ set_scene_expression(girl, "happy")
        $ Say_Line(girl, renpy.random.choice([
            _("Sitting on my boyfriend's lap? This isn't even a dare."),
            _("I do this every day. Make room, babe."),
            _("Finally, an easy one. Move over."),
        ]))
    elif _bf_here:
        $ set_scene_expression(girl, "looking_left", blush="1")
        $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice([
            _("On your lap... with %(po)s watching? This is so awkward..."),
            _("%(Pp)s is right there... but it's just a dare, right?"),
        ])))
    elif _has_bf:
        $ set_scene_expression(girl, "looking_left", blush="1")
        $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice([
            _("Did you accept it? That's... %(pl)s would kill me. But fine."),
            _("This is so wrong... but it's just a dare, right?"),
        ])))
    elif _is_cute:
        $ set_scene_expression(girl, "shy", blush="1")
        $ Say_Line(girl, renpy.random.choice([
            _("O-on your lap? That's so embarrassing..."),
            _("I'm going to be so close to you... okay, fine..."),
        ]))
    elif _is_hardcore:
        $ set_scene_expression(girl, "smirk")
        $ Say_Line(girl, renpy.random.choice([
            _("Your lap? Easy. Don't get too excited."),
            _("Sure. Hope you can handle it."),
        ]))
    else:
        $ set_scene_expression(girl, "looking_left")
        $ Say_Line(girl, renpy.random.choice([
            _("Okay... but don't make it weird."),
            _("Fine, but keep your hands to yourself."),
            _("Alright, scoot over."),
        ]))

    python:
        _lap_slot = _hangout_pos_for(girl)
        _lap_pose = _rear_pose_for(girl)
        _prev_sprite_loc = getattr(girl, "SpriteLoc", StageCenter)
        girl.SpriteLoc = 0.51
    python:
        print("[TOD_LAP] showing %s as %s — Over=%s Chest=%s Panties=%s clothes=%s clothes_state=%s" % (
            girl.gid, _lap_pose, getattr(girl, "Over", None), getattr(girl, "Chest", None),
            getattr(girl, "Panties", None), str(girl.clothes), str(girl.clothes_state)))
    if _lap_pose == "laying_down":
        $ _ld_show_rear_preview(girl)
    else:
        $ set_girl_sprite(girl.gid, pose=_lap_pose, at_list=[slot_center], zorder=100)
    $ Narration(_("[_gn] walks over and sits down on your lap. You can feel her warmth against you."))
    pause 1.0

    if _lap_pose == "laying_down":
        $ _hide_scene_layers("laying_down")

    if _is_gf:
        $ set_scene_expression(girl, "happy")
        $ Say_Line(girl, renpy.random.choice([
            _("See? This is MY spot."),
            _("I could stay here all night."),
            _("This is just a regular day for us."),
        ]))
    elif _is_cute:
        $ set_scene_expression(girl, "shy", blush="1")
        $ Say_Line(girl, renpy.random.choice([
            _("This is... actually kind of comfortable."),
            _("Your legs are warm... don't say anything."),
            _("I can feel your heartbeat... or is that mine?"),
        ]))
    elif _is_hardcore:
        $ set_scene_expression(girl, "smirk")
        $ Say_Line(girl, renpy.random.choice([
            _("Not bad. I could get used to this."),
            _("Comfortable. Very comfortable."),
            _("Don't get any ideas... unless you want to."),
        ]))
    else:
        $ set_scene_expression(girl, "looking_left")
        $ Say_Line(girl, renpy.random.choice([
            _("There. Happy? I'm on your lap."),
            _("This is actually not as awkward as I thought."),
            _("Okay, this is nice. I'll admit it."),
        ]))

    python:
        Change_Status(girl, "Love", 15)
        Change_Status(girl, "Inbt", 10)
        tod_register_cheat_act(girl, "touch")
        girl.SpriteLoc = _prev_sprite_loc

    $ set_girl_sprite(girl.gid, pose="standing", at_list=[_lap_slot], zorder=0)

    # GF watches another girl sit on player's lap
    python:
        _lap_gf_w = _hangout_find_gf()
        _lap_gf_watching = _lap_gf_w is not None and _lap_gf_w.gid != girl.gid
    if _lap_gf_watching:
        if store._hangout_is_harem_night:
            $ set_scene_expression(_lap_gf_w, "sly")
            $ Say_Line(_lap_gf_w, _tl(renpy.random.choice(_HAREM_GF_TEASE_LINES)))
        else:
            python:
                Change_Status(_lap_gf_w, "Love", -5)
                Change_Status(_lap_gf_w, "Obed", 5)
            $ set_scene_expression(_lap_gf_w, "looking_left")
            $ Say_Line(_lap_gf_w, renpy.random.choice([
                _("She's sitting on YOUR lap? While I'm right here?"),
                _("Oh, just make yourself comfortable, why don't you."),
                _("That's my spot, by the way. Just so everyone knows."),
            ]))

    call _tod_npc_react_dare(girl, 3) from _call_npc_react_pdare_lap
    return


# ============================================================
# GIRL DARE: Sit on player's lap (difficulty 3)
# ============================================================
label tod_dare_sit_lap(girl):
    $ _gn = girl.Name
    $ set_girl_sprite(girl.gid, pose="standing", zorder=10)
    python:
        _is_cute = hasattr(girl, "has_trait") and girl.has_trait("cute_sex")
        _is_hardcore = hasattr(girl, "has_trait") and girl.has_trait("hardcore_sex")
        _is_gf = hasattr(girl, "is_dating_player") and girl.is_dating_player()
        _has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _bf_here = _has_bf and _npc_is_active() and _bf_is_gf(store._h_npc, girl)
        _lap_slot = _hangout_pos_for(girl)
        _lap_pose = _rear_pose_for(girl)
        _prev_sprite_loc = getattr(girl, "SpriteLoc", StageCenter)
        girl.SpriteLoc = 0.51

    if store._hangout_is_harem_night:
        $ set_scene_expression(girl, "smirk")
        $ Say_Line(girl, renpy.random.choice([
            _("With pleasure, babe. Move over~"),
            _("Finally, a dare I actually want to do."),
            _("Gladly. Hope you don't mind an audience."),
        ]))
    elif _is_gf:
        $ set_scene_expression(girl, "happy")
        $ Say_Line(girl, renpy.random.choice([
            _("My boyfriend's lap? That's my favorite seat."),
            _("Gladly. Make room, babe."),
            _("This is the easiest dare ever."),
        ]))
    elif _bf_here:
        $ set_scene_expression(girl, "looking_left", blush="1")
        $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice([
            _("On his lap... with %(po)s watching? This is awkward..."),
            _("%(Pp)s is right there... it's just a dare, okay?"),
        ])))
    else:
        $ set_scene_expression(girl, "looking_left")
        $ Say_Line(girl, renpy.random.choice([
            _("Sit on your lap? ...Okay. It's just a dare."),
            _("Fine. But I'm only doing this because I was dared."),
            _("Alright, make room."),
        ]))

    python:
        print("[TOD_LAP] showing %s as %s — Over=%s Chest=%s Panties=%s clothes=%s clothes_state=%s" % (
            girl.gid, _lap_pose, getattr(girl, "Over", None), getattr(girl, "Chest", None),
            getattr(girl, "Panties", None), str(girl.clothes), str(girl.clothes_state)))
    if _lap_pose == "laying_down":
        $ _ld_show_rear_preview(girl)
    else:
        $ set_girl_sprite(girl.gid, pose=_lap_pose, at_list=[slot_center], zorder=100)
    $ Narration(_("[_gn] gets up and settles herself on your lap."))
    pause 1.0

    if _lap_pose == "laying_down":
        $ _hide_scene_layers("laying_down")

    if store._hangout_is_harem_night:
        $ set_scene_expression(girl, "pleasure", blush="1")
        $ Say_Line(girl, renpy.random.choice([
            _("Mm, this is my favorite seat~"),
            _("I could get used to this."),
            _("Don't get too excited, she's watching~"),
        ]))
    elif _is_gf:
        $ set_scene_expression(girl, "happy")
        $ Say_Line(girl, renpy.random.choice([
            _("See? This is where I belong."),
            _("Just like at home. Except with witnesses."),
            _("I could stay here all night, babe."),
        ]))
    elif _bf_here:
        $ set_scene_expression(girl, "looking_left", blush="1")
        $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice([
            _("Don't look at me like that, %(pl)s... it's just a dare."),
            _("It doesn't mean anything, %(pn)s. Relax."),
        ])))
    elif _is_cute:
        $ set_scene_expression(girl, "shy", blush="1")
        $ Say_Line(girl, renpy.random.choice([
            _("You're warm... I mean, this is fine. This is fine."),
            _("My heart is racing... don't tell anyone."),
        ]))
    elif _is_hardcore:
        $ set_scene_expression(girl, "smirk")
        $ Say_Line(girl, renpy.random.choice([
            _("Mm. Comfortable. I might stay here."),
            _("You're lucky I'm in a good mood tonight."),
        ]))
    else:
        $ set_scene_expression(girl, "looking_left")
        $ Say_Line(girl, renpy.random.choice([
            _("There. Dare completed. ...I'll get up in a second."),
            _("This is actually kind of nice. Shut up."),
        ]))

    python:
        Change_Status(girl, "Love", 15)
        Change_Status(girl, "Inbt", 10)
        Change_Status(girl, "Obed", 5)
        tod_register_cheat_act(girl, "touch")
        girl.SpriteLoc = _prev_sprite_loc

    # Return to standing
    $ set_girl_sprite(girl.gid, pose="standing", at_list=[_lap_slot], zorder=0)
    return


# ============================================================
# SAFE DARES
# ============================================================

# --- Silly Face (difficulty 1) ---
label tod_dare_silly_face(girl):
    $ _gn = girl.Name
    $ set_scene_expression(girl, "happy")
    $ Narration(_("[_gn] looks up, crosses her eyes, and sticks her tongue out."))
    $ set_scene_expression(girl, "laugh")
    $ Say_Line(girl, renpy.random.choice([_("Bleeeh!"), _("How's this? Sexy enough?"), _("I look like a complete idiot right now.")]))
    python:
        for _other in _tod_other_girls(girl):
            set_scene_expression(_other, "laugh")
    python:
        _reactions = [
            _("That face is going to haunt my dreams."),
            _("Beautiful. Truly. A masterpiece."),
            _("I think I just lost brain cells looking at that."),
        ]
        Narration(renpy.random.choice(_reactions))
        Change_Status(girl, "Inbt", 10)
    return


# --- Sing a Song (difficulty 2) ---
label tod_dare_sing_song(girl):
    $ _gn = girl.Name
    $ Narration(_("[_gn] clears her throat and starts singing."))
    $ set_scene_expression(girl, "embarrassed", blush=1)
    $ Say_Line(girl, renpy.random.choice([_("Okay, don't laugh..."), _("I'm warning you, this won't be pretty."), _("Here goes nothing...")]))
    python:
        _songs = [
            _("[_gn] belts out a pop song completely off-key. It's painful. And hilarious."),
            _("[_gn] attempts a ballad. She forgets the words halfway through and just hums loudly."),
            _("[_gn] sings a nursery rhyme with way too much emotion. Oscar-worthy performance."),
        ]
        Narration(renpy.random.choice(_songs))
        for _other in _tod_other_girls(girl):
            set_scene_expression(_other, "laugh")
    $ set_scene_expression(girl, "shy", blush=1)
    $ Say_Line(girl, renpy.random.choice([_("I told you it would be bad!"), _("Thank you, thank you. No autographs."), _("We never speak of this again.")]))
    $ Change_Status(girl, "Inbt", 10)
    return


# --- Show Flashgram (difficulty 2) ---
label tod_dare_show_flashgram(girl):
    $ _gn = girl.Name
    $ set_scene_expression(girl, "looking_left")
    $ Narration(_("[_gn] pulls out her phone and opens her Flashgram page."))
    python:
        _content = renpy.random.choice(["muscles", "drawings", "memes"])

    if _content == "muscles":
        $ set_scene_expression(girl, "embarrassed", blush=1)
        $ Narration(_("Her feed is full of muscular men posing in tight shirts."))
        $ Say_Player(_("That's... a lot of abs."))
        $ set_scene_expression(girl, "looking_right", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("What? I appreciate the male form."), _("Don't judge me. They're fitness influencers."), _("A girl can look, can't she?")]))
    elif _content == "drawings":
        $ Narration(_("Her feed is full of detailed drawings and art tutorials."))
        $ Say_Player(_("Oh wow, you're into art?"))
        $ set_scene_expression(girl, "happy")
        $ Say_Line(girl, renpy.random.choice([_("Yeah, I follow a bunch of artists. Their work is amazing."), _("I wish I could draw like that."), _("It's relaxing to scroll through, okay?")]))
    else:
        $ set_scene_expression(girl, "smirk")
        $ Narration(_("Her feed is nothing but memes. Page after page of memes."))
        $ Say_Player(_("That's... your entire feed?"))
        $ set_scene_expression(girl, "sly")
        $ Say_Line(girl, renpy.random.choice([_("Memes are the only thing keeping me sane."), _("I'm a woman of culture."), _("What else would I follow? News? Gross.")]))

    $ Change_Status(girl, "Inbt", 5)
    return


# --- Chicken Impression (difficulty 2) ---
label tod_dare_chicken(girl):
    $ _gn = girl.Name
    $ set_scene_expression(girl, "embarrassed", blush=1)
    $ Narration(_("[_gn] stands up, tucks her hands under her armpits, and starts clucking."))
    $ set_scene_expression(girl, "laugh")
    $ Say_Line(girl, _("Bawk bawk bawk!"))
    python:
        _reactions = [
            _("[_gn] flaps her arms and struts around. It's disturbingly accurate."),
            _("She commits fully. Head bobbing, feet stomping. The whole thing."),
            _("For a moment, you genuinely believe she might be part chicken."),
        ]
        Narration(renpy.random.choice(_reactions))
        for _other in _tod_other_girls(girl):
            set_scene_expression(_other, "laugh")
    $ set_scene_expression(girl, "looking_left", blush=1)
    $ Say_Line(girl, renpy.random.choice([_("I can't believe I just did that."), _("My dignity is officially gone."), _("If anyone recorded that, I'm coming for you.")]))
    $ Change_Status(girl, "Inbt", 10)
    return


# --- Dance (difficulty 3) ---
label tod_dare_dance(girl):
    $ _gn = girl.Name
    $ set_scene_expression(girl, "shy", blush=1)
    $ Narration(_("[_gn] gets up and starts dancing."))
    python:
        _dances = [
            _("She moves with surprising confidence, swaying her hips to an imaginary beat."),
            _("She does a goofy little shimmy, throwing her hands in the air without a care."),
            _("She tries a sexy dance but keeps giggling, breaking character every few seconds."),
        ]
        _dance_pick = renpy.random.choice(_dances)
        Narration(_dance_pick)
        if "confidence" in _dance_pick or "sexy" in _dance_pick:
            set_scene_expression(girl, "smirk", blush=1)
        else:
            set_scene_expression(girl, "laugh")
    $ Say_Line(girl, renpy.random.choice([_("How was that?"), _("I'm way better with actual music, just saying."), _("Eat your heart out.")]))
    $ Change_Status(girl, "Inbt", 15)
    return


# ============================================================
# LEWD DARES
# ============================================================

# --- Flash Boobs (difficulty 3) ---
label tod_dare_flash_boobs(girl):
    $ _gn = girl.Name
    python:
        _fb_is_gf = hasattr(girl, "is_dating_player") and girl.is_dating_player()
        _fb_has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _fb_bf_here = _fb_has_bf and _npc_is_active() and _bf_is_gf(store._h_npc, girl)
    if store._hangout_is_harem_night:
        $ set_scene_expression(girl, "sly", blush=1)
        $ Narration(_("[_gn] smirks confidently."))
        $ Say_Line(girl, renpy.random.choice([_("You've both seen more than this already~"), _("Nothing new for you, right babe?"), _("Easy one. Watch and learn.")]))
    elif _fb_is_gf:
        $ set_scene_expression(girl, "smirk", blush=1)
        $ Narration(_("[_gn] shrugs casually."))
        $ Say_Line(girl, renpy.random.choice([_("Nothing you haven't seen a hundred times, babe."), _("This isn't even a challenge. You know what's under here."), _("For you? Sure. Everyone else, don't get used to it.")]))
    elif _fb_bf_here:
        $ set_scene_expression(girl, "embarrassed", blush=2)
        $ Narration(_("[_gn] glances nervously at her boyfriend."))
        $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice([_("Flashing in front of %(po)s... this is mortifying."), _("%(Pp)s is going to kill me... but a dare is a dare."), _("Don't look at me like that, %(pn)s... it's just a dare.")])))
    else:
        python:
            _fb_alc = hangout_get_alcohol(girl)
            _fb_bold = hasattr(girl, "has_trait") and girl.has_trait("hardcore_sex")
        if _fb_alc >= 7 or _fb_bold:
            $ set_scene_expression(girl, "smirk", blush=1)
            $ Narration(_("[_gn] grabs her top without hesitation."))
            $ Say_Line(girl, renpy.random.choice([_("Eyes up here after this."), _("Enjoy the show."), _("Don't say I never did anything for you.")]))
        elif _fb_alc >= 4:
            $ set_scene_expression(girl, "looking_left", blush=1)
            $ Narration(_("[_gn] takes a breath and laughs nervously."))
            $ Say_Line(girl, renpy.random.choice([_("The drinks are making this easier than it should be."), _("Blame the alcohol for this one."), _("Fine, fine... here goes.")]))
        else:
            $ set_scene_expression(girl, "embarrassed", blush=2)
            $ Narration(_("[_gn] takes a deep breath."))
            $ set_scene_expression(girl, "looking_down", blush=2)
            $ Say_Line(girl, renpy.random.choice([_("Okay... don't make it weird."), _("Just a quick peek. That's it."), _("If you stare too long, I'm slapping you.")]))
    $ _flash_saved_over = girl.clothes.get("over")
    $ _flash_saved_mid = girl.clothes.get("mid")
    $ girl.Outfit_Change(over="none", mid="none", chest_up=True, refresh=False)
    $ set_girl_sprite(girl.gid, pose="standing", at_list=[_hangout_pos_for(girl)])
    python:
        girl.RegisterAction("player_saw_boobs")
        for _watcher in _tod_other_girls(girl):
            if store._hangout_is_harem_night:
                set_scene_expression(_watcher, "sly", blush=1)
            else:
                set_scene_expression(_watcher, "surprised", blush=1)
    $ set_scene_expression(girl, "shy", blush=2)
    $ Narration(_("She lifts her top. For a brief moment, everything is right in the world."))
    pause 1.5
    if store._hangout_is_harem_night:
        $ set_scene_expression(girl, "smirk")
        $ Say_Line(girl, renpy.random.choice([_("Enjoy the view, babe~"), _("Your turn next."), _("See? No big deal.")]))
    else:
        python:
            _is_bold = hasattr(girl, "has_trait") and girl.has_trait("hardcore_sex")
        if _is_bold:
            $ set_scene_expression(girl, "smirk", blush=1)
        else:
            $ set_scene_expression(girl, "embarrassed", blush=2)
        $ Say_Line(girl, renpy.random.choice([_("Okay, show's over!"), _("Done! Stop staring!"), _("Happy now?")]))
    $ girl.Outfit_Change(over=_flash_saved_over, mid=_flash_saved_mid, chest_up=False, refresh=False)
    $ set_girl_sprite(girl.gid, pose="standing", at_list=[_hangout_pos_for(girl)])
    python:
        Change_Status(girl, "Inbt", 15)
        Change_Status(girl, "Obed", 10)
    return


# --- Strip All (difficulty 5) ---
label tod_dare_strip_all(girl):
    $ _gn = girl.Name
    python:
        _sa_is_gf = hasattr(girl, "is_dating_player") and girl.is_dating_player()
        _sa_has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _sa_bf_here = _sa_has_bf and _npc_is_active() and _bf_is_gf(store._h_npc, girl)
    if store._hangout_is_harem_night:
        $ set_scene_expression(girl, "lipbite", blush=1)
        $ Narration(_("[_gn] shrugs and starts undressing without hesitation."))
        $ Say_Line(girl, renpy.random.choice([_("It's nothing you haven't seen before~"), _("All off? Sure. Enjoy the full show."), _("Let's make this interesting.")]))
    elif _sa_is_gf:
        $ set_scene_expression(girl, "smirk", blush=1)
        $ Narration(_("[_gn] rolls her eyes and starts undressing casually."))
        $ Say_Line(girl, renpy.random.choice([_("You've seen all of this already, babe. But sure, enjoy the show."), _("Stripping for my boyfriend. What a dare."), _("Everyone else, you're welcome. Babe, you already know the view.")]))
    elif _sa_bf_here:
        $ set_scene_expression(girl, "embarrassed", blush=2)
        $ Narration(_("[_gn] looks at her boyfriend with wide eyes before slowly starting to undress."))
        $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice([_("Stripping naked with %(po)s watching... I want to disappear."), _("%(Pn)s, please don't hate me... it's a dare."), _("I can't believe I'm doing this in front of %(po)s...")])))
    else:
        python:
            _sa_alc = hangout_get_alcohol(girl)
            _sa_bold = hasattr(girl, "has_trait") and girl.has_trait("hardcore_sex")
        if _sa_alc >= 7 or _sa_bold:
            $ set_scene_expression(girl, "smirk", blush=1)
            $ Narration(_("[_gn] stands up and starts undressing without hesitation."))
            $ Say_Line(girl, renpy.random.choice([_("You wanted a show? Here's your show."), _("Fine. Everything off. Enjoy."), _("Nothing you haven't imagined already.")]))
        elif _sa_alc >= 4:
            $ set_scene_expression(girl, "looking_left", blush=1)
            $ Narration(_("[_gn] laughs nervously and starts undressing."))
            $ Say_Line(girl, renpy.random.choice([_("Okay... the drinks are helping. Here goes everything."), _("I'll blame the alcohol tomorrow."), _("Fine. But you all owe me drinks after this.")]))
        else:
            $ set_scene_expression(girl, "embarrassed", blush=2)
            $ Narration(_("[_gn] hesitates for a moment, then slowly starts undressing."))
            $ set_scene_expression(girl, "looking_down", blush=2)
            $ Say_Line(girl, renpy.random.choice([_("I can't believe I'm doing this..."), _("You all owe me after this."), _("Fine. Everything off. Happy?")]))
    python:
        girl.Outfit_Change(over="none", mid="none", chest="none", legs="none", panties="none", refresh=False)
        _slot = _hangout_pos_for(girl)
        set_girl_sprite(girl.gid, pose="standing", at_list=[_slot])
        girl.RegisterAction("player_saw_boobs")
        girl.RegisterAction("player_saw_pussy")
        for _watcher in _tod_other_girls(girl):
            set_scene_expression(_watcher, "surprised", blush=1)
    $ Narration(_("[_gn] stands completely naked, arms crossed, glaring at everyone."))
    python:
        _is_bold = hasattr(girl, "has_trait") and girl.has_trait("hardcore_sex")
    if _is_bold:
        $ set_scene_expression(girl, "smug", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("There. Feast your eyes."), _("Like what you see?"), _("Take a picture, it'll last longer.")]))
    else:
        $ set_scene_expression(girl, "embarrassed", blush=2)
        $ Say_Line(girl, renpy.random.choice([_("Stop looking at me like that..."), _("This stays between us. Forever."), _("Can I put my clothes back on now?")]))
    python:
        Change_Status(girl, "Inbt", 25)
        Change_Status(girl, "Obed", 15)
    return


# --- Kiss Player (difficulty 4) ---
label tod_dare_kiss_player(girl):
    $ _gn = girl.Name
    python:
        _kiss_cute = hasattr(girl, "has_trait") and girl.has_trait("cute_sex")
        _kiss_bold = hasattr(girl, "has_trait") and girl.has_trait("hardcore_sex")
        _kiss_npc = store._h_npc if _npc_is_active() else None
        _kiss_npc_is_bf = _kiss_npc is not None and hasattr(_kiss_npc, "girl_gid") and _kiss_npc.girl_gid == girl.gid
        _kp_is_gf = hasattr(girl, "is_dating_player") and girl.is_dating_player()
    python:
        _kp_alc = hangout_get_alcohol(girl)

    if store._hangout_is_harem_night:
        $ Narration(_("[_gn] looks at you with a confident smile."))
        $ set_scene_expression(girl, "lipbite", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("This one's for you, babe~"), _("I've been wanting to do this all night."), _("Let me show her how it's done.")]))
    elif _kp_is_gf:
        $ Narration(_("[_gn] turns to you with a warm smile."))
        $ set_scene_expression(girl, "smirk", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("Kiss my boyfriend? You don't have to dare me twice."), _("This is the easiest dare of the night."), _("Come here, babe. Let me show them how it's done.")]))
    else:
        # NPC boyfriend confrontation before the kiss
        if _kiss_npc_is_bf:
            $ _kiss_bf_name = _kiss_npc.Name
            $ set_scene_expression(girl, "neutral", blush=1)
            $ Say_Line(girl, _tl(_("It's just a dare, right %s? No big deal.")) % _kiss_bf_name)
            $ Character(_kiss_npc.Name, color=_kiss_npc.color)(_tl(_("Wait, you're REALLY going to do this? Kiss someone right in front of me?")))
            $ set_scene_expression(girl, "smirk", blush=1)
            $ Say_Line(girl, _tl(_("It's just a silly dare, it doesn't count. Just watch!")))
            $ Character(_kiss_npc.Name, color=_kiss_npc.color)(_tl(renpy.random.choice([
                _("I can't believe this..."),
                _("This is insane..."),
                _("You can't be serious right now."),
            ])))
            $ Narration(_format_partner_line(girl, _tl(_("{npc} crosses %(poss)s arms, jaw clenched, but says nothing else.")).replace("{npc}", _kiss_bf_name)))
            python:
                _kiss_npc.suspicion = getattr(_kiss_npc, "suspicion", 0) + 15
                _kiss_npc.friendship_with_player = max(0, getattr(_kiss_npc, "friendship_with_player", 200) - 20)
                print("[TOD-KISS] NPC %s: suspicion +15, friendship -20" % _kiss_bf_name)
        elif _kp_alc >= 7 or _kiss_bold:
            $ Narration(_("[_gn] turns to you with a bold grin."))
            $ set_scene_expression(girl, "lipbite", blush=1)
            $ Say_Line(girl, renpy.random.choice([_("Come here. Let's make this count."), _("I'm not going to be shy about it."), _("A dare is a dare. Get over here.")]))
        elif _kp_alc >= 4:
            $ Narration(_("[_gn] looks at you, cheeks flushed from the drinks."))
            $ set_scene_expression(girl, "looking_left", blush=1)
            $ Say_Line(girl, renpy.random.choice([_("Okay... the drinks are helping. Come here."), _("I blame the alcohol for this. Close your eyes."), _("Just a quick one, okay?")]))
        elif _kiss_cute:
            $ Narration(_("[_gn] looks at you, blushing furiously."))
            $ set_scene_expression(girl, "shy", blush=1)
            $ Say_Line(girl, renpy.random.choice([_("Just... close your eyes, okay?"), _("Don't look at me like that... just..."), _("This is so embarrassing...")]))
        else:
            $ Narration(_("[_gn] looks at you, trying to play it cool."))
            $ set_scene_expression(girl, "looking_left", blush=1)
            $ Say_Line(girl, renpy.random.choice([_("Just a quick one, okay?"), _("Close your eyes..."), _("Don't read too much into this.")]))
    call KISS_Launch(girl) from _call_KISS_Launch_dare
    $ Narration(_("She leans in and presses her lips against yours."))
    call KISS_Smooch(girl) from _call_KISS_Smooch_dare
    # intimacy/Sex_acts/cheat registration happens once, in tod_register_cheat_act below
    $ girl.set_flag("tod_kiss_done", True)
    $ Narration(_("It's brief, but electric."))
    call KISS_End(girl) from _call_KISS_End_dare
    $ set_girl_sprite(girl.gid, pose="standing", at_list=[_hangout_pos_for(girl)])
    python:
        _kp_gf = _hangout_find_gf()
        _kp_gf_watching = _kp_gf is not None and _kp_gf.gid != girl.gid
        for _other in _tod_other_girls(girl):
            if _kp_gf_watching and _other.gid == _kp_gf.gid:
                set_scene_expression(_other, "looking_left")
            else:
                set_scene_expression(_other, "sly")
    if store._hangout_is_harem_night:
        $ set_scene_expression(girl, "smirk")
        $ Say_Line(girl, renpy.random.choice([_("Mm, I never get tired of that."), _("Your lips are mine tonight~"), _("Beat that, girl.")]))
    elif _kp_is_gf:
        $ set_scene_expression(girl, "smirk", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("Mm, just like always. But better with an audience."), _("See? That's how you kiss your boyfriend."), _("I don't need a dare for that, but I'll take it.")]))
    elif _kp_alc >= 7 or _kiss_bold:
        $ set_scene_expression(girl, "smirk")
        $ Say_Line(girl, renpy.random.choice([_("...Not bad."), _("Mm. I could get used to that."), _("That was fun. Next?")]))
    elif _kp_alc >= 4:
        $ set_scene_expression(girl, "shy", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("...Okay, that was actually nice."), _("The drinks made that way too easy."), _("...That wasn't terrible.")]))
    elif _kiss_cute:
        $ set_scene_expression(girl, "embarrassed", blush=2)
        $ Say_Line(girl, renpy.random.choice([_("...Can we pretend that didn't happen?"), _("My heart won't stop racing..."), _("That was... I need a second.")]))
    else:
        $ set_scene_expression(girl, "shy", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("There. Done. Moving on."), _("...It was just a dare."), _("Okay, wow... I mean, whatever.")]))

    # GF reaction after watching another girl kiss the player
    if _kp_gf_watching:
        if store._hangout_is_harem_night:
            $ set_scene_expression(_kp_gf, "sly")
            $ Say_Line(_kp_gf, _tl(renpy.random.choice(_HAREM_GF_TEASE_LINES)))
        else:
            python:
                Change_Status(_kp_gf, "Love", -10)
                Change_Status(_kp_gf, "Obed", 5)
            $ set_scene_expression(_kp_gf, "serious")
            $ Say_Line(_kp_gf, renpy.random.choice([
                _("Right. So that just happened. In front of me."),
                _("I'm sitting right here, you know."),
                _("Cool. Great. Love that for me."),
                _("Just a dare, right? ...Right?"),
            ]))

    # NPC boyfriend reaction after the kiss
    if _kiss_npc_is_bf:
        $ Character(_kiss_npc.Name, color=_kiss_npc.color)(_tl(renpy.random.choice([
            _("...Are you done? Can we move on now?"),
            _("That was... longer than I expected."),
            _("Great. Just great."),
        ])))
        $ set_scene_expression(girl, "neutral")
        $ Say_Line(girl, _tl(renpy.random.choice([
            _("Relax, it was just a game."),
            _("See? No big deal. I'm still here."),
            _("Don't be like that. It meant nothing."),
        ])))

    python:
        Change_Status(girl, "Love", 15)
        Change_Status(girl, "Inbt", 10)
        tod_register_cheat_act(girl, "kiss")
    return


# --- Kiss Other Girl (difficulty 5) ---
label tod_dare_kiss_girl(girl, other):
    $ _gn = girl.Name
    $ _on = other.Name

    python:
        _kg_alc = hangout_get_alcohol(girl)
        _kg_alc_o = hangout_get_alcohol(other)
        _kg_bold = hasattr(girl, "has_trait") and girl.has_trait("hardcore_sex")
        _kg_bold_o = hasattr(other, "has_trait") and other.has_trait("hardcore_sex")
        _kg_is_gf = hasattr(girl, "is_dating_player") and girl.is_dating_player()
        _kg_is_gf_o = hasattr(other, "is_dating_player") and other.is_dating_player()
        _kg_has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _kg_has_bf_o = hasattr(other, "has_npc_partner") and other.has_npc_partner()
        _kg_bf_here = _kg_has_bf and _npc_is_active() and _bf_is_gf(store._h_npc, girl)
        _kg_bf_here_o = _kg_has_bf_o and _npc_is_active() and _bf_is_gf(store._h_npc, other)

    if store._hangout_is_harem_night:
        $ set_scene_expression(girl, "sly")
        $ Say_Line(girl, renpy.random.choice([_("Kiss her? Gladly~"), _("[_on] and I? You'd love that, wouldn't you?"), _("Come here, girl.")]))
        $ set_scene_expression(other, "lipbite", blush="1")
        $ Say_Line(other, renpy.random.choice([_("I'm not complaining."), _("For our boyfriend's entertainment? Sure~"), _("Let's give him a show.")]))
    elif _kg_is_gf or _kg_is_gf_o:
        python:
            _kg_gf_girl = girl if _kg_is_gf else other
            _kg_non_gf = other if _kg_is_gf else girl
        $ set_scene_expression(_kg_gf_girl, "smirk", blush="1")
        $ Say_Line(_kg_gf_girl, renpy.random.choice([_("Kissing a girl in front of my boyfriend... hope you enjoy the show, babe."), _("Don't get too excited, babe. It's just a dare."), _("I bet you like this one, huh, babe?")]))
        $ set_scene_expression(_kg_non_gf, "shy", blush="1")
        $ Say_Line(_kg_non_gf, renpy.random.choice([_("Your boyfriend is staring..."), _("Is he okay with this?"), _("This feels weird with him watching...")]))
    elif _kg_bf_here or _kg_bf_here_o:
        python:
            _kg_bf_girl = girl if _kg_bf_here else other
            _kg_no_bf = other if _kg_bf_here else girl
        $ set_scene_expression(_kg_bf_girl, "embarrassed", blush="1")
        $ Say_Line(_kg_bf_girl, _format_partner_line(_kg_bf_girl, renpy.random.choice([_("Kissing a girl in front of %(po)s... this is so wrong."), _("%(Pn)s, it's just a dare, okay?"), _("%(Pp)s is watching... I want to disappear.")])))
        $ set_scene_expression(_kg_no_bf, "looking_left", blush="1")
        $ Say_Line(_kg_no_bf, _format_partner_line(_kg_bf_girl, renpy.random.choice([_("Her %(pl)s is right there..."), _("This is kind of awkward..."), _("Maybe we should skip this one?")])))
    elif _kg_alc >= 7 or _kg_bold:
        $ set_scene_expression(girl, "smirk", blush="1")
        $ Say_Line(girl, renpy.random.choice([_("Come here, [_on]~"), _("Alright, [_on], let's make this good."), _("I'm not going to half-ass this. Come here.")]))
        if _kg_alc_o >= 5 or _kg_bold_o:
            $ set_scene_expression(other, "lipbite", blush="1")
            $ Say_Line(other, renpy.random.choice([_("Let's do this."), _("Bring it on, girl."), _("Alright, alright. Come here.")]))
        else:
            $ set_scene_expression(other, "shy", blush="1")
            $ Say_Line(other, renpy.random.choice([_("O-okay... if you say so."), _("You seem way too into this..."), _("Well... I guess it's just a dare.")]))
    elif _kg_alc >= 4:
        $ set_scene_expression(girl, "looking_left", blush="1")
        $ Say_Line(girl, renpy.random.choice([_("Okay, [_on]... a dare is a dare."), _("The drinks are making this feel less weird. Come here, [_on]."), _("Let's just get it over with, [_on].")]))
        $ set_scene_expression(other, "looking_left", blush="1")
        $ Say_Line(other, renpy.random.choice([_("A dare is a dare, I guess."), _("Okay... let's just do it."), _("Fine... but this stays between us.")]))
    else:
        $ set_scene_expression(girl, "shy", blush="1")
        $ Say_Line(girl, renpy.random.choice([_("I can't believe I'm doing this... come here, [_on]."), _("Okay... [_on], you ready?"), _("This is so weird... but a dare is a dare.")]))
        $ set_scene_expression(other, "shy", blush="1")
        $ Say_Line(other, renpy.random.choice([_("Only if she wants to."), _("Let's just... get it over with."), _("Well... I guess it's just a dare.")]))

    # Move both girls close together (elevated zorder so bystanders don't overlap)
    $ set_girl_sprite(girl.gid, pose="standing", at_list=[Transform(xalign=0.60, yalign=2.0)], zorder=10)
    $ set_girl_sprite(other.gid, pose="standing", at_list=[Transform(xalign=0.70, yalign=2.0)], zorder=10)

    if store._hangout_is_harem_night:
        $ Narration(_("They close the distance without hesitation, lips meeting with practiced ease."))
    elif _kg_alc >= 7 or (_kg_bold and _kg_bold_o):
        $ Narration(_("They close the distance quickly, lips meeting with zero hesitation."))
    else:
        $ Narration(_("They lean toward each other, hesitate for a second, then their lips meet."))
    $ set_scene_expression(girl, "kissing", blush="1")
    $ set_scene_expression(other, "kissing", blush="1")
    pause 1.5
    $ set_scene_expression(girl, "pleasure", blush="2")
    $ set_scene_expression(other, "pleasure", blush="2")
    $ Narration(_("The kiss lingers longer than expected. When they pull apart, both are blushing."))

    # Move back to normal positions
    $ set_girl_sprite(girl.gid, pose="standing", at_list=[_hangout_pos_for(girl)], zorder=0)
    $ set_girl_sprite(other.gid, pose="standing", at_list=[_hangout_pos_for(other)], zorder=0)

    if store._hangout_is_harem_night:
        $ set_scene_expression(girl, "smirk", blush=1)
        $ set_scene_expression(other, "smirk", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("Mm, she's a good kisser. You picked well, babe."), _("That was fun. We should do this more often~"), _("Not bad at all, girl.")]))
        $ Say_Line(other, renpy.random.choice([_("Right back at you~"), _("I think he liked that more than we did."), _("Your turn next, babe.")]))
    elif _kg_is_gf or _kg_is_gf_o:
        python:
            _kg_gf_girl_r = girl if _kg_is_gf else other
            _kg_non_gf_r = other if _kg_is_gf else girl
        $ set_scene_expression(_kg_gf_girl_r, "smirk", blush=1)
        $ Say_Line(_kg_gf_girl_r, renpy.random.choice([_("See, babe? That wasn't so bad."), _("Don't worry, you're still my favorite."), _("That was nice. But you're better, babe.")]))
        $ set_scene_expression(_kg_non_gf_r, "looking_left", blush=2)
        $ Say_Line(_kg_non_gf_r, renpy.random.choice([_("I can feel him staring at us..."), _("Your boyfriend is never going to let this go."), _("That was interesting... to say the least.")]))
    elif _kg_bf_here or _kg_bf_here_o:
        python:
            _kg_bf_girl_r = girl if _kg_bf_here else other
            _kg_no_bf_r = other if _kg_bf_here else girl
        $ set_scene_expression(_kg_bf_girl_r, "embarrassed", blush=2)
        $ Say_Line(_kg_bf_girl_r, _format_partner_line(_kg_bf_girl_r, renpy.random.choice([_("%(Pn)s, please say something..."), _("I can't look at %(po)s right now."), _("%(Pp)s is never forgiving me for that.")])))
        $ set_scene_expression(_kg_no_bf_r, "looking_left", blush=1)
        $ Say_Line(_kg_no_bf_r, _format_partner_line(_kg_bf_girl_r, renpy.random.choice([_("Her %(pl)s looks like %(pp)s is about to pass out."), _("I feel kind of bad for %(po)s..."), _("That was fun, but her %(pl)s sure didn't think so.")])))
    elif _kg_alc >= 7 or (_kg_bold and _kg_bold_o):
        $ set_scene_expression(girl, "smirk", blush=1)
        $ set_scene_expression(other, "smirk", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("Not bad, [_on]. Not bad at all."), _("Okay, she knows what she's doing."), _("That was better than I expected.")]))
        $ Say_Line(other, renpy.random.choice([_("Right back at you."), _("You're not half bad yourself."), _("I'll admit, that was good.")]))
    elif _kg_alc >= 4:
        $ set_scene_expression(girl, "looking_left", blush=2)
        $ set_scene_expression(other, "looking_left", blush=2)
        $ Say_Line(girl, renpy.random.choice([_("Okay, that was... kind of nice."), _("The drinks definitely helped with that."), _("Let's not overthink it.")]))
        $ Say_Line(other, renpy.random.choice([_("I need another drink after that."), _("That was... not terrible."), _("We blame the alcohol, agreed?")]))
    else:
        $ set_scene_expression(girl, "shy", blush=2)
        $ set_scene_expression(other, "shy", blush=2)
        $ Say_Line(girl, renpy.random.choice([_("That was... something."), _("We don't talk about this later."), _("My heart is pounding...")]))
        $ Say_Line(other, renpy.random.choice([_("I can't believe we did that."), _("Let's just... move on."), _("Well, that happened.")]))

    python:
        Change_Status(girl, "Inbt", 20)
        Change_Status(other, "Inbt", 20)
        girl.add_like_for(other.gid, 15)
        other.add_like_for(girl.gid, 15)
        girl.RegisterAction("kiss")
        other.RegisterAction("kiss")
        girl.set_flag("tod_kiss_done", True)
        other.set_flag("tod_kiss_done", True)
        shift_spectrum(girl, 4)
        shift_spectrum(other, 4)
        debug_log("[TOD] kiss_girl spectrum shift: %s=%d %s=%d" % (girl.gid, girl.sexuality_spectrum, other.gid, other.sexuality_spectrum))
    return


# --- Suck Other Girl's Boobs (difficulty 6) ---
label tod_dare_suck_boobs(girl, other):
    $ _gn = girl.Name
    $ _on = other.Name

    python:
        _sb_alc = hangout_get_alcohol(girl)
        _sb_alc_o = hangout_get_alcohol(other)
        _sb_bold = hasattr(girl, "has_trait") and girl.has_trait("hardcore_sex")
        _sb_bold_o = hasattr(other, "has_trait") and other.has_trait("hardcore_sex")
        _sb_is_gf = hasattr(girl, "is_dating_player") and girl.is_dating_player()
        _sb_is_gf_o = hasattr(other, "is_dating_player") and other.is_dating_player()
        _sb_has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _sb_has_bf_o = hasattr(other, "has_npc_partner") and other.has_npc_partner()
        _sb_bf_here = _sb_has_bf and _npc_is_active() and _bf_is_gf(store._h_npc, girl)
        _sb_bf_here_o = _sb_has_bf_o and _npc_is_active() and _bf_is_gf(store._h_npc, other)

    if store._hangout_is_harem_night:
        $ set_scene_expression(girl, "sly")
        $ Say_Line(girl, renpy.random.choice([_("Gladly. Come here, [_on]~"), _("Now this is a dare I can get behind."), _("I was hoping for this one.")]))
        $ set_scene_expression(other, "lipbite", blush="1")
        $ Say_Line(other, renpy.random.choice([_("Go ahead, I'm curious~"), _("For our boyfriend's show? Sure."), _("Don't hold back.")]))
    elif _sb_is_gf or _sb_is_gf_o:
        python:
            _sb_gf_girl = girl if _sb_is_gf else other
            _sb_non_gf = other if _sb_is_gf else girl
        $ set_scene_expression(_sb_gf_girl, "smirk", blush="1")
        $ Say_Line(_sb_gf_girl, renpy.random.choice([_("My boyfriend gets to watch this? Lucky him."), _("Babe, don't enjoy this too much."), _("A dare is a dare. Don't get any ideas, babe.")]))
        $ set_scene_expression(_sb_non_gf, "embarrassed", blush="1")
        $ Say_Line(_sb_non_gf, renpy.random.choice([_("Your boyfriend is watching us..."), _("Is he going to be okay with this?"), _("This is weird with him here...")]))
    elif _sb_bf_here or _sb_bf_here_o:
        python:
            _sb_bf_girl = girl if _sb_bf_here else other
            _sb_no_bf = other if _sb_bf_here else girl
        $ set_scene_expression(_sb_bf_girl, "embarrassed", blush="1")
        $ Say_Line(_sb_bf_girl, _format_partner_line(_sb_bf_girl, renpy.random.choice([_("Doing this in front of %(po)s... I want to die."), _("%(Pn)s, it's just a dare... don't be mad."), _("%(Pp)s is watching... this is the worst.")])))
        $ set_scene_expression(_sb_no_bf, "looking_left", blush="1")
        $ Say_Line(_sb_no_bf, _format_partner_line(_sb_bf_girl, renpy.random.choice([_("Her %(pl)s is right there..."), _("Maybe we shouldn't..."), _("This is really awkward with %(po)s here.")])))
    elif _sb_alc >= 7 or _sb_bold:
        $ set_scene_expression(girl, "smirk", blush="1")
        $ Say_Line(girl, renpy.random.choice([_("Come here, [_on]. Let me show you something."), _("This one I don't mind at all."), _("Alright, [_on]... let's make it good.")]))
        if _sb_alc_o >= 5 or _sb_bold_o:
            $ set_scene_expression(other, "lipbite", blush="1")
            $ Say_Line(other, renpy.random.choice([_("Go for it."), _("I'm not going to say no."), _("Let's do this.")]))
        else:
            $ set_scene_expression(other, "embarrassed", blush="1")
            $ Say_Line(other, renpy.random.choice([_("Wait, you're serious? Okay... fine."), _("You seem way too eager... but a dare is a dare."), _("Just... be gentle.")]))
    elif _sb_alc >= 4:
        $ set_scene_expression(girl, "looking_left", blush="1")
        $ Say_Line(girl, renpy.random.choice([_("Okay... the drinks are making this feel doable."), _("A dare is a dare. Come here, [_on]."), _("Alright... let's just do it.")]))
        $ set_scene_expression(other, "embarrassed", blush="1")
        $ Say_Line(other, renpy.random.choice([_("Fine... I blame the alcohol."), _("Okay... just don't make it weird."), _("This stays between us.")]))
    else:
        $ set_scene_expression(girl, "surprised")
        $ Say_Line(girl, renpy.random.choice([_("That's... a lot."), _("Okay... if [_on] is cool with it."), _("I... alright. A dare is a dare.")]))
        $ set_scene_expression(other, "embarrassed", blush="1")
        $ Say_Line(other, renpy.random.choice([_("I mean... it's a dare. I guess I have to."), _("This is insane. Fine."), _("Just... be gentle.")]))

    # Other girl needs to expose chest too
    $ other.Outfit_Change(over="none", mid="none", chest_up=True, refresh=False)
    $ set_girl_sprite(other.gid, pose="standing", at_list=[_hangout_pos_for(other)])
    $ other.RegisterAction("player_saw_boobs")

    $ set_girl_sprite(girl.gid, pose="standing", at_list=[Transform(xalign=0.60, yalign=2.0)], zorder=10)
    $ set_girl_sprite(other.gid, pose="standing", at_list=[Transform(xalign=0.70, yalign=2.0)], zorder=10)

    $ set_scene_expression(girl, "pleasure", blush="1", mouth="mouth_tongue")
    $ set_scene_expression(other, "pleasure", blush="2")
    $ Narration(_("[_gn] leans in and takes [_on]'s breast into her mouth. [_on] gasps softly."))
    $ set_girl_sprite(girl.gid, pose="standing", at_list=[_tod_suck_lean])
    pause 1.5
    $ set_girl_sprite(girl.gid, pose="standing", at_list=[Transform(xalign=0.60, yalign=2.0, yoffset=0)])
    $ Narration(_("The room goes completely silent for a few seconds."))

    $ set_girl_sprite(girl.gid, pose="standing", at_list=[_hangout_pos_for(girl)], zorder=0)
    $ set_girl_sprite(other.gid, pose="standing", at_list=[_hangout_pos_for(other)], zorder=0)

    if store._hangout_is_harem_night:
        $ set_scene_expression(girl, "smirk", blush="1")
        $ Say_Line(girl, renpy.random.choice([_("Mm, she tastes nice~"), _("That was fun. Your turn next, babe?"), _("I could get used to this.")]))
        $ set_scene_expression(other, "pleasure", blush="2")
        $ Say_Line(other, renpy.random.choice([_("Okay, wow... that felt really good."), _("I think I liked that more than I should."), _("Your girlfriend is talented, babe~")]))
    elif _sb_is_gf or _sb_is_gf_o:
        python:
            _sb_gf_girl_r = girl if _sb_is_gf else other
            _sb_non_gf_r = other if _sb_is_gf else girl
        $ set_scene_expression(_sb_gf_girl_r, "smirk", blush=1)
        $ Say_Line(_sb_gf_girl_r, renpy.random.choice([_("You loved every second of that, didn't you, babe?"), _("One-time thing. Probably."), _("Don't worry, you're still my number one.")]))
        $ set_scene_expression(_sb_non_gf_r, "looking_left", blush=2)
        $ Say_Line(_sb_non_gf_r, renpy.random.choice([_("Her boyfriend will never let this go."), _("That was intense with him watching."), _("I feel like I crossed a line...")]))
    elif _sb_bf_here or _sb_bf_here_o:
        python:
            _sb_bf_girl_r = girl if _sb_bf_here else other
            _sb_no_bf_r = other if _sb_bf_here else girl
        $ set_scene_expression(_sb_bf_girl_r, "embarrassed", blush=2)
        $ Say_Line(_sb_bf_girl_r, _format_partner_line(_sb_bf_girl_r, renpy.random.choice([_("%(Pn)s, please don't hate me..."), _("I can't look at %(po)s after that."), _("%(Pp)s is never going to forget this.")])))
        $ set_scene_expression(_sb_no_bf_r, "looking_left", blush=1)
        $ Say_Line(_sb_no_bf_r, _format_partner_line(_sb_bf_girl_r, renpy.random.choice([_("Her %(pl)s looks devastated..."), _("I feel really bad for %(po)s..."), _("That was fun, but her %(pl)s didn't think so.")])))
    elif _sb_alc >= 7 or (_sb_bold and _sb_bold_o):
        $ set_scene_expression(girl, "smirk", blush="1")
        $ Say_Line(girl, renpy.random.choice([_("That was actually fun."), _("I could do that again."), _("She has great boobs, by the way.")]))
        $ set_scene_expression(other, "pleasure", blush="2")
        $ Say_Line(other, renpy.random.choice([_("Okay, wow... she's good at that."), _("That felt way better than I expected."), _("I'm not going to lie, that was nice.")]))
    elif _sb_alc >= 4:
        $ set_scene_expression(girl, "looking_left", blush="1")
        $ Say_Line(girl, renpy.random.choice([_("Okay... that was more intense than I expected."), _("I blame the drinks for how much I didn't hate that."), _("Well, that happened.")]))
        $ set_scene_expression(other, "shy", blush="2")
        $ Say_Line(other, renpy.random.choice([_("I need another drink after that."), _("That was... something."), _("The alcohol made that way too intense.")]))
    else:
        $ set_scene_expression(girl, "embarrassed", blush="1")
        $ Say_Line(girl, renpy.random.choice([_("Done. Are you satisfied now?"), _("I can't believe that just happened."), _("Okay... that was way more intense than I expected.")]))
        $ set_scene_expression(other, "shy", blush="2")
        $ Say_Line(other, renpy.random.choice([_("My brain just short-circuited."), _("I... need a moment."), _("That was... not what I expected to feel.")]))

    python:
        Change_Status(girl, "Inbt", 25)
        Change_Status(other, "Inbt", 25)
        Change_Status(girl, "Obed", 10)
        girl.add_like_for(other.gid, 15)
        other.add_like_for(girl.gid, 15)
        shift_spectrum(girl, 6)
        shift_spectrum(other, 6)
        debug_log("[TOD] suck_boobs spectrum shift: %s=%d %s=%d" % (girl.gid, girl.sexuality_spectrum, other.gid, other.sexuality_spectrum))
    return


# --- Player Slaps Girl's Ass (difficulty 5) ---
label tod_dare_spank_player(girl):
    $ _gn = girl.Name
    $ set_scene_expression(girl, "looking_right")
    $ Narration(_("[_gn] rolls her eyes but gets up."))
    python:
        _spk_hardcore = hasattr(girl, "has_trait") and girl.has_trait("hardcore_sex")
        _spk_cute = hasattr(girl, "has_trait") and girl.has_trait("cute_sex")
        _spk_is_gf = hasattr(girl, "is_dating_player") and girl.is_dating_player()
        _spk_has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _spk_bf_here = _spk_has_bf and _npc_is_active() and _bf_is_gf(store._h_npc, girl)
    if store._hangout_is_harem_night:
        $ set_scene_expression(girl, "lipbite")
        $ Say_Line(girl, renpy.random.choice([_("Go ahead, babe. I know you want to~"), _("Don't be gentle. She's watching."), _("Slap it like you mean it.")]))
    elif _spk_is_gf:
        $ set_scene_expression(girl, "smirk", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("Spanking your girlfriend in front of everyone? You're shameless."), _("Go ahead, babe. Not like you don't do this already."), _("Make it good. I know you can.")]))
    elif _spk_bf_here:
        $ set_scene_expression(girl, "embarrassed", blush=2)
        $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice([_("Getting spanked with %(po)s watching... kill me now."), _("%(Pn)s, please look away... this is just a dare."), _("I'm so sorry, %(pn)s... it doesn't mean anything.")])))
    elif _spk_hardcore:
        $ set_scene_expression(girl, "smirk")
        $ Say_Line(girl, renpy.random.choice([_("Go ahead. Don't hold back."), _("Slap it properly or don't bother."), _("Make it count.")]))
    else:
        $ set_scene_expression(girl, "embarrassed", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("Fine. But not too hard."), _("One slap. That's it."), _("If you leave a mark, I'm leaving.")]))

    # Girl goes to rear pose (RCG or LD) -- hide other girls so they don't overlap
    python:
        _spank_pose_d = _rear_pose_for(girl)
        _spank_others_d = _tod_other_girls(girl)
        for _so in _spank_others_d:
            renpy.hide(_so.gid)
        print("[SPANK_DEBUG] dare_spank: gid=%s pose=%s clothes=%s clothes_state=%s" % (girl.gid, _spank_pose_d, str(girl.clothes), str(girl.clothes_state)))
        if _spank_pose_d == "reverse_cowgirl":
            _dbg_attrs = _build_rcg_attributes(girl)
            print("[SPANK_DEBUG] dare_spank: rcg_attrs=%s" % str(_dbg_attrs))
    if _spank_pose_d == "laying_down":
        $ _ld_show_rear_preview(girl)
    else:
        $ set_girl_sprite(girl.gid, pose=_spank_pose_d, at_list=[slot_center])
    $ Narration(_("[_gn] bends over, presenting her backside."))
    $ Say_Player(_("Here goes..."))
    $ slap_crack()   # the shared crack (SubEvents.rpy): this dare landed mute until 2026-10-10
    call Punch from _call_Punch_dare_spank

    # Return to standing and restore others
    if _spank_pose_d == "laying_down":
        $ _hide_scene_layers("laying_down")
    $ set_girl_sprite(girl.gid, pose="standing", at_list=[_hangout_pos_for(girl)])
    python:
        for _so in _spank_others_d:
            set_girl_sprite(_so.gid, pose="standing", at_list=[_hangout_pos_for(_so)])

    $ set_scene_expression(girl, "surprised", blush=1)
    $ Say_Line(girl, renpy.random.choice([_("Ah! Hey!"), _("Ow! You didn't have to go that hard!"), _("Mmph...!")]))

    python:
        has_hardcore = _spk_hardcore
        Change_Status(girl, "Obed", 15)
        Change_Status(girl, "Inbt", 10)
        tod_register_cheat_act(girl, "touch")
        if has_hardcore:
            Change_Status(girl, "Obed", 10)
        for _other in _tod_other_girls(girl):
            set_scene_expression(_other, "laugh")
        # her spank record (spank_note): only the hardcore answer below enjoyed it, the others complain
        spank_note(girl, has_hardcore, "tod_dare")

    if has_hardcore:
        $ set_scene_expression(girl, "smug")
        $ Say_Line(girl, renpy.random.choice([_("...Do it again."), _("That actually felt kind of good."), _("Harder next time.")]))
    else:
        if _spk_cute:
            $ set_scene_expression(girl, "embarrassed", blush=1)
            $ Say_Line(girl, renpy.random.choice([_("M-my butt! That was so mean!"), _("Ow ow ow... I can still feel it..."), _("You're terrible! My face is so red right now...")]))
        else:
            $ set_scene_expression(girl, "looking_left", blush=1)
            $ Say_Line(girl, renpy.random.choice([_("Okay, we're done. Never again."), _("My butt is on fire..."), _("You enjoyed that way too much.")]))
    return


# --- Player Kisses Girl's Boobs (difficulty 5) ---
label tod_dare_kiss_boobs_player(girl):
    $ _gn = girl.Name
    python:
        _kb_bold = hasattr(girl, "has_trait") and girl.has_trait("hardcore_sex")
        _kb_is_gf = hasattr(girl, "is_dating_player") and girl.is_dating_player()
        _kb_has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _kb_bf_here = _kb_has_bf and _npc_is_active() and _bf_is_gf(store._h_npc, girl)
    if store._hangout_is_harem_night:
        $ set_scene_expression(girl, "lipbite", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("Go ahead, they're all yours~"), _("Kiss them properly this time, babe."), _("Don't be shy, she's seen this before.")]))
    elif _kb_is_gf:
        $ set_scene_expression(girl, "smirk", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("Kissing your girlfriend's boobs? Nothing new for you."), _("You do this every night. But sure, show off."), _("Go ahead, babe. Give them a good show.")]))
    elif _kb_bf_here:
        $ set_scene_expression(girl, "embarrassed", blush=2)
        $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice([_("%(Pp)s is right there and someone's kissing my boobs... God."), _("This is beyond humiliating with %(po)s watching..."), _("Don't look, %(pn)s... please just don't look.")])))
    elif _kb_bold:
        $ set_scene_expression(girl, "lipbite")
        $ Say_Line(girl, renpy.random.choice([_("Go ahead. Don't be shy."), _("You can look all you want while you're at it."), _("Make it count.")]))
    else:
        $ set_scene_expression(girl, "shy", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("This is so embarrassing..."), _("Okay, but be quick about it."), _("I'm only doing this because it's a dare.")]))
    $ girl.Outfit_Change(over="none", mid="none", chest_up=True, refresh=False)
    $ set_girl_sprite(girl.gid, pose="standing", at_list=[_hangout_pos_for(girl)])
    python:
        girl.RegisterAction("player_saw_boobs")
        for _watcher in _tod_other_girls(girl):
            set_scene_expression(_watcher, "surprised", blush=1)
    $ Narration(_("[_gn] lifts her top, exposing her chest. You lean in and press your lips gently against her skin."))
    if _kb_bold:
        $ set_scene_expression(girl, "smirk", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("...Your lips are warm."), _("Mm, you can keep going if you want."), _("Not bad. You've got some nerve.")]))
    else:
        $ set_scene_expression(girl, "embarrassed", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("O-okay, that's enough."), _("That tickles... stop..."), _("...Your lips are warm.")]))
    python:
        Change_Status(girl, "Inbt", 20)
        Change_Status(girl, "Love", 15)
        tod_register_cheat_act(girl, "touch")
    return


# --- Girl Slaps Other Girl's Ass (difficulty 4) ---
label tod_dare_spank_other(girl, other):
    $ _gn = girl.Name
    $ _on = other.Name

    python:
        _so_bold = hasattr(girl, "has_trait") and girl.has_trait("hardcore_sex")
        _so_is_gf = hasattr(girl, "is_dating_player") and girl.is_dating_player()
        _so_is_gf_o = hasattr(other, "is_dating_player") and other.is_dating_player()
        _so_has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _so_has_bf_o = hasattr(other, "has_npc_partner") and other.has_npc_partner()
        _so_bf_here = _so_has_bf and _npc_is_active() and _bf_is_gf(store._h_npc, girl)
        _so_bf_here_o = _so_has_bf_o and _npc_is_active() and _bf_is_gf(store._h_npc, other)

    # --- Spanker (girl) approach ---
    if _so_is_gf:
        $ set_scene_expression(girl, "smirk", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("Spanking another girl in front of my boyfriend. He's loving this."), _("Babe, don't enjoy this too much."), _("Sorry [_on], my boyfriend's watching so I gotta make it good.")]))
    elif _so_bf_here:
        $ set_scene_expression(girl, "embarrassed", blush=1)
        $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice([_("Spanking a girl in front of %(po)s... awkward."), _("%(Pn)s, it's just a dare, okay?"), _("%(Pp)s is watching... let's get this over with.")])))
    elif _so_bold:
        $ set_scene_expression(girl, "smirk")
        $ Say_Line(girl, renpy.random.choice([_("You want me to slap [_on]'s butt? Seriously?"), _("Okay, this is weird. But fine."), _("Sorry in advance, [_on].")]))
    else:
        $ set_scene_expression(girl, "embarrassed", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("You want me to slap [_on]'s butt? Seriously?"), _("Okay, this is weird. But fine."), _("Sorry in advance, [_on].")]))

    # --- Spankee (other) reaction ---
    if _so_is_gf_o:
        $ set_scene_expression(other, "embarrassed", blush=1)
        $ Say_Line(other, renpy.random.choice([_("Getting spanked while my boyfriend watches... great."), _("Babe, please look away."), _("This is so embarrassing with him here...")]))
    elif _so_bf_here_o:
        $ set_scene_expression(other, "embarrassed", blush=1)
        $ Say_Line(other, _format_partner_line(other, renpy.random.choice([_("%(Pn)s, don't watch this..."), _("%(Pp)s is right there... just get it over with."), _("This is humiliating with %(po)s watching...")])))
    else:
        $ set_scene_expression(other, "startled")
        $ Say_Line(other, renpy.random.choice([_("Wait, what?!"), _("Oh no..."), _("Just get it over with.")]))

    # Hide slapper girl while target is in rear pose
    python:
        _slap_other_pose = _rear_pose_for(other)
    $ renpy.hide(girl.gid)
    if _slap_other_pose == "laying_down":
        $ _ld_show_rear_preview(other)
    else:
        $ set_girl_sprite(other.gid, pose=_slap_other_pose, at_list=[slot_center])
    $ Narration(_("[_on] bends over reluctantly. [_gn] winds up and..."))
    $ slap_crack()   # the shared crack (SubEvents.rpy): one slap lands here, two records follow (giver + taker)
    call Punch from _call_Punch_dare_spank_other

    # Restore both to standing
    if _slap_other_pose == "laying_down":
        $ _hide_scene_layers("laying_down")
    $ set_girl_sprite(other.gid, pose="standing", at_list=[_hangout_pos_for(other)])
    $ set_girl_sprite(girl.gid, pose="standing", at_list=[_hangout_pos_for(girl)])

    $ set_scene_expression(other, "surprised", blush=1)
    $ Say_Line(other, renpy.random.choice([_("OW! [_gn]!!"), _("That was WAY too hard!"), _("My butt!")]))
    if _so_bold:
        $ set_scene_expression(girl, "sly")
    else:
        $ set_scene_expression(girl, "looking_right", blush=1)
    python:
        _so_after = renpy.random.choice([_("Oops. My hand slipped."), _("Felt good, honestly."), _("Sorry not sorry.")])
        # her spank record, the hand side (spank_note given): her answer says whether she liked doing it
        spank_note(girl, _so_after in (_("Felt good, honestly."), _("Sorry not sorry.")), "tod_girl_dare_hand", given=True)
    $ Say_Line(girl, _so_after)

    python:
        Change_Status(girl, "Inbt", 10)
        Change_Status(other, "Inbt", 10)
        girl.add_like_for(other.gid, 10)
        other.add_like_for(girl.gid, 10)
        shift_spectrum(girl, 2)
        shift_spectrum(other, 2)
        debug_log("[TOD] spank_other spectrum shift: %s=%d %s=%d" % (girl.gid, girl.sexuality_spectrum, other.gid, other.sexuality_spectrum))
        # her spank record (spank_note): a girl's hand, not the player's, and every answer of hers above hurts
        spank_note(other, False, "tod_girl_dare", by_player=False)
    return


# --- Blowjob for Player (difficulty 8) ---
label tod_dare_bj_player(girl):
    $ _gn = girl.Name
    python:
        _bj_bold = hasattr(girl, "has_trait") and girl.has_trait("hardcore_sex")
        _bj_cute = hasattr(girl, "has_trait") and girl.has_trait("cute_sex")
        _bj_is_gf = hasattr(girl, "is_dating_player") and girl.is_dating_player()
        _bj_has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _bj_bf_here = _bj_has_bf and _npc_is_active() and _bf_is_gf(store._h_npc, girl)
    if store._hangout_is_harem_night:
        $ Narration(_("The energy in the room shifts. Both girls exchange a knowing look."))
        $ set_scene_expression(girl, "lusty", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("Mm, I was hoping for this one~"), _("Finally, a real dare. Watch and learn, girl."), _("Lucky you, babe. Right here, right now.")]))
        python:
            _others = _tod_other_girls(girl)
            for _other in _others:
                set_scene_expression(_other, "sly", blush=1)
    elif _bj_is_gf:
        $ Narration(_("The room goes quiet, but [_gn] doesn't hesitate."))
        $ set_scene_expression(girl, "lipbite", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("A blowjob for my boyfriend? You didn't have to dare me."), _("I already do this. Having an audience is the only new part."), _("Come here, babe. Let me show them what they're missing.")]))
        python:
            _others = _tod_other_girls(girl)
            for _other in _others:
                set_scene_expression(_other, "surprised", blush=2)
    elif _bj_bf_here:
        $ Narration(_("The room goes deathly quiet."))
        $ set_scene_expression(girl, "embarrassed", blush=2)
        $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice([_("I... with %(po)s right there? This is insane."), _("%(Pp)s is watching me... I can't believe I'm doing this."), _("I'm so sorry, %(pn)s... a dare is a dare.")])))
        $ Say_Player(_("You don't have to if you-"))
        $ set_scene_expression(girl, "serious")
        $ Say_Line(girl, renpy.random.choice([_("I already said I'd do it. Don't make it worse."), _("Just... let me get this over with."), _("Too late to back out now.")]))
        python:
            _others = _tod_other_girls(girl)
            for _other in _others:
                set_scene_expression(_other, "surprised", blush=2)
    else:
        $ Narration(_("The room goes quiet. Everyone knows this just got serious."))
        if _bj_bold:
            $ set_scene_expression(girl, "lusty", blush=1)
        else:
            $ set_scene_expression(girl, "embarrassed", blush=2)
        $ Say_Line(girl, renpy.random.choice([_("You're insane. ...But I said I'd do it."), _("I can't believe this is happening right now."), _("Fine. But everyone looks away.")]))
        $ Say_Player(_("You don't have to if you-"))
        $ set_scene_expression(girl, "serious")
        $ Say_Line(girl, renpy.random.choice([_("Shut up. A dare is a dare."), _("I already said I'd do it. Don't make it weird."), _("Too late to back out now.")]))
        python:
            _others = _tod_other_girls(girl)
            for _other in _others:
                set_scene_expression(_other, "surprised", blush=2)

    # Block interruptions during hangout dares
    $ store._interruption_happened = True
    $ store._witness_check_done = True
    $ _scene_exit_flags_reset()  # dares bypass sex_menu; clear scene-exit flags leaked by a prior dare's cum
    call BJ_Launch(girl) from _call_BJ_Launch_dare_bj
    call BJ_ControlMenu(girl) from _call_BJ_ControlMenu_dare_bj
    call BJ_End(girl) from _call_BJ_End_dare_bj
    python:
        for _rg in _hangout_girls_list():
            set_girl_sprite(_rg.gid, pose="standing", at_list=[_hangout_pos_for(_rg)])

    python:
        Change_Status(girl, "Obed", 30)
        Change_Status(girl, "Inbt", 25)
        Change_Status(girl, "Love", 20)
        # Register the act
        if not hasattr(girl, "Sex_acts"):
            girl.Sex_acts = {}
        tod_register_cheat_act(girl, "bj")  # also counts Sex_acts["bj"] via mark_intimacy
        if not hasattr(girl, "Sex_act_locations"):
            girl.Sex_act_locations = []
        girl.Sex_act_locations.append({"act": "bj", "location": getattr(store, "CurrentLocation", "room"), "day": getattr(store, "Day", 1)})
        for _w in _hangout_girls_list():
            if _w.gid != girl.gid:
                girl_learns_act(_w, girl, "bj", with_player=True)

    if _bj_bold:
        $ set_scene_expression(girl, "lewd", blush=2)
    else:
        $ set_scene_expression(girl, "lipbite", blush=2)
    $ Narration(_("When it's over, [_gn] wipes her mouth and sits back down as if nothing happened."))
    python:
        for _other in _others:
            set_scene_expression(_other, "sly", blush=1)
    if store._hangout_is_harem_night:
        $ set_scene_expression(girl, "smirk", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("Your turn next, girl~"), _("Think you can do better? I dare you."), _("Mm, I love this game.")]))
    elif _bj_is_gf:
        $ set_scene_expression(girl, "smirk", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("That was for my boyfriend. You're all just witnesses."), _("See? That's how it's done. Take notes."), _("Just another Tuesday for us. Except with an audience.")]))
    else:
        $ set_scene_expression(girl, "looking_left", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("We never speak of this."), _("...Next turn."), _("I need a drink. A strong one.")]))

    # GF watches another girl give player a BJ
    python:
        _bj_gf_w = _hangout_find_gf()
        _bj_gf_watching = _bj_gf_w is not None and _bj_gf_w.gid != girl.gid
    if _bj_gf_watching:
        if store._hangout_is_harem_night:
            $ set_scene_expression(_bj_gf_w, "sly")
            $ Say_Line(_bj_gf_w, _tl(renpy.random.choice(_HAREM_GF_TEASE_LINES)))
        else:
            python:
                Change_Status(_bj_gf_w, "Love", -25)
                Change_Status(_bj_gf_w, "Obed", 10)
            $ set_scene_expression(_bj_gf_w, "serious")
            $ Say_Line(_bj_gf_w, renpy.random.choice([
                _("She just... in front of me? Seriously?"),
                _("I'm RIGHT HERE. And she just did THAT to my boyfriend."),
                _("We are going to talk about this later. Trust me."),
            ]))

    return


# --- Titjob for Player (difficulty 7) ---
label tod_dare_tj_player(girl):
    $ _gn = girl.Name

    # Girl can't do TJ (bust too small) — she refuses with insecurity
    if not girl_has_pose(girl, "titjob"):
        python:
            set_scene_expression(girl, "sad", eyes="eyes_side")
            Say_Line(girl, renpy.random.choice([
                _("I... I can't do that. You know I can't."),
                _("A titjob? With what? ...Pass."),
                _("That's not fair. You know I don't have enough for that."),
            ]))
        $ Narration(_("[_gn] looks down and crosses her arms, clearly upset."))
        python:
            _others = _tod_other_girls(girl)
            for _other in _others:
                set_scene_expression(_other, "worried")
            Change_Status(girl, "Obed", 5)
            Change_Status(girl, "Inbt", 5)
        $ set_scene_expression(girl, "normal")
        $ Say_Line(girl, renpy.random.choice([_("...Next turn."), _("Can we move on?"), _("Just pick something else.")]))
        return

    python:
        _tj_bold = hasattr(girl, "has_trait") and girl.has_trait("hardcore_sex")
        _tj_cute = hasattr(girl, "has_trait") and girl.has_trait("cute_sex")
        _tj_is_gf = hasattr(girl, "is_dating_player") and girl.is_dating_player()
        _tj_has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _tj_bf_here = _tj_has_bf and _npc_is_active() and _bf_is_gf(store._h_npc, girl)
    if store._hangout_is_harem_night:
        $ Narration(_("The atmosphere is charged with excitement. No one is pretending this is innocent anymore."))
        $ set_scene_expression(girl, "lusty", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("With my boobs? You know I'm good at this~"), _("Time to put on a show."), _("Watch closely, girl. This is how you please our man.")]))
        python:
            _others = _tod_other_girls(girl)
            for _other in _others:
                set_scene_expression(_other, "sly", blush=1)
    elif _tj_is_gf:
        $ Narration(_("The room goes quiet, but [_gn] looks completely at ease."))
        $ set_scene_expression(girl, "lipbite", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("A titjob for my boyfriend? Watch and learn, girls."), _("I do this for him anyway. An audience won't change anything."), _("Come here, babe. Let me show off a little.")]))
        python:
            _others = _tod_other_girls(girl)
            for _other in _others:
                set_scene_expression(_other, "surprised", blush=1)
    elif _tj_bf_here:
        $ Narration(_("The room goes silent. Everyone feels the tension."))
        $ set_scene_expression(girl, "embarrassed", blush=2)
        $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice([_("A titjob... with %(po)s right there? This is insane."), _("%(Pp)s is watching me... I can't even look at %(po)s."), _("I'm sorry, %(pn)s... I really am. But a dare is a dare.")])))
        $ Say_Player(renpy.random.choice([_("You don't have to-"), _("Only if you're comfortable-")]))
        $ set_scene_expression(girl, "serious")
        $ Say_Line(girl, renpy.random.choice([_("I already said I'd do it. Don't make it worse."), _("Just... let me get this over with."), _("Too late to back out now.")]))
        python:
            _others = _tod_other_girls(girl)
            for _other in _others:
                set_scene_expression(_other, "surprised", blush=1)
    else:
        $ Narration(_("The room goes quiet again. This is getting intense."))
        if _tj_cute:
            $ set_scene_expression(girl, "embarrassed", blush=2)
        elif _tj_bold:
            $ set_scene_expression(girl, "smirk", blush=1)
        else:
            $ set_scene_expression(girl, "looking_down", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("Seriously? ...Fine. A dare is a dare."), _("You want me to use my boobs? Okay then..."), _("I can't believe this game...")]))
        $ Say_Player(renpy.random.choice([_("You don't have to-"), _("Only if you're comfortable-")]))
        $ set_scene_expression(girl, "serious")
        $ Say_Line(girl, renpy.random.choice([_("Too late. I already said yes."), _("Shut up and let me do this."), _("Don't make it weird. Just... let me handle it.")]))
        python:
            _others = _tod_other_girls(girl)
            for _other in _others:
                set_scene_expression(_other, "surprised", blush=1)

    # Block interruptions during hangout dares
    $ store._interruption_happened = True
    $ store._witness_check_done = True
    $ _scene_exit_flags_reset()  # dares bypass sex_menu; clear scene-exit flags leaked by a prior dare's cum
    call TITJOB_Launch(girl) from _call_TJ_Launch_dare_tj
    call TITJOB_ControlMenu(girl) from _call_TJ_ControlMenu_dare_tj
    call TITJOB_End(girl) from _call_TJ_End_dare_tj
    python:
        for _rg in _hangout_girls_list():
            set_girl_sprite(_rg.gid, pose="standing", at_list=[_hangout_pos_for(_rg)])

    python:
        Change_Status(girl, "Obed", 25)
        Change_Status(girl, "Inbt", 25)
        Change_Status(girl, "Love", 15)
        if not hasattr(girl, "Sex_acts"):
            girl.Sex_acts = {}
        tod_register_cheat_act(girl, "tj")  # also counts Sex_acts["tj"] via mark_intimacy
        if not hasattr(girl, "Sex_act_locations"):
            girl.Sex_act_locations = []
        girl.Sex_act_locations.append({"act": "tj", "location": getattr(store, "CurrentLocation", "room"), "day": getattr(store, "Day", 1)})
        for _w in _hangout_girls_list():
            if _w.gid != girl.gid:
                girl_learns_act(_w, girl, "tj", with_player=True)

    if _tj_cute:
        $ set_scene_expression(girl, "shy", blush=2)
    elif _tj_bold:
        $ set_scene_expression(girl, "smirk", blush=1)
    else:
        $ set_scene_expression(girl, "looking_left", blush=1)
    $ Narration(_("When it's over, [_gn] pulls her top back down and sits back like nothing happened."))
    python:
        for _other in _others:
            set_scene_expression(_other, "smug")
    if store._hangout_is_harem_night:
        $ set_scene_expression(girl, "smirk", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("Beat that, girl~"), _("Mm, I think he enjoyed it. A lot."), _("Who's next?")]))
    elif _tj_is_gf:
        $ set_scene_expression(girl, "smirk", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("That was for my boyfriend. Take notes, girls."), _("See? Girlfriend privileges."), _("Just our regular thing. Nothing to see here.")]))
    else:
        $ set_scene_expression(girl, "bemused", blush=1)
        $ Say_Line(girl, renpy.random.choice([_("Next turn. Now."), _("We're never talking about this again."), _("I need like three drinks after that.")]))

    # GF watches another girl give player a TJ
    python:
        _tj_gf_w = _hangout_find_gf()
        _tj_gf_watching = _tj_gf_w is not None and _tj_gf_w.gid != girl.gid
    if _tj_gf_watching:
        if store._hangout_is_harem_night:
            $ set_scene_expression(_tj_gf_w, "sly")
            $ Say_Line(_tj_gf_w, _tl(renpy.random.choice(_HAREM_GF_TEASE_LINES)))
        else:
            python:
                Change_Status(_tj_gf_w, "Love", -20)
                Change_Status(_tj_gf_w, "Obed", 10)
            $ set_scene_expression(_tj_gf_w, "serious")
            $ Say_Line(_tj_gf_w, renpy.random.choice([
                _("She just used her boobs on my boyfriend. In front of me."),
                _("I watched the whole thing. Every second. We WILL talk later."),
                _("That was way too comfortable for 'just a dare.'"),
            ]))

    # Watchers who can't do TJ react with jealousy/sadness
    python:
        for _w in _hangout_girls_list():
            if _w.gid != girl.gid and not girl_has_pose(_w, "titjob"):
                set_scene_expression(_w, "sad", eyes="eyes_side")
                Say_Line(_w, renpy.random.choice([
                    _("Must be nice to actually be able to do that..."),
                    _("...I could never do that for you."),
                    _("I wish I could do that too."),
                ]))
                set_scene_expression(_w, "normal")

    return
