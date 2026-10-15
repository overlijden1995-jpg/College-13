# ============================================================
# CHEAT GUILT SYSTEM
# After a girl cheats on her BF for the first time, she feels
# guilty and asks the player to leave. She gets "sad" status
# for the rest of the day which resets the next morning.
# Cheater trait girls skip this entirely.
# ============================================================

init python:

    # Narration shown when a sad girl is encountered at a location
    SAD_NARRATION = {
        "cheat_guilt": [
            _("She seems lost in thought. The guilt is clearly weighing on her."),
            _("She won't even look at you. Whatever happened between you two is still fresh."),
            _("She's avoiding eye contact. Give her some time to process what happened."),
        ],
        "cheat_escalation": [
            _("She looks distracted. Something is clearly on her mind."),
            _("She glances at you and quickly looks away. She needs more time."),
            _("She seems conflicted. Better give her space until tomorrow."),
        ],
    }

    # =============================================================
    # BISEXUAL+GF POST-PROCESSING
    # Swaps male partner references for female ones in translated text.
    # For lines with male anatomy content, _CHEAT_GF_ALT provides
    # full replacements keyed by the original English string.
    # =============================================================

    _CHEAT_GF_SUBS_EN = [
        ("{hint}boyfriend{/hint}", "{hint}girlfriend{/hint}"),
        ("boyfriend", "girlfriend"), ("Boyfriend", "Girlfriend"),
        ("another man's cock", "another person"),
        ("another man", "another woman"), ("a REAL man", "a REAL woman"),
        ("The man", "The woman"), ("the man", "the woman"),
        ("a man", "a woman"), ("a MAN", "a WOMAN"),
        ("a guy", "a girl"),
        (" HE ", " SHE "), (" He ", " She "), ("He ", "She "), (" he ", " she "),
        (" he.", " she."), (" he,", " she,"), (" he!", " she!"), (" he?", " she?"),
        ("He'd", "She'd"), (" he'd", " she'd"), ("He'll", "She'll"), (" he'll", " she'll"),
        ("HE's", "SHE's"), ("He's", "She's"), (" he's", " she's"),
        (" HIM.", " HER."), (" HIM,", " HER,"), (" HIM ", " HER "),
        (" him ", " her "), (" him.", " her."), (" him,", " her,"), (" him!", " her!"), (" him?", " her?"),
        (" his ", " her "), (" his.", " her."), (" his,", " her,"),
        ("His ", "Her "), (" HIS ", " HER "),
        (" himself", " herself"),
    ]

    _CHEAT_GF_SUBS_PT = [
        ("meu {hint}namorado{/hint}", "minha {hint}namorada{/hint}"),
        ("Meu {hint}namorado{/hint}", "Minha {hint}namorada{/hint}"),
        ("o {hint}namorado{/hint}", "a {hint}namorada{/hint}"),
        ("O {hint}namorado{/hint}", "A {hint}namorada{/hint}"),
        ("ao {hint}namorado{/hint}", "à {hint}namorada{/hint}"),
        ("{hint}namorado{/hint}", "{hint}namorada{/hint}"),
        (" namorado", " namorada"),
        ("Namorado", "Namorada"),
        ("O homem", "A mulher"), ("o homem", "a mulher"),
        ("outro homem", "outra pessoa"),
        ("um homem", "uma mulher"), ("um cara", "uma garota"),
        ("um HOMEM", "uma MULHER"),
        (" DELE ", " DELA "), (" DELE.", " DELA."),
        (" dele ", " dela "), (" dele.", " dela."), (" dele,", " dela,"),
        (" Dele ", " Dela "),
        (" ELE ", " ELA "), (" ELE!", " ELA!"),
        (" ele ", " ela "), (" ele.", " ela."), (" ele,", " ela,"), (" ele!", " ela!"), (" ele?", " ela?"),
        ("Ele ", "Ela "), ("ELE ", "ELA "),
    ]

    _CHEAT_GF_SUBS_ES = [
        ("mi {hint}novio{/hint}", "mi {hint}novia{/hint}"),
        ("Mi {hint}novio{/hint}", "Mi {hint}novia{/hint}"),
        ("el {hint}novio{/hint}", "la {hint}novia{/hint}"),
        ("El {hint}novio{/hint}", "La {hint}novia{/hint}"),
        ("al {hint}novio{/hint}", "a la {hint}novia{/hint}"),
        ("{hint}novio{/hint}", "{hint}novia{/hint}"),
        (" novio", " novia"), ("Novio", "Novia"),
        ("El hombre", "La mujer"), ("el hombre", "la mujer"),
        ("otro hombre", "otra persona"),
        ("un hombre", "una mujer"), ("un tipo", "una chica"),
        ("un HOMBRE", "una MUJER"),
        (" de ÉL ", " de ELLA "), (" de ÉL.", " de ELLA."),
        (" de él ", " de ella "), (" de él.", " de ella."), (" de él,", " de ella,"),
        (" De él ", " De ella "),
        (" ÉL ", " ELLA "), (" ÉL!", " ELLA!"),
        (" él ", " ella "), (" él.", " ella."), (" él,", " ella,"), (" él!", " ella!"), (" él?", " ella?"),
        ("Él ", "Ella "), ("ÉL ", "ELLA "),
    ]

    # by language code (renpy.game.preferences.language): a language without a table (Russian) writes the partner keys
    # of _format_partner_line in its translations instead (its nouns decline, a word swap cannot follow them)
    _CHEAT_GF_SUBS = {None: _CHEAT_GF_SUBS_EN, "pt": _CHEAT_GF_SUBS_PT, "es": _CHEAT_GF_SUBS_ES}

    def _cheat_gf_sub(girl, line):
        """Post-process TRANSLATED cheat dialogue for a female partner (_CHEAT_GF_SUBS of the language)."""
        if not line or not girl.get_flag("partner_is_female"):
            return line
        for old, new in _CHEAT_GF_SUBS.get(renpy.game.preferences.language, ()):
            line = line.replace(old, new)
        return line

    _CHEAT_GF_ALT = {
        _("Your... it's bigger than his. I just want to feel it against me. That's all. MY choice."):
            _("You're making me feel things she never could. I just want more of this. MY choice."),
        _("Mmm... it's so much bigger... I can feel every inch even from the outside..."):
            _("Mmm... this is so different from what I'm used to... I can feel everything even from the outside..."),
        _("I need to feel it... just a taste. Then I'll know if his is really that different. MY rules."):
            _("I need to feel it... just a taste. I need to know what this is really like. MY rules."),
        _("It's... it's SO much thicker than his... I just need a second to... to process..."):
            _("It's... nothing like being with her... I can't even think straight..."),
        _("So much bigger... so much deeper... I was fooling myself thinking I was in control..."):
            _("So different... so much more intense... I was fooling myself thinking I was in control..."),
        _("He has NO idea his girlfriend is moaning like this for someone else's cock..."):
            _("She has NO idea her girlfriend is moaning like this for a guy..."),
        _("His cock is in my ass and I'm the one who decided that... I'm still in charge..."):
            _("A guy is in my ass because I decided that... I'm still in charge..."),
        _("He BEGGED me for anal for months and I always said no. And this guy gets it first time asking."):
            _("She always wanted to try new things with me... but I never let her go this far. And this guy gets it first try."),
        _("Just the tip... consider it research. Seeing how a REAL man feels."):
            _("Just the tip... consider it research. Seeing how a guy actually feels."),
        _("Every time I think of his pathetic effort compared to THIS... I get even wetter..."):
            _("Every time I think of her gentle touch compared to THIS... I get even wetter..."),
        _("This isn't real... it's my ass... it's not like he's actually inside me... not REALLY..."):
            _("This isn't real... it's my ass... it's not like a guy is actually inside me... not REALLY..."),
        _("I was just... curious. I've been wanting to know what it felt like. Yours is... bigger than his."):
            _("I was just... curious. I've been wanting to know what it felt like with a guy. And... wow."),
        _("His dick never made me want to... to do THAT. But yours... I couldn't stop myself."):
            _("She never made me want to... to do THAT. But you... I couldn't stop myself."),
        _("If he ever finds out I put another man's cock in my mouth... he'd die."):
            _("If she ever finds out I had a guy's cock in my mouth... she'd die."),
        _("He can't even be bothered to touch me properly. So yeah, I put another man's cock in my mouth. Sue me."):
            _("She can't give me what I need. So yeah, I had a guy's cock in my mouth. Sue me."),
        _("It took everything in me to stop at the tip... he's so much bigger than my {hint}boyfriend{/hint}..."):
            _("It took everything in me to stop at the tip... he's so different from my {hint}girlfriend{/hint}..."),
        _("Just the tip of someone else's cock because my {hint}boyfriend{/hint} can't be bothered. Poetic."):
            _("The tip of a guy's cock while my {hint}girlfriend{/hint} has no idea. Poetic."),
        _("My {hint}boyfriend{/hint} begged me for anal for MONTHS and I always said no. But this guy? First time asking. He got it."):
            _("My {hint}girlfriend{/hint} never even asked to touch me there... I'd thought about it... but now this guy got there first."),
        _("He wanted my ass so bad... well, someone else has it now. And honestly? It felt amazing. His loss."):
            _("She never tried anything like this with me... and now a guy gets to do it first. Honestly? It felt amazing. Her loss."),
        _("Anal with another man while my {hint}boyfriend{/hint} is at home thinking I'm out with friends. This is the revenge he earned."):
            _("Anal with a guy while my {hint}girlfriend{/hint} is at home thinking I'm out with friends. This is what she gets for ignoring me."),
        _("You know my cock is way better than his."):
            _("I can give you something she never could."),
        _("I don't care anymore! FUCK ME! I'm cheating and I DON'T CARE! I just want your dick inside me RAW!"):
            _("I don't care anymore! FUCK ME! I'm cheating and I DON'T CARE! I just want to feel you RAW!"),
        _("This is what happens when you ignore your girlfriend... she finds someone who won't."):
            _("This is what happens when you ignore your girlfriend... she finds a guy who won't."),
        _("No condom... I let him inside me with NOTHING. That's not a mistake, that's a choice I made. Oh god."):
            _("No condom... I let him inside me with NOTHING. That's not a mistake, that's a choice I made. Oh god."),
        _("I let him put it in my ass... I've never even done that with my {hint}boyfriend{/hint}. What does that say about me?"):
            _("I let him put it in my ass... I've never even done that with my {hint}girlfriend{/hint}. What does that say about me?"),
        _("No condom. I let him go raw inside me. I didn't even TRY to stop it. What happened to being in charge?"):
            _("No condom. I let him go raw inside me. I didn't even TRY to stop it. What happened to being in charge?"),
        _("I was supposed to set boundaries... and instead I let him fuck me raw. I couldn't even manage that much."):
            _("I was supposed to set boundaries... and instead I let him fuck me raw. I couldn't even manage that much."),
        _("Letting him have my ass wasn't the plan. I was supposed to be in charge... instead I'm bent over for him."):
            _("Letting him have my ass wasn't the plan. I was supposed to be in charge... instead I'm bent over for him."),
        _("I let him fuck me raw. My {hint}boyfriend{/hint} hasn't touched me in weeks but THIS guy gets the full experience? Sounds about right."):
            _("I let him fuck me raw. My {hint}girlfriend{/hint} hasn't touched me in weeks but THIS guy gets the full experience? Sounds about right."),
    }

    def _cheat_partner_label(girl):
        """Her partner word for player menu text, translated (girl.partner_label)."""
        return girl.partner_label()

    def _cheat_gf_resolve(girl, line):
        """If girl has female partner and line has a GF override, return the override."""
        if girl.get_flag("partner_is_female") and line in _CHEAT_GF_ALT:
            return _CHEAT_GF_ALT[line]
        return line

    def _cheat_line(girl, line):
        """Full pipeline: GF override → translate (+ the partner keys a translation may carry) → GF pronoun sub."""
        _resolved = _cheat_gf_resolve(girl, line)
        if _resolved is not line:
            return _format_partner_line(girl, _resolved)
        return _cheat_gf_sub(girl, _format_partner_line(girl, line))

    def get_sad_narration(girl):
        """Return a narration hint based on the girl's sad reason."""
        reason = girl.get_temp_status_reason("sad") if hasattr(girl, "get_temp_status_reason") else None
        if reason and reason in SAD_NARRATION:
            # translated here: every caller shows it as is ("[_sad_narr]", renpy.say)
            return _tl(renpy.random.choice(SAD_NARRATION[reason]))
        return None

    # Lines the sad girl says when the player tries to approach her
    _SAD_LEAVE_LINES = [
        _("Sorry... I don't want to talk right now. Can we talk tomorrow?"),
        _("Not now, please. I just... need to be alone for a bit."),
        _("I'm fine, I just... I need some space. Tomorrow, okay?"),
        _("Please don't. I can't look at you right now without thinking about what I did."),
        _("I need to think. Just... give me until tomorrow."),
    ]

# ============================================================
# GUILT SCENE -- called after sex scene ends
# ============================================================
label cheat_guilt_scene(girl):

    $ _cg_action = getattr(store, "_cheat_guilt_action", "sex")

    # Pick scenario based on action weight
    python:
        _cg_tier = _cheat_action_tier(_cg_action) if callable(_cheat_action_tier) else 1

    # Show her standing in the room with sad expression
    $ set_girl_sprite(girl.gid, pose="standing", at_list=[slot_center])
    $ set_scene_expression(girl, "sad")

    # --- SCENARIO 1: Light acts (kiss, touch) -- she freezes up ---
    if _cg_tier <= 1:
        "..."
        "A heavy silence falls between you."

        if girl.get_flag("tod_kiss_done"):
            $ set_scene_expression(girl, "looking_left")
            $ Say_Line(girl, _cheat_line(girl, _("That time in the game... I told myself it was just a dare. It didn't count. But this... this was real.")))
            $ set_scene_expression(girl, "sad")

        python:
            _cg_lines = [
                _("What did I just do... I have a {hint}boyfriend{/hint}."),

                _("Oh god. I kissed you. I actually kissed you. He would be devastated."),
                _("That shouldn't have happened. I... I need to go."),
                _("I can't believe I let that happen. What kind of person am I?"),
                _("This was a mistake. A huge mistake."),
            ]
        $ Say_Line(girl, _cheat_line(girl, renpy.random.choice(_cg_lines)))

        "She pulls away, her hands trembling slightly."

        python:
            _cg_exit = [
                _("You need to leave. Now. Please."),
                _("Get out. I'm serious. I can't look at you right now."),
                _("Leave. I need to be alone. Don't come back today."),
            ]
        $ Say_Line(girl, _cheat_line(girl, renpy.random.choice(_cg_exit)))

    # --- SCENARIO 2: Medium acts (hj, tj, bj) -- shame and panic ---
    elif _cg_tier <= 3:
        "..."
        "She suddenly goes quiet. The energy in the room shifts completely."

        python:
            _act_names = {"hj": _("that"), "tj": _("that"), "bj": _("that with my mouth")}
            _cg_act_ref = _tl(_act_names.get(_cg_action, _("that")))
            _cg_lines = [
                _tl(_("I can't believe I just did {0} to someone who isn't my {hint}boyfriend{/hint}...")).replace("{0}", _cg_act_ref),
                _("What is WRONG with me? I have a {hint}boyfriend{/hint} and I just... oh god."),

                _("He trusts me. My {hint}boyfriend{/hint} trusts me and I just did THIS."),

                _("I feel sick. I literally feel sick. What did I just do?"),
                _("This is so much worse than a kiss. I actually... oh no. Oh no no no."),
            ]
        $ Say_Line(girl, _cheat_line(girl, renpy.random.choice(_cg_lines)))

        "Her face goes pale. She can't even look at you."

        python:
            if store.CurrentLocation == GIRL_ROOMS.get(girl.gid, ""):
                _cg_exit = [
                    _("Get OUT! I can't... I can't have you here right now!"),
                    _("Leave! Just get out of my room! I need to think!"),
                    _("Go. NOW. Before I start crying. Please just go."),
                ]
            else:
                _cg_exit = [
                    _("I can't be here right now. I need to go. Don't follow me."),
                    _("I have to leave. I can't... I can't stay here with you."),
                    _("I'm going. Don't come after me. Please."),
                ]
        $ Say_Line(girl, _cheat_line(girl, renpy.random.choice(_cg_exit)))

    # --- SCENARIO 3: Heavy acts (sex, anal) -- full breakdown ---
    else:
        "..."
        "The moment it's over, something changes in her eyes."

        python:
            _cg_lines = [
                _("I just cheated on my {hint}boyfriend{/hint}. I actually had sex with someone else."),

                _("Oh my god... I let you inside me. While he's out there thinking I'm faithful."),
                _("What have I done? I can't take this back. I can NEVER take this back."),
                _("He's going to find out. Someone always finds out. And I deserve it."),
                _("I'm the worst person alive. My {hint}boyfriend{/hint} loves me and I just... with you..."),

            ]
        $ Say_Line(girl, _cheat_line(girl, renpy.random.choice(_cg_lines)))

        "She's shaking. Tears are forming in the corners of her eyes."

        $ set_scene_expression(girl, "scared")
        python:
            _cg_lines2 = [
                _("I can still feel you. Every second of it. And the worst part is... part of me liked it."),
                _("How am I supposed to look him in the eye tonight? How?"),
                _("Don't touch me. Don't you DARE touch me right now."),
            ]
        $ Say_Line(girl, _cheat_line(girl, renpy.random.choice(_cg_lines2)))

        python:
            if store.CurrentLocation == GIRL_ROOMS.get(girl.gid, ""):
                _cg_exit = [
                    _("GET OUT! GET OUT OF MY ROOM! NOW!"),
                    _("Leave! I can't... I need to shower. I need to... just GET OUT!"),
                    _("I need you gone. Right now. I can't breathe with you in here."),
                ]
            else:
                _cg_exit = [
                    _("I need to get out of here. I need to go home. NOW."),
                    _("Don't touch me. Don't follow me. I'm leaving."),
                    _("I can't be here. I can't look at you. I have to go."),
                ]
        $ Say_Line(girl, _cheat_line(girl, renpy.random.choice(_cg_exit)))

    # Clean up witness/threesome state before outfit restore
    $ _sex_menu_exit_cleanup(silent=True)

    # Restore her clothes
    $ girl.RestoreOutfit()

    # --- Set sad status (expires at end of today) ---
    $ girl.set_temp_status("sad", days=1, reason="cheat_guilt")

    if girl in store.Party:
        $ store.Party.remove(girl)

    $ hide_girl_sprite(girl)

    python:
        _home = girl_home_loc(girl)
        _in_her_room = (store.CurrentLocation == _home)

    if _in_her_room:
        # In her room: she kicks the player out
        scene bg Door
        with dissolve
        "She shoves you out of her room and slams the door behind you."
        "You hear the lock click."
        "Maybe you should give her some space until tomorrow."
    else:
        # Outside her room: she runs away
        python:
            _loc_names = {
                "campus": _("across campus"), "pool": _("from the pool"), "showers": _("out of the showers"),
                "gym": _("out of the gym"), "classroom": _("out of the classroom"), "room": _("out of your room"),
                "mall": _("out of the mall"),
            }
            _loc_desc = _loc_names.get(store.CurrentLocation, _("away"))
        "Without another word, she grabs her things and runs [_loc_desc]."
        "You watch her disappear. She's heading straight to her room."
        "You won't be seeing her for the rest of the day. Maybe give her space until tomorrow."

    # Move girl to her room
    python:
        girl.loc = _home
        _cg_in_hangout = bool([g for g in _live_hangout_girls() if g.gid != girl.gid])
        # she is gone: the act loop dies with the scene, and the coercion never leaks forward
        store._sex_session_over = True
        store._coercion_type = None
        store._coercion_type_for_post = None

    if not _cg_in_hangout:
        $ navigate_to("campus", None)
        call Set_Scene(entry=True) from _call_Set_Scene_cheat_guilt

    return

# ============================================================
# CHEAT ESCALATION SCENE
# Fires when a girl escalates to a new cheating tier (2 or 3)
# for the first time. 3 narrative paths weighted by traits.
# Cheater trait girls skip this entirely.
# ============================================================

init python:

    def _pick_escalation_path(girl):
        """Pick one of 3 escalation paths, weighted by traits.
        Avoids duplicating paths already assigned to other bf girls
        until all 3 paths are taken (3+ girls with bf).
        Path 1 (innocent): 'it's just like a massage, not cheating'
        Path 2 (tempted):  'his is bigger, I'm curious, I'm in control'
        Path 3 (excuse):   'I'm bored/ignored, I'll spice things up'
        """
        # Collect paths already assigned to other bf girls
        _taken = set()
        for _og in ALL_GIRLS:
            if _og.gid == girl.gid:
                continue
            _op = getattr(_og, "_cheat_escalation_path", 0)
            if _op in (1, 2, 3):
                _taken.add(_op)

        # Available paths (not yet used by other girls)
        _available = [p for p in (1, 2, 3) if p not in _taken]

        # If all 3 are taken (3+ bf girls), allow any path again
        if not _available:
            _available = [1, 2, 3]

        # Weight by traits within available paths
        weights = {}
        for p in _available:
            weights[p] = 30
        if 1 in weights and (girl.has_trait("cute_sex") or girl.has_trait("loyal")):
            weights[1] += 40
        if 2 in weights and (girl.has_trait("hardcore_sex") or girl.has_trait("cum_slut")):
            weights[2] += 40
        if 3 in weights and (girl.has_trait("public_fetish") or girl.has_trait("exhibitionist")):
            weights[3] += 40

        # Weighted random pick from available paths
        total = sum(weights.values())
        roll = renpy.random.randint(1, total)
        cumulative = 0
        for p, w in weights.items():
            cumulative += w
            if roll <= cumulative:
                return p
        return _available[0]

    # =============================================================
    # CHEAT STAGE SYSTEM — progressive gating for path 1
    # Stages: 0=nothing, 1=did rub, 2=did tip, 3=did condom sex
    # =============================================================

    def _is_cheat_path1(girl):
        """Check if this girl is on cheat path 1 with a boyfriend.
        Returns False once she has broken (no longer requires condom)."""
        if not _is_bf_context(girl):
            return False
        if hasattr(girl, "has_trait") and girl.has_trait("cheater"):
            return False
        if getattr(girl, "_cheat_broke", False):
            return False  # she broke — condom no longer forced
        return getattr(girl, "_cheat_escalation_path", 0) == 1

    def _cheat_stage(girl):
        """Return current cheat stage (0-3)."""
        s = getattr(girl, "_cheat_sex_stage", 0)
        debug_log("[DEBUG] _cheat_stage: gid=%s stage=%s" % (girl.gid, s))
        return s

    def _advance_cheat_stage(girl, stage):
        """Advance stage if higher than current. Sets session flags ONLY when stage actually advances (first time doing this act)."""
        current = getattr(girl, "_cheat_sex_stage", 0)
        debug_log("[DEBUG] _advance_cheat_stage: gid=%s current=%s target=%s" % (girl.gid, current, stage))
        if stage > current:
            girl._cheat_sex_stage = stage
            debug_log("[DEBUG] _advance_cheat_stage: ADVANCED to %s" % stage)
            # Only set session flag when truly advancing (first time)
            if stage == 1:
                store._cheat_rub_just_done = True
                debug_log("[DEBUG] _advance_cheat_stage: _cheat_rub_just_done = True")
            elif stage == 2:
                store._cheat_tip_just_done = True
                debug_log("[DEBUG] _advance_cheat_stage: _cheat_tip_just_done = True")

    def _cheat_path1_can_tip(girl):
        """Path 1: tip only allowed after rub."""
        return _cheat_stage(girl) >= 1

    def _cheat_path1_can_sex(girl):
        """Path 1: sex only allowed after tip."""
        return _cheat_stage(girl) >= 2

    def _is_on_cheat_path(girl):
        """True if girl has a boyfriend and is not a cheater trait.
        Auto-assigns a path if she has a BF but no path yet.
        Returns False if NTR is discovered (partner knows and accepted)."""
        if not _is_bf_context(girl):
            return False
        if hasattr(girl, "has_trait") and girl.has_trait("cheater"):
            return False
        if hasattr(girl, "has_trait") and girl.has_trait("lesbian"):
            return False
        if getattr(girl, "_ntr_boundary_discovered", False):
            return False
        # Auto-assign path if she has BF but no path yet
        if not getattr(girl, "_cheat_escalation_path", 0):
            girl._cheat_escalation_path = _pick_escalation_path(girl)
            girl._cheat_sex_stage = 0
            girl._cheat_broke = False
            girl._cheat_heat = 0
            girl._cheat_heat_peak = 0
        return getattr(girl, "_cheat_escalation_path", None) in (1, 2, 3)

    # =============================================================
    # CHEAT HEAT SYSTEM — insistence / temptation accumulator (0-100)
    # Allows bypassing stage gates when high enough.
    # Does NOT replace stat-based approval (Love/Obed/Inbt).
    # =============================================================

    _CHEAT_ACT_TIER = {
        "kiss": 1, "touch": 1, "masturbate": 1,
        "hj": 2, "tj": 2,
        "bj": 3,
        "rub": 4, "tip": 4,
        "sex": 5, "cowgirl": 5, "reverse_cowgirl": 5, "doggy": 5,
        "anal": 6,
    }

    # Central heat table: (success, denied) per action.
    # ALL heat amounts live here — call sites use _notify_cheat_heat().
    _CHEAT_HEAT_TABLE = {
        # Flirt / interaction: only denials build heat
        "flirt":            (0, 1),
        "steal_kiss":       (0, 2),
        "kiss":             (0, 2),
        "lewd_flirt":       (0, 3),
        "touch":            (0, 2),
        "masturbate":       (0, 3),
        "hj":               (0, 3),
        "tj":               (0, 3),
        "bj":               (0, 5),
        "rub":              (0, 5),
        "tip":              (0, 6),
        "sex":              (0, 8),
        "anal":             (0, 8),
        # Scene completions: RELIEVE heat (negative = subtract)
        "scene_rub":        (-10, 0),
        "scene_tip":        (-12, 0),
        "scene_sex":        (-15, 0),
        "scene_anal":       (-20, 0),
        "scene_hj":         (-8, 0),
        "scene_tj":         (-8, 0),
        "scene_bj":         (-10, 0),
        # Gate denials (player pushes past cheat stage)
        "gate_tip":         (0, 5),
        "gate_sex":         (0, 8),
        "gate_anal":        (0, 8),
        # Counter-offer outcomes
        "counter_accept":   (-15, 0),
        "counter_refuse":   (10, 0),
        "no_counter":       (5, 0),
        # Special triggers
        "high_temptation":  (5, 0),
        "bf_flirt":         (0, 1),
    }

    def _cheat_highest_tier_done(girl):
        """Return the highest act tier the girl has done (via intimacy_flags)."""
        flags = getattr(girl, "intimacy_flags", set()) or set()
        best = 0
        for act in flags:
            best = max(best, _CHEAT_ACT_TIER.get(act, 0))
        return best

    def _cheat_effective_heat(girl):
        """Return effective heat: max of current heat and 70% of peak."""
        current = getattr(girl, "_cheat_heat", 0)
        peak = getattr(girl, "_cheat_heat_peak", 0)
        return max(current, int(peak * 0.7))

    def _cheat_heat_threshold(girl, skip_type):
        """Calculate heat threshold for a given skip, adjusted by stats/traits/path."""
        _bases = {
            "skip_to_tip":     70,
            "skip_s1_to_sex":  70,
            "skip_s0_to_sex":  85,
            "skip_s2_to_anal": 75,
            "skip_s1_to_anal": 90,
            "skip_s0_to_anal": 95,
        }
        base = _bases.get(skip_type, 90)

        # Stats reduce threshold (max -20 at score 1000)
        score = get_action_score(girl, "sex") if callable(get_action_score) else 0
        stat_discount = int(score / 1000.0 * 20)

        # Trait modifiers
        trait_mod = 0
        if hasattr(girl, "has_trait"):
            if girl.has_trait("hardcore_sex"):
                trait_mod -= 10
            if girl.has_trait("cheater"):
                trait_mod -= 30
            if girl.has_trait("cute_sex"):
                trait_mod += 8
            if girl.has_trait("loyal"):
                trait_mod += 15

        # Path modifier: path 2 (tempted) easiest, path 1 (innocent) hardest
        path = getattr(girl, "_cheat_escalation_path", 0)
        path_mod = {1: 5, 2: -8, 3: -3}.get(path, 0)

        result = base - stat_discount + trait_mod + path_mod
        return max(20, min(95, result))

    def _add_cheat_heat(girl, amount, reason=""):
        """Add heat with trait/path multipliers and session cap."""
        mult = 1.0
        if hasattr(girl, "has_trait"):
            if girl.has_trait("hardcore_sex"):
                mult *= 1.3
            if girl.has_trait("cheater"):
                mult *= 2.0
            if girl.has_trait("loyal"):
                mult *= 0.5
            if girl.has_trait("cute_sex"):
                mult *= 0.8

        path = getattr(girl, "_cheat_escalation_path", 0)
        if path == 2:
            mult *= 1.2
        elif path == 1:
            mult *= 0.9

        final = max(1, int(amount * mult))

        # Session cap: after 30 gained this session, efficiency drops to 1/5
        session_gained = getattr(store, "_cheat_heat_session_gained", 0)
        if session_gained >= 30:
            final = max(1, final // 5)

        old = getattr(girl, "_cheat_heat", 0)
        girl._cheat_heat = min(100, old + final)

        # Update peak
        peak = getattr(girl, "_cheat_heat_peak", 0)
        if girl._cheat_heat > peak:
            girl._cheat_heat_peak = girl._cheat_heat

        store._cheat_heat_session_gained = session_gained + final
        debug_log("[DEBUG] _add_cheat_heat: gid=%s +%s (raw %s, mult %.1f) reason=%s total=%s peak=%s session=%s" % (
            girl.gid, final, amount, mult, reason, girl._cheat_heat, girl._cheat_heat_peak,
            store._cheat_heat_session_gained))

        # Visual popup (same system as Love/Obed/Inbt popups)
        actual_delta = girl._cheat_heat - old
        if actual_delta > 0:
            _loc = getattr(girl, "SpriteLoc", None)
            _xpos = (_loc if _loc is not None else 0.75) - 0.15
            renpy.show_screen(
                _("StatHolder"),
                value=actual_delta,
                prefix="+",
                color=STAT_COLOR_HEAT,
                xpos=_xpos,
                ypos=0.43,
                label_text="Heat",
                hide_tag="stat_Heat",
                _tag="stat_Heat",
            )

    def _reduce_cheat_heat(girl, amount, reason=""):
        """Subtract heat (no multipliers — flat reduction)."""
        old = getattr(girl, "_cheat_heat", 0)
        if old <= 0:
            return
        girl._cheat_heat = max(0, old - abs(amount))
        actual_delta = girl._cheat_heat - old
        debug_log("[DEBUG] _reduce_cheat_heat: gid=%s -%s reason=%s total=%s" % (
            girl.gid, abs(amount), reason, girl._cheat_heat))
        if actual_delta < 0:
            _loc = getattr(girl, "SpriteLoc", None)
            _xpos = (_loc if _loc is not None else 0.75) - 0.15
            renpy.show_screen(
                _("StatHolder"),
                value=abs(actual_delta),
                prefix="-",
                color=STAT_COLOR_HEAT,
                xpos=_xpos,
                ypos=0.43,
                label_text="Heat",
                hide_tag="stat_Heat",
                _tag="stat_Heat",
            )

    def _notify_cheat_heat(girl, action, accepted=True):
        """Central heat dispatch. Looks up _CHEAT_HEAT_TABLE and calls _add/_reduce_cheat_heat.
        No-op if girl is not on a cheat path or action not in table.
        Gate denials (gate_*) are deduped per scene to prevent farming."""
        if not _is_on_cheat_path(girl):
            return
        if action.startswith("gate_") and not accepted:
            _given = getattr(store, "_cheat_gate_heat_given", set())
            _key = "%s_%s" % (girl.gid, action)
            if _key in _given:
                return
            _given.add(_key)
            store._cheat_gate_heat_given = _given
        entry = _CHEAT_HEAT_TABLE.get(action)
        if not entry:
            return
        amount = entry[0] if accepted else entry[1]
        if amount > 0:
            _add_cheat_heat(girl, amount, "%s_%s" % ("ok" if accepted else "no", action))
        elif amount < 0:
            _reduce_cheat_heat(girl, abs(amount), "%s_%s" % ("ok" if accepted else "no", action))

    # =============================================================
    # HEAT-AWARE GATE FUNCTIONS (replace old stage-only gates)
    # =============================================================

    def _cheat_can_tip(girl):
        """Tip allowed if: natural path passes OR heat exceeds threshold.
        Also bypassed if girl has already done tip or higher."""
        if _cheat_highest_tier_done(girl) >= _CHEAT_ACT_TIER.get("tip", 4):
            return True
        stage = getattr(girl, "_cheat_sex_stage", 0)
        rub_just = getattr(store, "_cheat_rub_just_done", False)
        heat = _cheat_effective_heat(girl)

        # Natural path (unchanged): stage >= 1 and not same-session rub
        if stage >= 1 and not rub_just:
            return True
        # Heat bypass: same-session rub (harder)
        if stage >= 1 and rub_just:
            result = heat >= _cheat_heat_threshold(girl, "skip_to_tip") + 15
            debug_log("[DEBUG] _cheat_can_tip: gid=%s heat=%s threshold=%s (same-session) -> %s" % (girl.gid, heat, _cheat_heat_threshold(girl, "skip_to_tip") + 15, result))
            return result
        # Heat bypass: skip rub entirely (stage 0)
        result = heat >= _cheat_heat_threshold(girl, "skip_to_tip")
        debug_log("[DEBUG] _cheat_can_tip: gid=%s stage=%s heat=%s threshold=%s -> %s" % (girl.gid, stage, heat, _cheat_heat_threshold(girl, "skip_to_tip"), result))
        return result

    def _cheat_can_sex(girl):
        """Sex allowed if: natural path passes OR heat exceeds threshold.
        Also bypassed if girl has already done sex or higher."""
        if _cheat_highest_tier_done(girl) >= _CHEAT_ACT_TIER.get("sex", 5):
            return True
        stage = getattr(girl, "_cheat_sex_stage", 0)
        tip_just = getattr(store, "_cheat_tip_just_done", False)
        rub_just = getattr(store, "_cheat_rub_just_done", False)
        heat = _cheat_effective_heat(girl)

        # Natural path
        if stage >= 2 and not tip_just:
            return True
        # Threshold depends on how much is being skipped
        if stage >= 1:
            skip = "skip_s1_to_sex"
        else:
            skip = "skip_s0_to_sex"
        threshold = _cheat_heat_threshold(girl, skip)
        if tip_just or rub_just:
            threshold += 15
        result = heat >= threshold
        debug_log("[DEBUG] _cheat_can_sex: gid=%s stage=%s heat=%s threshold=%s skip=%s -> %s" % (girl.gid, stage, heat, threshold, skip, result))
        return result

    def _cheat_can_anal(girl):
        """Anal gate — MUCH harder than sex. Separate from _cheat_can_sex.
        Still requires anal_penetration_check to pass (stats)."""
        if _cheat_highest_tier_done(girl) >= _CHEAT_ACT_TIER.get("anal", 6):
            return True
        stage = getattr(girl, "_cheat_sex_stage", 0)
        heat = _cheat_effective_heat(girl)
        same_session = getattr(store, "_cheat_tip_just_done", False) or getattr(store, "_cheat_rub_just_done", False)

        # Natural path: has done sex (stage 3), not same-session
        if stage >= 3 and not same_session:
            return True
        # Heat bypass by stage
        if stage >= 2:
            skip = "skip_s2_to_anal"
        elif stage >= 1:
            skip = "skip_s1_to_anal"
        else:
            skip = "skip_s0_to_anal"
        threshold = _cheat_heat_threshold(girl, skip)
        if same_session:
            threshold += 15
        if girl.has_trait("anal_lover"):
            threshold -= 10
        if girl.has_trait("anal_hater"):
            threshold += 15
        result = heat >= threshold
        debug_log("[DEBUG] _cheat_can_anal: gid=%s stage=%s heat=%s threshold=%s skip=%s -> %s" % (girl.gid, stage, heat, threshold, skip, result))
        return result

    def _cheat_too_fast_line(girl):
        """Line when player tries to escalate too fast on cheat path (same session as previous stage)."""
        _tip_just = getattr(store, "_cheat_tip_just_done", False)
        _rub_just = getattr(store, "_cheat_rub_just_done", False)
        _is_v = girl.has_trait("virgin")
        if _tip_just:
            if _is_v:
                return renpy.random.choice([
                    _("You want to go ALL the way?! I just let you put the tip in for the first time... that was already way too much for me today."),
                    _("I just felt a guy inside me for the first time... I need to process that before going any further!"),
                    _("That was my first time even having the tip in... I can't do more today. I need to think."),
                ])
            return renpy.random.choice([
                _("That's way too fast! We JUST did the tip... I can't go further today. Maybe next time..."),
                _("Slow down! I just let you put it in a little... I need time before going all the way."),
                _("We JUST did that... I can't go further today. I need time to think about what I'm doing..."),
            ])
        if _rub_just:
            if _is_v:
                return renpy.random.choice([
                    _("We literally just rubbed for the first time! You want to go FURTHER? Not today!"),
                    _("I just let you rub against me... that was already a huge step for me. Not today."),
                    _("That was the first time I've ever done anything like that... give me time!"),
                ])
            return renpy.random.choice([
                _("That's way too fast! We just rubbed for the first time... maybe the tip next time... but NOT today!"),
                _("We JUST rubbed... I can't jump to sex today. Give me time."),
                _("Slow down! We barely just started rubbing... I need to process this first."),
            ])
        return _("Not today... I need more time.")

    # =============================================================
    # COUNTER-OFFER SYSTEM
    # When a gate blocks an action, girl offers a lower alternative.
    # Player can accept (route to lower act) or refuse (+20 heat).
    # =============================================================

    def _cheat_get_counter_offer(girl, wanted_act):
        """Determine what counter-offer she makes, or None if no counter available.
        Always offers a lower act when the stage blocks, unless same-session."""
        stage = getattr(girl, "_cheat_sex_stage", 0)
        rub_just = getattr(store, "_cheat_rub_just_done", False)
        tip_just = getattr(store, "_cheat_tip_just_done", False)

        if wanted_act in ("sex", "anal"):
            if tip_just or rub_just:
                return None
            if wanted_act == "anal" and stage >= 2:
                return "sex"
            if wanted_act == "anal" and stage >= 1:
                return "tip"
            if stage >= 1:
                return "tip"
            return "rub"
        elif wanted_act == "tip":
            if rub_just:
                return None
            return "rub"
        return None

    # Counter-offer dialogue lines by (wanted, offered) and path
    _COUNTER_OFFER_LINES = {
        ("sex", "tip"): {
            1: [
                _("I'm not ready for THAT... but maybe... just the tip? Just to see how it feels..."),
                _("We can't do that! But... the tip? Maybe just the tip wouldn't be so bad..."),
                _("That's too far! But... I could let you put just the tip in..."),
            ],
            2: [
                _("I want it too but... let me try just the tip first. I need to feel in control."),
                _("Slow down... I need to ease into this. Just the tip. On MY terms."),
                _("Not yet... but I'm curious. Just the tip. I decide when it goes further."),
            ],
            3: [
                _("He doesn't deserve me going ALL the way yet... but the tip? That's barely anything."),
                _("I'm not giving you everything yet. But the tip? That's nothing compared to what he deserves."),
                _("Not the whole thing... but the tip? That's barely revenge. Fine."),
            ],
        },
        ("anal", "tip"): {
            1: [
                _("My BUTT?! No way! But... the tip? Maybe just the tip..."),
                _("Are you insane?! Not there! But... I could let you put the tip in..."),
            ],
            2: [
                _("Anal?! That's... I'm curious, but... let's start with just the tip."),
                _("My ass? Slow down! But... I could handle the tip."),
            ],
            3: [
                _("In my ass? He'd lose his mind... but I'm not ready. Maybe the tip first."),
                _("Not my ass. Not yet. But the tip? That's barely betrayal."),
            ],
        },
        ("anal", "sex"): {
            1: [
                _("Not there! That's way too much! But... we could do it normally..."),
                _("My butt?! No! But... if you want to be inside me, there's another option..."),
            ],
            2: [
                _("Anal? I'm not THAT far gone yet. But regular sex? I can handle that."),
                _("My ass is off limits for now. But I need you inside me... the normal way."),
            ],
            3: [
                _("He'd die if I let you in my ass. I'm saving that level of betrayal. Regular sex though? Sure."),
                _("Not my ass yet. But you can fuck me properly. That's enough revenge for now."),
            ],
        },
        ("sex", "rub"): {
            1: [
                _("That's WAY too far! But... we could rub? Rubbing isn't really cheating..."),
                _("No! We can't! But... rubbing? Rubbing is safe..."),
                _("I can't do THAT! But... we could just rub against each other... that's okay..."),
            ],
            2: [
                _("Slow down! Let's start with rubbing. I decide the pace."),
                _("Not yet. Rubbing first. I'm in control here."),
            ],
            3: [
                _("Straight to sex? He's not THAT bad yet... but rubbing? Sure."),
                _("I'm not going all the way yet. But rubbing? He earned at least that much betrayal."),
            ],
        },
        ("anal", "rub"): {
            1: [
                _("My butt?! Are you crazy?! But... we could rub... rubbing is fine..."),
                _("Absolutely NOT! But... if you want to feel me, we can rub..."),
            ],
            2: [
                _("Anal?! Way too far! But rubbing... rubbing I can handle."),
                _("You're insane. But I'll let you rub. That's it."),
            ],
            3: [
                _("He'd lose his mind at that. I'm not ready for THAT level. But rubbing? Sure."),
                _("Not my ass. Not even close. But we can rub."),
            ],
        },
        ("tip", "rub"): {
            1: [
                _("Not inside! That's almost sex! But... rubbing is okay."),
                _("I can't let you put it in! But we can rub... that's safe..."),
            ],
            2: [
                _("I'm not ready for anything inside... but I want to feel it against me."),
                _("Not yet. But I want to feel it. Rubbing. On my terms."),
            ],
            3: [
                _("Inside me already? Not yet. Let's just rub for now."),
                _("He doesn't deserve the tip yet. Rubbing is enough."),
            ],
        },
    }

    _COUNTER_REFUSE_LINES = {
        1: [
            _("Then... I guess we're done for now. I'm sorry."),
            _("If you don't want that... then I don't know what to tell you."),
            _("I can't do more than that... not today."),
        ],
        2: [
            _("Your loss. I was offering."),
            _("Fine. Then we're done. For now."),
            _("Take it or leave it. Looks like you're leaving it."),
        ],
        3: [
            _("Whatever. His loss, your loss. We're done here."),
            _("You don't want what I'm offering? Then forget it."),
            _("Fine. I was doing YOU a favor."),
        ],
    }

    # =============================================================
    # BIG JUMP DIALOGUE — when she accepts an act 3+ tiers above
    # her highest previous act. Triggered before the act begins.
    # =============================================================

    def _cheat_big_jump_distance(girl, new_act):
        """Return the tier distance between the new act and highest done."""
        new_tier = _CHEAT_ACT_TIER.get(new_act, 0)
        highest = _cheat_highest_tier_done(girl)
        return new_tier - highest

    def _cheat_big_jump_line(girl, new_act):
        """Return a big-jump reaction line, or None if skip < 3."""
        dist = _cheat_big_jump_distance(girl, new_act)
        if dist < 3:
            return None

        has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        is_hc = hasattr(girl, "has_trait") and girl.has_trait("hardcore_sex")
        is_cute = hasattr(girl, "has_trait") and girl.has_trait("cute_sex")

        if dist >= 5:
            if is_hc:
                pool = [
                    _("I don't care about steps. I don't care about 'normal'. Just do it. NOW."),
                    _("No buildup. No excuses. I want this and I want it now."),
                ]
            elif is_cute:
                pool = [
                    _("H-how did we get here...? We never kissed, never held hands, and now... oh god..."),
                    _("I don't understand... we skipped everything... and now I'm letting you..."),
                ]
            elif has_bf:
                pool = [
                    _("I won't even hold hands with my {hint}boyfriend{/hint} in public and here I am letting you do THIS... what is wrong with me?"),

                    _("My {hint}boyfriend{/hint} and I took months to get past kissing... and I'm giving YOU this already?"),

                ]
            else:
                pool = [
                    _("I don't understand what's happening to me... I never even kissed you and now I'm letting you..."),
                    _("This is insane... we skipped everything and here we are..."),
                ]
        elif dist >= 4:
            if is_hc:
                pool = [
                    _("We're doing this. No buildup. No excuses. Just straight to it."),
                    _("Foreplay is overrated anyway. Let's skip to the good part."),
                ]
            elif is_cute:
                pool = [
                    _("I can't believe I'm doing this... we never even... and now I'm letting you..."),
                    _("This is so sudden... my heart is racing... we barely did anything before this..."),
                ]
            elif has_bf:
                pool = [
                    _("My {hint}boyfriend{/hint} and I took months to get past kissing... and I'm giving YOU this already?"),

                    _("I never let my {hint}boyfriend{/hint} get this far this fast... and here I am with you..."),

                ]
            else:
                pool = [
                    _("This is insane... I've barely done anything with you and here we are..."),
                    _("We skipped a lot of steps... but I don't care anymore..."),
                ]
        else:  # dist == 3
            if is_hc:
                pool = [
                    _("Fuck it. I don't need the slow buildup. I want this NOW."),
                    _("Who needs foreplay when we have chemistry like this?"),
                ]
            elif is_cute:
                pool = [
                    _("We skipped so many steps... I feel like my heart is going to explode..."),
                    _("This is happening so fast... I'm nervous but I can't stop..."),
                ]
            elif has_bf:
                pool = [
                    _("I never even let my {hint}boyfriend{/hint} get this far... and I'm jumping straight to this with you?"),

                    _("We barely did anything and now THIS? If my {hint}boyfriend{/hint} knew..."),

                ]
            else:
                pool = [
                    _("I can't believe this is happening... we barely touched each other and now... this..."),
                    _("Everything is moving so fast... but I don't want to stop..."),
                ]
        return renpy.random.choice(pool)

    def _cheat_rub_first_line(girl):
        """Pick the first-rub line for this girl's path."""
        p = getattr(girl, "_cheat_escalation_path", 0)
        if p == 2:
            return _cheat_line(girl, renpy.random.choice(_PATH2_RUB_FIRST))
        elif p == 3:
            return _cheat_line(girl, renpy.random.choice(_PATH3_RUB_FIRST))
        return _cheat_line(girl, renpy.random.choice(_PATH1_RUB_FIRST))

    def _cheat_rub_midline(girl):
        p = getattr(girl, "_cheat_escalation_path", 0)
        if p == 2:
            return _cheat_line(girl, renpy.random.choice(_PATH2_RUB_LINES))
        elif p == 3:
            return _cheat_line(girl, renpy.random.choice(_PATH3_RUB_LINES))
        return _cheat_line(girl, renpy.random.choice(_PATH1_RUB_LINES))

    def _cheat_tip_first_line(girl):
        p = getattr(girl, "_cheat_escalation_path", 0)
        if p == 2:
            return _cheat_line(girl, renpy.random.choice(_PATH2_TIP_FIRST))
        elif p == 3:
            return _cheat_line(girl, renpy.random.choice(_PATH3_TIP_FIRST))
        return _cheat_line(girl, renpy.random.choice(_PATH1_TIP_FIRST))

    def _cheat_tip_midline(girl):
        p = getattr(girl, "_cheat_escalation_path", 0)
        if p == 2:
            return _cheat_line(girl, renpy.random.choice(_PATH2_TIP_LINES))
        elif p == 3:
            return _cheat_line(girl, renpy.random.choice(_PATH3_TIP_LINES))
        return _cheat_line(girl, renpy.random.choice(_PATH1_TIP_LINES))

    def _cheat_sex_first_line(girl):
        p = getattr(girl, "_cheat_escalation_path", 0)
        is_virgin = girl.has_trait("virgin")
        if p == 2:
            return _cheat_line(girl, renpy.random.choice(_PATH2_SEX_CONDOM_FIRST_VIRGIN if is_virgin else _PATH2_SEX_CONDOM_FIRST))
        elif p == 3:
            return _cheat_line(girl, renpy.random.choice(_PATH3_SEX_CONDOM_FIRST_VIRGIN if is_virgin else _PATH3_SEX_CONDOM_FIRST))
        if is_virgin:
            return _cheat_line(girl, renpy.random.choice(_PATH1_SEX_CONDOM_FIRST_VIRGIN))
        return _cheat_line(girl, renpy.random.choice(_PATH1_SEX_CONDOM_FIRST))

    def _cheat_sex_midline(girl):
        p = getattr(girl, "_cheat_escalation_path", 0)
        if p == 2:
            return _cheat_line(girl, renpy.random.choice(_PATH2_SEX_LINES))
        elif p == 3:
            return _cheat_line(girl, renpy.random.choice(_PATH3_SEX_LINES))
        return _cheat_line(girl, renpy.random.choice(_PATH1_SEX_LINES))

    # ── Path 1 mid-scene lines (rub) ──
    _PATH1_RUB_LINES = [
        _("Oh, thank god we're just rubbing! Nothing serious! Nothing going inside me! Just... rubbing!"),
        _("See? This is fine! Just friction! My {hint}boyfriend{/hint} wouldn't even consider this cheating!"),

        _("Just rubbing... just rubbing... this doesn't count... it CAN'T count..."),
        _("As long as it stays outside, it's fine! We're not doing anything wrong! ...Right?"),
        _("Good thing we're only rubbing! If something actually went inside... THAT would be cheating!"),
    ]

    # ── Path 1 mid-scene lines (tip) ──
    _PATH1_TIP_LINES = [
        _("Don't move so fast... it could slip in deeper... for now we're just... helping each other..."),
        _("Just the tip... just the tip... that barely counts as anything..."),
        _("It's barely inside... this is practically still rubbing... my {hint}boyfriend{/hint} would understand..."),

        _("Don't you DARE push deeper! Just... just the tip is fine. It's nothing."),
        _("I can feel it... just a little... but it's not real sex. It's NOT."),
    ]

    # ── Path 1 first-time rub dialogue ──
    _PATH1_RUB_FIRST = [
        _("Wait... we're just going to rub, right? Just rubbing isn't cheating... RIGHT?"),
        _("Promise me... just rubbing. Nothing inside. If it's just rubbing, it doesn't count."),
        _("As long as you don't put it in... this is just like a massage. An intimate massage. That's all."),
        _("Just the outside... just friction... my {hint}boyfriend{/hint} wouldn't even care about this."),

    ]

    # ── Path 1 first-time tip dialogue ──
    _PATH1_TIP_FIRST = [
        _("Just... just the tip... nothing else! It's still not cheating! I'm just so wet and I need to feel something inside..."),
        _("Only the tip... promise me. If it's only the tip, it's barely anything... barely..."),
        _("I can't believe I'm saying this but... just put the tip in. JUST the tip. And then we stop."),
        _("The tip doesn't count... it's not real sex if it's just the tip... right? ...RIGHT?"),
    ]

    # ── Path 1 first-time condom sex dialogue ──
    _PATH1_SEX_CONDOM_FIRST = [
        _("OK! This isn't enough... I need to feel something more... But... condom! He wouldn't mind, there's no real contact..."),
        _("I need more... I NEED more. But CONDOM. With a condom it's basically nothing. It's NOT cheating!"),
        _("Put it all in but USE A CONDOM. With rubber between us it doesn't count... it CAN'T count..."),
        _("I can't take it anymore, I need you inside me properly... but a condom! With a condom it's not REAL sex!"),
    ]

    _PATH1_SEX_CONDOM_FIRST_VIRGIN = [
        _("I... I know it's my first time, but this is just because I'm so turned on... it doesn't mean anything, the first time with a CONDOM is basically nothing..."),
        _("I never... I've never done this before. But with a condom, it barely counts... it's NOT real. The first time doesn't count if there's a condom..."),
        _("My first time and it's not even with him... but it's with a CONDOM. It's practically not even real. It DOESN'T COUNT."),
    ]

    # ── Path 1 during condom sex lines ──
    _PATH1_SEX_LINES = [
        _("Yes... so deep, and still... no, we're NOT cheating! We're using a condom! It's NOT cheating!"),
        _("It feels so good but... condom! We have a CONDOM! This is FINE!"),
        _("Oh god... oh god... but it's okay because... condom... the condom makes it okay..."),
        _("My {hint}boyfriend{/hint} would... no, he'd understand! There's a condom! It's NOTHING!"),

        _("Harder... wait, no, I mean... it doesn't matter how hard because the condom means it's NOT real!"),
    ]

    # ── Path 1 condom removal block ──
    _PATH1_CONDOM_BLOCK = [
        _("NO! We need to keep the condom on! I can't cheat for real!"),
        _("Are you INSANE?! The condom stays ON! Without it, it would be ACTUAL cheating!"),
        _("Don't you DARE take that off! The condom is the only thing keeping this not-cheating!"),
        _("NO! If you take the condom off, then... then it's REAL. And I can't do that to him!"),
        _("The condom STAYS. Without it, I'm just another cheating girlfriend. And I'm NOT that."),
    ]

    # =============================================================
    # PATH 2 — TEMPTED / CURIOSITY
    # She's driven by lust/curiosity, thinks she's in control.
    # Progresses faster, can go raw (she may even ask for it).
    # =============================================================

    def _is_cheat_path2(girl):
        return getattr(girl, "_cheat_escalation_path", 0) == 2 and _is_bf_context(girl) and not (hasattr(girl, "has_trait") and girl.has_trait("cheater"))

    _PATH2_RUB_FIRST = [
        _("I just want to feel it... he never made me feel this way. I decide when we stop."),
        _("I've been dying to know what it feels like with you... just rubbing. I'm in control here."),
        _("Your... it's bigger than his. I just want to feel it against me. That's all. MY choice."),
        _("I'm not cheating. I'm just... experimenting. Seeing what I've been missing. On MY terms."),
    ]

    _PATH2_RUB_LINES = [
        _("Mmm... it's so much bigger... I can feel every inch even from the outside..."),
        _("I'm in control... I'm in control... but god it feels good..."),
        _("He never rubbed me like this... I can feel why other girls lose their minds..."),
        _("Just a little more... I decide when to stop... I'M the one in charge here..."),
        _("It's throbbing against me... no, I'm FINE. I can handle this. I'M in control."),
    ]

    _PATH2_TIP_FIRST = [
        _("Just... just push the tip in. I need to know what it feels like. I'll tell you when to stop."),
        _("I'm just curious what it feels like inside... just a little. I'll pull away whenever I want."),
        _("Put it in... just the tip. I'm the one in charge, remember? I say when it's enough."),
        _("I need to feel it... just a taste. Then I'll know if his is really that different. MY rules."),
    ]

    _PATH2_TIP_LINES = [
        _("Oh... oh god it's stretching me... no, I'm fine... I SAID I'm fine... don't move yet..."),
        _("It's... it's SO much thicker than his... I just need a second to... to process..."),
        _("I can handle this... I can HANDLE this... just don't go deeper... not yet..."),
        _("My body wants more but I decide... I DECIDE... just... keep it right there..."),
        _("Why does it feel this good from just the tip... what am I getting myself into..."),
    ]

    _PATH2_SEX_CONDOM_FIRST = [
        _("I can't take it anymore... I need all of it inside me. NOW. ...Condom first though. I'm not STUPID."),
        _("Put it all the way in... I need to feel you deep. But condom. I'm still in control."),
        _("Fuck it. FUCK it. All the way in. But use a condom... I want to feel it, not regret it."),
    ]

    _PATH2_SEX_CONDOM_FIRST_VIRGIN = [
        _("I've never done this before but I NEED you inside me... condom first. At least I can control that."),
        _("My first time and it's not with him... I don't care. I need this. Just use a condom."),
    ]

    _PATH2_SEX_LINES = [
        _("Oh FUCK... this is what I've been missing?! He NEVER felt like this..."),
        _("Harder... I said HARDER! I'm... I'm the one who decided this... and I want MORE!"),
        _("I thought I could stop whenever I wanted... I don't WANT to stop..."),
        _("So much bigger... so much deeper... I was fooling myself thinking I was in control..."),
        _("He has NO idea his girlfriend is moaning like this for someone else's cock..."),
    ]

    # Path 2: she may ask to remove the condom herself (high lust)
    _PATH2_RAW_REQUEST = [
        _("Take it off... the condom... I need to feel you for REAL. I can't... I can't hold back anymore."),
        _("I'm going crazy but... I want it raw. I need to feel every inch without that stupid thing."),
        _("Pull it off. NOW. I've lost control and I don't even care. I need you skin to skin."),
        _("I started this thinking I was in control... but I need you raw. I NEED it."),
    ]

    # =============================================================
    # PATH 3 — EXCUSE / REVENGE
    # She blames the boyfriend, uses it as justification.
    # Progresses normally, can go raw via convincing.
    # =============================================================

    def _is_cheat_path3(girl):
        return getattr(girl, "_cheat_escalation_path", 0) == 3 and _is_bf_context(girl) and not (hasattr(girl, "has_trait") and girl.has_trait("cheater"))

    _PATH3_RUB_FIRST = [
        _("He hasn't touched me in weeks. I just need to feel wanted. This is HIS fault."),
        _("If he actually paid attention to me, I wouldn't be here. So really, HE drove me to this."),
        _("I deserve to feel desired. He takes me for granted. This is just... reclaiming myself."),
        _("You know what? HE stopped trying. I'm just reminding myself what passion feels like."),
    ]

    _PATH3_RUB_LINES = [
        _("He never does this for me... he just rolls over and falls asleep..."),
        _("If he could see how much better this feels... no, he doesn't deserve to know."),
        _("This is what happens when you ignore your girlfriend... she finds someone who won't."),
        _("He had his chance. Now someone else is making me feel things he never could."),
        _("His loss. His fault. His problem. Not mine."),
    ]

    _PATH3_TIP_FIRST = [
        _("Just a little inside... just to see what I've been missing because of HIM."),
        _("If he gave me what I needed, I wouldn't want this. But he doesn't. So here we are."),
        _("Just the tip... consider it research. Seeing how a REAL man feels."),
        _("He's probably out there not even thinking about me. So why should I feel guilty?"),
    ]

    _PATH3_TIP_LINES = [
        _("He never made me feel like this... not even close... what have I been settling for..."),
        _("I wasted so much time being faithful to someone who doesn't even notice me..."),
        _("Every inch I feel just proves how much he's been failing me..."),
        _("He'd cry if he knew how good this feels... and honestly? Good."),
        _("I'm angry. At him. For making me need THIS to feel alive."),
    ]

    _PATH3_SEX_CONDOM_FIRST = [
        _("I need more... I DESERVE more. But condom. I'm getting revenge, not getting pregnant."),
        _("All the way in. He neglected me and now I'm taking what he should have given me. Condom though."),
        _("I'm done pretending his mediocre effort was enough. Give me everything. ...With a condom."),
    ]

    _PATH3_SEX_CONDOM_FIRST_VIRGIN = [
        _("My first time should have been special with HIM. But he never made me feel ready. You did. Condom, please."),
        _("He was supposed to be my first... but he never made me want it. You do. Just... use a condom."),
    ]

    _PATH3_SEX_LINES = [
        _("THIS is what sex is supposed to feel like?! He had YEARS and never gave me this!"),
        _("I'm so angry at him for making me settle... while THIS was out there the whole time..."),
        _("He could NEVER... he could never make me feel like this... I wasted so much time..."),
        _("I used to think I was the problem... that I didn't like sex enough. Turns out I just didn't like it with HIM."),
        _("Every time I think of his pathetic effort compared to THIS... I get even wetter..."),
    ]

    # Path 3: condom removal — she rationalizes it as final revenge
    _PATH3_RAW_REQUEST = [
        _("Take it off. If I'm going to do this, I'm going ALL the way. He deserves it."),
        _("I want to feel you raw. No barrier. Complete betrayal. He earned this."),
        _("Remove the condom... I want to feel everything he was too afraid to give me."),
        _("Condom off. If I'm already here, might as well make it count. This is his fault anyway."),
    ]

    # =============================================================
    # ANAL-SPECIFIC LINES — "anal isn't real sex / cheating"
    # Virgin girls rationalize: virginity intact + not cheating.
    # Non-virgin girls rationalize: wrong hole = doesn't count.
    # =============================================================

    # ── Path 1 anal first-time (rationalization: anal isn't cheating) ──
    _PATH1_ANAL_FIRST = [
        _("It's just anal... it's not even the right hole! My {hint}boyfriend{/hint} can't be mad about THIS!"),

        _("We're not having real sex... it's my ass! That doesn't count as cheating!"),
        _("This is technically still not cheating... anal isn't sex... it's just... something else!"),
        _("My {hint}boyfriend{/hint} would understand... it's only my butt! It's NOT real sex!"),

    ]

    _PATH1_ANAL_FIRST_VIRGIN = [
        _("It's anal... I'm still a virgin! And it's not cheating because it's not real sex!"),
        _("My virginity is completely intact... this doesn't count. It CAN'T count. It's the wrong hole!"),
        _("I'm still pure... anal doesn't count! Not as sex, not as cheating... it's NOTHING!"),
        _("I never had real sex with anyone... my {hint}boyfriend{/hint} is still getting a virgin girlfriend. This is FINE."),

    ]

    # ── Path 1 anal mid-scene lines ──
    _PATH1_ANAL_LINES = [
        _("It's just my butt... this isn't real sex... my {hint}boyfriend{/hint} would understand..."),

        _("Anal doesn't count... it CAN'T count... it's the wrong hole..."),
        _("As long as it's just my ass, it's fine... it's NOT cheating... right?"),
        _("This isn't real... it's my ass... it's not like he's actually inside me... not REALLY..."),
        _("I'm not losing anything... my virginity is still there... this is just... just my butt..."),
    ]

    # ── Path 2 anal first-time (control: I choose which hole) ──
    _PATH2_ANAL_FIRST = [
        _("I always wondered what anal would feel like... and I'M the one choosing which hole. MY choice."),
        _("I wanted to try this... on MY terms. I decide what happens to my ass."),
        _("Anal was MY decision. I'm still in control of what goes where. This is just... research."),
    ]

    _PATH2_ANAL_FIRST_VIRGIN = [
        _("I've never done anything... and my first time is anal? At least I'm still technically a virgin. MY rules."),
        _("I'm choosing anal first... that way my first REAL time can still be special. Smart, right?"),
        _("Nobody's touched me before and I'm starting with my ass? Well... I'M in control of the order."),
    ]

    # ── Path 2 anal mid-scene lines ──
    _PATH2_ANAL_LINES = [
        _("I chose this hole... I'm in control... he's in my ass because I ALLOWED it..."),
        _("God, anal feels so different... I chose this... I can stop whenever I want..."),
        _("His cock is in my ass and I'm the one who decided that... I'm still in charge..."),
    ]

    # ── Path 3 anal first-time (revenge: he begged and I said no) ──
    _PATH3_ANAL_FIRST = [
        _("He BEGGED me for anal for months and I always said no. And this guy gets it first time asking."),
        _("My {hint}boyfriend{/hint} wanted my ass SO badly... well, someone else has it now. His loss."),

        _("He'll never know another man had my ass before he ever did. Serves him right."),
    ]

    _PATH3_ANAL_FIRST_VIRGIN = [
        _("He wanted to be my first everything... well, someone else is getting my ass instead. His loss."),
        _("My {hint}boyfriend{/hint} dreamed of being my first... and now this guy is taking my anal virginity. Good."),

        _("He begged for my ass AND my virginity. Someone else is getting one of those right now."),
    ]

    # ── Path 3 anal mid-scene lines ──
    _PATH3_ANAL_LINES = [
        _("He wanted this so bad and I always said no... but for you? My ass is all yours."),
        _("Another man is fucking my ass while my {hint}boyfriend{/hint} is still begging for it... perfect."),

        _("Every thrust in my ass is revenge for every night he ignored me..."),
    ]

    # ── Accessor functions ──
    def _cheat_anal_first_line(girl):
        """Pick the first-anal line for this girl's path. Virgin gets special pool."""
        p = getattr(girl, "_cheat_escalation_path", 0)
        is_virgin = girl.has_trait("virgin")
        if p == 2:
            return _cheat_line(girl, renpy.random.choice(_PATH2_ANAL_FIRST_VIRGIN if is_virgin else _PATH2_ANAL_FIRST))
        elif p == 3:
            return _cheat_line(girl, renpy.random.choice(_PATH3_ANAL_FIRST_VIRGIN if is_virgin else _PATH3_ANAL_FIRST))
        if is_virgin:
            return _cheat_line(girl, renpy.random.choice(_PATH1_ANAL_FIRST_VIRGIN))
        return _cheat_line(girl, renpy.random.choice(_PATH1_ANAL_FIRST))

    def _cheat_anal_midline(girl):
        p = getattr(girl, "_cheat_escalation_path", 0)
        if p == 2:
            return _cheat_line(girl, renpy.random.choice(_PATH2_ANAL_LINES))
        elif p == 3:
            return _cheat_line(girl, renpy.random.choice(_PATH3_ANAL_LINES))
        return _cheat_line(girl, renpy.random.choice(_PATH1_ANAL_LINES))

    # =============================================================
    # BREAKING POINT — she snaps and demands raw sex
    # Triggers when: condom sex count >= 3 AND raw check would pass
    # Fires mid-scene during keep going. Once triggered, she never
    # goes back to requiring condom (sets _cheat_broke flag).
    # =============================================================

    def _cheat_breaking_point_ready(girl):
        """Check if a cheat path girl is ready to break and go raw.
        Requires: on cheat path, has done condom sex 3+ times, not already broken,
        and the raw approval check would pass."""
        _on_path = _is_on_cheat_path(girl)
        _broke = getattr(girl, "_cheat_broke", False)
        _count = getattr(girl, "_cheat_condom_sex_count", 0)
        if story_act_locked(girl, "raw"):
            debug_log("[DEBUG] _cheat_breaking_point_ready: %s's story step locks raw -> False" % girl.gid)
            return False
        if not _on_path or _broke or _count < 2:
            debug_log("[DEBUG] _cheat_breaking_point_ready: on_path=%s broke=%s condom_count=%s -> False (early)" % (_on_path, _broke, _count))
            return False
        # Check if raw would pass (same logic as sex_penetration_check raw part)
        raw_count = getattr(girl, "raw_sex_count", 0)
        cream_count = getattr(girl, "CreampieCounts", 0)
        raw_bonus = min(raw_count * RAW_BONUS_PER, RAW_BONUS_CAP)
        cream_raw_bonus = min(cream_count * 30, 150)
        total_raw_bonus = min(raw_bonus + cream_raw_bonus, 300)
        base_rule = ApprovalRuleFor(girl, "sex", "sex")
        rule_raw = dict(base_rule)
        rule_raw["Bonus"] = rule_raw.get("Bonus", 0) + total_raw_bonus
        raw_result = ApprovalCheck(girl, ReturnData=True, **rule_raw)
        debug_log("[DEBUG] _cheat_breaking_point_ready: condom_count=%s raw_bonus=%s raw_accepted=%s -> %s" % (_count, total_raw_bonus, raw_result["accepted"], raw_result["accepted"]))
        return raw_result["accepted"]

    _BREAKING_POINT_PATH1 = [
        _("I don't care anymore! FUCK ME! I'm cheating and I DON'T CARE! I just want your dick inside me RAW!"),
        _("Take it OFF! The condom was a LIE! I was ALWAYS cheating! I want to FEEL you!"),
        _("I can't pretend anymore! The condom doesn't make it okay! So just... just take it off and FUCK ME!"),
        _("Forget the condom! Forget my {hint}boyfriend{/hint}! I want you RAW! I want EVERYTHING!"),

        _("I've been lying to myself this whole time! I'm a CHEATER! So take that stupid condom off and MAKE ME FEEL IT!"),
    ]

    _BREAKING_POINT_PATH2 = [
        _("I TOLD myself I was in control... but I NEED you raw. Take it off. NOW. I can't hold back anymore."),
        _("Forget the condom. I lost control a long time ago. I need to feel every inch without that thing."),
        _("I was fooling myself thinking I could stop whenever I wanted. Take it off. I need the REAL thing."),
        _("I can't... I can't take the condom anymore. I need to feel you skin to skin. I'm DONE pretending I'm in control."),
    ]

    _BREAKING_POINT_PATH3 = [
        _("He DESERVES this. Full betrayal. Take the condom off. I want to feel what he NEVER gave me."),
        _("Condom off. NOW. If I'm doing this behind his back, I'm going ALL the way. No barriers. No excuses."),
        _("You know what? Fuck him. Fuck the condom. I want the REAL thing. Complete betrayal. He EARNED this."),
        _("Take it off. I'm done half-cheating. He ignored me for MONTHS. I want you raw. Every. Single. Inch."),
    ]

    def _cheat_breaking_line(girl):
        p = getattr(girl, "_cheat_escalation_path", 0)
        if p == 1:
            return _cheat_line(girl, renpy.random.choice(_BREAKING_POINT_PATH1))
        elif p == 2:
            return _cheat_line(girl, renpy.random.choice(_BREAKING_POINT_PATH2))
        elif p == 3:
            return _cheat_line(girl, renpy.random.choice(_BREAKING_POINT_PATH3))
        return _cheat_line(girl, renpy.random.choice(_BREAKING_POINT_PATH1))

    # =============================================================
    # POST-SCENE GUILT LINES — said after rub/tip/sex ends
    # =============================================================

    _AFTERSCENE_PATH1 = {
        "rub": [
            _("That wasn't cheating. It's nothing serious, just a bit of skin on skin... But don't tell my {hint}boyfriend{/hint}. I don't want to have to explain."),

            _("See? We just rubbed. That's all. Nothing happened. Nothing REAL happened. My {hint}boyfriend{/hint} doesn't need to know about... nothing."),

            _("It's just friction. Friends do that, right? It's FINE. Just... don't mention this to anyone. Especially not him."),
            _("That was... innocent. Completely innocent. Just... please don't tell my {hint}boyfriend{/hint}. He wouldn't understand how innocent it was."),

            _("Okay... that happened. But it's not cheating. It's NOT. It's just rubbing. He'd understand... but let's not test that."),
        ],
        "tip": [
            _("It was JUST the tip. That barely counts as anything... right? My {hint}boyfriend{/hint} can NEVER know about this."),

            _("Just the tip went inside me... that's... that's practically nothing. It's not sex. I didn't cheat. I DIDN'T."),
            _("I can still feel it... but it was only the tip. That's not real. It doesn't count. ...Why does it feel like it counts?"),
            _("We didn't go all the way. Just the tip. My {hint}boyfriend{/hint} would... no, he doesn't need to know. Because nothing happened."),

            _("The tip doesn't count. Everyone knows the tip doesn't count. Right? ...RIGHT? Don't answer that."),
        ],
        "sex": [
            _("We used a condom so... it's not REAL cheating. The condom means nothing touched for real. My {hint}boyfriend{/hint} would understand that... in theory."),

            _("I just had sex with someone else... but the condom makes it... it HAS to make it okay. There was a barrier. So it doesn't count."),
            _("The condom was on the whole time. So technically... technically my {hint}boyfriend{/hint} wasn't betrayed. Right? The rubber was between us. It's FINE."),

            _("We had sex but with a condom. That's like... a medical procedure. Clinical. Not cheating. Definitely not cheating. ...Oh god."),
            _("My {hint}boyfriend{/hint} would die if he knew. But the condom... the condom means it's fine. It HAS to mean it's fine. I need it to mean it's fine."),

        ],
        "sex_raw": [
            _("I didn't even use protection... there's no excuse. No barrier. Nothing between us. My {hint}boyfriend{/hint} would never forgive this."),

            _("No condom... I let him inside me with NOTHING. That's not a mistake, that's a choice I made. Oh god."),
            _("We didn't use anything... I could feel every inch of him. How am I supposed to go back to my {hint}boyfriend{/hint} after that?"),

            _("Raw. We did it raw. I can't even lie to myself about this one. This was real. This was cheating. This was... everything."),
            _("At least with a condom I could pretend it wasn't real... but raw? I felt everything. My {hint}boyfriend{/hint} can never know."),

        ],
        "anal": [
            _("I let someone else have my ass... my {hint}boyfriend{/hint} has never even asked for that. What is wrong with me?"),

            _("That was my... my ass. I gave him my ASS. I can't even look at myself right now. My {hint}boyfriend{/hint} would be destroyed."),

            _("Anal... I did ANAL with someone who isn't my {hint}boyfriend{/hint}. I can't take that back. I can't unfeel that."),

            _("I let him put it in my ass... I've never even done that with my {hint}boyfriend{/hint}. What does that say about me?"),

            _("My {hint}boyfriend{/hint} doesn't know I've done anal... with another man. This is worse than I thought it would feel."),

        ],
    }

    _AFTERSCENE_PATH2 = {
        "rub": [
            _("That was... intense. But I chose to do it. I'm still in control. I can stop whenever I want."),
            _("Mmm... I can still feel it against me. His is nothing compared to... no. I'm fine. I'm in control."),
            _("I wanted that. And I chose to stop. See? I'm the one making the decisions here."),
        ],
        "tip": [
            _("I only let the tip in. I CHOSE that. And I can choose not to go further. ...Can't I?"),
            _("It took everything in me to stop at the tip... he's so much bigger than my {hint}boyfriend{/hint}..."),

            _("The tip was... god. If I let more than the tip in I don't think I'll be able to stop."),
        ],
        "sex": [
            _("I lost control. I completely lost control. I told myself I could stop anytime... I couldn't."),
            _("I was supposed to be in charge... but my body took over. I couldn't stop even if I wanted to."),
            _("So this is what happens when I stop pretending I'm in control... I can't go back to pretending."),
        ],
        "sex_raw": [
            _("I told myself I'd at least use a condom... and I didn't even do that. I have zero self-control."),
            _("No condom. I let him go raw inside me. I didn't even TRY to stop it. What happened to being in charge?"),
            _("I was supposed to set boundaries... and instead I let him fuck me raw. I couldn't even manage that much."),
        ],
        "anal": [
            _("I thought I could handle this... but anal? That crosses a line I can't uncross. I lost control completely."),
            _("Letting him have my ass wasn't the plan. I was supposed to be in charge... instead I'm bent over for him."),
            _("My ass was supposed to be off limits... and I gave it up. I didn't even put up a fight."),
        ],
    }

    _AFTERSCENE_PATH3 = {
        "rub": [
            _("He ignores me for weeks and then wonders why I do things like this. His fault."),
            _("If he touched me the way you just did, I wouldn't need to be here. Simple."),
            _("I don't feel guilty. He made me feel invisible. At least YOU see me."),
        ],
        "tip": [
            _("Just the tip of someone else's cock because my {hint}boyfriend{/hint} can't be bothered. Poetic."),

            _("He should be thanking you. At least SOMEONE is keeping his girlfriend satisfied."),
            _("If he finds out... well, maybe he should have paid attention to me first."),
        ],
        "sex": [
            _("He had YEARS to make me feel like this. You did it in one session. His loss."),
            _("I just slept with someone else and all I can think about is how much better it was..."),
            _("My {hint}boyfriend{/hint} is at home right now, clueless. And honestly? I don't care."),

        ],
        "sex_raw": [
            _("Raw. No condom. My {hint}boyfriend{/hint} would lose his mind. That's exactly what he deserves for ignoring me."),

            _("No condom? Good. If I'm cheating, I'm going ALL in. He doesn't get the mercy of 'at least she was safe'."),
            _("I let him fuck me raw. My {hint}boyfriend{/hint} hasn't touched me in weeks but THIS guy gets the full experience? Sounds about right."),

        ],
        "anal": [
            _("My {hint}boyfriend{/hint} begged me for anal for MONTHS and I always said no. But this guy? First time asking. He got it."),

            _("He wanted my ass so bad... well, someone else has it now. And honestly? It felt amazing. His loss."),
            _("Anal with another man while my {hint}boyfriend{/hint} is at home thinking I'm out with friends. This is the revenge he earned."),

        ],
    }

    def _cheat_afterscene_line(girl, act_type):
        """Pick a post-scene guilt line based on girl's path and what just happened."""
        p = getattr(girl, "_cheat_escalation_path", 0)
        if p == 1:
            pool = _AFTERSCENE_PATH1
        elif p == 2:
            pool = _AFTERSCENE_PATH2
        elif p == 3:
            pool = _AFTERSCENE_PATH3
        else:
            return None
        lines = pool.get(act_type)
        if lines:
            return _cheat_line(girl, renpy.random.choice(lines))
        return None

    # =============================================================
    # BF-TIER GUILT LINE
    # Additional guilt based on how good her relationship with BF is.
    # Called after the main afterscene line for extra BF emphasis.
    # =============================================================

    _BF_TIER_GUILT = {
        "in_love": {
            "rub": [
                _("I love him so much... and I just let someone else grind against me. What is wrong with me?"),
                _("He tells me he loves me every morning... and THIS is what I do behind his back?"),
            ],
            "tip": [
                _("He's the best thing that ever happened to me... and I let you put it inside me. Even just the tip..."),
                _("I love my {hint}boyfriend{/hint} with all my heart... why does it feel so good when you do this?"),

            ],
            "sex": [
                _("I love him. I really, truly love him. And I just had sex with you. I'm a horrible person."),
                _("He's everything to me... but when you're inside me I can't think about anything else..."),
                _("He'd be devastated if he found out. He trusts me completely... and I just betrayed that."),
            ],
            "anal": [
                _("I've never even done this with him... and I gave it to you instead. He'd never forgive me."),
                _("My {hint}boyfriend{/hint} is the man I love... and I just let someone else fuck my ass. I'm disgusting."),

            ],
        },
        "normal": {
            "rub": [
                _("Things are fine with him... but you make me feel something he doesn't."),
                _("He's a good boyfriend... I just... needed this. I don't know why."),
            ],
            "tip": [
                _("He's nice to me. He treats me well. And I still let you do this..."),
                _("My {hint}boyfriend{/hint} doesn't deserve what I'm doing... but I can't stop."),

            ],
            "sex": [
                _("He doesn't make me feel like you do. That's not an excuse... but it's the truth."),
                _("My {hint}boyfriend{/hint} is decent to me... and I still chose to sleep with someone else."),

            ],
            "anal": [
                _("He's never asked me for this... and I gave it to you without him even knowing."),
                _("My {hint}boyfriend{/hint} would probably never even think of doing this... and I WANTED it with you."),

            ],
        },
        "strained": {
            "rub": [
                _("Things aren't great with him anyway... this barely even feels like cheating anymore."),
                _("Our relationship is falling apart. At least SOMEONE makes me feel wanted."),
            ],
            "tip": [
                _("He barely touches me anymore... can you blame me for wanting this?"),
                _("Things are bad between us. This is just... filling a void he left."),
            ],
            "sex": [
                _("We've been fighting all the time... this almost feels like I deserve it."),
                _("He stopped trying months ago. You didn't. That's why I'm here."),
            ],
            "anal": [
                _("He can barely be bothered to hold my hand... and I'm here letting you have my ass. Ironic."),
                _("Our relationship is basically over anyway. At least I'm having fun."),
            ],
        },
        "miserable": {
            "rub": [
                _("I don't even care anymore. He makes me miserable. You don't."),
                _("Whatever. He lost the right to care about what I do a long time ago."),
            ],
            "tip": [
                _("He doesn't deserve my loyalty. Not after everything he's put me through."),
                _("I should have done this sooner. He's been awful to me."),
            ],
            "sex": [
                _("I feel nothing for him anymore. But THIS? This I felt."),
                _("He made me miserable for so long... and you make me feel alive."),
                _("Honestly? He deserves this. Every second of it."),
            ],
            "anal": [
                _("He'd lose his mind if he knew. Good. Let him feel something for once."),
                _("I gave you something he'll never get. And I don't feel bad about it at all."),
            ],
        },
    }

    def _bf_tier_guilt_line(girl, act_type):
        """Return a BF-tier-specific guilt line, or None."""
        if not hasattr(girl, "bf_loyalty_tier"):
            return None
        tier = girl.bf_loyalty_tier()
        # sex_raw uses same bf-tier guilt as condom sex
        _key = "sex" if act_type == "sex_raw" else act_type
        pool = _BF_TIER_GUILT.get(tier, {}).get(_key)
        if pool:
            return _cheat_line(girl, renpy.random.choice(pool))
        return None

    # =============================================================
    # HEAT RELIEF — Girl proactively suggests the next-stage act
    # Triggers when heat is high enough at the "Have Sex" menu.
    # If player accepts: heat drops, stage advances, scene starts.
    # If player refuses: she acknowledges weakness, heat stays.
    # =============================================================

    # Heat drop when the player accepts the girl's suggestion
    _HEAT_RELIEF_DROP = {
        "rub": -20,
        "tip": -25,
        "sex": -30,
        "anal": -30,
    }

    def _cheat_heat_relief_check(girl):
        """Return the act she'd suggest, or None if no relief triggers."""
        if not _is_on_cheat_path(girl):
            return None
        heat = _cheat_effective_heat(girl)
        if heat < 50:
            return None
        # Only once per session
        if getattr(store, "_heat_relief_done_this_session", False):
            return None
        # Probability: 30% at heat 50, 85% at heat 90+
        chance = min(0.3 + (heat - 50) * 0.014, 0.85)
        if renpy.random.random() > chance:
            return None
        # Suggest the next stage act
        stage = _cheat_stage(girl)
        if stage == 0:
            return "rub"
        elif stage == 1:
            return "tip"
        elif stage == 2:
            return "sex"
        elif stage >= 3:
            return "anal"
        return None

    # Position pick when she leads
    def _heat_relief_pick_position(girl):
        """Pick a position the girl prefers for heat relief."""
        if girl.has_trait("hardcore_sex"):
            _pool = ["doggy", "doggy", "reverse_cowgirl"]
        elif girl.has_trait("cute_sex"):
            _pool = ["cowgirl", "cowgirl", "reverse_cowgirl"]
        else:
            _pool = ["reverse_cowgirl", "cowgirl", "doggy"]
        _valid = [p for p in _pool if girl_has_pose(girl, p)]
        if not _valid:
            _valid = ["laying_down"] if girl_has_pose(girl, "laying_down") else ["cowgirl"]
        return renpy.random.choice(_valid)

    # Dialogue when she suggests an act (BF-tier-aware)
    _HEAT_RELIEF_LINES = {
        "rub": {
            "in_love": [
                _("I know I shouldn't... I love him... but I need to feel you against me. Just rubbing, nothing more."),
                _("Please... I can't stop thinking about it. Just press against me. It won't be cheating if we just rub... right?"),
            ],
            "normal": [
                _("I need this... just rub against me. I've been thinking about it all day."),
                _("I can't take it anymore. I need to feel you... just rubbing. Please."),
            ],
            "strained": [
                _("He doesn't touch me like I want him to. YOU do. Just... rub against me."),
                _("I've been craving this. Forget about him. Just press against me."),
            ],
            "miserable": [
                _("I need you. NOW. Rub against me. I don't care about him anymore."),
                _("He makes me feel nothing. You make me feel everything. I need your body on mine."),
            ],
        },
        "tip": {
            "in_love": [
                _("I know this is wrong... but can you just... put the tip in? Just the tip. I need to feel it..."),
                _("I love my {hint}boyfriend{/hint}... but I've been going crazy. Just the tip, please... that's barely cheating..."),

            ],
            "normal": [
                _("I need more than rubbing... just the tip. I can't stop thinking about how it felt."),
                _("Put the tip in... please. I know it's wrong but I need it."),
            ],
            "strained": [
                _("Things with him are bad... and I want to feel you inside me. Just the tip first."),
                _("I need something real. Not whatever he gives me. Put it in... just the tip."),
            ],
            "miserable": [
                _("I need you inside me. At least the tip. I can't pretend he's enough anymore."),
                _("Put it in. He doesn't deserve my loyalty and I'm done pretending."),
            ],
        },
        "sex": {
            "in_love": [
                _("I love him... but I need you to fuck me. I can't hold back anymore. Please..."),
                _("This is the worst thing I've ever done... but I need all of you. Not just the tip. All of it."),
            ],
            "normal": [
                _("I'm done holding back. I want you to fuck me. For real this time."),
                _("Forget the tip, forget the rubbing. I need you inside me. NOW."),
            ],
            "strained": [
                _("I've been dying for this. He can't give me what you can. Fuck me."),
                _("I'm past caring. I want you. All of you. Right now."),
            ],
            "miserable": [
                _("I want you to fuck me so hard I forget his name. I mean it."),
                _("Fuck me. He lost any right to have a say in what I do with my body."),
            ],
        },
        "anal": {
            "in_love": [
                _("I never even considered this with him... but with you, I can't stop thinking about it. Take my ass... please."),
                _("He'd be destroyed if he knew... but I want you in my ass. I NEED it."),
            ],
            "normal": [
                _("I want you to try something new with me... my ass. He never asked, and I never offered. But I'm offering you."),
                _("Take my ass. I've been curious for so long and you're the one I trust with it."),
            ],
            "strained": [
                _("He never cared enough to explore with me. You do. Fuck my ass."),
                _("I want you to have something he'll never get. My ass is yours."),
            ],
            "miserable": [
                _("He doesn't deserve any part of me. But you? Take my ass. Take whatever you want."),
                _("I want to give you everything he'll never have. Start with my ass."),
            ],
        },
    }

    def _heat_relief_line(girl, act):
        """Return the girl's suggestion line based on BF tier."""
        tier = girl.bf_loyalty_tier() if hasattr(girl, "bf_loyalty_tier") else "normal"
        pool = _HEAT_RELIEF_LINES.get(act, {}).get(tier)
        if pool:
            return _cheat_line(girl, renpy.random.choice(pool))
        return _("I need you... please.")

    # Dialogue when the player accepts (she gives in to the tension)
    _HEAT_RELIEF_ACCEPT = {
        "rub": [
            _("Thank you... I just needed to feel you close..."),
            _("Yes... just like that. This is all I needed..."),
        ],
        "tip": [
            _("Oh god... just feeling the tip... this is what I've been craving..."),
            _("Yes... just the tip... I can handle this much..."),
        ],
        "sex": [
            _("I'm really doing this... I'm letting you inside me... and I don't want to stop."),
            _("Yes... all of it. I've been fighting this for too long."),
        ],
        "anal": [
            _("I can't believe I'm asking for this... but I need it. Take me."),
            _("Do it... before I lose my nerve."),
        ],
    }

    # Dialogue when the player refuses (holds out for more)
    _HEAT_RELIEF_REFUSE = {
        "in_love": [
            _("You're right... I was being weak. He deserves better than this. ...But I don't know how much longer I can resist."),
            _("I almost gave in... what is happening to me? I love him, but you..."),
        ],
        "normal": [
            _("Fine... but I'm not going to be able to hold back much longer. You know that, right?"),
            _("You're really going to make me wait? ...I'm getting more desperate every time."),
        ],
        "strained": [
            _("You want more? ...God, you're going to break me completely, aren't you?"),
            _("I offered and you said no? Either you want all of me or nothing... and I think I know which one."),
        ],
        "miserable": [
            _("You want to push me further? Fine. I've got nothing left to lose."),
            _("I threw myself at you and you held back? ...When you finally take what you want, I'll be ready."),
        ],
    }

    def _heat_relief_refuse_line(girl):
        """Line when player holds out for more."""
        tier = girl.bf_loyalty_tier() if hasattr(girl, "bf_loyalty_tier") else "normal"
        pool = _HEAT_RELIEF_REFUSE.get(tier)
        if pool:
            return _cheat_line(girl, renpy.random.choice(pool))
        return _("Fine... but this isn't over.")

# =============================================================
# COUNTER-OFFER LABEL
# Called when a cheat gate blocks an action. Shows counter-offer
# menu and sets store._cheat_counter_result.
# =============================================================
label _cheat_counter_offer(girl, wanted_act):

    python:
        _co = _cheat_get_counter_offer(girl, wanted_act)
        _path = getattr(girl, "_cheat_escalation_path", 0)
        if not _path:
            _path = 1

    if _co is None:
        $ _notify_cheat_heat(girl, "no_counter")
        $ Say_Line(girl, _cheat_too_fast_line(girl))
        if getattr(store, "_ctr_financial_available", False):
            menu:
                "Offer her money":
                    $ store._cheat_counter_result = "offer_money"
                    return
                "Forget it":
                    $ store._cheat_counter_result = "denied"
                    return
        $ store._cheat_counter_result = "denied"
        return

    # Show counter-offer dialogue
    python:
        _co_key = (wanted_act, _co)
        _co_pool = _COUNTER_OFFER_LINES.get(_co_key, {}).get(_path)
        if not _co_pool:
            _co_pool = [_("How about something lighter first?")]
    $ Say_Line(girl, _cheat_line(girl, renpy.random.choice(_co_pool)))

    # Player choice: accept, offer money, or refuse
    menu:
        "Accept":
            $ _notify_cheat_heat(girl, "counter_accept")
            $ store._cheat_counter_result = _co
            return

        "Offer her money" if getattr(store, "_ctr_financial_available", False):
            $ store._cheat_counter_result = "offer_money"
            return

        "Refuse":
            $ _notify_cheat_heat(girl, "counter_refuse")
            python:
                _ref_pool = _COUNTER_REFUSE_LINES.get(_path, [_("Fine then.")])
            $ Say_Line(girl, _cheat_line(girl, renpy.random.choice(_ref_pool)))
            $ store._cheat_counter_result = "refused"
            return

# Routing helper: heat gain + counter-offer + scene launch in one call.
# Keeps each denial site to a single line.
label _cheat_counter_route(girl, wanted_act, position, anal=False):

    # Offended gate: stats too low for ANY counter-offer
    python:
        _ctr_sum = getattr(girl, "Love", 0) + getattr(girl, "Obed", 0) + getattr(girl, "Inbt", 0)
        debug_log("[OFFENDED] _cheat_counter_route: sum=%d wanted=%s" % (_ctr_sum, wanted_act))
    if _ctr_sum < 500:
        python:
            set_scene_expression(girl, "angry")
            _love_pen = -8 if wanted_act == "anal" else (-3 if wanted_act == "tip" else -5)
            Change_Status(girl, "Love", _love_pen)
            register_denial(girl, wanted_act)
            fail = {
                "score": 0, "tier": 0, "accepted": False,
                "outcome": "offended", "reason_primary": "offended",
                "reason_secondary": None, "reasons": ["offended"],
                "is_cheating": False, "cheating_state": None,
                "debug": {"offended": True},
            }
            setattr(girl, "LastApprovalResult", fail)
        call _deny_or_blackmail(girl, wanted_act) from _call_dob_cheat
        $ store._cheat_counter_result = "denied"
        return

    # position="anal" means doggy-anal context; resolve to actual position for scene launch
    python:
        _scene_pos = "doggy" if position == "anal" else position
        # read by the virgin refusal in _financial_attempt: an anal tip is not "losing her virginity for money"
        store._financial_is_anal = anal or position == "anal"
        _ctr_can_financial = _can_offer_money(girl) and not getattr(girl, "_ntr_boundary_discovered", False)
        _ctr_fin_attitude = _financial_attitude_stage(girl) if _ctr_can_financial else 0
        store._ctr_financial_available = _ctr_can_financial
        debug_log("[CHEAT_FIN] can_financial=%s attitude=%s wanted=%s pos=%s->%s" % (_ctr_can_financial, _ctr_fin_attitude, wanted_act, position, _scene_pos))

    # Girl-initiated financial (attitude 3+): she offers before counter-offer
    if _ctr_fin_attitude >= 3 and _ctr_can_financial:
        call _financial_girl_initiated(girl, wanted_act) from _call_fin_girl_init_cheat
        if store._financial_accepted:
            python:
                store._cheat_counter_result = "financial"
                store._coercion_type = "financial"
                store._financial_scene_active = True
                store._coercion_accepted = True
                _fin_act = wanted_act
                if getattr(store, "_financial_final_action", None):
                    _fin_act = store._financial_final_action
                    store._financial_final_action = None
                debug_log("[CHEAT_FIN] girl-initiated accepted: act=%s pos=%s" % (_fin_act, _scene_pos))
            # A negotiated lesser act (bj / tj / hj / masturbate) used to be counted here and then
            # nothing happened on screen. The central launcher starts the scene, which counts the act.
            call _coerced_act_launch(girl, _fin_act, _scene_pos, anal) from _call_cal_fin_cheat
            return

    call _cheat_counter_offer(girl, wanted_act) from _call_co_in_route

    if store._cheat_counter_result == "rub":
        if _is_on_cheat_path(girl) and _cheat_stage(girl) < 1:
            $ Say_Line(girl, _cheat_rub_first_line(girl))
            $ store._path1_rub_first_line_pending = True
        else:
            $ store._path1_rub_first_line_pending = False
        call start_rub(girl, _scene_pos) from _call_rub_ctr_rte

    elif store._cheat_counter_result == "tip":
        if _is_on_cheat_path(girl) and _cheat_stage(girl) < 2:
            $ Say_Line(girl, _cheat_tip_first_line(girl))
            $ store._path1_tip_first_line_pending = True
        else:
            $ store._path1_tip_first_line_pending = False
        call start_tip(girl, _scene_pos, anal=anal) from _call_tip_ctr_rte

    elif store._cheat_counter_result == "sex":
        if _is_on_cheat_path(girl) and not getattr(girl, "_cheat_broke", False):
            call condom_check(girl, True, "hard_deny") from _call_condom_ctr_rte_sex
            if store.condom_denied:
                return
        else:
            call condom_check(girl) from _call_condom_ctr_rte_sex_nr
            if store.condom_denied:
                return
        call start_scene(girl, "sex", _scene_pos) from _call_ss_ctr_rte_sex

    elif store._cheat_counter_result == "offer_money":
        call _financial_attempt(girl, wanted_act) from _call_fin_cheat_attempt
        if store._financial_accepted:
            python:
                store._coercion_type = "financial"
                store._financial_scene_active = True
                store._coercion_accepted = True
                _fin_act = wanted_act
                if getattr(store, "_financial_final_action", None):
                    _fin_act = store._financial_final_action
                    store._financial_final_action = None
                debug_log("[CHEAT_FIN] player-initiated accepted: act=%s pos=%s" % (_fin_act, _scene_pos))
            call _coerced_act_launch(girl, _fin_act, _scene_pos, anal) from _call_cal_fin_cheat2
        else:
            $ _notify_cheat_heat(girl, "gate_%s" % wanted_act, False)

    else:
        $ _notify_cheat_heat(girl, "gate_%s" % wanted_act, False)

    return

# Called during condom sex for cheat path girls — shows corruption narration
label _cheat_condom_corruption(girl):
    python:
        _cc = getattr(girl, "_cheat_condom_sex_count", 0)
        _cep = getattr(girl, "_cheat_escalation_path", 0)
        _broke = getattr(girl, "_cheat_broke", False)
    if _broke or _cc < 1:
        return

    # Mid-scene narration: she tries to remove condom
    python:
        if _cep == 1:
            _narr_pool = [
                _("In the heat of the moment, she reaches for the condom... her fingers start to pull it... but she stops herself."),
                _("Her hand wraps around the base and starts rolling the condom up... then she freezes and pulls away."),
                _("She grabs you and starts peeling the condom off... then catches herself and lets go."),
            ]
        elif _cep == 2:
            _narr_pool = [
                _("She reaches down and grabs the condom, pulling at it desperately... but forces herself to stop."),
                _("Her hips grind harder and she claws at the condom... then bites her lip and pulls her hand away."),
                _("She tries to rip it off in a frenzy... then catches your eye and reluctantly stops."),
            ]
        else:
            _narr_pool = [
                _("She reaches for the condom angrily, like she's about to tear it off... then stops and curses under her breath."),
                _("Her hands claw at the condom in frustration... she almost has it off before she catches herself."),
                _("She grabs the condom and starts pulling... muttering about how %(pp)s doesn't deserve this consideration."),
            ]
    $ Narration(_cheat_line(girl, renpy.random.choice(_narr_pool)))

    # Post-cum line: growing desire for raw
    python:
        if _cep == 1:
            _line_pool = [
                _("See? We used a condom... everything is fine, we didn't cheat on anyone... Even though it would be SO much better without it... going deep, skin on skin... BUT THAT WOULD BE CHEATING!"),
                _("Condom stayed on... so it doesn't count. It's NOT cheating... even if I keep wondering what it would feel like raw... NO! Condom means safe!"),
                _("We're fine... condom was on the whole time... my {hint}boyfriend{/hint} would understand... even though I almost... no. Condom. GOOD."),

            ]
        elif _cep == 2:
            _line_pool = [
                _("I almost lost it... I almost ripped it off. I wanted to feel you so badly... but I'm still in control. I'M STILL IN CONTROL."),
                _("God I wanted to take that off so bad... I need to feel you raw... but no. Not yet. I decide when. ME."),
                _("Every time it gets harder to keep that stupid thing on... I want you skin to skin so badly it HURTS... but I'm in charge here."),
            ]
        else:
            _line_pool = [
                _("Condom. Again. Because apparently I still care about being 'fair' to someone who doesn't even TOUCH me... Even though I want you raw so bad I could SCREAM."),
                _("We used a condom... for HIM. The man who ignores me. While I'm HERE wanting you without anything between us... his loss."),
                _("Another session with a condom... because I'm STILL protecting a relationship HE doesn't care about... I want you raw. I NEED you raw. But not today."),
            ]
    $ Say_Line(girl, _cheat_line(girl, renpy.random.choice(_line_pool)))
    "She seems to be slowly corrupting herself."
    return

# ============================================================
# BF PHONE CALL — phone vibrates mid-scene, boyfriend calling
# 100% chance (testing), once per run per girl, before broke
# ============================================================
label _cheat_bf_call_check(girl, scene_type):
    if not _is_on_cheat_path(girl):
        return
    if getattr(girl, "_cheat_broke", False):
        return
    if getattr(girl, "_cheat_bf_call_triggered", False):
        return
    if getattr(store, "_npc_passed_out", False):
        return
    if getattr(store, "_ntr_partner_watching", False):
        return
    if getattr(store, "_coercion_type", None) in ("blackmail", "financial"):
        return
    if renpy.random.random() > 0.25:
        return

    $ girl._cheat_bf_call_triggered = True

    # Notification sound
    play sound "audio/Notification.mp3" noloop

    # Surprised expression
    python:
        state = sprite_state.setdefault(girl.Id, {})
        _prev_eyes = state.get("eyes", "eyes_normal")
        _prev_mouth = state.get("mouth", "mouth_normal")
        _prev_brows = state.get("brows", "brows_normal")
        state["eyes"] = "eyes_surprised"
        state["mouth"] = "mouth_surprised"
        state["brows"] = "brows_surprised"

    call _cum_dispatch_apply_speed(girl, scene_type) from _call_as_bf_call

    python:
        _cep = getattr(girl, "_cheat_escalation_path", 0)

        if _cep == 1:
            _bf_call_lines = [
                _("Oh god... that's my {hint}boyfriend{/hint}'s ringtone! Stop, STOP! ...no wait, don't answer it. Just... don't stop either. Oh god, what am I doing?!"),

                _("That's HIM calling! He can't know about this! Just... keep going but be QUIET! ...I'm a terrible person."),
                _("My phone! That's my {hint}boyfriend{/hint}! I should answer... I should stop... why can't I make myself stop?!"),

            ]
        elif _cep == 2:
            _bf_call_lines = [
                _("Hm? That's my {hint}boyfriend{/hint}. He can wait. I'm busy with something... much better right now."),

                _("Oh, he's calling? That's cute. I'll call him back later. Don't you dare slow down."),
                _("My {hint}boyfriend{/hint}'s timing is impeccable. Ignore it. I'm not done with you yet."),

            ]
        else:
            _bf_call_lines = [
                _("Ha! That's HIM calling. If only he knew what I'm doing right now. His fault for ignoring me. Keep going."),
                _("My {hint}boyfriend{/hint}? Let it ring. He never calls when I actually need him, so why should I answer now?"),

                _("Oh, look who decided to call. Too late, sweetheart. I found someone who actually pays attention to me."),
            ]

    $ Say_Line(girl, _cheat_line(girl, renpy.random.choice(_bf_call_lines)))

    # Restore expression
    python:
        state["eyes"] = _prev_eyes
        state["mouth"] = _prev_mouth
        state["brows"] = _prev_brows

    call _cum_dispatch_apply_speed(girl, scene_type) from _call_as_bf_call_end

    return

# ============================================================
# SPANK MARK EVENT - visible marks after 3+ spanks, path reactions
# 30% chance, once per run per girl, before broke
# ============================================================
label _cheat_spank_mark_check(girl):
    if not _is_on_cheat_path(girl):
        return
    if getattr(girl, "_cheat_broke", False):
        return
    if getattr(girl, "_cheat_spank_mark_triggered", False):
        return
    if getattr(girl, "SpankLevel", 0) < 3:
        return
    if renpy.random.random() > 0.30:
        return

    $ girl._cheat_spank_mark_triggered = True

    python:
        _cep = getattr(girl, "_cheat_escalation_path", 0)
        _spank_lvl = getattr(girl, "SpankLevel", 0)
        _heavy = _spank_lvl >= 6

        if _cep == 1:
            if _heavy:
                _mark_lines = [
                    _("Oh no... look at the marks you left! My {hint}boyfriend{/hint} is going to see these! How am I supposed to explain bright red handprints on my ass?!"),

                    _("You spanked me so hard... these marks won't fade for DAYS! If my {hint}boyfriend{/hint} sees them I'll have to lie about falling or something!"),

                ]
            else:
                _mark_lines = [
                    _("Wait... are those marks? From the spanking? My {hint}boyfriend{/hint} might notice... I need to be more careful."),

                    _("I can feel the sting still... if my {hint}boyfriend{/hint} sees any redness I don't know what I'll say."),

                ]
        elif _cep == 2:
            if _heavy:
                _mark_lines = [
                    _("Mmm... look at those marks. Part of me wants my {hint}boyfriend{/hint} to see them and wonder who put them there."),

                    _("You really left your mark on me. I could hide them... or I could let him wonder. The thought excites me."),
                ]
            else:
                _mark_lines = [
                    _("Those marks... they're like a secret. My {hint}boyfriend{/hint} has no idea another man's handprints are on me."),

                    _("I can still feel where you hit me. It's thrilling knowing he'll never know about this."),
                ]
        else:
            if _heavy:
                _mark_lines = [
                    _("Ha! Look at these marks! I DARE my {hint}boyfriend{/hint} to ask about them. Maybe then he'll realize what he's been missing."),

                    _("You marked me good. If my {hint}boyfriend{/hint} notices? Good. Maybe he'll finally understand that ignoring me has consequences."),

                ]
            else:
                _mark_lines = [
                    _("Nice marks. My {hint}boyfriend{/hint} never does anything this exciting. His loss if he sees them."),

                    _("A little redness from a real man's hand. My {hint}boyfriend{/hint} wouldn't even know what to do with a girl like me."),

                ]

    $ set_scene_expression(girl, "smirk" if _cep == 3 else "embarrassed", blush=1)
    "..."
    $ Say_Line(girl, _cheat_line(girl, renpy.random.choice(_mark_lines)))
    $ set_scene_expression(girl, "normal", blush=0)

    return

# Called after any rub/tip/sex scene ends for a cheat path girl
# Only shows the afterscene line the FIRST time for each act type
label _cheat_afterscene(girl, act_type):
    python:
        _shown_key = "_cheat_afterscene_shown_%s" % act_type
        _already_shown = getattr(girl, _shown_key, False)
    if _already_shown:
        # Even if afterscene line was shown before, still check spank marks
        call _cheat_spank_mark_check(girl) from _call_cheat_spank_after_repeat
        return
    $ _after_line = _cheat_afterscene_line(girl, act_type)
    $ _bf_line = _bf_tier_guilt_line(girl, act_type)
    # Show if either path-specific or BF-tier guilt line exists
    if _after_line is not None or _bf_line is not None:
        $ setattr(girl, _shown_key, True)
        python:
            _as_slot = _safe_restore_slot(getattr(girl, "_prev_slot", StageCenter))
            _as_tf = [slot_left] if _as_slot == StageLeft else [slot_right] if _as_slot == StageRight else [slot_center]
        $ set_girl_sprite(girl.gid, pose="standing", at_list=_as_tf)
        $ set_scene_expression(girl, "sad", eyes="eyes_side", blush=1)
        "..."
        if _after_line is not None:
            $ Say_Line(girl, _after_line)

        # BF-tier-specific guilt emphasis
        if _bf_line is not None:
            $ Say_Line(girl, _bf_line)
            if act_type == "anal":
                $ girl.discover("discovered_bf_never_anal")

        # Comfort option — player can ease her guilt (reduces BF loyalty loss)
        if hasattr(girl, "has_npc_partner") and girl.has_npc_partner():
            menu:
                "Comfort her":
                    python:
                        _tier = girl.bf_loyalty_tier() if hasattr(girl, "bf_loyalty_tier") else "normal"
                        if _tier == "in_love":
                            _comfort_pool = [
                                _("You don't have to feel guilty. You came to me because something is missing. That's not your fault."),
                                _("Hey... it's okay. What happened between us doesn't make you a bad person."),
                            ]
                            _restore = 12
                        elif _tier == "normal":
                            _comfort_pool = [
                                _("Don't overthink it. You deserve to feel good. That's all this was."),
                                _("You're allowed to want things. Don't let guilt ruin this."),
                            ]
                            _restore = 8
                        elif _tier == "strained":
                            _comfort_pool = [
                                _("Things aren't great with him. You know that. This is just you taking care of yourself."),
                                _("You're not doing anything wrong. He stopped putting in the effort a long time ago."),
                            ]
                            _restore = 5
                        else:
                            _comfort_pool = [
                                _("You don't owe him anything. Especially not your happiness."),
                                _("Forget about him. You deserve better than what he gives you."),
                            ]
                            _restore = 3
                    $ Say_Player(_cheat_line(girl, renpy.random.choice(_comfort_pool)))
                    python:
                        if _tier == "in_love":
                            _comfort_react = renpy.random.choice([_("...Thank you. I needed to hear that. Even if I'm not sure I believe it yet."), _("You're sweet... I don't feel as terrible now. But I still feel something.")])
                        elif _tier == "normal":
                            _comfort_react = renpy.random.choice([_("Maybe you're right... I do deserve this."), _("...Yeah. You're right. I shouldn't feel guilty for wanting more.")])
                        elif _tier == "strained":
                            _comfort_react = renpy.random.choice([_("You're right. He gave up on us first."), _("I know... I just needed someone to say it out loud.")])
                        else:
                            _comfort_react = renpy.random.choice([_("You're damn right I don't."), _("I stopped caring what he thinks a long time ago. But hearing you say it helps.")])
                    $ Say_Line(girl, _cheat_line(girl, _comfort_react))
                    $ girl.change_bf_loyalty(_restore)
                    $ Change_Status(girl, "Love", 5)

                "Brag about it":
                    python:
                        _brag_pool = [
                            _("You know my cock is way better than his."),
                            _("He'd never make you cum like I do."),
                            _("You moan louder with me and you know it."),
                        ]
                    $ Say_Player(_cheat_line(girl, renpy.random.choice(_brag_pool)))
                    $ set_scene_expression(girl, "worried", blush=2)
                    python:
                        _tier = girl.bf_loyalty_tier() if hasattr(girl, "bf_loyalty_tier") else "normal"
                        if _tier == "in_love":
                            _brag_react = renpy.random.choice([
                                _("...Don't say that about him. He's still... he's still my boyfriend."),
                                _("That's not fair... but I can't exactly argue after what just happened."),
                            ])
                            _obed_gain = 6
                            _love_change = -5
                            _loyalty_loss = -5
                        elif _tier == "normal":
                            _brag_react = renpy.random.choice([
                                _("...You don't have to rub it in. But... you're not wrong."),
                                _("Stop... you're making this worse. And I hate that you're right."),
                            ])
                            _obed_gain = 8
                            _love_change = 0
                            _loyalty_loss = -8
                        elif _tier == "strained":
                            _brag_react = renpy.random.choice([
                                _("...Yeah. You're right. He never made me feel like this."),
                                _("I know. Trust me, I know. He doesn't even come close."),
                            ])
                            _obed_gain = 12
                            _love_change = 0
                            _loyalty_loss = -6
                        else:
                            _brag_react = renpy.random.choice([
                                _("Tell me something I don't know. He's pathetic compared to you."),
                                _("Damn right. He couldn't satisfy me if his life depended on it."),
                            ])
                            _obed_gain = 15
                            _love_change = 0
                            _loyalty_loss = -3
                    $ Say_Line(girl, _cheat_line(girl, _brag_react))
                    $ Change_Status(girl, "Obed", _obed_gain)
                    if _love_change:
                        $ Change_Status(girl, "Love", _love_change)
                    $ girl.change_bf_loyalty(_loyalty_loss)

                "Say nothing":
                    pass

        $ set_scene_expression(girl, "normal", blush=0)
    # Spank mark check (centralized - fires from all 6 afterscene call points)
    call _cheat_spank_mark_check(girl) from _call_cheat_spank_after
    return

# ============================================================
# BREAKING POINT SCENE — mid-scene, she snaps and removes condom
# Called from control menus during keep going
# ============================================================
label _cheat_breaking_point(girl, scene_type):
    $ debug_log("[DEBUG] BREAKING POINT: triggered for %s in %s" % (girl.gid, scene_type))

    # She snaps
    $ set_scene_expression(girl, "lipbite", blush=2)
    $ Say_Line(girl, _cheat_breaking_line(girl))

    # She rips the condom off. force=True: this IS the girl-initiated removal, so
    # it must bypass the cheat-path condom block. Without it, _on_condom_removed
    # sees she isn't broken yet (set below), fires a "keep the condom on!" refusal,
    # and returns WITHOUT clearing condom_active -> contradictory line + the condom
    # sprite re-appears on the next ApplySpeed.
    "She reaches down and rips the condom off before you can react."
    $ _on_condom_removed(girl, skip_hide=_cum_skip_hide(scene_type), force=True)
    call _cum_dispatch_condom_remove(girl, scene_type) from _call_cdr_cheat_break

    # Mark her as broken — no more condom requirement
    $ girl._cheat_broke = True
    $ girl.discover("discovered_trait_cheater") if girl.has_trait("cheater") else None
    $ unlock_achievement("broken_will")

    # Follow-up line
    python:
        p = getattr(girl, "_cheat_escalation_path", 0)
        if p == 1:
            _bp_followup = [
                _("YES! Oh god YES! THIS is what I've been denying myself!"),
                _("I can feel EVERYTHING! Why did I wait so long?!"),
                _("So THIS is what it feels like without that stupid thing... I'm never going back!"),
            ]
        elif p == 2:
            _bp_followup = [
                _("FUCK! This is SO much better! I knew I couldn't control myself forever!"),
                _("I can feel every inch... I'm completely lost and I don't CARE!"),
                _("This is what I've been craving... no more pretending!"),
            ]
        else:
            _bp_followup = [
                _("THIS is what he should have been giving me! NOW I know what I was missing!"),
                _("He'll never know... and honestly? He doesn't DESERVE to know how good this feels!"),
                _("Complete betrayal... and it feels INCREDIBLE!"),
            ]
    $ Say_Line(girl, _cheat_line(girl, renpy.random.choice(_bp_followup)))

    # Re-apply speed to refresh sprite without condom
    call _cum_dispatch_apply_speed(girl, scene_type) from _call_cas_cheat_break

    return

label cheat_escalation_scene(girl):

    $ _esc_action = getattr(store, "_cheat_escalation_action", "hj")
    $ _esc_tier = getattr(store, "_cheat_escalation_tier", 2)
    $ store._cheat_escalation_pending = False

    # Persist path per girl — once chosen, stays the same for all escalation tiers
    python:
        _saved_path = getattr(girl, "_cheat_escalation_path", 0)
        if _saved_path:
            _esc_path = _saved_path
        else:
            _esc_path = _pick_escalation_path(girl)
            girl._cheat_escalation_path = _esc_path

    # Show her standing with sad expression
    $ set_girl_sprite(girl.gid, pose="standing", at_list=[slot_center])
    $ set_scene_expression(girl, "sad")

    python:
        _esc_bf = "{hint}%s{/hint}" % girl.partner_label()

    # ================================================================
    # PATH 1 — INNOCENT / DENIAL ("It's not really cheating")
    # Higher chance for: loyal, cute_sex
    # She convinced herself it wasn't real cheating. Player played along.
    # ================================================================
    if _esc_path == 1:
        "She stops. Her expression shifts, like something just clicked."

        if _esc_tier == 2:
            # HJ / TJ — she rationalized it as "just helping" or "a massage"
            $ set_scene_expression(girl, "sad", eyes="eyes_side")
            python:
                _esc_lines = [
                    _("Wait... that wasn't... I mean, you said it was like a massage, right? Just... hands?"),
                    _("That's... that's not cheating, right? It's just... touching. People touch each other all the time."),
                    _("You said it wasn't a big deal. Just helping out. That's all it was... right?"),
                    _("My [_esc_bf] wouldn't consider this cheating. It's just... it's nothing. It has to be nothing."),
                ]
            $ Say_Line(girl, _cheat_line(girl, renpy.random.choice(_esc_lines)))

            "She's trying to convince herself more than you."

            menu:
                "It's not cheating. Just two friends helping each other.":
                    # Love path — reinforce her denial
                    $ Say_Line(girl, _("Right... right. That's what I thought. Friends do this. It's normal."))
                    "She nods to herself, clearly not fully believing it."
                    $ Say_Line(girl, _("Just... don't tell anyone. And we probably shouldn't do it again."))
                    $ Change_Status(girl, "Love", 5)
                    $ Change_Status(girl, "Inbt", 3)

                "You know exactly what it was. And you liked it.":
                    # Obed path — break the denial
                    $ Say_Line(girl, _("I... no. Don't say that. That's not..."))
                    "She goes quiet."
                    $ set_scene_expression(girl, None, blush="2")
                    $ Say_Line(girl, _("...Maybe I did. But that doesn't make it okay."))
                    $ Change_Status(girl, "Obed", 8)
                    $ Change_Status(girl, "Inbt", 5)
                    $ Change_Status(girl, "Love", -3)

        else:
            # BJ — harder to deny
            python:
                _esc_lines = [
                    _("Oh god... I just... with my mouth... that's... that's definitely not 'just helping', is it?"),
                    _("I told myself touching was one thing. But THIS? I can't pretend this is a massage."),
                    _("Using my hands was one thing... but my mouth? What am I even doing anymore?"),
                    _("This is so much worse than before. My [_esc_bf] would never forgive me for this."),
                ]
            $ Say_Line(girl, _cheat_line(girl, renpy.random.choice(_esc_lines)))

            "Her eyes are wide. The denial she built up is crumbling."
            $ set_scene_expression(girl, None, blush="1")

            menu:
                "Hey. You wanted to. And it felt good for both of us.":
                    $ set_scene_expression(girl, None, blush="2")
                    $ Say_Line(girl, _("I know... that's what scares me. I WANTED to do it."))
                    "She hugs herself, staring at the floor."
                    $ Say_Line(girl, _("What kind of person does that make me...?"))
                    $ Change_Status(girl, "Love", 3)
                    $ Change_Status(girl, "Inbt", 5)

                "Your [_cheat_partner_label(girl)] can't give you what I can. You know that.":
                    $ set_scene_expression(girl, None, blush="2")
                    $ Say_Line(girl, _cheat_line(girl, _("Stop... don't bring him into this. He's a good person.")))
                    "A pause."
                    $ Say_Line(girl, _cheat_line(girl, _("...But you're right. He never makes me feel like... like that.")))
                    $ Change_Status(girl, "Obed", 8)
                    $ Change_Status(girl, "Inbt", 8)
                    $ Change_Status(girl, "Love", -2)

    # ================================================================
    # PATH 2 — TEMPTED / CURIOSITY ("I was curious, I'm in control")
    # Higher chance for: hardcore_sex, cum_slut
    # She was drawn by lust/size and thinks she decides when to stop.
    # ================================================================
    elif _esc_path == 2:
        $ set_scene_expression(girl, "lusty", blush=1)
        "She catches her breath, but there's no panic in her eyes. Just... hunger."

        if _esc_tier == 2:
            python:
                _esc_lines = [
                    _("I was just... curious. I've been wanting to know what it felt like. Yours is... bigger than his."),
                    _("Don't get the wrong idea. I just wanted to try it once. I'm the one who decides when this stops."),
                    _("This doesn't mean anything. I was curious and now I know. We're done when I say we're done."),
                    _("I'm not some cheating slut. I just... needed to feel something different. I'm still in control."),
                ]
            $ Say_Line(girl, _cheat_line(girl, renpy.random.choice(_esc_lines)))

            "She's breathing fast. Her hands are still trembling from what she just did."

            menu:
                "If you say so. But you can come back anytime you want.":
                    # Love path — let her feel in control
                    $ Say_Line(girl, _("I might. Or I might not. That's MY decision."))
                    "She straightens up, trying to look composed."
                    $ Say_Line(girl, _("...But it did feel really good. Maybe just one more time. Eventually."))
                    $ Change_Status(girl, "Love", 5)
                    $ Change_Status(girl, "Inbt", 5)
                    $ girl.Lust = min(100, getattr(girl, "Lust", 0) + 10)

                "I know you couldn't resist. This will happen again soon":
                    # Obed path — expose the illusion
                    $ set_scene_expression(girl, "surprised", blush=2)
                    $ Say_Line(girl, _("That's not... I chose to be here. I CHOSE this."))
                    "You stare at her without saying anything."
                    $ Say_Line(girl, _("...Fine. Maybe I couldn't stop thinking about it. But that doesn't mean I'll lose control."))
                    $ Change_Status(girl, "Obed", 10)
                    $ Change_Status(girl, "Inbt", 5)

        else:
            # BJ — she went further than planned
            python:
                _esc_lines = [
                    _("I was only going to use my hands again... but then I just... I couldn't help myself."),
                    _("I keep telling myself I'm in control. But then I was on my knees and... god, I wanted it."),
                    _("I promised myself I wouldn't go further. And here I am with the taste of you in my mouth."),
                    _("His dick never made me want to... to do THAT. But yours... I couldn't stop myself."),
                ]
            $ Say_Line(girl, _cheat_line(girl, renpy.random.choice(_esc_lines)))

            "She wipes her mouth. Her eyes say she's already thinking about next time."

            menu:
                "You enjoyed it. There's nothing wrong with that.":
                    $ Say_Line(girl, _("I know I enjoyed it. That's the problem. I enjoyed it WAY too much."))
                    $ Say_Line(girl, _cheat_line(girl, _("If he ever finds out I put another man's cock in my mouth... he'd die.")))
                    $ set_scene_expression(girl, None, blush="2")
                    "She shakes her head but can't hide the flush on her face."
                    $ Change_Status(girl, "Love", 5)
                    $ Change_Status(girl, "Inbt", 8)
                    $ girl.Lust = min(100, getattr(girl, "Lust", 0) + 10)

                "Face it. You lost control the moment you saw it.":
                    $ set_scene_expression(girl, "lipbite", blush=2)
                    $ Say_Line(girl, _("Shut up. I'm not... I didn't..."))
                    "She can't even finish the sentence."
                    $ Say_Line(girl, _cheat_line(girl, _("...Okay. Maybe I did. Maybe I'm losing my mind. But I'm NOT his little obedient girlfriend anymore.")))
                    $ Change_Status(girl, "Obed", 10)
                    $ Change_Status(girl, "Inbt", 8)
                    $ girl.Lust = min(100, getattr(girl, "Lust", 0) + 5)

    # ================================================================
    # PATH 3 — EXCUSE / REVENGE ("I'm being ignored, this will help")
    # Higher chance for: public_fetish, exhibitionist
    # She frames it as revenge or relationship improvement.
    # ================================================================
    else:
        $ set_scene_expression(girl, "normal", eyes="eyes_side")
        "She doesn't look guilty. She looks... justified."

        if _esc_tier == 2:
            python:
                _esc_lines = [
                    _("He's been ignoring me lately. This is just... me reminding myself I'm still desirable."),
                    _("Maybe if he paid more attention to me, I wouldn't need someone else's hands on me."),
                    _("I'm not cheating. I'm just... giving him a reason to try harder. He won't even know."),
                    _("It's his fault, really. A girl has needs. And he hasn't been meeting them."),
                ]
            $ Say_Line(girl, _cheat_line(girl, renpy.random.choice(_esc_lines)))

            "She crosses her arms, daring you to judge her."

            menu:
                "You deserve someone who appreciates you.":
                    # Love path — validate her feelings
                    $ set_scene_expression(girl, None, blush="1")
                    $ Say_Line(girl, _("Thank you. At least SOMEONE gets it."))
                    "She relaxes a little."
                    $ Say_Line(girl, _("Maybe we can do this again sometime. Just... between us. To keep things spicy."))
                    $ Change_Status(girl, "Love", 8)
                    $ Change_Status(girl, "Inbt", 3)

                "You're making excuses. You did it because you wanted MY hands on you.":
                    # Obed path — cut through the justification
                    $ set_scene_expression(girl, "surprised", blush=2)
                    $ Say_Line(girl, _("What? No! This has nothing to do with you specifically!"))
                    "You raise an eyebrow."
                    $ Say_Line(girl, _("...Okay, maybe it does. Maybe I've been thinking about it for a while. Happy now?"))
                    $ Change_Status(girl, "Obed", 8)
                    $ Change_Status(girl, "Inbt", 5)
                    $ Change_Status(girl, "Love", -2)

        else:
            # BJ — her excuse is getting thin
            python:
                _esc_lines = [
                    _("I needed to feel wanted. My [_esc_bf] barely looks at me anymore. And you... you look at me like I'm everything."),
                    _("He can't even be bothered to touch me properly. So yeah, I put another man's cock in my mouth. Sue me."),
                    _("Maybe this will make me appreciate what I have with him more. Or maybe I'll realize I've been wasting my time."),
                    _("I told myself this was just to scare him a little. But now I realize he'll never know. And I don't even care."),
                ]
            $ Say_Line(girl, _cheat_line(girl, renpy.random.choice(_esc_lines)))

            "The defiance in her voice is cracking. Reality is setting in."

            menu:
                "You don't have to justify it. You wanted it and that's okay.":
                    $ Say_Line(girl, _("I DID want it. And that terrifies me."))
                    "She looks away."
                    $ Say_Line(girl, _("Because now I know what I've been missing. And I can't un-know that."))
                    $ Change_Status(girl, "Love", 5)
                    $ Change_Status(girl, "Inbt", 8)

                "Your [_cheat_partner_label(girl)] is the excuse. I'm the reason. Admit it.":
                    $ set_scene_expression(girl, "shy", blush=2)
                    $ Say_Line(girl, _("You're so full of yourself..."))
                    "But she doesn't deny it."
                    $ Say_Line(girl, _cheat_line(girl, _("...Fine. You're the reason. He's just the excuse I use to sleep at night.")))
                    $ Change_Status(girl, "Obed", 10)
                    $ Change_Status(girl, "Inbt", 8)
                    $ Change_Status(girl, "Love", -3)

    # --- Common aftermath ---
    "An awkward silence fills the room."
    $ set_scene_expression(girl, "normal", blush=0)

    python:
        _esc_in_player_room = (store.CurrentLocation == "room")
        if _esc_in_player_room:
            _esc_exit = [
                _("I need to go. I need to think about what I'm doing."),
                _("I can't be here right now. I need some time."),
                _("I should leave before I do something else I might regret."),
            ]
        else:
            _esc_exit = [
                _("I think you should go. I need to think about what I'm doing."),
                _("Let's not talk about this right now. Just... give me some time."),
                _("You should leave before I do something else I might regret."),
            ]
    $ Say_Line(girl, _cheat_line(girl, renpy.random.choice(_esc_exit)))

    # Restore her clothes
    $ girl.RestoreOutfit()

    # She needs space for the rest of the day
    $ girl.set_temp_status("sad", days=1, reason="cheat_escalation")

    $ hide_girl_sprite(girl)

    python:
        if girl in store.Party:
            store.Party.remove(girl)   # or the next navigate_to pulls her right back along
        _home = girl_home_loc(girl)
        girl.loc = _home
        _esc_in_hangout = bool([g for g in _live_hangout_girls() if g.gid != girl.gid])
        store._sex_session_over = True
        store._coercion_type = None
        store._coercion_type_for_post = None

    if _esc_in_hangout:
        $ Narration(_("Without another word, she grabs her things and leaves."))
    elif _esc_in_player_room:
        $ Narration(_("Without another word, she grabs her things and walks out. The door closes quietly behind her."))
    else:
        scene bg Door
        with dissolve
        $ Narration(_("She asks you to leave. You step outside and the door closes quietly behind you."))
        $ navigate_to("campus", None)
        call Set_Scene(entry=True) from _call_Set_Scene_cheat_esc

    return

# =============================================================
# HEAT RELIEF LABEL
# Girl proactively suggests the next-stage act when heat is high.
# Called from the "Have Sex" menu before position selection.
# Sets store._heat_relief_result to the act or "refused".
# =============================================================

label _cheat_heat_relief(girl):
    # Use pre-computed act from store._hr_pending_act (avoids double random roll)
    python:
        _hr_act = getattr(store, "_hr_pending_act", None)
        store._hr_pending_act = None  # consume
    if _hr_act is None:
        $ store._heat_relief_result = None
        return

    $ store._heat_relief_done_this_session = True

    # She speaks up — BF-tier-aware suggestion
    $ set_scene_expression(girl, "lipbite", blush=2)
    $ Say_Line(girl, _heat_relief_line(girl, _hr_act))

    menu:
        "Give in":
            # Heat drops, she gets what she wants
            python:
                _drop = _HEAT_RELIEF_DROP.get(_hr_act, -20)
                _reduce_cheat_heat(girl, abs(_drop), "heat_relief_%s" % _hr_act)
                store._heat_relief_result = _hr_act
            $ set_scene_expression(girl, "pleasure", blush=1)
            $ Say_Line(girl, renpy.random.choice(_HEAT_RELIEF_ACCEPT.get(_hr_act, [_("Yes...")])))
            return

        "Not enough":
            # Player holds out — heat stays, +5 bump from the tension
            $ _add_cheat_heat(girl, 5, "heat_relief_refuse")
            $ store._heat_relief_result = "refused"
            $ set_scene_expression(girl, "sad", blush=1)
            $ Say_Line(girl, _heat_relief_refuse_line(girl))
            $ set_scene_expression(girl, "normal", blush=0)
            return
