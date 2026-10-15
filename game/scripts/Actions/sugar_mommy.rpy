# ============================================================
# sugar_mommy.rpy... a rich SUBMISSIVE girl keeps the player (docs/plan_sugar_mommy.md, camada 3).
# Trait-driven, zero gid checks: today the broken stepmom (CANON_BREAK_RULES), tomorrow any girl who is
# submissive + rich. The ARRANGEMENT is her own offer by text (Wait 6h2, system_time.rpy) and he can end or
# restart it in the Ask menu (interactions.rpy). While it is on:
#   - her weekly allowance lands on Fridays (Wait 6a1), additive to the family's $100 and never frozen;
#   - every orgasm of hers in a scene pays him (sugar_payout_orgasm, hook in GirlCumming), capped per scene
#     (_sugar_scene_paid, reset with the session in femdom_session_reset / sub_event_reset);
#   - the "Charge her" answers of the sub-events quote her real price (sugar_charge_quote: the financial
#     table x SUGAR_CHARGE_MULT) instead of the flat $100, and she almost always pays;
#   - he can ask her for spending money or an item of the shop (cooldown days).
# Every payment logs [SUGAR].
# ============================================================

default _sugar_scene_paid = 0       # her paid orgasms this scene (cap SUGAR_ORGASM_CAP; session resets clear it)

init python:

    SUGAR_ALLOWANCE = 400           # her Friday transfer
    SUGAR_PER_ORGASM = 25           # per orgasm of hers in a scene...
    SUGAR_HARD_MULT = 2             # ...x2 when it is a hard one
    SUGAR_ORGASM_CAP = 3            # paid orgasms per scene
    SUGAR_CHARGE_MULT = 1.5         # x the financial table when a sugar girl is charged
    SUGAR_CHARGE_ACCEPT = 0.95      # she almost never refuses to pay
    SUGAR_GIFT_CASH = 150           # "Ask her for spending money"
    SUGAR_GIFT_COOLDOWN = 2         # days between money asks
    SUGAR_ITEM_COOLDOWN = 3         # days between item asks
    SUGAR_OFFER_COOLDOWN = 4        # days before she offers the arrangement again after "not now"
    SUGAR_SPONT_CHANCE = 0.06       # a morning text with a small transfer, while the arrangement is on
    SUGAR_SPONT_CASH = 100

    def sugar_eligible(girl):
        """She could offer the arrangement: a rich submissive who already shares his bed."""
        return (hasattr(girl, "has_trait") and girl.has_trait("submissive") and girl.has_trait("rich")
                and girl_had_sex(girl))

    def sugar_active(girl):
        """The arrangement is on (her offer accepted, not ended) and she still is who she was."""
        return bool(getattr(girl, "_sugar_mommy", False)) and sugar_eligible(girl)

    def sugar_girls_active():
        return [_g for _g in ALL_GIRLS if sugar_active(_g)]

    def sugar_offer_girl():
        """The girl whose arrangement offer texts him this morning (Wait 6h2), or None."""
        for _g in ALL_GIRLS:
            if not sugar_eligible(_g) or getattr(_g, "_sugar_mommy", False):
                continue
            if getattr(_g, "_sugar_offer_day", 0) > store.Day:
                continue
            if getattr(_g, "_sugar_ended_once", False):
                continue   # he ended it: she waits for HIM to ask (the Ask menu), she never re-offers
            if girl_is_away(_g) or getattr(_g, "loc", None) == store.CurrentLocation:
                continue
            if _g.gid not in getattr(store.Player, "phone_contacts", set()):
                continue
            if hasattr(_g, "has_temp_status") and (_g.has_temp_status("angry") or _g.has_temp_status("sad")):
                continue
            return _g
        return None

    def sugar_spont_girl():
        """A sugar girl whose small spontaneous transfer texts him this morning (one roll a day), or None."""
        for _g in sugar_girls_active():
            if girl_is_away(_g) or getattr(_g, "loc", None) == store.CurrentLocation:
                continue
            if _g.gid not in getattr(store.Player, "phone_contacts", set()):
                continue
            if hasattr(_g, "has_temp_status") and (_g.has_temp_status("angry") or _g.has_temp_status("sad")):
                continue
            if renpy.random.random() <= SUGAR_SPONT_CHANCE:
                return _g
        return None

    def sugar_payout_orgasm(girl, hard=False):
        """Her orgasm pays him (hook in GirlCumming, right after her counter): silent popup, capped per scene."""
        if not sugar_active(girl):
            return
        if store._sugar_scene_paid >= SUGAR_ORGASM_CAP:
            print("[SUGAR] %s orgasm payout capped this scene (%d)" % (girl.gid, SUGAR_ORGASM_CAP))
            return
        _amt = SUGAR_PER_ORGASM * (SUGAR_HARD_MULT if hard else 1)
        store._sugar_scene_paid += 1
        Player.add_cash(_amt)
        renpy.show_screen("StatHolder", value=_amt, prefix="+", color="#4ade80",
                          xpos=0.5, ypos=0.35, label_text="$",
                          hide_tag="stat_sugar_cash", _tag="stat_sugar_cash")
        print("[SUGAR] %s came: +$%d (%d/%d this scene, hard=%s, cash %d)" % (
            girl.gid, _amt, store._sugar_scene_paid, SUGAR_ORGASM_CAP, hard, Player.cash))

    def _sugar_price_table(girl, act):
        """_calc_financial_price without its side effects (it writes store._financial_gap / _financial_gap_mult,
        read later by the financial flow: snapshot and restore them)."""
        _gap, _mult = getattr(store, "_financial_gap", None), getattr(store, "_financial_gap_mult", None)
        try:
            return _calc_financial_price(girl, act)
        finally:
            store._financial_gap, store._financial_gap_mult = _gap, _mult

    def sugar_charge_quote(girl, act):
        """The price the 'Charge her' answers show and take (store._se_charge_now): a sugar girl pays her real
        price (financial table x SUGAR_CHARGE_MULT, rounded to 10), anyone else the flat _SE_CHARGE_PRICE."""
        if sugar_active(girl):
            _p = max(50, int(round(_sugar_price_table(girl, act) * SUGAR_CHARGE_MULT / 10.0)) * 10)
        else:
            _p = _SE_CHARGE_PRICE
        store._se_charge_now = _p
        print("[SUGAR] charge quote for %s (%s): $%d (sugar=%s)" % (girl.gid, act, _p, sugar_active(girl)))
        return _p

    def sugar_charge_accepts(girl):
        """Her answer to being charged: a sugar girl pays almost always, the rest keep today's odds."""
        if sugar_active(girl):
            return renpy.random.random() <= SUGAR_CHARGE_ACCEPT
        return _se_charge_accepts(girl)

    def sugar_charge_paid(girl, why="charge"):
        """The ONE writer of a paid 'Charge her' (store._se_charge_now): money, popup, achievement, log.
        The popup matters: the HUD is hidden mid-scene, so a silent add_cash read as her never paying
        (tester 2026-10-11, "WHERES MAH MONEY")."""
        _amt = int(getattr(store, "_se_charge_now", 0) or 0)
        if _amt > 0:
            Player.add_cash(_amt)
        renpy.show_screen("StatHolder", value=_amt, prefix="+", color="#4ade80",
                          xpos=0.5, ypos=0.35, label_text="$",
                          hide_tag="stat_sugar_cash", _tag="stat_sugar_cash")
        unlock_achievement("reverse_card")
        print("[SUGAR] %s paid the %s charge: +$%d (cash %d)" % (girl.gid, why, _amt, Player.cash))

default _se_charge_now = 100

# ── Her offer (Wait 6h2): she proposes to keep him ──
label _sugar_mommy_offer(girl):
    play sound "audio/Notification.mp3" noloop
    "Your phone buzzes. Someone sent you a message."
    call _phone_typing(girl, choices=[]) from _sugar_offer_typing_1
    $ phone_add_msg(girl.gid, girl.gid, _tl(_("I've been thinking about what I'm good for, these days.")))
    call _phone_typing(girl, choices=[]) from _sugar_offer_typing_2
    $ phone_add_msg(girl.gid, girl.gid, _tl(_("Let me take care of you. Money, I mean. It's the one language I still speak better than anyone.")))
    call _phone_typing(girl, choices=[]) from _sugar_offer_typing_3
    $ phone_add_msg(girl.gid, girl.gid, _tl(_("A weekly transfer. Whatever you need, when you need it. Nobody has to know where it comes from.")))
    call screen phone_chat_screen(girl, choices=[(_("Take care of me, then."), "yes"), (_("Not now."), "later")])
    if _return == "yes":
        $ phone_add_msg(girl.gid, "player", _tl(_("Take care of me, then.")))
        call _phone_typing(girl, choices=[]) from _sugar_offer_typing_yes
        $ phone_add_msg(girl.gid, girl.gid, _tl(_("Good. Check your account on Friday. And don't argue with the amounts.")))
        python:
            girl._sugar_mommy = True
            print("[SUGAR] %s arrangement ON (her offer accepted)" % girl.gid)
    else:
        $ phone_add_msg(girl.gid, "player", _tl(_("Not now.")))
        call _phone_typing(girl, choices=[]) from _sugar_offer_typing_no
        $ phone_add_msg(girl.gid, girl.gid, _tl(_("The offer doesn't expire. I'll ask again.")))
        python:
            girl._sugar_offer_day = store.Day + SUGAR_OFFER_COOLDOWN
            print("[SUGAR] %s offer postponed to Day %d" % (girl.gid, girl._sugar_offer_day))
    call screen phone_chat_screen(girl, choices=[])
    $ _phone_restore_others()
    return

# ── Her small spontaneous transfer (Wait 6h2 while the arrangement is on) ──
label _sugar_spont_gift(girl):
    play sound "audio/Notification.mp3" noloop
    "Your phone buzzes. Someone sent you a message."
    call _phone_typing(girl, choices=[]) from _sugar_spont_typing
    python:
        Player.add_cash(SUGAR_SPONT_CASH)
        print("[SUGAR] %s spontaneous transfer +$%d (cash %d)" % (girl.gid, SUGAR_SPONT_CASH, Player.cash))
        phone_add_msg(girl.gid, girl.gid, _tl(_("I sent you a little something. No reason. Spend it badly.")))
    call screen phone_chat_screen(girl, choices=[])
    $ _phone_restore_others()
    return

# ── The Ask menu entries (talk_ask_question, interactions.rpy) ──
label _sugar_ask_money(girl):
    if getattr(girl, "_sugar_money_day", 0) > Day:
        $ set_scene_expression(girl, "normal")
        $ Say_Line(girl, _("Again? I just did. Friday isn't far. ...Fine, ask me Friday."))
        $ set_scene_expression(girl, "normal")
        return
    python:
        girl._sugar_money_day = store.Day + SUGAR_GIFT_COOLDOWN
        Player.add_cash(SUGAR_GIFT_CASH)
        print("[SUGAR] %s hand-out +$%d (next ask Day %d, cash %d)" % (girl.gid, SUGAR_GIFT_CASH, girl._sugar_money_day, Player.cash))
    $ set_scene_expression(girl, "happy")
    $ Say_Line(girl, _("Of course. Here. I like it when you ask instead of pretending you don't need it."))
    $ Change_Status(girl, "Love", 2)
    $ set_scene_expression(girl, "normal")
    return

label _sugar_ask_item(girl):
    if getattr(girl, "_sugar_item_day", 0) > Day:
        $ set_scene_expression(girl, "normal")
        $ Say_Line(girl, _("Another one already? Give me a couple of days between favors, or I'll start auditing you."))
        $ set_scene_expression(girl, "normal")
        return
    if not Player.has_item("tripod"):
        python:
            girl._sugar_item_day = store.Day + SUGAR_ITEM_COOLDOWN
            Player.add_item("tripod", 1)
            _pharmacy_popup("Tripod", 1, 0)
            print("[SUGAR] %s bought him the tripod (next ask Day %d)" % (girl.gid, girl._sugar_item_day))
        $ set_scene_expression(girl, "smug")
        $ Say_Line(girl, _("A tripod. I don't ask what for. ...I absolutely know what for. It's already paid."))
    else:
        $ set_scene_expression(girl, "normal")
        $ Say_Line(girl, _("You already own everything I'd buy you today. Think of something and ask me again."))
    $ set_scene_expression(girl, "normal")
    return

# ── Ending / restarting the arrangement (the Ask menu) ──
label _sugar_toggle_off(girl):
    python:
        girl._sugar_mommy = False
        girl._sugar_ended_once = True   # from now on only HE restarts it (_sugar_toggle_on)
        girl._sugar_offer_day = store.Day + SUGAR_OFFER_COOLDOWN
        print("[SUGAR] %s arrangement OFF (he ended it)" % girl.gid)
    $ set_scene_expression(girl, "sad")
    $ Say_Line(girl, _("...Alright. The transfers stop. The offer doesn't. Say the word and it all comes back."))
    $ set_scene_expression(girl, "normal")
    return

label _sugar_toggle_on(girl):
    python:
        girl._sugar_mommy = True
        print("[SUGAR] %s arrangement ON (he asked for it back)" % girl.gid)
    $ set_scene_expression(girl, "happy")
    $ Say_Line(girl, _("I never closed the account. Check it Friday. ...Thank you for asking me again."))
    $ set_scene_expression(girl, "normal")
    return
