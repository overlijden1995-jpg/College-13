## pregnancy_discovery.rpy — Phase 5: Discovery Event + Player Choices
## Girl discovers pregnancy, confronts player, player makes a choice.
## Every per-girl chain ends in an `else:` = the "_default" pool: a girl with no scene of her own yet still
## speaks and still gets the stat changes of his answer. A new girl gets her own branch in each chain.

# ============================================================
# MAIN DISCOVERY LABEL
# ============================================================

label _pregnancy_discovery:
    python:
        _disc_gid = store._pregnancy_discovery_pending
        _disc_girl = GIRL_BY_ID.get(_disc_gid)
        if not _disc_girl:
            store._pregnancy_discovery_pending = None
            print("[PREGNANCY] discovery: invalid gid %s, clearing" % _disc_gid)
            renpy.return_statement()

        _disc_slept = getattr(_disc_girl, "_slept_with_player_tonight", False)
        _disc_dating = _disc_girl.is_dating_player()
        _disc_has_npc = hasattr(_disc_girl, "has_npc_partner") and _disc_girl.has_npc_partner()
        _disc_has_fetish = _disc_girl.has_trait("pregnancy_fetish")
        _disc_has_fear = _disc_girl.has_trait("pregnancy_fear")
        _disc_is_lesbian = _disc_girl.has_trait("lesbian")
        _disc_is_blackmail = getattr(_disc_girl, "_blackmail_leverage", 0) >= 2
        # True once a branch of his answer ENDS the conversation (she walks out, runs out, throws him out):
        # Step 5 then flags the partner confrontation without her coming back to say three calm lines
        _disc_she_left = False

    # --- Step 1: Morning narration (sleepover check) ---
    if _disc_slept:
        python:
            _others_slept = sum(1 for _og in ALL_GIRLS if _og.gid != _disc_gid and getattr(_og, "_slept_with_player_tonight", False))
        if _others_slept > 0:
            "You wake up alone. The bed is empty, and that's unusual."
        else:
            "You wake up, but [_disc_girl.Name] is not in the room. Her side of the bed is still warm."

    # --- Step 2: Girl arrives ---
    if _disc_has_fetish:
        "[_disc_girl.Name] comes in with a strange expression. Is she... smiling?"
    elif _disc_slept:
        "The door opens. [_disc_girl.Name] walks in holding something behind her back. Her eyes are red."
    else:
        "[_disc_girl.Name] knocks on your door. When you open it, she pushes past you without a word. She's holding something behind her back."

    # --- Step 3: Per-girl emotional scene. She WANTED this (pregnancy_fetish) = her own, happy scene:
    #     the fear monologues below would contradict everything she says during sex ---
    if _disc_has_fetish:
        $ _disc_wanted_label = _PREG_DISCOVERY_WANTED.get(_disc_gid, _PREG_DISCOVERY_WANTED["_default"])
        $ print("[PREGNANCY] %s: discovery scene = wanted (%s)" % (_disc_gid, _disc_wanted_label))
        call expression _disc_wanted_label pass (_disc_girl) from _call_preg_disc_wanted
        # she just told him she had been hoping for it
        $ _disc_girl.discover("discovered_trait_pregnancy_fetish")
        $ unlock_achievement("baby_fever")
    elif _disc_gid == "gwen":
        call _pregnancy_discovery_gwen(_disc_girl) from _call_preg_disc_gwen
    elif _disc_gid == "rogue":
        call _pregnancy_discovery_rogue(_disc_girl) from _call_preg_disc_rogue
    elif _disc_gid == "ntw":
        call _pregnancy_discovery_ntw(_disc_girl) from _call_preg_disc_ntw
    elif _disc_gid == "tenny":
        call _pregnancy_discovery_tenny(_disc_girl) from _call_preg_disc_tenny
    elif preg_own_lines(_disc_girl, "discovery"):
        call _pregnancy_discovery_own(_disc_girl) from _call_preg_disc_own
    else:
        call _pregnancy_discovery_default(_disc_girl) from _call_preg_disc_default

    # --- Trait addendum lines ---
    if _disc_has_npc and not _disc_dating:
        python:
            # _PREG_PARTNER_ADDENDUM(_WANTED): (line, face); she wanted the baby = she only remembers him, no drama
            _pa_pool = _PREG_PARTNER_ADDENDUM_WANTED if _disc_has_fetish else _PREG_PARTNER_ADDENDUM
            _pa_line, _pa_face = _pa_pool.get(_disc_gid, _pa_pool["_default"])
            _pa_line = _format_partner_line(_disc_girl, _pa_line)
            print("[PREGNANCY] %s: partner addendum (%s), partner=%s" % (
                _disc_gid, "wanted" if _disc_has_fetish else "worried", _disc_girl.partner_name()))
        if _disc_has_fetish:
            $ Narration(_("Then something else crosses her mind."))
        $ set_scene_expression(_disc_girl, _pa_face, blush=0)
        $ Say_Line(_disc_girl, _pa_line)

    if _disc_is_lesbian and not _disc_has_npc:
        if _disc_has_fetish:
            $ set_scene_expression(_disc_girl, "perplexed", blush=0)
            $ Say_Line(_disc_girl, _("I always wanted to be a mom. I just never pictured a guy being part of how it happened."))
        else:
            $ set_scene_expression(_disc_girl, "sad")
            $ Say_Line(_disc_girl, _("I'm not even straight. This wasn't supposed to be possible for someone like me."))

    if _disc_is_blackmail:
        if _disc_has_fetish:
            # she wanted a baby, not the leverage it came with (same conflict as the "_coerced_pregnancy_fetish" tease pools)
            $ set_scene_expression(_disc_girl, "serious", blush=0)
            $ Say_Line(_disc_girl, _("I hate how this started. I hate what you hold over me. And I still wanted this baby more than I hate any of it. Work out for yourself what that makes us."))
        else:
            $ set_scene_expression(_disc_girl, "angry")
            $ Say_Line(_disc_girl, _("And let's not forget... this only happened because of what you've been doing to me. Because you gave me no choice."))

    # --- Step 3.5: Financial concern ---
    call _pregnancy_financial_concern(_disc_girl) from _call_preg_financial

    # --- Step 4: Player choice menu ---
    call _pregnancy_player_choice(_disc_girl) from _call_preg_choice

    # --- Step 4b: married with a husband among his contacts: officially the husband's (shion_pregnancy.rpy) ---
    if pregnancy_husband(_disc_girl) is not None and not _disc_she_left:
        call _pregnancy_husband_claim(_disc_girl) from _call_preg_husband_claim

    # --- Step 5: NPC partner warning ---
    #     Not SPOKEN when his answer ended the conversation (_disc_she_left: she used to walk out, slam the
    #     door, and then calmly say three more lines). Her partner still finds out: the flag is set either way.
    #     A loyal / cheating girl who wants her boyfriend to believe it brings the lie up herself first (_PREG_LIE_WILLING).
    if _disc_has_npc and not _disc_dating and not getattr(_disc_girl, "_npc_paternity_claimed", False):
        if _disc_she_left:
            $ _flag_npc_confrontation(_disc_girl, "she left: no warning spoken")
        else:
            $ _disc_suggest = _preg_lie_suggest_ok(_disc_girl)
            if _disc_suggest:
                call _pregnancy_npc_lie_suggest(_disc_girl) from _call_preg_lie_suggest
            if not getattr(_disc_girl, "_npc_paternity_claimed", False):
                # he was JUST the subject (her own proposal, Choice 4, or the last line of Choice 1 / 2, which both end
                # on him): no "one more thing we need to talk about: him" right after
                $ _disc_he_was_topic = (_disc_suggest or _pc_npc_pat_asked
                                        or _disc_girl._player_pregnancy_response in ("supportive", "breeding"))
                call _pregnancy_npc_warning(_disc_girl, skip_intro=_disc_he_was_topic) from _call_preg_npc_warn

    # --- Post-scene effects ---
    python:
        # the blush of this scene must not follow her around campus (it lives in sprite_state until someone resets it)
        sprite_state.setdefault(_disc_girl.Id, {})["blush"] = _normalize_blush_value(0)
        _disc_girl._pregnancy_known = True
        store._pregnancy_discovery_pending = None
        # The milestone is dated from the moment she TELLS him, never from the act (he must not learn it
        # from a banner mid-scene). Player status > FIRSTS reads player_firsts + _pregnancy_told_day.
        _disc_girl._pregnancy_told_day = store.Day
        if not _disc_girl.player_firsts.get("first_pregnancy"):
            _disc_girl.player_firsts["first_pregnancy"] = True
        _disc_girl.discover("player_first_pregnancy")
        # achievements that show the player what the pregnancy system allows (unlocked when SHE tells him)
        if _disc_is_lesbian:
            unlock_achievement("not_supposed_to_be_possible")
        if _disc_has_npc and _disc_girl.get_flag("partner_is_female"):
            unlock_achievement("immaculate_conception")
        print("[PREGNANCY] %s: discovery complete, response=%s" % (
            _disc_girl.gid, _disc_girl._player_pregnancy_response))

    return

# ============================================================
# PER-GIRL DISCOVERY SCENES
# ============================================================

label _pregnancy_discovery_gwen(girl):
    $ set_scene_expression(girl, "worried")

    "She sits on the edge of the bed, staring at the test in her hands. The confident, rebellious girl you know looks completely lost."

    $ set_scene_expression(girl, "nervous")

    $ Say_Line(girl, _("I... I..."))

    "She opens her mouth, closes it, tries again."

    $ set_scene_expression(girl, "serious")

    $ Say_Line(girl, _("Okay. I knew this could happen. I'm not stupid, I knew the risks. But knowing it and... and THIS... are two very different things."))

    "She holds up the test. Two lines."

    $ set_scene_expression(girl, "sad")

    $ Say_Line(girl, _("It's positive. I'm pregnant."))

    "She lets out a long breath, like she's been holding it since she took the test."

    $ set_scene_expression(girl, "bemused")

    $ Say_Line(girl, _("You know what's funny? I spent my whole life being the rebel. The goth girl who didn't care about consequences. Skipping class, breaking rules, not giving a damn about what anyone thought of me."))

    $ set_scene_expression(girl, "smirk")

    $ Say_Line(girl, _("And it felt great. Every time someone told me I was being irresponsible, I wore it like a badge of honor."))

    $ set_scene_expression(girl, "worried")

    $ Say_Line(girl, _("But this... this isn't a piercing I can take out. This isn't a class I can retake next semester. This isn't a rule I can laugh about breaking."))

    $ set_scene_expression(girl, "sad")

    $ Say_Line(girl, _("This is a person. An actual, real, breathing person."))

    $ set_scene_expression(girl, "sad", eyes="eyes_looking_down")

    $ Say_Line(girl, _("I spent so long running from anything serious. From commitment, from responsibility, from growing up. And now... I can't run anymore. There's nowhere to go."))

    "She looks at you, and for the first time, you see genuine vulnerability behind those dark eyes."

    $ set_scene_expression(girl, "scared")

    $ Say_Line(girl, _("I've been pretending my whole life that nothing gets to me. That I'm too cool to care. But right now? I'm terrified."))

    $ set_scene_expression(girl, "bemused")

    $ Say_Line(girl, _("I've spent weeks on an island with strangers, cameras and a lunatic running the show. I didn't flinch once. This? This is the scariest thing that's ever happened to me."))

    $ set_scene_expression(girl, "sad")

    $ Say_Line(girl, _("Not just of the baby. Of the fact that I have to become someone I don't even know how to be."))

    "A long pause."

    $ set_scene_expression(girl, "worried")

    $ Say_Line(girl, _("So... what do we do? Because for the first time in my life, I don't have a sarcastic comeback. I don't have an answer. I have nothing."))

    return

label _pregnancy_discovery_rogue(girl):
    $ set_scene_expression(girl, "worried")

    "She sits across from you, fidgeting with the test, turning it over and over in her gloved hands."

    $ Say_Line(girl, _("Sugar... I never thought this would happen. Not to me. Not in a million years."))

    $ set_scene_expression(girl, "serious")

    $ Say_Line(girl, _("You know where I come from. You know what I've been through."))

    $ set_scene_expression(girl, "sad")

    $ Say_Line(girl, _("I spent YEARS scared to touch another person. Years where even a handshake felt like a risk I couldn't take. Years of watching other girls hold hands with boys while I couldn't even brush against someone's arm."))

    "Her voice cracks. She clears her throat, tries to hold it together."

    $ set_scene_expression(girl, "sad", eyes="eyes_looking_down")

    $ Say_Line(girl, _("I used to lie awake at night wondering if I'd ever feel someone's skin against mine. If I'd ever know what a kiss felt like without being scared of what it might do."))

    $ set_scene_expression(girl, "nervous")

    $ Say_Line(girl, _("And now..."))

    "She holds up the test, almost laughing at the absurdity."

    $ set_scene_expression(girl, "surprised")

    $ Say_Line(girl, _("Now there's someone GROWING inside me. Someone I made. With another person. With you."))

    $ set_scene_expression(girl, "perplexed")

    $ Say_Line(girl, _("I went from never being able to touch a soul on this earth... to carrying a baby. How does that even make sense? How is that my life?"))

    "She stares at the test like it might change its answer if she looks hard enough."

    $ set_scene_expression(girl, "scared")

    $ Say_Line(girl, _("I ain't ready for this. Not even close. My own childhood wasn't exactly a blueprint for raisin' a kid. My aunt did her best with me, Lord knows she did, but half of what I remember is runnin'."))

    $ set_scene_expression(girl, "worried")

    $ Say_Line(girl, _("But I also know what it's like to grow up feeling like nobody wanted you around. And I won't... I can't let that happen to someone else."))

    "She looks up at you."

    $ set_scene_expression(girl, "sad")

    $ Say_Line(girl, _("I need you to help me think this through. Because right now, darlin'? I'm the most lost I've ever been. And considering my life, that's saying something."))

    return

label _pregnancy_discovery_ntw(girl):
    "The door SLAMS open."

    "Before you can say a word, she's already in your face."

    $ set_scene_expression(girl, "angry")

    $ Say_Line(girl, _("You..."))

    show layer master at bj_slap_shake

    $ Say_Line(girl, _("Son..."))

    show layer master at bj_slap_shake

    $ Say_Line(girl, _("Of a..."))

    show layer master at bj_slap_shake

    $ Say_Line(girl, _("BITCH!"))

    "Your ears are ringing. She's shaking. Not from fear. From pure, undiluted rage."

    $ Say_Line(girl, _("YOU GOT ME PREGNANT!"))

    $ Say_Line(girl, _("You filled me with your cum and now there's something GROWING inside me! Something ALIVE! Do you have ANY idea what you've done to me?!"))

    "She throws the pregnancy test at your chest. It bounces off and clatters to the floor."

    $ Say_Line(girl, _("I had a PLAN! I had my whole life figured out! No kids, no complications, no bullshit! And you just... you just..."))

    "She punches the wall. Hard. Then winces, holding her fist."

    $ set_scene_expression(girl, "grimace")

    $ Say_Line(girl, _("FUCK!"))

    $ set_scene_expression(girl, "worried")

    $ Say_Line(girl, _("I can't even... I can't even punch a wall right now because what if it hurts the..."))

    $ set_scene_expression(girl, "startled")

    "She stops mid-sentence. Realizes what she just said. That she's already protecting something she didn't even know existed an hour ago."

    $ set_scene_expression(girl, "angry")

    $ Say_Line(girl, _("...Don't. Don't you DARE look at me like that. Don't you DARE smile."))

    $ set_scene_expression(girl, "annoyed")

    $ Say_Line(girl, _("I hate you. I hate you more than I've ever hated anyone in my entire miserable life."))

    $ set_scene_expression(girl, "embarrassed")

    $ Say_Line(girl, _("And I hate that I can't even hate you properly right now because my stupid brain won't stop thinking about the stupid thing inside me."))

    # pregnancy_fear (canonical NTW trait)
    if girl.has_trait("pregnancy_fear"):
        "The anger fades. What's left underneath is worse."

        $ set_scene_expression(girl, "sad")

        $ Say_Line(girl, _("...I'm so scared. And I don't get scared. I don't DO scared."))

        $ set_scene_expression(girl, "scared")

        $ Say_Line(girl, _("But this is the one thing I always said would never happen to me. And it happened."))

        $ set_scene_expression(girl, "sad")

        $ Say_Line(girl, _("I don't know what to do. I don't know anything anymore."))

    return

label _pregnancy_discovery_tenny(girl):
    $ set_scene_expression(girl, "worried")

    "She's already crying before she even sits down."

    $ set_scene_expression(girl, "nervous")

    $ Say_Line(girl, _("I-I... I took a test and... and..."))

    "She can't finish the sentence. She just holds up the test, her hand trembling so badly you can barely read it."

    $ set_scene_expression(girl, "sad")

    $ Say_Line(girl, _("I'm p-pregnant."))

    "The dam breaks. She sobs into her hands for a long time before she can speak again."

    $ set_scene_expression(girl, "scared")

    $ Say_Line(girl, _("W-what about my studies?! I worked so hard to get here! I studied every night, I gave up everything, I-I can't drop out... I WON'T drop out!"))

    $ set_scene_expression(girl, "sad")

    $ Say_Line(girl, _("I was supposed to get my doctorate. That was the plan. Ever since I was little, that was the ONLY plan."))

    $ set_scene_expression(girl, "sad", eyes="eyes_looking_down")

    $ Say_Line(girl, _("My grandpa... he fixed pipes for forty years so his family could have it easier. Every summer in that old RV he'd quiz me at the fold-out table, even when he was exhausted from driving all day."))

    $ set_scene_expression(girl, "smile")

    $ Say_Line(girl, _("He always said 'Tenny, you're gonna be the first one in this family to get that degree. I know it.' And I believed him. I still believe him."))

    "She wipes her eyes with her sleeve, but the tears keep coming."

    $ set_scene_expression(girl, "scared")

    $ Say_Line(girl, _("But how?! How am I supposed to study with morning sickness? How do I take exams with a baby? What happens to my lab hours? My research?"))

    $ set_scene_expression(girl, "worried")

    $ Say_Line(girl, _("What if I have to postpone my doctorate? What if I fall behind and never catch up? What if all those years of studying were for nothing?"))

    $ set_scene_expression(girl, "worried")

    "She sniffles. Something changes in her expression. A tiny spark through the tears."

    $ set_scene_expression(girl, "thinking")

    $ Say_Line(girl, _("But... my grandpa never backed down from a hard job in his life. And he always, always said he'd support me no matter what."))

    $ set_scene_expression(girl, "surprised")

    $ Say_Line(girl, _("Maybe he could help? With the baby, while I'm in class? He'd... he'd love that, actually. He always said the house was too quiet."))

    $ set_scene_expression(girl, "bemused")

    $ Say_Line(girl, _("And my parents... they'll panic for a week. And then my mom will start buying baby clothes. I know them."))

    $ set_scene_expression(girl, "smile")

    $ Say_Line(girl, _("And there ARE other students who had babies and still graduated, right? I've read about them. It's hard, but it's not impossible."))

    "She looks at you with red, puffy eyes. But there's something in them now that wasn't there a minute ago."

    $ set_scene_expression(girl, "scared")

    $ Say_Line(girl, _("I'm so scared. I've never been this scared in my life."))

    $ set_scene_expression(girl, "smile")

    $ Say_Line(girl, _("But I'm not alone. I have you. And I have my grandpa. And I have my brain, which still works even if the rest of me is falling apart."))

    $ set_scene_expression(girl, "sad")

    $ Say_Line(girl, _("...Please tell me that's enough. Please tell me I can do this."))

    return

label _pregnancy_discovery_default(girl):
    # "_default" voice of the emotional scene
    $ set_scene_expression(girl, "worried")

    "She sits down slowly, turning the test over in her hands before she finally holds it out to you."

    $ Say_Line(girl, _("I took a test this morning. Then a second one, because I didn't believe the first."))

    $ set_scene_expression(girl, "serious")

    $ Say_Line(girl, _("They both say the same thing. I'm pregnant."))

    "She lets the words hang there, watching your face."

    $ set_scene_expression(girl, "sad")

    $ Say_Line(girl, _("I keep doing the math in my head. Classes, money, my family, what people will say. None of it adds up yet."))

    $ set_scene_expression(girl, "sad", eyes="eyes_looking_down")

    $ Say_Line(girl, _("I had plans. I still have them. I just don't know where a baby fits into any of it."))

    $ set_scene_expression(girl, "worried")

    $ Say_Line(girl, _("I'm scared. I'm not going to pretend I'm not."))

    "She takes a breath and looks straight at you."

    $ set_scene_expression(girl, "serious")

    $ Say_Line(girl, _("But I didn't get here alone. So I need to hear it from you. What do we do now?"))

    return

# ============================================================
# PER-GIRL DISCOVERY SCENES: SHE WANTED THIS (pregnancy_fetish)
# ============================================================
# Same job as the scenes above (she tells him, then asks where he stands), but she is happy. Routed by
# _PREG_DISCOVERY_WANTED in _pregnancy_discovery. A new girl gets her own label + one entry in the dict;
# without one she speaks with the "_default" voice. Lines never claim more than "you finished inside me"
# (true for every pregnancy, a broken condom included).

init python:
    _PREG_DISCOVERY_WANTED = {
        "gwen": "_pregnancy_discovery_gwen_wanted",
        "rogue": "_pregnancy_discovery_rogue_wanted",
        "ntw": "_pregnancy_discovery_ntw_wanted",
        "tenny": "_pregnancy_discovery_tenny_wanted",
        "_default": "_pregnancy_discovery_default_wanted",
    }

    # Step 3 addendum when she has an NPC partner: (line, face). %(pn)s / %(Pn)s = partner NAME, %(pp)s %(po)s = his /
    # her pronouns (_format_partner_line translates at display time). She WANTED the baby (pregnancy_fetish): she only
    # remembers her partner mid-celebration, a beat and never a drama (author, 2026-09-19: "deve ser mais algo sobre
    # lembrar que tem um namorado, nao ficar triste quando tem o breed kink").
    _PREG_PARTNER_ADDENDUM = {
        "gwen": (_("And... %(pn)s. God, what am I going to tell %(po)s?"), "worried"),
        "rogue": (_("Lord have mercy, %(pn)s... what's %(pp)s gonna think?"), "worried"),
        "ntw": (_("And just to make this perfect, I get to explain this to %(pn)s too."), "worried"),
        "tenny": (_("A-and %(pn)s... %(pp)s is going to be so upset with me..."), "worried"),
        "_default": (_("And then there is %(pn)s. I have no idea what I'm going to tell %(po)s."), "worried"),
    }
    _PREG_PARTNER_ADDENDUM_WANTED = {
        "gwen": (_("...Oh. Right. %(Pn)s. I got so wrapped up in this I forgot %(pp)s exists. Problem for future me."), "perplexed"),
        "rogue": (_("Oh, Lord. %(Pn)s. I plumb forgot about %(po)s for a minute there. We'll cross that bridge when we get to it."), "surprised"),
        "ntw": (_("...Right. %(Pn)s. That's going to be a fun conversation. Later. Much later."), "looking_left"),
        "tenny": (_("Oh! %(Pn)s! I-I kind of forgot about %(po)s for a second... Is that awful? I'll figure it out."), "surprised"),
        "_default": (_("Oh. %(Pn)s. I was so happy I forgot about %(po)s for a second. We'll figure that part out."), "perplexed"),
    }

    # Choice 4 and the lie by her side of the affair (author, 2026-09-19: "garotas com o trait de fiel querem mentir
    # para o namorado e podem ate sugerir / garotas com cheater de trait querem mentir pela diversao e para continuar").
    # LOYAL: she wants her boyfriend to believe it (she cannot lose him). CHEATER: for the thrill, and to keep seeing
    # the player. Either agrees at once to "convince" or "order" (no Love cost, no Obed gate, no sulking) and, if he
    # never brings it up (Choice 4 not played, the baby not denied), suggests it herself before the warning (Step 5).
    # Only a man can be told it is his: "male" route only. First trait of _PREG_LIE_ORDER wins.
    #   (line, face) pairs: base = her answer to Choice 4, again = Choice 4 clicked again after he dropped it (she is glad,
    #   never the angry _PREG_NPC_PAT_REPEAT), accept = to "convince" / "order", confirm = the lie is agreed, refuse = he
    #   says no to the lie she wanted, suggest = her own proposal. love = her Love when the lie is agreed.
    #   Shared voice; _PREG_LIE_STYLE holds a girl's own wording. Always read through _preg_lie_line / _preg_lie_say.
    _PREG_LIE_WILLING = {
        "loyal": {
            "base": (_("...I know it isn't his. But if he believed it was... I wouldn't lose him. God, listen to me."), "worried"),
            "again": (_("...You keep coming back to it. So do I."), "worried"),
            "accept": (_("...Okay. He'll believe me. He always does. I'll carry this for the rest of my life, but I'll keep him."), "sad"),
            "confirm": (_("Then it's done. He gets a family, and I get to keep him. Please never bring this up again."), "worried"),
            "refuse": (_("...Okay. I heard you. I just don't know how I'm going to face him."), "sad"),
            "suggest": (_("And %(pn)s... what if %(pp)s never has to know it isn't %(poss)s? %(Pp)s'd be happy. We'd stay together. Nobody gets hurt."), "worried"),
            "love": 5,
        },
        "cheater": {
            "base": (_("His? We both know it's yours. But I like where your head is at."), "sly"),
            "again": (_("Back to that idea? Good. I was hoping you'd come around."), "sly"),
            "accept": (_("Deal. He gets a baby to brag about, and I keep sneaking out to see you."), "smirk"),
            "confirm": (_("Then it's settled. Daddy %(pn)s it is. Oh, this is going to be fun."), "sly"),
            "refuse": (_("Your call. It would've been a lot more fun the other way."), "annoyed"),
            "suggest": (_("And %(pn)s? Why tell %(po)s anything? %(Pp)s'll assume it's %(poss)s, and we keep doing what we do. Best of both worlds."), "sly"),
            "love": 10,
        },
    }
    _PREG_LIE_ORDER = ("loyal", "cheater")

    # Her own style where the shared wording would break it: Rogue is Southern ("sugar", "ain't", -in'), Tenny
    # stutters whenever the baby comes up. Same keys and faces as _PREG_LIE_WILLING; a missing key = the shared line.
    _PREG_LIE_STYLE = {
        "rogue": {
            "loyal": {
                "base": (_("...I know it ain't his, sugar. But if he believed it was... I wouldn't lose him. Lord, listen to me."), "worried"),
                "again": (_("...You keep comin' back to it, darlin'. So do I."), "worried"),
                "accept": (_("...Alright, sugar. He'll believe me. He always does. I'll carry this till the day I die, but I'll keep him."), "sad"),
                "confirm": (_("Then it's done. He gets his family, and I get to keep him. Don't you ever bring this up again, sugar."), "worried"),
                "refuse": (_("...Alright. I heard you. I just don't know how I'm gonna look him in the eye."), "sad"),
                "suggest": (_("And %(pn)s... what if %(pp)s never has to know it ain't %(poss)s? %(Pp)s'd be happy. We'd stay together. Nobody gets hurt, sugar."), "worried"),
            },
            "cheater": {
                "base": (_("His? Sugar, we both know it's yours. But I like where your head's at."), "sly"),
                "again": (_("Back to that idea, darlin'? Good. I was hopin' you'd come around."), "sly"),
                "accept": (_("Deal. He gets a baby to brag about, and I keep sneakin' out to see you."), "smirk"),
                "confirm": (_("Then it's settled. Daddy %(pn)s it is. Lord, this is gonna be fun."), "sly"),
                "refuse": (_("Your call, sugar. Would've been a whole lot more fun the other way."), "annoyed"),
                "suggest": (_("And %(pn)s? Why tell %(po)s anything? %(Pp)s'll figure it's %(poss)s, and we keep doin' what we do. Best of both worlds, darlin'."), "sly"),
            },
        },
        "tenny": {
            "loyal": {
                "base": (_("...I-I know it isn't his. But if he believed it was... I wouldn't lose him. Oh god, listen to me..."), "worried"),
                "again": (_("...Y-you keep coming back to it. So do I..."), "worried"),
                "accept": (_("...O-okay. He'll believe me. He always does. I'll carry this forever, b-but I'll keep him."), "sad"),
                "confirm": (_("Then it's d-done. He gets a family, and I get to keep him. P-please never bring this up again."), "worried"),
                "refuse": (_("...O-okay. I heard you. I just don't know how I'm going to f-face him."), "sad"),
                "suggest": (_("A-and %(pn)s... what if %(pp)s never has to know it isn't %(poss)s? %(Pp)s'd be so happy. We'd stay together. N-nobody gets hurt."), "worried"),
            },
            "cheater": {
                "base": (_("H-his? We both know it's yours. B-but... I kind of like where your head is at."), "sly"),
                "again": (_("B-back to that idea? Good. I was h-hoping you'd come around."), "sly"),
                "accept": (_("D-deal. He gets a baby to brag about, and I keep sneaking out to see you."), "smirk"),
                "confirm": (_("Then it's s-settled. Daddy %(pn)s it is. This is so wrong... and so f-fun."), "sly"),
                "refuse": (_("Y-your call. It would've been a lot more fun the other way."), "annoyed"),
                "suggest": (_("And %(pn)s? W-why tell %(po)s anything? %(Pp)s'll assume it's %(poss)s, and we keep doing what we do. B-best of both worlds."), "sly"),
            },
        },
    }

    def _preg_lie_willing(girl):
        """"loyal" / "cheater" when she WANTS her boyfriend to believe the baby is his, else None."""
        if not girl.has_npc_partner() or girl.get_flag("partner_is_female"):
            return None
        return next((_t for _t in _PREG_LIE_ORDER if girl.has_trait(_t)), None)

    def _preg_lie_line(girl, key):
        """(line, face) of her side of the lie: her own style (_PREG_LIE_STYLE) first, then the shared one."""
        _w = _preg_lie_willing(girl)
        return _PREG_LIE_STYLE.get(girl.gid, {}).get(_w, {}).get(key) or _PREG_LIE_WILLING[_w][key]

    def _preg_lie_say(girl, key):
        """Her side of the lie, said: face, then the line with his name and pronouns filled in."""
        _line, _face = _preg_lie_line(girl, key)
        print("[PREGNANCY] %s: lie line '%s' (%s)" % (girl.gid, key, _preg_lie_willing(girl)))
        set_scene_expression(girl, _face, blush=0)
        Say_Line(girl, _format_partner_line(girl, _line))

    def _preg_lie_suggest_ok(girl):
        """Step 5: she brings the lie up herself when she wants it, he never did (Choice 4 not played in this
        discovery) and he did not deny the baby."""
        return (_preg_lie_willing(girl) is not None and not getattr(store, "_pc_npc_pat_asked", False)
                and getattr(girl, "_player_pregnancy_response", None) != "deny")

    def _preg_npc_pat_confirm(girl, why):
        """The lie is agreed: her boyfriend will be told the baby is his (Choice 4 confirmed, or her own suggestion)."""
        _w = _preg_lie_willing(girl)
        girl._npc_paternity_claimed = True
        girl._player_pregnancy_response = "npc_paternity"
        Change_Status(girl, "Love", _PREG_LIE_WILLING[_w]["love"] if _w else -10)
        store._npc_pat_accepted = False
        # the lie answers the worry "what do I say to him?" (sad of Choice 1 when she has a partner): the girl who
        # wanted it is relieved (loyal) or amused (cheater), never sad for the rest of the day (no talk, no invite)
        if _w and girl.get_temp_status_reason("sad") == "pregnancy_discovery":
            girl.temp_statuses.pop("sad", None)
            girl.temp_status_reasons.pop("sad", None)
            print("[PREGNANCY] %s: the lie answers her worry about him, sad lifted" % girl.gid)
        unlock_achievement("the_big_lie")
        print("[PREGNANCY] %s: npc_paternity CONFIRMED (%s, willing=%s)" % (girl.gid, why, _w))

label _pregnancy_discovery_gwen_wanted(girl):
    $ set_scene_expression(girl, "smirk")

    "She drops onto the edge of the bed and holds the test up between two fingers, like a winning card she has been dying to play."

    $ Say_Line(girl, _("So. Funny thing about playing with fire."))

    "She flips the test around. Two lines."

    $ set_scene_expression(girl, "happy", blush=1)

    $ Say_Line(girl, _("Sometimes you get exactly what you were hoping for. I'm pregnant."))

    "The smirk cracks. What is underneath is softer than anything she has ever let you see."

    $ set_scene_expression(girl, "shy", blush=2)

    $ Say_Line(girl, _("I know what I look like. The goth girl who rolls her eyes at baby showers. And I do. They're awful."))

    $ set_scene_expression(girl, "shy", eyes="eyes_looking_down", blush=1)

    $ Say_Line(girl, _("But I've wanted this for longer than I ever admitted to anyone. Something that's mine. Someone I don't get to walk away from."))

    $ set_scene_expression(girl, "embarrassed", blush=2)

    $ Say_Line(girl, _("Every time you finished inside me, some part of me was hoping it would take. I just never had the guts to say it out loud.") if getattr(girl, "CreampieCounts", 0) > 1
             else _("When you finished inside me, some part of me was hoping it would take. I just never had the guts to say it out loud."))

    $ set_scene_expression(girl, "closed_happy", blush=2)

    $ Say_Line(girl, _("I took three tests. I cried at the second one. Happy crying. Tell anybody and I'll deny it."))

    "She presses a hand to her stomach, flat as ever, and laughs under her breath."

    $ set_scene_expression(girl, "happy", blush=1)

    $ Say_Line(girl, _("There's a person in there. Ours. How insane is that?"))

    $ set_scene_expression(girl, "nervous", blush=0)

    $ Say_Line(girl, _("So... say something. Because I'm over the moon right now, and I really need to know you're not about to run."))

    return

label _pregnancy_discovery_rogue_wanted(girl):
    $ set_scene_expression(girl, "happy", blush=1)

    "She pushes the door shut with her heel, both gloved hands wrapped around something she keeps pressed to her chest."

    $ Say_Line(girl, _("Sugar, sit down. No, really. Sit."))

    $ set_scene_expression(girl, "nervous", blush=1)

    $ Say_Line(girl, _("I had a whole speech worked out on the way over, and it's plumb gone."))

    "She gives up on the speech and simply holds the test out to you. Two lines."

    $ set_scene_expression(girl, "closed_happy", blush=2)

    $ Say_Line(girl, _("I'm pregnant, darlin'. We're havin' a baby."))

    $ set_scene_expression(girl, "sad", eyes="eyes_looking_down", blush=1)

    $ Say_Line(girl, _("You know where I come from. All those years I was too scared to let a soul get close enough to touch. I used to watch mamas in the park with their little ones and think, that ain't ever gonna be me."))

    "Her voice wobbles. She laughs at herself and wipes her eyes with the back of a glove."

    $ set_scene_expression(girl, "happy", blush=2)

    $ Say_Line(girl, _("And I wanted it so bad. A family that's mine. One nobody can take away or send packin'."))

    $ set_scene_expression(girl, "embarrassed", blush=2)

    $ Say_Line(girl, _("I never said it out loud 'cause it sounded crazy. But every time you stayed inside me, I was prayin' it would take.") if getattr(girl, "CreampieCounts", 0) > 1
             else _("I never said it out loud 'cause it sounded crazy. But when you stayed inside me, I was prayin' it would take."))

    $ set_scene_expression(girl, "laugh", blush=1)

    $ Say_Line(girl, _("And it did. Lord have mercy, it did."))

    "She takes your hand and lays it flat on her stomach, holding it there with both of hers."

    $ set_scene_expression(girl, "worried", blush=0)

    $ Say_Line(girl, _("I ain't scared of the baby. I'm scared of you lookin' at me like I did somethin' wrong. So tell me, sugar. Are you happy too?"))

    return

label _pregnancy_discovery_ntw_wanted(girl):
    # The smile he thought he saw (Step 2) is gone by the time she speaks: she fights it for the whole scene.
    # "...Okay. Fine. I was being dramatic." down to "Don't you DARE tell anyone" are the lines her
    # pregnancy_fetish turn had at the end of the angry scene.
    $ set_scene_expression(girl, "angry")

    "Whatever you saw on her face is gone by the time she plants herself in front of you. Jaw tight. Arms crossed."

    $ Say_Line(girl, _("You. Don't talk. Just look."))

    "She presses a pregnancy test flat against your chest and pins it there with one finger. Two lines."

    $ set_scene_expression(girl, "serious")

    $ Say_Line(girl, _("Pregnant. Positive. Knocked up. Pick whichever word you like."))

    $ Say_Line(girl, _("I walked over here with a whole speech. I hate you, you ruined my life, all of it."))

    "You brace for the punch. It never comes."

    $ set_scene_expression(girl, "looking_left", blush=1)

    $ Say_Line(girl, _("...Okay. Fine. I was being dramatic."))

    $ set_scene_expression(girl, "annoyed", blush=1)

    $ Say_Line(girl, _("Maybe I don't hate you THAT much."))

    $ Say_Line(girl, _("I told everyone I'd never want this. No kids, no complications. I said it so many times I almost believed it."))

    $ set_scene_expression(girl, "embarrassed", blush=2)

    $ Say_Line(girl, _("And then every time you came inside me, I caught myself hoping. Like an idiot.") if getattr(girl, "CreampieCounts", 0) > 1
             else _("And then when you came inside me, I caught myself hoping. Like an idiot."))

    "The corner of her mouth twitches. She loses the fight against it."

    $ set_scene_expression(girl, "smirk", blush=2)

    $ Say_Line(girl, _("So congratulations. You gave me the one thing I actually wanted. Don't let it go to your head."))

    $ Say_Line(girl, _("And maybe... maybe this is just the first one."))

    "She glares at you, but she can't hide the smirk."

    $ set_scene_expression(girl, "angry", blush=1)

    $ Say_Line(girl, _("Don't you DARE tell anyone I said that. Ever."))

    $ set_scene_expression(girl, "serious", blush=0)

    $ Say_Line(girl, _("Now say something. Before I change my mind about not hitting you."))

    return

label _pregnancy_discovery_tenny_wanted(girl):
    $ set_scene_expression(girl, "nervous", blush=1)

    "She slips inside and stands there hugging something to her chest, rocking on her heels. She's crying, and she can't stop smiling."

    $ Say_Line(girl, _("I-I took a test. And then another one. And then I made the pharmacy lady read the instructions to me again."))

    $ set_scene_expression(girl, "happy", blush=2)

    $ Say_Line(girl, _("I'm p-pregnant! I'm really pregnant!"))

    "She bounces once on her toes, remembers herself, and goes bright red."

    $ set_scene_expression(girl, "embarrassed", blush=2)

    $ Say_Line(girl, _("I-I know I'm supposed to be scared. My studies, my doctorate, all of it. I made a whole spreadsheet about how it could work. A long time ago. J-just in case."))

    $ set_scene_expression(girl, "shy", blush=2)

    $ Say_Line(girl, _("Because I always wanted this. A big noisy family. The best weeks of my life were the three of us crammed into grandpa's old RV, and I want that every single day."))

    $ set_scene_expression(girl, "shy", eyes="eyes_looking_down", blush=2)

    $ Say_Line(girl, _("I never told you, but every time you finished inside me, I was h-hoping. Is that bad? That's bad, isn't it?") if getattr(girl, "CreampieCounts", 0) > 1
             else _("I never told you, but when you finished inside me, I was h-hoping. Is that bad? That's bad, isn't it?"))

    "She peeks up at you through wet lashes."

    $ set_scene_expression(girl, "closed_happy", blush=1)

    $ Say_Line(girl, _("Grandpa is going to cry. He always said he wanted to hold a great-grandbaby while he could still lift one."))

    $ set_scene_expression(girl, "worried", blush=0)

    $ Say_Line(girl, _("I can do both. The degree and the baby. I know I can. I just... I need to know you're happy too. A-are you?"))

    return

label _pregnancy_discovery_default_wanted(girl):
    # "_default" voice of the happy scene. Shared voice: she says family and never names a relative.
    $ set_scene_expression(girl, "happy")

    "She comes in holding something in both hands, and she can't keep the smile off her face."

    $ Say_Line(girl, _("I have news. Good news. At least I hope you'll think so too."))

    "She holds out a pregnancy test. Two lines."

    $ set_scene_expression(girl, "closed_happy", blush=2)

    $ Say_Line(girl, _("I'm pregnant."))

    $ set_scene_expression(girl, "shy", blush=1)

    $ Say_Line(girl, _("I should probably be panicking. Classes, money, my family, what people will say. I know all of that is coming."))

    $ set_scene_expression(girl, "happy", blush=1)

    $ Say_Line(girl, _("But the truth is I wanted this. I've wanted it for a long time, and I never found the right way to tell you."))

    $ set_scene_expression(girl, "embarrassed", blush=2)

    $ Say_Line(girl, _("Every time you finished inside me, I was hoping this would happen.") if getattr(girl, "CreampieCounts", 0) > 1
             else _("When you finished inside me, I was hoping this would happen."))

    "She lays a hand on her stomach, almost shyly."

    $ set_scene_expression(girl, "worried", blush=0)

    $ Say_Line(girl, _("I'm happy. Really happy. And I need to know where you stand. What do we do now?"))

    return

# ============================================================
# STEP 3.5: FINANCIAL CONCERN
# ============================================================

init python:
    # A RICH mother's family pays the child support in full (child_support_player_share = 0, author's rule
    # 2026-09-30): her money talk says so instead of the "you're paying for this" speech. (expression, line);
    # "_default" for a girl without her own voice here. Middle class (neither trait) keeps the speech plus the
    # "we split it" lines (she pays part); poor keeps the speech plus "I need real help" (he pays it all).
    _PREG_FIN_RICH_TALK = {
        "ntw": [("serious", _("And money? Not your problem. My family will cover every cent of it.")),
                ("smirk", _("They'd rather sign checks than ask questions. So you're off the hook for the money. Not for the rest."))],
        "tenny": [("nervous", _("M-money isn't the problem, at least. My parents will pay for everything. Doctors, diapers, all of it.")),
                  ("shy", _("So you don't have to pay anything. I just... I still need you there. Please."))],
        "gwen": [("bemused", _("Okay, practical stuff. Money is the one thing my family is actually good for. They'll cover all of it.")),
                 ("smirk", _("So your wallet's safe. Your weekends, on the other hand, are mine now."))],
        "rogue": [("serious", _("Now don't you fret about the money, sugar. My family's got it covered, every last cent.")),
                  ("shy", _("You just worry 'bout bein' there. That's the part money can't buy."))],
        "_default": [("serious", _("At least money isn't a problem. My family will cover all of it.")),
                     ("shy", _("You don't have to pay anything. Just be there for us."))],
    }

label _pregnancy_financial_concern(girl):
    python:
        _fc_gid = girl.gid
        _fc_love = girl.Love
        _fc_poor = girl.has_trait("poor")
        _fc_rich = girl.has_trait("rich")
        # she WANTED this baby (pregnancy_fetish): glad and practical, never "this is YOUR mess"
        _fc_wanted = girl.has_trait("pregnancy_fetish")
        print("[PREGNANCY] %s: money talk wanted=%s love=%d poor=%s rich=%s" % (_fc_gid, _fc_wanted, _fc_love, _fc_poor, _fc_rich))

    # rich: her family pays the child support in full, so no "you're paying" speech (_PREG_FIN_RICH_TALK)
    if _fc_rich:
        python:
            for _fc_expr, _fc_line in _PREG_FIN_RICH_TALK.get(_fc_gid, _PREG_FIN_RICH_TALK["_default"]):
                set_scene_expression(girl, _fc_expr, blush=0)
                Say_Line(girl, _fc_line)
        return

    if _fc_gid == "ntw":
        if _fc_wanted:
            $ set_scene_expression(girl, "serious", blush=0)
            $ Say_Line(girl, _("And before you get comfortable: wanting this doesn't make it free. Diapers, doctors, a crib. All of it costs money."))
            $ set_scene_expression(girl, "smirk")
            $ Say_Line(girl, _("I carry it. You help pay for it. That's the deal, and it isn't up for negotiation."))
        elif _fc_love >= 600:
            $ set_scene_expression(girl, "serious", blush=0)
            $ Say_Line(girl, _("And just so we're clear... this isn't free. Babies cost money. A LOT of money."))
            $ set_scene_expression(girl, "annoyed")
            $ Say_Line(girl, _("Diapers, formula, a crib, doctor visits... you're helping pay for all of it."))
        else:
            $ set_scene_expression(girl, "angry", blush=0)
            $ Say_Line(girl, _("And you're paying for this. Every single bill. Every diaper, every bottle, every doctor visit."))
            $ Say_Line(girl, _("This is YOUR mess. So open your wallet."))
        if _fc_poor:
            $ set_scene_expression(girl, "worried")
            $ Say_Line(girl, _("I can barely afford to feed myself right now. If you think I'm doing this alone financially, you're out of your mind."))
        else:   # middle class: she pays part of it (the rich one never gets here)
            $ set_scene_expression(girl, "annoyed")
            $ Say_Line(girl, _("I have some savings, but that doesn't mean you get to walk away from YOUR share. This isn't a charity."))

    elif _fc_gid == "tenny":
        if _fc_wanted:
            $ set_scene_expression(girl, "nervous", blush=0)
            $ Say_Line(girl, _("I-I already made a budget. Three versions, actually. Diapers, doctor visits, a savings account for college..."))
            $ set_scene_expression(girl, "worried")
            $ Say_Line(girl, _("It's a lot of money. I can't cover it by myself. C-could we go over the numbers together?"))
        elif _fc_love >= 600:
            $ set_scene_expression(girl, "worried", blush=0)
            $ Say_Line(girl, _("I-I've been thinking... babies need so many things. But what really scares me is the future."))
            $ Say_Line(girl, _("I want this child to go to college someday. To have the same chances I had. But that costs SO much money..."))
            $ set_scene_expression(girl, "serious")
            $ Say_Line(girl, _("We need to start saving now. Like, right now. Every dollar counts."))
        else:
            $ set_scene_expression(girl, "scared", blush=0)
            $ Say_Line(girl, _("D-do you know how much it costs to raise a child? To put them through SCHOOL?"))
            $ Say_Line(girl, _("I looked it up once for a class project. The numbers are terrifying."))
            $ set_scene_expression(girl, "sad")
            $ Say_Line(girl, _("I can't do that alone. I just can't."))
        if _fc_poor:
            $ set_scene_expression(girl, "sad")
            $ Say_Line(girl, _("I'm already on scholarship because my family can't afford tuition... how am I supposed to pay for a baby AND finish my degree?"))
        else:
            $ set_scene_expression(girl, "thinking")
            $ Say_Line(girl, _("My family can help, I know they will... but I don't want to depend on grandpa for everything. I need to be responsible too."))

    elif _fc_gid == "gwen":
        if _fc_wanted:
            $ set_scene_expression(girl, "thinking", blush=0)
            $ Say_Line(girl, _("Okay, practical stuff, before I float away. Babies cost a fortune. Tiny clothes, a crib, a stroller that costs more than my first car."))
            $ set_scene_expression(girl, "serious")
            $ Say_Line(girl, _("I wanted this, so I'm not dumping all of it on you. But I can't do it alone either. We split it. Deal?"))
        elif _fc_love >= 600:
            $ set_scene_expression(girl, "serious", blush=0)
            $ Say_Line(girl, _("Okay, real talk? Do you have ANY idea how much baby stuff costs?"))
            $ set_scene_expression(girl, "bemused")
            $ Say_Line(girl, _("Clothes. Tiny, adorable clothes that they grow out of in like two weeks. Strollers. Car seats. A crib."))
            $ set_scene_expression(girl, "worried")
            $ Say_Line(girl, _("We need to figure out a budget. Like, yesterday."))
        else:
            $ set_scene_expression(girl, "serious", blush=0)
            $ Say_Line(girl, _("And let's talk about the elephant in the room. Money."))
            $ Say_Line(girl, _("Baby clothes, strollers, bottles, blankets... it all adds up. Fast."))
            $ set_scene_expression(girl, "angry")
            $ Say_Line(girl, _("I'm not asking. I'm telling you. You WILL help with this."))
        if _fc_poor:
            $ set_scene_expression(girl, "worried")
            $ Say_Line(girl, _("I've been stretching every dollar as it is. Adding a baby to this? I'll need help. Real help. Not just words."))
        else:
            $ set_scene_expression(girl, "serious")
            $ Say_Line(girl, _("I can cover the basics, but that doesn't let you off the hook. This is half yours, so half the cost is yours too."))

    elif _fc_gid == "rogue":
        if _fc_wanted:
            $ set_scene_expression(girl, "thinking", blush=0)
            $ Say_Line(girl, _("Now, I ain't so happy I've gone stupid. Doctor visits, vitamins, ultrasounds... it adds up quick, sugar."))
            $ set_scene_expression(girl, "serious")
            $ Say_Line(girl, _("I'll pull my weight, I swear it. I just need you pullin' right next to me."))
        elif _fc_love >= 600:
            $ set_scene_expression(girl, "worried", blush=0)
            $ Say_Line(girl, _("Sugar, there's something else we gotta talk about. The doctor stuff."))
            $ Say_Line(girl, _("Prenatal exams, ultrasounds, blood work, vitamins... the list goes on and on."))
            $ set_scene_expression(girl, "serious")
            $ Say_Line(girl, _("I need you there. Not just emotionally. The bills ain't gonna pay themselves."))
        else:
            $ set_scene_expression(girl, "serious", blush=0)
            $ Say_Line(girl, _("And since you're responsible for this, you're responsible for the medical bills too."))
            $ Say_Line(girl, _("Prenatal appointments, ultrasounds, lab work, supplements... all of it."))
            $ set_scene_expression(girl, "angry")
            $ Say_Line(girl, _("Don't even think about leaving me to handle that alone."))
        if _fc_poor:
            $ set_scene_expression(girl, "worried")
            $ Say_Line(girl, _("I don't have insurance that covers half of this. Every appointment is coming out of pocket, and I don't HAVE pockets deep enough."))
        else:
            $ set_scene_expression(girl, "serious")
            $ Say_Line(girl, _("I can afford the basics, but medical ain't cheap. Especially not for months of checkups and the delivery itself. You're splitting this with me."))

    else:
        # "_default" voice
        if _fc_wanted:
            $ set_scene_expression(girl, "thinking", blush=0)
            $ Say_Line(girl, _("There's the practical side too. Doctor visits, clothes, a crib. It adds up fast."))
            $ set_scene_expression(girl, "serious")
            $ Say_Line(girl, _("I wanted this, and I'll do my part. I just can't carry all of it alone."))
        elif _fc_love >= 600:
            $ set_scene_expression(girl, "worried", blush=0)
            $ Say_Line(girl, _("There's something else we have to talk about. Money."))
            $ Say_Line(girl, _("Doctor visits, clothes, a crib, everything a baby needs. It adds up fast, and I can't carry it alone."))
        else:
            $ set_scene_expression(girl, "serious", blush=0)
            $ Say_Line(girl, _("And this is going to cost money. A lot of it."))
            $ set_scene_expression(girl, "annoyed")
            $ Say_Line(girl, _("You're part of this, so you're paying your share. That's not up for discussion."))
        if _fc_poor:
            $ set_scene_expression(girl, "worried")
            $ Say_Line(girl, _("I can barely cover my own bills as it is. I need real help, not promises."))
        else:
            $ set_scene_expression(girl, "serious")
            $ Say_Line(girl, _("I can cover part of it, but that doesn't take you off the hook. Half of this is yours."))

    return

# ============================================================
# STEP 4: PLAYER CHOICE MENU
# ============================================================

label _pregnancy_player_choice(girl):
    python:
        _pc_dating = girl.is_dating_player()
        _pc_has_npc = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _pc_show_npc_opt = _pc_has_npc and not _pc_dating
        _pc_npc_pat_asked = False   # Choice 4 already played in THIS discovery (set before the loop label)

    # Choice 4 "Forget it. You're right, it's mine." comes back here (docs: back to the Step 4 menu).
    # jump, not call: the Choice 4 call has already returned, so the call stack does not grow.
    label .choice_menu:

    menu:
        "Come here. We'll figure this out.":
            call _pregnancy_choice_supportive(girl) from _call_preg_supportive

        "Good. I want to keep filling you up.":
            call _pregnancy_choice_breeding(girl) from _call_preg_breeding

        "I don't even know if that's mine.":
            call _pregnancy_choice_deny(girl) from _call_preg_deny

        "Wait... don't you think it could be [_disc_girl.npc_partner_name]'s?" if _pc_show_npc_opt:
            if _pc_npc_pat_asked and not _preg_lie_willing(girl):
                # she already gave her rebuttal: no replay, no free second try
                $ _preg_npc_pat_repeat(girl)
                jump .choice_menu
            # a girl who WANTS the lie (_PREG_LIE_WILLING) is glad he came back to it: straight to the sub-menu
            $ _pc_npc_pat_again = _pc_npc_pat_asked
            $ _pc_npc_pat_asked = True
            call _pregnancy_choice_npc_paternity(girl, again=_pc_npc_pat_again) from _call_preg_npc_pat
            if _return == _PREG_NPC_PAT_BACK_OUT:
                jump .choice_menu

    return

# ============================================================
# CHOICE 1: SUPPORTIVE
# ============================================================

label _pregnancy_choice_supportive(girl):
    python:
        _sp_dating = girl.is_dating_player()
        _sp_gid = girl.gid
        # she WANTED this (pregnancy_fetish): "I know this wasn't planned, I know you're scared" would answer
        # a scene that never happened, and so would her relief at not being left
        _sp_wanted = girl.has_trait("pregnancy_fetish")
        print("[PREGNANCY] %s: supportive wanted=%s dating=%s" % (_sp_gid, _sp_wanted, _sp_dating))

    if _sp_wanted:
        $ Say_Player(_("Come here."))
        "You pull her in before she can brace for a different answer."
        $ Say_Player(_("You wanted this. It's all over your face. So stop looking at me like I'm about to bolt."))
        if _sp_dating:
            $ Say_Player(_("You're my girlfriend, and you're having my baby. I'm not going anywhere."))
        else:
            $ Say_Player(_("I don't know exactly what we are yet. But I know I'm not going anywhere."))
        $ Say_Player(_("Doctor appointments, 3 AM cravings, all of it. I'm in."))
    elif _sp_dating:
        $ Say_Player(_("Come here."))
        "You pull her closer."
        $ Say_Player(_("We're together. This is US. Not just yours, not just mine. Ours."))
        $ Say_Player(_("I'm your boyfriend. When I said I'd be here for you, I meant for ALL of it. The good, the bad, and the... completely unplanned."))
        $ Say_Player(_("I'm not going anywhere. We'll handle this the same way we handle everything. Together. As a team."))
        $ Say_Player(_("And hey... maybe this is exactly where we were supposed to end up."))
    else:
        $ Say_Player(_("Hey. Look at me."))
        $ Say_Player(_("I know this wasn't planned. And I know you're scared. Hell, I'm scared too."))
        $ Say_Player(_("But I'm not the kind of guy who runs from something like this. Whatever you need... doctor appointments, money, someone to hold your hand at 3 AM when you can't sleep... I'll be there."))
        $ Say_Player(_("We didn't plan this. But we'll figure it out. Step by step. I promise."))

    # Per-girl reactions
    python:
        _sp_love_bonus = 0
        _sp_mood = None
        _sp_mood_days = 0
        _sp_mood_reason = None

    if preg_own_lines(girl, "supportive"):
        call _preg_own_react(girl, "supportive") from _call_preg_own_react_sp
        $ _sp_love_bonus = _preg_own_out.get("love", 38)
    elif _sp_gid == "gwen":
        if _sp_wanted:
            $ set_scene_expression(girl, "happy", blush=1)
            $ Say_Line(girl, _("There it is. That's the face I was hoping for."))
            $ set_scene_expression(girl, "smirk", blush=1)
            $ Say_Line(girl, _("Ugh, I'm going to be so insufferable about this. You have no idea."))
            $ _sp_love_bonus = 55 if _sp_dating else 40
        elif _sp_dating:
            $ set_scene_expression(girl, "surprised")
            $ Say_Line(girl, _("When you say 'team'... every team I was ever on voted me off sooner or later. I got used to being the lone rebel."))
            $ set_scene_expression(girl, "smile")
            $ Say_Line(girl, _("Maybe it's time I stopped running."))
            $ _sp_love_bonus = 55
        else:
            $ set_scene_expression(girl, "serious")
            $ Say_Line(girl, _("You mean that? Because right now I need someone who means it, not someone who's saying what I want to hear."))
            $ set_scene_expression(girl, "smile")
            $ Say_Line(girl, _("...Thank you. Really."))
            $ _sp_love_bonus = 40

    elif _sp_gid == "rogue":
        if _sp_wanted:
            $ set_scene_expression(girl, "closed_happy", blush=1)
            $ Say_Line(girl, _("Oh, thank the Lord. C'mere, sugar."))
            $ set_scene_expression(girl, "happy", blush=2)
            $ Say_Line(girl, _("We're gonna be a family. A real one. I actually get to have that."))
            $ _sp_love_bonus = 50 if _sp_dating else 35
        elif _sp_dating:
            $ set_scene_expression(girl, "smile")
            $ Say_Line(girl, _("You know, for the first time since I saw that test... I actually believe it's gonna be okay."))
            $ set_scene_expression(girl, "closed_happy")
            $ Say_Line(girl, _("Come here, darlin'. Hold me for a bit."))
            $ _sp_love_bonus = 50
        else:
            $ set_scene_expression(girl, "worried")
            $ Say_Line(girl, _("You ain't just saying that, right? Because I swear to God, if you disappear on me..."))
            $ set_scene_expression(girl, "smile")
            $ Say_Line(girl, _("...Okay. Okay, I believe you."))
            $ _sp_love_bonus = 35

    elif _sp_gid == "ntw":
        if _sp_wanted:
            $ set_scene_expression(girl, "looking_left", blush=1)
            $ Say_Line(girl, _("...Good answer."))
            $ set_scene_expression(girl, "smirk", blush=1)
            $ Say_Line(girl, _("You're on diaper duty. And wipe that grin off your face. ...Fine. Keep it."))
            $ _sp_love_bonus = 35 if _sp_dating else 25
        elif _sp_dating:
            $ set_scene_expression(girl, "angry")
            $ Say_Line(girl, _("If you're lying to me right now, I will actually kill you."))
            $ set_scene_expression(girl, "looking_left")
            $ Say_Line(girl, _("...But you're not. I can tell."))
            $ set_scene_expression(girl, "embarrassed", blush=1)
            $ Say_Line(girl, _("...Okay."))
            $ _sp_love_bonus = 35
        else:
            $ set_scene_expression(girl, "neutral")
            $ Say_Line(girl, _("..."))
            $ set_scene_expression(girl, "annoyed")
            $ Say_Line(girl, _("...Don't expect me to cry. I don't cry."))
            $ set_scene_expression(girl, "embarrassed", blush=1)
            $ Say_Line(girl, _("...Thank you. Or whatever."))
            $ _sp_love_bonus = 25

    elif _sp_gid == "tenny":
        if _sp_wanted:
            $ set_scene_expression(girl, "surprised", blush=1)
            $ Say_Line(girl, _("R-really?! You're happy too?!"))
            $ set_scene_expression(girl, "closed_happy", blush=2)
            $ Say_Line(girl, _("I'm going to be a mom! We're going to be a family!"))
            $ _sp_love_bonus = 60 if _sp_dating else 50
        elif _sp_dating:
            $ set_scene_expression(girl, "sad")
            $ Say_Line(girl, _("I was so scared you'd want to break up... I was already imagining doing this alone..."))
            $ set_scene_expression(girl, "happy")
            $ Say_Line(girl, _("But you're here. You're staying. That changes everything."))
            $ _sp_love_bonus = 60
        else:
            $ set_scene_expression(girl, "surprised")
            $ Say_Line(girl, _("R-really?! You're not mad?! You're not going to leave?!"))
            $ set_scene_expression(girl, "closed_happy")
            $ Say_Line(girl, _("Thank you, thank you, thank you!"))
            $ _sp_love_bonus = 50

    else:
        # "_default" voice (bonus = the middle of the four girls)
        if _sp_wanted:
            $ set_scene_expression(girl, "surprised", blush=1)
            $ Say_Line(girl, _("You mean it? You're really happy too?"))
            $ set_scene_expression(girl, "closed_happy", blush=2)
            $ Say_Line(girl, _("Then this is the best day of my life."))
            $ _sp_love_bonus = 50 if _sp_dating else 38
        elif _sp_dating:
            $ set_scene_expression(girl, "surprised")
            $ Say_Line(girl, _("I was so afraid of what you would say. Hearing that... I can breathe again."))
            $ set_scene_expression(girl, "smile")
            $ Say_Line(girl, _("Okay. Together, then."))
            $ _sp_love_bonus = 50
        else:
            $ set_scene_expression(girl, "serious")
            $ Say_Line(girl, _("Do you mean it? I need you to mean it."))
            $ set_scene_expression(girl, "smile")
            $ Say_Line(girl, _("...Thank you. I really needed to hear that."))
            $ _sp_love_bonus = 38

    # Trait overrides
    if _sp_wanted:
        # her answer is the per-voice one above; this is only the bonus of hearing what she hoped for
        $ _sp_love_bonus += 15

    if girl.has_trait("pregnancy_fear"):
        $ set_scene_expression(girl, "worried", blush=0)
        $ Say_Line(girl, _("Thank you... but I'm still terrified. I don't think that goes away."))
        $ _sp_mood = "sad"
        $ _sp_mood_days = 2
        $ _sp_mood_reason = "pregnancy_fear"

    if girl.has_trait("lesbian"):
        $ set_scene_expression(girl, "sad", blush=0)
        $ Say_Line(girl, _("That doesn't fix what this means for me. For who I am. But... at least I'm not alone."))
        $ _sp_love_bonus = min(_sp_love_bonus, 20)
        $ _sp_mood = "sad"
        $ _sp_mood_days = 2
        $ _sp_mood_reason = "pregnancy_lesbian"

    if getattr(girl, "_blackmail_leverage", 0) >= 2:
        $ set_scene_expression(girl, "annoyed", blush=0)
        $ Say_Line(girl, _("Don't pretend you care NOW. But... I'll take what I can get."))
        $ _sp_love_bonus = min(_sp_love_bonus, 10)
        $ _sp_mood = "angry"
        $ _sp_mood_days = 1
        $ _sp_mood_reason = "pregnancy_deny"

    python:
        _has_npc = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
    if _has_npc and not _sp_dating:
        if _sp_wanted:
            # she wanted this: her partner is a thought for later, never the worry that sours the moment
            # (author, 2026-09-19: "nao ficar triste quando tem o breed kink"). No sad mood, no Love cost.
            # A girl who wants him to believe it's his brings him up herself right after, with the lie (Step 5).
            if not _preg_lie_suggest_ok(girl):
                $ set_scene_expression(girl, "smile", blush=0)
                python:
                    _npc_line = _format_partner_line(girl, _("And I still have to figure out what to tell %(pn)s. Later. Right now I just want to enjoy this."))
                $ Say_Line(girl, _npc_line)
        else:
            $ set_scene_expression(girl, "worried", blush=0)
            python:
                _npc_line = _format_partner_line(girl, _("But %(pn)s... I still have to deal with %(po)s. What do I say?"))
            $ Say_Line(girl, _npc_line)
            $ _sp_love_bonus -= 5
            if not _sp_mood:
                $ _sp_mood = "sad"
                $ _sp_mood_days = 1
                $ _sp_mood_reason = "pregnancy_discovery"

    python:
        Change_Status(girl, "Love", _sp_love_bonus)
        girl._player_pregnancy_response = "supportive"
        if _sp_mood:
            girl.set_temp_status(_sp_mood, _sp_mood_days, reason=_sp_mood_reason)
        print("[PREGNANCY] %s: choice=supportive love_bonus=%d mood=%s" % (girl.gid, _sp_love_bonus, _sp_mood))

    return

# ============================================================
# CHOICE 2: BREEDING / LUST
# ============================================================

label _pregnancy_choice_breeding(girl):
    python:
        _br_dating = girl.is_dating_player()
        _br_gid = girl.gid

    if _br_dating:
        $ Say_Player(_("You know what? I'm glad."))
        $ Say_Player(_("I've been thinking about this since the first time I was inside you. How it would feel to know I got you pregnant. And it feels even better than I imagined."))

    $ Say_Player(_("Good."))
    "A long pause. You're not worried. You're not scared. You're... smiling."
    $ Say_Player(_("Every time I came inside you... every single time... I wanted this.") if getattr(girl, "CreampieCounts", 0) > 1
             else _("When I came inside you... I wanted this."))
    $ Say_Player(_("I wanted to fill you up and watch what happens. Feel you take every last drop."))
    $ Say_Player(_("And this isn't the last time. I'm going to keep doing it. Over and over. Until your body can't take anymore."))
    $ Say_Player(_("You're mine. And now there's proof growing inside you."))

    python:
        _br_love = 0
        _br_obed = 0
        _br_mood = "angry"
        _br_mood_days = 3
        _br_mood_reason = "pregnancy_deny"

    # Trait overrides first (highest priority)
    if girl.has_trait("pregnancy_fetish"):
        $ set_scene_expression(girl, "lusty", blush=2)
        $ Say_Line(girl, _("Yes... YES! Say it again. Tell me you'll fill me up again. Promise me!"))
        $ _br_love = 50
        $ _br_obed = 20
        $ _br_mood = None
        $ _br_mood_days = 0
    elif girl.has_trait("pregnancy_fear"):
        $ set_scene_expression(girl, "sad")
        $ Say_Line(girl, _("You're SICK! This is my WORST NIGHTMARE and you're getting off on it?!"))
        $ _br_love = -60
        $ _br_mood = "sad"
        $ _br_mood_days = 5
        $ _br_mood_reason = "pregnancy_fear"
    elif preg_own_lines(girl, "breeding"):
        call _preg_own_react(girl, "breeding") from _call_preg_own_react_br
        python:
            _br_love = _preg_own_out.get("love", 0)
            _br_obed = _preg_own_out.get("obed", 0)
            _br_mood = _preg_own_out.get("mood", _br_mood)
            _br_mood_days = _preg_own_out.get("mood_days", _br_mood_days)
    elif _br_gid == "gwen":
        if _br_dating:
            $ set_scene_expression(girl, "perplexed")
            $ Say_Line(girl, _("I... okay, that's... that's intense. I don't even know how to process what you just said."))
            $ _br_love = -15
            $ _br_mood = "sad"
            $ _br_mood_days = 2
        else:
            $ set_scene_expression(girl, "angry")
            $ Say_Line(girl, _("Are you... are you serious right now?! I'm telling you I'm PREGNANT and you're talking about cum?!"))
            $ _br_love = -30
            $ _br_mood_days = 3
    elif _br_gid == "rogue":
        if _br_dating:
            $ set_scene_expression(girl, "uncomfortable")
            $ Say_Line(girl, _("Sugar... I love that you want me but this is NOT the time for dirty talk!"))
            $ _br_love = -20
            $ _br_mood_days = 2
        else:
            $ set_scene_expression(girl, "angry")
            $ Say_Line(girl, _("Lord have mercy... I'm having a crisis and you're thinking with your dick?!"))
            $ _br_love = -35
            $ _br_mood_days = 3
    elif _br_gid == "ntw":
        if girl.has_trait("lesbian"):
            $ set_scene_expression(girl, "angry")
            $ Say_Line(girl, _("You... you think you can just BREED me like I'm yours?! I'm not your property!"))
            $ _br_love = -60
            $ _br_mood_days = 5
        else:
            $ set_scene_expression(girl, "angry")
            $ Say_Line(girl, _("I just told you I'm pregnant and your response is you want to keep CUMMING INSIDE ME?!"))
            $ _br_love = -50
            $ _br_mood_days = 4
    elif _br_gid == "tenny":
        if _br_dating:
            $ set_scene_expression(girl, "shy", blush=1)
            $ Say_Line(girl, _("Y-you really want... more? With me? Even though I'm scared?"))
            $ _br_love = -5
            $ _br_obed = 10
            $ _br_mood = "sad"
            $ _br_mood_days = 1
        else:
            $ set_scene_expression(girl, "embarrassed", blush=1)
            $ Say_Line(girl, _("I-I... that's... you can't say things like that right now!"))
            $ _br_love = -20
            $ _br_mood = "sad"
            $ _br_mood_days = 3
    else:
        # "_default" voice
        if _br_dating:
            $ set_scene_expression(girl, "perplexed")
            $ Say_Line(girl, _("I tell you I'm pregnant and that's where your mind goes? I need a minute."))
            $ _br_love = -15
            $ _br_mood = "sad"
            $ _br_mood_days = 2
        else:
            $ set_scene_expression(girl, "angry")
            $ Say_Line(girl, _("Are you serious? I'm telling you I'm pregnant and you're talking about doing it again?!"))
            $ _br_love = -30
            $ _br_mood_days = 3

    if getattr(girl, "_blackmail_leverage", 0) >= 2 and not girl.has_trait("pregnancy_fetish"):
        $ set_scene_expression(girl, "disgusted", blush=0)
        $ Say_Line(girl, _("So that's what this is. I'm just a body for you to breed. I always knew it."))
        $ _br_love = min(_br_love, -40)
        $ _br_mood = "angry"
        $ _br_mood_days = max(_br_mood_days, 4)

    python:
        _has_npc = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
    if _has_npc and not _br_dating:
        if girl.has_trait("pregnancy_fetish"):
            # she just begged "Promise me!": no fight about her partner one line later (author, 2026-09-19).
            # A girl who wants him to believe it's his brings him up herself right after, with the lie (Step 5).
            if not _preg_lie_suggest_ok(girl):
                $ set_scene_expression(girl, "smirk", blush=1)
                python:
                    _npc_breed_line = _format_partner_line(girl, _("And %(pn)s can think whatever %(pp)s wants. Just keep that promise."))
                $ Say_Line(girl, _npc_breed_line)
        else:
            $ set_scene_expression(girl, "angry", blush=0)
            python:
                _npc_breed_line = _format_partner_line(girl, _("And what about %(pn)s?! You want to keep getting me pregnant while I'm dating %(po)s?!"))
            $ Say_Line(girl, _npc_breed_line)
            $ _br_love -= 10
            $ _br_mood_days += 1

    python:
        Change_Status(girl, "Love", _br_love)
        if _br_obed > 0:
            Change_Status(girl, "Obed", _br_obed)
        girl._player_pregnancy_response = "breeding"
        if _br_mood:
            girl.set_temp_status(_br_mood, _br_mood_days, reason=_br_mood_reason)
        print("[PREGNANCY] %s: choice=breeding love=%d obed=%d mood=%s(%d)" % (
            girl.gid, _br_love, _br_obed, _br_mood, _br_mood_days))

    return

# ============================================================
# CHOICE 3: DENY / NOT MINE
# ============================================================

label _pregnancy_choice_deny(girl):
    python:
        _dn_dating = girl.is_dating_player()
        _dn_gid = girl.gid
        _dn_obed = girl.Obed

    $ Say_Player(_("How do I even know that's mine?"))
    $ Say_Player(_("Look, I'm going to be honest with you. I don't know what to tell you, but I'm not signing up for this."))

    if _dn_dating:
        $ Say_Player(_("I know we're together, but this... this changes everything. And I can't handle it. I'm sorry."))
    else:
        $ Say_Player(_("This isn't what I'm here for. I'm sorry, but... this is your problem."))

    python:
        _dn_love = 0
        _dn_mood = "angry"
        _dn_mood_days = 5
        _dn_mood_reason = "pregnancy_deny"

    # Trait overrides (apply regardless of Obed tier)
    python:
        _dn_trait_override = False

    if girl.has_trait("pregnancy_fetish"):
        $ set_scene_expression(girl, "angry", blush=0)
        $ Say_Line(girl, _("Fine! I'll raise this baby WITHOUT you. And it'll be the most loved child in the world."))
        $ _dn_love = -40
        $ _dn_mood = "angry"
        $ _dn_mood_days = 2
        $ _dn_trait_override = True

    elif girl.has_trait("pregnancy_fear"):
        $ set_scene_expression(girl, "scared")
        $ Say_Line(girl, _("You did this to me... you CAUSED this... and you're leaving me with it?!"))
        $ _dn_love = -70
        $ _dn_mood = "sad"
        $ _dn_mood_days = 5
        $ _dn_mood_reason = "pregnancy_fear"
        $ _dn_trait_override = True

    elif preg_own_lines(girl, "deny"):
        call _preg_own_react(girl, "deny") from _call_preg_own_react_dn
        python:
            _dn_love = _preg_own_out.get("love", -40)
            _dn_mood = _preg_own_out.get("mood", _dn_mood)
            _dn_mood_days = _preg_own_out.get("mood_days", _dn_mood_days)
            _dn_trait_override = True

    # Obed-tiered reactions (if no trait override)
    if not _dn_trait_override:
        if _dn_obed < 400:
            # Full resistance: every voice ends the conversation here
            $ _disc_she_left = True
            if _dn_gid == "gwen":
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, _("Are you KIDDING me right now?! You were INSIDE me! Without a condom! Multiple times! And now you 'don't know if it's yours'?!"))
                $ Say_Line(girl, _("Get out of my sight before I do something I regret."))
                $ _dn_love = -80
            elif _dn_gid == "rogue":
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, _("You ABSOLUTE piece of... You know EXACTLY whose it is! You were there! Every. Single. Time!"))
                $ Say_Line(girl, _("GET OUT!"))
                $ _dn_love = -90
            elif _dn_gid == "ntw":
                $ set_scene_expression(girl, "serious")
                "She doesn't speak. She just stares at you with an expression that makes your blood run cold. Then she walks out and slams the door so hard the frame cracks."
                $ _dn_love = -70
            elif _dn_gid == "tenny":
                $ set_scene_expression(girl, "sad")
                "Breaks down completely. Can't even form words. Just sobs and shakes her head."
                $ _dn_love = -100
                $ _dn_mood = "sad"
                $ _dn_mood_days = 6
            else:
                # "_default" voice
                $ set_scene_expression(girl, "angry")
                $ Say_Line(girl, _("You were there. Every single time. And now you 'don't know' if it's yours?!"))
                $ Say_Line(girl, _("Get out. I can't even look at you."))
                $ _dn_love = -85

        elif _dn_obed < 700:
            # Partial resistance
            if _dn_gid == "gwen":
                $ set_scene_expression(girl, "disgusted")
                $ Say_Line(girl, _("You know it's yours. You KNOW. But I can't make you be a man about it, can I?"))
                $ set_scene_expression(girl, "sad")
                $ Say_Line(girl, _("Fine. I'll handle it myself. Like I always do."))
                $ _dn_love = -60
                $ _dn_mood_days = 4
            elif _dn_gid == "rogue":
                $ set_scene_expression(girl, "sad")
                $ Say_Line(girl, _("I can't force you to care, can I? Even though you should."))
                $ Say_Line(girl, _("I expected more from you. That's on me, I guess."))
                $ _dn_love = -65
                $ _dn_mood_days = 4
            elif _dn_gid == "ntw":
                $ set_scene_expression(girl, "annoyed")
                $ Say_Line(girl, _("...Typical. Why did I even bother telling you."))
                $ _dn_love = -50
                $ _dn_mood_days = 3
            elif _dn_gid == "tenny":
                $ set_scene_expression(girl, "sad")
                $ Say_Line(girl, _("B-but... you know it's yours... why are you doing this to me?"))
                $ _dn_love = -80
                $ _dn_mood = "sad"
                $ _dn_mood_days = 5
            else:
                # "_default" voice
                $ set_scene_expression(girl, "sad")
                $ Say_Line(girl, _("You know it's yours. I can't force you to act like it."))
                $ Say_Line(girl, _("Fine. I'll do this without you."))
                $ _dn_love = -65
                $ _dn_mood_days = 4

        elif _dn_obed < 950:
            # Reluctant submission
            if _dn_gid == "gwen":
                $ set_scene_expression(girl, "sad")
                $ Say_Line(girl, _("...If that's what you want. I can't argue with you. I don't have the energy."))
                $ set_scene_expression(girl, "sad", eyes="eyes_looking_down")
                $ Say_Line(girl, _("I just... I thought you were different."))
                $ _dn_love = -40
                $ _dn_mood = "sad"
                $ _dn_mood_days = 4
            elif _dn_gid == "rogue":
                $ set_scene_expression(girl, "sad", eyes="eyes_looking_down")
                $ Say_Line(girl, _("...Okay, sugar. Whatever you say."))
                "Staring at nothing."
                $ _dn_love = -45
                $ _dn_mood = "sad"
                $ _dn_mood_days = 4
            elif _dn_gid == "ntw":
                $ set_scene_expression(girl, "looking_left")
                $ Say_Line(girl, _("..."))
                $ set_scene_expression(girl, "sad")
                $ Say_Line(girl, _("...Fine."))
                $ _dn_love = -35
                $ _dn_mood = "sad"
                $ _dn_mood_days = 3
            elif _dn_gid == "tenny":
                $ set_scene_expression(girl, "sad")
                $ Say_Line(girl, _("I-if you say it's not yours... then... then I guess I'm alone."))
                $ _dn_love = -60
                $ _dn_mood = "sad"
                $ _dn_mood_days = 5
            else:
                # "_default" voice
                $ set_scene_expression(girl, "sad")
                $ Say_Line(girl, _("...If that's what you want. I don't have the strength to fight you on this."))
                $ _dn_love = -45
                $ _dn_mood = "sad"
                $ _dn_mood_days = 4

        else:
            # Total submission (Obed 950+)
            if _dn_gid == "gwen":
                $ set_scene_expression(girl, "neutral")
                $ Say_Line(girl, _("...Okay."))
                "Nothing else. She just nods and leaves quietly."
                $ _disc_she_left = True
                $ _dn_love = -25
                $ _dn_mood = "sad"
                $ _dn_mood_days = 3
            elif _dn_gid == "rogue":
                $ set_scene_expression(girl, "sad", eyes="eyes_looking_down")
                $ Say_Line(girl, _("...You're right. It's not yours. I'll figure it out."))
                $ _dn_love = -30
                $ _dn_mood = "sad"
                $ _dn_mood_days = 3
            elif _dn_gid == "ntw":
                $ set_scene_expression(girl, "neutral")
                "No reaction. Turns around. Walks out. Closes the door gently. That's worse than slamming it."
                $ _disc_she_left = True
                $ _dn_love = -20
                $ _dn_mood = "sad"
                $ _dn_mood_days = 2
            elif _dn_gid == "tenny":
                $ set_scene_expression(girl, "sad")
                $ Say_Line(girl, _("Y-yes. You're right. I-I'm sorry for bothering you."))
                $ _dn_love = -35
                $ _dn_mood = "sad"
                $ _dn_mood_days = 3
            else:
                # "_default" voice
                $ set_scene_expression(girl, "neutral")
                $ Say_Line(girl, _("...Okay. I understand."))
                "She nods once and leaves without another word."
                $ _disc_she_left = True
                $ _dn_love = -28
                $ _dn_mood = "sad"
                $ _dn_mood_days = 3

    # Additional trait penalties
    if girl.has_trait("lesbian") and not _dn_trait_override:
        $ set_scene_expression(girl, "angry")
        $ Say_Line(girl, _("You forced yourself into my life, you did THIS to me, and now you RUN? You're a coward."))
        $ _dn_love -= 20
        $ _dn_mood_days = max(_dn_mood_days, 5)

    # lose_virginity() removes the "virgin" trait, so a pregnant girl never has it: read who took it
    if getattr(girl, "virginity_taken_by_player", False) and not _dn_trait_override:
        $ set_scene_expression(girl, "angry")
        $ Say_Line(girl, _("I was a VIRGIN before you. A VIRGIN. There is NO ONE else. You KNOW that."))
        $ _dn_love -= 20
        $ _dn_mood_days = max(_dn_mood_days, 5)

    if _dn_dating:
        $ _dn_love -= 20
        $ _dn_mood_days += 2

    python:
        Change_Status(girl, "Love", _dn_love)
        girl._player_pregnancy_response = "deny"
        girl.set_temp_status(_dn_mood, _dn_mood_days, reason=_dn_mood_reason)
        print("[PREGNANCY] %s: choice=deny love=%d obed_tier=%s mood=%s(%d)" % (
            girl.gid, _dn_love,
            "total_sub" if _dn_obed >= 950 else "reluctant" if _dn_obed >= 700 else "partial" if _dn_obed >= 400 else "full_resist",
            _dn_mood, _dn_mood_days))

    return

# ============================================================
# CHOICE 4: NPC PATERNITY
# ============================================================

init python:
    # Choice 4: her first answer, keyed by route (see _preg_npc_pat_route). A woman cannot be the
    # father, so the female routes never reach the convince / order sub-menu ("tell him it's his").
    # _() only marks the strings for extraction; _format_partner_line translates at display time.
    _PREG_NPC_PAT_BASE = {
        "male":           _("No... you know it's not %(poss)s. %(Pp)s barely touches me."),
        "female":         _("Are you even listening to yourself? %(pn)s is a woman. She can't get me pregnant. That only leaves you."),
        "female_lesbian": _("I'm gay, remember? %(Pn)s is a woman. She can't get me pregnant. You're the ONLY possibility."),
    }

    # Choice 4: HIS opening line. "his" is right both before a noun and alone ("it's his"); "her" alone is not
    # ("could be her?" = "could be hers?"), so a female partner has her own sentence. "male" keeps the old
    # string and its PT / ES pairs (their %(poss)s = "dele" / "dela" already worked).
    _PREG_NPC_PAT_INIT = {
        "male":   _("Wait... you're with %(pn)s. Don't you think it could be %(poss)s?"),
        "female": _("Wait... you're with %(pn)s. Don't you think it could be hers?"),
    }

    # Choice 4 lines that are only true while the affair is a secret, keyed by line then by context
    # (_preg_npc_pat_ctx): "secret" = he has no idea, "ntr_known" = _ntr_active_discovered(girl), he
    # knows about the player and set rules. Same sentence shape in every context. Shared voice (the
    # PLAYER says the order line), so no per-girl split. What she hides in "ntr_known" is the
    # paternity, not the affair: every "lie to %(po)s" line of the flow stays true in both contexts.
    _PREG_NPC_PAT_CTX_LINES = {
        "order_wont_know": {
            "secret":    _("%(Pp)s doesn't know I'm fucking you, and %(pp)s won't know the difference. Your boyfriend, your baby. Simple."),
            "ntr_known": _("%(Pp)s knows I'm fucking you, and %(pp)s still won't know the difference. Your boyfriend, your baby. Simple."),
        },
    }

    def _preg_npc_pat_ctx(girl):
        """Choice 4 context, a key of every _PREG_NPC_PAT_CTX_LINES entry."""
        _ctx = "ntr_known" if _ntr_active_discovered(girl) else "secret"
        print("[PREGNANCY] %s: npc_paternity ctx=%s" % (girl.gid, _ctx))
        return _ctx

    def _preg_npc_pat_ctx_line(girl, key):
        """Formatted Choice 4 line for the current context; falls back to the secret wording."""
        _pool = _PREG_NPC_PAT_CTX_LINES[key]
        return _format_partner_line(girl, _pool.get(_preg_npc_pat_ctx(girl), _pool["secret"]))

    def _preg_npc_pat_route(girl):
        """Choice 4 route, a key of _PREG_NPC_PAT_BASE. Partner gender comes from the girl's
        partner_is_female flag, the same source _format_partner_line uses for the pronouns."""
        if not girl.get_flag("partner_is_female"):
            _route = "male"
        elif girl.has_trait("lesbian"):
            _route = "female_lesbian"
        else:
            _route = "female"
        print("[PREGNANCY] %s: npc_paternity route=%s partner=%s" % (girl.gid, _route, girl.partner_name()))
        return _route

    # Step 5, her face on the last warning line ("he will come for you"), by voice
    _PREG_WARN_FACE = {"ntw": "smirk", "tenny": "scared", "_default": "serious"}

    # Return value of _pregnancy_choice_npc_paternity when the player backs out at the sub-menu:
    # _pregnancy_player_choice re-opens the Step 4 menu on it.
    _PREG_NPC_PAT_BACK_OUT = "back_out"

    def _preg_npc_pat_back_out(girl, route):
        """Player drops the idea at the Choice 4 sub-menu. docs/pregnancy_system.md: this leaves Choice 4
        and goes back to the Step 4 menu. Nothing is recorded or rewarded here: "supportive" + Love +20
        belong to "No. Forget it. I'll step up." at the FINAL menu, and the real supportive scene is one
        click away in the Step 4 menu."""
        print("[PREGNANCY] %s: npc_paternity (%s) -> backed out at sub-menu, back to the Step 4 menu" % (girl.gid, route))
        return _PREG_NPC_PAT_BACK_OUT

    # Choice 4 clicked AGAIN in the same discovery, after backing out. The button stays (never hide a
    # button): she already answered, so there is no replay of the rebuttal and it is never free.
    _PREG_NPC_PAT_REPEAT = {
        "love": -15,
        "expr": {"tenny": "sad", "_default": "angry"},
        "lines": {
            "gwen":     _("I already answered that. Don't make me say it twice."),
            "rogue":    _("Sugar, I already told you whose it is. Don't ask me that again."),
            "ntw":      _("Ask me that one more time. I dare you."),
            "tenny":    _("I-I already told you... p-please stop asking me that..."),
            "_default": _("I already answered that. Don't ask me again."),
        },
    }

    def _preg_npc_pat_repeat(girl):
        """In-game reaction to a second Choice 4 click: expression + line + Love loss, then the caller
        jumps back to the Step 4 menu."""
        _cfg = _PREG_NPC_PAT_REPEAT
        set_scene_expression(girl, _cfg["expr"].get(girl.gid, _cfg["expr"]["_default"]))
        Say_Line(girl, _format_partner_line(girl, _cfg["lines"].get(girl.gid, _cfg["lines"]["_default"])))
        Change_Status(girl, "Love", _cfg["love"])
        print("[PREGNANCY] %s: npc_paternity asked again -> repeat reaction, Love %d" % (girl.gid, _cfg["love"]))

    # Choice 4, her proof that it is his: the raw sex. "we've been doing it" needs more than 3 raw times
    # (raw_sex_count, the real counter); "for weeks" needs raw sex that started _PREG_RAW_WEEKS_DAYS ago or more
    # (_first_raw_day, stamped by _track_raw_sex_start). A save that went raw before that stamp has no first day:
    # it falls back on _last_inside_day, the last time he finished inside her raw as far as she knows
    # (pregnancy.rpy). Raw sex had started by then, so an old enough one still proves the weeks.
    _PREG_RAW_MIN_TIMES = 4
    _PREG_RAW_WEEKS_DAYS = 14
    _PREG_NPC_PAT_RAW_LINES = {
        "weeks": _("Meanwhile, we've been doing it without a condom for weeks."),
        "plain": _("Meanwhile, we've been doing it without a condom."),
    }

    def _preg_npc_pat_raw_line(girl):
        """Choice 4 raw sex line, or None when they have not gone raw often enough for her to say it."""
        _times = getattr(girl, "raw_sex_count", 0)
        if _times < _PREG_RAW_MIN_TIMES:
            return None
        _first = getattr(girl, "_first_raw_day", None)
        _raw_day = _first if _first is not None else getattr(girl, "_last_inside_day", None)
        _key = "weeks" if _raw_day is not None and store.Day - _raw_day >= _PREG_RAW_WEEKS_DAYS else "plain"
        print("[PREGNANCY] %s: npc_paternity raw line=%s (raw_sex_count=%d, first raw day=%s, last inside day=%s, today=%d)" % (
            girl.gid, _key, _times, _first, getattr(girl, "_last_inside_day", None), store.Day))
        return _PREG_NPC_PAT_RAW_LINES[_key]

label _pregnancy_choice_npc_paternity(girl, again=False):
    python:
        _np_npc = get_npc_partner_for(girl)
        _np_gid = girl.gid
        _np_route = _preg_npc_pat_route(girl)
        # loyal / cheater: she WANTS him to believe it (_PREG_LIE_WILLING, male route only)
        _np_willing = _preg_lie_willing(girl) if _np_route == "male" else None

    if _np_willing and again:
        # he dropped the lie she wanted and brought it back (Step 4 menu, second click): no replay of her answer
        $ _preg_lie_say(girl, "again")
        jump .np_submenu

    python:
        _np_init = _format_partner_line(girl, _PREG_NPC_PAT_INIT["male" if _np_route == "male" else "female"])
    $ Say_Player(_np_init)

    if _np_willing:
        # She takes the idea up instead of arguing the baby is his: no history lines to prove it
        $ _preg_lie_say(girl, "base")
        jump .np_submenu

    # Girl rejects immediately. Her line depends on the route: a woman cannot be the father (she is insulted);
    # a man could be (she is cornered).
    $ set_scene_expression(girl, "angry" if _np_route != "male" else "uncomfortable", blush=0)
    python:
        _np_base = _format_partner_line(girl, _PREG_NPC_PAT_BASE[_np_route])
    $ Say_Line(girl, _np_base)

    # Dynamic follow-up lines based on history
    python:
        _np_raw_line = _preg_npc_pat_raw_line(girl)
        _cream_count = getattr(girl, "CreampieCounts", 0)

    if _np_raw_line:
        $ set_scene_expression(girl, "serious")
        $ Say_Line(girl, _np_raw_line)

    # "every time" / "keep filling me": more than once
    if girl.has_trait("cum_slut") and _cream_count > 1:
        $ set_scene_expression(girl, "annoyed")
        $ Say_Line(girl, _("And you keep cumming inside me... so much... every time... you fill me up until it's dripping down my legs. You KNOW this is yours."))
    elif girl.has_trait("hate_cum") and _cream_count > 1:
        $ set_scene_expression(girl, "disgusted")
        $ Say_Line(girl, _("And I don't even know what gets into me to let you keep filling me with your disgusting cum... I hate it every time but I let you do it anyway."))
    elif _cream_count > 5:
        $ set_scene_expression(girl, "serious")
        $ Say_Line(girl, _("You've cum inside me more times than I can count. Who else could it possibly be?"))
    elif _cream_count == 0:
        $ set_scene_expression(girl, "serious")
        $ Say_Line(girl, _("Even pulling out isn't perfect. You know that."))

    # lose_virginity() removes the "virgin" trait, so a pregnant girl never has it: read who took it
    if getattr(girl, "virginity_taken_by_player", False):
        $ set_scene_expression(girl, "angry")
        $ Say_Line(girl, _("I was a virgin before you. There IS no one else. Literally no one."))

    # Sub-menu, female partner: "pass it off as hers" cannot exist. Her answer above is the in-game
    # reaction; what is left are two branches that were already written (deny / back out).
    if _np_route != "male":
        menu:
            "Fine, not hers. That still doesn't make it mine.":
                $ print("[PREGNANCY] %s: npc_paternity (%s) -> deny" % (girl.gid, _np_route))
                call _pregnancy_choice_deny(girl) from _call_preg_npc_pat_f_deny
                return

            "Forget it. You're right, it's mine.":
                return _preg_npc_pat_back_out(girl, _np_route)

    # Sub-menu, male partner (only reached when the partner is a man: his / him are correct here).
    # hide: the say statements below keep this label's translation ids (the PT / ES ones already written)
    label .np_submenu hide:

    menu:
        "Think about it... maybe it really is his.":
            call _pregnancy_npc_convince(girl) from _call_preg_npc_convince

        "I want you to tell him it's his.":
            call _pregnancy_npc_order(girl) from _call_preg_npc_order

        "Forget it. You're right, it's mine.":
            return _preg_npc_pat_back_out(girl, _np_route)

    # Final confirmation menu (if we got here from convince/order accept)
    if getattr(store, "_npc_pat_accepted", False):
        menu:
            "Yes. Tell him the baby is his.":
                $ _preg_npc_pat_confirm(girl, "choice 4")

                if _np_willing:
                    # she wanted this lie: relief (loyal) or fun (cheater), never "don't talk to me"
                    $ _preg_lie_say(girl, "confirm")
                elif _np_gid == "gwen":
                    $ set_scene_expression(girl, "sad")
                    $ Say_Line(girl, _("...Don't talk to me for a while. I need to figure out how to live with this."))
                elif _np_gid == "rogue":
                    $ set_scene_expression(girl, "sad")
                    $ Say_Line(girl, _("I'll do what you asked. But something between us just died, sugar."))
                elif _np_gid == "ntw":
                    $ set_scene_expression(girl, "neutral")
                    "She says nothing. Turns around. Walks out."
                elif _np_gid == "tenny":
                    $ set_scene_expression(girl, "sad")
                    python:
                        _ten_confirm = _format_partner_line(girl, _("I-I'll do my best... I'll try to make %(pn)s believe it..."))
                    $ Say_Line(girl, _ten_confirm)
                else:
                    # "_default" voice
                    $ set_scene_expression(girl, "sad")
                    $ Say_Line(girl, _("...I'll do it. But don't expect me to look at you the same way again."))

                if not _np_willing:
                    python:
                        _mood_days = girl.temp_statuses.get("angry", girl.temp_statuses.get("sad", store.Day))
                        _remaining = max(0, _mood_days - store.Day) + 1
                        girl.set_temp_status("sad" if girl.has_temp_status("sad") else "angry", _remaining + 1, reason="pregnancy_deny")

            "No. Forget it. I'll step up.":
                python:
                    girl._player_pregnancy_response = "supportive"
                    # the girl who WANTED the lie gets nothing out of him stepping up
                    Change_Status(girl, "Love", 0 if _np_willing else 20)
                    store._npc_pat_accepted = False
                    # lifted BEFORE she answers: a sad / angry mood forces its face on the sprite (set_girl_sprite)
                    if girl.has_temp_status("angry") or girl.has_temp_status("sad"):
                        girl.temp_statuses.pop("angry", None)
                        girl.temp_statuses.pop("sad", None)
                        girl.temp_status_reasons.pop("angry", None)
                        girl.temp_status_reasons.pop("sad", None)

                if _np_willing:
                    $ _preg_lie_say(girl, "refuse")
                elif _np_gid == "gwen":
                    $ set_scene_expression(girl, "smile")
                    $ Say_Line(girl, _("...Thank god. I couldn't have lived with that lie. Neither of us could."))
                elif _np_gid == "rogue":
                    $ set_scene_expression(girl, "smile")
                    $ Say_Line(girl, _("You had me scared there for a minute, darlin'. Don't ever ask me something like that again."))
                elif _np_gid == "ntw":
                    $ set_scene_expression(girl, "smirk")
                    $ Say_Line(girl, _("...Good. Because I wasn't going to do it anyway."))
                elif _np_gid == "tenny":
                    $ set_scene_expression(girl, "happy")
                    $ Say_Line(girl, _("R-really?! You changed your mind?! Oh thank you, thank you!"))
                else:
                    # "_default" voice
                    $ set_scene_expression(girl, "smile")
                    $ Say_Line(girl, _("...Thank you. I don't think I could have lived with that lie."))

                $ print("[PREGNANCY] %s: npc_paternity -> backed out at final, treating as supportive" % girl.gid)
    else:
        # Order was refused — only option is back out
        python:
            girl._player_pregnancy_response = "deny"
            print("[PREGNANCY] %s: npc_paternity -> order refused, response=deny" % girl.gid)

    return

label _pregnancy_npc_lie_agrees(girl):
    # She WANTED this lie (loyal: to keep him / cheater: for the thrill): no persuasion, no Obed gate, no sulking
    $ store._npc_pat_accepted = True
    $ _preg_lie_say(girl, "accept")
    return

label _pregnancy_npc_convince(girl):
    python:
        _conv_line = _format_partner_line(girl, _("I know, but... think about it. You're with %(po)s. People would just assume it's %(poss)s. And maybe... maybe that's easier for everyone."))
    $ Say_Player(_conv_line)

    if _preg_lie_willing(girl):
        call _pregnancy_npc_lie_agrees(girl) from _call_preg_lie_agrees_convince
        return

    if girl.gid == "gwen":
        $ set_scene_expression(girl, "angry")
        python:
            _g_line = _format_partner_line(girl, _("You're asking me to LIE. To %(pn)s's face. About who the father of my child is."))
        $ Say_Line(girl, _g_line)
        $ set_scene_expression(girl, "disgusted")
        $ Say_Line(girl, _("Do you have any idea how messed up that is?"))
    elif girl.gid == "rogue":
        $ set_scene_expression(girl, "sad")
        python:
            _r_line = _format_partner_line(girl, _("Sugar... that is a BIG ask. You're asking me to look %(po)s in the eyes every day and lie about the most important thing that's ever happened to me."))
        $ Say_Line(girl, _r_line)
    elif girl.gid == "ntw":
        $ set_scene_expression(girl, "annoyed")
        $ Say_Line(girl, _("So your solution is to make ME the liar. Make ME carry the guilt while you walk free."))
        $ set_scene_expression(girl, "disgusted")
        $ Say_Line(girl, _("Typical."))
    elif girl.gid == "tenny":
        $ set_scene_expression(girl, "worried")
        python:
            _t_line = _format_partner_line(girl, _("B-but that would be lying to %(pn)s... %(pp)s trusts me... I-I don't know if I can do that..."))
        $ Say_Line(girl, _t_line)
        $ set_scene_expression(girl, "sad")
        python:
            _t_line2 = _format_partner_line(girl, _("Every time %(pp)s looks at the baby and smiles... I'd know. I'd know the truth."))
        $ Say_Line(girl, _t_line2)
    else:
        # "_default" voice
        $ set_scene_expression(girl, "sad")
        python:
            _d_line = _format_partner_line(girl, _("You're asking me to lie to %(pn)s about who the father of my child is. Every day, for the rest of my life."))
        $ Say_Line(girl, _d_line)

    python:
        Change_Status(girl, "Love", -40)
        girl.set_temp_status("sad", 3, reason="pregnancy_deny")
        store._npc_pat_accepted = True
        print("[PREGNANCY] %s: npc_paternity convince path, Love -40" % girl.gid)

    return

label _pregnancy_npc_order(girl):
    python:
        _ord_line1 = _format_partner_line(girl, _("But you need to tell %(po)s it's %(poss)s. You're dating %(po)s. It makes more sense."))
    $ Say_Player(_("Look, I know it's mine. And I want to keep cumming inside your pussy. This wasn't the last time."))
    $ Say_Player(_ord_line1)
    python:
        # "he doesn't know" is only true while the affair is secret: see _PREG_NPC_PAT_CTX_LINES
        _ord_line2 = _preg_npc_pat_ctx_line(girl, "order_wont_know")
    $ Say_Player(_ord_line2)

    if _preg_lie_willing(girl):
        call _pregnancy_npc_lie_agrees(girl) from _call_preg_lie_agrees_order
        return

    if girl.Obed < 950:
        # Refuses
        if girl.gid == "gwen":
            $ set_scene_expression(girl, "angry")
            python:
                _g_ref = _format_partner_line(girl, _("Have you lost your MIND?! You want me to lie about my baby's father so you can keep screwing me?!"))
            $ Say_Line(girl, _g_ref)
            $ set_scene_expression(girl, "disgusted")
            $ Say_Line(girl, _("You're disgusting. Absolutely disgusting."))
            # her answer, said out loud: the lines above never said whether she would do it
            python:
                _g_no = _format_partner_line(girl, _("And no. I'm not lying to %(pn)s. Not for you, not for anyone."))
            $ set_scene_expression(girl, "angry")
            $ Say_Line(girl, _g_no)
            $ Change_Status(girl, "Love", -60)
        elif girl.gid == "rogue":
            $ set_scene_expression(girl, "angry")
            python:
                _r_ref = _format_partner_line(girl, _("You... you want to keep using me AND make me lie to %(pn)s about it?!"))
            $ Say_Line(girl, _r_ref)
            $ set_scene_expression(girl, "disgusted")
            $ Say_Line(girl, _("I should have NEVER let you touch me."))
            python:
                _r_no = _format_partner_line(girl, _("And no, I ain't lyin' to %(pn)s about this baby. Not for you."))
            $ set_scene_expression(girl, "angry")
            $ Say_Line(girl, _r_no)
            $ Change_Status(girl, "Love", -70)
        elif girl.gid == "ntw":
            $ set_scene_expression(girl, "serious")
            python:
                _n_ref = _format_partner_line(girl, _("Let me get this straight. You want to keep fucking me, keep cumming inside me, AND make me tell %(pn)s the baby is %(poss)s."))
            $ Say_Line(girl, _n_ref)
            $ set_scene_expression(girl, "disgusted")
            $ Say_Line(girl, _("You're the worst person I've ever met. And I've met some real pieces of work."))
            python:
                _n_no = _format_partner_line(girl, _("So no. I'm not telling %(pn)s it's %(poss)s. Deal with it."))
            $ set_scene_expression(girl, "serious")
            $ Say_Line(girl, _n_no)
            $ Change_Status(girl, "Love", -50)
        elif girl.gid == "tenny":
            $ set_scene_expression(girl, "scared")
            python:
                _t_ref = _format_partner_line(girl, _("You... you want me to LIE to %(pn)s... so you can keep... keep..."))
            $ Say_Line(girl, _t_ref)
            "Can't finish. Runs out crying."
            $ Narration(_("She never said it, but the answer was no."))
            $ _disc_she_left = True
            $ Change_Status(girl, "Love", -80)
        else:
            # "_default" voice
            $ set_scene_expression(girl, "angry")
            python:
                _d_ref = _format_partner_line(girl, _("You want me to lie to %(pn)s about my own baby so you can keep sleeping with me?!"))
            $ Say_Line(girl, _d_ref)
            $ set_scene_expression(girl, "disgusted")
            $ Say_Line(girl, _("No. Absolutely not. What is wrong with you?"))
            $ Change_Status(girl, "Love", -65)

        python:
            girl.set_temp_status("angry" if girl.gid != "tenny" else "sad", 5 if girl.gid != "tenny" else 6, reason="pregnancy_deny")
            store._npc_pat_accepted = False
            print("[PREGNANCY] %s: npc_paternity order REFUSED (Obed=%d)" % (girl.gid, girl.Obed))

    else:
        # Accepts (Obed >= 950, devastated)
        if girl.gid == "gwen":
            $ set_scene_expression(girl, "sad")
            python:
                _g_acc = _format_partner_line(girl, _("...You want me to look %(pn)s in the eyes. And tell %(po)s this baby is %(poss)s. While you keep..."))
            $ Say_Line(girl, _g_acc)
            $ set_scene_expression(girl, "sad", eyes="eyes_looking_down")
            $ Say_Line(girl, _("...If that's what you want."))
            $ Change_Status(girl, "Love", -100)
        elif girl.gid == "rogue":
            $ set_scene_expression(girl, "sad")
            python:
                _r_acc = _format_partner_line(girl, _("Darlin'... you're asking me to betray %(pn)s in the worst way a person can."))
            $ Say_Line(girl, _r_acc)
            $ set_scene_expression(girl, "sad", eyes="eyes_looking_down")
            $ Say_Line(girl, _("...But I'll do it. God help me, I'll do it."))
            $ Change_Status(girl, "Love", -110)
        elif girl.gid == "ntw":
            $ set_scene_expression(girl, "looking_left")
            python:
                _n_acc = _format_partner_line(girl, _("...Fine. I'll lie to %(po)s. I'll smile and pretend. And I'll hate myself every second."))
            $ Say_Line(girl, _n_acc)
            $ set_scene_expression(girl, "angry")
            $ Say_Line(girl, _("Happy?"))
            $ Change_Status(girl, "Love", -90)
        elif girl.gid == "tenny":
            $ set_scene_expression(girl, "sad")
            python:
                _t_acc = _format_partner_line(girl, _("I-I'll do it... I'll tell %(po)s... even though it's going to eat me alive."))
            $ Say_Line(girl, _t_acc)
            $ set_scene_expression(girl, "sad", eyes="eyes_looking_down")
            $ Say_Line(girl, _("I just... I just wish you cared enough to not ask me to do this."))
            $ Change_Status(girl, "Love", -120)
        else:
            # "_default" voice
            $ set_scene_expression(girl, "sad")
            python:
                _d_acc = _format_partner_line(girl, _("...You want me to tell %(pn)s the baby is %(poss)s. And keep seeing you."))
            $ Say_Line(girl, _d_acc)
            $ set_scene_expression(girl, "sad", eyes="eyes_looking_down")
            $ Say_Line(girl, _("...I'll do it. I hate that I will. But I'll do it."))
            $ Change_Status(girl, "Love", -105)

        python:
            girl.set_temp_status("sad" if girl.gid != "ntw" else "angry", 5 if girl.gid != "tenny" else 6, reason="pregnancy_deny")
            store._npc_pat_accepted = True
            print("[PREGNANCY] %s: npc_paternity order ACCEPTED (Obed=%d)" % (girl.gid, girl.Obed))

    return

# ============================================================
# STEP 5: NPC PARTNER WARNING
# ============================================================

label _pregnancy_npc_lie_suggest(girl):
    # She wants her boyfriend to believe the baby is his (loyal: to keep him / cheater: for the thrill) and he never
    # brought it up: she does. Yes = the same agreed lie as Choice 4; no = her answer, then the usual warning.
    $ _preg_lie_say(girl, "suggest")
    menu:
        "Let him think it's his.":
            $ _preg_npc_pat_confirm(girl, "she suggested it")
            $ _preg_lie_say(girl, "confirm")
        "No. He deserves the truth.":
            $ print("[PREGNANCY] %s: he said no to the lie she suggested" % girl.gid)
            $ _preg_lie_say(girl, "refuse")
    return

label _pregnancy_npc_warning(girl, skip_intro=False):
    # skip_intro: he was just the subject (Step 5 decides: her proposal of the lie, Choice 4, or the partner line that
    # closes Choice 1 / 2): no "one more thing we need to talk about" about the man she was talking about
    python:
        _npc = get_npc_partner_for(girl)
        _w_gid = girl.gid

    if _w_gid == "gwen":
        python:
            _w1 = _format_partner_line(girl, _("There's one more thing we need to talk about. %(Pn)s."))
            _w2 = _format_partner_line(girl, _("I'll hide this from %(po)s for as long as I can. Baggy clothes, avoiding %(po)s... I'll figure it out."))
            _w3 = _format_partner_line(girl, _("But when %(pp)s finds out... and %(pp)s WILL find out... %(pp)s is going to want to strangle you. I'd be ready if I were you."))

    elif _w_gid == "rogue":
        python:
            _w1 = _format_partner_line(girl, _("Sugar... we still gotta deal with %(pn)s."))
            _w2 = _format_partner_line(girl, _("I'll keep this under wraps as long as I can. Oversized hoodies, staying away from %(po)s when I'm sick..."))
            _w3 = _format_partner_line(girl, _("But the second %(pp)s sees my belly, it's over. And %(pp)s'll come for you. I'm warning you now."))

    elif _w_gid == "ntw":
        python:
            _w1 = _format_partner_line(girl, _("And then there's %(pn)s."))
            _w2 = _format_partner_line(girl, _("I'll keep %(po)s in the dark. I'm good at lying."))
            _w3 = _format_partner_line(girl, _("But when %(pp)s figures it out... and %(pp)s's not stupid... %(pp)s'll want your head on a plate. Don't say I didn't warn you."))

    elif _w_gid == "tenny":
        python:
            _w1 = _format_partner_line(girl, _("W-what about %(pn)s? %(Pp)s is going to notice eventually..."))
            _w2 = _format_partner_line(girl, _("I-I'll try to hide it. Loose clothes, staying busy with school..."))
            _w3 = _format_partner_line(girl, _("But %(pp)s is going to find out. And %(pp)s'll be so angry... I'm scared for both of us."))

    else:
        # "_default" voice
        python:
            _w1 = _format_partner_line(girl, _("There's one more thing. %(Pn)s."))
            _w2 = _format_partner_line(girl, _("I'll hide it from %(po)s for as long as I can. Loose clothes, excuses, whatever it takes."))
            _w3 = _format_partner_line(girl, _("But %(pp)s is going to find out. And when %(pp)s does, %(pp)s will come looking for you. Be ready."))

    # said once, after the per-voice chain picked the words; the last line is the threat she fears
    if not skip_intro:
        $ set_scene_expression(girl, "worried", blush=0)
        $ Say_Line(girl, _w1)
    $ set_scene_expression(girl, "worried", eyes="eyes_looking_down")
    $ Say_Line(girl, _w2)
    $ set_scene_expression(girl, _PREG_WARN_FACE.get(_w_gid, _PREG_WARN_FACE["_default"]))
    $ Say_Line(girl, _w3)

    $ _flag_npc_confrontation(girl, "she warned him")
    return

# ============================================================
# PHASE 6: NPC PREGNANCY CONFRONTATION
# ============================================================

label _npc_pregnancy_confrontation:
    python:
        _conf_gid = store._npc_pregnancy_confrontation_pending
        _conf_girl = GIRL_BY_ID.get(_conf_gid)
        if not _conf_girl:
            store._npc_pregnancy_confrontation_pending = None
            print("[PREGNANCY] NPC confrontation: invalid gid %s, clearing" % _conf_gid)
            renpy.return_statement()

        _conf_npc = get_npc_partner_for(_conf_girl)
        if not _conf_npc:
            store._npc_pregnancy_confrontation_pending = None
            print("[PREGNANCY] NPC confrontation: %s has no NPC partner, clearing" % _conf_gid)
            renpy.return_statement()

        _conf_is_ntr = getattr(_conf_npc, "_ntr_active", False) and getattr(_conf_girl, "_ntr_boundary_discovered", False)
        _conf_is_female = _conf_girl.get_flag("partner_is_female")
        _conf_energy = getattr(store.Player, "energy_max", 3)

    # --- Campus arrival ---
    #     The scene IS campus, but it fires with the morning hooks, where he woke up (his room, or hers after a
    #     sleepover): take him there and put the partner in front of him, alone on screen (author, 2026-09-19).
    #     Whoever slept over stays where she woke up.
    python:
        store.Party = []
        _conf_npc.loc = "campus"
        navigate_to("campus", None)
        print("[PREGNANCY] %s: NPC confrontation on campus (partner %s, ntr=%s)" % (_conf_gid, _conf_npc.Name, _conf_is_ntr))
    call Set_Scene(entry=False, show_chars=False) from _call_conf_campus_scene
    "You walk into campus. It's a normal morning. Until it isn't."
    $ _conf_npc.show_sprite(_get_slot_transform_for_index(0, 1))
    with dissolve

    python:
        _npc_char = Character(_conf_npc.Name)

    # the NTR partner has his own opening (leaning on the wall, exhausted): no angry arrival, no second reveal
    if not _conf_is_ntr:
        python:
            _arrive_line = _format_partner_line(_conf_girl, _("%(Pn)s is standing near the entrance. Waiting. Arms crossed. Eyes locked on you."))
        "[_arrive_line]"

        $ _npc_char(_("We need to talk."))

        "The other students can feel the tension. A few of them slow down, watching."

        python:
            _preg_reveal = _tl(_("She's pregnant. %s is pregnant.")) % _conf_girl.Name
        $ _npc_char(_preg_reveal)

        if _conf_is_female:
            $ _npc_char(_("And I know it's not from IMMACULATE CONCEPTION. She's been with a man. With YOU."))
        else:
            $ _npc_char(_("And I KNOW it's not mine."))

    # --- Path routing ---
    if _conf_is_ntr:
        call _npc_confrontation_ntr(_conf_girl, _conf_npc) from _call_conf_ntr
    elif _conf_energy >= 4:
        call _npc_confrontation_strong(_conf_girl, _conf_npc) from _call_conf_strong
    else:
        call _npc_confrontation_weak(_conf_girl, _conf_npc) from _call_conf_weak

    # Every path ends with him walking away: off the screen before the texts, and to HER (her room) for the rest
    # of the slot, or the campus menu would draw him again right after (resolve_npc_for_location)
    python:
        _conf_npc.hide_sprite()
        _conf_npc.loc = girl_home_loc(_conf_gid)
        store._npc_on_scene = None
    with dissolve

    # --- Breakup decision ---
    #     From here on he KNOWS the child is not his. Set BEFORE the breakup: a partner who leaves takes the
    #     flag with him (clear_npc_partner resets the "partner" scope), one who stays keeps it.
    $ _conf_girl._npc_pregnancy_confronted = True
    call _npc_pregnancy_breakup(_conf_girl, _conf_npc) from _call_conf_breakup

    # --- Cleanup ---
    python:
        _conf_girl._npc_pregnancy_confrontation_pending = False
        store._npc_pregnancy_confrontation_pending = None
        print("[PREGNANCY] %s: NPC confrontation complete, partner now at %s" % (_conf_gid, _conf_npc.loc))
    # campus as it really is this morning (who is here, who walks off angry)
    call Set_Scene(entry=True) from _call_conf_campus_after

    return

# ── Path 1: Player Strong (energy_max >= 4) ──

label _npc_confrontation_strong(girl, npc):
    python:
        _npc_char = Character(npc.Name)
        _swing = _format_partner_line(girl, _("%(Pn)s swings at you."))

    "[_swing]"
    "But you see it coming a mile away."

    show layer master at bj_slap_shake

    python:
        _catch = _format_partner_line(girl, _("You catch %(poss)s fist mid-air and twist %(poss)s arm behind %(poss)s back. %(Pp)s stumbles, off balance."))
    "[_catch]"

    $ Say_Player(_("I wouldn't do that if I were you."))

    python:
        _shove = _format_partner_line(girl, _("You shove %(po)s away. %(Pp)s staggers, catches %(po)sself on a bench. A few students gasp. %(Pp)s looks up at you, humiliated, breathing hard."))
    "[_shove]"

    if hasattr(npc, "has_trait") and npc.has_trait("proud"):
        $ _npc_char(_("This isn't over. Not even CLOSE."))
        python:
            _storm = _format_partner_line(girl, _("%(Pp)s storms off, fists clenched."))
        "[_storm]"
    else:
        $ _npc_char(_("..."))
        python:
            _defeat = _format_partner_line(girl, _("%(Pp)s stays there, defeated. Can't even look at you. Walks away."))
        "[_defeat]"

    return

# ── Path 2: Player Weak (energy_max <= 3) ──

label _npc_confrontation_weak(girl, npc):
    python:
        _npc_char = Character(npc.Name)
        _swing = _format_partner_line(girl, _("%(Pn)s swings at you."))

    "[_swing]"
    "You don't react fast enough."

    show layer master at bj_slap_shake

    "The fist connects with your jaw. Hard."

    call _cum_punch_pair("oral") from _call_conf_punch

    python:
        _ground = _format_partner_line(girl, _("You hit the ground. Students scatter. %(Pn)s stands over you, chest heaving."))
    "[_ground]"

    $ _npc_char(_("Stay away from her. Stay away from BOTH of us."))

    if hasattr(npc, "has_trait") and npc.has_trait("proud"):
        $ _npc_char(_("Touch her again and I'll put you in the hospital."))
    else:
        $ _npc_char(_("I trusted you, man. I TRUSTED you."))

    # his last word first, THEN he walks away (he used to leave and keep talking)
    python:
        _spit = _format_partner_line(girl, _("%(Pp)s spits on the ground next to you and walks away."))
    "[_spit]"

    return

# ── Path 3: NTR NPC (active + discovered) ──

label _npc_confrontation_ntr(girl, npc):
    python:
        _npc_char = Character(npc.Name)
        _lean = _format_partner_line(girl, _("%(Pn)s is leaning against the wall near the entrance. %(Pp)s doesn't look angry. %(Pp)s looks... exhausted."))
    "[_lean]"

    $ _npc_char(_("So. She's pregnant."))
    $ _npc_char(_("I figured this would happen eventually. It was always a risk, right?"))

    python:
        _bl = getattr(npc, "_ntr_boundary_level", 1)

    if _bl <= 1:
        $ _npc_char(_("I said no penetration. You did it anyway. And now THIS. I should have known better than to trust any of this."))
    elif _bl == 2:
        $ _npc_char(_("Condoms break, I guess. Or maybe you just didn't bother. Either way... here we are."))
    elif _bl == 3:
        $ _npc_char(_("I said no creampies. No cumming inside. And now she's pregnant. So either you lied, or she's lying. Either way, someone broke the rules."))
    else:
        $ _npc_char(_("I knew the risk. No limits means no limits. I just... didn't think it would actually happen."))

    $ _npc_char(_("I need time to process this. Don't talk to me for a while."))

    python:
        _ntr_walk = _format_partner_line(girl, _("%(Pp)s pushes off the wall and walks away without another word."))
    "[_ntr_walk]"

    python:
        Change_NPC_Status(npc, "friendship_with_player", -100)
        print("[PREGNANCY] %s: NTR NPC confrontation, friendship -100" % girl.gid)

    return

# ============================================================
# PHASE 6: BREAKUP DECISION (Post-Confrontation)
# ============================================================

init python:
    # Proud partner dumps her by text; she tells HIM by text (she is not on campus). _format_partner_line at send.
    _NPC_PREG_PROUD_TEXTS = {
        "gwen": [_("%(Pn)s broke up with me. Just like that. A text message. No explanation needed, I guess."),
                 _("Well... at least I don't have to hide anymore.")],
        "rogue": [_("%(Pn)s ended it. %(Pp)s didn't even want to hear my side."),
                  _("Can't say I blame %(po)s.")],
        "ntw": [_("%(Pn)s dumped me. Good. One less thing to deal with.")],
        "tenny": [_("%(Pn)s... %(pp)s broke up with me. Over text."),
                  _("I-I knew it was coming but it still hurts.")],
        "_default": [_("%(Pn)s ended it. One message, and that was that."),
                     _("I can't even be angry. I did this.")],
    }

# Texts that arrive in front of him: the buzz, each line typed live in the SENDER's own thread (hers, or the NPC
# partner's: npc_phone_text), then the thread stays open until he closes it. phone_add_msg alone only files a
# text in the history: these used to sit unread while "Try to work things out" was asked on screen.
# lines = raw _() strings with partner placeholders; girl = whose partner they name (the NPC sender's girl).
label _preg_live_texts(who, lines, girl=None, buzz=True):
    python:
        _plt_girl = girl or who
        _plt_is_npc = isinstance(who, NPCPartner)
        _plt_lines = [_format_partner_line(_plt_girl, _l) for _l in lines]
        print("[PREGNANCY] live texts from %s: %d" % (getattr(who, "gid", "?"), len(_plt_lines)))
    if buzz:
        play sound "audio/Notification.mp3" noloop
        $ Narration(_("Your phone buzzes. Someone sent you a message."))
    while _plt_lines:
        call _phone_typing(who, choices=[]) from _typing_preg_live
        python:
            if _plt_is_npc:
                npc_phone_text(who, _plt_lines.pop(0))
            else:
                phone_add_msg(who.gid, who.gid, _plt_lines.pop(0), "text")
    call screen phone_chat_screen(who, choices=[])
    return

label _npc_pregnancy_breakup(girl, npc):
    python:
        _npc_char = Character(npc.Name)
        _bu_is_ntr = getattr(npc, "_ntr_active", False) and getattr(girl, "_ntr_boundary_discovered", False)
        _bu_is_proud = hasattr(npc, "has_trait") and npc.has_trait("proud")
        _bu_gid = girl.gid
        _bu_bl = getattr(npc, "_ntr_boundary_level", 1)

    # ── Proud NPC: Immediate breakup ──
    if _bu_is_proud:
        python:
            _breakup_msg = _format_partner_line(girl, _("We're done. Don't call me."))
            # HIS text, in HIS thread: sender = girl.gid in her thread read as the girl dumping the player
            npc_phone_text(npc, _breakup_msg)

        # she is not on campus with him: she texts it (her voice, or "_default")
        call _preg_live_texts(girl, girl_pool(_NPC_PREG_PROUD_TEXTS, girl, "proud breakup texts")) from _call_conf_proud_texts

        python:
            if girl.has_trait("has_boyfriend"):
                girl.remove_trait("has_boyfriend")
            elif girl.has_trait("has_girlfriend"):
                girl.remove_trait("has_girlfriend")
            girl.clear_npc_partner()   # same exit as _npc_process_breakup: removes the NPC, resets the partner-bound pregnancy flags
            girl._npc_breakup_result = "broke_up"
            print("[PREGNANCY] %s: proud NPC -> immediate breakup" % girl.gid)

    # ── NTR NPC: No breakup ──
    elif _bu_is_ntr:
        python:
            # NPC -> PLAYER texts go to the NPC's own thread (npc_phone_text), never the girl's thread
            _ntr_texts = [_("I've been thinking about it. I'm not leaving her."),
                          _("This is messed up. I know that. But I knew what I was getting into.")]
            if _bu_bl <= 2:
                _ntr_texts.append(_("But we need to talk about boundaries again. Because clearly the old ones didn't hold."))
            elif _bu_bl == 3:
                _ntr_texts.append(_("You crossed the line. The ONE line. But... I'll deal with it."))
            else:
                _ntr_texts.append(_("No limits is no limits. Even this. I'll raise the kid."))
        call _preg_live_texts(npc, _ntr_texts, girl=girl) from _call_conf_ntr_texts
        if _bu_bl > 3:
            $ _npc_raises_child(girl, npc, "NTR who knew, no limits")

        python:
            Change_NPC_Status(npc, "friendship_with_player", -50)
            print("[PREGNANCY] %s: NTR NPC stays, friendship -50 (additional), bl=%d" % (girl.gid, _bu_bl))

    # ── Normal NPC: Girl tries to save ──
    else:
        call _preg_live_texts(girl, [
            _("Hey... %(pn)s and I talked last night. It was bad. Really bad."),
            _("But I think... I think I can convince %(po)s not to leave me."),
            _("The thing is... I'm carrying YOUR baby. So what do you think? Should I try to keep things together with %(po)s, or should we just... let it end?"),
        ]) from _call_conf_save_texts

        menu:
            "Try to work things out with [_conf_girl.npc_partner_name].":
                call _preg_live_texts(girl, [_("Okay. I'll talk to %(po)s. I don't know if %(pp)s'll forgive me, but I'll try.")],
                                      buzz=False) from _call_conf_try_text
                python:
                    girl._npc_pregnancy_save_attempt = True
                    Change_NPC_Status(npc, "love_for_girl", -200)
                    Change_NPC_Status(npc, "friendship_with_player", -150)
                    print("[PREGNANCY] %s: normal NPC, girl tries to save relationship" % girl.gid)

            "Let it end. It's better this way.":
                call _preg_live_texts(girl, [_("...Yeah. You're probably right."),
                                             _("I'll tell %(po)s it's over. At least I don't have to lie anymore.")],
                                      buzz=False) from _call_conf_end_texts
                python:
                    if girl.has_trait("has_boyfriend"):
                        girl.remove_trait("has_boyfriend")
                    elif girl.has_trait("has_girlfriend"):
                        girl.remove_trait("has_girlfriend")
                    girl.clear_npc_partner()   # same exit as _npc_process_breakup
                    girl._npc_breakup_result = "broke_up"
                    print("[PREGNANCY] %s: normal NPC, player chose to let it end" % girl.gid)

    return

# ============================================================
# PHASE 7: BIRTH EVENT
# ============================================================

init python:

    # Her texts when labor starts and when she is back on campus (3 each, sent in order).
    # A girl with no voice of her own uses "_default" (girl_pool, pregnancy.rpy).
    # labor starts: she is leaving for about a week
    _PREG_BIRTH_TEXTS = {
        "gwen": [
            _("Hey. So... it's happening. Like, NOW. My water broke in the middle of packing."),
            _("I'm going to my parents' place. My mom's already freaking out. In a good way, I think."),
            _("I'll be gone for about a week. Don't do anything stupid while I'm gone."),
        ],
        "rogue": [
            _("Sugar, it's time. The baby's coming."),
            _("My aunt's already on her way to pick me up. I'm going home for the delivery."),
            _("I'll be back in a week or so. Take care of yourself, okay?"),
        ],
        "ntw": [
            _("Okay so this kid has decided TODAY is the day. Cool. Great timing."),
            _("Going to my mom's. She's the only person I trust not to make this worse."),
            _("Back in a week. Maybe. If this little gremlin cooperates."),
        ],
        "tenny": [
            _("I-I think it's happening... the contractions started..."),
            _("My dad is driving me to the hospital. Grandpa is right behind us in the RV, and I can hear him honking at everyone."),
            _("I'll be at my parents' place for a week after. I'm s-scared but... I'll be okay. I think."),
        ],
        "_default": [
            _("It's happening. The baby is coming. Right now."),
            _("My family is taking me home for the delivery. They have everything ready."),
            _("I'll be gone for about a week. I'll text you when I'm back."),
        ],
    }

    # a week later: she is back, the baby stays with her family
    _PREG_RETURN_TEXTS = {
        "gwen": [
            _("I'm back! The baby is with my parents. They're already obsessed."),
            _("My mom has taken approximately 400 photos. The kid isn't even a week old."),
            _("I'm exhausted but... I missed campus. And you. Don't let that go to your head."),
        ],
        "rogue": [
            _("Hey sugar. I'm back on campus."),
            _("Left the baby with my aunt. Hardest thing I've ever done, walking out that door."),
            _("But my aunt's got it handled. She's already got a schedule, a routine, and a list of rules longer than my arm."),
        ],
        "ntw": [
            _("I'm back. The tiny human has been deposited with my mother."),
            _("She cried when I left. My mom, not the baby. The baby was asleep. Figures."),
            _("Don't ask me how I'm feeling. I'm fine. Totally fine. Shut up."),
        ],
        "tenny": [
            _("I-I'm back... I left the baby with my parents. And grandpa, who has basically moved in."),
            _("He already bought a little lab coat for the baby. And a periodic table mobile for the crib."),
            _("I cried the whole bus ride back. But I need to finish my degree. For both of us now."),
        ],
        "_default": [
            _("I'm back on campus."),
            _("The baby is with my family. They're already in love."),
            _("Leaving was the hardest thing I've ever done. But I'm here, and I'm okay."),
        ],
    }

    def _preg_send_texts(girl, table):
        """Queue her texts in her own phone thread: her voice, or "_default"."""
        for _msg in girl_pool(table, girl, "birth / return texts"):
            # phone_add_msg stores the text verbatim and nothing translates it at display time: _tl HERE
            # (these texts used to be stored as bare _() and stayed English in PT / ES)
            phone_add_msg(girl.gid, girl.gid, _tl(_msg), "text")

label _pregnancy_birth:
    python:
        _birth_gid = store._pregnancy_birth_pending
        _birth_girl = GIRL_BY_ID.get(_birth_gid)
        if not _birth_girl:
            store._pregnancy_birth_pending = None
            print("[PREGNANCY] birth: invalid gid %s, clearing" % _birth_gid)
            renpy.return_statement()

    # Phone message from girl announcing she's leaving
    $ _preg_send_texts(_birth_girl, _PREG_BIRTH_TEXTS)

    if getattr(_birth_girl, "_pregnancy_count", 0) > 0:
        "You get a series of messages. [_birth_girl.Name] is having another baby."
    else:
        "You get a series of messages. [_birth_girl.Name] is having the baby."
    "She'll be gone for about a week."

    # NPC partner notification (if claimed paternity)
    python:
        _birth_npc = get_npc_partner_for(_birth_girl) if callable(globals().get("get_npc_partner_for", None)) else None
        if _birth_npc and getattr(_birth_girl, "_npc_paternity_claimed", False):
            _npc_birth_char = Character(_birth_npc.Name)

    if _birth_npc and getattr(_birth_girl, "_npc_paternity_claimed", False):
        python:
            _npc_birth_msg = _("She just told me. The baby's coming. I'm heading to the hospital.")
            npc_phone_text(_birth_npc, _npc_birth_msg)
            # a female partner gets here through NTR boundary level 4 ("I'll raise the kid")
            _npc_birth_narr = _format_partner_line(_birth_girl, _("You also see a message from %(pn)s. %(Pp)s's rushing to be there."))
            print("[PREGNANCY] %s: birth, partner %s notified (paternity claimed)" % (_birth_girl.gid, getattr(_birth_npc, "Name", "?")))
        "[_npc_birth_narr]"

    # her husband (shion_pregnancy.rpy): he texts from the hospital this morning (Wait 6zz2)
    python:
        if pregnancy_husband(_birth_girl) is store.Dad:
            store._dad_text_pending = "baby_labor"
            print("[PREGNANCY] %s: birth, her husband texts from the hospital" % _birth_girl.gid)

    python:
        # next announcement of the same morning (label Wait loops while this is set), else None
        store._pregnancy_birth_pending = _pregnancy_next_birth()
        print("[PREGNANCY] %s: birth event complete, girl away for 7 days (next announcement: %s)" % (_birth_gid, store._pregnancy_birth_pending))

    return

# ============================================================
# PHASE 7: RETURN EVENT (7 days after birth)
# ============================================================

label _pregnancy_return:
    python:
        _ret_gid = store._pregnancy_return_pending
        _ret_girl = GIRL_BY_ID.get(_ret_gid)
        if not _ret_girl:
            store._pregnancy_return_pending = None
            print("[PREGNANCY] return: invalid gid %s, clearing" % _ret_gid)
            renpy.return_statement()

    # Per-girl return phone message
    $ _preg_send_texts(_ret_girl, _PREG_RETURN_TEXTS)

    if girl_off_campus(_ret_girl):
        "You get a message from [_ret_girl.Name]. She's back home."
        "The baby is home with her."
    else:
        "You get a message from [_ret_girl.Name]. She's back on campus."
        "The baby is with her family."

    # her husband (shion_pregnancy.rpy): they are home with the baby, with a doubt if the calls left him suspicious
    python:
        _ret_h = pregnancy_husband(_ret_girl)
        if _ret_h is store.Dad:
            store._dad_text_pending = "baby_home_doubt" if getattr(_ret_h, "suspicion", 0) >= PREG_HUSBAND_DOUBT else "baby_home"
            print("[PREGNANCY] %s: home with the baby, her husband texts '%s' (suspicion %d)" % (_ret_girl.gid, store._dad_text_pending, getattr(_ret_h, "suspicion", 0)))

    # The child exists from now on, the pregnancy is over, she is back on the map (state: pregnancy.rpy)
    python:
        pregnancy_return_apply(_ret_girl)
        # another girl whose week ends today (label Wait loops while this is set), else None
        store._pregnancy_return_pending = _pregnancy_next_return()

    return
