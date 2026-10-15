# ============================================================
# alcohol.rpy
# Centralized alcohol / drunkenness system.
#
# One source of truth for drinks, the drunkenness meter, and the
# gate-softening bonuses that drunkenness grants during EVENTS.
#
# IMPORTANT design notes:
# - Girls only get drunk inside specific EVENTS (hangout, ToD, party).
#   Nothing here raises drunkenness passively around campus.
# - The meter is backed by the girl's `_hangout_alcohol` field so the
#   existing Truth-or-Dare logic keeps working unchanged; this module
#   just gives it a clean API (add_drunk / get_drunk) and a higher cap.
# - Code keys are GENERIC tiers (low/med/high). The player-facing brand
#   names are per-language and live in _I18N (see script.rpy). Flavor and
#   preference lines always reference the generic type (beer / a middle
#   drink / something strong), never the brand.
# ============================================================

init -5 python:

    # Meter cap. Raised from the old 10 to give events more headroom.
    DRUNK_MAX = 15

    # ---- Drink registry (single source of truth) ---------------------
    # potency = drunkenness points added when the girl drinks one.
    # price   = shop cost. abv = flavor-only alcohol-content string.
    # label   = English brand marker; real display comes from _tr() via _I18N.
    # Multiple brands per tier: potency/price are set by the TIER, brands differ
    # only by name + ABV, so a girl can prefer one specific brand within a tier.
    DRINKS = {
        # LOW tier (beer) — potency +0.8, $50
        "drink_low":   {"tier": "low",  "potency": 0.8, "price": 50,  "abv": "4%",  "label": _("Cools Light Beer")},
        "drink_low2":  {"tier": "low",  "potency": 0.8, "price": 50,  "abv": "5%",  "label": _("Alinmus Beer")},
        # MEDIUM tier — potency +1.4, $70
        "drink_med":   {"tier": "med",  "potency": 1.4, "price": 70,  "abv": "40%", "label": _("Xitos Vodka")},
        "drink_med2":  {"tier": "med",  "potency": 1.4, "price": 70,  "abv": "18%", "label": _("HunterMaster")},
        # HIGH tier — potency +2.0, $120
        "drink_high":  {"tier": "high", "potency": 2.0, "price": 120, "abv": "45%", "label": _("Running Douglas Whiskey")},
        "drink_high2": {"tier": "high", "potency": 2.0, "price": 120, "abv": "50%", "label": _("UnusualAlias Moonshine")},
    }

    # Purchase / serving order = weakest tier first (brands grouped by tier).
    DRINK_IDS = ["drink_low", "drink_low2", "drink_med", "drink_med2", "drink_high", "drink_high2"]

    def drinks_of_tier(tier):
        """All drink ids in a tier (multiple brands per tier)."""
        return [d for d in DRINK_IDS if DRINKS[d]["tier"] == tier]

    # Pre-0.9 saves may still hold the old single "Bottle of Vodka" under id
    # "drinks". Treat it as a medium drink so those bottles still work.
    _LEGACY_DRINK_IDS = ["drinks"]

    def _all_owned_drink_ids():
        return DRINK_IDS + _LEGACY_DRINK_IDS

    def drink_info(drink_id):
        """Registry entry for a drink id, or a medium-tier fallback for legacy ids."""
        d = DRINKS.get(drink_id)
        if d:
            return d
        if drink_id in _LEGACY_DRINK_IDS:
            return DRINKS["drink_med"]
        return None

    def drink_tier_of(drink_id):
        d = drink_info(drink_id)
        return d["tier"] if d else None

    def drink_potency_of(drink_id):
        d = drink_info(drink_id)
        return d["potency"] if d else 0

    # ---- Drunkenness meter (0..DRUNK_MAX), backed by _hangout_alcohol -
    def get_drunk(girl):
        """Current drunkenness level of a girl (0..DRUNK_MAX). Float, so
        fractional tolerance doses accumulate correctly."""
        if girl is None:
            return 0.0
        return float(getattr(girl, "_hangout_alcohol", 0))

    def set_drunk(girl, value):
        if girl is None:
            return
        girl._hangout_alcohol = max(0.0, min(float(DRUNK_MAX), float(value)))
        # Girls are re-created fresh on load and restored from the _girl_save
        # snapshot. set_drunk bypasses Change_Status, so sync explicitly or the
        # value is lost on save/load (the player's is a default var, so it's fine).
        if callable(globals().get("_sync_girl")):
            _sync_girl(girl)
        return girl._hangout_alcohol

    def add_drunk(girl, amount):
        """Raise (or lower) a girl's drunkenness. Clamped to [0, DRUNK_MAX].
        Only call from inside events."""
        return set_drunk(girl, get_drunk(girl) + float(amount))

    def reset_drunk(girl):
        set_drunk(girl, 0)

    # ---- Tiers & gate bonuses ---------------------------------------
    def drunk_tier_name(level):
        """Bucket a raw drunkenness level into a named tier."""
        if level <= 0:
            return "sober"
        if level <= 4:
            return "tipsy"
        if level <= 9:
            return "drunk"
        return "wasted"

    def girl_drunk_tier(girl):
        return drunk_tier_name(get_drunk(girl))

    # Temporary approval boost while intoxicated (read by ApprovalCheck).
    # Mirrors the date_afterglow bonus in scale (afterglow gives +30/+60).
    DRUNK_APPROVAL_BONUS = {"sober": 0, "tipsy": 25, "drunk": 55, "wasted": 90}

    def drunk_approval_bonus(girl):
        return DRUNK_APPROVAL_BONUS.get(girl_drunk_tier(girl), 0)

    # Effective-temptation nudge for the hetero cheat path (read by
    # is_loyalty_blocked). Being drunk lowers her guard.
    DRUNK_CHEAT_TEMPT = {"sober": 0, "tipsy": 1, "drunk": 3, "wasted": 5}

    def drunk_cheat_bonus(girl):
        return DRUNK_CHEAT_TEMPT.get(girl_drunk_tier(girl), 0)

    # At/above this level, a drunk lesbian's stage gate opens temporarily
    # (read by _is_lesbian_stage_blocked). She still has to pass approval.
    DRUNK_LESBIAN_GATE = 6

    # ============================================================
    # Truth-or-Dare "right dose" minigame
    # ============================================================
    # Zones on the 0..DRUNK_MAX meter:
    #   0-4   sober   : alcohol barely helps
    #   5-10  sweet   : good bonuses, no risk (bonus math caps at TOD_SWEET_TOP)
    #   11-13 over    : no extra bonus, rising sick risk
    #   14-15 wasted  : high sick risk, likely taps out
    TOD_SWEET_LOW = 5
    TOD_SWEET_TOP = 10     # bonus-effective alcohol is capped here
    TOD_SICK_START = 11    # sick rolls begin at/above this level

    # Tolerance traits scale how fast the meter fills and how easily she gets sick.
    TOLERANCE_FILL = {"lightweight": 1.3, "normal": 1.0, "heavy_drinker": 0.6}
    def girl_tolerance(girl):
        """'lightweight' / 'heavy_drinker' / 'normal' for a girl (None = normal).
        NPCs are always lightweight. An NPC partner HAS has_trait (ntr, voyeur...), so it is tested by its class
        first: the old has_trait test let him drink at the normal rate, and 'party_must_go_on' / 'secret_party'
        (he passes out at the hangout) almost never happened."""
        if girl is not None and isinstance(girl, NPCPartner):
            return "lightweight"
        if girl is not None and hasattr(girl, "has_trait"):
            if girl.has_trait("lightweight"):
                return "lightweight"
            if girl.has_trait("heavy_drinker"):
                return "heavy_drinker"
            return "normal"
        if girl is not None:
            return "lightweight"
        return "normal"

    def _npc_is_active():
        """True when the NPC partner is present AND conscious."""
        _npc = getattr(store, "_h_npc", None)
        if not _npc:
            _npc = getattr(store, "_hangout_partner_npc", None)
            if _npc:
                store._h_npc = _npc
        return _npc is not None and not getattr(store, "_npc_passed_out", False)

    def tod_effective_alc(girl):
        """Drunkenness used for BONUS math — capped at the sweet-spot top so
        over-drinking gives NO extra bonus (only sick risk)."""
        return min(get_drunk(girl), TOD_SWEET_TOP)

    def tod_effective_alc_val(level):
        """Same cap, for a raw level value (e.g. player alcohol)."""
        return min(float(level), TOD_SWEET_TOP)

    def _tod_bottle_potency():
        """Potency of the bottle the player brought to this hangout (default med)."""
        p = drink_potency_of(getattr(store, "_hangout_brought_drink", None))
        return p if p else 2

    def tod_drink(girl, goles=1):
        """A girl drinks `goles` measures. Amount scales by the brought bottle's
        potency and her tolerance. Returns her new level. EVENT-ONLY."""
        amt = goles * _tod_bottle_potency() * TOLERANCE_FILL.get(girl_tolerance(girl), 1.0)
        lvl = add_drunk(girl, amt)
        print("[TOD] %s drinks %d gole(s): +%.1f -> %.1f" % (getattr(girl, "gid", "?"), goles, amt, lvl))
        return lvl

    def tod_drink_player(goles=1):
        """The player drinks `goles` measures (tolerance = normal)."""
        amt = goles * _tod_bottle_potency()
        cur = getattr(store, "_hangout_player_alcohol", 0)
        store._hangout_player_alcohol = max(0.0, min(float(DRUNK_MAX), cur + amt))
        return store._hangout_player_alcohol

    def tod_zone(level):
        if level <= 4:
            return "sober"
        if level <= TOD_SWEET_TOP:
            return "sweet"
        if level <= 13:
            return "over"
        return "wasted"

    def tod_bar_color(level):
        """Zone color for the drunk bar HUD."""
        return {"sober": "#eab308", "sweet": "#22c55e",
                "over": "#f97316", "wasted": "#ef4444"}.get(tod_zone(level), "#22c55e")

    def tod_rolls_sick(girl):
        return get_drunk(girl) >= DRUNK_MAX

    def tod_player_rolls_sick():
        return getattr(store, "_hangout_player_alcohol", 0) >= DRUNK_MAX

    def tod_bar_data():
        """[(level, label, color), ...] for the HUD: player + present girls.
        Label = girl initial / 'YOU'; color = each girl's signature color."""
        out = [(getattr(store, "_hangout_player_alcohol", 0), _tr("You").upper(), "#93c5fd")]
        for _g in _hangout_girls_list():
            _init = (getattr(_g, "Name", "?")[:1] or "?").upper()
            out.append((get_drunk(_g), _init, getattr(_g, "color", "#e2e8f0")))
        _bf = getattr(store, "_hangout_partner_npc", None)
        if not _bf:
            _bf = getattr(store, "_h_npc", None)
        print("[TOD_BAR] _hangout_partner_npc=%s _h_npc=%s _bf=%s" % (
            getattr(store, "_hangout_partner_npc", "MISSING"),
            getattr(store, "_h_npc", "MISSING"),
            _bf))
        if _bf:
            if getattr(store, "_npc_passed_out", False):
                out.append((get_drunk(_bf), "X", "#555555"))
            else:
                _binit = (getattr(_bf, "Name", "?")[:1] or "?").upper()
                out.append((get_drunk(_bf), _binit, getattr(_bf, "color", "#b0bec5")))
        return out

    # ---- Player-owned drinks ----------------------------------------
    def player_has_any_drink():
        return any(store.Player.get_item_count(d) > 0 for d in _all_owned_drink_ids())

    def player_total_drinks():
        return sum(store.Player.get_item_count(d) for d in _all_owned_drink_ids())

    def player_owned_drinks():
        """[(drink_id, count), ...] the player currently holds, weakest first."""
        out = []
        for d in _all_owned_drink_ids():
            c = store.Player.get_item_count(d)
            if c > 0:
                out.append((d, c))
        return out

    def player_consume_drink(drink_id=None):
        """Remove one drink from the player's inventory and return its id.
        If drink_id is None (or not owned), consumes the weakest available.
        Returns None if the player has no drinks."""
        if drink_id and store.Player.get_item_count(drink_id) > 0:
            store.Player.remove_item(drink_id, 1)
            return drink_id
        for d in _all_owned_drink_ids():
            if store.Player.get_item_count(d) > 0:
                store.Player.remove_item(d, 1)
                return d
        return None

    def serve_drink(girl, drink_id=None):
        """Player-initiated pour: consume one drink from inventory, raise the
        girl's drunkenness by its potency, soften the lesbian gate, and react to
        how well the drink matches her taste. EVENT-ONLY.

        match: "brand" (her exact favorite brand), "tier" (right type but wrong
        brand -> she hints she prefers another), or "none". Returns
        {id, tier, potency, match, drunk} or None if nothing to serve."""
        served = player_consume_drink(drink_id)
        if served is None:
            return None
        info = drink_info(served)
        tier = info["tier"]
        potency = info["potency"]
        add_drunk(girl, potency)

        fav_tier = getattr(girl, "FavoriteDrink", None)
        fav_brand = getattr(girl, "FavoriteBrand", None)
        if fav_brand and served == fav_brand:
            match = "brand"
        elif fav_tier and tier == fav_tier:
            match = "tier"
        else:
            match = "none"

        if match == "brand":
            # Her exact brand: reveals both tier + brand and pleases her most.
            if hasattr(girl, "discover"):
                girl.discover("discovered_fav_drink")
                girl.discover("discovered_fav_brand")
            if callable(globals().get("Change_Status")):
                Change_Status(girl, "Love", 4)
        elif match == "tier":
            # Right type, wrong brand: reveals the tier; she hints at her brand.
            if hasattr(girl, "discover"):
                girl.discover("discovered_fav_drink")
            if callable(globals().get("Change_Status")):
                Change_Status(girl, "Love", 2)

        # Alcohol temporarily shifts spectrum toward center (feeds
        # threshold formula via _effective_spectrum; auto-resets nightly).
        girl.apply_spectrum_temp_shift(potency * 3)

        print("[ALCOHOL] served %s (tier=%s pot=%d match=%s) to %s -> drunk=%d"
              % (served, tier, potency, match, girl.gid, get_drunk(girl)))
        return {"id": served, "tier": tier, "potency": potency,
                "match": match, "drunk": get_drunk(girl)}

    # ---- Flavor lines -----------------------------------------------
    # Her reaction to the drink she's just been served, by generic tier.
    DRINK_FLAVOR_LINES = {
        "low": [
            _("Mm, a nice cold beer. Easy and refreshing."),
            _("Beer's always a safe bet. I could sip this all night."),
        ],
        "med": [
            _("A decent middle ground. Good and cheap, haha."),
            _("Ooh, this one's got a kick. Not bad at all."),
        ],
        "high": [
            _("Whoa, this one's strong! Help!"),
            _("That burns going down... okay, that's the good stuff."),
        ],
    }

    def drink_flavor_line(tier):
        pool = DRINK_FLAVOR_LINES.get(tier) or DRINK_FLAVOR_LINES["low"]
        return _tl(renpy.random.choice(pool))

    # Served her EXACT favorite brand.
    DRINK_FAVORITE_BRAND_LINES = [
        _("This is exactly my brand! You actually remembered."),
        _("Oh, you got me the good stuff. This is my brand."),
    ]

    # Right type, WRONG brand — she hints she prefers a different one.
    DRINK_WRONG_BRAND_LINES = [
        _("Aw, I like this, but honestly I prefer another brand."),
        _("It's fine, though I've got a brand I like better than this one."),
    ]

    def drink_served_line(match, tier):
        """Line she says when handed a drink, keyed by how well it matches her taste."""
        if match == "brand":
            return _tl(renpy.random.choice(DRINK_FAVORITE_BRAND_LINES))
        if match == "tier":
            return _tl(renpy.random.choice(DRINK_WRONG_BRAND_LINES))
        return drink_flavor_line(tier)

    # ---- Reaction to a specific bottle brought to an event ------------
    # Loved tier + exact brand = best; loved tier + other brand = good;
    # hated tier (any brand) = bad; anything else = neutral.
    def drink_reaction(girl, drink_id):
        """'love_brand', 'love_tier', 'hate', or 'neutral'."""
        info = drink_info(drink_id)
        if not info:
            return "neutral"
        tier = info["tier"]
        if getattr(girl, "FavoriteDrink", None) == tier:
            if getattr(girl, "FavoriteBrand", None) == drink_id:
                return "love_brand"
            return "love_tier"
        if getattr(girl, "HatedDrink", None) == tier:
            return "hate"
        return "neutral"

    # Acceptance-chance delta the brought bottle applies (hangout invite, etc.)
    DRINK_ACCEPT_MOD = {"love_brand": 0.30, "love_tier": 0.18, "neutral": 0.0, "hate": -0.22}

    def drink_accept_mod(girl, drink_id):
        return DRINK_ACCEPT_MOD.get(drink_reaction(girl, drink_id), 0.0)

    # "a case of X" / "a bottle of X" for the invite message.
    DRINK_BRING_TEMPLATE = {"low": _("a case of %s"), "med": _("a bottle of %s"), "high": _("a bottle of %s")}

    def drink_bring_phrase(drink_id):
        """Natural phrase naming the bottle the player brings (translated)."""
        info = drink_info(drink_id)
        if not info:
            return _tl(_("some drinks"))
        tmpl = DRINK_BRING_TEMPLATE.get(info["tier"], DRINK_BRING_TEMPLATE["med"])
        return _tl(tmpl) % _tr(info["label"])

    # What she opens with when she hears what you're bringing.
    DRINK_INVITE_REACT = {
        "love_brand": [
            _("Wait, %s?! That's literally my brand."),
            _("Is that %s? You clearly know me."),
        ],
        "love_tier": [
            _("Ooh, that's exactly my kind of drink."),
            _("Mmm, I actually love that stuff."),
        ],
        "hate": [
            _("Ugh, that's really not my thing..."),
            _("Not gonna lie, I can't stand that stuff."),
        ],
    }

    def drink_event_greeting(girl, drink_id):
        """Bringing a bottle to an event CONFIRMS her feeling (discovery). Returns
        the reaction sentence she opens with (translated), or '' if neutral."""
        cat = drink_reaction(girl, drink_id)
        # Confirmation: loving the bottle reveals the preference for certain.
        if cat in ("love_brand", "love_tier") and hasattr(girl, "discover"):
            girl.discover("discovered_fav_drink")
            if cat == "love_brand":
                girl.discover("discovered_fav_brand")
        if cat not in DRINK_INVITE_REACT:
            return ""
        line = _tl(renpy.random.choice(DRINK_INVITE_REACT[cat]))
        if "%s" in line:
            info = drink_info(drink_id)
            line = line % (_tr(info["label"]) if info else _tr("Drinks"))
        return line

    # Preference chit-chat: she hints at the kind of drink she likes, by tier.
    DRINK_PREF_LINES = {
        "low": [
            _("It's so hot today... I'd kill for an ice-cold beer right now."),
            _("Honestly? A cold beer on a day like this is all I want."),
        ],
        "med": [
            _("I could really go for a good drink to take the edge off tonight."),
            _("Something with a little kick, nothing too crazy. That's my sweet spot."),
        ],
        "high": [
            _("My day was hell... I'd love something really strong right now."),
            _("Pour me something that actually burns. I've earned it today."),
        ],
    }
