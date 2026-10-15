init python:

    # ================================================================
    # FINANCIAL DIALOGUE SYSTEM
    # Dict-based dialogue with girl-specific overrides.
    # Pattern mirrors rod_lines/rod_pick_line: Global + per-girl.
    #
    # Usage:
    #   _fin_line(girl, "opener_s0_c0")
    #   _fin_line(girl, "price_s1", fmt={"price": 130, "act": "give you a handjob"})
    #   _fin_line(girl, "opener_cheat_s0", tk=_fin_partner_key(girl))
    #   _fin_line(girl, "girl_init", fmt=fmt, tk=_fin_girl_init_key(girl))
    # ================================================================

    def _fin_trait_key(girl, femdom=False):
        """Her trait key. femdom=True builds the femdom key instead (les_fd / poor_fd / rich_fd / fd): the same
        chain with femdom checked before hardcore_sex (orders are femdom, not hardcore: docs/plan_femdom.md D3)."""
        _les = girl.has_trait("lesbian")
        _poor = girl.has_trait("poor")
        _rich = girl.has_trait("rich")
        _cute = girl.has_trait("cute_sex")
        _hc = girl.has_trait("hardcore_sex")
        _fd = femdom and girl.has_trait("femdom")
        if _les:
            if _poor: return "les_poor"
            if _rich: return "les_rich"
            if _cute: return "les_cute"
            if _fd: return "les_fd"
            if _hc: return "les_hc"
            return "les"
        if _poor:
            if _fd: return "poor_fd"
            if _hc: return "poor_hc"
            return "poor"
        if _rich:
            if _fd: return "rich_fd"
            if _hc: return "rich_hc"
            return "rich"
        if _cute: return "cute"
        if _fd: return "fd"
        if _hc: return "hc"
        return "default"

    def _fin_partner_key(girl):
        if not (hasattr(girl, "has_npc_partner") and girl.has_npc_partner()):
            return None
        _les = girl.has_trait("lesbian")
        _pf = girl.get_flag("partner_is_female")
        if _les and _pf: return "les_gf"
        if _les: return "les_bf"
        if girl.has_trait("poor"): return "poor_bf"
        if girl.has_trait("rich"): return "rich_bf"
        return "het_bf"

    def _fin_girl_init_key(girl):
        _les = girl.has_trait("lesbian")
        _hp = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _pf = girl.get_flag("partner_is_female") if _hp else False
        if _les and _hp and _pf: return "les_gf"
        if _les and _hp: return "les_bf"
        if _les and girl.has_trait("poor"): return "les_poor"
        if _les and girl.has_trait("rich"): return "les_rich"
        if _les: return "les"
        if _hp: return "het_bf"
        if girl.has_trait("poor") and girl.has_trait("hardcore_sex"): return "poor_hc"
        if girl.has_trait("poor"): return "poor"
        if girl.has_trait("rich") and girl.has_trait("hardcore_sex"): return "rich_hc"
        if girl.has_trait("rich"): return "rich"
        if girl.has_trait("cute_sex"): return "cute"
        if girl.has_trait("hardcore_sex"): return "hc"
        return "default"

    def _fin_lookup(pool, tk):
        # records which key answered (store._fin_hit_tk): "default" is no trait evidence
        if tk in pool:
            store._fin_hit_tk = tk
            return pool[tk]
        if "_" in tk:
            base = tk.split("_", 1)[0]
            if base in pool:
                store._fin_hit_tk = base
                return pool[base]
        store._fin_hit_tk = "default"
        return pool.get("default")

    def _fin_format(entry, girl, fmt):
        line = renpy.random.choice(entry) if isinstance(entry, list) else entry
        _en = line
        line = _tl(line)
        if "%(" in line:
            # every partner key (partner_fmt: the Russian case forms too; %(partner)s = his name, else the label),
            # under the scene's own keys (act, price...)
            fdict = {}
            if hasattr(girl, "has_npc_partner") and girl.has_npc_partner():
                fdict.update(partner_fmt(girl))
                fdict["partner"] = getattr(girl, "_npc_partner_name", None) or girl.partner_label()
            if fmt:
                fdict.update(fmt)
            if fdict:
                line = fmt_safe(line, fdict, _en)
        return line

    def _fin_extra_trait_key(girl, extra_type):
        _poor = girl.has_trait("poor")
        _rich = girl.has_trait("rich")
        if extra_type in ("creampie", "condom_remove"):
            if girl.has_trait("cum_slut"):
                return "cum_slut_poor" if _poor else "cum_slut"
            if girl.has_trait("hate_cum"):
                if _poor: return "hate_cum_poor"
                if _rich: return "hate_cum_rich"
                return "hate_cum"
        elif extra_type == "recording":
            if girl.has_trait("camera_lover"):
                return "camera_lover_poor" if _poor else "camera_lover"
            if girl.has_trait("camera_hater"):
                if _poor: return "camera_hater_poor"
                if _rich: return "camera_hater_rich"
                return "camera_hater"
        return _fin_trait_key(girl)

    def _fin_line(girl, key, fmt=None, tk=None):
        # A femdom key only counts where the pool has exactly that entry; anywhere else she keeps her usual key
        # (a femdom + hardcore girl still gets the _hc lines, never the plain fallback of an unwritten _fd key).
        _fdk = None
        if tk is None:
            tk = _fin_trait_key(girl)
            _fdk = _fin_trait_key(girl, femdom=True)
            if _fdk == tk:
                _fdk = None
        gid = getattr(girl, "gid", None)
        store._fin_hit_tk = "default"
        if gid and gid in _FINANCIAL_GIRL_LINES:
            gblock = _FINANCIAL_GIRL_LINES[gid].get(key)
            if gblock:
                if _fdk in gblock:
                    store._fin_hit_tk = _fdk
                    result = gblock[_fdk]
                else:
                    result = _fin_lookup(gblock, tk)
                if result is not None:
                    if key.startswith("opener") and not key.startswith("opener_cheat"):
                        store._fin_opener_tk = store._fin_hit_tk
                    return _fin_format(result, girl, fmt)
        pool = _FINANCIAL_LINES.get(key)
        if pool:
            if _fdk in pool:
                debug_log("[FIN_LINE] femdom key=%s tk=%s gid=%s" % (key, _fdk, gid))
                store._fin_hit_tk = _fdk
                result = pool[_fdk]
            else:
                result = _fin_lookup(pool, tk)
            if result is not None:
                if key.startswith("opener") and not key.startswith("opener_cheat"):
                    store._fin_opener_tk = store._fin_hit_tk
                return _fin_format(result, girl, fmt)
        debug_log("[FIN_LINE] MISS key=%s tk=%s gid=%s" % (key, tk, gid))
        return "..."

    # ════════════════════════════════════════════════════════
    # DIALOGUE DATA
    # ════════════════════════════════════════════════════════

    _FINANCIAL_LINES = {

        # ──────────────────────────────────────
        # NEVER BUYABLE (GIRL_FINANCIAL_CONFIG "never_buyable", _financial_attempt's first gate): money gets
        # him nothing but her contempt, whatever the act or his cash (author, 2026-10-09: the stepmom CEO).
        # The femdom keys ("fd" / "rich_fd") win for a femdom girl, _fin_line's usual chain.
        # ──────────────────────────────────────

        "never_buyable": {
            "rich_fd": [
                _("Money? Sweetheart, I sign checks bigger than your tuition before breakfast. Put it away and apologize, that's the only currency you own."),
                _("You're trying to BUY me? Adorable. I could buy the building you sleep in. Keep the cash, you'll need it for therapy after tonight."),
            ],
            "fd": [
                _("You think I can be rented? Oh, that's precious. Put it away before I decide to make you regret the thought."),
            ],
            "rich": [
                _("I make more in an hour than you're holding right now. This is embarrassing. For you, I mean."),
            ],
            "default": [
                _("You think money fixes that? Put it away. This is just sad."),
            ],
        },

        # ──────────────────────────────────────
        # MID-SCENE PAID EXTRAS
        # ──────────────────────────────────────

        "midscene_creampie_paid": {
            "cum_slut":      _("Inside me? I'd want that anyway. Give me $%(price)d and it's yours."),
            "cum_slut_poor": _("Cum inside AND pay me $%(price)d? Best deal I've ever made."),
            "hate_cum":      _("Cum INSIDE me?! I'd need at least $%(price)d for that. And I'll hate every second."),
            "hate_cum_poor": _("Inside me... I hate it. But $%(price)d is $%(price)d. Fine."),
            "hate_cum_rich": _("You want to cum inside ME? That would cost you at least $%(price)d. And I still won't enjoy it."),
            "poor":          _("Inside? ...I'd do it for $%(price)d. I need the money."),
            "rich":          _("Cum inside? That'll cost you $%(price)d. Non-negotiable."),
            "les":           _("Finish inside a lesbian...? It would take $%(price)d to make me agree."),
            "les_poor":      _("A man cumming inside me... $%(price)d. I need the money."),
            "cute":          _("I-inside me? I'd need at least $%(price)d for that..."),
            "hc":            _("Creampie? $%(price)d and go ahead."),
            "default":       _("If you want to finish inside... $%(price)d. That's my price."),
        },

        "midscene_condom_paid": {
            "cum_slut":      _("Take the condom off? I was hoping you'd ask. $%(price)d and it's gone."),
            "cum_slut_poor": _("No condom AND you pay me $%(price)d? Deal. Take it off."),
            "hate_cum":      _("Go raw?! I'd need at least $%(price)d. And don't you DARE cum inside after."),
            "hate_cum_poor": _("No condom... I hate it. But $%(price)d... I need the cash. Fine."),
            "hate_cum_rich": _("Take the condom off? Disgusting. $%(price)d minimum. And don't push it further."),
            "poor":          _("Go raw? ...$%(price)d and you can take it off."),
            "rich":          _("No condom? That's $%(price)d for the risk. Take it or leave it."),
            "les":           _("Raw with a man... $%(price)d. That's what it'll take."),
            "les_poor":      _("No condom with a guy... $%(price)d. I need the money."),
            "cute":          _("W-without a condom? I'd need at least $%(price)d..."),
            "hc":            _("Go raw? $%(price)d. Take it off."),
            "default":       _("If you want the condom off... $%(price)d. That's my price."),
        },

        "midscene_combo_paid": {
            "cum_slut":      _("Raw AND inside? For $%(price)d? You don't even have to ask twice."),
            "cum_slut_poor": _("Raw and cum inside AND you pay me $%(price)d? This is too good to be true."),
            "hate_cum":      _("Take it off AND cum inside?! I'd need at least $%(price)d. And I'll hate every second."),
            "hate_cum_poor": _("Raw and inside... I hate everything about this. But $%(price)d... fine."),
            "hate_cum_rich": _("Both?! That would cost you $%(price)d. And I still won't enjoy it."),
            "poor":          _("Condom off and cum inside? ...$%(price)d and it's yours."),
            "rich":          _("Both? That's $%(price)d. Non-negotiable."),
            "les":           _("Raw and inside from a man... $%(price)d. That's what it takes."),
            "les_poor":      _("No condom and cum inside... $%(price)d. I need the money."),
            "cute":          _("B-both?! I'd need at least $%(price)d for that..."),
            "hc":            _("Raw and inside? $%(price)d. Deal."),
            "default":       _("Condom off and finish inside? ...$%(price)d. That's my price."),
        },

        "midscene_recording_paid_hidden": {
            "camera_lover":      _("Record me? I'd almost do it for free. Give me $%(price)d and we have a deal."),
            "camera_lover_poor": _("You want to film me? I love cameras AND money. $%(price)d and I'm all yours."),
            "camera_hater":      _("You want to FILM me?! ...I'd need at least $%(price)d. And I'm looking away the whole time."),
            "camera_hater_poor": _("Film me... I HATE cameras. But for $%(price)d... I need the money. Fine."),
            "camera_hater_rich": _("Record me? Ugh. I'd need at least $%(price)d. And don't expect me to enjoy it."),
            "poor":              _("Record me? ...I'd do it for $%(price)d. I need the money."),
            "rich":              _("If you want to record, it'll cost you $%(price)d. Take it or leave it."),
            "les":               _("Film a lesbian doing this with a man... it'll cost you $%(price)d."),
            "les_poor":          _("Film this? ...Give me $%(price)d and fine."),
            "cute":              _("R-record?! I... I'd need at least $%(price)d for that..."),
            "hc":                _("Record? Sure. $%(price)d and we have a deal."),
            "default":           _("If you want to record... $%(price)d. That's my price."),
        },

        "midscene_recording_paid_full": {
            "camera_lover":      _("The full thing on camera? I don't even mind. $%(price)d and record whatever you want."),
            "camera_lover_poor": _("Film everything? For $%(price)d I'll even pose for you. Let's go."),
            "camera_hater":      _("Record EVERYTHING?! ...It would take at least $%(price)d to make me agree to that."),
            "camera_hater_poor": _("The whole thing on camera... I hate this. But $%(price)d is $%(price)d. Fine."),
            "camera_hater_rich": _("You want the full thing filmed? $%(price)d. And I still hate every second of it."),
            "poor":              _("Everything on camera? ...I'd need $%(price)d for that. I really need the money."),
            "rich":              _("The full recording? That's going to cost you $%(price)d. Non-negotiable."),
            "les":               _("A full recording of a lesbian with a man... $%(price)d. That's what it'll take."),
            "les_poor":          _("Record all of it? ...$%(price)d. At this point, what's one more thing."),
            "cute":              _("A full recording...? I'd need at least $%(price)d... and promise me you won't share it."),
            "hc":                _("Full shoot? $%(price)d. Make sure you get my good side."),
            "default":           _("If you want the full thing on camera... $%(price)d. That's my price."),
        },

        # ──────────────────────────────────────
        # TIER PROGRESSION — flavor lines before post-accept
        # ──────────────────────────────────────

        "tier_advance": {
            "poor":    _("This is... more than we've done before. But for that money... okay."),
            "les":     _("You want me to go further? With a man? ...The money better be worth it."),
            "les_poor": _("Further than before... with a guy... for cash. I hate everything about this. ...Okay."),
            "cute":    _("That's... a big step up from what we've done. I'm nervous... but okay."),
            "hc":      _("Stepping it up, huh? Fine. I can handle it."),
            "rich":    _("This is further than before. You're lucky I find this arrangement... interesting."),
            "default": _("This is more than we've done before. I hope you know that."),
        },

        "tier_normalize": {
            "poor":    _("Same as last time? Sure. You know the price."),
            "les":     _("Again? ...At this point it's just routine. Fine."),
            "cute":    _("The same thing as before...? At least I know what to expect now."),
            "hc":      _("Again? You liked it that much? Fine, let's go."),
            "rich":    _("The usual arrangement? Very well."),
            "default": _("Same as before? Okay. At least I know what I'm getting into."),
        },

        "tier_first_penetrative": {
            "poor":    _("Sex? For money? I... I never thought I'd... okay. I need the money."),
            "les":     _("You want a lesbian to have sex with you for money. Let that sink in. ...Fine."),
            "les_poor": _("Sex with a man. For cash. I'm a lesbian prostitute now. ...Just do it."),
            "cute":    _("We're really going to... have sex? This isn't just touching anymore... I'm scared."),
            "hc":      _("So we're doing this for real now? Sex? Fine. Don't hold back."),
            "rich":    _("Actual sex. This just became a very different kind of arrangement."),
            "default": _("Sex. For money. This is really happening. ...Okay. Let's just do this."),
        },

        "tier_virginity_sold": {
            "poor":    _("I'm selling my {hint}virginity{/hint}. I never imagined this is how it would happen... but I need the money so badly..."),
            "les":     _("A lesbian losing her {hint}virginity{/hint} to a man for money. I can't even process how wrong this is."),
            "les_poor": _("I'm giving my {hint}virginity{/hint} to a man. For cash. A lesbian's first time... sold. I hate everything about this."),
            "cute":    _("My... my {hint}first time{/hint}... I always imagined it would be special... not like this... not for money..."),
            "hc":      _("You're paying for my {hint}virginity{/hint}? Fine. At least make it worth the price."),
            "rich":    _("My {hint}virginity{/hint} for money I don't even need. I must be losing my mind."),
            "default": _("I can't believe I'm doing this. My {hint}first time{/hint}... for money. There's no taking this back."),
        },

        # ──────────────────────────────────────
        # RICH GATE — she refuses cash (not enough gifts yet)
        # ──────────────────────────────────────

        "rich_gate_refuse": {
            "rich":    _("Save your money for tomorrow's lunch. {hint}You don't have enough to buy me{/hint}."),
            "rich_hc": _("That's cute. {hint}I spend more on coffee{/hint} than whatever you're about to offer. Don't waste my time."),
            "les_rich": _("A man offering me pocket change? I'm a lesbian who {hint}can buy and sell you{/hint}. Get lost."),
            "default": _("{hint}You couldn't afford me{/hint} on your best day. Put your wallet away, it's embarrassing."),
        },

        # Generic gift gate (_financial_attempt): the money option is never hidden, she refuses until his gifts
        # prove he's serious (the narration right after points at the gifts)
        "gift_gate_refuse": {
            "les":      _("Cash? From a guy? I don't even know if you're serious. You haven't shown me anything."),
            "les_poor": _("I could use the money... but I don't trust a guy waving cash around. Show me you're serious first."),
            "poor":     _("I'm not taking random cash from you. ...Show me you're actually serious first."),
            "default":  _("Money? Just like that? I don't even know if you mean it. Prove you're serious first."),
        },

        # ──────────────────────────────────────
        # PARTNER PRESENT — financial with partner nearby
        # ──────────────────────────────────────

        "partner_present_refuse": {
            "les":     _("Are you insane? My %(pl)s is RIGHT HERE. No amount of money would make me do that with a man in front of %(po)s."),
            "les_poor": _("I need money but... my %(pl)s is right there. I can't. Not in front of %(po)s. Not for any price."),
            "cute":    _("My %(pl)s is right there! I... no! I could never do that with %(po)s watching! Please don't ask me that..."),
            "hc":      _("With my %(pl)s standing right there? You've lost your mind. Not happening."),
            "poor":    _("I need the cash, I really do... but my %(pl)s is RIGHT THERE. I can't... not like this."),
            "default": _("Money won't help you here. My %(pl)s is right there. I'm not that far gone."),
        },

        "partner_present_premium": {
            "les":     _("In front of my %(pl)s...? With a man...? For money...? ...You'd have to pay me triple. And I might still say no."),
            "cute":    _("With %(pl)s watching...? That's... I feel sick just thinking about it. It would have to be a LOT of money..."),
            "hc":      _("In front of my %(pl)s? That's bold. It's going to cost you. A lot."),
            "poor":    _("My %(pl)s is right there... but I need the money so bad... it would have to be way more than usual."),
            "default": _("With my %(pl)s watching? You're out of your mind. That's going to cost triple. At least."),
        },

        # ──────────────────────────────────────
        # OPENER — Player offers money
        # ──────────────────────────────────────

        "opener_s0_c0": {
            "les_poor": _("Money? To touch a man? ...How much? I hate that I'm even asking."),
            "les_rich": _("Money? I'm a lesbian AND {hint}I don't need your cash{/hint}. You'd have to offer a fortune."),
            "les_cute": _("Y-you're offering me money to... with a man...? Are you serious right now?"),
            "les_hc": _("You're trying to PAY a lesbian to do stuff with you? Wow. Just... wow."),
            "les": _("Money? You think money will make a lesbian want to touch a man? ...How much?"),
            "poor_hc": _("You're offering to pay? For real? I mean... I wouldn't mind. How much?"),
            "poor": _("Money? I... {hint}I really need it{/hint}... but how much are we talking?"),
            "rich_hc": _("Pay me? I don't need it, but the idea is... interesting. How much?"),
            "rich": _("You're trying to BUY me? {hint}I don't need your money{/hint}. But amuse me. How much?"),
            "cute": _("W-what...? You're offering me money to... I'm not that kind of girl..."),
            "hc": _("You're seriously trying to buy me? That's bold. And stupid."),
            "default": _("You want to pay me? For... that? I... are you serious?"),
        },

        "opener_s0_c1": {
            "les_poor": _("Again... I promised myself never again. But the bills don't care about promises."),
            "les_rich": _("You're back? My price went up. I don't do this because I need to."),
            "les": _("Again...? A lesbian, selling herself to a man... twice. What is my life."),
            "poor_hc": _("Round two? Fine by me. Same deal as before?"),
            "poor": _("Again...? I was hoping {hint}I wouldn't need to do this{/hint} anymore... how much?"),
            "rich_hc": _("Back again? Sure, I could use the entertainment. What's the deal?"),
            "rich": _("You came back? I'm surprised you can afford me twice. What's the number?"),
            "cute": _("Again...? I told myself last time was the only time..."),
            "hc": _("Back for more? At least you're consistent. What's the offer?"),
            "default": _("Again? I said last time was a one-time thing... how much?"),
        },

        "opener_s0_c2": {
            "les_poor": _("At this point it's a job. A job I hate. But a job that pays the bills."),
            "les_rich": _("This again? You must really want a lesbian. Fine, but the price keeps going up."),
            "les": _("Third time a man is paying me for... I've stopped pretending this isn't a pattern."),
            "poor_hc": _("We have a good thing going. What's the number this time?"),
            "poor": _("I'm not even surprised anymore. How much? {hint}I can't afford my textbooks{/hint}."),
            "rich_hc": _("Same arrangement. I don't do this for the money. What do you want?"),
            "rich": _("At this rate I should charge you double. What's the offer?"),
            "cute": _("I keep saying never again and here I am... how much this time?"),
            "hc": _("Fine. We both know how this works by now. Name your price, I name mine."),
            "default": _("At this point we have a routine, don't we? ...How much?"),
        },

        "opener_s1": {
            "les_poor": _("I know why you're here. And I know I need the cash. Just... name the price."),
            "les_rich": _("Fine. My rates are premium. A lesbian with standards doesn't come cheap."),
            "les": _("Fine. I know the routine by now. A lesbian, selling herself... what else is new."),
            "poor_hc": _("Cash for a good time? Works for me. What are we doing?"),
            "poor": _("I already know why you're here. How much? {hint}I could really use it{/hint}."),
            "rich_hc": _("Skip the formalities. What do you want and what's the budget?"),
            "rich": _("My time is expensive. You know that. What's the offer?"),
            "cute": _("I already know what you're going to say... how much this time?"),
            "hc": _("Skip the pitch. How much?"),
            "default": _("Let me guess... same arrangement? ...How much?"),
        },

        "opener_s23": {
            "les_poor": _("The usual? Good, I've got bills to pay. Let's hear it."),
            "les_rich": _("I know the routine. I don't need the money, but it's become our thing."),
            "les": _("I already know. Let's talk numbers."),
            "poor_hc": _("Always happy to do business. What do you need?"),
            "poor": _("Same deal? Good. What's the job and what's it pay?"),
            "rich_hc": _("Let's do this. Not for the money, obviously. What do you want?"),
            "rich": _("This again? Fine. I set the price, though."),
            "cute": _("Okay... what do you need? And how much are you offering?"),
            "hc": _("Straight to business. I like that. What's the job?"),
            "default": _("Right. What are we doing and how much?"),
        },

        # ──────────────────────────────────────
        # OPENER — Cheating follow-up
        # tk = _fin_partner_key(girl)
        # ──────────────────────────────────────

        "opener_cheat_s0": {
            "les_gf": _("If %(pp)s ever finds out I'm doing things with a man for money... %(pp)s would never forgive me."),
            "les_bf": _("I have a %(pl)s, you know that? And here I am... selling myself to another man."),
            "default": _("I have a %(pl)s... if %(pp)s finds out I'm doing this for cash... God, what am I doing."),
        },

        "opener_cheat_s1": {
            "les_gf": _("%(Pp)s thinks I'm studying right now... not getting paid to be with a man."),
            "les_bf": _("My %(pl)s would lose it if %(pp)s knew about this. Whatever. Money is money."),
            "default": _("My %(pl)s has no idea I do this. Let's keep it that way."),
        },

        "opener_cheat_s23": {
            "les_gf": _("%(Pp)s stopped asking where the extra money comes from. Probably better that way."),
            "les_bf": _("My %(pl)s is clueless. And honestly? I've stopped caring."),
            "default": _("Don't worry about my %(pl)s. %(Pp)s doesn't know and never will."),
        },

        # ──────────────────────────────────────
        # PRICE NAMING
        # fmt = {"price": int, "act": str, "act_cap": str}
        #
        # NOTE: In Stage 0, poor/rich are checked BEFORE les.
        # les_poor and les_rich entries duplicate the poor/rich text
        # so the fallback chain (les_poor -> les) doesn't misroute.
        # ──────────────────────────────────────

        "price_s0_first": {
            "les_poor": _("I... I really shouldn't... but $%(price)d would help a lot right now... fine. $%(price)d. To %(act)s."),
            "les_rich": _("You think I'm cheap? If you want me to %(act)s, it's going to cost you. $%(price)d. Minimum."),
            "les": _("You want a lesbian to %(act)s for money? ...$%(price)d. And don't you dare tell anyone."),
            "poor": _("I... I really shouldn't... but $%(price)d would help a lot right now... fine. $%(price)d. To %(act)s."),
            "rich": _("You think I'm cheap? If you want me to %(act)s, it's going to cost you. $%(price)d. Minimum."),
            "cute": _("I can't believe I'm saying this... $%(price)d. To %(act)s. And nobody ever finds out."),
            "hc": _("$%(price)d. To %(act)s. Take it or leave it. Non-negotiable."),
            "default": _("...$%(price)d. To %(act)s. And we never talk about this."),
        },

        "price_s0_repeat": {
            "les_poor": _("$%(price)d. Same as always. I need the money."),
            "les_rich": _("$%(price)d. And don't try to negotiate. I don't need your money that badly."),
            "les": _("$%(price)d. You know the drill. Pay up and keep your mouth shut."),
            "poor": _("$%(price)d. Same as always. I need the money."),
            "rich": _("$%(price)d. And don't try to negotiate. I don't need your money that badly."),
            "cute": _("$%(price)d... and please stop looking at me like that."),
            "hc": _("$%(price)d. You know the terms."),
            "default": _("$%(price)d. Same deal as before."),
        },

        "price_s1": {
            "les": _("$%(price)d. To %(act)s... with a man. You know the price."),
            "poor": _("$%(price)d... to %(act)s. I need the money, so..."),
            "rich": _("$%(price)d. If you want me to %(act)s, that's the rate."),
            "cute": _("$%(price)d... to %(act)s. You already know I'll say yes..."),
            "hc": _("$%(price)d. To %(act)s. Same terms as before."),
            "default": _("$%(price)d to %(act)s. Same as last time."),
        },

        "price_s23": {
            "les": _("$%(price)d to %(act)s. You know the terms."),
            "poor": _("$%(price)d? To %(act)s. That works for me."),
            "rich": _("$%(price)d. To %(act)s. Fair price."),
            "cute": _("$%(price)d... to %(act)s. If that's okay with you."),
            "hc": _("$%(price)d. %(act_cap)s. Non-negotiable."),
            "default": _("$%(price)d to %(act)s. Standard rate."),
        },

        # ──────────────────────────────────────
        # POST-ACCEPT
        # ──────────────────────────────────────

        "postaccept_s0_c0": {
            "les_poor": _("I need this money... but doing this with a man... I hate every second already. Just hurry up."),
            "les_rich": _("I can't believe I agreed to this. I don't even need the money. What is wrong with me."),
            "les": _("I can't believe I'm doing this for money... with a man... just get it over with."),
            "poor_hc": _("Paid and ready. This might actually be fun. Let's go."),
            "poor": _("I need this money so badly... fine. Just... let's get it over with."),
            "rich_hc": _("I don't need your cash, but a deal's a deal. Let's see what you've got."),
            "rich": _("I can't believe I'm doing this. I don't even need the money... whatever. Let's go."),
            "cute": _("I can't believe I agreed to this for money... just... be gentle, okay?"),
            "hc": _("Money's money. Let's get this over with."),
            "default": _("Fine. You paid. Let's just... get it over with."),
        },

        "postaccept_s0_c1": {
            "les_poor": _("Again... these books won't pay for themselves. A lesbian being paid by a man... just do it."),
            "les_rich": _("Twice now. I don't need this. I don't know why I keep agreeing."),
            "les": _("Again... a lesbian being paid by a man... fine. Let's just do this."),
            "poor_hc": _("Easy money again. Less talking, more action. Let's go."),
            "poor": _("Again... I told myself once was enough. But the money helps too much."),
            "rich_hc": _("Round two. Not for the cash, honestly. Let's just do this."),
            "rich": _("Why do I keep doing this? I have money... whatever. Let's go."),
            "cute": _("Again...? I said never again... just... be quick this time."),
            "hc": _("Same deal. Less talking. Let's go."),
            "default": _("I keep coming back to this. Fine. Let's go."),
        },

        "postaccept_s0_c2": {
            "les_poor": _("Third time... at least the money keeps coming. Let's get this over with."),
            "les_rich": _("Third time and I still don't need the cash. I must be losing my mind."),
            "les": _("Third time... I'm not even going to pretend this surprises me anymore. Do it."),
            "poor_hc": _("We've got a good routine going. You pay, I deliver. Let's go."),
            "poor": _("Third time... the money makes it easier to swallow. Let's just do it."),
            "rich": _("I keep coming back and I don't even need the money. Whatever. Let's go."),
            "cute": _("I stopped counting how many times I said 'never again'... let's just do it..."),
            "default": _("You know the drill. I know the drill. Let's go."),
        },

        "postaccept_s0_c3": {
            "les_poor": _("Same arrangement. I need the money, you know the rest. Let's go."),
            "les": _("Same arrangement. Pay up. Let's go."),
            "poor_hc": _("Easy money. Let's do this."),
            "poor": _("You paid. I need it. Let's go."),
            "rich": _("You paid. Not that I needed it. Let's go."),
            "cute": _("...Just tell me what you want. I already agreed."),
            "default": _("You paid. Let's do this."),
        },

        "postaccept_s1": {
            "les_poor": _("I know the drill. The money keeps me going. Let's just do this."),
            "les_rich": _("Fine. I still don't need the cash, but here we are. Let's go."),
            "les": _("I know the drill by now. Let's just get this over with."),
            "poor_hc": _("Cash in, fun starts. Let's go."),
            "poor": _("The money really helps. Alright, let's just do this."),
            "rich": _("I don't know why I keep saying yes. It's not the money. Whatever, let's go."),
            "cute": _("Okay... let's just do it. Please be quick..."),
            "hc": _("Cash received. Let's go."),
            "default": _("Alright. You paid, so... let's do this."),
        },

        "shock_accept": {
            "les_poor": _("Wait, you're actually paying that?! I said that number to scare you off!"),
            "les_rich": _("Hold on. You're serious? I named that price because I was SURE you'd say no!"),
            "les": _("You... what?! That was supposed to be impossible! No man would pay that much to touch a lesbian!"),
            "poor_hc": _("Whoa. You're actually paying? I threw out a crazy number on purpose!"),
            "poor": _("W-wait, you have that kind of money?! I just said that to make you go away!"),
            "rich_hc": _("Excuse me? You're actually pulling out that much cash? I was testing you!"),
            "rich": _("You're actually going to pay THAT? I said that price because nobody in their right mind would!"),
            "cute": _("Y-you... that's real money?! I only said that because I thought you'd never actually..."),
            "hc": _("Hold on. You're not bluffing? I set that price to shut you up, not to actually DO it."),
            "default": _("Wait. You're serious?! I named that price because I thought it was impossible!"),
        },

        "shock_backout": {
            "les_poor": _("No no no, wait. I wasn't serious! Take your money back, I'm not doing that with a man!"),
            "les_rich": _("Absolutely not. I said that to make you leave. Take your money and go."),
            "les": _("Stop. I said that to scare you off. I'm a lesbian, I'm NOT doing that. Take it back."),
            "poor_hc": _("Whoa, hold on. I was bluffing! You can't just... I didn't mean it! Take your money back!"),
            "poor": _("Wait, please! I wasn't serious! I just said a crazy number so you'd go away! Take it back!"),
            "rich_hc": _("No. Stop. I said that number because nobody would pay it. Take your cash and get out."),
            "rich": _("Absolutely not. I don't care how much you throw at me. Take it back. Now."),
            "cute": _("N-no! I didn't mean it! I was just trying to make you stop asking! Please take it back!"),
            "hc": _("Hold on. That was a scare tactic, not an offer. Take your money and leave."),
            "default": _("Wait, stop! I wasn't actually offering! That was supposed to be impossible! Take your money back!"),
        },

        "shock_rich_refuse": {
            "les_rich": _("I don't need your money. I'm a lesbian. No amount will change that. We're done here."),
            "rich_hc": _("I don't need money. I have plenty. And I'm not for sale. Get out."),
            "rich": _("You think you can just throw money at me? I don't need it. Not for any amount. Leave."),
            "default": _("No. Keep your cash. I'm not desperate enough to sell myself for any price."),
        },

        "shock_caved": {
            "les": _("I... damn it. I DID say a number. And you paid it. I hate this, but... fine."),
            "cute": _("That's... that's not fair... I said a price and you actually... ugh, fine..."),
            "hc": _("...You're ruthless. Fine. I gave my word. But don't think I'll enjoy this."),
            "default": _("...You're right. I named a price and you paid. I can't back out of my own deal..."),
        },

        "shock_poor_caved": {
            "les_poor": _("I... God. I need that money so badly. And I DID say a number... fine. FINE."),
            "poor_hc": _("...Damn it. You're right. A deal's a deal. And that's SO much money..."),
            "poor": _("I... you're right. I said it. And I... I really need that money. Okay. Fine."),
            "default": _("...You're right. I named my price. And it's too much money to just give back..."),
        },

        "shock_poor_need": {
            "les_poor": _("...Don't say that. Don't you DARE say that. ...But you're right. I need it. I hate you."),
            "poor_hc": _("...Low blow. But yeah. I do. That kind of money changes everything. Fine."),
            "poor": _("That's... that's cruel. But you're not wrong. {hint}I can't even afford new clothes{/hint}..."),
            "default": _("...Don't rub it in. I know I need it. That's what makes this so awful. Fine."),
        },

        "shock_player_backs": {
            "les_poor": _("...Thank you. Seriously. I almost did something really stupid."),
            "les": _("...Good. Smart choice. For both of us."),
            "poor": _("Thank you... I was scared for a second there. Keep your money."),
            "cute": _("Oh thank God... I thought you were really going to make me..."),
            "hc": _("Good. You came to your senses."),
            "default": _("...Right. Good. Let's just pretend this never happened."),
        },

        "postaccept_s2": {
            "les_poor": _("Good, I needed that. Let's get to work."),
            "les_rich": _("Consider it entertainment money. Let's go."),
            "les": _("Transaction complete. Let's get to it."),
            "poor_hc": _("Paid and excited. Let's have some fun."),
            "poor": _("That'll cover a lot. Alright, let's get started."),
            "rich_hc": _("Money's just a formality at this point. Time to deliver."),
            "rich": _("Pocket money. Whatever. Let's get this done."),
            "cute": _("Okay, we're good. What do you want me to do first?"),
            "hc": _("Paid in full. Time to deliver."),
            "default": _("Deal. Let's get started."),
        },

        "postaccept_s3": {
            "les_poor": _("Reliable income. You know I always deliver for a paying client."),
            "les_rich": _("It was never about the money with us. Let's enjoy this."),
            "les": _("Easy money. You know I always deliver."),
            "poor_hc": _("Best job I ever had. Cash AND fun. Let's go."),
            "poor": _("You always come through when I need it. I won't disappoint."),
            "rich_hc": _("Forget the money. I'm here because I want to be. Let's go."),
            "rich": _("The money's nice, but honestly? I kind of enjoy our arrangement."),
            "cute": _("Thanks for the cash. I'll make it worth your while, promise."),
            "hc": _("Good. Let's make this count."),
            "default": _("Perfect. You know I'm always available for the right price."),
        },

        # ──────────────────────────────────────
        # POST-ACCEPT — Cheating follow-up
        # tk = _fin_partner_key(girl)
        # ──────────────────────────────────────

        "postaccept_cheat_s01": {
            "les_gf": _("%(Pp)s would be devastated if %(pp)s knew... a man is paying me to... God."),
            "les_bf": _("My %(pl)s would kill me if %(pp)s knew I'm taking cash for this."),
            "poor_bf": _("If my %(pl)s knew I'm selling myself because {hint}I can't afford a decent phone{/hint}... %(pp)s would never look at me the same."),
            "rich_bf": _("My %(pl)s gives me everything. And here I am, being paid by another man. What is wrong with me."),
            "default": _("If my %(pl)s ever finds out... just, make it quick."),
        },

        "postaccept_cheat_s2": {
            "les_gf": _("%(Pp)s doesn't need to know about my side income. Let's go."),
            "les_bf": _("What %(pp)s doesn't know won't hurt %(po)s. Business as usual."),
            "poor_bf": _("My %(pl)s doesn't know I do this on the side. The money covers what %(pp)s can't provide."),
            "rich_bf": _("My %(pl)s has no idea. It's not about the money. Never was."),
            "default": _("My %(pl)s is none of your concern. This is between us."),
        },

        "postaccept_cheat_s3": {
            "les_gf": _("%(Pp)s thinks I'm out with friends. Which is technically true... you're a friend who pays."),
            "les_bf": _("My %(pl)s? Please. %(Pp)s can barely keep up with me. You're just a bonus."),
            "poor_bf": _("My %(pl)s can't provide like you do. This stays between us."),
            "rich_bf": _("My %(pl)s gives me everything except this. Our little secret."),
            "default": _("Don't even mention my %(pl)s. This is our thing. %(Pp)s has nothing to do with it."),
        },

        # ──────────────────────────────────────
        # NEGOTIATE
        # fmt = {"counter_act": str}
        # ──────────────────────────────────────

        "negotiate_s1": {
            "les_poor": _("I need every dollar, but... fine. I could %(counter_act)s for less."),
            "les_rich": _("My rates are premium. But I could %(counter_act)s for less. Consider it a favor."),
            "les": _("I'm not lowering the price for that. But... I could %(counter_act)s for less."),
            "poor_hc": _("Negotiating? Sure, I'm flexible. I could %(counter_act)s for less."),
            "poor": _("I really need the money, but... I could %(counter_act)s for a lower price instead."),
            "rich": _("My price is firm. But I could %(counter_act)s for less. Take it or leave it."),
            "cute": _("I can't go lower for that... but maybe I could %(counter_act)s instead? For less?"),
            "hc": _("I don't like lowering prices. But... I could %(counter_act)s for a lower rate instead."),
            "default": _("That price is firm. But if you want, I could %(counter_act)s for cheaper."),
        },

        "negotiate_s23": {
            "les_poor": _("I need the money, so... yeah, I can work with a lower number."),
            "les": _("Hmm. I could work with a lower number. Let me think..."),
            "poor_hc": _("Negotiating? I like that. Let's find something that works for both of us."),
            "poor": _("I could use any amount, honestly. Let me see what I can offer."),
            "rich_hc": _("Not about the money. But I'm flexible. Here's what I can do."),
            "rich": _("Fine. I don't need the money anyway. Here's what I can do."),
            "cute": _("Well... I guess I could be flexible. What did you have in mind?"),
            "hc": _("Negotiating? Fine. I respect that. Here's what I can do."),
            "default": _("Alright, let's talk numbers. I can be flexible."),
        },

        # ──────────────────────────────────────
        # MENU REFUSALS
        # ──────────────────────────────────────

        "too_expensive": {
            "rich": _("I'm already doing something I never thought I would. The price stays."),
            "hc": _("I set the price for a reason. Pay it or walk away."),
            "cute": _("I already feel bad enough about this... please don't try to haggle..."),
            "default": _("I'm not going lower. This is already hard enough for me."),
        },

        "cant_afford": {
            "rich": _("You can't even afford me? Don't waste my time."),
            "cute": _("You don't have enough...? Well... maybe next time, I guess..."),
            "default": _("Come back when you actually have the money."),
        },

        "cant_afford_negotiate": {
            "default": _("You can't even afford that? Don't waste my time."),
        },

        # ──────────────────────────────────────
        # POST-SCENE (via _coercion_post_scene)
        # Lists = random choice
        # ──────────────────────────────────────

        "postscene_s0": {
            "les_poor": [
                _("I sold myself to a man because I need money... I can't even afford to keep my dignity."),

                _("I hate this. I hate that I needed the money. I hate that it was with a man. Everything about this is wrong."),

                _("The worst part isn't what I did. It's that I'll probably do it again because I need the cash."),

            ],
            "les_rich": [
                _("I don't even need the money. Why did I agree to this? A lesbian selling herself to a man for cash she doesn't need..."),

                _("This was stupid. I have money. I have standards. And I just threw both away. Get out."),

            ],
            "les_cute": [
                _("I can't believe I did that for money... with a man... what is happening to me..."),

                _("You paid me to... I'm a lesbian... why did I agree to that..."),

                _("I feel so cheap... doing that with a man for cash... I need to be alone..."),

            ],
            "les_hc": [
                _("You bought a few minutes with a lesbian. Enjoy the memory. It won't happen again."),

                _("Money doesn't change who I am. I'm still a lesbian. That was just... a transaction."),

                _("Don't confuse payment with interest. I needed the money. That's all."),

            ],
            "les": [
                _("I let a man pay me for... that. I'm a lesbian. What is wrong with me..."),

                _("The money doesn't make this better. If anything, it makes it worse. Just go."),

                _("This was purely financial. Nothing more. Don't read into it."),

            ],
            "poor_hc": [
                _("Got paid AND had a good time. I call that a productive afternoon."),

                _("Business is business. And honestly? That wasn't bad. The money is just a bonus."),

            ],
            "poor": [
                _("I needed the money... that's the only reason. Please don't think I do this for fun..."),

                _("I can't afford to feel bad about this. Literally. The money will help. That's all that matters."),

                _("Please don't tell anyone about this... I just really needed the cash..."),

            ],
            "rich_hc": [
                _("I didn't need the money. But getting paid to have fun? Why not."),

                _("Don't think you bought me. I did that because I felt like it. The cash is just a souvenir."),

            ],
            "rich": [
                _("I don't know why I agreed. I have money. I didn't need yours. This was a mistake."),

                _("I can't believe I let you pay me for that. I'm not desperate. I just... don't know what I was thinking."),

            ],
            "cute": [
                _("I feel so gross... I did that for money... what kind of person does that..."),

                _("Please don't tell anyone about this... the money was... I just needed it... please..."),

                _("That was horrible... I can't believe I agreed to that for cash..."),

            ],
            "hc": [
                _("Business is business. Don't expect a discount next time."),

                _("You got what you paid for. Now we're done. Get out."),

                _("That was a one-time deal. Don't get used to it."),

            ],
            "default": [
                _("I can't believe I just did that for money... this is a new low for me."),

                _("We're done. I did what you paid me for. Now please leave me alone."),

                _("Don't look at me like that. It was just... I needed the money. That's all."),

            ],
        },

        "postscene_s1": {
            "les_poor": [
                _("Another transaction with a man... at least the bills are covered."),

                _("I hate that this is becoming routine. But the money... I need it."),

            ],
            "les_rich": [
                _("I keep doing this and I don't even need the money. Something is wrong with me."),

                _("We're done. And I still don't understand why I keep agreeing."),

            ],
            "les": [
                _("Another transaction with a man... I'm getting used to it. That's the worst part."),

                _("We're done. Same as always. Just... don't talk about it."),

            ],
            "poor_hc": [
                _("That was fine. Good money for a good time."),

                _("Easy money, easy fun. We're done. See you next time."),

            ],
            "poor": [
                _("The money really helps. That's all I'll say about it."),

                _("I'm not proud of this, but the bills are paid. We're done."),

            ],
            "rich": [
                _("I don't need your money. I keep saying that and I keep taking it anyway."),

                _("Whatever that was... it wasn't about the cash. I don't know what it was about."),

            ],
            "cute": [
                _("That was... fine. I'm not going to pretend it ruined my day anymore."),

                _("I'm okay. Really. It's just... money. That's all it is now."),

            ],
            "hc": [
                _("Efficient as always. Now get out, I have things to do."),

                _("Job's done. You know where the door is."),

            ],
            "default": [
                _("It is what it is. We're done here."),

                _("Alright, that's that. I'll see you around, I guess."),

            ],
        },

        "postscene_s2": {
            "les_poor": [
                _("Steady income. I can live with that. Same time next week?"),

                _("The money keeps things simple. You know where to find me."),

            ],
            "les_rich": [
                _("I still don't need the money. But our arrangement has become... comfortable."),

                _("It's not about the cash anymore. But keep paying. I like the principle."),

            ],
            "les": [
                _("I keep letting a man pay me for this. I don't know what that makes me anymore."),

                _("It's becoming routine. With a man. For money. I can't even pretend I hate it anymore."),

            ],
            "poor_hc": [
                _("Great money for a great time. I love this arrangement."),

                _("Best side job ever. Seriously. See you next time."),

            ],
            "poor": [
                _("This really keeps me afloat. Thanks. Same time next week?"),

                _("Reliable income. I appreciate that. You know where to find me."),

            ],
            # setting the rules is femdom, not hardcore (docs/plan_femdom.md D3)
            "rich_fd": [
                _("Professional entertainment. I set the rules, you pay the fee. Works for me."),

                _("I don't need your money. I take it so you remember who runs this arrangement."),

                _("My rules, my schedule, your wallet. I could get used to this."),

            ],
            "rich_hc": [
                _("I don't need the cash but I enjoy our sessions. That's worth more."),

                _("The cash is pocket change. The workout, on the other hand... that I needed."),

            ],
            "rich": [
                _("The money's irrelevant. It's become a routine I don't hate."),

                _("I keep telling myself I'll stop. But here we are. Same time next week?"),

            ],
            "cute": [
                _("That was nice, actually. Thanks for the cash."),

                _("See? Easy. No drama. I'll be around if you need me again."),

            ],
            "hc": [
                _("Clean transaction. I appreciate a repeat customer."),

                _("Professional as always. Pleasure doing business."),

            ],
            "default": [
                _("Same time, same place. You know the deal."),

                _("Smooth as usual. You know where to find me."),

            ],
        },

        "postscene_s3": {
            "les_poor": [
                _("I need your money. That's the only reason I keep doing this. Don't forget that."),

                _("I depend on this now. Which disgusts me. But bills don't pay themselves."),

            ],
            "les_rich": [
                _("I don't even need the money anymore. I just... I don't know why I keep agreeing. Habit, maybe."),

                _("This has become routine. I hate that. But here I am, every time you ask."),

            ],
            "les": [
                _("I've gotten used to this. That's the worst part. I should be fighting harder."),

                _("Another time. Another transaction. I keep telling myself this is the last one."),

            ],
            "poor_hc": [
                _("Easy money and I get something out of it too. Could be worse."),

                _("You keep paying, I keep showing up. It works for both of us."),

            ],
            "poor": [
                _("I don't know what I'd do without this money. I need it. That's why I'm here."),

                _("You've been keeping me afloat. I'm not proud of how, but... I need it."),

            ],
            "rich_hc": [
                _("I don't need your money. But the arrangement has its perks. Don't let it go to your head."),

                _("The cash is irrelevant. But our little routine... I've gotten comfortable with it."),

            ],
            "rich": [
                _("I don't need the money. I know that. You know that. But I keep coming back anyway."),

                _("This arrangement has become... familiar. I'm not sure what that says about me."),

            ],
            "cute": [
                _("The money really helps. And it's not as scary as it used to be. So... same time next time?"),

                _("I've gotten used to this. The cash helps a lot and... at least you're not rough about it."),

            ],
            "hc": [
                _("You know my rates. I know what you want. Let's not pretend this is more than it is."),

                _("Efficient as always. Cash on the table, we do our thing. See you next time."),

            ],
            "default": [
                _("You know where to find me. Same arrangement, same price."),

                _("This has become routine. I'm not sure if that's a good thing. But the money helps."),

            ],
        },

        # ──────────────────────────────────────
        # POST-SCENE — Partner reference
        # tk = _fin_partner_key(girl)
        # ──────────────────────────────────────

        "postscene_partner_s0": {
            "les_gf": [
                _("If my %(pl)s ever finds out I did this with a man... for MONEY... she would never speak to me again."),

                _("My %(pl)s thinks I'm faithful. And here I am, selling myself to a man. I'm disgusting."),

            ],
            "les_bf": [
                _("If my %(pl)s ever finds out what I just did... because of YOU..."),

                _("My %(pl)s deserves better than this. I deserve better than this."),

            ],
            "poor_bf": [
                _("If my %(pl)s knew I'm selling myself because we need the money... what have I become."),

                _("My %(pl)s works so hard for us and I'm here doing THIS for cash... %(pp)s can never know."),

            ],
            "rich_bf": [
                _("My %(pl)s gives me everything and I still do this. I don't even need the money. I'm a horrible person."),

                _("%(Pp)s provides for me. And I just... for money I don't need... God."),

            ],
            "default": [
                _("If my %(pl)s ever finds out what I just did... because of YOU..."),

                _("My %(pl)s deserves better than this. I deserve better than this."),

                _("%(Pp)s can never know. You hear me? NEVER."),

            ],
        },

        "postscene_partner_s1": {
            "les_gf": [
                _("%(Pp)s trusts me completely... and I'm here doing this with a man for cash..."),

                _("I keep telling myself %(pp)s won't find out. But the guilt is eating me alive."),

            ],
            "les_bf": [
                _("My %(pl)s has no idea... and I don't know how much longer I can keep this up."),

                _("Every time I go back to %(po)s after this, I feel like a fraud."),

            ],
            "poor_bf": [
                _("If my %(pl)s knew I'm doing this for money we need... %(pp)s would be devastated."),

                _("My %(pl)s thinks I'm working extra shifts. Not... this."),

            ],
            "rich_bf": [
                _("My %(pl)s gives me everything. So why am I here? I don't even need the cash..."),

                _("%(Pp)s would never understand. I have everything and I still do this."),

            ],
            "default": [
                _("My %(pl)s would be crushed if %(pp)s knew..."),

                _("I can't even look at my %(pl)s after doing this..."),

            ],
        },

        "postscene_partner_s23": {
            "les_gf": [
                _("%(Pp)s doesn't need to know about my... business arrangements."),

                _("What %(pp)s doesn't know won't hurt %(po)s. We're good."),

            ],
            "les_bf": [
                _("My %(pl)s is irrelevant here. This is work."),

                _("%(Pp)s has nothing to do with our arrangement."),

            ],
            "poor_bf": [
                _("My %(pl)s doesn't know I do this on the side. The extra cash keeps us afloat."),

                _("%(Pp)s can't provide like you do. This is just business."),

            ],
            "rich_bf": [
                _("My %(pl)s has no clue. It's not about the money. Never was."),

                _("%(Pp)s gives me everything except this. Our arrangement stays private."),

            ],
            "default": [
                _("My %(pl)s? That's my problem, not yours."),

                _("Don't worry about my %(pl)s. This stays between us."),

            ],
        },

        # ──────────────────────────────────────
        # INLINE POST-SCENE (kiss/masturbate paths)
        # ──────────────────────────────────────

        "inline_s0": {
            "les_poor": _("A lesbian selling herself to a man for some extra cash... just go. Please."),
            "les": _("I just let a man pay me to... ugh. Leave. Now."),
            "poor_hc": _("That wasn't bad, honestly. And the money helps. We're done though."),
            "poor": _("I needed the money... that's all. Please, just go."),
            "rich": _("I don't even need your money. Why did I do that? Just leave."),
            "cute": _("I can't believe I did that for money... please, just go."),
            "hc": _("Transaction complete. Now get out of my sight."),
            "default": _("We're done. Take your... 'purchase' and leave me alone."),
        },

        "inline_s1": {
            "les_poor": _("Another one for the bills. Go."),
            "les": _("Another one. I'm getting used to this. Go."),
            "poor_hc": _("Easy money. See you around."),
            "poor": _("The money helps. That's all I'll say. We're done."),
            "rich": _("I still don't know why I keep doing this. Go."),
            "cute": _("That was... okay. I'm fine. Really."),
            "hc": _("Done. You know where the door is."),
            "default": _("Alright, we're done. See you around."),
        },

        "inline_s2": {
            "les_poor": _("Steady income. Can't complain. See you next time."),
            "les": _("I should stop doing this. But I won't. ...See you next time."),
            "poor_hc": _("Great time, great pay. See you next week."),
            "poor": _("That keeps the lights on. Thanks. Same time next week?"),
            "rich": _("The money's a bonus. The routine is what keeps me coming back."),
            "cute": _("Thanks for the cash. That was nice, actually."),
            "hc": _("Clean transaction. See you next time."),
            "default": _("Good doing business. Same time next week?"),
        },

        "inline_s3": {
            "les_poor": _("I need the money. That's it. Don't read into it."),
            "les": _("This is just business. Same as always."),
            "poor_hc": _("Cash and I get something out of it. Works for me."),
            "poor": _("I depend on this money now. You know where to find me."),
            "rich": _("It's become routine. I don't question it anymore."),
            "cute": _("That was... fine. The money helps. Thanks."),
            "hc": _("Clean transaction. Same rates next time."),
            "default": _("Same arrangement, same price. You know the deal."),
        },

        # ──────────────────────────────────────
        # GIRL-INITIATED (Stage 3)
        # tk = _fin_girl_init_key(girl)
        # fmt = {"price": int, "act": str}
        # ──────────────────────────────────────

        "girl_init": {
            "les_gf": _("%(Pp)s is out today. I know what you want, and I could use the cash. $%(price)d to %(act)s. Our little secret."),
            "les_bf": _("My %(pl)s doesn't need to know. $%(price)d and I'll %(act)s. What do you say?"),
            "les_poor": _("I need the cash and you need me. $%(price)d to %(act)s. We both know I'll say yes."),
            "les_rich": _("I don't need the money, but I know you want this. $%(price)d to %(act)s. Consider it a favor."),
            "les": _("I know what you want. And I could use some cash. $%(price)d to %(act)s. Interested?"),
            "het_bf": _("My %(pl)s doesn't have to know. $%(price)d and I'll %(act)s for you. Interested?"),
            "poor_hc": _("I could use the cash AND the fun. $%(price)d and I'll %(act)s. Everybody wins."),
            "poor": _("Hey... I could really use some money right now. $%(price)d and I'll %(act)s for you. Deal?"),
            "rich_hc": _("Forget the money. I'm offering because I want to. $%(price)d to %(act)s. The cash is just tradition."),
            "rich": _("I don't need the cash, but our arrangement works. $%(price)d and I'll %(act)s. Interested?"),
            "cute": _("Um... I was thinking... if you want, I could %(act)s. For $%(price)d? If that's okay..."),
            "hc": _("You want to %(act)s? $%(price)d. I'm offering. Take it or leave it."),
            "default": _("Look, I know the drill. $%(price)d and I'll %(act)s. You in?"),
        },

        "girl_init_negotiate": {
            "les": _("Alright, let's talk. I could %(counter_act)s for $%(counter_price)d instead. How about that?"),
            "cute": _("Okay, um... I could %(counter_act)s for $%(counter_price)d? Would that work?"),
            "hc": _("Fine. $%(counter_price)d and I'll %(counter_act)s. Final offer."),
            "default": _("How about this: $%(counter_price)d and I'll %(counter_act)s instead. Deal?"),
        },

        "girl_init_reject": {
            "les": _("Your loss. I don't offer twice."),
            "cute": _("Oh... okay. Maybe another time, I guess."),
            "hc": _("Fine. Don't expect me to ask again."),
            "default": _("Suit yourself. The offer stands if you change your mind."),
        },

        # ──────────────────────────────────────
        # CHITCHAT
        # ──────────────────────────────────────

        "chitchat_s3": {
            "default": [
                _("So... I was thinking. If you ever need some company, you know my rates."),

                _("Things have been tight lately. If you're in the mood, I'm available. Just saying."),

                _("You know, it's not even weird anymore. It's just... our thing. Right?"),

            ],
        },

        "chitchat_s2": {
            "default": [
                _("About our arrangement... it works for both of us. No need to make it awkward."),

                _("I've been thinking about our little deal. It's honestly not bad. Clean, simple."),

                _("You pay, I deliver. No drama, no strings. We've got a good system going."),

            ],
        },

        "chitchat_shame_1": {
            "default": [
                _("Don't... don't bring up money around me, okay? I'm not proud of what I did."),

                _("I used the money you gave me for textbooks. At least something good came out of it..."),

                _("Can we just... pretend the money thing never happened? Please?"),

            ],
        },

        "chitchat_shame_2": {
            "default": [
                _("Twice now... I keep telling myself it was just for the money..."),

                _("I'm starting to hate the sound of cash. It reminds me of... you know."),

                _("Don't look at me like that. You paid. I delivered. That's all it was."),

            ],
        },

        "chitchat_shame_3": {
            "default": [
                _("At this point, what's one more time, right? ...I hate that I think like that now."),

                _("I've stopped counting. The money helps. That's all I'll say."),

                _("You know, some days I barely think about it. Other days... I can't stop."),

            ],
        },

        # ──────────────────────────────────────
        # NTR BOUNDARY — FINANCIAL COERCION
        # When act is outside NPC partner's boundary level.
        # ──────────────────────────────────────

        # Refuse: attitude 0, act outside NTR boundary
        "ntr_boundary_refuse": {
            "les": [
                _("No. %(Pp)s set rules and I'm not breaking them for money. Not yet."),
                _("I'm not crossing %(partner)s's line for cash. That's a whole different kind of betrayal."),
            ],
            "cute": [
                _("I... I can't. %(partner)s trusts me. Even for money, I can't do that to %(po)s."),
                _("%(partner)s set limits and... I just can't break them. Not like this. I'm sorry."),
            ],
            "hc": [
                _("%(partner)s's rules are %(partner)s's rules. I'll cross that line when I'm ready, not because you're waving cash."),
                _("Not for money. %(Pp)s set a boundary and I'm respecting it. For now."),
            ],
            "poor": [
                _("I need the money, but... %(partner)s trusts me. I can't break %(poss)s rules. Not for this."),
                _("God, I could really use the cash, but... no. %(partner)s set limits and I have to respect them."),
            ],
            "default": [
                _("%(partner)s set rules for a reason. I'm not breaking them for money."),
                _("No. That goes past what %(partner)s agreed to. Money doesn't change that."),
            ],
        },

        # Refuse: attitude 0, but cheater trait (lighter, doesn't care about NPC)
        "ntr_boundary_refuse_cheater": {
            "default": [
                _("Look, I'd totally do it, but %(partner)s has been weird about this stuff lately. Ask me again another time."),
                _("Hmm, tempting, but the timing is bad. %(Pp)s is already suspicious. Come back later."),
            ],
        },

        # Price: attitude 1+, act outside NTR boundary (she accepts but premium)
        "ntr_boundary_price": {
            "les": [
                _("$%(price)d. And that's extra because %(partner)s didn't agree to this. %(Pp)s said limits, and I'm breaking them for you."),
                _("%(partner)s set boundaries. I'm crossing them. That costs extra. $%(price)d."),
            ],
            "cute": [
                _("I... okay. But $%(price)d. This is past what %(partner)s allowed and I feel terrible about it."),
                _("$%(price)d... %(partner)s trusts me and I'm about to break that trust. The price reflects how awful I feel."),
            ],
            "hc": [
                _("$%(price)d. %(partner)s's rules, %(partner)s's problem. But the risk premium is real."),
                _("$%(price)d. Breaking %(partner)s's boundary isn't free. You're paying for the complications."),
            ],
            "poor": [
                _("$%(price)d. I shouldn't be doing this, %(partner)s set limits... but I really need the money."),
                _("%(partner)s would kill me if %(pp)s knew. $%(price)d. The extra is guilt money."),
            ],
            "default": [
                _("$%(price)d. That's above what %(partner)s agreed to, so yes, the price is higher."),
                _("%(partner)s set limits on what we could do. Going past that is $%(price)d. Non-negotiable."),
            ],
        },

        # Price: attitude 2+, act outside NTR boundary (transactional, casual)
        "ntr_boundary_price_casual": {
            "les": [
                _("$%(price)d. We both know %(partner)s wouldn't approve. But %(pp)s's not here to complain."),
                _("%(partner)s's rules? Please. $%(price)d and we do what we want."),
            ],
            "cute": [
                _("$%(price)d... I've stopped worrying about %(partner)s's rules. But the risk is still real."),
                _("$%(price)d. I used to feel guilty about crossing %(partner)s's lines. Now I just charge extra."),
            ],
            "hc": [
                _("$%(price)d. %(partner)s's boundary means nothing to me at this point. But you're still paying for it."),
                _("$%(price)d. Breaking rules has a price tag. Nothing personal."),
            ],
            "poor": [
                _("$%(price)d. %(partner)s's limits stopped mattering a while ago. But the surcharge stays."),
                _("$%(price)d. I need the money more than I need %(partner)s's approval."),
            ],
            "default": [
                _("$%(price)d. Extra for going past %(partner)s's boundary. Standard surcharge at this point."),
                _("$%(price)d. Yes it's more. %(partner)s set rules and breaking them costs extra. Simple."),
            ],
        },

        # Price: cheater trait (doesn't care about NPC, just charges because she can)
        "ntr_boundary_price_cheater": {
            "default": [
                _("$%(price)d. I don't care about %(partner)s's rules, but hey, if you're willing to pay extra, I'll take it."),
                _("$%(price)d. %(partner)s's limits are %(poss)s problem. I'm just charging what the market allows."),
            ],
        },
    }

    # ════════════════════════════════════════════════════════
    # GIRL-SPECIFIC OVERRIDES
    # Same structure as _FINANCIAL_LINES but keyed by gid.
    # Lookup: girl-specific -> trait combo -> base trait -> default
    # ════════════════════════════════════════════════════════

    _FINANCIAL_GIRL_LINES = {

        "ntw": {
            "opener_s0_c0": {
                "default": _("You're offering me money. For that. With you. ...How much."),
            },
            "opener_s0_c1": {
                "default": _("Again. Awesome. How much this time."),
            },
            "opener_s1": {
                "default": _("You're here again. I know why. Just tell me the number."),
            },
            "opener_s23": {
                "default": _("Same deal. Skip the speech. How much."),
            },
            "shock_accept": {
                "default": _("You... wait. You actually have that kind of money? I said that to make you leave."),
            },
            "shock_backout": {
                "default": _("No. Nope. I was bluffing. Take your cash back. This isn't happening."),
            },
            "shock_caved": {
                "default": _("...Ugh. Fine. I said a number. You paid it. I hate everything about this."),
            },
            "shock_player_backs": {
                "default": _("Smart. Now get out before I change my mind about not kicking you."),
            },
            "postaccept_s0_c0": {
                "default": _("Wow. I really just agreed to that. For money. Let's just get it over with."),
            },
            "postaccept_s1": {
                "default": _("Yeah, yeah. Let's go."),
            },
            "postscene_s0": {
                "default": [
                    _("That was every bit as awful as I predicted. Leave."),

                    _("I'm going to pretend this never happened. Get out."),

                ],
            },
            "postscene_s3": {
                "default": [
                    _("Not terrible. For a guy. See you next time."),

                    _("You're tolerable. Door's open."),

                ],
            },
            "girl_init": {
                "default": _("I'm broke and bored. $%(price)d and I'll %(act)s. Don't make it weird."),
            },
            "girl_init_reject": {
                "default": _("Whatever. Your loss."),
            },
            "inline_s0": {
                "default": _("Cool. That happened. Leave."),
            },
            "inline_s3": {
                "default": _("Not the worst way to make money. See you around."),
            },
        },

        "tenny": {
            "girl_gate_refuse": {
                "default": [
                    _("You want to buy my time? You haven't even invested in getting to know me. Come back when you've proven you're serious."),
                    _("Money? From you? I barely know your name and you think I'm for sale. Try harder. Much harder."),
                    _("That's flattering in the worst possible way. You haven't earned the right to make that offer yet."),
                ],
            },
            "opener_s0_c0": {
                "default": _("You're offering ME money. For THAT. You clearly didn't think this through. How much."),
            },
            "opener_s0_c1": {
                "default": _("Back again with the wallet. I expected more creativity from you. How much."),
            },
            "opener_s0_c2": {
                "default": _("At this point you should just set up a direct deposit. How much."),
            },
            "opener_s1": {
                "default": _("I know the routine by now. State your price and let's see if it's insulting."),
            },
            "opener_s23": {
                "default": _("The usual arrangement? Fine. I've made my peace with this. What's the offer."),
            },
            "price_s0_first": {
                "default": _("If you're serious... $%(price)d. To %(act)s. And not a cent less."),
            },
            "price_s0_repeat": {
                "default": _("$%(price)d. Same terms as before. I don't do discounts."),
            },
            "price_s1": {
                "default": _("$%(price)d for %(act)s. You know my standards by now."),
            },
            "price_s23": {
                "default": _("%(act_cap)s. $%(price)d. Standard rate."),
            },
            "postaccept_s0_c0": {
                "default": _("I can't believe I'm agreeing to this. Don't mistake this for weakness. I just decided the price was right."),
            },
            "postaccept_s1": {
                "default": _("Fine. Let's get this over with. Professionally."),
            },
            "postaccept_s3": {
                "default": _("Accepted. You know where to find me."),
            },
            "postscene_s0": {
                "default": [
                    _("That was transactional. Nothing more. Don't read into it."),
                    _("We're done. Don't tell anyone about this. I have a reputation."),
                ],
            },
            "postscene_s1": {
                "default": [
                    _("Same time next week? ...I'm joking. Mostly."),
                    _("This is becoming a pattern. I'm not sure how I feel about that."),
                ],
            },
            "postscene_s3": {
                "default": [
                    _("Efficient as always. See you next time."),
                    _("Another successful transaction. The door is always open."),
                ],
            },
            "inline_s0": {
                "default": _("That happened. Moving on. Don't bring it up."),
            },
            "inline_s3": {
                "default": _("Quick and clean. Exactly how I like business."),
            },
            "shock_accept": {
                "default": _("You... actually paid that? I named that price to scare you off."),
            },
            "shock_backout": {
                "default": _("Wait. No. I was testing you. Give that back."),
            },
            "shock_caved": {
                "default": _("...A deal is a deal. I said a number. You paid it. I keep my word."),
            },
            "shock_player_backs": {
                "default": _("Smart. Now leave before I raise my rates."),
            },
            "girl_init": {
                "default": _("I've been thinking. $%(price)d and I'll %(act)s. Strictly business."),
            },
            "girl_init_reject": {
                "default": _("Your loss. The offer won't last forever."),
            },
            "too_expensive": {
                "default": _("I didn't set the price to be generous. Pay it or don't."),
            },
        },
    }
