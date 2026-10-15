# ============================================================
# ACHIEVEMENT SYSTEM — persistent across saves and runs
# ============================================================

init python:

    # ── Achievement registry ────────────────────────────────

    ACHIEVEMENTS = {
        "not_santa_claus": {
            "name": _("Not Santa Claus"),
            "hint": _("Guess the right girl on campus"),
        },
        "moonlight_nude": {
            "name": _("Under the moonlight"),
            "hint": _("Find her at the pool at night"),
        },
        "hardcore_player": {
            "name": _("Hardcore Player"),
            "hint": _("Start with all negative traits (all girls)"),
        },
        "shower_masturbation": {
            "name": _("Shower Masturbation"),
            "hint": _("Get a girl in the showers"),
        },
        "room_masturbation": {
            "name": _("Room Masturbation"),
            "hint": _("Get a girl in her room"),
        },
        "knock_knock": {
            "name": _("Knock Knock"),
            "hint": _("Someone's at the door"),
        },
        "gf_at_the_door": {
            "name": _("Special Knock"),
            "hint": _("Your girlfriend's at the door"),
        },
        "blackmail": {
            "name": _("Blackmail"),
            "hint": _("End her relationship"),
        },
        "max_fit": {
            "name": _("Max Fit"),
            "hint": _("On the juice"),
        },
        "neeeerd": {
            "name": _("Neeeerd"),
            "hint": _("Ace the test"),
        },
        "girls_night": {
            "name": _("Girls' Night"),
            "hint": _("Invite the girls over"),
        },
        "unwanted_gift": {
            "name": _("Unwanted Gift"),
            "hint": _("Give her what she hates most"),
        },
        "say_cheese": {
            "name": _("Say Cheese"),
            "hint": _("Camera is her worst nightmare"),
        },
        "broken_will": {
            "name": _("Broken Will"),
            "hint": _("Break her (engaged)"),
        },
        "broken_by_accident": {
            "name": _("Happy Accident"),
            "hint": _("The condom decided for her"),
        },
        "she_wants_it": {
            "name": _("She Wants It"),
            "hint": _("She asked for more"),
        },
        "just_the_tip": {
            "name": _("Just The Tip"),
            "hint": _("It wasn't just the tip"),
        },
        "red_handed": {
            "name": _("Red Handed"),
            "hint": _("Leave your mark on her"),
        },
        "no_choice": {
            "name": _("No Choice - Creampie"),
            "hint": _("She decided for you"),
        },
        "double_betrayal": {
            "name": _("Double Betrayal"),
            "hint": _("Four hearts, zero loyalty"),
        },
        "till_death": {
            "name": _("Till Death Do Us Part"),
            "hint": _("His ring, your mark"),
        },
        "study_session": {
            "name": _("Study Session"),
            "hint": _("Your father thinks she's tutoring you"),
        },
        "group_chat": {
            "name": _("Group Chat"),
            "hint": _("The more the merrier"),
        },
        "persistence_pays": {
            "name": _("Persistence Pays Off"),
            "hint": _("Not now... not now... and Creampie."),
        },
        "backdoor_virgin": {
            "name": _("Backdoor Virgin"),
            "hint": _("Find the loophole"),
        },
        "wrong_order": {
            "name": _("Wrong Order"),
            "hint": _("Start from the last page"),
        },
        "it_doesnt_count": {
            "name": _("It Doesn't Count"),
            "hint": _("Wrong hole, clear conscience"),
        },
        "acquired_taste": {
            "name": _("Acquired Taste"),
            "hint": _("From the back door to the mouth"),
        },
        "until_the_end": {
            "name": _("Until The End"),
            "hint": _("Hold her and make her swallow"),
        },
        "first_kiss": {
            "name": _("First Kiss"),
            "hint": _("She said she'd never kiss a guy"),
        },
        "soap_time": {
            "name": _("Soap Time"),
            "hint": _("Let her use soap on you"),
        },
        "fight_fight_fight": {
            "name": _("Fight Fight Fight"),
            "hint": _("Win a fight without throwing a punch"),
        },
        "expensive_pie": {
            "name": _("Expensive Pie"),
            "hint": _("Pay for the ultimate act"),
        },
        "reverse_card": {
            "name": _("Reverse Card"),
            "hint": _("Make her pay"),
        },
        "game_night": {
            "name": _("Game Night"),
            "hint": _("Buy vodka and Invite them"),
        },
        "jurassic_help": {
            "name": _("Jurassic Help"),
            "hint": _("Get a hidden tip from the caveman"),
        },
        "fashion_stylist": {
            "name": _("Fashion Stylist"),
            "hint": _("Accompany her in the dressing room"),
        },
        "oops_it_broke": {
            "name": _("Oops, It Broke"),
            "hint": _("Rip a condom"),
        },
        "hot_date": {
            "name": _("Hot Date"),
            "hint": _("Trigger a special event during a date"),
        },
        "perfect_fit": {
            "name": _("Occupied Fitting Room"),
            "hint": _("Walk around the mall as a trio"),
        },
        "wingman": {
            "name": _("Wingman"),
            "hint": _("Befriend him, then betray him"),
        },
        "iron_will": {
            "name": _("Iron Will"),
            "hint": _("She tried, but you're stronger"),
        },
        "sugar_daddy": {
            "name": _("Sugar Daddy"),
            "hint": _("She comes to you for money now"),
        },
        "cuckold_show": {
            "name": _("Private Show"),
            "hint": _("He watched the whole thing"),
        },
        "boundary_broken": {
            "name": _("Boundary Broken"),
            "hint": _("Cross every line he drew"),
        },
        "viral_video": {
            "name": _("Viral Video"),
            "hint": _("Send it to the wrong person"),
        },
        "full_access": {
            "name": _("Full Access"),
            "hint": _("He gave up all limits"),
        },
        "double_trouble": {
            "name": _("Double Trouble"),
            "hint": _("Under the table, two mouths are better than one"),
        },
        "hidden_menu": {
            "name": _("Hidden Menu"),
            "hint": _("Peek under the tablecloth"),
        },
        "fitting_fun": {
            "name": _("Fitting Fun"),
            "hint": _("The curtain doesn't lock"),
        },
        "restroom_break": {
            "name": _("Restroom Break"),
            "hint": _("She locked the door behind you"),
        },
        "ask_permission": {
            "name": _("Ask Permission"),
            "hint": _("She asked him. He said yes."),
        },
        "hidden_cream": {
            "name": _("Hidden Cream"),
            "hint": _("She thinks the condom worked"),
        },
        "ugly_bastard": {
            "name": _("Ugly Bastard"),
            "hint": _("Even ugly can conquer a mind"),
        },
        "femdom_cuckold": {
            "name": _("Femdom Cuckold"),
            "hint": _("Exhibitionist + Cheater + NTR"),
        },
        "shes_my_favorite": {
            "name": _("She's My Favorite"),
            "hint": _("She cums twice, the other zero"),
        },
        "party_for_three": {
            "name": _("Party for 3"),
            "hint": _("3 girls in the hangout"),
        },
        "cups_and_hangout": {
            "name": _("Cups and Hangout"),
            "hint": _("2 girls and 1 NPC"),
        },
        "party_must_go_on": {
            "name": _("The Party Must Keep Going"),
            "hint": _("NPC drank too much"),
        },
        "secret_party": {
            "name": _("Secret Party After Some Drinks"),
            "hint": _("You have more time with the girl"),
        },
        "the_3_way": {
            "name": _("The 3 Way"),
            "hint": _("1 + 1 + 1"),
        },
        "female_rivalry": {
            "name": _("Female Rivalry"),
            "hint": _("Build a harem with girls who hate each other"),
        },
        "helping_hand": {
            "name": _("Helping Hand"),
            "hint": _("Threesome with a condom and one who likes it raw"),
        },
        "stealth_master": {
            "name": _("Stealth Master"),
            "hint": _("She never saw it coming off"),
        },
        "worst_first_kiss": {
            "name": _("Worst First Kiss"),
            "hint": _("Her lips touched something else before yours"),
        },
        "identity_crisis": {
            "name": _("Identity Crisis"),
            "hint": _("Break a lesbian completely"),
        },
        "edge_lord": {
            "name": _("Edge Lord"),
            "hint": _("Deny her three times in a row"),
        },
        "speedrun": {
            "name": _("Speedrun"),
            "hint": _("Skip every step with a virgin"),
        },
        "change_of_heart": {
            "name": _("Change of Heart"),
            "hint": _("She used to hate it"),
        },
        "secret_admirer": {
            "name": _("Secret Admirer"),
            "hint": _("Fulfill a very familiar request on BigFans"),
        },
        "homewrecker": {
            "name": _("Homewrecker"),
            "hint": _("She chose you over her partner"),
        },
        "stage_fright": {
            "name": _("Stage Fright"),
            "hint": _("She's shy, this is public"),
        },
        "directors_cut": {
            "name": _("Director's Cut"),
            "hint": _("Her first time, on camera"),
        },
        "hold_steady": {
            "name": _("Hold Steady!"),
            "hint": _("Hold on for at least 3 acts after reaching max lust"),
        },
        "playing_both_sides": {
            "name": _("Playing Both Sides"),
            "hint": _("Make someone discover a new side of herself"),
        },
        "great_good_morning": {
            "name": _("A Great Good Morning"),
            "hint": _("Pleasure upon waking"),
        },
        "bad_influence": {
            "name": _("Bad Influence"),
            "hint": _("The nerd gets an F"),
        },
        "second_chances": {
            "name": _("Second Chances"),
            "hint": _("Re-date an ex"),
        },
        "she_came_to_me": {
            "name": _("She Came to Me"),
            "hint": _("Accept a girl's confession"),
        },
        "forgive_and_forget": {
            "name": _("Forgive and Forget"),
            "hint": _("Reconcile with a cheating ex"),
        },
        "trust_rebuilt": {
            "name": _("Trust Rebuilt"),
            "hint": _("Rebuild trust completely with a reconciled ex"),
        },
        "heartbreaker": {
            "name": _("Heartbreaker"),
            "hint": _("Break 2 or more hearts"),
        },
        "noisy_bet": {
            "name": _("Noisy Bet"),
            "hint": _("Make him lose the bet"),
        },
        # her NPC partner holds the phone while the player is inside her (interactions.rpy _watcher_record_start)
        "behind_the_camera": {
            "name": _("Behind the Camera"),
            "hint": _("Her partner held the camera while you took her"),
        },
        # a girl watcher holds the phone during a threesome (interactions.rpy _watcher_record_start)
        "girl_behind_camera": {
            "name": _("Her Turn to Film"),
            "hint": _("She watched AND recorded"),
        },
        # have sex during NTR bet event while NPC hasn't turned around yet (ntr_bet_event.rpy _bet_sex_loop)
        "ntr_listening": {
            "name": _("Thin Walls"),
            "hint": _("He's right there, but hasn't looked yet"),
        },
        # children (children.rpy: _CHILD_ACHIEVEMENTS decides when)
        "first_child": {
            "name": _("Proud Father"),
            "hint": _("Have your first child"),
        },
        "two_cribs": {
            "name": _("Two Cribs"),
            "hint": _("Have children with 2 different girls"),
        },
        "full_house": {
            "name": _("Full House"),
            "hint": _("Have a child with every girl"),
        },
        "not_the_father": {
            "name": _("Not the Father"),
            "hint": _("Let someone else raise your child"),
        },
        # pregnancy (2026-09-19, author: players who skip the changelog should see what is possible)
        "the_big_lie": {
            "name": _("The Big Lie"),
            "hint": _("Convince her to tell her boyfriend the baby is his"),
        },
        "eyes_wide_open": {
            "name": _("Eyes Wide Open"),
            "hint": _("Her partner knows it's yours and raises it anyway"),
        },
        "not_supposed_to_be_possible": {
            "name": _("Not Supposed to Be Possible"),
            "hint": _("Get a lesbian pregnant"),
        },
        "immaculate_conception": {
            "name": _("Immaculate Conception"),
            "hint": _("Get a girl with a girlfriend pregnant"),
        },
        "against_all_odds": {
            "name": _("Against All Odds"),
            "hint": _("Her partner forgives a baby that isn't theirs"),
        },
        "baby_fever": {
            "name": _("Baby Fever"),
            "hint": _("Get a girl pregnant who was hoping for it"),
        },
        "sugar_pills": {
            "name": _("Sugar Pills"),
            "hint": _("Get her pregnant while she trusts the pills you gave her"),
        },
        "baby_boom": {
            "name": _("Baby Boom"),
            "hint": _("Get every girl on campus pregnant at the same time"),
        },
        "plan_b": {
            "name": _("Plan B"),
            "hint": _("Talk her into the morning after pill"),
        },
        "full_term": {
            "name": _("Full Term"),
            "hint": _("Take her when her belly is at its roundest"),
        },
        # her partner on scene while you flirt (FLIRT_PARTNER_WATCH) / her taste in gifts (GIRL_GIFT_TASTE)
        "close_call": {
            "name": _("Close Call"),
            "hint": _("Kiss her with her partner right there, and get away with it"),
        },
        "perfect_gift": {
            "name": _("Perfect Gift"),
            "hint": _("Give her a gift she loves"),
        },
        # her partner at your door after 3 nights of sleepovers, and he leaves without her (sleepover.rpy)
        "finders_keepers": {
            "name": _("Finders Keepers"),
            "hint": _("Keep her in your room when her partner comes looking for her"),
        },
        # a nerd gets carried away in a Chit Chat and talks for most of the slot (nerd_ramble.rpy)
        "nerds_talk": {
            "name": _("Nerds Talk"),
            "hint": _("She gets carried away in the conversation"),
        },
        # ── Her Story (the story ladder, story_steps.rpy; today the stepmom) ──
        "won_her_heart": {
            "name": _("Won Her Heart"),
            "hint": _("Complete her story by earning her"),
        },
        "under_your_thumb": {
            "name": _("Under Your Thumb"),
            "hint": _("Complete her story through leverage"),
        },
        "what_she_hides": {
            "name": _("What She Hides"),
            "hint": _("Uncover her secret life"),
        },
        "the_queen_falls": {
            "name": _("The Queen Falls"),
            "hint": _("Make a dominant girl lose her crown"),
        },
        "beg_for_it": {
            "name": _("Beg For It"),
            "hint": _("Hear a dominant girl beg"),
        },
        "not_for_sale": {
            "name": _("Not For Sale"),
            "hint": _("Offer money to the wrong woman"),
        },
        "lawyers_on_retainer": {
            "name": _("Lawyers On Retainer"),
            "hint": _("Blackmail a woman out of your league"),
        },
        # ── exclusive acts (POSE_ONLY_FOR: one girl has the art) ──
        "kiss_the_throne": {
            "name": _("Kiss the Throne"),
            "hint": _("Get a rimjob"),
        },
        "best_foot_forward": {
            "name": _("Best Foot Forward"),
            "hint": _("Get a footjob"),
        },
        # ── the turned queen (control corruption stage 30) ──
        "new_management": {
            "name": _("New Management"),
            "hint": _("Get a turned queen pregnant"),
        },
        "sugar_baby": {
            "name": _("Sugar Baby"),
            "hint": _("Receive her weekly allowance"),
        },
    }

    # ── Categories for viewer tabs ────────────────────────────
    ACHIEVEMENT_CATEGORIES = [
        (_("Campus"), [
            "not_santa_claus", "moonlight_nude", "girls_night", "group_chat",
            "game_night", "jurassic_help", "hot_date", "perfect_fit",
            "fashion_stylist", "fitting_fun", "double_trouble", "hidden_menu",
            "restroom_break", "soap_time", "knock_knock", "gf_at_the_door",
            "max_fit", "neeeerd", "nerds_talk", "fight_fight_fight",
            "party_for_three", "cups_and_hangout", "party_must_go_on",
            "secret_party", "secret_admirer", "homewrecker",
            "second_chances", "she_came_to_me", "forgive_and_forget",
            "trust_rebuilt", "against_all_odds", "perfect_gift",
        ]),
        (_("Intimate"), [
            "shower_masturbation", "room_masturbation", "she_wants_it",
            "just_the_tip", "red_handed", "no_choice", "persistence_pays",
            "oops_it_broke", "hidden_cream", "first_kiss", "backdoor_virgin",
            "wrong_order", "it_doesnt_count", "acquired_taste", "until_the_end",
            "iron_will", "sugar_daddy", "shes_my_favorite", "the_3_way",
            "helping_hand", "worst_first_kiss", "edge_lord", "speedrun",
            "change_of_heart", "stage_fright", "directors_cut", "hold_steady",
            "playing_both_sides", "great_good_morning",
            "first_child", "two_cribs", "full_house",
            "baby_fever", "baby_boom", "plan_b", "full_term",
            "kiss_the_throne", "best_foot_forward",
        ]),
        (_("Dark Path"), [
            "hardcore_player", "blackmail", "unwanted_gift", "say_cheese",
            "broken_will", "broken_by_accident", "double_betrayal", "expensive_pie", "reverse_card",
            "wingman", "cuckold_show", "boundary_broken", "viral_video",
            "full_access", "ask_permission", "ugly_bastard", "femdom_cuckold",
            "female_rivalry", "stealth_master", "identity_crisis",
            "bad_influence", "heartbreaker", "noisy_bet", "not_the_father",
            "behind_the_camera", "girl_behind_camera", "ntr_listening",
            "the_big_lie", "eyes_wide_open",
            "not_supposed_to_be_possible", "immaculate_conception", "sugar_pills",
            "close_call", "finders_keepers", "till_death", "study_session",
        ]),
        (_("Her Story"), [
            "what_she_hides", "won_her_heart", "under_your_thumb",
            "not_for_sale", "lawyers_on_retainer", "beg_for_it", "the_queen_falls",
            "new_management", "sugar_baby",
        ]),
    ]

    def unlock_achievement(key):
        """Unlock an achievement. Stored in persistent (shared across saves)."""
        if key not in ACHIEVEMENTS:
            return
        if persistent.achievements is None:
            persistent.achievements = {}
        if key in persistent.achievements:
            return
        persistent.achievements[key] = True
        _ach = ACHIEVEMENTS[key]
        try:
            renpy.music.play("audio/Information.mp3", channel="notify_sfx", loop=False)
            renpy.show_screen("achievement_banner", _tl(_ach["name"]))
        except Exception:
            pass

    def is_achievement_unlocked(key):
        """Check if an achievement is unlocked."""
        if persistent.achievements is None:
            return False
        return key in persistent.achievements

    def achievement_progress():
        """Returns (unlocked_count, total_count)."""
        if persistent.achievements is None:
            return (0, len(ACHIEVEMENTS))
        return (sum(1 for k in ACHIEVEMENTS if k in persistent.achievements), len(ACHIEVEMENTS))

    def _ach_category_progress(keys):
        """Returns (unlocked, total) for a list of achievement keys."""
        if persistent.achievements is None:
            return (0, len(keys))
        return (sum(1 for k in keys if k in persistent.achievements), len(keys))

    def _check_hardcore_traits():
        """Check if all enabled girls have negative traits + boyfriend. A trait or a partner she can never have
        (her canon, her girl type: Shion is married and always experienced) is not asked of her."""
        _neg = ("hate_cum", "camera_hater", "public_shy", "cute_sex", "virgin", "loyal")
        # girls_reachable: a girl whose optional route is off (the stepmom) is not in this run and is never asked
        for g in girls_reachable():
            if not getattr(g, "enabled", True):
                continue
            for t in _neg:
                if not trait_possible_for(g, t):
                    continue
                if not (hasattr(g, "has_trait") and g.has_trait(t)):
                    return False
            _can_partner = trait_possible_for(g, "has_boyfriend") or trait_possible_for(g, "has_girlfriend")
            if _can_partner and getattr(g, "npc_partner_id", None) is None:
                return False
        return True

    def clear_all_achievements():
        persistent.achievements = {}

# ── Achievement notification banner ─────────────────────────

transform achievement_banner_slide:
    xoffset 500
    ease 0.4 xoffset 0
    pause 3.0
    ease 0.3 xoffset 500

screen achievement_banner(ach_name):
    zorder 301

    frame at achievement_banner_slide:
        xalign 1.0
        ypos 140
        right_margin 24
        background _pk_pill("#101c30", 0.96)
        padding (14, 12, 28, 12)

        hbox:
            spacing 14

            fixed:
                xysize (46, 46)
                yalign 0.5
                add _pk_tint(_PK_DISC, ROD_ACCENT_WARM) xysize (46, 46)
                add _pk_icon("star", MENU_INK) zoom 1.1 align (0.5, 0.5)

            vbox:
                yalign 0.5
                spacing 2
                text _("Achievement Unlocked"):
                    style "phone_text"
                    size 16
                    bold True
                    color ROD_ACCENT_WARM
                text ach_name:
                    style "phone_text"
                    size 22
                    bold True
                    color "#e2e8f0"

    timer 3.7 action Hide("achievement_banner")

# ── Achievement viewer (main menu and game menu) ─────────────

init python:
    def achievements_view(tab):
        """What the achievements screen shows for category `tab`: overall progress, the category tabs
        [(index, caption)] and the cards of that category."""
        _unlocked, _total = achievement_progress()
        _tabs = []
        for _i, (_cat, _keys) in enumerate(ACHIEVEMENT_CATEGORIES):
            _u, _t = _ach_category_progress(_keys)
            _tabs.append((_i, "%s  %d/%d" % (_tl(_cat), _u, _t)))
        _cards = []
        for _k in ACHIEVEMENT_CATEGORIES[tab][1]:
            _a = ACHIEVEMENTS.get(_k, {})
            # "steps": the how-to bullets of its "Get more details" dialog (ACHIEVEMENT_STEPS, achievement_steps.rpy)
            _cards.append({"key": _k, "name": _tl(_a.get("name", _k)), "hint": _tl(_a.get("hint", "")),
                           "unlocked": is_achievement_unlocked(_k),
                           "steps": [_tl(_s) for _s in ACHIEVEMENT_STEPS.get(_k, ())]})
        return {"unlocked": _unlocked, "total": _total, "tabs": _tabs, "cards": _cards}

default _ach_tab = 0

screen achievements_viewer():

    tag menu

    use navigation

    $ _av = achievements_view(_ach_tab)

    use menu_panel():

        vbox:
            spacing 18

            use menu_header(_("Achievements")):
                text "%d / %d" % (_av["unlocked"], _av["total"]) style "ach_count"
                bar value StaticValue(_av["unlocked"], max(1, _av["total"])) style "menu_progress" xsize 280 yalign 0.5

            hbox:
                spacing 8
                for _i, _caption in _av["tabs"]:
                    textbutton _caption style "menu_option_button" action SetVariable("_ach_tab", _i)

            vpgrid:
                style_prefix "menu"                     # its scrollbar = menu_vscrollbar
                cols 3
                spacing 14
                yfill True
                mousewheel True
                draggable True
                scrollbars "vertical"

                for _ac in _av["cards"]:
                    use achievement_card(_ac)

screen achievement_card(card):
    frame:
        style ("ach_card_on" if card["unlocked"] else "ach_card")

        hbox:
            spacing 16
            yalign 0.5

            fixed:
                xysize (52, 52)
                yalign 0.5
                if card["unlocked"]:
                    add _pk_tint(_PK_DISC, ROD_ACCENT_WARM) xysize (52, 52)
                    add _pk_icon("star", MENU_INK) zoom 1.25 align (0.5, 0.5)
                else:
                    add _pk_tint(_PK_DISC, "#ffffff", 0.07) xysize (52, 52)
                    add _pk_tint(_PK_LOCK, "#5a6f86") align (0.5, 0.5)

            vbox:
                yalign 0.5
                spacing 3
                text card["name"] style ("ach_name_on" if card["unlocked"] else "ach_name")
                text card["hint"] style "ach_hint"
                if card["steps"]:
                    textbutton _("Get more details") style "ach_details_button" action Show("achievement_details", card=card)

# The how-to of one achievement: its name, its hint, the steps (ACHIEVEMENT_STEPS), a Close
screen achievement_details(card):

    modal True
    zorder 999

    add "#000000b8"

    use menu_dialog():
        text card["name"] style "menu_dialog_title"
        text (_("Unlocked") if card["unlocked"] else card["hint"]) style "menu_dialog_note" xalign 0.5 color (ROD_ACCENT_WARM if card["unlocked"] else "#8093a8")

        vbox:
            spacing 12
            for _st in card["steps"]:
                hbox:
                    spacing 14
                    # a tinted disc: the subset Work Sans has no bullet glyph
                    add _pk_tint(_PK_DISC, ROD_ACCENT_WARM) xysize (10, 10) yoffset 9
                    text _st style "ach_step"

        textbutton _("Close") style "menu_primary_button" xalign 0.5 action Hide("achievement_details")

    key "game_menu" action Hide("achievement_details")

init 1:
    style ach_count is text:
        font "fonts/WorkSans-SemiBold.ttf"
        size 26
        color ROD_TEXT_DIM
        yalign 0.5

    style ach_card is frame:
        xsize (MENU_INNER_W - 2 * 14 - 16) // 3
        ysize 128
        padding (18, 0, 18, 0)
        background _pk_pill("#ffffff", 0.045)

    style ach_card_on is ach_card:
        background _pk_pill(ROD_ACCENT_WARM, 0.1)

    style ach_name is text:
        font "fonts/WorkSans-SemiBold.ttf"
        size 19
        color ROD_TEXT

    style ach_name_on is ach_name:
        color "#fde68a"

    style ach_hint is text:
        font "fonts/WorkSans-Medium.ttf"
        size 15
        color "#8093a8"

    # "Get more details" under the hint: small, accent, no frame
    style ach_details_button is button:
        padding (0, 4, 0, 0)
        background None
    style ach_details_button_text is text:
        font "fonts/WorkSans-SemiBold.ttf"
        size 15
        color ROD_ACCENT_WARM
        hover_color "#fde68a"
        underline True

    # one how-to step of the details dialog
    style ach_step is text:
        font "fonts/WorkSans-Medium.ttf"
        size 21
        color ROD_TEXT
        xmaximum 760
