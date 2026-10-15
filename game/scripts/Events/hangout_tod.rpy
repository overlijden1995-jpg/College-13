# ============================================================
# TRUTH OR DARE — Hangout sub-event
# Bottle spin -> target picks truth or dare
# ============================================================

# The fetish she named in her last "What's your biggest fetish?" answer (None: no fetish trait answered);
# the watching partner reacts to that one, not to every trait she has (_bf_content_reaction)
default _tod_fetish_pick = None

init python:

    _TOD_MILD_ACTS ={"kiss", "touch", "touch_thighs", "touch_ass", "touch_tits", "touch_pussy"}

    # Acts whose name (_act_names) reads well after "Doing": "Doing sex" / "Doing riding someone" do not
    _TOD_DOING_ACTS = ("anal", "bj", "tj", "hj")

    def tod_bf_partner_did(girl, act, current=False):
        """bf_history's `act` (bf_has_done) as every answer of this file must read it: a male act
        (BF_MALE_ONLY_ACTS, characters_stats.rpy) is never read straight from bf_history: a girlfriend never did one,
        and with a girlfriend it is only an experienced non-lesbian's past with men (bf_history_from_men).
        current=True: only when that history is her CURRENT NPC partner's (_is_bf_context), the condition of a line
        that says "my %(pl)s did it". set_npc_partner rolls a new history for every new partner and clear_npc_partner
        keeps it, so with no partner it is her ex's (or an experienced girl's past) and %(pl)s names nobody (or the
        player, when she dates him): those answers say "my ex" / "someone I was dating"."""
        _cur = _is_bf_context(girl)
        _did = bool(girl.bf_has_done(act))
        _gf_male = bool(act in BF_MALE_ONLY_ACTS and _cur and girl.has_npc_girlfriend())
        if _gf_male:
            _did = _did and not current and bf_history_from_men(girl)
        elif current:
            _did = _did and _cur
        print("[TOD] bf_history %s act=%s current=%s: %s (partner=%s girlfriend_male_act=%s)" % (
            girl.gid, act, current, _did, _cur, _gf_male))
        return _did

    def tod_girl_picks_dare(girl):
        """Girls pick truth or dare based on Inbt + alcohol.
        Higher Inbt and more drunk = more likely to pick dare."""
        inbt = getattr(girl, "Inbt", 0)
        alc = tod_effective_alc(girl)   # bonus caps at the sweet-spot top

        # Base dare chance from Inbt (0-1000 -> 10%-60%)
        base = 0.10 + (inbt / 1000.0) * 0.50

        # Alcohol boost (+3% per level)
        base += alc * 0.03

        base = max(0.10, min(0.90, base))
        return renpy.random.random() < base

    def _tod_girl_strip_level(girl):
        """Get the current strip level for a girl (0-4)."""
        key = "_hangout_strip_level_" + girl.gid
        return getattr(store, key, 0)

    def tod_girl_refuses(girl):
        """A girl may refuse to answer a truth question.
        Returns True if she refuses (must drink and strip as penalty).
        If next strip would expose chest or panties, she's less likely to refuse."""
        inbt = getattr(girl, "Inbt", 0)
        alc = tod_effective_alc(girl)
        strip_lvl = _tod_girl_strip_level(girl)

        # Base refuse chance
        if inbt < 200 and alc < 5:
            chance = 0.25
        elif inbt < 400 and alc < 3:
            chance = 0.10
        else:
            return False

        # If next strip would expose chest (level 2->3) or panties (level 3->4),
        # she's more motivated to answer instead of stripping
        if strip_lvl == 2:
            chance -= 0.20  # rather answer than show boobs
        elif strip_lvl == 3:
            chance -= 0.30  # really doesn't want to show everything
        elif strip_lvl >= 4:
            chance -= 0.15  # already naked, less pressure

        chance = max(0.02, chance)
        return renpy.random.random() < chance

    def tod_spin_bottle(participants):
        """Spin the bottle. Returns a random participant.
        participants = list of (id_string, display_obj) tuples.
        """
        return renpy.random.choice(participants)

    # ── SAFE truth questions ──────────────────────────────
    # Each function returns (question_text, answer_lines, discovery_keys)
    # answer_lines = list of (speaker, text) where speaker is girl obj or "player"
    # discovery_keys = list of strings to pass to girl.discover() ONLY if she answers

    def tod_truth_who_you_like_most(girl, other_girl):
        """Who do you like most on campus?"""
        question = _("Who do you like the most on campus right now?")
        _discoveries = []
        like_player = getattr(girl, "Love", 0)
        like_other = int(girl.Girl_like.get(other_girl.gid, 500))
        other_name = other_girl.Name

        _is_dating_p = hasattr(girl, "is_dating_player") and girl.is_dating_player()
        if _is_dating_p:
            answers = [
                (girl, _("My boyfriend, obviously. Was that supposed to be a hard question?"), "happy"),
                (girl, _("You, duh. We're literally dating."), "smirk"),
                (girl, _("Do I really have to say it out loud? You. Always you."), "happy"),
            ]
        elif like_player > like_other and like_player >= 400:
            answers = [
                (girl, _("Hmm... honestly? I think I like hanging out with you the most."), "shy", "1"),
                (girl, _("Don't make it weird, but... probably you."), "shy", "1"),
                (girl, _("I mean... you are the one who invited me here, so..."), "shy", "1"),
            ]
        elif like_other > like_player and like_other >= 600:
            answers = [
                (girl, _tl(_("Honestly? %s. We just click, you know?")) % other_name, "looking_left"),
                (girl, _tl(_("%s, for sure. She gets me.")) % other_name, "looking_left"),
                (girl, _tl(_("Probably %s. We've been getting along really well lately.")) % other_name, "looking_left"),
            ]
        else:
            answers = [
                (girl, _("That's hard! I like both of you. Don't make me choose."), "happy"),
                (girl, _("Hmm... I don't think I can pick just one person."), "happy"),
                (girl, _("You're both pretty cool, honestly. I'm not picking favorites."), "happy"),
            ]
        return (question, [renpy.random.choice(answers)], _discoveries)

    def tod_truth_had_boyfriend(girl):
        """Have you ever had a boyfriend/girlfriend?"""
        _discoveries = []
        has_bf = getattr(girl, "npc_partner_id", None) is not None
        _is_f = girl.get_flag("partner_is_female") if hasattr(girl, "get_flag") else False
        _pl = girl.partner_label() if hasattr(girl, "partner_label") and has_bf else (_tr("girlfriend") if _is_f else _tr("boyfriend"))
        question = _tl(_("Have you ever had a %s?")) % _pl
        bf_loyalty = getattr(girl, "bf_loyalty", 0)
        is_ex = hasattr(girl, "is_ex_of_player") and girl.is_ex_of_player()
        _ex_hist = getattr(girl, "ex_player_history", None) if is_ex else None

        if is_ex:
            _ex_mood = _ex_hist.get("breakup_mood", "angry") if _ex_hist else "angry"
            if _ex_mood == "sad":
                answers = [
                    (girl, _("I was with someone recently. We broke up. I'm still getting over it..."), "sad"),
                    (girl, _("Yeah... I dated someone. It didn't end well. I'd rather not talk about it."), "sad"),
                    (girl, _("I had a boyfriend. Recently. It's... complicated. And painful."), "sad"),
                ]
            else:
                answers = [
                    (girl, _("Yeah. I dated someone. It ended badly. Let's leave it at that."), "angry"),
                    (girl, "I had a boyfriend. {hint}He's closer than you think{/hint}. But we're done.", "angry"),
                    (girl, _("Don't even get me started. Yes, I dated someone. He screwed it up."), "angry"),
                ]
            _discoveries.append("discovered_ex_relationship")
            return (question, [renpy.random.choice(answers)], _discoveries)

        if has_bf and bf_loyalty >= 500:
            answers = [
                (girl, "Yeah... I actually {hint}have one right now{/hint}. It's... complicated.", "looking_right", "1"),
                (girl, "I do, actually. {hint}I'm with someone{/hint}. But let's not talk about that tonight.", "looking_right", "1"),
                (girl, _format_partner_line(girl, _("Mhm. I {hint}have a %(pl)s{/hint}. Things have been a bit weird lately though.")), "looking_right", "1"),
            ]
            _discoveries.append("discovered_has_partner")
        elif has_bf and bf_loyalty < 500:
            answers = [
                (girl, "Technically yes. But honestly, {hint}it doesn't feel like it anymore{/hint}.", "uncomfortable"),
                (girl, "I {hint}have one on paper{/hint}. In practice... I don't know what we are.", "uncomfortable"),
                (girl, "Yeah. But {hint}things haven't been great{/hint}. Can we move on?", "uncomfortable"),
            ]
            _discoveries.append("discovered_has_partner")
        elif getattr(store, "_hangout_is_harem_night", False) and girl.is_dating_player():
            answers = [
                (girl, _("I have a boyfriend right now. We all know who he is. And I'm sharing him with this one~"), "smirk"),
                (girl, _("Yeah, I have one. He's sitting right there. Along with his other girlfriend."), "sly"),
                (girl, "Do I have a boyfriend? Technically, {hint}we all do{/hint}. Same one.", "happy"),
            ]
        elif hasattr(girl, "is_dating_player") and girl.is_dating_player():
            answers = [
                (girl, _("Yeah, I have a boyfriend right now. It's going really well, actually."), "happy"),
                (girl, _("I do, actually. He makes me really happy."), "happy"),
                (girl, _("Yeah... I'm with someone. It feels right."), "shy"),
            ]
            _discoveries.append("discovered_has_partner")
        else:
            answers = [
                (girl, "Nope! {hint}Free as a bird{/hint}.", "happy"),
                (girl, "Not right now. I'm {hint}enjoying being single{/hint}, honestly.", "smug"),
                (girl, _("No. Haven't found anyone worth the trouble yet."), "happy"),
            ]
            _discoveries.append("discovered_single")
        return (question, [renpy.random.choice(answers)], _discoveries)

    def tod_truth_first_notice_about_player(girl):
        """What's the first thing you noticed about me?"""
        question = _("What's the first thing you noticed about me?")
        _discoveries = []
        attr = getattr(store.Player, "attractiveness", 50)

        if attr >= 76:
            answers = [
                (girl, _("Your face. Obviously. You're not exactly hard to look at."), "smirk", "1"),
                (girl, _("Honestly? Your looks. Don't let that go to your head."), "smirk", "1"),
                (girl, _("The way you carry yourself. You've got this... confidence thing going on."), "smirk", "1"),
                (girl, _("Your smile. It's kind of hard to miss."), "smirk", "1"),
            ]
        elif attr >= 26:
            answers = [
                (girl, _("Your vibe, I guess. You seemed chill."), "happy"),
                (girl, _("Hmm... you just seemed like someone easy to talk to."), "happy"),
                (girl, _("Your sense of humor, probably. You said something funny early on."), "happy"),
                (girl, _("I don't know, you just seemed... normal? In a good way."), "happy"),
            ]
        else:
            answers = [
                (girl, _("Your persistence, honestly. You kept trying to talk to me."), "bemused"),
                (girl, _("Hmm... I think it was your attitude. You didn't give up easily."), "bemused"),
                (girl, _("You were... bold. I'll give you that."), "bemused"),
                (girl, _("I noticed you kept looking my way. It was kind of endearing, actually."), "bemused"),
            ]
        return (question, [renpy.random.choice(answers)], _discoveries)

    def tod_truth_worst_gift(girl):
        """What's the worst gift you've ever received?"""
        question = _("What's the worst gift you've ever received?")
        _discoveries = []
        answers = [
            (girl, _("Someone gave me a self-help book once. Like, what are you trying to say?"), "laugh"),
            (girl, _("Socks. On my birthday. Just... socks."), "happy"),
            (girl, _("A candle that smelled like old shoes. I'm not even joking."), "laugh"),
            (girl, _("One time someone gave me a gift card with like two dollars on it."), "happy"),
            (girl, _("A stuffed animal that looked like it had seen better days. Way better days."), "laugh"),
            (girl, _("My ex gave me a mug that said 'World's Okayest Girlfriend'. We broke up shortly after."), "happy"),
        ]
        return (question, [renpy.random.choice(answers)], _discoveries)

    def tod_truth_exam_grades(girl):
        """What were your last exam grades? (only if exams have happened)"""
        question = _("How did you do on your last exam?")
        _discoveries = []
        study = getattr(girl, "study_level", 0)
        # study_level resets after exam, so if Day >= EXAM_FIRST_DAY, at least one happened
        # We generate a fake remembered grade for flavor
        grade_pool_good = ["A", "A", "B"]
        grade_pool_mid = ["B", "C", "C"]
        grade_pool_bad = ["D", "D", "F"]

        # Smart girls (high study or high Love = motivated) tend to do better
        if study >= 7:
            grade = renpy.random.choice(grade_pool_good)
        elif study >= 4:
            grade = renpy.random.choice(grade_pool_mid)
        else:
            grade = renpy.random.choice(grade_pool_bad)

        if grade in ("A", "B"):
            answers = [
                (girl, _tl(_("I got a %s! I actually studied for once.")) % grade, "happy"),
                (girl, _tl(_("Pretty good, actually. %s. I was surprised myself.")) % grade, "smug"),
                (girl, _tl(_("%s. Not bad, right? I might actually graduate.")) % grade, "happy"),
            ]
        elif grade == "C":
            answers = [
                (girl, _("A C. Could be worse, could be better. Story of my life."), "looking_left"),
                (girl, _("C. I'll take it. I barely studied anyway."), "bemused"),
                (girl, _("Average. A solid C. I'm okay with that."), "looking_left"),
            ]
        else:
            answers = [
                (girl, _("...Next question."), "embarrassed"),
                (girl, _("Let's just say it wasn't my proudest moment."), "grimace"),
                (girl, _("Bad. Really bad. I don't want to talk about it."), "embarrassed"),
            ]
        return (question, [renpy.random.choice(answers)], _discoveries)

    def tod_truth_favorite_hobby(girl):
        """What's your favorite hobby?"""
        question = _("What do you do for fun when you're not studying?")
        _discoveries = []
        hobby_pool = [
            (girl, _("Swimming. There's something about being in the water that just clears my head."), "normal"),
            (girl, _("Working out. I know it sounds basic, but it really helps with stress."), "happy"),
            (girl, _("Reading. I can lose hours in a good book and not even notice."), "normal"),
            (girl, _("Listening to music. I have playlists for every mood."), "happy"),
            (girl, _("Going for walks. Sometimes I just wander around campus at night."), "normal"),
        ]
        return (question, [renpy.random.choice(hobby_pool)], _discoveries)

    def tod_truth_sexuality(girl):
        """Are you into guys, girls, or both?"""
        question = _("Are you into guys, girls, or both?")
        _discoveries = []
        _is_les = hasattr(girl, "has_trait") and girl.has_trait("lesbian")
        _is_bi = hasattr(girl, "has_trait") and girl.has_trait("bisexual")
        has_bf = getattr(girl, "npc_partner_id", None) is not None
        _is_f = girl.get_flag("partner_is_female") if hasattr(girl, "get_flag") else False
        alc = hangout_get_alcohol(girl)
        _had_sex_w_player = girl_had_sex(girl)

        if _is_les:
            if _had_sex_w_player:
                answers = [
                    (girl, _("Girls. Only girls. ...Usually. Don't ask about the exceptions."), "uncomfortable", "1"),
                    (girl, _("I'm a lesbian. What happened between us doesn't change that. It just... complicates things."), "looking_left", "1"),
                    (girl, _("I like women. Period. Whatever you think happened doesn't count."), "serious"),
                ]
            elif alc >= 5:
                answers = [
                    (girl, _("Girls. One hundred percent. Although... some guys can be charming, I'll give you that."), "smirk", "1"),
                    (girl, _("Women. But I'd be lying if I said I've never been curious. Just a little."), "sly", "1"),
                ]
            else:
                answers = [
                    (girl, "Girls. I'm a lesbian.", "neutral"),
                    (girl, _("Women. Always have been, always will be."), "serious"),
                    (girl, _("Only girls. That's not really a mystery, is it?"), "smirk"),
                ]
            _discoveries.append("discovered_trait_lesbian")
        elif _is_bi:
            if has_bf and _is_f:
                answers = [
                    (girl, _("Both, actually. I'm with a girl right now, but I've always liked guys too."), "happy"),
                    (girl, _("I'm bi. Having a girlfriend doesn't mean I'm not into guys."), "smirk"),
                    (girl, _("Both. People assume I'm gay because I'm dating a girl, but... nope. I like both."), "happy"),
                ]
            elif has_bf and not _is_f:
                answers = [
                    (girl, _("Both. I have a boyfriend, but I've been with girls too. I like who I like."), "happy"),
                    (girl, _("I'm bi. My boyfriend knows. It's not a big deal."), "smirk"),
                ]
            elif hasattr(girl, "is_dating_player") and girl.is_dating_player():
                answers = [
                    (girl, _("Both. My boyfriend is right there, but I've always liked girls too."), "happy"),
                    (girl, _("I'm bi. My boyfriend knows. He's pretty cool about it, actually."), "smirk"),
                    (girl, _("Guys and girls. And yes, my boyfriend is very aware."), "sly"),
                ]
            else:
                answers = [
                    (girl, _("Both. I like guys and girls. Why limit yourself, right?"), "sly"),
                    (girl, _("I'm bi. I don't really have a preference. Depends on the person."), "happy"),
                    (girl, _("Both. Always have been. It took me a while to figure that out, but yeah."), "happy"),
                ]
            _discoveries.append("discovered_trait_bisexual")
        else:
            if alc >= 5:
                answers = [
                    (girl, _("Guys. Definitely guys. Although... some girls are really pretty. Not in that way! ...Maybe a little."), "embarrassed", "1"),
                    (girl, _("Men. But I'm not blind. Some women are gorgeous. I can appreciate that."), "smirk"),
                ]
            else:
                answers = [
                    (girl, _("Guys. Pretty straightforward, honestly."), "happy"),
                    (girl, _("Men. Nothing complicated about that."), "neutral"),
                    (girl, _("I like guys. Always have."), "happy"),
                ]
        return (question, [renpy.random.choice(answers)], _discoveries)

    # ── LEWD truth questions ─────────────────────────────
    # All based on real game data: Sex_acts, traits, raw_sex_count, etc.

    def tod_lewd_most_extreme(girl):
        """What's the most extreme thing you've ever done?"""
        question = _("What's the most extreme thing you've done... sexually?")
        _discoveries = []
        acts = getattr(girl, "Sex_acts", {})

        # Find the most extreme act she's done (by hierarchy)
        # Check creampie separately (not in Sex_acts)
        cream_count = getattr(girl, "CreampieCounts", 0)
        bf_creampie = tod_bf_partner_did(girl, "creampie")
        has_creampie = cream_count > 0 or bf_creampie

        _act_hierarchy = ["anal", "reverse_cowgirl", "cowgirl", "sex", "bj", "tj", "hj", "masturbate", "kiss"]
        _act_names = {
            "creampie": _tl(_("letting someone finish inside me")),
            "anal": _tl(_("anal")), "sex": _tl(_("sex")), "reverse_cowgirl": _tl(_("sex from behind")), "cowgirl": _tl(_("riding someone")),
            "bj": _tl(_("a blowjob")), "tj": _tl(_("a titjob")), "hj": _tl(_("a handjob")),
            "masturbate": _tl(_("touching myself for someone")), "kiss": _tl(_("making out")),
        }
        # Creampie is the most extreme if it happened
        top_act = None
        if has_creampie:
            top_act = "creampie"

        if top_act is None:
            for a in _act_hierarchy:
                if acts.get(a, 0) > 0:
                    top_act = a
                    break

        if top_act is None:
            # Check BF history as fallback (its creampie, read through tod_bf_partner_did, is already in has_creampie)
            bf_hist = getattr(girl, "bf_history", {})
            for a in _act_hierarchy:
                # bf_history only knows ACTS. "sex" there never proves a position, so she
                # answers with the act ("having sex"), never "sex from behind" / "riding someone"
                key = scene_type_act(a)
                if bf_hist.get(key, False):
                    top_act = key
                    break

        # Check for extreme combos: multiple creampies and/or public acts.
        # Several in one night: process_cum records the most creampies she took in one time slot
        # (_creampie_slot_max, 0 on a save older than it). The counts give a second proof that also covers what
        # happened before the record existed: every creampie happens in a session that counted sex, anal or the
        # tip, so more creampies than those sessions proves that one session had two or more (pigeonhole: at least
        # the rounded-up ratio). The larger of the two answers.
        # The place (no log keeps it with a creampie): when the location log holds every one of those sessions and
        # they all took place at ONE public place, every creampie happened there.
        _cream_acts = _SEX_PENETRATION_ACTS + ("tip",)
        _cream_sessions = girl_act_counts(girl)[0] + acts.get("tip", 0)
        _cream_slot_rec = getattr(girl, "_creampie_slot_max", 0) or 0
        _cream_count_proof = -(-cream_count // _cream_sessions) if _cream_sessions else 0
        _cream_night_max = max(_cream_slot_rec, _cream_count_proof)
        _pub_locs = {"campus", "classroom", "pool", "gym", "showers", "hall", "street", "mall", "restaurant_restroom"}
        _pub_acts = [s for s in getattr(girl, "Sex_act_locations", []) if s.get("location", "") in _pub_locs and s.get("act", "") not in _TOD_MILD_ACTS]
        _cream_log = [s.get("location", "") for s in getattr(girl, "Sex_act_locations", []) if s.get("act", "") in _cream_acts]
        _cream_pub_loc = _cream_log[0] if (cream_count > 1 and _cream_sessions and len(_cream_log) >= _cream_sessions
                                          and len(set(_cream_log)) == 1 and _cream_log[0] in _pub_locs) else None
        # The public answer names the most extreme act she did THERE (top_act may have happened anywhere)
        _pub_top = next((a for a in _act_hierarchy if any(s.get("act", "") == a for s in _pub_acts)), None)
        _pub_loc_names = {"campus": _("campus"), "classroom": _("the classroom"), "pool": _("the pool"), "gym": _("the gym"), "showers": _("the showers"), "hall": _("the hallway"), "street": _("the street"), "mall": _("the mall"), "restaurant_restroom": _("the restaurant restroom")}
        print("[TOD] most_extreme %s: creampies=%d cream_sessions=%d night_max=%d (slot record %d, count proof %d) cream_pub_loc=%s pub_top=%s top_act=%s" % (
            girl.gid, cream_count, _cream_sessions, _cream_night_max,
            _cream_slot_rec, _cream_count_proof, _cream_pub_loc, _pub_top, top_act))

        if _cream_pub_loc:
            _ploc_name = _tl(_pub_loc_names.get(_cream_pub_loc, _cream_pub_loc))
            answers = [
                (girl, _tl(_("Someone came inside me multiple times... at %s. In public. I don't even know who I am anymore.")) % _ploc_name, "lipbite", "2"),
                (girl, _tl(_("Getting creampied more than once at %s. That's... yeah. That's my answer.")) % _ploc_name, "lipbite", "2"),
            ]
            return (question, [renpy.random.choice(answers)], _discoveries)
        elif _cream_night_max >= 2:
            answers = [
                (girl, _("Letting someone cum inside me... more than once. In the same night. I couldn't say no."), "embarrassed", "2"),
            ]
            if _cream_night_max >= 3:   # "I lost count": three or more in that one night
                answers.append((girl, _("Multiple creampies. One after another. I lost count at some point."), "embarrassed", "2"))
            return (question, [renpy.random.choice(answers)], _discoveries)
        elif _pub_top:
            _ploc = renpy.random.choice([s for s in _pub_acts if s.get("act", "") == _pub_top]).get("location", "")
            _ploc_name = _tl(_pub_loc_names.get(_ploc, _ploc))
            _act_name = _act_names[_pub_top]
            answers = [
                (girl, _tl(_("%s at %s. In public. My heart was about to explode.")) % (_act_name.capitalize(), _ploc_name), "sly", "1"),
            ]
            if _pub_top in _TOD_DOING_ACTS:
                answers.append((girl, _tl(_("Doing %s at %s. Where anyone could have walked in.")) % (_act_name, _ploc_name), "sly", "1"))
            return (question, [renpy.random.choice(answers)], _discoveries)

        # Virginity loss to player is extremely personal and extreme
        _vtp = getattr(girl, "virginity_taken_by_player", False)
        if _vtp and top_act in ("reverse_cowgirl", "cowgirl", "sex"):
            alc = hangout_get_alcohol(girl)
            if alc >= 5:
                answers = [
                    (girl, _("I lost my virginity. To someone in this room. And I don't regret it."), "shy", "2"),
                    (girl, "My first time. With {hint}him{/hint}. I was shaking the whole time... but it was everything.", "shy", "2"),
                    (girl, _tl(_("Losing my virginity to %s. That's my answer.")) % getattr(store.Player, "Name", "someone"), "shy", "2"),
                ]
            else:
                answers = [
                    (girl, _("Losing my virginity. That's my answer. I'm not giving details."), "embarrassed", "1"),
                    (girl, _("My... first time. It was intense. I'll leave it at that."), "embarrassed", "1"),
                    (girl, _("I gave someone my first time. That's the most extreme thing I've ever done."), "embarrassed", "1"),
                ]
            return (question, [renpy.random.choice(answers)], _discoveries)

        if top_act is None:
            answers = [
                (girl, "...{hint}Nothing{/hint}. I haven't done anything like that.", "confused"),
                (girl, "I'm serious, I {hint}haven't done anything{/hint}. Stop looking at me like that.", "normal"),
                (girl, _("Honestly? Nothing worth mentioning. I'm boring, I know."), "confused"),
            ]
        elif top_act == "creampie":
            has_cum_slut = hasattr(girl, "has_trait") and girl.has_trait("cum_slut")
            if has_cum_slut:
                answers = [
                    (girl, "I {hint}let someone finish inside me{/hint}. And I loved it. Every. Second.", "lusty", "1"),
                    (girl, "{hint}Creampie{/hint}. There, I said it. And honestly? I'd do it again in a heartbeat.", "lusty", "1"),
                    (girl, "The most extreme? {hint}Letting someone cum inside me{/hint}. And wanting more.", "lusty", "1"),
                ]
            elif cream_count > 1:
                answers = [
                    (girl, "I've... {hint}let someone finish inside me{/hint}. More than once. I know.", "embarrassed", "2"),
                ]
                if cream_count >= 3:   # "a few times": three or more
                    answers.append((girl, "Someone {hint}came inside me{/hint}. It happened a few times. I'm still processing it.", "embarrassed", "2"))
            else:
                answers = [
                    (girl, "I... {hint}let someone finish inside me{/hint} once. My heart almost stopped.", "scared", "1"),
                    (girl, "Someone {hint}came inside me{/hint}. It just... happened. I was terrified afterward.", "worried", "1"),
                    (girl, "The most extreme thing? Probably {hint}letting it happen without protection. Inside{/hint}.", "worried", "1"),
                ]
        elif top_act in ("anal", "sex", "reverse_cowgirl", "cowgirl"):
            act_name = _act_names[top_act]
            count = acts.get(top_act, 0)
            if count > 3:
                answers = [
                    (girl, _tl(_("Probably {hint}%s{/hint}. And... more than once. Don't judge me.")) % act_name, "smirk", "1"),
                    (girl, _tl(_("{hint}%s{/hint}. I've done it a few times now. It gets better.")) % act_name.capitalize(), "smirk", "1"),
                    (girl, _tl(_("Let's just say {hint}%s{/hint} is not exactly new territory for me.")) % act_name, "smirk", "1"),
                ]
            else:
                answers = [
                    (girl, _tl(_("I guess... {hint}%s{/hint}. It was intense.")) % act_name, "shy", "1"),
                    (girl, _tl(_("{hint}%s{/hint}, probably. My heart was pounding the whole time.")) % act_name.capitalize(), "shy", "1"),
                    (girl, _tl(_("Um... {hint}%s{/hint}. I'm still not sure how I feel about it.")) % act_name, "shy", "1"),
                ]
        elif top_act in ("bj", "tj", "hj"):
            act_name = _act_names[top_act]
            answers = [
                (girl, _tl(_("Probably {hint}%s{/hint}. That's as far as I've gone.")) % act_name, "looking_left", "1"),
                (girl, _tl(_("{hint}%s{/hint}, I think. It was... an experience.")) % act_name.capitalize(), "looking_left", "1"),
                (girl, _tl(_("I've given {hint}%s{/hint} before. That's my limit so far.")) % act_name, "looking_left", "1"),
            ]
        else:
            act_name = _act_names.get(top_act, top_act)
            answers = [
                (girl, _tl(_("Just %s, really. Nothing too wild.")) % act_name, "shy"),
                (girl, _tl(_("%s. I know, not exactly scandalous.")) % act_name.capitalize(), "shy"),
            ]
        # Discover the extreme act if it was done with the player (not creampie)
        if top_act and top_act != "creampie" and acts.get(top_act, 0) > 0:
            _discoveries.append("discovered_extreme_" + top_act)
        return (question, [renpy.random.choice(answers)], _discoveries)

    def tod_lewd_recorded_video(girl):
        """Have you ever recorded an intimate video?"""
        question = _("Have you ever recorded an intimate video of yourself?")
        _discoveries = []
        has_camera_lover = hasattr(girl, "has_trait") and girl.has_trait("camera_lover")
        has_camera_hater = hasattr(girl, "has_trait") and girl.has_trait("camera_hater")

        # Check if player has recorded videos of this girl - only consensual ones (she knows about)
        vids = getattr(store.Player, "recorded_videos", [])
        girl_vids = [v for v in vids if v.get("girl_gid") == girl.gid and v.get("consensual", False)]
        has_vids = len(girl_vids) > 0

        # Build a description of a specific video if one exists
        _vid_desc = None
        if has_vids:
            _vpick = renpy.random.choice(girl_vids)
            _vtype = _vpick.get("type", "")
            _vloc = _vpick.get("location", "room")
            _vid_type_names = {
                "hj": _tl(_("a handjob")), "bj": _tl(_("a blowjob")), "tj": _tl(_("a titjob")),
                "cowgirl": _tl(_("me riding")), "reverse_cowgirl": _tl(_("it from behind")), "reverse_cowgirl_anal": _tl(_("it in the ass while riding")),
                "full_nelson": _tl(_("being held up")), "full_nelson_anal": _tl(_("being held up and taken from behind")),
                "laying_down": _tl(_("getting it while laying down")), "laying_anal": _tl(_("getting it in the ass while laying down")),
                "masturbate": _tl(_("me touching myself")), "creampie": _tl(_("a creampie")),
            }
            _vid_loc_names = {
                "room": _tl(_("in the room")), "pool": _tl(_("at the pool")), "showers": _tl(_("in the showers")),
                "campus": _tl(_("on campus")), "classroom": _tl(_("in the classroom")), "gym": _tl(_("at the gym")),
                "mall": _tl(_("at the mall")),
            }
            _vt = _vid_type_names.get(_vtype, _tl(_("something intimate")))
            _vl = _vid_loc_names.get(_vloc, _tl(_("somewhere")))
            _vid_desc = _tl("%s %s") % (_vt, _vl)

        if has_camera_hater:
            if has_vids:
                answers = [
                    (girl, _tl(_("I {hint}hate cameras{/hint}. You know that. ...But apparently someone recorded %s without asking.")) % _vid_desc, "angry"),
                    (girl, _tl(_("I would NEVER do that voluntarily. But there's one of %s out there...")) % _vid_desc, "angry"),
                    (girl, _tl(_("Absolutely not. I despise being filmed. ...But someone filmed %s. I'm still mad about it.")) % _vid_desc, "angry"),
                ]
            else:
                answers = [
                    (girl, "God no. I {hint}hate cameras{/hint}. The thought of being recorded makes my skin crawl.", "disgusted"),
                    (girl, _("Never. And if anyone ever tried, I'd break their phone."), "disgusted"),
                    (girl, _("Not a chance. I don't even like taking normal selfies."), "disgusted"),
                ]
            _discoveries.append("discovered_trait_camera_hater")
        elif has_camera_lover:
            if has_vids:
                answers = [
                    (girl, _tl(_("Maybe~ There might be one of %s. And honestly, I looked amazing in it.")) % _vid_desc, "smug", "1"),
                    (girl, _tl(_("I might have one of %s. The camera really does love me~")) % _vid_desc, "smug", "1"),
                    (girl, _tl(_("Let's just say there's a video of %s and I'm not ashamed of it at all.")) % _vid_desc, "smug", "1"),
                ]
            else:
                answers = [
                    (girl, "Not yet, but I wouldn't say no to it. I actually {hint}love being on camera{/hint}.", "sly"),
                    (girl, _("I haven't, but honestly? The idea excites me. I'd totally be into it."), "sly"),
                    (girl, _("No, but I've thought about it. I think I'd look amazing on film~"), "sly"),
                ]
            _discoveries.append("discovered_trait_camera_lover")
        else:
            if has_vids:
                answers = [
                    (girl, _tl(_("...There might be one. Of %s. In the heat of the moment, I let it happen.")) % _vid_desc, "embarrassed", "1"),
                    (girl, _tl(_("Someone recorded %s once. I try not to think about it.")) % _vid_desc, "embarrassed", "1"),
                    (girl, _tl(_("Yeah... there's a video of %s. I still don't know how I feel about it.")) % _vid_desc, "embarrassed", "1"),
                ]
            else:
                answers = [
                    (girl, _("No! That's way too risky. What if it got out?"), "looking_right"),
                    (girl, _("Nope. I'm not brave enough for that."), "looking_right"),
                    (girl, _("No way. Some things should stay in the moment."), "looking_right"),
                ]
        # Prepend a threat/reaction line when she has vids and is NOT camera_lover
        if has_vids and not has_camera_lover:
            if has_camera_hater:
                _threat = (girl, renpy.random.choice([
                    _("{size=-6}I'm gonna kill you...{/size}"),

                    _("{size=-6}You recorded that?! You're dead.{/size}"),

                    _("{size=-6}Delete it. Now.{/size}"),

                ]))
            else:
                _threat = (girl, renpy.random.choice([
                    _("{size=-6}Oh no... that exists?{/size}"),

                    _("{size=-6}Wait... you kept that?{/size}"),

                    _("{size=-6}Please tell me nobody else has seen it...{/size}"),

                ]))
            _answer_lines = [_threat, renpy.random.choice(answers)]
            return (question, _answer_lines, _discoveries)
        return (question, [renpy.random.choice(answers)], _discoveries)

    def tod_lewd_raw_sex(girl, other_girl=None):
        """Do you prefer going raw or using a condom?"""
        question = _("Do you prefer going raw or using a condom?")
        _discoveries = []
        raw_count = getattr(girl, "raw_sex_count", 0)
        has_cum_slut = hasattr(girl, "has_trait") and girl.has_trait("cum_slut")
        has_hate_cum = hasattr(girl, "has_trait") and girl.has_trait("hate_cum")
        is_virgin = hasattr(girl, "has_trait") and girl.has_trait("virgin")
        alc = hangout_get_alcohol(girl)

        # Also check BF history
        bf_raw = tod_bf_partner_did(girl, "sex_raw")
        bf_sex = getattr(girl, "bf_history", {}).get("sex", False)

        # Other girl's trait for reaction
        _other_cum_slut = other_girl and hasattr(other_girl, "has_trait") and other_girl.has_trait("cum_slut")
        _other_hate_cum = other_girl and hasattr(other_girl, "has_trait") and other_girl.has_trait("hate_cum")
        _did_raw = raw_count > 0 or bf_raw

        # Lesbian: condom/raw doesn't apply to lesbian sex
        is_lesbian = hasattr(girl, "has_trait") and girl.has_trait("lesbian")
        is_bi = hasattr(girl, "has_trait") and girl.has_trait("bisexual")
        has_gf = hasattr(girl, "get_flag") and girl.get_flag("partner_is_female")

        if is_lesbian:
            has_bf = getattr(girl, "npc_partner_id", None) is not None
            if has_bf and has_gf:
                answers = [
                    (girl, _("I'm with a girl, so... condoms aren't really part of the equation."), "smirk"),
                    (girl, _format_partner_line(girl, _("I'm with my %(pl)s. We don't need that.")), "looking_right"),
                    (girl, _("That's a straight girl question. I wouldn't know."), "smirk"),
                ]
            else:
                answers = [
                    (girl, _("I'm a lesbian, so... that's never been an issue for me."), "looking_right"),
                    (girl, _("Condoms? I'm into girls. That question doesn't really apply to me."), "smirk"),
                    (girl, _("That's not something I've ever had to think about."), "looking_right"),
                ]
            if alc >= 6:
                answers.append((girl, _("I'm a lesbian, so... no comment. But I bet the raw girls are fun at parties."), "smirk", "1"))
            _answer_lines = [renpy.random.choice(answers)]
            _discoveries.append("discovered_trait_lesbian")
            if other_girl:
                _other_is_les = hasattr(other_girl, "has_trait") and other_girl.has_trait("lesbian")
                if _other_is_les:
                    _answer_lines.append((other_girl, renpy.random.choice([
                        _("Same here. Not our department."),
                        _("Right? Lucky us."),
                    ])))
                    # "Same here": her own line states her identity (rule: her line, her trait)
                    _discoveries.append((other_girl, "discovered_trait_lesbian"))
                else:
                    _answer_lines.append((other_girl, renpy.random.choice([
                        _("Fair point. You lucked out of that debate."),
                        _("Must be nice not worrying about that."),
                    ])))
            return (question, _answer_lines, _discoveries)

        # Bi with a girlfriend: acknowledge current relationship
        if is_bi and has_gf:
            has_bf = getattr(girl, "npc_partner_id", None) is not None
            # bf_raw here is an experienced girl's raw past with men (tod_bf_partner_did): what the raw lines say
            if raw_count > 0 or bf_raw:
                answers = [
                    (girl, _("I'm with a girl now, so it's not an issue. But when I was with guys... raw. Definitely raw."), "lipbite", "1"),
                    (girl, _("With my girlfriend, condoms aren't a thing. But with guys? I've done raw. I liked it."), "smirk", "1"),
                ]
                _discoveries.append("discovered_trait_bisexual")
            else:
                answers = [
                    (girl, _("I'm with a girl now, so we don't need condoms. Never really had to deal with that question."), "looking_right"),
                    (girl, _("Condoms aren't part of my life right now. I'm with a girl, so... lucky me, I guess?"), "smirk"),
                ]
            _answer_lines = [renpy.random.choice(answers)]
            if other_girl:
                _answer_lines.append((other_girl, renpy.random.choice([
                    _("Best of both worlds, huh?"),
                    _("That's one way to avoid the debate."),
                ])))
            return (question, _answer_lines, _discoveries)

        _still_virgin = is_virgin and raw_count == 0 and not bf_raw and not bf_sex

        # Harem night: frank, open discussion about preferences with shared boyfriend (a virgin answers below)
        if getattr(store, "_hangout_is_harem_night", False) and girl.is_dating_player() and not _still_virgin:
            if has_cum_slut and raw_count > 0 and not trait_is_discovering(girl, "cum_slut"):
                answers = [
                    (girl, _("Raw. Always. And I want every drop. He knows that~"), "lusty", "1"),
                    (girl, _("Raw, obviously. You know our boyfriend. He knows what I like."), "smirk", "1"),
                ]
            elif has_cum_slut and raw_count > 0:
                # still discovering it: he showed her, she is no old hand
                answers = [
                    (girl, _("Raw. He showed me what I was missing~"), "lusty", "1"),
                    (girl, _("Raw. I didn't know it could feel that good. Now I get it."), "lipbite", "1"),
                ]
            elif has_cum_slut:
                answers = [
                    (girl, _("We haven't gone raw yet... but I really want to. He knows that~"), "lipbite", "1"),
                ]
            elif has_hate_cum:
                answers = [
                    (girl, _("Condom. Always. Even with our boyfriend. He respects that."), "serious"),
                    (girl, _("Protection first. He knows the rules. Right, babe?"), "normal"),
                ]
            elif _did_raw:
                answers = [
                    (girl, _("We've done both. But between us girls... raw is better. Way better."), "lipbite", "1"),
                    (girl, _("I used to always use protection. But with him... things changed."), "sly", "1"),
                ]
            else:
                answers = [
                    (girl, _("Condom for now. But honestly, with the way things are going..."), "looking_left", "1"),
                    (girl, _("We use protection. But I'm curious about trying without..."), "shy", "1"),
                ]
            if has_cum_slut:
                _discoveries.append("discovered_trait_cum_slut")
            elif has_hate_cum:
                _discoveries.append("discovered_trait_hate_cum")
            _answer_lines = [renpy.random.choice(answers)]
            if other_girl:
                _answer_lines.append((other_girl, renpy.random.choice([
                    _("Interesting... I'll keep that in mind~"),
                    _("Good to know. Sharing is caring, right?"),
                ]), "sly"))
            return (question, _answer_lines, _discoveries)

        # Virgin check first
        if _still_virgin:
            has_bf = getattr(girl, "npc_partner_id", None) is not None
            _is_gf_raw = hasattr(girl, "is_dating_player") and girl.is_dating_player()
            if has_bf:
                answers = [
                    (girl, _("Uh... I'm still a virgin, so... no. We're waiting."), "embarrassed", "1"),
                    (girl, _format_partner_line(girl, _("I haven't even had sex yet. My %(pl)s and I are taking it slow.")), "shy", "1"),
                    (girl, _format_partner_line(girl, _("N-no... I haven't done anything like that. Not even with my %(pl)s.")), "embarrassed", "1"),
                ]
                _discoveries.append("discovered_has_partner")
            elif _is_gf_raw:
                answers = [
                    (girl, _("I'm still a virgin... we're taking it slow. But when it happens, I trust him."), "shy", "1"),
                    (girl, _("We haven't gone that far yet. My boyfriend and I are taking our time."), "shy", "1"),
                ]
                _discoveries.append("discovered_has_partner")
            else:
                answers = [
                    (girl, _("Uh... I'm still a virgin, so... no."), "embarrassed", "1"),
                    (girl, _("I haven't even had sex yet. So... that's a no."), "embarrassed", "1"),
                    (girl, _("That question doesn't really apply to me... I'm still a virgin."), "embarrassed", "1"),
                ]
            _discoveries.append("discovered_virgin")
            return (question, [renpy.random.choice(answers)], _discoveries)

        if has_hate_cum:
            if raw_count > 0:
                if alc >= 6:
                    answers = [
                        (girl, _("Condom. Always. I tried raw once and... okay, the warmth was something. But no. Never again."), "uncomfortable", "1"),
                        (girl, _("Condom. I did it raw once and hated almost every second. Almost."), "uncomfortable", "1"),
                    ]
                else:
                    answers = [
                        (girl, _("Condom. Always. I tried raw once and hated every second of it."), "disgusted"),
                        (girl, _("Definitely condom. I did it raw before and it was a mistake I won't repeat."), "disgusted"),
                    ]
            else:
                answers = [
                    (girl, _("Condom. No question. No exceptions. Ever."), "serious"),
                    (girl, _("Always protection. I don't even want to think about going without one."), "serious"),
                ]
            _discoveries.append("discovered_trait_hate_cum")
        elif has_cum_slut:
            if raw_count > 0 and trait_is_discovering(girl, "cum_slut"):
                # still discovering it: no "always" yet
                answers = [
                    (girl, _("Raw. I didn't expect it to feel that different... but it really does."), "lipbite", "1"),
                    (girl, _("Raw. I tried it and... yeah. I don't think I can go back."), "lipbite", "1"),
                ]
            elif raw_count > 0:
                if alc >= 5:
                    answers = [
                        (girl, _("Raw. Always raw. Feeling everything, the warmth, the cum... I'm getting excited just talking about it."), "lusty", "2"),
                        (girl, _("Raw, no question. Condoms are a crime against pleasure. I want to feel all of it."), "lusty", "2"),
                    ]
                else:
                    answers = [
                        (girl, _("Raw. One hundred percent. Feeling everything is the whole point."), "lewd", "1"),
                        (girl, _("Raw, always. Condoms ruin everything. I want to feel it all."), "lewd", "1"),
                    ]
            elif tod_bf_partner_did(girl, "sex_raw", current=True):
                answers = [
                    (girl, _format_partner_line(girl, _("Raw. With my %(pl)s it was always raw. And honestly... I loved every second.")), "lipbite", "1"),
                ]
            elif bf_raw:
                answers = [
                    (girl, _("Raw for sure. My ex and I never used condoms. The feeling is addictive."), "smirk", "1"),
                ]
            else:
                if alc >= 5:
                    answers = [
                        (girl, _("I haven't tried raw yet, but I already know I'd prefer it. Condoms feel like nothing."), "lipbite", "1"),
                        (girl, _("I want to go raw so badly. The idea of feeling someone cum inside me... sorry, the drinks are talking."), "lipbite", "1"),
                    ]
                else:
                    answers = [
                        (girl, _("I haven't tried raw yet, but... I already know I'd prefer it. Condoms feel like nothing."), "looking_right"),
                        (girl, _("Raw, probably. I haven't done it yet, but condoms just seem so... boring."), "looking_right"),
                    ]
            _discoveries.append("discovered_trait_cum_slut")
        else:
            _is_gf_raw2 = hasattr(girl, "is_dating_player") and girl.is_dating_player()
            if raw_count > 0 and _is_gf_raw2:
                if alc >= 6:
                    answers = [
                        (girl, _("With my boyfriend? Yeah, we've done it raw. And it felt amazing."), "lipbite", "1"),
                        (girl, _("Honestly... raw with my boyfriend. I know I shouldn't say that, but condoms feel like nothing."), "lipbite", "1"),
                    ]
                else:
                    answers = [
                        (girl, _("We've gone raw before. It just happened in the moment, and... I prefer it honestly."), "embarrassed", "1"),
                        (girl, _("With my boyfriend, yes. It's hard to go back to condoms after that."), "embarrassed", "1"),
                    ]
            elif raw_count > 0:
                if alc >= 6:
                    answers = [
                        (girl, _("I've gone raw before. And drunk me right now wants to say it felt amazing. Because it did."), "lipbite", "1"),
                        (girl, _("Honestly... raw. I know I shouldn't say that, but after trying it... condoms feel like nothing."), "lipbite", "1"),
                    ]
                else:
                    answers = [
                        (girl, _("I've gone raw before. In the moment it just... happened. I prefer it honestly, but I know I shouldn't."), "embarrassed", "1"),
                        (girl, _("Raw, I think. I've done it before and... yeah. It's hard to go back to condoms after that."), "embarrassed", "1"),
                    ]
            elif bf_raw:
                answers = [
                    (girl, _("Only in a committed relationship. Not something I'd do casually."), "looking_left"),
                ]
                if tod_bf_partner_did(girl, "sex_raw", current=True):
                    answers.append((girl, _format_partner_line(girl, _("With my %(pl)s, yes. But only because we were serious.")), "looking_right"))
            else:
                if alc >= 6:
                    answers = [
                        (girl, _("Condom usually... but tonight I'm wondering what raw would feel like."), "looking_right", "1"),
                        (girl, _("Condom, I guess. But with enough drinks in me, the idea of raw doesn't sound so bad..."), "looking_right", "1"),
                    ]
                else:
                    answers = [
                        (girl, _("Condom, I guess. I haven't been brave enough to try without one."), "shy"),
                        (girl, _("Condom for sure. I'm not ready to take that kind of risk."), "shy"),
                        (girl, _("Protection, always. I'm too careful to go without."), "shy"),
                ]
        # Build answer lines with other girl's reaction
        _answer_lines = [renpy.random.choice(answers)]

        if other_girl:
            if _did_raw:
                # She admitted to doing it raw
                if _other_cum_slut:
                    _answer_lines.append((other_girl, renpy.random.choice([
                        _("See? She gets it. Raw is the only way."),

                        _("That's my girl. Condoms are overrated~"),

                        _("Welcome to the club."),

                    ])))
                    _discoveries.append((other_girl, "discovered_trait_cum_slut"))
                elif _other_hate_cum:
                    _answer_lines.append((other_girl, renpy.random.choice([
                        _("Ugh, that's so risky. I could never."),

                        _("That's dangerous... you should be more careful."),

                        _("I don't know how you can stand that."),

                    ])))
                    _discoveries.append((other_girl, "discovered_trait_hate_cum"))
                else:
                    _answer_lines.append((other_girl, renpy.random.choice([
                        _("Bold. Very bold."),

                        _("Well, that's... honest."),

                        _("No judgment, but... wow."),

                    ])))
            else:
                # She said she hasn't / prefers condoms
                if _other_cum_slut:
                    _answer_lines.append((other_girl, renpy.random.choice([
                        _("You don't know what you're missing..."),

                        _("Trust me, once you try raw, you'll never go back."),

                        _("Condoms? Boring. You need to live a little~"),

                    ])))
                    _discoveries.append((other_girl, "discovered_trait_cum_slut"))
                elif _other_hate_cum:
                    _answer_lines.append((other_girl, renpy.random.choice([
                        _("Finally, someone with sense!"),

                        _("Smart girl. Protection always."),

                        _("At least one of us is responsible."),

                    ])))
                    _discoveries.append((other_girl, "discovered_trait_hate_cum"))
                else:
                    _answer_lines.append((other_girl, renpy.random.choice([
                        _("Fair enough."),

                        _("I respect that."),

                        _("Safe is safe."),

                    ])))

        return (question, _answer_lines, _discoveries)

    def tod_lewd_creampie(girl):
        """Has anyone ever finished inside you?"""
        question = _("Has anyone ever... finished inside you?")
        _discoveries = []
        cream_count = getattr(girl, "CreampieCounts", 0)
        consented = getattr(girl, "ConsentedCreampies", 0)
        has_cum_slut = hasattr(girl, "has_trait") and girl.has_trait("cum_slut")
        has_hate_cum = hasattr(girl, "has_trait") and girl.has_trait("hate_cum")
        bf_creampie = tod_bf_partner_did(girl, "creampie")
        is_virgin = hasattr(girl, "has_trait") and girl.has_trait("virgin")
        bf_sex = getattr(girl, "bf_history", {}).get("sex", False)
        _is_les = hasattr(girl, "has_trait") and girl.has_trait("lesbian")

        # Lesbian with no creampie experience
        if _is_les and cream_count == 0 and not bf_creampie:
            answers = [
                (girl, _("I'm a lesbian. So... no. That's not really something that comes up."), "serious"),
                (girl, _("That question doesn't exactly apply to me. I'm into girls."), "bemused"),
                (girl, _("No. And I never planned on finding out what that's like."), "looking_left"),
            ]
            _discoveries.append("discovered_trait_lesbian")
            return (question, [renpy.random.choice(answers)], _discoveries)

        # Lesbian who HAS been creampied (by player through the system)
        if _is_les and cream_count > 0:
            answers = [
                (girl, _("...Yes. Don't ask me how. I don't want to think about it."), "uncomfortable", "1"),
                (girl, _("That... happened. It wasn't supposed to. Can we move on?"), "looking_down", "1"),
                (girl, _("I'm a lesbian who got... yeah. Life is complicated. Next question."), "embarrassed", "1"),
            ]
            return (question, [renpy.random.choice(answers)], _discoveries)

        # Virgin check first
        if is_virgin and cream_count == 0 and not bf_creampie and not bf_sex:
            has_bf = getattr(girl, "npc_partner_id", None) is not None
            _is_gf_cream = hasattr(girl, "is_dating_player") and girl.is_dating_player()
            if has_bf:
                answers = [
                    (girl, _("I... I'm still a virgin. We haven't gone that far. Not even close."), "embarrassed", "1"),
                    (girl, _format_partner_line(girl, _("No... I haven't even had sex. My %(pl)s and I are waiting.")), "shy", "1"),
                    (girl, _("That's... no. I'm a virgin. So that's definitely a no."), "embarrassed", "1"),
                ]
                _discoveries.append("discovered_has_partner")
            elif _is_gf_cream:
                answers = [
                    (girl, _("I'm still a virgin... my boyfriend and I are taking things slow."), "shy", "1"),
                    (girl, _("We haven't gone that far yet. So no, definitely not."), "embarrassed", "1"),
                ]
                _discoveries.append("discovered_has_partner")
            else:
                answers = [
                    (girl, _("Uh... no. I'm still a virgin. So... definitely not."), "embarrassed", "1"),
                    (girl, _("I haven't even had sex yet. So no, nobody has."), "embarrassed", "1"),
                    (girl, _("No... that question is way beyond where I'm at right now."), "embarrassed", "1"),
                ]
            _discoveries.append("discovered_virgin")
            return (question, [renpy.random.choice(answers)], _discoveries)

        if has_cum_slut:
            if cream_count > 0 and trait_is_discovering(girl, "cum_slut"):
                # still discovering it: she loved it, she is no old hand at it
                answers = [
                    (girl, _("Yes. And I loved every second of it. The warmth, the feeling... everything."), "lusty", "2"),
                    (girl, _("...Yeah. And I liked it way more than I thought I would."), "shy", "2"),
                ]
            elif cream_count > 0:
                answers = [
                    (girl, _("Yes. And I loved every second of it. The warmth, the feeling... everything."), "lusty", "2"),
                    (girl, _("Yes... and honestly, it's my favorite part. I can't get enough of that feeling."), "lusty", "2"),
                ]
                if cream_count > 1:
                    answers.append((girl, _("Mhm~ More than once. I actually asked for it. I know, I know..."), "lusty", "2"))
            elif tod_bf_partner_did(girl, "creampie", current=True):
                answers = [
                    (girl, _format_partner_line(girl, _("My %(pl)s did once. And... I begged %(po)s to. I'm not ashamed to admit it.")), "lipbite", "2"),
                ]
            elif bf_creampie:
                answers = [
                    (girl, _("Yeah, with my ex. It was incredible. I've been craving it ever since."), "smirk", "1"),
                ]
            else:
                answers = [
                    (girl, _("Not yet. But god, I want to feel it so badly."), "lipbite"),
                    (girl, _("No... but I think about it a lot. Like, a lot."), "lipbite"),
                ]
            _discoveries.append("discovered_trait_cum_slut")
        elif has_hate_cum:
            # bf_creampie (an ex's, or an experienced girl's past) makes "Never" false too
            if cream_count > 0 or bf_creampie:
                # the lines with no count are always there: the branch never goes empty
                answers = [
                    (girl, _("...Yes. And it was awful. I felt disgusting afterward."), "disgusted"),
                    (girl, _("It happened and I hated it. I don't want to talk about it."), "disgusted"),
                ]
                if cream_count == 1 and not bf_creampie:   # "Once."
                    answers.append((girl, _("Once. Against my preferences. I never want that again."), "disgusted"))
            else:
                answers = [
                    (girl, _("Absolutely not. That's where I draw the line. Hard no."), "serious"),
                    (girl, _("Never. And never will. The thought makes me physically uncomfortable."), "serious"),
                    (girl, _("No! That's my biggest rule. Not happening."), "serious"),
                ]
            _discoveries.append("discovered_trait_hate_cum")
        else:
            _is_gf_cream2 = hasattr(girl, "is_dating_player") and girl.is_dating_player()
            if cream_count > 0 and consented > 0 and _is_gf_cream2:
                answers = [
                    (girl, _("...My boyfriend did. I let it happen. It was... intense."), "shy", "1"),
                    (girl, _("Yeah. With my boyfriend. In the moment it felt right."), "shy", "1"),
                    (girl, _("It happened with my boyfriend. Scary but... there's something about it."), "shy", "1"),
                ]
            # Count lines only where the count is true; the lines with no count are always there (never empty)
            elif cream_count > 0 and _is_gf_cream2:
                answers = [
                    (girl, _("...Yes. My boyfriend did. It wasn't really planned. Let's leave it at that."), "worried"),
                ]
                if cream_count == 1:   # "It happened once."
                    answers.append((girl, _("It happened once. With my boyfriend. I didn't exactly plan for it."), "worried"))
            elif cream_count > 0 and consented > 0:
                answers = [
                    (girl, _("...Yes. I let it happen. It was... intense."), "shy", "1"),
                    (girl, _("Yeah. In the moment it felt right. Afterward I kind of panicked, though."), "shy", "1"),
                ]
                if cream_count <= 2:   # "Once or twice."
                    answers.append((girl, _("Once or twice. It's scary but... there's something about it."), "shy", "1"))
            elif cream_count > 0:
                answers = [
                    (girl, _("...Yes. But it wasn't really my choice. Let's leave it at that."), "worried"),
                ]
                if cream_count == 1:   # "It happened once."
                    answers.append((girl, _("It happened once. I didn't exactly plan for it."), "worried"))
            elif tod_bf_partner_did(girl, "creampie", current=True):
                answers = [
                    (girl, _format_partner_line(girl, _("My %(pl)s did. When things were serious. I was nervous the whole time.")), "shy", "1"),
                ]
            elif bf_creampie:
                # her ex (or the past of an experienced girl): nobody to call "my %(pl)s"
                answers = [
                    (girl, _("Someone I was dating. It felt right at the time."), "shy", "1"),
                    (girl, _("...Yes. I let it happen. It was... intense."), "shy", "1"),
                ]
            else:
                answers = [
                    (girl, _("No. That's a step I haven't taken."), "normal"),
                    (girl, _("Nope. I'm not ready for that level of trust."), "normal"),
                    (girl, _("No way. That's too much for me."), "normal"),
                ]
        return (question, [renpy.random.choice(answers)], _discoveries)

    def tod_lewd_public_acts(girl):
        """What do you think about doing things in public?"""
        question = _("What do you think about doing... things... in public places?")
        _discoveries = []
        has_public = hasattr(girl, "has_trait") and girl.has_trait("public_fetish")
        has_shy = hasattr(girl, "has_trait") and girl.has_trait("public_shy")
        has_exhib = hasattr(girl, "has_trait") and girl.has_trait("exhibitionist")

        # Check if she actually did something in a public location
        _public_locs = {"pool", "campus", "classroom", "gym", "showers", "hall", "street", "mall", "restaurant_restroom"}
        _pub_act_locs = set()
        for sal in getattr(girl, "Sex_act_locations", []):
            if sal.get("location", "") in _public_locs and sal.get("act", "") not in _TOD_MILD_ACTS:
                _pub_act_locs.add(sal.get("location", ""))
        # Also check recorded videos
        for vid in getattr(store.Player, "recorded_videos", []):
            if vid.get("girl_gid") == girl.gid and vid.get("location", "") in _public_locs:
                _pub_act_locs.add(vid.get("location", ""))

        _pub_loc_names = {
            "pool": _("the pool"), "campus": _("campus"), "classroom": _("the classroom"),
            "gym": _("the gym"), "showers": _("the showers"), "hall": _("the hallway"),
            "street": _("the street"), "mall": _("the mall"),
            "restaurant_restroom": _("the restaurant restroom"),
        }
        _did_public = len(_pub_act_locs) > 0

        if _did_public:
            _ploc = renpy.random.choice(list(_pub_act_locs))
            _ploc_name = _tl(_pub_loc_names.get(_ploc, _ploc))
            if has_public or has_exhib:
                answers = [
                    (girl, _tl(_("I love it. We already did it at %s, remember? I'd do it again in a heartbeat.")) % _ploc_name, "smug", "1"),
                    (girl, _tl(_("Are you kidding? After what happened at %s? I'm addicted to the rush.")) % _ploc_name, "smug", "1"),
                    (girl, _tl(_("I think about %s all the time. The risk makes everything feel ten times more intense.")) % _ploc_name, "smug", "1"),
                ]
            elif has_shy:
                answers = [
                    (girl, _tl(_("I... it already happened at %s. I was terrified the whole time. But... I can't stop thinking about it.")) % _ploc_name, "embarrassed", "2"),
                    (girl, _tl(_("We did something at %s and I almost had a heart attack. I don't know if I could do it again...")) % _ploc_name, "embarrassed", "2"),
                    (girl, _tl(_("After %s I swore I'd never do it again in public. ...But part of me wants to.")) % _ploc_name, "embarrassed", "2"),
                ]
            else:
                answers = [
                    (girl, _tl(_("Well... we already did it at %s once. It was terrifying and exciting at the same time.")) % _ploc_name, "looking_left", "1"),
                    (girl, _tl(_("After what happened at %s? I'd be lying if I said I didn't think about doing it again.")) % _ploc_name, "looking_left", "1"),
                    (girl, _tl(_("I mean... %s already happened. So I guess I'm not as innocent as I thought.")) % _ploc_name, "looking_left", "1"),
                ]
            if has_public:
                _discoveries.append("discovered_trait_public_fetish")
            if has_exhib:
                _discoveries.append("discovered_trait_exhibitionist")
            if has_shy:
                _discoveries.append("discovered_trait_public_shy")
        elif has_public or has_exhib:
            answers = [
                (girl, _("I... actually think about it more than I should. The risk of getting caught is thrilling."), "lusty"),
                (girl, _("Honestly? It turns me on. The adrenaline, the danger... it's a huge rush."), "lusty"),
                (girl, _("I love it. Knowing someone could see you at any moment... it makes everything more intense."), "lusty"),
            ]
            if has_public:
                _discoveries.append("discovered_trait_public_fetish")
            if has_exhib:
                _discoveries.append("discovered_trait_exhibitionist")
        elif has_shy:
            answers = [
                (girl, _("Absolutely not! I would die of embarrassment. I can barely hold hands in public."), "scared"),
                (girl, _("That terrifies me. Even the thought of someone catching me makes me want to disappear."), "scared"),
                (girl, _("No way. Never. I need four walls and a locked door, minimum."), "scared"),
            ]
            _discoveries.append("discovered_trait_public_shy")
        else:
            answers = [
                (girl, _("It's risky... but I won't lie, the idea is kind of exciting."), "looking_right"),
                (girl, _("I've never done it, but sometimes I wonder what it would be like."), "looking_right"),
                (girl, _("Scary, honestly. But in a way that's also kind of... thrilling?"), "looking_right"),
            ]
        return (question, [renpy.random.choice(answers)], _discoveries)

    def tod_lewd_favorite_position(girl):
        """What's your favorite position or act?"""
        question = _("What's your favorite position... or act?")
        _discoveries = []
        fav = getattr(girl, "FavoriteAct", None)
        acts = getattr(girl, "Sex_acts", {})
        orgasms = getattr(girl, "Orgasms", {})

        # Find the act with the most orgasms as real favorite
        real_fav = None
        max_org = 0
        for act, count in orgasms.items():
            if count > max_org:
                max_org = count
                real_fav = act

        # If she has real experience, use it
        if real_fav and max_org > 0:
            _fav_display = {
                "kiss": _tl(_("making out")), "massage": _tl(_("being massaged")),
                "hj": _tl(_("handjobs")), "bj": _tl(_("blowjobs")), "tj": _tl(_("titjobs")),
                "cowgirl": _tl(_("being on top")), "reverse_cowgirl": _tl(_("reverse cowgirl")),
                "doggy": _tl(_("doggy style")), "sex": _tl(_("regular sex")),
                "anal": _tl(_("anal")), "full_nelson": _tl(_("full nelson")),
                "laying_down": _tl(_("laying down")),
                "masturbate": _tl(_("being watched while touching myself")),
            }
            fav_name = _fav_display.get(real_fav, real_fav.replace("_", " "))
            answers = [
                (girl, _tl(_("Definitely %s. That's the one that gets me every time.")) % fav_name, "lipbite", "1"),
                (girl, _tl(_("%s. I don't know why, but it just hits different.")) % fav_name.capitalize(), "lipbite", "1"),
                (girl, _tl(_("If I'm being honest... %s. My body just responds to it.")) % fav_name, "lipbite", "1"),
            ]
            _discoveries.append("discovered_fav_act")
        elif fav:
            _fav_display = {
                "kiss": _tl(_("kissing")), "massage": _tl(_("massages")),
                "hj": _tl(_("using my hands")), "bj": _tl(_("oral")), "tj": _tl(_("titjobs")),
                "cowgirl": _tl(_("being on top")), "reverse_cowgirl": _tl(_("reverse cowgirl")),
                "doggy": _tl(_("being taken from behind")), "sex": _tl(_("regular sex")),
                "anal": _tl(_("anal")), "full_nelson": _tl(_("full nelson")),
                "laying_down": _tl(_("laying down")),
                "masturbate": _tl(_("solo stuff")),
            }
            fav_name = _fav_display.get(fav, fav)
            answers = [
                (girl, _tl(_("I think I'd like %s. At least, that's what I fantasize about.")) % fav_name, "shy", "1"),
                (girl, _tl(_("I haven't done a lot, but the idea of %s really excites me.")) % fav_name, "shy", "1"),
                (girl, _tl(_("Probably %s? I don't have much experience, but that's what I imagine.")) % fav_name, "shy", "1"),
            ]
            _discoveries.append("discovered_fav_act")
        else:
            answers = [
                (girl, _("I... don't really know yet. I haven't had enough experience to say."), "confused"),
                (girl, _("Pass! I'm not answering that. I don't even know myself."), "confused"),
                (girl, _("I genuinely don't know. Ask me again later when I've figured it out."), "confused"),
            ]
        return (question, [renpy.random.choice(answers)], _discoveries)

    def tod_lewd_ever_cheated(girl, other_girl):
        """Have you ever cheated on someone?"""
        question = _("Have you ever cheated on someone?")
        _discoveries = []
        has_cheater = hasattr(girl, "has_trait") and girl.has_trait("cheater")
        has_loyal = hasattr(girl, "has_trait") and girl.has_trait("loyal")
        has_bf = getattr(girl, "npc_partner_id", None) is not None
        is_dating_player = hasattr(girl, "is_dating_player") and girl.is_dating_player()
        is_ex = hasattr(girl, "is_ex_of_player") and girl.is_ex_of_player()
        _ex_hist = getattr(girl, "ex_player_history", None) if is_ex else None

        # Check if she did sexual acts with the player while having a BF
        did_stuff_with_player = False
        acts = getattr(girl, "Sex_acts", {})
        if has_bf and any(acts.get(a, 0) > 0 for a in ("hj", "bj", "tj", "sex", "anal")):
            did_stuff_with_player = True

        # Check if the OTHER girl is the player's GF (this girl is "the other woman")
        other_is_gf = hasattr(other_girl, "is_dating_player") and other_girl.is_dating_player()
        she_did_it_with_taken_player = other_is_gf and any(acts.get(a, 0) > 0 for a in ("hj", "bj", "tj", "sex", "anal"))

        # Harem night: reframe cheating question
        if getattr(store, "_hangout_is_harem_night", False) and is_dating_player:
            answers = [
                (girl, _("Is it even cheating if we all agreed to this? I don't think so."), "smirk"),
                (girl, _("Before this? Never. Now? We have an arrangement, so no~"), "sly"),
                (girl, _("Define cheating. Because sharing a boyfriend doesn't count when everyone's on board."), "happy"),
            ]
            return (question, [renpy.random.choice(answers)], _discoveries)

        # Ex-girlfriend: she was cheated ON (or relationship ended for other reasons)
        if is_ex and not did_stuff_with_player and not she_did_it_with_taken_player:
            _ex_mood = _ex_hist.get("breakup_mood", "angry") if _ex_hist else "angry"
            if _ex_mood == "angry":
                answers = [
                    (girl, "I've never cheated. But I've been cheated {b}on{/b}. And it's the worst feeling in the world.", "angry"),
                    (girl, _("No. But someone cheated on ME. And he's right here. So thanks for bringing it up."), "angry"),
                    (girl, _("Never. I'm loyal. Can't say the same for everyone in this room though."), "angry"),
                ]
            else:
                answers = [
                    (girl, _("No... but I've been on the other side of it. Being cheated on breaks you."), "sad"),
                    (girl, _("I haven't. But I know what it feels like to be the one who gets hurt."), "sad"),
                    (girl, _("Never cheated. But my last relationship ended because of trust issues. That's all I'll say."), "sad"),
                ]
            return (question, [renpy.random.choice(answers)], _discoveries)

        if has_cheater:
            if did_stuff_with_player or she_did_it_with_taken_player:
                answers = [
                    (girl, _("Yeah. I have. And honestly... I don't feel that bad about it."), "smirk"),
                    (girl, _("More than once. Life's too short to hold back, you know?"), "smirk"),
                    (girl, _("Guilty as charged. What can I say, I follow my desires."), "smirk"),
                ]
            else:
                answers = [
                    (girl, _("I mean... not technically. But I've been close. Very close."), "sly"),
                    (girl, _("Define cheating. Because in my head, I've definitely crossed some lines."), "sly"),
                    (girl, _("Not yet. But I won't pretend I'm not tempted sometimes."), "sly"),
                ]
            _discoveries.append("discovered_trait_cheater")
        elif has_loyal:
            if did_stuff_with_player:
                answers = [
                    (girl, _("...Yes. And I feel terrible about it. I never thought I'd be that person."), "sad", "1"),
                    (girl, _("I... did something I'm not proud of. The guilt keeps me up at night."), "sad", "1"),
                    (girl, _("Yes. And it's eating me alive. I don't know how to forgive myself."), "sad", "1"),
                ]
                _discoveries.append("discovered_trait_loyal")
            elif she_did_it_with_taken_player:
                answers = [
                    (girl, _("Well... yes. Lust of the moment is hard to resist."), "looking_left"),
                    (girl, _("I... things got complicated. I know it's wrong. I know."), "uncomfortable", "1"),
                    (girl, _("Something happened that shouldn't have. I'm still processing it."), "uncomfortable", "1"),
                ]
            else:
                answers = [
                    (girl, _("Never. I could never do that to someone. Loyalty means everything to me."), "serious"),
                    (girl, _("No. If I'm with someone, I'm with them. Period."), "serious"),
                    (girl, _("Absolutely not. The thought alone makes me feel sick."), "serious"),
                ]
                _discoveries.append("discovered_trait_loyal")
            # the taken-player branch says the same line a no-trait girl says: nothing revealed
        else:
            if did_stuff_with_player:
                answers = [
                    (girl, _("...Yeah. I have. It just happened. I didn't plan for it."), "embarrassed", "1"),
                    (girl, _("Once. Maybe more. Things got complicated with someone."), "embarrassed", "1"),
                    (girl, _("I'm not proud of it, but... yes. The moment just took over."), "embarrassed", "1"),
                ]
            elif she_did_it_with_taken_player:
                answers = [
                    (girl, _("Well... yes. Lust of the moment is hard to resist."), "looking_left"),
                    (girl, _("Things happened that I probably shouldn't have let happen."), "looking_left"),
                ]
            else:
                answers = [
                    (girl, _("No. I've been tempted, but I've always held back."), "normal"),
                    (girl, _("Nope. I'm not perfect, but I draw the line there."), "normal"),
                    (girl, _("Never. But who knows what the future holds, right?"), "normal"),
                ]
        return (question, [renpy.random.choice(answers)], _discoveries)

    def tod_lewd_hardcore_or_gentle(girl):
        """Do you prefer it rough or gentle?"""
        question = _("Do you like it rough... or gentle?")
        _discoveries = []
        has_hardcore = hasattr(girl, "has_trait") and girl.has_trait("hardcore_sex")
        has_cute = hasattr(girl, "has_trait") and girl.has_trait("cute_sex")
        alc = hangout_get_alcohol(girl)

        if has_hardcore:
            answers = [
                (girl, _("Rough. No question. I want to feel it the next day."), "smirk"),
                (girl, _("Hard and fast. Gentle is nice for a movie, not for the bedroom."), "smirk"),
                (girl, _("I like it intense. Don't hold back. I can take it."), "smirk"),
            ]
            _discoveries.append("discovered_trait_hardcore_sex")
        elif has_cute:
            answers = [
                (girl, _("Gentle. Slow. Eye contact. That's what gets me."), "shy", "1"),
                (girl, _("Soft and intimate. I want to feel loved, not used."), "shy", "1"),
                (girl, _("Gentle, always. There's something beautiful about taking your time."), "shy", "1"),
            ]
            _discoveries.append("discovered_trait_cute_sex")
        # neither rough nor gentle: HER way (femdom, docs/plan_femdom.md 7). Still discovering it she has no answer
        # of her own yet and gives the usual one (trait_line_keys rule)
        elif trait_is_veteran(girl, "femdom"):
            answers = [
                (girl, _("Neither. I like it my way. Rough when I say, slow when I say."), "smug"),
                (girl, _("Whatever I decide that night. The other person just follows along."), "smug"),
                (girl, _("Rough, gentle... who cares? What matters is who's in charge. Me."), "smirk"),
            ]
            _discoveries.append("discovered_trait_femdom")
            print("[FEMDOM] %s answers the rough-or-gentle truth as a femdom" % girl.gid)
        else:
            # Alcohol makes her more honest/bold
            if alc >= 6:
                answers = [
                    (girl, _("Depends on the mood. Sometimes I want soft, sometimes I want to be thrown around."), "lipbite", "1"),
                    (girl, _("Both? I'm versatile. Start gentle, finish rough. Best of both worlds."), "lipbite", "1"),
                    (girl, _("Honestly... I like it when it starts sweet and then gets a little wild."), "lipbite", "1"),
                ]
            else:
                answers = [
                    (girl, _("I... don't know. I think a mix of both?"), "looking_right"),
                    (girl, _("I've never really thought about it. Maybe somewhere in between?"), "looking_right"),
                    (girl, _("That's personal! ...But if I had to choose, probably gentle. With some surprises."), "looking_right"),
                ]
        return (question, [renpy.random.choice(answers)], _discoveries)

    # ── NEW LEWD TRUTHS ─────────────────────────────────

    def tod_lewd_craziest_place(girl):
        """Where's the craziest place you'd do it?"""
        question = "Where's the craziest place you'd do it?"
        _discoveries = []
        has_public = hasattr(girl, "has_trait") and girl.has_trait("public_fetish")
        has_shy = hasattr(girl, "has_trait") and girl.has_trait("public_shy")
        has_exhib = hasattr(girl, "has_trait") and girl.has_trait("exhibitionist")
        alc = hangout_get_alcohol(girl)

        # Check real locations from sex act history, recorded videos, and witness history
        # Rank locations by "exposure level" (most public first)
        _exposure_rank = {
            "campus": 6, "street": 6, "mall": 6, "hall": 5, "classroom": 5,
            "gym": 4, "pool": 4, "showers": 3,
            "gwen_room": 1, "rogue_room": 1, "ntw_room": 1, "room": 0,
        }
        _loc_names = {
            "pool": _("the pool"), "showers": _("the showers"), "campus": _("the campus"),
            "classroom": _("the classroom"), "gym": _("the gym"), "hall": _("the hallway"),
            "street": _("the street"), "mall": _("the mall"),
        }

        _real_locs = {}  # loc -> exposure rank
        for sal in getattr(girl, "Sex_act_locations", []):
            loc = sal.get("location", "")
            if loc and loc != "room" and sal.get("act", "") not in _TOD_MILD_ACTS:
                _real_locs[loc] = _exposure_rank.get(loc, 2)
        for vid in getattr(store.Player, "recorded_videos", []):
            if vid.get("girl_gid") == girl.gid:
                loc = vid.get("location", "")
                if loc and loc != "room":
                    _real_locs[loc] = _exposure_rank.get(loc, 2)

        # Pick the MOST exposed location she's actually done something at
        _best_loc = None
        _best_rank = -1
        for loc, rank in _real_locs.items():
            if loc in _loc_names and rank > _best_rank:
                _best_rank = rank
                _best_loc = loc

        if _best_loc:
            _loc_name = _tl(_loc_names[_best_loc])
            if has_public or has_exhib:
                answers = [
                    (girl, _tl(_("I already did it at %s. And I'd do it again without thinking twice.")) % _loc_name, "smug", "1"),
                    (girl, _tl(_("%s. It already happened there. The rush was unreal.")) % _loc_name.capitalize(), "smug", "1"),
                    (girl, _tl(_("After %s? That's my answer. Nothing else even comes close.")) % _loc_name, "smug", "1"),
                ]
                if has_public:
                    _discoveries.append("discovered_trait_public_fetish")
                if has_exhib:
                    _discoveries.append("discovered_trait_exhibitionist")
            elif has_shy:
                answers = [
                    (girl, _tl(_("I... it happened at %s once. I was dying inside the whole time. But... I think about it a lot.")) % _loc_name, "embarrassed", "2"),
                    (girl, _tl(_("Don't judge me, but... %s. I was so scared, but it was also... exciting?")) % _loc_name, "embarrassed", "2"),
                    (girl, _tl(_("%s. I swore I'd never do anything like that. And then I did. And now I can't stop thinking about it.")) % _loc_name.capitalize(), "embarrassed", "2"),
                ]
                _discoveries.append("discovered_trait_public_shy")
            else:
                answers = [
                    (girl, _tl(_("Well... %s already happened. So I guess that's my craziest place.")) % _loc_name, "looking_left", "1"),
                    (girl, _tl(_("%s. We actually did it there. Still can't believe it.")) % _loc_name.capitalize(), "looking_left", "1"),
                    (girl, _tl(_("I'd say %s. Because it already happened and I survived.")) % _loc_name, "looking_left", "1"),
                ]
        elif has_public or has_exhib:
            answers = [
                (girl, _("The pool at night. With the lights on. Where anyone could walk by."), "lusty"),
                (girl, _("In the classroom. During a break. Door unlocked."), "lusty"),
                (girl, _("Outside, on campus. Under the stars. I don't care who sees."), "lusty"),
            ]
            if has_public:
                _discoveries.append("discovered_trait_public_fetish")
            if has_exhib:
                _discoveries.append("discovered_trait_exhibitionist")
        elif has_shy:
            answers = [
                (girl, _("My room. With the door locked. And the lights off. That's crazy enough for me."), "scared"),
                (girl, _("Nowhere crazy! A bed. A normal bed. Why would anyone want anything else?"), "scared"),
                (girl, _("Maybe... a hotel? That's as wild as I'd go."), "scared"),
            ]
            _discoveries.append("discovered_trait_public_shy")
        else:
            if alc >= 6:
                answers = [
                    (girl, _("The showers. Something about the water and the echo..."), "sly", "1"),
                    (girl, _("In a car. Parked somewhere dark. The cramped space makes it exciting."), "sly", "1"),
                    (girl, _("At the gym. After hours. On the mats. Don't judge me."), "sly", "1"),
                ]
            else:
                answers = [
                    (girl, _("Hmm... maybe the pool? After everyone's gone?"), "looking_right"),
                    (girl, _("Somewhere private but not a bedroom. Like... a balcony at night?"), "looking_right"),
                    (girl, _("I don't know... the showers? At least there's hot water."), "looking_right"),
                ]
        return (question, [renpy.random.choice(answers)], _discoveries)

    def tod_lewd_touch_yourself(girl):
        """Do you touch yourself?"""
        question = _("Be honest... do you touch yourself?")
        _discoveries = []
        mast_count = getattr(girl, "Sex_acts", {}).get("masturbate", 0)
        caught_count = girl.GetActionCount("girl_caught_masturbating") if hasattr(girl, "GetActionCount") else 0
        alone_count = girl.GetActionCount("girl_masturbated_alone") if hasattr(girl, "GetActionCount") else 0
        total_mast = mast_count + caught_count + alone_count
        lust = getattr(girl, "Lust", 0)
        alc = hangout_get_alcohol(girl)
        has_cute = hasattr(girl, "has_trait") and girl.has_trait("cute_sex")
        has_hardcore = hasattr(girl, "has_trait") and girl.has_trait("hardcore_sex")

        if total_mast > 0:
            if has_hardcore:
                if caught_count > 0:
                    answers = [
                        (girl, _("Obviously. Someone walked in on me once. I didn't stop."), "smug"),
                        (girl, _("Yes. Regularly. A girl has needs. Someone even caught me at it once."), "smug"),
                        (girl, _("All the time. What, you don't? I got caught once and didn't even care."), "smug"),
                    ]
                else:
                    answers = [
                        (girl, _("Obviously. Everyone does. I'm not ashamed of it."), "smirk"),
                        (girl, _("Yes. Regularly. A girl has needs."), "smirk"),
                        (girl, _("All the time. What, you don't?"), "smirk"),
                    ]
            elif has_cute:
                if caught_count > 0:
                    answers = [
                        (girl, _("S-sometimes... I got caught once... that was mortifying."), "embarrassed", "2"),
                        (girl, _("I... yes. Someone walked in on me once and I wanted to disappear."), "embarrassed", "2"),
                        (girl, _("Only when I really need to. I got caught once and I still think about it..."), "embarrassed", "2"),
                    ]
                else:
                    answers = [
                        (girl, _("S-sometimes... when I can't sleep... it helps me relax."), "embarrassed", "2"),
                        (girl, _("I... yes. But I feel weird talking about it."), "embarrassed", "2"),
                        (girl, _("Only when I really need to. And I always feel guilty after."), "embarrassed", "2"),
                    ]
            else:
                if caught_count > 0:
                    answers = [
                        (girl, _("Yeah. More than I'd like to admit. Got caught once too... that was awkward."), "embarrassed", "1"),
                        (girl, _("Sometimes. Someone walked in on me once. I wanted to die."), "embarrassed", "1"),
                        (girl, _("I do. I even got caught once. Let's not talk about that part."), "embarrassed", "1"),
                    ]
                else:
                    answers = [
                        (girl, _("Yeah. More than I'd like to admit."), "looking_left", "1"),
                        (girl, _("Sometimes. When the mood hits. It's natural, right?"), "looking_left", "1"),
                        (girl, _("I do. There, I said it. Happy?"), "looking_left", "1"),
                    ]
        elif lust >= 60:
            answers = [
                (girl, _("I... haven't. But lately I've been thinking about it a lot."), "lipbite", "1"),
                (girl, _("Not yet. But honestly, I've been so pent up recently..."), "lipbite", "1"),
            ]
        else:
            if has_cute:
                answers = [
                    (girl, _("N-no! That's so personal! I would never... well... no!"), "embarrassed", "1"),
                    (girl, _("I don't think that's anyone's business! ...No."), "embarrassed", "1"),
                ]
            else:
                answers = [
                    (girl, _("Not really. I just haven't felt the need to."), "normal"),
                    (girl, _("No. Is that weird? I just never got around to it."), "normal"),
                ]
        return (question, [renpy.random.choice(answers)], _discoveries)

    def tod_lewd_biggest_fetish(girl):
        """What's your biggest fetish?"""
        question = _("What's your biggest fetish? And be honest.")
        _discoveries = []
        _ht = lambda t: hasattr(girl, "has_trait") and girl.has_trait(t)
        has_cam = _ht("camera_lover")
        has_pub = _ht("public_fetish")
        has_exhib = _ht("exhibitionist")
        has_voyeur = _ht("voyeur")
        has_hardcore = _ht("hardcore_sex")
        has_femdom = _ht("femdom")
        has_sub = _ht("submissive")
        has_cute = _ht("cute_sex")
        has_cum = _ht("cum_slut")
        has_cheater = _ht("cheater")
        has_loyal = _ht("loyal")
        has_hate_cum = _ht("hate_cum")
        has_cam_hater = _ht("camera_hater")
        has_pub_shy = _ht("public_shy")
        has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()

        _fetish_pool = []
        if has_cam:
            _fetish_pool.append(("camera", [
                (girl, _("Being filmed. I know it sounds crazy, but knowing there's a camera... it drives me wild."), "sly"),
                (girl, _("Cameras. Recording it. Watching it back later. I can't help it."), "sly"),
                (girl, _("Having it on tape. Something about knowing you can replay the moment..."), "sly"),
            ], ["discovered_trait_camera_lover"]))
        if has_pub or has_exhib:
            _pub_disc = []
            if has_pub:
                _pub_disc.append("discovered_trait_public_fetish")
            if has_exhib:
                _pub_disc.append("discovered_trait_exhibitionist")
            _fetish_pool.append(("public", [
                (girl, _("Doing it where someone might see. The risk, the adrenaline... it's addicting."), "lusty"),
                (girl, _("Public places. Knowing someone could catch us at any moment."), "lusty"),
                (girl, _("Being seen. Not on purpose, but... the idea that someone might walk in on us? My heart races just thinking about it."), "lusty"),
            ], _pub_disc))
        if has_voyeur:
            _fetish_pool.append(("voyeur", [
                (girl, _("Watching. I like watching other people... be intimate. Don't look at me like that."), "sly", "1"),
                (girl, _("I'm a watcher. Seeing other people in the act does something to me."), "sly", "1"),
                (girl, _("Honestly? Watching someone else do it. From a distance. Without them knowing. I know that sounds weird..."), "sly", "1"),
            ], ["discovered_trait_voyeur"]))
        # being in charge is femdom (docs/plan_femdom.md 7). Still discovering it (D7), she is only finding out
        if has_femdom:
            if trait_is_veteran(girl, "femdom"):
                _fd_fetish = [
                    (girl, _("Being in charge. Telling someone exactly what to do... and watching them do it."), "smug"),
                    (girl, _("Control. Mine. Someone on their knees, waiting for my next order."), "smug"),
                    (girl, _("Making someone beg. Nicely. Then deciding if they've earned it."), "lipbite", "1"),
                ]
            else:
                _fd_fetish = [
                    (girl, _("I didn't know I had one until recently... I like being the one who decides. A lot."), "embarrassed", "1"),
                    (girl, _("I'm still figuring it out, but... when someone does what I say, it does something to me."), "lipbite", "1"),
                ]
            print("[FEMDOM] %s: femdom fetish answer in the pool (veteran=%s)" % (girl.gid, trait_is_veteran(girl, "femdom")))
            _fetish_pool.append(("femdom", _fd_fetish, ["discovered_trait_femdom"]))
        # being dominated is submissive, not hardcore (docs/plan_femdom.md D3): hardcore keeps the rough answers
        if has_sub:
            _fetish_pool.append(("submissive", [
                (girl, _("Being dominated. Rough hands, firm grip, someone who takes control."), "smirk"),
                (girl, _("Hair pulling, pinning me down... I like it when someone is in charge."), "smirk"),
                (girl, _("I want someone who doesn't ask permission. Who just... takes what they want. Is that messed up?"), "lipbite", "1"),
            ], ["discovered_trait_submissive"]))
        if has_hardcore:
            _fetish_pool.append(("hardcore", [
                (girl, _("Rough. Fast, hard, and loud enough that the neighbors complain."), "smirk"),
                (girl, _("Getting spanked. Hard. I like feeling it the next morning."), "smirk"),
                (girl, _("Being pounded so hard I forget my own name. Is that messed up?"), "lipbite", "1"),
            ], ["discovered_trait_hardcore_sex"]))
        if has_cum:
            # the feeling of it is something she can only talk about once someone has finished inside her
            if getattr(girl, "CreampieCounts", 0) > 0 or tod_bf_partner_did(girl, "creampie") or _ht("experienced"):
                _cum_fetish = [
                    (girl, _("Creampies. Feeling it inside me. I know it's risky, but I can't help it."), "lewd", "1"),
                    (girl, _("Finishing inside. The warmth, the closeness... it's my weakness."), "lewd", "1"),
                    (girl, _("When someone finishes inside... the feeling of being full. I can't explain it. I just love it."), "lusty", "2"),
                ]
            else:
                _cum_fetish = [
                    (girl, _("Someone finishing inside me. I've never... but I think about it way too much."), "lipbite", "1"),
                    (girl, _("I've never let anyone finish inside me. But the idea of it? That's my weakness."), "lipbite", "1"),
                ]
            _fetish_pool.append(("cum", _cum_fetish, ["discovered_trait_cum_slut"]))
        if has_cute:
            _fetish_pool.append(("cute", [
                (girl, _("Eye contact during. It sounds simple, but when someone really looks at you while..."), "shy", "2"),
                (girl, _("Being held after. The intimacy. The gentle stuff that makes you feel wanted."), "shy", "2"),
                (girl, _("Slow, deep, face to face. Feeling their breath on my skin. The emotional connection during it is everything."), "looking_right", "1"),
            ], ["discovered_trait_cute_sex"]))
        if has_cheater:
            _fetish_pool.append(("cheater", [
                (girl, _("The forbidden part. Doing something I'm not supposed to. That's what makes it exciting."), "smirk", "1"),
                (girl, _("Sneaking around. The secrecy, the lies, the thrill of almost getting caught... it's a rush."), "smirk", "1"),
                (girl, _("Knowing it's wrong. That I shouldn't be doing this. That's exactly why it feels so good."), "smirk", "1"),
            ], ["discovered_trait_cheater"]))
        if has_loyal:
            _fetish_pool.append(("loyal", [
                (girl, _("Feeling completely safe with someone. Trusting them with everything. That's when I let go."), "looking_right"),
                (girl, _("Being with someone who's only mine. Knowing they chose me and nobody else. That intimacy..."), "shy", "1"),
                (girl, _("One person. Total devotion. That's what really turns me on. Loyalty is the hottest thing."), "looking_right"),
            ], ["discovered_trait_loyal"]))

        store._tod_fetish_pick = None
        if _fetish_pool:
            _pick = renpy.random.choice(_fetish_pool)
            answers = _pick[1]
            _discoveries.extend(_pick[2])
            store._tod_fetish_pick = _pick[0]
        else:
            # Fallback based on sexual history and stats
            _inbt = getattr(girl, "Inbt", 0)
            _obed = getattr(girl, "Obed", 0)
            _love = getattr(girl, "Love", 0)
            _alc = hangout_get_alcohol(girl)
            # girl.sex_act_history was never written anywhere (always empty): read the acts themselves
            _fet_acts = getattr(girl, "Sex_acts", None) or {}
            _has_sex = girl_had_sex(girl)
            _has_bj = _fet_acts.get("bj", 0) > 0
            _has_hj = _fet_acts.get("hj", 0) > 0

            answers = []
            _is_gf_fetish = hasattr(girl, "is_dating_player") and girl.is_dating_player()

            # GF + no strong fetish trait = answers about feeling safe/connected with BF
            if _is_gf_fetish:
                answers.extend([
                    (girl, _("Feeling completely safe with someone I love. That's when I can really let go."), "looking_right", "1"),
                    (girl, _("When my boyfriend looks at me like I'm the only person in the world. That does something to me."), "shy", "1"),
                    (girl, _("Honestly? The trust. Knowing he won't judge me. That's what makes it exciting."), "looking_right", "1"),
                ])
            # BF + no strong fetish trait = interesting answers about guilt/fantasy
            elif has_bf:
                answers.extend([
                    (girl, _("I... probably shouldn't say this, but... the idea of someone wanting me so badly they don't care that I'm taken."), "looking_left", "1"),
                    (girl, _("Sometimes I think about what it would be like with someone else. Not that I'd ever... I mean... next question."), "looking_left", "1"),
                    (girl, _format_partner_line(girl, _("My %(pl)s is sweet, but... sometimes I wonder what it would feel like to just... let go with someone new.")), "looking_left", "1"),
                ])

            # Based on actual experience with the player
            if _has_sex:
                answers.extend([
                    (girl, _("I didn't think I had one, but... recently some things happened that made me rethink that. I liked it more than I expected."), "bemused", "1"),
                    (girl, _("I think I'm still figuring that out. But some of the things I've done lately... opened my eyes."), "bemused", "1"),
                ])
            elif _has_bj or _has_hj:
                answers.extend([
                    (girl, _("I don't have a lot of experience, but... the things I've tried so far? I liked the feeling of making someone lose control."), "bemused", "1"),
                    (girl, _("Honestly? Seeing the effect I have on someone. The power in that moment. It's... exciting."), "bemused", "1"),
                ])

            # High Inbt = more self-aware sexually
            if _inbt >= 500:
                answers.extend([
                    (girl, _("I think about it a lot, actually. I just haven't named it yet. But when I figure it out, you'll know."), "sly"),
                    (girl, _("I'm still exploring. But I know what I like, and I know I want more of it."), "sly"),
                ])
            # High Obed = submissive leaning
            elif _obed >= 500:
                answers.extend([
                    (girl, _("Being told what to do. Not in a mean way, but... when someone takes charge, I just melt."), "shy", "1"),
                    (girl, _("I think I like... giving up control? Letting someone else decide. It takes the pressure off and feels... right."), "shy", "1"),
                ])
            # High Love = romance leaning
            elif _love >= 500:
                answers.extend([
                    (girl, _("Feeling genuinely desired. Not just physically, but emotionally too. When someone really wants you..."), "looking_right", "1"),
                    (girl, _("When there's real passion behind it. Not just bodies. The way someone looks at you like you're the only person in the world."), "looking_right", "1"),
                ])

            # Drunk honesty
            if _alc >= 5:
                answers.extend([
                    (girl, _("Okay okay, the drinks are talking... I think about being taken by surprise. Like, spontaneously. Out of nowhere. Is that weird?"), "lipbite", "1"),
                    (girl, _("Ugh, fine. I'll say it. I want someone who can't keep their hands off me. Like, physically can't stop touching me. There."), "embarrassed", "2"),
                ])

            # Anti-trait fallbacks
            if has_hate_cum:
                answers.extend([
                    (girl, _("I know what I DON'T like. Cum anywhere near me. Keep that away. But what I do like... clean, controlled, intense."), "serious"),
                ])
            if has_cam_hater:
                answers.extend([
                    (girl, _("Definitely not cameras. God, no. But... privacy? The feeling that it's just us, no one else will ever know? That's hot."), "serious"),
                ])
            if has_pub_shy:
                answers.extend([
                    (girl, _("Definitely nothing public. Just the thought makes me want to die. But somewhere safe, behind closed doors? I can be... surprising."), "serious"),
                ])

            # Ultimate fallback (still interesting)
            if not answers:
                answers = [
                    (girl, _("I think I'm still figuring myself out. Ask me again after a few more drinks and maybe I'll have a real answer."), "confused"),
                    (girl, _("Honestly? I don't know yet. I haven't done enough to really know what drives me crazy. But I want to find out."), "confused"),
                    (girl, _("I'm not the kind of girl who has a fetish she can just name. But... I know there's something in me waiting to come out."), "confused"),
                ]

        return (question, [renpy.random.choice(answers)], _discoveries)

    # ── Propagate knowledge to all present girls ─────────

    def _tod_propagate_knowledge(target_girl, discoveries):
        """After a truth is answered, all other present girls learn from
        what was revealed. Maps discovery keys to girl_learns_* calls.
        A (girl, key) tuple entry belongs to that girl (her own reaction line)."""
        for disc in discoveries:
            _d_girl = disc[0] if isinstance(disc, tuple) else target_girl
            _d_key = disc[1] if isinstance(disc, tuple) else disc
            for other in [g for g in _hangout_girls_list() if g.gid != _d_girl.gid]:
                if _d_key == "discovered_virgin":
                    girl_learns_virgin(other, _d_girl)
                elif _d_key == "discovered_has_partner":
                    girl_learns_has_bf(other, _d_girl)
                elif _d_key == "discovered_trait_lesbian":
                    girl_learns_lesbian(other, _d_girl)
                elif _d_key == "discovered_trait_cheater":
                    girl_learns_cheating(other, _d_girl)
        if discoveries:
            print("[TOD-KNOW] %s revealed %s -> propagated" % (
                target_girl.gid, [(d[0].gid, d[1]) if isinstance(d, tuple) else d for d in discoveries]))

    # ── Knowledge-based callout from other girl ──────────

    def _tod_knowledge_callout(other, target, topic):
        """Generate a reaction from other girl based on what she knows.
        Uses knows_with_player, witness_history, video_seen_history, knows_cheating.
        Returns (speaker, text) or None."""
        if other is None or target is None:
            return None
        _pname = getattr(store.Player, "Name", "him")

        _kw = getattr(other, "knows_with_player", {}).get(target.gid, set())
        _kc = getattr(other, "knows_cheating", {}).get(target.gid, False)
        _witness = getattr(other, "witness_history", [])
        _tw = [w for w in _witness if w.get("girl") == target.gid]
        _vs = getattr(other, "video_seen_history", [])
        _tvs = [v for v in _vs if v.get("girl_gid") == target.gid]
        _loc_names = {
            "pool": _("the pool"), "showers": _("the showers"), "campus": _("campus"),
            "classroom": _("the classroom"), "gym": _("the gym"), "hall": _("the hallway"),
            "mall": _("the mall"),
        }

        if topic == "extreme":
            if _kw & {"sex", "cowgirl", "reverse_cowgirl"}:
                if _tw:
                    _wl = _tl(_loc_names.get(_tw[0].get("location", ""), ""))
                    if _wl:
                        return (other, renpy.random.choice([
                            _tl(_("Funny... because I saw something at %s that says otherwise.")) % _wl,
                            _tl(_("Interesting. I remember %s though...")) % _wl,
                        ]), "smug")
                return (other, renpy.random.choice([
                    _("Hmm. That's not what I heard happened between you two."),

                    _("Really? Because I know you've done more than that."),

                ]), "smug")
            if _tvs:
                return (other, renpy.random.choice([
                    _("I've seen a video that tells a very different story~"),

                    _("That's not what the video showed..."),

                ]), "sly", "1")

        elif topic == "cheating":
            if _kc:
                return (other, renpy.random.choice([
                    _("Don't even try to deny it. I know what happened."),

                    _("Girl, I literally know. You're not fooling anyone."),

                    _("We both know the truth here."),

                ]), "serious")
            if any(w.get("saw_cheating_girl", False) for w in _tw):
                return (other, renpy.random.choice([
                    _tl(_("I saw you with someone while you had a %s. So...")) % (target.partner_label() if hasattr(target, "partner_label") else _tl(_("partner"))),
                    _("Hmm, I remember something that contradicts that answer."),

                ]), "smug")

        elif topic == "recorded":
            if _tvs:
                _vtn = {"hj": _tl(_("a handjob")), "bj": _tl(_("a blowjob")), "tj": _tl(_("a titjob")),
                        "cowgirl": _tl(_("riding someone")), "reverse_cowgirl": _tl(_("from behind"))}
                _vt = _vtn.get(_tvs[0].get("type", ""), _tl(_("something intimate")))
                return (other, renpy.random.choice([
                    _tl(_("I've actually seen a video of you doing %s...")) % _vt,
                    _tl(_("The video of %s? Yeah, I've seen it.")) % _vt,
                ]), "smirk", "1")

        elif topic == "raw":
            if _kw & {"sex", "cowgirl", "reverse_cowgirl"}:
                return (other, renpy.random.choice([
                    _("Based on what I know... I have my doubts about that answer."),

                    _("Hmm. I know more than you think."),

                ]), "sly")

        elif topic == "first_time":
            if _kw & {"sex", "cowgirl", "reverse_cowgirl"}:
                return (other, renpy.random.choice([
                    _("I have a feeling I know exactly who that was..."),

                    _("The way you're looking at him tells me everything."),

                    _tl(_("Wait... was it %s?!")) % _pname,
                ]), "surprised", "1")
            if any(w.get("act", "") in ("sex", "cowgirl", "reverse_cowgirl") for w in _tw):
                return (other, renpy.random.choice([
                    _("I think I might have walked in on that, actually..."),

                    _("Oh... is THAT what was happening when I saw you two?!"),

                ]), "surprised")

        elif topic == "creampie":
            if _kw & {"sex", "cowgirl", "reverse_cowgirl"}:
                return (other, renpy.random.choice([
                    _("Based on what I saw... I don't think protection was part of the plan."),

                    _("Hmm. I have a feeling there's more to that story."),

                ]), "sly")

        elif topic == "virgin":
            _kv = getattr(other, "knows_virgin", {}).get(target.gid, False)
            if _kv:
                return (other, renpy.random.choice([
                    _("I already knew that, actually."),

                    _("Yeah, I could tell. No judgment though."),

                ]), "bemused")

        return None

    # ── Lewd truth: First time ───────────────────────────

    def tod_lewd_first_time(girl, other_girl=None):
        """Who was your first time with?"""
        question = _("Who was your first time with?")
        _discoveries = []
        is_virgin = hasattr(girl, "has_trait") and girl.has_trait("virgin")
        _vtp = getattr(girl, "virginity_taken_by_player", False)
        _bf_sex = getattr(girl, "bf_history", {}).get("sex", False)
        has_bf = getattr(girl, "npc_partner_id", None) is not None
        alc = hangout_get_alcohol(girl)
        _had_sex = girl_had_sex(girl)
        _pname = getattr(store.Player, "Name", "someone")

        # Harem night: virginity taken by player — proud/open about it
        if getattr(store, "_hangout_is_harem_night", False) and _vtp and other_girl:
            _answer_lines = [
                renpy.random.choice([
                    (girl, _tl(_("Our boyfriend, obviously. %s was my first and I wouldn't have it any other way.")) % _pname, "happy"),
                    (girl, _tl(_("It was %s. He was gentle. And amazing. Don't be jealous, girl~")) % _pname, "smirk", "1"),
                    (girl, _tl(_("%s. Best first time a girl could ask for.")) % _pname, "smirk"),
                ])
            ]
            _answer_lines.append((other_girl, renpy.random.choice([
                _("I'm not jealous. I had my own moment with him~"),
                _("He has that effect on all of us, doesn't he?"),
                _("Aw, that's actually sweet."),
            ]), "sly"))
            return (question, _answer_lines, _discoveries)

        if is_virgin:
            _is_gf_ft = hasattr(girl, "is_dating_player") and girl.is_dating_player()
            if has_bf:
                answers = [
                    (girl, _("I... haven't had my first time yet. We're waiting."), "embarrassed", "1"),
                    (girl, _format_partner_line(girl, _("That hasn't happened for me. My %(pl)s and I are taking it slow.")), "shy", "1"),
                ]
                _discoveries.append("discovered_has_partner")
            elif _is_gf_ft:
                answers = [
                    (girl, _("We haven't done it yet. My boyfriend and I are taking it slow."), "shy", "1"),
                    (girl, _("I haven't had my first time yet. But I'm with someone I trust, so... when it happens, it'll be right."), "shy", "1"),
                ]
                _discoveries.append("discovered_has_partner")
            else:
                answers = [
                    (girl, _("I'm still waiting for the right person."), "shy"),
                    (girl, _("Haven't had it yet. I know, I know..."), "shy"),
                    (girl, _("That's... not something I can answer yet."), "shy"),
                ]
            _discoveries.append("discovered_virgin")
            _answer_lines = [renpy.random.choice(answers)]

        elif _vtp:
            if alc >= 5:
                answers = [
                    (girl, _tl(_("...It was %s. He was my first. You happy now?")) % _pname, "shy", "2"),
                    (girl, _("Someone in this room. I think you all know who."), "shy", "2"),
                    (girl, _tl(_("Do I really have to say it out loud? {hint}%s{/hint}. He knows.")) % _pname, "shy", "2"),
                ]
            else:
                answers = [
                    (girl, _("Someone... close. That's all I'm saying."), "embarrassed", "1"),
                    (girl, _("I'd rather not say who. But they know who they are."), "looking_left"),
                    (girl, _("My first time was recent. With someone I trust. That's it."), "embarrassed", "1"),
                ]
            _answer_lines = [renpy.random.choice(answers)]

            if other_girl:
                _okw = getattr(other_girl, "knows_with_player", {}).get(girl.gid, set())
                _otw = [w for w in getattr(other_girl, "witness_history", []) if w.get("girl") == girl.gid]
                _other_knows = bool(_okw & {"sex", "cowgirl", "reverse_cowgirl"}) or any(w.get("act", "") in ("sex", "cowgirl", "reverse_cowgirl") for w in _otw)
                if _other_knows:
                    _answer_lines.append((other_girl, renpy.random.choice([
                        _tl(_("Wait... it was %s, wasn't it?! I KNEW it!")) % _pname,
                        _tl(_("Oh my god... the way you looked at him. It was %s.")) % _pname,
                        _tl(_("I can see it on your face. It was definitely %s.")) % _pname,
                    ]), "surprised"))
                    _answer_lines.append((girl, renpy.random.choice([
                        _("Shut up! That was ONE question!"),

                        _("Can we PLEASE move on?!"),

                        _("I hate this game so much right now..."),

                    ]), "angry", "2"))

        elif _bf_sex:
            if tod_bf_partner_did(girl, "sex", current=True):
                answers = [
                    (girl, _format_partner_line(girl, _("My %(pl)s. When things were serious.")), "looking_down", "1"),
                ]
            else:
                # her ex (or an experienced girl's past): nobody to call "my %(pl)s"
                answers = [
                    (girl, _("Someone I was dating. It felt right at the time."), "looking_left", "1"),
                    (girl, _("My ex. We were both nervous. It was kind of sweet, actually."), "looking_left", "1"),
                ]
            _answer_lines = [renpy.random.choice(answers)]

        else:
            if _had_sex:
                answers = [
                    (girl, _("Someone I was seeing. It wasn't planned, it just happened."), "shy", "1"),
                    (girl, _("Someone I liked. It was awkward but... I remember everything."), "looking_right", "1"),
                ]
            else:
                answers = [
                    (girl, _("I... don't really want to go into details. Can we move on?"), "shy", "1"),
                    (girl, _("It was a while ago. Not the most romantic story."), "shy", "1"),
                ]
            _answer_lines = [renpy.random.choice(answers)]

        return (question, _answer_lines, _discoveries)

    # ── CONDOM BREAK truth ──────────────────────────────────

    def tod_lewd_condom_break(girl):
        """Has a condom ever broken on you during sex?"""
        question = "Has a condom ever broken on you during sex?"
        _discoveries = []
        cream_count = getattr(girl, "CreampieCounts", 0)
        raw_count = getattr(girl, "raw_sex_count", 0)
        has_cum_slut = hasattr(girl, "has_trait") and girl.has_trait("cum_slut")
        has_hate_cum = hasattr(girl, "has_trait") and girl.has_trait("hate_cum")
        has_hardcore = hasattr(girl, "has_trait") and girl.has_trait("hardcore_sex")
        has_cute = hasattr(girl, "has_trait") and girl.has_trait("cute_sex")
        is_virgin = hasattr(girl, "has_trait") and girl.has_trait("virgin")
        _is_les = hasattr(girl, "has_trait") and girl.has_trait("lesbian")
        bf_sex = getattr(girl, "bf_history", {}).get("sex", False)
        alc = hangout_get_alcohol(girl)
        _had_sex = girl_had_sex(girl)

        if _is_les and not _had_sex and not bf_sex:
            answers = [
                (girl, _("I'm a lesbian. Condoms aren't exactly part of my world."), "bemused"),
                (girl, _("That doesn't really apply to me. I'm into girls, remember?"), "smirk"),
            ]
            _discoveries.append("discovered_trait_lesbian")
            return (question, [renpy.random.choice(answers)], _discoveries)

        if _is_les and _had_sex:
            if cream_count > 0:
                answers = [
                    (girl, _("...Something like that happened. With a guy. Don't ask how I ended up there."), "uncomfortable", "1"),
                    (girl, _("I'm a lesbian who somehow ended up in that situation. And yes, it broke. My life is a mess."), "grimace", "1"),
                ]
                _discoveries.append("discovered_trait_lesbian")
            else:
                answers = [
                    (girl, _("I had an experience with a guy. The condom held, at least. Small mercies."), "looking_left"),
                    (girl, _("That happened once. With a man. I don't want to talk about how or why."), "serious"),
                ]
            return (question, [renpy.random.choice(answers)], _discoveries)

        if is_virgin and not _had_sex and not bf_sex:
            answers = [
                (girl, _("I'm a virgin. I've never even used one."), "embarrassed", "1"),
                (girl, _("I haven't had sex yet, so... definitely no."), "shy", "1"),
            ]
            _discoveries.append("discovered_virgin")
            return (question, [renpy.random.choice(answers)], _discoveries)

        if cream_count > 0 and _had_sex:
            if has_cum_slut:
                answers = [
                    (girl, _("Yeah... it broke once. And honestly? Best accident of my life. I felt everything."), "lusty", "1"),
                    (girl, _("It happened. The condom just ripped. And I didn't want him to stop. Is that bad?"), "lipbite", "1"),
                    (girl, _("Once. And I was secretly hoping it would happen again the whole time after."), "lewd", "1"),
                ]
                _discoveries.append("discovered_trait_cum_slut")
            elif has_hate_cum:
                answers = [
                    (girl, _("YES. And it was the worst experience of my life. I could feel the difference immediately."), "angry"),
                    (girl, _("It broke once. I was FURIOUS. I spent the next week in complete anxiety."), "angry", "1"),
                    (girl, _("Don't even remind me. It happened and I still have nightmares about it."), "disgusted"),
                ]
                _discoveries.append("discovered_trait_hate_cum")
            elif has_hardcore:
                answers = [
                    (girl, _("Yeah, it happened. I barely noticed until after. Shit happens, right?"), "smirk"),
                    (girl, _("Once. He panicked more than I did. I told him to just keep going."), "smug"),
                ]
            elif has_cute:
                answers = [
                    (girl, _("It happened once... I was so scared. I didn't know what to do."), "scared", "1"),
                    (girl, _("Yes. And I cried afterward. Not from pain, but because he didn't tell me right away."), "sad", "1"),
                ]
            else:
                _is_gf_cb = hasattr(girl, "is_dating_player") and girl.is_dating_player()
                if _is_gf_cb:
                    if alc >= 5:
                        answers = [
                            (girl, _("Yeah... with my boyfriend. My heart stopped. But the excuse he gave me was hilarious."), "laugh", "1"),
                            (girl, _("It happened with my boyfriend. And the worst part? Part of me didn't even care."), "embarrassed", "1"),
                        ]
                    else:
                        answers = [
                            (girl, _("Yeah... it happened with my boyfriend. That was a stressful week for both of us."), "worried"),
                            (girl, _("It happened once. With my boyfriend. We both panicked."), "worried"),
                        ]
                elif alc >= 5:
                    answers = [
                        (girl, _("Yeah... once. My heart stopped. But honestly, the excuse he gave me was hilarious."), "laugh", "1"),
                        (girl, _("It happened. And the worst part? Part of me didn't even care in the moment."), "embarrassed", "1"),
                    ]
                else:
                    answers = [
                        (girl, _("Yeah... once. My heart stopped when I realized. That was a stressful week."), "worried"),
                        (girl, _("It happened. I didn't notice until it was too late. The excuse I got was questionable."), "perplexed"),
                        (girl, _("Once. And the excuse he gave me... let's just say I didn't fully believe him."), "serious"),
                    ]
        elif _had_sex or bf_sex:
            if raw_count > 0:
                if has_cum_slut:
                    answers = [
                        (girl, _("I don't really use condoms, so... no. I prefer to feel everything."), "sly", "1"),
                        (girl, _("Hard to break something you never use~"), "smug"),
                    ]
                    _discoveries.append("discovered_trait_cum_slut")
                else:
                    answers = [
                        (girl, _("I've gone without a few times, but when I used one, it never broke. Lucky, I guess."), "looking_left", "1"),
                        (girl, _("No. But I've taken risks that were probably worse than a broken condom."), "uncomfortable", "1"),
                    ]
            else:
                answers = [
                    (girl, _("No, thankfully. That's one of my biggest fears though."), "worried"),
                    (girl, _("Never. And I always check afterward. I'm paranoid about it."), "serious"),
                    (girl, _("No. I'd probably have a panic attack if it happened."), "scared"),
                ]
        else:
            if alc >= 5:
                answers = [
                    (girl, _("No... but the idea terrifies me. And also kind of excites me? No, just terrifies me."), "confused", "1"),
                    (girl, _("Never happened. But after a few more drinks, ask me if I'd even care~"), "sly", "1"),
                ]
            else:
                answers = [
                    (girl, _("No. And I don't want to find out what that's like."), "serious"),
                    (girl, _("Never. That's literally my worst nightmare."), "scared"),
                ]

        return (question, [renpy.random.choice(answers)], _discoveries)

    # ── FINANCIAL COERCION truth ─────────────────────────────

    def tod_lewd_financial(girl):
        """Would you ever do something sexual for money?"""
        question = _("Would you ever do something sexual for money?")
        _discoveries = []
        _fin_times = getattr(girl, "_financial_times", 0)
        _fin_att = getattr(girl, "_financial_attitude", 0)
        has_cum_slut = hasattr(girl, "has_trait") and girl.has_trait("cum_slut")
        has_hate_cum = hasattr(girl, "has_trait") and girl.has_trait("hate_cum")
        has_hardcore = hasattr(girl, "has_trait") and girl.has_trait("hardcore_sex")
        has_cute = hasattr(girl, "has_trait") and girl.has_trait("cute_sex")
        is_virgin = hasattr(girl, "has_trait") and girl.has_trait("virgin")
        _is_les = hasattr(girl, "has_trait") and girl.has_trait("lesbian")
        has_bf = getattr(girl, "npc_partner_id", None) is not None
        alc = hangout_get_alcohol(girl)
        _is_poor = hasattr(girl, "has_trait") and girl.has_trait("poor")
        _is_rich = hasattr(girl, "has_trait") and girl.has_trait("rich")

        if _fin_att >= 3:
            if has_cum_slut:
                answers = [
                    (girl, _("I already do. And honestly? I'd do it for free. The money is just a bonus."), "smug", "1"),
                    (girl, _("Please. I get paid AND I get what I want. It's a win-win."), "sly"),
                ]
                _discoveries.append("discovered_trait_cum_slut")
            elif _is_les:
                answers = [
                    (girl, _("...I have. With a guy. For money. My life has taken some unexpected turns."), "uncomfortable", "1"),
                    (girl, _("It happened. Multiple times. The money made it easier to justify it."), "looking_down"),
                ]
            else:
                answers = [
                    (girl, _("Hypothetically? Sure. Realistically? I already have. It's just business at this point."), "smirk"),
                    (girl, _("I've done it. More than once. At some point you stop overthinking it."), "neutral"),
                    (girl, _("Yeah. I have. And the money is good enough that I stopped feeling weird about it."), "looking_left"),
                ]
        elif _fin_att == 2:
            if _is_poor:
                answers = [
                    (girl, _("When rent is due and you're broke? Yeah. You do what you have to do."), "serious"),
                    (girl, _("I've done things I never thought I would. Money changes your perspective fast."), "looking_down"),
                ]
                _discoveries.append("discovered_trait_poor")
            else:
                answers = [
                    (girl, _("I... have. It's not something I'm proud of, but it happened. And I'd do it again."), "looking_left", "1"),
                    (girl, _("Let's just say I've learned that everyone has a price. Including me."), "smirk"),
                ]
        elif _fin_att == 1:
            answers = [
                (girl, _("I thought I'd never... but then someone offered enough that I couldn't say no."), "looking_down", "1"),
                (girl, _("It happened once. I felt awful afterward. But the money helped. A lot."), "uncomfortable", "1"),
                (girl, _("I said yes once. I'm still not sure how I feel about it."), "confused"),
            ]
        elif _fin_times > 0:
            answers = [
                (girl, _("...Once. I was desperate. I hated every second of it. And myself after."), "sad"),
                (girl, _("Someone offered me money and I... I took it. I still feel dirty thinking about it."), "looking_down", "1"),
            ]
        elif _is_poor:
            if alc >= 5:
                answers = [
                    (girl, _("I've thought about it. When you're broke, those thoughts creep in. But I haven't. Yet."), "worried"),
                    (girl, _("Honestly? If someone offered enough right now... I don't know. Being poor sucks."), "looking_down"),
                ]
            else:
                answers = [
                    (girl, _("I'd like to say never, but when you can barely afford food, you think about things differently."), "serious"),
                    (girl, _("No. But I understand why someone would. Money problems make you consider things."), "looking_left"),
                ]
            _discoveries.append("discovered_trait_poor")
        elif _is_rich:
            answers = [
                (girl, _("Absolutely not. I don't need anyone's money. That's beneath me."), "disgusted"),
                (girl, _("Never. I have everything I need. Why would I sell myself?"), "serious"),
                (girl, _("No. And honestly, I judge people who do. Sorry, but it's true."), "smug"),
            ]
            _discoveries.append("discovered_trait_rich")
        elif is_virgin:
            answers = [
                (girl, _("I haven't even had sex yet. So no. Definitely not for money."), "embarrassed", "1"),
                (girl, _("No! I'm saving myself for someone special, not for a paycheck!"), "angry"),
            ]
            _discoveries.append("discovered_virgin")
        elif _is_les:
            if alc >= 5:
                answers = [
                    (girl, _("With a woman, maybe. For money? That cheapens everything. ...With a guy? Not enough money in the world."), "smirk"),
                    (girl, _("I'm a lesbian. Most offers would come from men. So no. Unless it's an insane amount and we never speak of it again."), "sly", "1"),
                ]
            else:
                answers = [
                    (girl, _("With a woman, maybe if the chemistry was right. For money? That cheapens everything."), "serious"),
                    (girl, _("I'm a lesbian. Most of the offers I'd get would be from men. So no."), "neutral"),
                ]
            _discoveries.append("discovered_trait_lesbian")
        elif has_cum_slut:
            if alc >= 5:
                answers = [
                    (girl, _("I'd do it for free, so getting paid would just be a perk~"), "lewd", "1"),
                    (girl, _("Money AND sex? Where do I sign up?"), "lusty"),
                ]
            else:
                answers = [
                    (girl, _("I mean... I love it enough that I don't need the incentive. But sure, why not?"), "sly", "1"),
                    (girl, _("I wouldn't need the money to say yes. But it wouldn't hurt."), "smirk"),
                ]
            _discoveries.append("discovered_trait_cum_slut")
        elif has_hate_cum:
            answers = [
                (girl, _("No. Not for any amount. Some things aren't worth any price."), "serious"),
                (girl, _("Never. And anyone who offers is getting slapped."), "angry"),
            ]
        # setting the terms is femdom (docs/plan_femdom.md 7); still discovering it, the usual answers
        elif trait_is_veteran(girl, "femdom"):
            answers = [
                (girl, _("Maybe. But I'd set the rules, the price and the pace. Money doesn't buy control over me."), "smug"),
                (girl, _("Whoever pays still does what I say. That's the only deal I'd take."), "smirk"),
            ]
            _discoveries.append("discovered_trait_femdom")
            print("[FEMDOM] %s answers the money truth as a femdom" % girl.gid)
        elif has_hardcore:
            if alc >= 5:
                answers = [
                    (girl, _("Depends on how much. I'm not cheap, but I'm open to negotiation."), "smirk"),
                    (girl, _("For the right amount? I'd consider it. Sex is sex. Money is money."), "sly"),
                ]
            else:
                answers = [
                    (girl, _("I won't pretend I haven't thought about it. But thinking and doing are different things."), "looking_left"),
                    (girl, _("Depends. How much are we talking?"), "smirk"),
                ]
        elif has_cute:
            answers = [
                (girl, _("No! That's horrible! My body isn't for sale!"), "angry"),
                (girl, _("Never. The thought alone makes me feel sick. Sex should be about love."), "disgusted"),
                (girl, _("Absolutely not. That would ruin everything beautiful about intimacy."), "sad"),
            ]
        elif hasattr(girl, "is_dating_player") and girl.is_dating_player():
            if alc >= 5:
                answers = [
                    (girl, _("No! I already have a boyfriend. What more do I need?"), "happy"),
                    (girl, _("Pff, why would I? I already have everything I want."), "smirk"),
                ]
            else:
                answers = [
                    (girl, _("I have a boyfriend. So absolutely not."), "serious"),
                    (girl, _("No. I'm in a relationship. That's not even a question for me."), "neutral"),
                ]
        elif has_bf:
            if alc >= 5:
                answers = [
                    (girl, _format_partner_line(girl, _("I have a %(pl)s. So obviously no. ...Unless %(pp)s never found out and it was a LOT of money.")), "embarrassed", "1"),
                    (girl, _format_partner_line(girl, _("No! I'm with my %(pl)s! ...How much are we talking about? No! Forget I said that.")), "surprised", "2"),
                ]
            else:
                answers = [
                    (girl, _format_partner_line(girl, _("I have a %(pl)s. So absolutely not.")), "serious"),
                    (girl, _("No. I'm in a relationship. That's not even a question for me."), "neutral"),
                ]
        else:
            if alc >= 5:
                answers = [
                    (girl, _("I'd like to say no, but... everyone has a number, right? What's yours?"), "sly", "1"),
                    (girl, _("Sober me says no. Drunk me says... how much?"), "laugh", "1"),
                    (girl, _("Probably not. But I won't pretend the thought has never crossed my mind."), "looking_left"),
                ]
            else:
                answers = [
                    (girl, _("No. I don't think I could live with myself afterward."), "serious"),
                    (girl, _("That's a hard no. Some things should never be transactional."), "neutral"),
                    (girl, _("No way. I'm not judging anyone who would, but it's not for me."), "looking_right"),
                ]

        return (question, [renpy.random.choice(answers)], _discoveries)

    # ── THREESOME truth ─────────────────────────────────

    def tod_lewd_threesome(girl, other_girl=None):
        """Ever done a threesome?"""
        question = "Ever done a threesome?"
        _discoveries = []

        _participated_gids = []
        _watched_gids = []
        for _g in store.ALL_GIRLS:
            if _g.gid == girl.gid:
                continue
            if girl.get_history_with(_g.gid, "threesome") > 0:
                _participated_gids.append(_g.gid)
            if girl.get_history_with(_g.gid, "threesome_watched") > 0:
                _watched_gids.append(_g.gid)

        _has_participated = len(_participated_gids) > 0
        _has_watched = len(_watched_gids) > 0

        has_cum_slut = hasattr(girl, "has_trait") and girl.has_trait("cum_slut")
        has_exhib = hasattr(girl, "has_trait") and girl.has_trait("exhibitionist")
        has_voyeur = hasattr(girl, "has_trait") and girl.has_trait("voyeur")
        has_shy = hasattr(girl, "has_trait") and girl.has_trait("public_shy")
        _is_les = hasattr(girl, "has_trait") and girl.has_trait("lesbian")
        has_hardcore = hasattr(girl, "has_trait") and girl.has_trait("hardcore_sex")
        has_cute = hasattr(girl, "has_trait") and girl.has_trait("cute_sex")
        is_virgin = hasattr(girl, "has_trait") and girl.has_trait("virgin")
        alc = hangout_get_alcohol(girl)

        _other_involved = other_girl is not None and other_girl.gid in _participated_gids
        _other_watched_by_me = other_girl is not None and other_girl.gid in _watched_gids

        # --- Harem night: open and playful ---
        if getattr(store, "_hangout_is_harem_night", False) and other_girl is not None:
            _answer_lines = []
            if _has_participated and _other_involved:
                answers = [
                    (girl, _tl(_("With %s and our boyfriend? Obviously~ Best night ever.")) % other_girl.Name, "smirk", "1"),
                    (girl, _tl(_("Ask %s. She was there. And she definitely enjoyed it.")) % other_girl.Name, "sly", "1"),
                ]
                _answer_lines.append(renpy.random.choice(answers))
                _answer_lines.append((other_girl, renpy.random.choice([
                    _("Guilty as charged~ And I'd do it again."),
                    _("The best things in life are shared, right?"),
                ]), "smirk"))
            elif _has_participated:
                answers = [
                    (girl, _("Yes, actually. But not with the girl who's sitting right here... yet~"), "sly", "1"),
                    (girl, _("I have. But I wouldn't mind a repeat with present company~"), "smirk", "1"),
                ]
                _answer_lines.append(renpy.random.choice(answers))
            else:
                answers = [
                    (girl, _tl(_("Not yet. But with %s right here... who knows how tonight ends~")) % other_girl.Name, "sly", "1"),
                    (girl, _("No, but I have a feeling that's going to change pretty soon~"), "lipbite", "1"),
                ]
                _answer_lines.append(renpy.random.choice(answers))
                _answer_lines.append((other_girl, renpy.random.choice([
                    _("Is that a dare? Because I might accept~"),
                    _("Careful what you wish for, girl~"),
                ]), "sly"))
            return (question, _answer_lines, _discoveries)

        # --- Participated + other girl was there → coy ---
        if _has_participated and _other_involved:
            _answer_lines = []
            if has_exhib or has_cum_slut:
                answers = [
                    (girl, _("Hehe... you want me to talk about that night? With you right here?"), "smug", "1"),
                    (girl, _("*smirks* I think someone in this room already knows the answer."), "smug", "1"),
                ]
            elif has_shy or has_cute:
                answers = [
                    (girl, _("I... *glances sideways* ...Some things are better left unsaid right now."), "embarrassed", "2"),
                    (girl, _("Can we please skip this one? Please?"), "embarrassed", "2"),
                ]
            elif _is_les:
                answers = [
                    (girl, _("It happened. With a man, of all things. And someone here was there too."), "uncomfortable"),
                    (girl, _("*looks away* ...Ask me when she's not in the room."), "uncomfortable"),
                ]
            else:
                answers = [
                    (girl, _tl(_("*looks at %s* ...You really want me to answer this right now?")) % other_girl.Name, "sly", "1"),
                    (girl, _("Hehe... let's just say some memories are shared."), "sly", "1"),
                ]
            _answer_lines.append(renpy.random.choice(answers))

            if hasattr(other_girl, "has_trait") and other_girl.has_trait("exhibitionist"):
                _answer_lines.append((other_girl, renpy.random.choice([
                    _("Oh come on, just say it. It was fun~"),
                    _("Why so shy? I remember you weren't shy that night."),
                ]), "smug"))
            elif hasattr(other_girl, "has_trait") and other_girl.has_trait("public_shy"):
                _answer_lines.append((other_girl, renpy.random.choice([
                    _("Please don't... just... don't."),
                    _("Can we change the subject?! NOW?!"),
                ]), "scared"))
            else:
                _answer_lines.append((other_girl, renpy.random.choice([
                    _("...I'm just going to pretend I didn't hear that."),
                    _("Wow. Okay. We're doing this."),
                ]), "surprised"))

            _discoveries.append("discovered_threesome")
            return (question, _answer_lines, _discoveries)

        # --- Participated, other not involved ---
        if _has_participated:
            if has_cum_slut:
                answers = [
                    (girl, _("Yes. And honestly? One of the best experiences of my life."), "smug", "1"),
                    (girl, _("Yeah... the more, the merrier. I don't see the problem."), "smug", "1"),
                ]
            elif has_exhib:
                answers = [
                    (girl, _("Yes. Being desired by two people at once? Nothing compares."), "lusty"),
                    (girl, _("Mhm. The attention, the energy... it was incredible."), "lusty"),
                ]
                _discoveries.append("discovered_trait_exhibitionist")
            # femdom (docs/plan_femdom.md 7): only what she WANTS next time (who ran that night is not tracked)
            elif trait_is_veteran(girl, "femdom"):
                answers = [
                    (girl, _("Once. Next time I'm the one deciding who does what."), "smug"),
                    (girl, _("Yes. And if there's a next time, I'm running it."), "smug"),
                ]
                _discoveries.append("discovered_trait_femdom")
                print("[FEMDOM] %s answers the threesome truth as a femdom (did one)" % girl.gid)
            elif has_hardcore:
                answers = [
                    (girl, _("Yeah. It was intense. Wouldn't say no to another one."), "smirk"),
                    (girl, _("Once. It was wild. I'd do it again with the right people."), "smirk"),
                ]
                _discoveries.append("discovered_trait_hardcore_sex")
            elif has_cute:
                answers = [
                    (girl, _("It... happened once. I was so nervous the whole time."), "embarrassed", "1"),
                    (girl, _("Yes... but it was a lot. Emotionally and physically."), "embarrassed", "1"),
                ]
            elif _is_les:
                if alc >= 5:
                    answers = [
                        (girl, _("With a guy, no less. Don't ask how that happened. Alcohol."), "uncomfortable"),
                        (girl, _("...A man was involved. I'm still questioning my life choices."), "uncomfortable"),
                    ]
                else:
                    answers = [
                        (girl, _("Something like that happened. It was... complicated."), "looking_left"),
                        (girl, _("Let's say I ended up in a situation I didn't expect. With people I didn't expect."), "looking_left"),
                    ]
            else:
                if alc >= 5:
                    answers = [
                        (girl, _("Yeah... it happened. And I think about it more often than I should."), "sly", "1"),
                        (girl, _("Once. Not gonna lie, it was really hot."), "sly", "1"),
                    ]
                else:
                    answers = [
                        (girl, _("Something like that happened once. That's all I'll say."), "shy"),
                        (girl, _("...Yes. But I'd rather not go into details."), "shy"),
                    ]

            _discoveries.append("discovered_threesome")
            return (question, [renpy.random.choice(answers)], _discoveries)

        # --- Watched + other was the one she watched → coy ---
        if _has_watched and _other_watched_by_me:
            _answer_lines = []
            if has_voyeur:
                answers = [
                    (girl, _("I didn't do anything myself, but I saw things. With someone in this room."), "sly", "1"),
                    (girl, _tl(_("*glances at %s* I was just watching. But I saw everything.")) % other_girl.Name, "sly", "1"),
                ]
                _discoveries.append("discovered_trait_voyeur")
            elif has_shy:
                answers = [
                    (girl, _("I was there when... something happened. I couldn't look away."), "embarrassed", "2"),
                    (girl, _("I... saw it happen. With... *avoids eye contact* ...someone here."), "embarrassed", "2"),
                ]
            else:
                answers = [
                    (girl, _("I didn't participate, but I had a front-row seat. *meaningful look*"), "smirk"),
                    (girl, _("Let's say I watched someone. And she knows who she is."), "smirk"),
                ]
            _answer_lines.append(renpy.random.choice(answers))

            _answer_lines.append((other_girl, renpy.random.choice([
                _("Wait... you WATCHED?! The whole time?!"),
                _("I knew you were there! I KNEW it!"),
                _("Oh my god... I thought you left the room!"),
            ]), "surprised", "2"))

            _discoveries.append("discovered_threesome_watched")
            return (question, _answer_lines, _discoveries)

        # --- Watched, other not involved ---
        if _has_watched:
            if has_voyeur:
                answers = [
                    (girl, _("I watched one. And... I liked it. A lot."), "sly", "1"),
                    (girl, _("Not directly, but I saw two people going at it. Couldn't stop watching."), "sly", "1"),
                ]
                _discoveries.append("discovered_trait_voyeur")
            elif has_shy:
                answers = [
                    (girl, _("I accidentally walked in on... something. I was frozen."), "embarrassed", "1"),
                    (girl, _("I saw it happen once. I was mortified. And also... confused."), "embarrassed", "1"),
                ]
            elif has_exhib:
                answers = [
                    (girl, _("I watched. Next time, I'm not just going to watch."), "smug"),
                    (girl, _("I was just the audience last time. I'm ready to be on stage."), "smug"),
                ]
            else:
                if alc >= 5:
                    answers = [
                        (girl, _("I watched. And honestly? Part of me wanted to join."), "smirk"),
                        (girl, _("I didn't join, but I saw everything. It was... educational."), "smirk"),
                    ]
                else:
                    answers = [
                        (girl, _("I was present for one. Just watching. That's all."), "looking_left"),
                        (girl, _("I saw it happen. I didn't participate."), "looking_left"),
                    ]

            _discoveries.append("discovered_threesome_watched")
            return (question, [renpy.random.choice(answers)], _discoveries)

        # --- No experience ---
        if is_virgin:
            answers = [
                (girl, _("I haven't even had sex yet. A threesome is way beyond my reality."), "confused"),
                (girl, _("I'm still figuring out the basics. Three is... a big number."), "confused"),
            ]
            _discoveries.append("discovered_virgin")
        elif _is_les:
            answers = [
                (girl, _("I'm into girls. So the 'three' part would have to be very specific."), "serious"),
                (girl, _("Not yet. And it would have to be with the right women."), "serious"),
            ]
            _discoveries.append("discovered_trait_lesbian")
        elif has_exhib or has_cum_slut:
            if alc >= 5:
                answers = [
                    (girl, _("No, but I'm VERY open to trying. Tonight? ...Half kidding."), "lusty", "1"),
                    (girl, _("Not yet, but it's on my list. Who's volunteering?"), "lusty", "1"),
                ]
            else:
                answers = [
                    (girl, _("No, but I'd be lying if I said I haven't thought about it."), "lipbite"),
                    (girl, _("Not yet. But the idea doesn't scare me. It excites me, actually."), "lipbite"),
                ]
        elif has_cute:
            answers = [
                (girl, _("No! I can barely handle one person emotionally, let alone two!"), "embarrassed"),
                (girl, _("That's way too intense for me. I want intimacy, not a performance."), "embarrassed"),
            ]
        elif trait_is_veteran(girl, "femdom"):
            answers = [
                (girl, _("Not yet. But if it happens, I'm the one giving the orders. To both of them."), "smirk"),
                (girl, _("No. Two people doing exactly what I say, though? I've thought about it."), "smirk"),
            ]
            print("[FEMDOM] %s answers the threesome truth as a femdom (never did one)" % girl.gid)
        elif has_hardcore:
            answers = [
                (girl, _("Not yet. But I'd try it with the right people."), "smirk"),
                (girl, _("No, but I've thought about it. It sounds like a challenge."), "smirk"),
            ]
        elif has_shy:
            answers = [
                (girl, _("N-no! The idea of someone watching me? I'd die."), "scared", "1"),
                (girl, _("Absolutely not. I can barely do stuff with one person without feeling self-conscious."), "scared", "1"),
            ]
        else:
            if alc >= 5:
                answers = [
                    (girl, _("No, but ask me again after two more drinks."), "sly"),
                    (girl, _("Not yet. But I'm curious. There, I said it."), "sly"),
                ]
            else:
                answers = [
                    (girl, _("No. It's not something I've pursued."), "normal"),
                    (girl, _("Never. Sounds complicated and messy."), "normal"),
                ]

        return (question, [renpy.random.choice(answers)], _discoveries)

    # ── Harem-exclusive truth: "Who does he treat better?" ──

    def tod_lewd_who_treats_better(girl, other_girl=None):
        """Harem-only: who does the player treat better?"""
        question = _("Who do you think he treats better?")
        _discoveries = []
        if other_girl is None:
            answers = [(girl, _("I think he treats us both pretty well, honestly."), "happy")]
            return (question, [renpy.random.choice(answers)], _discoveries)

        _my_love = getattr(girl, "Love", 0)
        _her_love = getattr(other_girl, "Love", 0)
        _on = other_girl.Name

        _answer_lines = []
        if _my_love > _her_love + 100:
            _answer_lines.append(renpy.random.choice([
                (girl, _tl(_("Me, obviously. Sorry %s, but I've got him wrapped around my finger.")) % _on, "smug"),
                (girl, _tl(_("I think he likes me more. No offense, %s.")) % _on, "smirk"),
                (girl, _("I mean... have you seen the way he looks at me? Case closed."), "smug"),
            ]))
            _answer_lines.append((other_girl, renpy.random.choice([
                _("Oh, really? We'll see about that."),
                _("In your dreams. He's just being polite with you."),
                _("Don't get too comfortable, girl."),
            ]), "angry"))
        elif _her_love > _my_love + 100:
            _answer_lines.append(renpy.random.choice([
                (girl, _tl(_("Honestly? Probably %s. But I'm working on it.")) % _on, "uncomfortable"),
                (girl, _("I think he has a favorite. And it's not me. Yet."), "looking_left"),
                (girl, _tl(_("Fine, I'll admit it. He's a little more attentive with %s.")) % _on, "looking_left"),
            ]))
            _answer_lines.append((other_girl, renpy.random.choice([
                _("Aw, don't be sad. I'll share~"),
                _("He loves us both. I just get a few extra kisses."),
                _("Don't worry, I keep him warmed up for you too."),
            ]), "smirk"))
        else:
            _answer_lines.append(renpy.random.choice([
                (girl, _("I think he treats us equally. Which is probably why this works."), "happy"),
                (girl, _tl(_("He's fair. I'll give him that. Right, %s?")) % _on, "smile"),
                (girl, _("We both get spoiled. I'm not complaining."), "happy"),
            ]))
            _answer_lines.append((other_girl, renpy.random.choice([
                _("Agreed. He knows how to keep us both happy."),
                _("For now. But I'm going to pull ahead~"),
                _("True. He's a good boyfriend. To both of us."),
            ]), "happy"))
        return (question, _answer_lines, _discoveries)

    # ── Question registry ─────────────────────────────────

    # Safe questions: (label, builder_func, needs_other_girl, needs_exam)
    TOD_SAFE_QUESTIONS = [
        ("Who do you like most on campus?",    tod_truth_who_you_like_most,          True,  False),
        (_("Have you ever been in a relationship?"), tod_truth_had_boyfriend,             False, False),
        ("What did you first notice about me?",tod_truth_first_notice_about_player,  False, False),
        (_("Worst gift you ever received?"),      tod_truth_worst_gift,                 False, False),
        (_("How did your last exam go?"),         tod_truth_exam_grades,                False, True),
        ("What's your favorite hobby?",        tod_truth_favorite_hobby,             False, False),
        ("Are you into guys, girls, or both?", tod_truth_sexuality,                  False, False),
    ]

    # Lewd questions: (label, builder_func, needs_other_girl)
    TOD_LEWD_QUESTIONS = [
        (_("Most extreme thing you've done?"),    tod_lewd_most_extreme,        False),
        (_("Ever recorded an intimate video?"),   tod_lewd_recorded_video,      False),
        (_("Do you prefer going raw or using a condom?"), tod_lewd_raw_sex,     True),
        (_("Has anyone ever finished inside you?"), tod_lewd_creampie,           False),
        ("Thoughts on public places?",         tod_lewd_public_acts,         False),
        (_("Favorite position or act?"),          tod_lewd_favorite_position,   False),
        (_("Ever cheated on someone?"),           tod_lewd_ever_cheated,        True),
        (_("Rough or gentle?"),                   tod_lewd_hardcore_or_gentle,  False),
        ("Craziest place you'd do it?",        tod_lewd_craziest_place,      False),
        ("Do you touch yourself?",             tod_lewd_touch_yourself,      False),
        ("What's your biggest fetish?",        tod_lewd_biggest_fetish,      False),
        (_("Who was your first time with?"),      tod_lewd_first_time,          True),
        (_("Ever had a condom break?"),           tod_lewd_condom_break,        False),
        ("Would you do something sexual for money?", tod_lewd_financial,     False),
        ("Ever done a threesome?",                 tod_lewd_threesome,     True),
    ]

    # ── PLAYER TRUTH QUESTIONS (asked by girls) ───────────
    # Each returns a label for the menu + a key used in the flow label
    # The actual interaction is handled in renpy labels because
    # player choices need menus.

    TOD_PLAYER_QUESTIONS = [
        ("Who do you like most on campus?",     "player_who_like"),
        (_("How did you do on your last exam?"),   "player_exam"),
        ("Have you ever had a girlfriend?",     "player_had_gf"),
        ("What's your favorite hobby?",         "player_hobby"),
        (_("Most extreme thing you've done?"),     "player_extreme"),
        (_("Favorite position?"),                  "player_fav_position"),
        (_("Do you prefer going raw or using a condom?"), "player_condom_pref"),
        (_("Ever recorded a video?"),              "player_recorded_video"),
        (_("Do you like it rough during sex?"),    "player_rough_or_gentle"),
        ("Craziest place you'd do it?",        "player_craziest_place"),
        ("Do you touch yourself?",             "player_touch_yourself"),
        ("What's your biggest fetish?",        "player_biggest_fetish"),
        (_("Ever had a condom break?"),           "player_condom_break"),
        ("Would you do something sexual for money?", "player_financial"),
        ("Ever done a threesome?",                  "player_threesome"),
        ("What breast size do you prefer?",             "player_bust_pref"),
        # Special: only added dynamically when conditions are met
        # ("Who made you feel better, me or her?", "player_who_better"),
    ]

    def tod_check_who_better(asker, other):
        """Check if the 'who made you feel better' question can appear.
        Requires: asker did sexual acts with player AND asker knows other did too
        (via witness_history or video_seen_history)."""
        # Asker must have done stuff with player
        asker_acts = getattr(asker, "Sex_acts", {})
        asker_did = any(asker_acts.get(a, 0) > 0 for a in ("hj", "bj", "tj", "sex", "anal"))
        if not asker_did:
            return False

        # Asker must know other girl also did stuff with player
        # Check witness_history
        witness = getattr(asker, "witness_history", [])
        saw_other = any(w.get("girl") == other.gid for w in witness)
        if saw_other:
            return True

        # Check video_seen_history
        vids_seen = getattr(asker, "video_seen_history", [])
        saw_vid = any(v.get("girl_gid") == other.gid for v in vids_seen)
        if saw_vid:
            return True

        # Check if other girl's Sex_acts show she did stuff (asker might have heard about it)
        other_acts = getattr(other, "Sex_acts", {})
        other_did = any(other_acts.get(a, 0) > 0 for a in ("hj", "bj", "tj", "sex", "anal"))
        # Only if asker is drunk enough to be bold about it
        if other_did and hangout_get_alcohol(asker) >= 5:
            return True

        return False

# ============================================================
# TRUTH OR DARE — Main flow
# ============================================================

label _tod_get_sick(who):
    # Someone drank past their limit — they get sick and the night winds down.
    $ store._tod_ended_sick = who
    if who == "player":
        $ Narration(_("The room tilts hard and your stomach lurches. You've had way too much tonight."))
        $ Say_Player(_("Okay... I'm done. I need to lie down before I throw up."))
        $ Narration(_("You call it a night before things get messy."))
    else:
        $ _sick_name = who.Name
        $ set_scene_expression(who, "disgusted")
        $ Narration(_("[_sick_name] goes pale mid-laugh and presses a hand to her mouth."))
        python:
            _sick_lines = [
                _("I... I don't feel so good. I think I had way too much."),
                _("Ugh, the room is spinning. I need to stop, right now."),
                _("No more for me... I feel really sick."),
            ]
        $ Say_Line(who, _tl(renpy.random.choice(_sick_lines)))
        $ who.discover("discovered_trait_lightweight") if who.has_trait("lightweight") else None
        $ Narration(_("The mood fizzles out as [_sick_name] has to call it a night."))
    return

label hangout_tod_round:
    python:
        _h_ga = store._hangout_girl_a
        _h_gb = store._hangout_girl_b
        _h_gc = store._hangout_girl_c
        _tod_girls = _hangout_girls_list()
        store._h_npc = getattr(store, "_hangout_partner_npc", None)
        _h_name_a = _h_ga.Name if _h_ga else "???"
        _h_name_b = _h_gb.Name if _h_gb else "???"

    python:
        _tod_played_before = getattr(store, "_hangout_tod_played", False)

    if not _tod_played_before:
        $ Narration(_("You grab the empty bottle and place it in the middle."))
        $ Say_Player(_("Alright, time for truth or dare. Whoever the bottle points at has to answer or do the dare."))
        $ Say_Player(_("One rule though: if you refuse a dare, you drink double AND take off a piece of clothing. No exceptions."))

        python:
            _tod_react_pools = [
                [
                    _("Wait, take off clothes?! That's brutal!"),
                    _("You're joking, right? ...You're not joking."),
                    _("Okay, I'm in. But nothing too crazy!"),
                ],
                [
                    _("That's a dangerous rule. I like it."),
                    _("So basically, no refusing. Got it."),
                    _("Fine, but I reserve the right to complain loudly!"),
                ],
                [
                    _("This is going to get interesting fast."),
                    _("I have a bad feeling about this... but I'm in."),
                    _("No backing out now, right?"),
                ],
            ]
            _react_expressions = ["surprised", "smirk", "happy"]
            for _ri, _rg in enumerate(_tod_girls):
                _rp = _tod_react_pools[min(_ri, len(_tod_react_pools) - 1)]
                set_scene_expression(_rg, _react_expressions[min(_ri, len(_react_expressions) - 1)])
                Say_Line(_rg, _tl(renpy.random.choice(_rp)))

        if _npc_is_active():
            python:
                _tod_npc_ntr = _npc_is_ntr(store._h_npc) if callable(globals().get("_npc_is_ntr")) else False
                _tod_npc_name = store._h_npc.Name
            if _tod_npc_ntr:
                $ Character(store._h_npc.Name, color=store._h_npc.color)(_tl(_("Stripping... clothes? Er... okay, I guess.")))
                $ Character(store._h_npc.Name, color=store._h_npc.color)(_tl(_("I mean... if that's the rule, who am I to argue?")))
            else:
                $ Character(store._h_npc.Name, color=store._h_npc.color)(_tl(_("Stripping?! Are you out of your mind?!")))
                python:
                    _npc_gf = GIRL_BY_ID.get(store._h_npc.girl_gid) if hasattr(store._h_npc, "girl_gid") else _h_ga
                    _npc_gf_for_react = _npc_gf if _npc_gf else _h_ga
                $ set_scene_expression(_npc_gf_for_react, "smirk")
                $ Say_Line(_npc_gf_for_react, _tl(_("Stop being so uptight, %s! It's just a game and it's only us here. It's no big deal.")) % _tod_npc_name)
                $ Character(store._h_npc.Name, color=store._h_npc.color)(_tl(_("Er... fine. But no funny business.")))
                $ Character(store._h_npc.Name, color=store._h_npc.color)(_tl(_("And I'm NOT doing that! I'll drink double, but I'm not taking anything off.")))

        $ store._hangout_tod_played = True
        $ unlock_achievement("game_night")
    else:
        python:
            _again_lines = [
                _("Another round? Let's go!"),
                _("Alright, the bottle is back. Round two!"),
                _("Ready for more? Let's spin it."),
                _("Okay, who's next? Bottle time."),
            ]
        $ Say_Player(_tl(renpy.random.choice(_again_lines)))

        python:
            _again_pools = [
                [
                    _("I'm ready."),
                    _("Bring it on."),
                    _("Let's see who gets it this time."),
                ],
                [
                    _("This time I'm not holding back."),
                    _("I have a feeling this round will be worse."),
                    _("Let's do this!"),
                ],
                [
                    _("I'm even more ready this time."),
                    _("Let's keep this energy going!"),
                    _("My turn to get lucky with the bottle."),
                ],
            ]
            for _ri, _rg in enumerate(_tod_girls):
                _rp = _again_pools[min(_ri, len(_again_pools) - 1)]
                set_scene_expression(_rg, "happy" if _ri == 0 else "smirk")
                Say_Line(_rg, _tl(renpy.random.choice(_rp)))

        if _npc_is_active():
            python:
                _npc_ntr_rem = _npc_is_ntr(store._h_npc) if callable(globals().get("_npc_is_ntr")) else False
                if _npc_ntr_rem:
                    _npc_rem_line = renpy.random.choice([
                        _("And, uh... I'm still just drinking. Not stripping."),
                        _("Same rules as before. I drink, I don't strip."),
                    ])
                else:
                    _npc_rem_line = renpy.random.choice([
                        _("And I'm STILL not taking anything off. Just so everyone remembers."),
                        _("Same deal as before. I drink double, but I keep my clothes ON."),
                        _("Don't even think about it. I'm drinking, not stripping."),
                    ])
            $ Character(store._h_npc.Name, color=store._h_npc.color)(_tl(_npc_rem_line))

    # Each person spins once per round. Order: Player, then each present girl.
    # (The NPC partner is present but does NOT spin — "Present + target".)
    $ _tod_turn = 0
    $ _tod_nparts = 1 + len(_hangout_girls_list()) + (1 if _npc_is_active() else 0)

    label .tod_turn_loop:
        $ print("[TOD-LOOP] turn=%d nparts=%d passed_out=%s party_ended=%s" % (_tod_turn, _tod_nparts, getattr(store, "_npc_passed_out", False), getattr(store, "_secret_party_ended", False)))
        if getattr(store, "_secret_party_ended", False):
            $ print("[TOD-LOOP] _secret_party_ended=True, returning immediately")
            return
        if _tod_turn >= _tod_nparts:
            $ Narration(_("The round is over. Everyone takes a sip to celebrate."))
            python:
                tod_drink_player(1)
                for _g in _hangout_girls_list():
                    tod_drink(_g, 1)
                _tod_npc_sick = False
                if _npc_is_active():
                    tod_drink(store._h_npc, 1)
                    if tod_rolls_sick(store._h_npc):
                        _tod_npc_sick = True
                _tod_sick_who = None
                if tod_player_rolls_sick():
                    _tod_sick_who = "player"
                else:
                    for _g in _hangout_girls_list():
                        if tod_rolls_sick(_g):
                            _tod_sick_who = _g
                            break
                print("[TOD-ROUND-END] npc_sick=%s sick_who=%s" % (_tod_npc_sick, _tod_sick_who))
            if _tod_npc_sick:
                $ print("[TOD-ROUND-END] NPC pass-out firing (girls=%d)" % len(_hangout_girls_list()))
                if len(_hangout_girls_list()) == 1:
                    call _npc_pass_out_1girl_event from _call_npc_po_1g_tod
                else:
                    call _npc_pass_out_event from _call_npc_po_tod
                $ print("[TOD-ROUND-END] After pass-out: _secret_party_ended=%s" % getattr(store, "_secret_party_ended", False))
            if _tod_sick_who is not None:
                call _tod_get_sick(_tod_sick_who) from _call_tod_get_sick
            $ print("[TOD-ROUND-END] About to return from hangout_tod_round")
            return

        python:
            # Build participants (player + present girls + optional NPC).
            _tod_parts = [("player", None)]
            for _gg in _hangout_girls_list():
                _tod_parts.append((_gg.gid, _gg))
            if _npc_is_active():
                _tod_parts.append(("bf", store._h_npc))
            _tod_nparts = len(_tod_parts)

        if _tod_turn >= len(_tod_parts):
            $ print("[TOD] turn %d >= parts %d — participant left mid-round, ending" % (_tod_turn, len(_tod_parts)))
            return

        python:
            _sp_id, _sp_obj = _tod_parts[_tod_turn]
            if _sp_id == "player":
                _spinner = "player"
                _spinner_name = "You"
            else:
                _spinner = _sp_obj
                _spinner_name = _sp_obj.Name
            _targets = [p for _i, p in enumerate(_tod_parts) if _i != _tod_turn]

        if _spinner == "player":
            $ Narration(_("It's your turn to spin the bottle."))
        else:
            $ Narration(_("[_spinner_name] grabs the bottle and gives it a spin."))

        # Spin result
        if not _targets:
            $ print("[TOD] No valid targets — ending round early")
            return
        python:
            _target_pick = renpy.random.choice(_targets)
            _target_id = _target_pick[0]
            _target_girl = _target_pick[1]

            if _target_id == "player":
                _target_name = _tl(_("you"))
            elif _target_id == "bf":
                _target_name = store._h_npc.Name if store._h_npc else "???"
            else:
                _target_name = _target_girl.Name if _target_girl else "???"

        $ Narration(_("The bottle spins... and lands on [_target_name]!"))

        # Bf spun -> he asks/dares the target from his own reduced pool.
        if _spinner is store._h_npc and _npc_is_active():
            call hangout_tod_bf_ask(store._h_npc, _target_id, _target_girl) from _call_hangout_tod_bf_ask
            $ _tod_turn += 1
            jump .tod_turn_loop

        # Bottle landed on the bf -> he answers/does his own reduced pool.
        if _target_id == "bf":
            call hangout_tod_bf_target(store._h_npc, _spinner) from _call_hangout_tod_bf_target
            $ _tod_turn += 1
            jump .tod_turn_loop

        # If target is the player, player chooses freely
        if _target_id == "player":
            $ _asker = _spinner
            menu:
                "The bottle is pointing at you. Truth or dare?"

                "Truth":
                    # Girl who spun picks a question
                    python:
                        _has_exam = store.Day >= EXAM_FIRST_DAY
                        _pq_avail = list(TOD_PLAYER_QUESTIONS)
                        if not _has_exam:
                            _pq_avail = [q for q in _pq_avail if q[1] != "player_exam"]
                        # Dynamically add "who was better" if conditions met
                        _pq_others = _tod_other_girls(_asker)
                        _pq_other = _pq_others[0] if _pq_others else None
                        if _pq_other and tod_check_who_better(_asker, _pq_other):
                            _wb_label = _tl(_("Who made you feel better... me or %s?")) % _pq_other.Name
                            _pq_avail.append((_wb_label, "player_who_better"))
                        # Filter out already-used questions
                        _pq_avail = [q for q in _pq_avail if not tod_is_used(q[1])]
                        if not _pq_avail:
                            # Fallback: allow repeats
                            _pq_avail = list(TOD_PLAYER_QUESTIONS)
                            if not _has_exam:
                                _pq_avail = [q for q in _pq_avail if q[1] != "player_exam"]
                        _pq_pick = renpy.random.choice(_pq_avail)
                        _pq_label = _pq_pick[0]
                        _pq_key = _pq_pick[1]

                    $ set_scene_expression(_asker, "smirk")
                    $ Say_Line(_asker, _tl(_pq_label))

                    # Jump to the specific player-answer label
                    call tod_player_answer(_pq_key, _asker) from _call_tod_player_answer

                "Dare":
                    call hangout_tod_player_dare(_asker) from _call_hangout_tod_player_dare

            $ _tod_turn += 1
            jump .tod_turn_loop

        # If target is a girl, she picks truth or dare based on stats
        python:
            _picks_dare = tod_girl_picks_dare(_target_girl)
            _choice_str = "dare" if _picks_dare else "truth"

        if _picks_dare:
            $ set_scene_expression(_target_girl, "smirk")
            $ Say_Line(_target_girl, renpy.random.choice([_("Dare. I'm feeling bold."), _("Dare! Hit me."), _("Dare. Let's make it interesting.")]))
            call hangout_tod_dare(_target_girl, _spinner) from _call_hangout_tod_dare
            $ _tod_turn += 1
            jump .tod_turn_loop
        else:
            $ set_scene_expression(_target_girl, "neutral")
            $ Say_Line(_target_girl, renpy.random.choice([_("Truth. Play it safe."), _("Truth... I'm not doing anything weird."), _("I'll go with truth.")]))

        # Girl chose truth -- player or other girl asks
        # If player spun, player picks the question
        # If another girl spun, she picks randomly
        if _spinner == "player":
            # Player picks question category
            python:
                _has_exam = store.Day >= EXAM_FIRST_DAY
                _safe_menu = []
                for _ql, _qf, _needs_other, _needs_exam in TOD_SAFE_QUESTIONS:
                    if _needs_exam and not _has_exam:
                        continue
                    if _needs_other and len(_hangout_girls_list()) < 2:
                        continue
                    if tod_is_used(_ql):
                        continue
                    _safe_menu.append((_tl(_ql), (_ql, _qf, _needs_other)))

                _lewd_menu = []
                for _ql, _qf, _needs_other in TOD_LEWD_QUESTIONS:
                    if _needs_other and len(_hangout_girls_list()) < 2:
                        continue
                    if tod_is_used(_ql):
                        continue
                    _lewd_menu.append((_tl(_ql), (_ql, _qf, _needs_other)))

            $ _chosen_q = None
            label .tod_pick_category:
            $ _tod_was_lewd = False
            menu:
                "Pick a question category:"

                "Safe questions":
                    python:
                        _tod_was_lewd = False
                        if not _safe_menu:
                            Narration(_("All safe questions have been asked already."))
                            _chosen_q = None
                        else:
                            _q_choices = [(lbl, val) for lbl, val in _safe_menu]
                            _q_choices.append((_("Back"), "_back"))
                            _chosen_q = renpy.display_menu(_q_choices)

                "Lewd questions":
                    python:
                        _tod_was_lewd = True
                        if not _lewd_menu:
                            Narration(_("All lewd questions have been asked already."))
                            _chosen_q = None
                        else:
                            _q_choices = [(lbl, val) for lbl, val in _lewd_menu]
                            _q_choices.append((_("Back"), "_back"))
                            _chosen_q = renpy.display_menu(_q_choices)

            if _chosen_q == "_back":
                jump .tod_pick_category

            if _chosen_q is None:
                $ _tod_turn += 1
                jump .tod_turn_loop

            python:
                _chosen_q_label, _qfunc, _needs_other = _chosen_q
                _last_q = _chosen_q_label
                _other_g = _tod_other_girl(_target_girl)

                if _needs_other:
                    _question, _answer_lines, _discoveries = _qfunc(_target_girl, _other_g)
                else:
                    _question, _answer_lines, _discoveries = _qfunc(_target_girl)

            $ Say_Player(_tl(_question))

            # Check if girl refuses to answer
            if tod_girl_refuses(_target_girl):
                $ set_scene_expression(_target_girl, "angry")
                $ Say_Line(_target_girl, renpy.random.choice([_("I'm not answering that."), _("Nope. Pass."), _("No way. I'll drink instead.")]))
                python:
                    _strip_lvl, _exposed, _removed = tod_dare_strip_penalty(_target_girl)
                    _ref_name = _target_girl.Name
                $ Narration(_("[_ref_name] refuses to answer. She drinks double and takes off her [_removed]."))
                $ tod_drink(_target_girl, 3)
                # First-time exposure reaction
                if _exposed == "chest":
                    $ set_scene_expression(_target_girl, "embarrassed", blush="2")
                    $ Say_Line(_target_girl, renpy.random.choice([
                        _("Don't stare! I said don't stare!"),
                        _("This is so humiliating..."),
                        _("I can't believe you're all seeing this..."),
                    ]))
                    $ Say_Player(renpy.random.choice([
                        _("Wow..."),
                        _("Not bad at all."),
                        _("I'm definitely looking."),
                    ]))
                    python:
                        Change_Status(_target_girl, "Inbt", 15)
                elif _exposed == "panties":
                    $ set_scene_expression(_target_girl, "embarrassed", blush="2")
                    $ Say_Line(_target_girl, renpy.random.choice([
                        _("There! You happy now?! Everything is out!"),
                        _("I'm completely naked... in front of everyone..."),
                        _("This game has gone way too far..."),
                    ]))
                    $ Say_Player(renpy.random.choice([
                        _("You look amazing, honestly."),
                        _("Nothing to be ashamed of."),
                        _("That's... quite the view."),
                    ]))
                    python:
                        Change_Status(_target_girl, "Inbt", 25)
                        Change_Status(_target_girl, "Obed", 10)
                # NPC watched her strip instead of answering.
                if _npc_is_active() and _removed is not None and _bf_is_gf(store._h_npc, _target_girl):
                    call _bf_watch_girl_truth(store._h_npc, _target_girl, _tod_was_lewd, True, _chosen_q_label) from _call_bf_watch_girl_strip
            else:
                # Girl answers
                $ _ai = 0
                while _ai < len(_answer_lines):
                    python:
                        _a_item = _answer_lines[_ai]
                        _a_speaker = _a_item[0]
                        _a_text = _a_item[1]
                        _a_expr = _a_item[2] if len(_a_item) > 2 else None
                        _a_blush = _a_item[3] if len(_a_item) > 3 else None
                        if _a_expr is not None:
                            set_scene_expression(_a_speaker, _a_expr, blush=_a_blush)
                        Say_Line(_a_speaker, _tl(_a_text))
                        _ai += 1
                # Apply discoveries only when she actually answered
                $ tod_mark_used(_chosen_q_label)
                $ _disc_idx = 0
                while _disc_idx < len(_discoveries):
                    python:
                        _dk = _discoveries[_disc_idx]
                        if isinstance(_dk, tuple):
                            # (girl, key): the OTHER girl's own reaction line evidenced HER trait
                            if hasattr(_dk[0], "discover"):
                                _dk[0].discover(_dk[1])
                        elif hasattr(_target_girl, "discover"):
                            _target_girl.discover(_dk)
                        _disc_idx += 1
                    pause 0.5

                $ _tod_propagate_knowledge(_target_girl, _discoveries)

                # Virgin reveal follow-up from other girl
                if "discovered_virgin" in _discoveries and _other_g is not None:
                    $ set_scene_expression(_target_girl, "embarrassed", blush="2")
                    python:
                        _has_bf_reveal = "discovered_has_partner" in _discoveries
                    if _has_bf_reveal:
                        $ set_scene_expression(_other_g, "surprised")
                        $ Say_Line(_other_g, _format_partner_line(_target_girl, renpy.random.choice([
                            _("Wait, not even with your %(pl)s?"),
                            _("Hold on... you and your %(pl)s never...?"),
                            _("Really? Not even %(po)s?"),
                        ])))
                        $ set_scene_expression(_target_girl, "shy", blush="2")
                        $ Say_Line(_target_girl, renpy.random.choice([
                            _("No... we're waiting."),
                            _("We decided to take things slow."),
                            _("It just hasn't happened yet, okay?"),
                        ]))
                    else:
                        $ set_scene_expression(_other_g, "surprised")
                        $ Say_Line(_other_g, renpy.random.choice([
                            _("Wait, seriously? You're a virgin?"),
                            _("Oh... I honestly didn't expect that."),
                            _("For real? That's actually kind of sweet."),
                        ]))

                # Knowledge callout from other girl (she knows something about the answer)
                python:
                    _kc_topic_map = {
                        "Most extreme thing you've done?": "extreme",
                        "Ever recorded an intimate video?": "recorded",
                        "Do you prefer going raw or using a condom?": "raw",
                        "Has anyone ever finished inside you?": "creampie",
                        "Ever cheated on someone?": "cheating",
                        "Who was your first time with?": "first_time",
                        "Ever had a condom break?": "creampie",
                        "Ever done a threesome?": "threesome",
                    }
                    _kc_topic = _kc_topic_map.get(_chosen_q_label, None)
                    _kc_line = _tod_knowledge_callout(_other_g, _target_girl, _kc_topic) if (_kc_topic and _other_g is not None) else None
                if _kc_line is not None:
                    python:
                        _kc_expr = _kc_line[2] if len(_kc_line) > 2 else None
                        _kc_blush = _kc_line[3] if len(_kc_line) > 3 else None
                        if _kc_expr is not None:
                            set_scene_expression(_kc_line[0], _kc_expr, blush=_kc_blush)
                    $ Say_Line(_kc_line[0], _tl(_kc_line[1]))

                # NPC was watching a girl answer a truth.
                if _npc_is_active():
                    if _bf_is_gf(store._h_npc, _target_girl):
                        call _bf_watch_girl_truth(store._h_npc, _target_girl, _tod_was_lewd, False, _chosen_q_label) from _call_bf_watch_girl_answer
                    elif _tod_was_lewd:
                        call _bf_watch_nongf_truth(store._h_npc, _target_girl, _discoveries) from _call_bf_watch_nongf_answer

        else:
            # Another girl asks -- safe or lewd depending on alcohol + Inbt
            python:
                _has_exam = store.Day >= EXAM_FIRST_DAY
                _lewd_chance = _tod_lewd_chance(_spinner)
                _go_lewd = renpy.random.random() < _lewd_chance

                if _go_lewd and TOD_LEWD_QUESTIONS:
                    _tod_was_lewd = True
                    _avail_q = []
                    for _ql, _qf, _needs_other in TOD_LEWD_QUESTIONS:
                        _avail_q.append((_ql, _qf, _needs_other))
                    if store._hangout_is_harem_night and len(_hangout_girls_list()) >= 2:
                        _avail_q.append((_("Who does he treat better?"), tod_lewd_who_treats_better, True))
                    _avail_q = [q for q in _avail_q if not tod_is_used(q[0])]
                else:
                    _tod_was_lewd = False
                    _avail_q = []
                    for _ql, _qf, _needs_other, _needs_exam in TOD_SAFE_QUESTIONS:
                        if _needs_exam and not _has_exam:
                            continue
                        _avail_q.append((_ql, _qf, _needs_other))
                    _avail_q = [q for q in _avail_q if not tod_is_used(q[0])]

                # Fallback: if all questions used, allow repeats
                if not _avail_q:
                    if _go_lewd:
                        for _ql, _qf, _needs_other in TOD_LEWD_QUESTIONS:
                            _avail_q.append((_ql, _qf, _needs_other))
                        if store._hangout_is_harem_night and len(_hangout_girls_list()) >= 2:
                            _avail_q.append((_("Who does he treat better?"), tod_lewd_who_treats_better, True))
                    else:
                        for _ql, _qf, _needs_other, _needs_exam in TOD_SAFE_QUESTIONS:
                            if _needs_exam and not _has_exam:
                                continue
                            _avail_q.append((_ql, _qf, _needs_other))

                _pick = renpy.random.choice(_avail_q)
                _q_label_auto = _pick[0]
                _last_q = _q_label_auto
                _qfunc_auto = _pick[1]
                _needs_other_auto = _pick[2]

                _other_g_auto = _tod_other_girl(_target_girl)

                if _needs_other_auto:
                    _question_auto, _answer_auto, _discoveries_auto = _qfunc_auto(_target_girl, _other_g_auto)
                else:
                    _question_auto, _answer_auto, _discoveries_auto = _qfunc_auto(_target_girl)

            $ set_scene_expression(_spinner, "smirk")
            $ Say_Line(_spinner, _tl(_q_label_auto))

            # Check if girl refuses to answer
            if tod_girl_refuses(_target_girl):
                $ set_scene_expression(_target_girl, "angry")
                $ Say_Line(_target_girl, renpy.random.choice([_("I'm not answering that."), _("Nope. Pass."), _("No way. I'll drink instead.")]))
                python:
                    _strip_lvl, _exposed2, _removed = tod_dare_strip_penalty(_target_girl)
                    _ref_name = _target_girl.Name
                $ Narration(_("[_ref_name] refuses to answer. She drinks double and takes off her [_removed]."))
                $ tod_drink(_target_girl, 3)
                if _exposed2 == "chest":
                    $ set_scene_expression(_target_girl, "embarrassed", blush="2")
                    $ Say_Line(_target_girl, renpy.random.choice([
                        _("Stop looking!"),
                        _("This is the worst game ever..."),
                        _("I should have just answered the question..."),
                    ]))
                    $ set_scene_expression(_spinner, "bemused")
                    $ Say_Line(_spinner, renpy.random.choice([
                        _("Well, that's one way to avoid the question~"),
                        _("Should have just answered!"),
                        _("Nice view though."),
                    ]))
                    python:
                        Change_Status(_target_girl, "Inbt", 15)
                elif _exposed2 == "panties":
                    $ set_scene_expression(_target_girl, "embarrassed", blush="2")
                    $ Say_Line(_target_girl, renpy.random.choice([
                        _("Are you all satisfied now?! I have nothing left!"),
                        _("I'm literally naked... this is insane..."),
                        _("I should have answered every single question..."),
                    ]))
                    $ set_scene_expression(_spinner, "bemused")
                    $ Say_Line(_spinner, renpy.random.choice([
                        _("Wow. You really chose this over answering?"),
                        _("Must have been a really bad answer if she'd rather strip."),
                        _("I'm impressed by the commitment, honestly."),
                    ]))
                    python:
                        Change_Status(_target_girl, "Inbt", 25)
                        Change_Status(_target_girl, "Obed", 10)
            else:
                $ _ai2 = 0
                while _ai2 < len(_answer_auto):
                    python:
                        _a2_item = _answer_auto[_ai2]
                        _a2_speaker = _a2_item[0]
                        _a2_text = _a2_item[1]
                        _a2_expr = _a2_item[2] if len(_a2_item) > 2 else None
                        _a2_blush = _a2_item[3] if len(_a2_item) > 3 else None
                        if _a2_expr is not None:
                            set_scene_expression(_a2_speaker, _a2_expr, blush=_a2_blush)
                        Say_Line(_a2_speaker, _tl(_a2_text))
                        _ai2 += 1
                # Apply discoveries only when she actually answered
                $ tod_mark_used(_q_label_auto)
                $ _disc_idx2 = 0
                while _disc_idx2 < len(_discoveries_auto):
                    python:
                        _dk2 = _discoveries_auto[_disc_idx2]
                        if isinstance(_dk2, tuple):
                            # (girl, key): the OTHER girl's own reaction line evidenced HER trait
                            if hasattr(_dk2[0], "discover"):
                                _dk2[0].discover(_dk2[1])
                        elif hasattr(_target_girl, "discover"):
                            _target_girl.discover(_dk2)
                        _disc_idx2 += 1
                    pause 0.5

                $ _tod_propagate_knowledge(_target_girl, _discoveries_auto)

                # Virgin reveal follow-up from spinner
                if "discovered_virgin" in _discoveries_auto:
                    python:
                        _has_bf_reveal2 = "discovered_has_partner" in _discoveries_auto
                    if _has_bf_reveal2:
                        $ set_scene_expression(_spinner, "surprised")
                        $ Say_Line(_spinner, _format_partner_line(_target_girl, renpy.random.choice([
                            _("Wait, not even with your %(pl)s?!"),
                            _("Seriously? You guys never...?"),
                            _("Hold on. %(Pp)s never...? Like, ever?"),
                        ])))
                        $ set_scene_expression(_target_girl, "shy", blush="1")
                        $ Say_Line(_target_girl, renpy.random.choice([
                            _("No... we're waiting. Is that so hard to believe?"),
                            _("It just hasn't happened. We're taking it slow."),
                            _("Not everyone rushes into it, you know..."),
                        ]))
                    else:
                        $ set_scene_expression(_spinner, "surprised")
                        $ Say_Line(_spinner, renpy.random.choice([
                            _("Wait... you're a virgin?"),
                            _("Oh! I had no idea..."),
                            _("Wow, for real? I wouldn't have guessed."),
                        ]))

                # Knowledge callout from other girl present
                python:
                    _kc_topic_map2 = {
                        "Most extreme thing you've done?": "extreme",
                        "Ever recorded an intimate video?": "recorded",
                        "Do you prefer going raw or using a condom?": "raw",
                        "Has anyone ever finished inside you?": "creampie",
                        "Ever cheated on someone?": "cheating",
                        "Who was your first time with?": "first_time",
                        "Ever had a condom break?": "creampie",
                        "Ever done a threesome?": "threesome",
                    }
                    _kc_topic2 = _kc_topic_map2.get(_q_label_auto, None)
                    # The "other" for callout: any girl NOT the target and NOT the spinner
                    _kc_candidates2 = [g for g in _hangout_girls_list() if g.gid != _target_girl.gid and g is not _spinner]
                    _kc_other2 = renpy.random.choice(_kc_candidates2) if _kc_candidates2 else None
                    _kc_line2 = _tod_knowledge_callout(_kc_other2, _target_girl, _kc_topic2) if (_kc_topic2 and _kc_other2) else None
                if _kc_line2 is not None:
                    python:
                        _kc2_expr = _kc_line2[2] if len(_kc_line2) > 2 else None
                        _kc2_blush = _kc_line2[3] if len(_kc_line2) > 3 else None
                        if _kc2_expr is not None:
                            set_scene_expression(_kc_line2[0], _kc2_expr, blush=_kc2_blush)
                    $ Say_Line(_kc_line2[0], _tl(_kc_line2[1]))

                # NPC was watching a girl answer a truth (girl-asks-girl path).
                if _npc_is_active() and _target_girl is not None:
                    if _bf_is_gf(store._h_npc, _target_girl):
                        call _bf_watch_girl_truth(store._h_npc, _target_girl, _tod_was_lewd, False, _q_label_auto) from _call_bf_watch_girl_answer_auto
                    elif _tod_was_lewd:
                        call _bf_watch_nongf_truth(store._h_npc, _target_girl, _discoveries_auto) from _call_bf_watch_nongf_answer_auto

        # Brief reaction from others (context-aware)
        python:
            # Pick a reactor: any girl who is NOT the target and NOT the spinner
            _reactor_candidates = [g for g in _hangout_girls_list()
                                   if (_target_girl is None or g.gid != _target_girl.gid)
                                   and g is not _spinner]
            if not _reactor_candidates:
                _reactor_candidates = [g for g in _hangout_girls_list()
                                       if _target_girl is None or g.gid != _target_girl.gid]
            _reactor = renpy.random.choice(_reactor_candidates) if _reactor_candidates else None

            _r_alc = hangout_get_alcohol(_reactor)
            _r_hardcore = hasattr(_reactor, "has_trait") and _reactor.has_trait("hardcore_sex")
            _r_cute = hasattr(_reactor, "has_trait") and _reactor.has_trait("cute_sex")
            _r_cheater = hasattr(_reactor, "has_trait") and _reactor.has_trait("cheater")
            _r_loyal = hasattr(_reactor, "has_trait") and _reactor.has_trait("loyal")
            _r_cam = hasattr(_reactor, "has_trait") and _reactor.has_trait("camera_lover")
            _r_pub = hasattr(_reactor, "has_trait") and _reactor.has_trait("public_fetish")

            _react_pool = []

            if _tod_was_lewd:
                # Base lewd reactions
                _react_pool.extend([
                    _("Oh wow..."),

                    _("I was not ready for that answer."),

                    _("This game is getting intense."),

                ])

                # Trait-specific reactions to lewd content
                if _r_hardcore:
                    _react_pool.extend([
                        _("Ha! That's nothing. I've done worse."),

                        _("Finally, someone who isn't boring."),

                        _("Now we're talking."),

                        _("Mmm, I like where this is going."),

                    ])
                elif _r_cute:
                    _react_pool.extend([
                        _("Oh my god... I can't believe she just said that."),

                        _("I'm covering my ears! Too much!"),

                        _("My face is so red right now..."),

                        _("How can you just... say that out loud?"),

                    ])
                elif _r_cheater:
                    _react_pool.extend([
                        _("Heh, no judgment from me~"),

                        _("Been there, done that. Next."),

                        _("I have stories too, trust me."),

                    ])
                elif _r_loyal:
                    _react_pool.extend([
                        _("I could never do that..."),

                        _("That's... a lot. Are you okay?"),

                        _("I don't know how you can be so open about it."),

                    ])

                # Drunk reactor is more expressive
                if _r_alc >= 7:
                    _react_pool.extend([
                        _("Hahaha! Oh my god!"),

                        _("Tell me more! I want details!"),

                        _("This is the best game ever!"),

                        _("Wait wait wait, say that again!"),

                    ])
                elif _r_alc >= 4:
                    _react_pool.extend([
                        _("The drinks are making this game way too honest."),

                        _("Okay, I need another sip after that one."),

                        _("Haha, this is getting wild."),

                    ])

                # Camera lover reacts to video/recording topics (only when relevant)
                if _r_cam and _last_q == "Ever recorded an intimate video?":
                    _react_pool.extend([
                        _("See, cameras make everything more exciting~"),

                        _("I would have loved to see that."),

                    ])

                # Public fetish reacts to public act topics (only when relevant)
                if _r_pub and _last_q in (_("Thoughts on public places?"), _("Craziest place you'd do it?")):
                    _react_pool.extend([
                        _("Public? That's so hot."),

                        _("The risk is what makes it exciting, right?"),

                    ])

                # Knowledge-based reactions (reactor knows something about the target)
                if _target_id != "player" and _target_girl:
                    _r_kw = getattr(_reactor, "knows_with_player", {}).get(_target_girl.gid, set())
                    _r_tw = [w for w in getattr(_reactor, "witness_history", []) if w.get("girl") == _target_girl.gid]
                    _r_tvs = [v for v in getattr(_reactor, "video_seen_history", []) if v.get("girl_gid") == _target_girl.gid]
                    if _r_kw & {"sex", "cowgirl", "reverse_cowgirl", "hj", "bj", "tj"}:
                        _react_pool.extend([
                            _("Hmm... I know more than she thinks I do."),

                            _("Interesting answer, considering what I've seen."),

                            _("I could say something right now, but I'll hold my tongue. For now."),

                        ])
                    elif _r_tw:
                        _react_pool.extend([
                            _("I've seen things. That's all I'll say."),

                            _("She's not telling the whole story."),

                        ])
                    elif _r_tvs:
                        _react_pool.extend([
                            _("There's a video that paints a very different picture..."),

                            _("I've seen the evidence. Just saying."),

                        ])

            else:
                # Base safe reactions
                _react_pool.extend([
                    _("Interesting..."),
                    _("Haha, really?"),

                    _("I did not expect that."),

                ])

                # Trait-specific reactions to safe content
                if _r_hardcore:
                    _react_pool.extend([
                        _("Boring answer. Next."),

                        _("Can we get to the fun questions already?"),

                        _("Yawn. Wake me up when it gets spicy."),

                    ])
                elif _r_cute:
                    _react_pool.extend([
                        _("Aww, that's sweet!"),

                        _("That's actually really nice."),

                        _("Hehe, cute answer."),

                    ])

                # Drunk safe reactions
                if _r_alc >= 6:
                    _react_pool.extend([
                        _("Hahahaha! Why is that so funny to me right now?"),

                        _("I love this game when I'm drunk."),

                        _("Everything is hilarious tonight."),

                    ])
                elif _r_alc >= 3:
                    _react_pool.extend([
                        _("Fair enough."),

                        _("I can respect that."),

                        _("Good answer, good answer."),

                    ])
                else:
                    _react_pool.extend([
                        _("That's so you."),

                        _("Classic answer."),

                        _("Ha! Not what I expected."),

                    ])

        if _reactor:
            $ set_scene_expression(_reactor, "bemused")
            $ Say_Line(_reactor, _tl(renpy.random.choice(_react_pool)))

        $ _tod_turn += 1
        jump .tod_turn_loop

# ============================================================
# PLAYER TRUTH ANSWERS
# ============================================================
label tod_player_answer(key, asker):
    python:
        _pa_girls = _hangout_girls_list()
        _other = _tod_other_girl(asker) if asker is not None and asker != "player" else None

    if key == "player_who_like":
        call tod_pa_who_like(_pa_girls) from _call_tod_pa_who_like
    elif key == "player_exam":
        call tod_pa_exam(_pa_girls) from _call_tod_pa_exam
    elif key == "player_had_gf":
        call tod_pa_had_gf(_pa_girls) from _call_tod_pa_gf
    elif key == "player_hobby":
        call tod_pa_hobby(_pa_girls) from _call_tod_pa_hobby
    elif key == "player_extreme":
        call tod_pa_extreme(_pa_girls) from _call_tod_pa_extreme
    elif key == "player_fav_position":
        call tod_pa_fav_position(_pa_girls) from _call_tod_pa_fav_pos
    elif key == "player_condom_pref":
        call tod_pa_condom(_pa_girls) from _call_tod_pa_condom
    elif key == "player_recorded_video":
        call tod_pa_video(_pa_girls) from _call_tod_pa_video
    elif key == "player_rough_or_gentle":
        call tod_pa_rough(_pa_girls) from _call_tod_pa_rough
    elif key == "player_who_better":
        call tod_pa_who_better(asker, _other) from _call_tod_pa_who_better
    elif key == "player_craziest_place":
        call tod_pa_craziest_place(_pa_girls) from _call_tod_pa_crazy_place
    elif key == "player_touch_yourself":
        call tod_pa_touch_yourself(_pa_girls) from _call_tod_pa_touch
    elif key == "player_biggest_fetish":
        call tod_pa_biggest_fetish(_pa_girls) from _call_tod_pa_fetish
    elif key == "player_condom_break":
        call tod_pa_condom_break(_pa_girls) from _call_tod_pa_cbreak
    elif key == "player_financial":
        call tod_pa_financial(_pa_girls) from _call_tod_pa_financial
    elif key == "player_threesome":
        call tod_pa_threesome(_pa_girls) from _call_tod_pa_threesome
    elif key == "player_bust_pref":
        call tod_pa_bust_pref(_pa_girls) from _call_tod_pa_bust_pref
    # Mark player truth as used
    $ tod_mark_used(key)
    return

# --- 1. Who do you like most on campus? ---
label tod_pa_who_like(girls):
    python:
        ga = girls[0] if len(girls) > 0 else None
        gb = girls[1] if len(girls) > 1 else None
    if gb is None:
        $ Say_Player(_("That is a tough question..."))
        $ set_scene_expression(ga, "happy")
        $ Say_Line(ga, renpy.random.choice([_("Aww, you're sweet."), _("Come on, just say it!")]))
        return
    python:
        _choices = []
        _choices.append((ga.Name, "ga"))
        _choices.append((gb.Name, "gb"))
        _choices.append((_("Professor Williams"), "prof"))
    menu:
        "Who do you like most on campus?"

        "[ga.Name]":
            $ Say_Player(_("Honestly? [ga.Name]. There's just something about her."))
            python:
                Change_Status(ga, "Love", 20)
                set_scene_expression(ga, "embarrassed", blush="1")
                Say_Line(ga, renpy.random.choice([
                    _("W-what?! Really?"),

                    _("Oh... I wasn't expecting that."),

                    _("You're making me blush..."),

                ]))
                set_scene_expression(gb, "sad")
                Say_Line(gb, renpy.random.choice([
                    _("Wow. Right in front of me."),

                    _("Noted. I see how it is."),

                    _("Ouch. But fair, I guess."),

                ]))

        "[gb.Name]":
            $ Say_Player(_("I'd have to say [gb.Name]. She's something special."))
            python:
                Change_Status(gb, "Love", 20)
                set_scene_expression(gb, "embarrassed", blush="1")
                Say_Line(gb, renpy.random.choice([
                    _("Oh! That's... really sweet."),

                    _("Wait, really? Me?"),

                    _("Heh... thanks."),

                ]))
                set_scene_expression(ga, "angry")
                Say_Line(ga, renpy.random.choice([
                    _("Interesting choice."),

                    _("Of course you'd pick her."),

                    _("Hmph. Next question."),

                ]))

        "Professor Williams":
            $ Say_Player(_("Professor Williams. Have you seen those arms?"))
            python:
                Change_Status(ga, "Love", -10)
                Change_Status(gb, "Love", -10)
                set_scene_expression(ga, "disgusted")
                Say_Line(ga, renpy.random.choice([
                    _("...Are you serious right now?"),

                    _("I can't tell if you're joking or not."),

                ]))
                set_scene_expression(gb, "confused")
                Say_Line(gb, renpy.random.choice([
                    _("That's... not what I expected."),

                    _("You have weird taste."),

                ]))
    return

# --- 2. How did you do on your last exam? ---
label tod_pa_exam(girls):
    python:
        ga = girls[0] if len(girls) > 0 else None
        gb = girls[1] if len(girls) > 1 else None
    $ _grade = study_grade(Player.study_level)
    if _grade in ("A", "B"):
        $ Say_Player(_("Actually, pretty good. Got a [_grade]."))
        python:
            Change_Status(ga, "Love", 10)
            if gb is not None:
                Change_Status(gb, "Love", 10)
            set_scene_expression(ga, "surprised")
            Say_Line(ga, renpy.random.choice([
                _("Nice! Maybe you can tutor me sometime."),

                _("Wow, smart AND fun? Dangerous combo."),

            ]))
    elif _grade == "C":
        $ Say_Player(_("Average. A solid C. Not my best work."))
        python:
            if gb is not None:
                set_scene_expression(gb, "sly")
                Say_Line(gb, renpy.random.choice([
                    _("Relatable. Painfully relatable."),

                    _("C gang! We're in this together."),

                ]))
    else:
        $ Say_Player(_("...Bad. Really bad. I'd rather not say the letter."))
        python:
            Change_Status(ga, "Obed", 10)
            if gb is not None:
                Change_Status(gb, "Obed", 10)
            set_scene_expression(ga, "sad")
            Say_Line(ga, renpy.random.choice([
                _("Aww. At least you're honest about it."),

                _("That's okay. Exams don't define you."),

            ]))
            if gb is not None:
                set_scene_expression(gb, "sly")
                Say_Line(gb, renpy.random.choice([
                    _("Respect for admitting it, at least."),

                    _("Yikes. But hey, you're fun at parties!"),

                ]))
    return

# --- 3. Have you ever had a girlfriend? ---
label tod_pa_had_gf(girls):
    python:
        ga = girls[0] if len(girls) > 0 else None
        gb = girls[1] if len(girls) > 1 else None
        _has_gf = any(g.is_dating_player() for g in ALL_GIRLS)
        _has_ex = any(hasattr(g, "is_ex_of_player") and g.is_ex_of_player() for g in ALL_GIRLS)
        _ex_girl = None
        if _has_ex:
            for _eg in ALL_GIRLS:
                if hasattr(_eg, "is_ex_of_player") and _eg.is_ex_of_player():
                    _ex_girl = _eg
                    break
    menu:
        "Have you ever had a girlfriend?"

        "I had one, but it didn't work out" if _has_ex and not _has_gf:
            $ Say_Player(_("I did... but it ended. Things got complicated."))
            python:
                # Find the ex girl in the room
                _ex_present = None
                if _ex_girl and (_ex_girl.gid == ga.gid or (gb is not None and _ex_girl.gid == gb.gid)):
                    _ex_present = _ex_girl
                    _ex_other = gb if _ex_present.gid == ga.gid else ga
            if _ex_present is not None:
                $ _exn = _ex_present.Name
                python:
                    _ex_hist = getattr(_ex_present, "ex_player_history", None)
                    _ex_mood = _ex_hist.get("breakup_mood", "angry") if _ex_hist else "angry"
                if _ex_mood == "sad":
                    $ set_scene_expression(_ex_present, "sad")
                    $ Say_Line(_ex_present, renpy.random.choice([
                        _("..."),
                        _("Yeah. It did."),
                        _("Can we talk about something else?"),
                    ]))
                else:
                    $ set_scene_expression(_ex_present, "angry")
                    $ Say_Line(_ex_present, renpy.random.choice([
                        _("Complicated? That's one word for it."),
                        _("You're really going to bring that up? Here?"),
                        _("Hmph. 'Complicated' is putting it mildly."),
                    ]))
                if _ex_other is not None:
                    $ set_scene_expression(_ex_other, "surprised")
                    $ Say_Line(_ex_other, renpy.random.choice([
                        _("Wait... is she talking about...?"),
                        _("The tension in this room just went up about ten degrees."),
                        _("Oh. Oh wow. This just got awkward."),
                    ]))
            else:
                python:
                    set_scene_expression(ga, "sad")
                    Say_Line(ga, renpy.random.choice([_("What happened?"), _("Aw, that sucks.")]))
                    if gb is not None:
                        set_scene_expression(gb, "happy")
                        Say_Line(gb, renpy.random.choice([_("Her loss."), _("Moving on is hard. But you'll be fine.")]))

        "No, never" if not _has_gf and not _has_ex:
            $ Say_Player(_("Nope. Haven't found the right person yet."))
            python:
                Change_Status(ga, "Love", 10)
                if gb is not None:
                    Change_Status(gb, "Love", 10)
                set_scene_expression(ga, "surprised")
                Say_Line(ga, renpy.random.choice([
                    _("Really? That's kind of surprising."),

                    _("Hmm... interesting."),

                ]))
                if gb is not None:
                    set_scene_expression(gb, "smug", blush="1")
                    Say_Line(gb, renpy.random.choice([
                        _("Maybe you just haven't been looking in the right place~"),

                        _("Well, you're doing fine socially, at least."),

                    ]))

        "Yeah, I'm seeing someone" if _has_gf:
            $ Say_Player(_("Actually... yeah. I'm with someone right now."))
            python:
                Change_Status(ga, "Obed", 10)
                if gb is not None:
                    Change_Status(gb, "Obed", 10)
                _ga_is_gf = hasattr(ga, "is_dating_player") and ga.is_dating_player()
                _gb_is_gf = gb is not None and hasattr(gb, "is_dating_player") and gb.is_dating_player()
                if _ga_is_gf:
                    set_scene_expression(ga, "happy")
                    Say_Line(ga, renpy.random.choice([
                        _("That's me! Hi~"),
                        _("And she's sitting right here, for the record."),
                        _("Aww. Yeah, he's mine."),
                    ]))
                    if gb is not None:
                        set_scene_expression(gb, "surprised")
                        Say_Line(gb, renpy.random.choice([
                            _("Wait, you two are together?!"),
                            _("Oh! I had no idea! That's cute."),
                        ]))
                elif _gb_is_gf:
                    set_scene_expression(ga, "surprised")
                    Say_Line(ga, renpy.random.choice([
                        _("Wait, really? Who is it?"),
                        _("Oh! Details!"),
                    ]))
                    set_scene_expression(gb, "happy")
                    Say_Line(gb, renpy.random.choice([
                        _("That would be me, actually~"),
                        _("He's talking about me. Hi."),
                    ]))
                else:
                    set_scene_expression(ga, "surprised")
                    Say_Line(ga, renpy.random.choice([
                        _("Oh! Who's the lucky girl?"),
                        _("Wait, really? Details!"),
                    ]))
                    if gb is not None:
                        set_scene_expression(gb, "sly")
                        Say_Line(gb, renpy.random.choice([
                            _("And you're here drinking with us? Bold."),
                            _("Hmm... noted."),
                        ]))

        "No, never" if _has_gf:
            $ Say_Player(_("Nah, no one special in my life right now."))
            $ Narration(_("(You lied.)"))
            python:
                Change_Status(ga, "Love", 10)
                if gb is not None:
                    Change_Status(gb, "Love", 10)

    return

# --- 4. What's your favorite hobby? ---
label tod_pa_hobby(girls):
    python:
        ga = girls[0] if len(girls) > 0 else None
        gb = girls[1] if len(girls) > 1 else None
    menu:
        "What's your favorite hobby?"

        "Studying":
            $ Say_Player(_("Studying, honestly. I like learning new things."))
            python:
                Change_Status(ga, "Love", 10)
                if gb is not None:
                    Change_Status(gb, "Love", 10)
                set_scene_expression(ga, "happy")
                Say_Line(ga, renpy.random.choice([
                    _("That's actually really attractive."),

                    _("A nerd! I like it."),

                ]))

        "Working out":
            $ Say_Player(_("Hitting the gym. Nothing beats a good workout."))
            python:
                Change_Status(ga, "Obed", 10)
                if gb is not None:
                    Change_Status(gb, "Obed", 10)
                    set_scene_expression(gb, "lipbite")
                    Say_Line(gb, renpy.random.choice([
                        _("I can tell. Looking good."),

                        _("That explains a few things~"),

                    ]))

        "Swimming":
            $ Say_Player(_("Swimming. There's something peaceful about it."))
            python:
                Change_Status(ga, "Inbt", 10)
                if gb is not None:
                    Change_Status(gb, "Inbt", 10)
                set_scene_expression(ga, "smug", blush="1")
                Say_Line(ga, renpy.random.choice([
                    _("At the pool? I'll have to join you sometime."),

                    _("Swimming, huh? In those tiny trunks?"),

                ]))
                if gb is not None:
                    set_scene_expression(gb, "lipbite")
                    Say_Line(gb, renpy.random.choice([
                        _("So you're a pool guy. Good to know."),

                        _("Wet and shirtless. Nice hobby~"),

                    ]))

    return

# --- 5. Most extreme thing you've done? ---
label tod_pa_extreme(girls):
    python:
        ga = girls[0] if len(girls) > 0 else None
        gb = girls[1] if len(girls) > 1 else None
        # Find the most extreme act player has done
        _ext_hierarchy = ["creampie", "anal", "reverse_cowgirl", "cowgirl", "sex", "bj", "tj", "hj", "masturbate", "kiss"]
        _ext_names = {
            "creampie": _tl(_("finished inside someone")),
            "anal": _tl(_("anal")), "sex": _tl(_("had sex")), "reverse_cowgirl": _tl(_("sex from behind")), "cowgirl": _tl(_("had a girl ride me")),
            "bj": _tl(_("gotten a blowjob")), "tj": _tl(_("gotten a titjob")), "hj": _tl(_("gotten a handjob")),
            "masturbate": _tl(_("watched someone touch herself")), "kiss": _tl(_("made out")),
        }
        _top_player_act = None
        _top_girl_gid = None

        # Check creampie first
        for _g in ALL_GIRLS:
            if getattr(_g, "CreampieCounts", 0) > 0:
                _top_player_act = "creampie"
                _top_girl_gid = _g.gid
                break

        if _top_player_act is None:
            for _a in _ext_hierarchy[1:]:  # skip creampie, already checked
                for _g in ALL_GIRLS:
                    _g_acts = getattr(_g, "Sex_acts", {})
                    if _g_acts.get(_a, 0) > 0:
                        _top_player_act = _a
                        _top_girl_gid = _g.gid
                        break
                if _top_player_act is not None:
                    break

    if _top_player_act is not None:
        $ _act_desc = _ext_names.get(_top_player_act, _top_player_act)
        $ Say_Player(_("The most extreme? I've... [_act_desc]."))

        # Check if the girl he did it with is present
        python:
            _present_girl = None
            _absent_girl = None
            if ga is not None and _top_girl_gid == ga.gid:
                _present_girl = ga
                _absent_girl = gb
            elif gb is not None and _top_girl_gid == gb.gid:
                _present_girl = gb
                _absent_girl = ga

        if _present_girl is not None and _absent_girl is not None:
            $ _pn = _present_girl.Name
            $ set_scene_expression(_absent_girl, "smug")
            $ Say_Line(_absent_girl, renpy.random.choice([_("Wow... and who was that with?"), _("Wait, with who?!"), _("Spill! Who was it?!")]))
            python:
                Change_Status(_present_girl, "Inbt", 25)
                set_scene_expression(_present_girl, "embarrassed", blush="2")
                Say_Line(_present_girl, renpy.random.choice([
                    _("H-hey! That was only ONE question per round!"),

                    _("Next question! NEXT QUESTION!"),

                    _("Can we PLEASE move on?!"),

                ]))
            $ set_scene_expression(_absent_girl, "laugh")
            $ Say_Line(_absent_girl, renpy.random.choice([_("Oh my god, it was [_pn]?!"), _("The look on her face says everything!"), _("Hahaha, called it!"), _("Wait, HER?! No way!"), _("I'm going to remember this forever.")]))
        elif _present_girl is not None:
            python:
                Change_Status(_present_girl, "Inbt", 15)
                set_scene_expression(_present_girl, "embarrassed", blush="1")
                Say_Line(_present_girl, renpy.random.choice([
                    _("H-hey! Don't just... say it like that!"),

                    _("Next question! NEXT QUESTION!"),

                    _("Can we PLEASE move on?!"),

                ]))
        else:
            python:
                set_scene_expression(ga, "surprised")
                Say_Line(ga, renpy.random.choice([_("Wow, really?"), _("That's... more than I expected."), _("Okay then!")]))
    else:
        $ Say_Player(_("Honestly? Nothing too crazy. Just making out, really."))
        python:
            Say_Line(ga, renpy.random.choice([_("That's sweet, actually."), _("Innocent boy~"), _("Sure, we believe you.")]))
    return

# --- 6. Favorite position? ---
label tod_pa_fav_position(girls):
    python:
        ga = girls[0] if len(girls) > 0 else None
        gb = girls[1] if len(girls) > 1 else None
    menu:
        "What's your favorite position?"

        "Her on top (cowgirl)":
            $ Say_Player(_("When she's on top. Best view in the world."))
            python:
                for _g in girls:
                    if getattr(_g, "FavoriteAct", None) == "cowgirl":
                        Change_Status(_g, "Obed", 15)
                        Change_Status(_g, "Inbt", 15)
                        set_scene_expression(_g, "lipbite", blush="1")
                        Say_Line(_g, renpy.random.choice([_("That's my favorite too~"), _("Great taste."), _("Same here, actually...")]))

        "Reverse cowgirl":
            $ Say_Player(_("From behind. What can I say, I like the view."))
            python:
                for _g in girls:
                    if getattr(_g, "FavoriteAct", None) == "reverse_cowgirl":
                        Change_Status(_g, "Obed", 15)
                        Change_Status(_g, "Inbt", 15)
                        set_scene_expression(_g, "smug", blush="1")
                        Say_Line(_g, renpy.random.choice([_("Interesting~"), _("Good choice."), _("I can work with that.")]))

        "Blowjob":
            $ Say_Player(_("Getting head. I mean, is there a wrong answer?"))
            python:
                for _g in girls:
                    if getattr(_g, "FavoriteAct", None) == "bj":
                        Change_Status(_g, "Obed", 15)
                        Change_Status(_g, "Inbt", 15)
                        set_scene_expression(_g, "sly", blush="1")
                        Say_Line(_g, renpy.random.choice([_("Ha! Called it."), _("Typical~"), _("I do enjoy that...")]))

        "Doggy style":
            $ Say_Player(_("Doggy style. Bent over, from behind. Nothing beats that view."))
            python:
                for _g in girls:
                    if getattr(_g, "FavoriteAct", None) == "doggy":
                        Change_Status(_g, "Obed", 15)
                        Change_Status(_g, "Inbt", 15)
                        set_scene_expression(_g, "lipbite", blush="1")
                        Say_Line(_g, renpy.random.choice([_("Same here. There's something about that angle..."), _("Good choice. I like giving up control like that."), _("The view from my side isn't bad either~")]))

        "Laying Down":
            $ Say_Player(_("When she's laying back and I'm on top. I like being in control."))
            python:
                for _g in girls:
                    if getattr(_g, "FavoriteAct", None) == "laying_down":
                        Change_Status(_g, "Obed", 15)
                        Change_Status(_g, "Inbt", 15)
                        set_scene_expression(_g, "lipbite", blush="1")
                        Say_Line(_g, renpy.random.choice([_("I like that too, actually."), _("Something about being pinned down..."), _("Good. I like when you take charge.")]))

        "Kissing":
            $ Say_Player(_("Just making out, honestly. A good kiss beats everything."))
            python:
                for _g in girls:
                    if getattr(_g, "FavoriteAct", None) == "kiss":
                        Change_Status(_g, "Love", 15)
                        set_scene_expression(_g, "shy", blush="1")
                        Say_Line(_g, renpy.random.choice([_("That's actually really sweet."), _("A man of taste."), _("Same... a good kiss is everything.")]))
                    else:
                        set_scene_expression(_g, "confused")
                        Say_Line(_g, renpy.random.choice([_("Boring..."), _("That's it? Just kissing?"), _("Come on, that can't be your real answer."), _("Really? Nothing more... exciting?")]))

        "I don't have enough experience yet":
            $ Say_Player(_("I haven't done enough to pick a favorite, honestly."))
            python:
                Say_Line(ga, renpy.random.choice([_("Aww, that's okay."), _("Plenty of time to figure it out~")]))

    return

# --- 7. Condom or raw? ---
label tod_pa_condom(girls):
    python:
        ga = girls[0] if len(girls) > 0 else None
        gb = girls[1] if len(girls) > 1 else None
    menu:
        "Do you prefer using a condom, or going raw?"

        "Always condom":
            $ Say_Player(_("Condom. Always. Safety first."))
            python:
                for _g in girls:
                    if hasattr(_g, "has_trait") and _g.has_trait("hate_cum"):
                        Change_Status(_g, "Love", 15)
                        set_scene_expression(_g, "happy")
                        Say_Line(_g, renpy.random.choice([_("Thank god. A man with sense."), _("Finally, someone responsible.")]))
                        _g.discover("discovered_trait_hate_cum")
                    elif hasattr(_g, "has_trait") and _g.has_trait("cum_slut"):
                        set_scene_expression(_g, "confused")
                        Say_Line(_g, renpy.random.choice([_("Boring~"), _("Where's the fun in that?")]))
                        _g.discover("discovered_trait_cum_slut")

        "Raw feels better":
            $ Say_Player(_("Raw. The feeling is on another level."))
            python:
                for _g in girls:
                    if hasattr(_g, "has_trait") and _g.has_trait("cum_slut"):
                        Change_Status(_g, "Obed", 15)
                        Change_Status(_g, "Inbt", 15)
                        set_scene_expression(_g, "lipbite", blush="1")
                        Say_Line(_g, renpy.random.choice([_("Now you're speaking my language~"), _("Right?! It's so much better.")]))
                        _g.discover("discovered_trait_cum_slut")
                    elif hasattr(_g, "has_trait") and _g.has_trait("hate_cum"):
                        Change_Status(_g, "Love", -10)
                        Change_Status(_g, "Inbt", 10)
                        set_scene_expression(_g, "disgusted")
                        Say_Line(_g, renpy.random.choice([_("That's... concerning."), _("Yikes. I hope you're careful at least.")]))

        "Raw... and finishing inside":
            $ Say_Player(_("Raw, and... all the way. Inside."))
            python:
                for _g in girls:
                    if hasattr(_g, "has_trait") and _g.has_trait("cum_slut"):
                        Change_Status(_g, "Obed", 20)
                        set_scene_expression(_g, "lewd", blush="2")
                        Say_Line(_g, renpy.random.choice([
                            _("...Okay, that's really hot."),

                            _("You can't just say that and expect me to stay calm."),

                        ]))
                        _g.discover("discovered_trait_cum_slut")
                    elif hasattr(_g, "has_trait") and _g.has_trait("hate_cum"):
                        Change_Status(_g, "Love", -15)
                        Change_Status(_g, "Inbt", 10)
                        set_scene_expression(_g, "angry")
                        Say_Line(_g, renpy.random.choice([
                            _("That's disgusting. Absolutely not."),

                            _("I'm going to pretend I didn't hear that."),

                        ]))
                        _g.discover("discovered_trait_hate_cum")
                    else:
                        Change_Status(_g, "Inbt", 10)
                        set_scene_expression(_g, "embarrassed", blush="1")

    return

# --- 8. Ever recorded a video? ---
label tod_pa_video(girls):
    python:
        ga = girls[0] if len(girls) > 0 else None
        gb = girls[1] if len(girls) > 1 else None
        _vids = getattr(store.Player, "recorded_videos", [])
        _has_vids = len(_vids) > 0
        _vid_girl_gids = set(v.get("girl_gid", "") for v in _vids) if _has_vids else set()

    if _has_vids:
        $ Say_Player(_("...Yeah. I've recorded something before."))
        python:
            # Only consider consensual videos for embarrassment (she knows about those)
            _consensual_gids = set(v.get("girl_gid", "") for v in _vids if v.get("consensual", False))
            _present_in_vid = None
            _other_v = None
            if ga is not None and ga.gid in _consensual_gids:
                _present_in_vid = ga
                _other_v = gb
            elif gb is not None and gb.gid in _consensual_gids:
                _present_in_vid = gb
                _other_v = ga

        if _present_in_vid is not None:
            $ _pvn = _present_in_vid.Name
            if _other_v is not None:
                $ set_scene_expression(_other_v, "smug")
                $ Say_Line(_other_v, renpy.random.choice([_("Ooh! With who?"), _("Wait, seriously? Who was in it?")]))
            python:
                Change_Status(_present_in_vid, "Inbt", 25)
                set_scene_expression(_present_in_vid, "embarrassed", blush="2")
                Say_Line(_present_in_vid, renpy.random.choice([
                    _("Don't you DARE say my name!"),

                    _("ONE question per turn! MOVE ON!"),

                    _("I swear, if you answer that..."),

                ]))
            if _other_v is not None:
                $ set_scene_expression(_other_v, "laugh")
                $ Say_Line(_other_v, renpy.random.choice([_("Her face is SO red right now!"), _("That reaction is all the answer I need!"), _("Hahaha, called it!"), _("Oh my god, it was [_pvn]?!"), _("I'm going to remember this forever.")]))
        else:
            python:
                set_scene_expression(ga, "surprised")
                Say_Line(ga, renpy.random.choice([_("Wow, really?"), _("Bold of you to admit that.")]))
                if gb is not None:
                    Say_Line(gb, renpy.random.choice([_("I'm both impressed and scared."), _("Who was it with?!")]))
    else:
        $ Say_Player(_("Nah, never recorded anything."))
        python:
            Say_Line(ga, renpy.random.choice([_("Sure, we believe you."), _("That's what they all say.")]))
    return

# --- 9. Do you like it rough during sex? ---
label tod_pa_rough(girls):
    python:
        ga = girls[0] if len(girls) > 0 else None
        gb = girls[1] if len(girls) > 1 else None
    menu:
        "Do you like being rough during sex?"

        "Yeah, I like it intense":
            $ Say_Player(_("I like it rough. Pulling hair, being dominant. The works."))
            python:
                for _g in girls:
                    # him dominant, to a femdom (docs/plan_femdom.md 7): a challenge, never Obed for her
                    if trait_is_veteran(_g, "femdom"):
                        Change_Status(_g, "Inbt", 10)
                        set_scene_expression(_g, "smug")
                        Say_Line(_g, renpy.random.choice([
                            _("Dominant? Cute. We'll see how long that lasts with me."),
                            _("Pulling hair is fine. Being in charge? That part's taken."),
                        ]))
                        _g.discover("discovered_trait_femdom")
                        print("[FEMDOM] %s answers the player's 'rough and dominant' as a femdom" % _g.gid)
                    elif hasattr(_g, "has_trait") and _g.has_trait("hardcore_sex"):
                        Change_Status(_g, "Obed", 15)
                        set_scene_expression(_g, "lewd", blush="1")
                        Say_Line(_g, renpy.random.choice([
                            _("Now THAT is what I like to hear."),

                            _("Finally, a man who gets it."),

                            _("...I think I like you even more now."),

                        ]))
                        _g.discover("discovered_trait_hardcore_sex")
                    elif hasattr(_g, "has_trait") and _g.has_trait("cute_sex"):
                        set_scene_expression(_g, "uncomfortable")
                        Say_Line(_g, renpy.random.choice([
                            _("Oh... that's a bit much for me."),

                            _("I prefer things a little softer, personally."),

                        ]))
                        _g.discover("discovered_trait_cute_sex")

        "No, I prefer being gentle":
            $ Say_Player(_("I'm more of a gentle guy. Slow, intimate. Making it mean something."))
            python:
                for _g in girls:
                    if hasattr(_g, "has_trait") and _g.has_trait("cute_sex"):
                        Change_Status(_g, "Love", 15)
                        set_scene_expression(_g, "shy", blush="1")
                        Say_Line(_g, renpy.random.choice([
                            _("That's... really sweet. I like that."),

                            _("You had me at 'slow and intimate'."),

                            _("That's exactly how I feel about it too."),

                        ]))
                        _g.discover("discovered_trait_cute_sex")
                    elif hasattr(_g, "has_trait") and _g.has_trait("hardcore_sex"):
                        set_scene_expression(_g, "confused")
                        Say_Line(_g, renpy.random.choice([
                            _("Hmm. That's a little tame for my taste."),

                            _("Boring~ But I respect it."),

                        ]))
                        _g.discover("discovered_trait_hardcore_sex")

        "Depends on the mood":
            $ Say_Player(_("Depends on the mood. Sometimes gentle, sometimes not."))
            python:
                Say_Line(ga, renpy.random.choice([_("Versatile. I can respect that."), _("Best of both worlds, huh?")]))
                if gb is not None:
                    Say_Line(gb, renpy.random.choice([_("That's a safe answer."), _("Diplomatic. I see you.")]))

    return

# --- 10. Who made you feel better, me or her? ---
label tod_pa_who_better(asker, other):
    $ _an = asker.Name
    $ _on = other.Name

    menu:
        "Who made you feel better... [_an] or [_on]?"

        "[_an]":
            $ Say_Player(_("[_an], honestly. Something about the way you do it just... hits different."))
            python:
                Change_Status(asker, "Love", 20)
                Change_Status(asker, "Obed", 15)
                set_scene_expression(asker, "smug", blush="1")
                Say_Line(asker, renpy.random.choice([
                    _("I knew it. I could tell by the way you looked at me."),

                    _("Ha! See? I told you."),

                    _("That... actually means a lot. Thank you."),

                ]))
                set_scene_expression(other, "angry")
                Say_Line(other, renpy.random.choice([
                    _("Wow. Okay. That stings a little."),

                    _("Right in front of me? Really?"),

                    _("I'll just pretend I didn't hear that."),

                    _("Hmph. Maybe I just need another chance to prove myself."),

                ]))

        "[_on]":
            $ Say_Player(_("[_on], no offense. It was just... something else."))
            python:
                Change_Status(other, "Love", 20)
                Change_Status(other, "Obed", 15)
                set_scene_expression(other, "happy", blush="1")
                Say_Line(other, renpy.random.choice([
                    _("Oh? Well... thank you for being honest~"),

                    _("Interesting. Very interesting."),

                    _("I'm flattered. Truly."),

                ]))
                set_scene_expression(asker, "angry")
                Say_Line(asker, renpy.random.choice([
                    _("...Excuse me?"),

                    _("You did NOT just say that."),

                    _("I'm sitting right here, you know."),

                    _("Fine. I'll just have to step up my game then."),

                ]))

        "You're both amazing, I can't choose":
            $ Say_Player(_("I honestly can't pick. You're both incredible in your own way."))
            python:
                Change_Status(asker, "Love", 10)
                Change_Status(other, "Love", 10)
                set_scene_expression(asker, "sly")
                Say_Line(asker, renpy.random.choice([
                    _("Smooth answer. Too smooth."),

                    _("That's a cop-out and you know it."),

                    _("Hmm... I'll accept that. For now."),

                ]))
                set_scene_expression(other, "sly")
                Say_Line(other, renpy.random.choice([
                    _("Diplomatic. I see what you're doing."),

                    _("At least you didn't pick her over me."),

                    _("I'll take that as a compliment."),

                ]))

    return

# --- 11. Craziest place you'd do it? ---
label tod_pa_craziest_place(girls):
    python:
        ga = girls[0] if len(girls) > 0 else None
        gb = girls[1] if len(girls) > 1 else None
    menu:
        "Where's the craziest place you'd do it?"

        "The pool at night":
            $ Say_Player(_("The pool. Late at night. Water, moonlight, nobody around."))
            python:
                for _g in girls:
                    Change_Status(_g, "Inbt", 10)
                set_scene_expression(ga, "shy", blush="1")
                Say_Line(ga, renpy.random.choice([_("That's actually kind of romantic."), _("The pool? At night? ...I'd be down.")]))
                if gb is not None:
                    Say_Line(gb, renpy.random.choice([_("Interesting choice."), _("I can picture it. Not bad.")]))

        "The classroom":
            $ Say_Player(_("The classroom. During a break. Door unlocked. The risk is the thrill."))
            python:
                for _g in girls:
                    Change_Status(_g, "Inbt", 15)
                set_scene_expression(ga, "surprised")
                Say_Line(ga, renpy.random.choice([_("That's insane. ...I kind of love it."), _("You're crazy. But also kind of hot.")]))
                if gb is not None:
                    set_scene_expression(gb, "scared")
                    Say_Line(gb, renpy.random.choice([_("What if someone walks in?!"), _("Risky. Very risky. ...Go on.")]))

        "The showers":
            $ Say_Player(_("The showers. Steam, hot water, slippery tiles... dangerous but worth it."))
            python:
                for _g in girls:
                    Change_Status(_g, "Inbt", 10)
                set_scene_expression(ga, "smug", blush="1")
                Say_Line(ga, renpy.random.choice([_("The acoustics in there though..."), _("Slippery. Could be fun or a disaster.")]))

        "Nowhere crazy, just a bed":
            $ Say_Player(_("A bed. I'm a simple man."))
            python:
                set_scene_expression(ga, "confused")
                Say_Line(ga, renpy.random.choice([_("Boring!"), _("Classic but boring."), _("Come on, live a little!")]))
                if gb is not None:
                    Say_Line(gb, renpy.random.choice([_("Safe answer."), _("Boooo!")]))

    return

# --- 12. Do you touch yourself? ---
label tod_pa_touch_yourself(girls):
    python:
        ga = girls[0] if len(girls) > 0 else None
        gb = girls[1] if len(girls) > 1 else None
    menu:
        "Do you touch yourself?"

        "Yeah, of course":
            $ Say_Player(_("Yeah. Who doesn't? It's natural."))
            python:
                for _g in girls:
                    Change_Status(_g, "Inbt", 10)
                set_scene_expression(ga, "sly")
                Say_Line(ga, renpy.random.choice([_("Honest. I respect that."), _("Ha! At least you're not pretending.")]))
                if gb is not None:
                    Say_Line(gb, renpy.random.choice([_("Fair enough."), _("Bold of you to just say it like that.")]))

        "Only when I think about someone specific":
            $ Say_Player(_("Only when I'm thinking about someone... specific."))
            python:
                for _g in girls:
                    Change_Status(_g, "Inbt", 15)
                    Change_Status(_g, "Love", 5)
                set_scene_expression(ga, "embarrassed", blush="1")
                Say_Line(ga, renpy.random.choice([_("Oh? Someone specific? Do tell~"), _("Why are you looking at me when you say that?")]))
                if gb is not None:
                    set_scene_expression(gb, "shy", blush="1")
                    Say_Line(gb, renpy.random.choice([_("I feel like I should be flattered or concerned."), _("Don't look at me like that...")]))

        "That's private!":
            $ Say_Player(_("I'm not answering that. Next question!"))
            python:
                set_scene_expression(ga, "laugh")
                Say_Line(ga, renpy.random.choice([_("Coward! That's basically a yes!"), _("Your face says it all.")]))
                if gb is not None:
                    set_scene_expression(gb, "smug")
                    Say_Line(gb, renpy.random.choice([_("The silence speaks volumes."), _("Haha, guilty!")]))

    return

# --- 13. What's your biggest fetish? ---
label tod_pa_biggest_fetish(girls):
    python:
        ga = girls[0] if len(girls) > 0 else None
        gb = girls[1] if len(girls) > 1 else None
    menu:
        "What's your biggest fetish?"

        "Creampies":
            $ Say_Player(_("Finishing inside. No pulling out. The closeness, the heat... everything."))
            python:
                for _g in girls:
                    if hasattr(_g, "has_trait") and _g.has_trait("cum_slut"):
                        Change_Status(_g, "Obed", 20)
                        Change_Status(_g, "Inbt", 15)
                        set_scene_expression(_g, "lewd", blush="2")
                        Say_Line(_g, renpy.random.choice([_("...That's my fetish too."), _("Okay, I need a moment after hearing that.")]))
                        _g.discover("discovered_trait_cum_slut")
                    elif hasattr(_g, "has_trait") and _g.has_trait("hate_cum"):
                        Change_Status(_g, "Inbt", 5)
                        set_scene_expression(_g, "disgusted")
                        Say_Line(_g, renpy.random.choice([_("Absolutely not."), _("That's disgusting. Hard pass.")]))
                        _g.discover("discovered_trait_hate_cum")
                    else:
                        Change_Status(_g, "Inbt", 10)
                        set_scene_expression(_g, "embarrassed", blush="1")

        "Being rough and dominant":
            $ Say_Player(_("Being dominant. Taking control. Hair pulling, pinning down, the works."))
            python:
                for _g in girls:
                    # him taking control, to a femdom (docs/plan_femdom.md 7): a challenge, never Obed for her
                    if trait_is_veteran(_g, "femdom"):
                        Change_Status(_g, "Inbt", 10)
                        set_scene_expression(_g, "smug")
                        Say_Line(_g, renpy.random.choice([
                            _("You, taking control? Adorable. I'd have you on your back in a minute."),
                            _("Try that with me sometime. I dare you."),
                        ]))
                        _g.discover("discovered_trait_femdom")
                        print("[FEMDOM] %s answers the player's 'dominant' fetish as a femdom" % _g.gid)
                    elif hasattr(_g, "has_trait") and _g.has_trait("hardcore_sex"):
                        Change_Status(_g, "Obed", 20)
                        Change_Status(_g, "Inbt", 15)
                        set_scene_expression(_g, "lipbite", blush="1")
                        Say_Line(_g, renpy.random.choice([_("...Yes. Yes please."), _("You just became ten times more attractive.")]))
                        _g.discover("discovered_trait_hardcore_sex")
                    elif hasattr(_g, "has_trait") and _g.has_trait("cute_sex"):
                        set_scene_expression(_g, "scared")
                        Say_Line(_g, renpy.random.choice([_("That's a bit scary..."), _("I prefer something softer.")]))
                        _g.discover("discovered_trait_cute_sex")
                    else:
                        Change_Status(_g, "Inbt", 10)
                        set_scene_expression(_g, "surprised")

        "Gentle and romantic":
            $ Say_Player(_("The intimate stuff. Eye contact, slow pace, feeling connected."))
            python:
                for _g in girls:
                    if hasattr(_g, "has_trait") and _g.has_trait("cute_sex"):
                        Change_Status(_g, "Love", 20)
                        set_scene_expression(_g, "shy", blush="1")
                        Say_Line(_g, renpy.random.choice([_("That's beautiful..."), _("You just made my heart skip a beat.")]))
                        _g.discover("discovered_trait_cute_sex")
                    elif hasattr(_g, "has_trait") and _g.has_trait("hardcore_sex"):
                        set_scene_expression(_g, "confused")
                        Say_Line(_g, renpy.random.choice([_("Yawn."), _("Sweet, but boring.")]))
                        _g.discover("discovered_trait_hardcore_sex")
                    else:
                        Change_Status(_g, "Love", 10)
                        set_scene_expression(_g, "happy")

        "Being filmed":
            $ Say_Player(_("Recording it. Watching it back. Having a souvenir of the moment."))
            python:
                for _g in girls:
                    if hasattr(_g, "has_trait") and _g.has_trait("camera_lover"):
                        Change_Status(_g, "Obed", 15)
                        Change_Status(_g, "Inbt", 15)
                        set_scene_expression(_g, "smug", blush="1")
                        Say_Line(_g, renpy.random.choice([_("I knew you were my kind of person."), _("The camera loves me. I'd be down~")]))
                        _g.discover("discovered_trait_camera_lover")
                    elif hasattr(_g, "has_trait") and _g.has_trait("camera_hater"):
                        set_scene_expression(_g, "angry")
                        Say_Line(_g, renpy.random.choice([_("If you ever point a camera at me, I will end you."), _("That's a dealbreaker.")]))
                        _g.discover("discovered_trait_camera_hater")
                    else:
                        Change_Status(_g, "Inbt", 10)
                        set_scene_expression(_g, "surprised")

        "Doing it in public":
            $ Say_Player(_("The risk of getting caught. Public places. The adrenaline rush."))
            python:
                for _g in girls:
                    if hasattr(_g, "has_trait") and _g.has_trait("public_fetish"):
                        Change_Status(_g, "Obed", 15)
                        Change_Status(_g, "Inbt", 15)
                        set_scene_expression(_g, "lipbite", blush="1")
                        Say_Line(_g, renpy.random.choice([_("Okay, we need to hang out more."), _("A man after my own heart~")]))
                        _g.discover("discovered_trait_public_fetish")
                    elif hasattr(_g, "has_trait") and _g.has_trait("public_shy"):
                        set_scene_expression(_g, "scared")
                        Say_Line(_g, renpy.random.choice([_("Absolutely not. Never."), _("That's my worst nightmare.")]))
                        _g.discover("discovered_trait_public_shy")
                    else:
                        Change_Status(_g, "Inbt", 10)

        "Titjobs / Blowjobs":
            $ Say_Player(_("Oral stuff. Titjobs, blowjobs. There's something about it."))
            python:
                for _g in girls:
                    Change_Status(_g, "Inbt", 10)
                Say_Line(ga, renpy.random.choice([_("Simple tastes. I can respect that."), _("At least you know what you like.")]))
                if gb is not None:
                    Say_Line(gb, renpy.random.choice([_("Classic."), _("Not the worst answer.")]))

    return

# --- Player: Ever had a condom break? ---
label tod_pa_condom_break(girls):
    python:
        ga = girls[0] if len(girls) > 0 else None
        gb = girls[1] if len(girls) > 1 else None
    menu:
        "Has a condom ever broken on you during sex?"

        "Yeah, it happened once":
            $ Say_Player(_("Yeah... it broke once. I panicked. She panicked. Good times."))
            python:
                for _g in girls:
                    if hasattr(_g, "has_trait") and _g.has_trait("cum_slut"):
                        Change_Status(_g, "Inbt", 15)
                        set_scene_expression(_g, "lipbite", blush="1")
                        Say_Line(_g, renpy.random.choice([_("And? Did you keep going?"), _("That's kind of hot, honestly.")]))
                        _g.discover("discovered_trait_cum_slut")
                    elif hasattr(_g, "has_trait") and _g.has_trait("hate_cum"):
                        set_scene_expression(_g, "scared")
                        Say_Line(_g, renpy.random.choice([_("That's terrifying. I'd lose it."), _("And you just... kept going?! Please say no.")]))
                        _g.discover("discovered_trait_hate_cum")
                    else:
                        Change_Status(_g, "Inbt", 10)
                        set_scene_expression(_g, "surprised")
                        Say_Line(_g, renpy.random.choice([_("That must have been scary."), _("Yikes. What did you do?")]))

        "No, never":
            $ Say_Player(_("Nope. I'm careful with that stuff. Always check."))
            python:
                for _g in girls:
                    if hasattr(_g, "has_trait") and _g.has_trait("cute_sex"):
                        Change_Status(_g, "Love", 5)
                        set_scene_expression(_g, "happy")
                        Say_Line(_g, renpy.random.choice([_("That's really responsible."), _("Good. I like someone who's careful.")]))
                    else:
                        Say_Line(_g, renpy.random.choice([_("Smart."), _("Fair enough.")]))

        "I don't use condoms":
            $ Say_Player(_("I usually go raw. So... no broken condoms to report."))
            python:
                for _g in girls:
                    if hasattr(_g, "has_trait") and _g.has_trait("cum_slut"):
                        Change_Status(_g, "Obed", 15)
                        Change_Status(_g, "Inbt", 15)
                        set_scene_expression(_g, "lewd", blush="1")
                        Say_Line(_g, renpy.random.choice([_("Oh? Interesting..."), _("A man who knows what he wants~")]))
                    elif hasattr(_g, "has_trait") and _g.has_trait("hate_cum"):
                        set_scene_expression(_g, "angry")
                        Say_Line(_g, renpy.random.choice([_("That's incredibly irresponsible."), _("I would NEVER let that happen.")]))
                        _g.discover("discovered_trait_hate_cum")
                    else:
                        Change_Status(_g, "Inbt", 10)
                        set_scene_expression(_g, "surprised")
                        Say_Line(_g, renpy.random.choice([_("Bold."), _("Risky move, but okay.")]))

    return

# --- Player: Would you do something sexual for money? ---
label tod_pa_financial(girls):
    python:
        ga = girls[0] if len(girls) > 0 else None
        gb = girls[1] if len(girls) > 1 else None
    menu:
        "Would you do something sexual for money?"

        "If the price is right, sure":
            $ Say_Player(_("Everyone has a price. I'm not gonna pretend otherwise."))
            python:
                for _g in girls:
                    if hasattr(_g, "has_trait") and _g.has_trait("hardcore_sex"):
                        Change_Status(_g, "Inbt", 10)
                        set_scene_expression(_g, "sly")
                        Say_Line(_g, renpy.random.choice([_("Honest. I respect that."), _("At least you're not a hypocrite.")]))
                    elif hasattr(_g, "has_trait") and _g.has_trait("cute_sex"):
                        set_scene_expression(_g, "sad")
                        Say_Line(_g, renpy.random.choice([_("That's kind of sad, honestly..."), _("I don't like that answer.")]))
                    else:
                        Change_Status(_g, "Inbt", 5)
                        set_scene_expression(_g, "surprised")
                        Say_Line(_g, renpy.random.choice([_("Wow. Just like that?"), _("At least you're honest about it.")]))

        "No, never":
            $ Say_Player(_("No. Some things shouldn't have a price tag."))
            python:
                for _g in girls:
                    if hasattr(_g, "has_trait") and _g.has_trait("cute_sex"):
                        Change_Status(_g, "Love", 10)
                        set_scene_expression(_g, "happy")
                        Say_Line(_g, renpy.random.choice([_("That's really sweet."), _("Good answer. I agree completely.")]))
                    elif hasattr(_g, "has_trait") and _g.has_trait("cum_slut"):
                        set_scene_expression(_g, "confused")
                        Say_Line(_g, renpy.random.choice([_("Boring. But noble, I guess."), _("Your loss~")]))
                    else:
                        Change_Status(_g, "Love", 5)
                        Say_Line(_g, renpy.random.choice([_("Respect."), _("Good to know.")]))

        "I'd pay, not sell":
            $ Say_Player(_("I wouldn't sell. But I might buy. Is that worse?"))
            python:
                for _g in girls:
                    _fin_t = getattr(_g, "_financial_times", 0)
                    if _fin_t > 0:
                        Change_Status(_g, "Inbt", 15)
                        set_scene_expression(_g, "embarrassed", blush="1")
                        Say_Line(_g, renpy.random.choice([_("...Noted."), _("Interesting perspective.")]))
                    elif hasattr(_g, "has_trait") and _g.has_trait("hardcore_sex"):
                        Change_Status(_g, "Inbt", 10)
                        set_scene_expression(_g, "sly")
                        Say_Line(_g, renpy.random.choice([_("At least you know which side of the deal you're on."), _("Honest. Dark, but honest.")]))
                    elif hasattr(_g, "has_trait") and _g.has_trait("cute_sex"):
                        set_scene_expression(_g, "uncomfortable")
                        Say_Line(_g, renpy.random.choice([_("That's... kind of creepy."), _("I don't know how to feel about that.")]))
                    else:
                        Change_Status(_g, "Inbt", 5)
                        set_scene_expression(_g, "surprised")
                        Say_Line(_g, renpy.random.choice([_("Well, that took a turn."), _("Bold answer. Very bold.")]))

    return

# --- Player: Ever done a threesome? ---
label tod_pa_threesome(girls):
    python:
        ga = girls[0] if len(girls) > 0 else None
        gb = girls[1] if len(girls) > 1 else None
    menu:
        "Ever done a threesome?"

        "Yeah, I've been in one":
            $ Say_Player(_("Yeah... it happened. No regrets."))
            python:
                _both_involved = gb is not None and ga.get_history_with(gb.gid, "threesome") > 0
                if _both_involved:
                    set_scene_expression(ga, "embarrassed", blush="2")
                    Say_Line(ga, renpy.random.choice([_("...Are you talking about what I think you're talking about?"), _("We're really doing this right now?")]))
                    set_scene_expression(gb, "embarrassed", blush="2")
                    Say_Line(gb, renpy.random.choice([_("Well, this just got awkward."), _("I remember. Do you?")]))
                else:
                    for _g in girls:
                        _g_three = any(_g.get_history_with(_o.gid, "threesome") > 0 for _o in store.ALL_GIRLS if _o.gid != _g.gid)
                        if _g_three:
                            Change_Status(_g, "Inbt", 15)
                            set_scene_expression(_g, "embarrassed", blush="1")
                            Say_Line(_g, renpy.random.choice([_("Was I... involved in that?"), _("Wait, with who?!")]))
                        elif hasattr(_g, "has_trait") and _g.has_trait("exhibitionist"):
                            Change_Status(_g, "Inbt", 10)
                            set_scene_expression(_g, "smug")
                            Say_Line(_g, renpy.random.choice([_("And you didn't invite me?"), _("Details. Now.")]))
                        else:
                            Change_Status(_g, "Inbt", 10)
                            set_scene_expression(_g, "surprised")
                            Say_Line(_g, renpy.random.choice([_("Wow. Bold confession."), _("And you just drop that casually?")]))

        "No, never":
            $ Say_Player(_("Nope. One person at a time is plenty for me."))
            python:
                for _g in girls:
                    if hasattr(_g, "has_trait") and _g.has_trait("cute_sex"):
                        Change_Status(_g, "Love", 5)
                        set_scene_expression(_g, "happy")
                        Say_Line(_g, renpy.random.choice([_("Good answer. Quality over quantity."), _("Smart. It's more personal that way.")]))
                    elif hasattr(_g, "has_trait") and _g.has_trait("exhibitionist"):
                        set_scene_expression(_g, "confused")
                        Say_Line(_g, renpy.random.choice([_("Boring~"), _("You're missing out.")]))
                    else:
                        Say_Line(_g, renpy.random.choice([_("That's fair."), _("Reasonable.")]))

        "Not yet, but I'm open to it":
            $ Say_Player(_("Never happened. But if the right people were involved... I wouldn't say no."))
            python:
                for _g in girls:
                    _g_three = any(_g.get_history_with(_o.gid, "threesome") > 0 for _o in store.ALL_GIRLS if _o.gid != _g.gid)
                    if _g_three:
                        Change_Status(_g, "Inbt", 15)
                        set_scene_expression(_g, "shy", blush="1")
                        Say_Line(_g, renpy.random.choice([_("...Interesting."), _("Sounds like you're looking at me.")]))
                    elif hasattr(_g, "has_trait") and _g.has_trait("exhibitionist"):
                        Change_Status(_g, "Obed", 10)
                        set_scene_expression(_g, "lipbite")
                        Say_Line(_g, renpy.random.choice([_("Same~"), _("Oh? Tell me more.")]))
                    elif hasattr(_g, "has_trait") and _g.has_trait("cute_sex"):
                        set_scene_expression(_g, "uncomfortable")
                        Say_Line(_g, renpy.random.choice([_("That's... a lot to think about."), _("I don't think I could handle that.")]))
                    else:
                        Change_Status(_g, "Inbt", 5)
                        set_scene_expression(_g, "sly")
                        Say_Line(_g, renpy.random.choice([_("Bold, saying that with both of us here."), _("At least you're honest about it.")]))

    return

# --- 16. What breast size do you prefer? ---
label tod_pa_bust_pref(girls):
    python:
        _bp_girls = list(girls)
        _bp_npc = getattr(store, "_h_npc", None)
        _bp_memory_reacted = set()

    # Girls who already know the answer react before the question
    python:
        _bp_already = [g for g in _bp_girls if getattr(g, "knows_player_bust_pref", None)]
    if _bp_already:
        python:
            for _bp_kg in _bp_already:
                set_scene_expression(_bp_kg, "smirk")
                Say_Line(_bp_kg, renpy.random.choice([
                    _("Oh, I already know the answer to this one~"),
                    _("I remember what you said last time. Let's see if you changed your mind."),
                    _("Haven't we been through this already?"),
                ]))

    menu:
        "What breast size do you prefer?"

        "The bigger the better!":
            $ Say_Player(_("Honestly? The bigger the better. I'm a simple man."))
            $ _bp_pick = "large"

        "Medium sizes please me":
            $ Say_Player(_("Something in the middle. Not too big, not too small. Just right."))
            $ _bp_pick = "medium"

        "I like girls more modest in that area...":
            $ Say_Player(_("I actually prefer smaller. There's something about a more modest look."))
            $ _bp_pick = "small"

        "Boobs are boobs! Doesn't matter!":
            $ Say_Player(_("Boobs are boobs! Every size is great. I'm not picky."))
            $ _bp_pick = "any"

    # Girls who already knew react to same/changed answer
    if _bp_already:
        python:
            for _bp_kg in _bp_already:
                _bp_old_pref = _bp_kg.knows_player_bust_pref
                if _bp_pick == "any" and _bp_old_pref:
                    set_scene_expression(_bp_kg, "angry")
                    Say_Line(_bp_kg, renpy.random.choice([
                        _("Last time you had an actual answer. Now you're dodging?"),
                        _("Oh, so NOW you don't have a preference? Sure."),
                    ]))
                    Change_Status(_bp_kg, "Obed", -20)
                    _bp_memory_reacted.add(_bp_kg.gid)
                elif _bp_pick == _bp_old_pref:
                    set_scene_expression(_bp_kg, "sly")
                    Say_Line(_bp_kg, renpy.random.choice([
                        _("Told you I remembered."),
                        _("Same answer. At least you're consistent."),
                    ]))
                else:
                    set_scene_expression(_bp_kg, "surprised")
                    Say_Line(_bp_kg, renpy.random.choice([
                        _("Wait, you changed your mind? Last time you said something different!"),
                        _("That's not what you said before! Did your taste change?"),
                    ]))

    # Girls present remember the player's preference
    python:
        for _bp_g in _bp_girls:
            _bp_g.knows_player_bust_pref = _bp_pick
            print("[TOD] %s now knows player prefers bust=%s" % (_bp_g.gid, _bp_pick))

    python:
        for _bp_g in _bp_girls:
            _bp_bust = getattr(_bp_g, "bust", "medium")
            _bp_matched = (_bp_pick == "any" or _bp_pick == _bp_bust)

            if _bp_pick == "any":
                if _bp_g.gid in _bp_memory_reacted:
                    continue
                set_scene_expression(_bp_g, "angry", eyes="eyes_side")
                Say_Line(_bp_g, renpy.random.choice([
                    _("Wow. What a non-answer."),
                    _("That's the most boring thing you could have said."),
                    _("So you don't even care? Cool."),
                ]))
                Change_Status(_bp_g, "Obed", -20)

            elif _bp_matched:
                set_scene_expression(_bp_g, "embarrassed", blush="1")
                if _bp_bust == "large":
                    Say_Line(_bp_g, renpy.random.choice([
                        _("Well... you're welcome."),
                        _("I knew you were looking!"),
                        _("At least you're honest about it~"),
                    ]))
                elif _bp_bust == "medium":
                    Say_Line(_bp_g, renpy.random.choice([
                        _("Good taste. I approve."),
                        _("See? Perfect balance."),
                        _("I always knew you had good eyes."),
                    ]))
                else:
                    Say_Line(_bp_g, renpy.random.choice([
                        _("R-really? You mean that?"),
                        _("That's... actually really sweet."),
                        _("Most people don't say that. Thanks."),
                    ]))
                Change_Status(_bp_g, "Love", 15)
                Change_Status(_bp_g, "Obed", 10)
                if _bp_bust == "small" and not girl_has_pose(_bp_g, "titjob"):
                    Say_Line(_bp_g, renpy.random.choice([
                        _("You... you really mean that? That makes me so happy."),
                        _("I always felt bad about my size. Thank you for saying that."),
                    ]))
                    Change_Status(_bp_g, "Love", 5)

            else:
                set_scene_expression(_bp_g, "sad", eyes="eyes_side")
                if _bp_bust == "large":
                    Say_Line(_bp_g, renpy.random.choice([
                        _("Oh. So mine are... too much?"),
                        _("Wow. These aren't good enough for you?"),
                        _("Noted. I'll just... sit here with my huge disappointments."),
                    ]))
                elif _bp_bust == "medium":
                    Say_Line(_bp_g, renpy.random.choice([
                        _("So I'm just... average to you?"),
                        _("Great. Not big enough, not small enough."),
                        _("I see. Middle of the road. Cool."),
                    ]))
                else:
                    Say_Line(_bp_g, renpy.random.choice([
                        _("So... mine aren't enough for you."),
                        _("Okay. I get it."),
                        _("Well, sorry I can't compete."),
                    ]))
                Change_Status(_bp_g, "Love", -5)
                if _bp_bust == "small" and not girl_has_pose(_bp_g, "titjob"):
                    set_scene_expression(_bp_g, "looking_down")
                    Say_Line(_bp_g, renpy.random.choice([
                        _("I knew it. I'll never be enough."),
                        _("Maybe I should just stop trying..."),
                    ]))
                    Change_Status(_bp_g, "Love", -5)

            # If she has an NPC partner and the player picked her type, raise suspicion
            if _bp_matched and _bp_pick != "any" and _bp_g.has_npc_partner():
                _bp_g_npc = get_npc_partner_for(_bp_g)
                if _bp_g_npc and _bp_g_npc == _bp_npc:
                    Change_NPC_Status(_bp_g_npc, "suspicion", 8)

    return
