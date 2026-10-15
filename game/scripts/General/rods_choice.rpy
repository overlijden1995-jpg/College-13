# ============================================================
# ROD'S CHOICE — Achievement-driven game setup templates
# ============================================================

init python:

    ROD_TEMPLATES = [
        # ── 1. NTR Explorer ──────────────────────────────────
        ("UnusualAlias", {
            "girls": {
                "gwen": {
                    "traits": ["cheater", "cum_slut", "camera_lover", "has_boyfriend"],
                    "npc": {"disposition": "ntr", "sub": ["voyeur"], "bl": 2},
                },
                "rogue": {
                    "traits": ["cheater", "hardcore_sex", "exhibitionist", "has_boyfriend"],
                    "npc": {"disposition": "ntr", "sub": ["camera_lover"], "bl": 3},
                },
                "ntw": {
                    "traits": ["cheater", "public_fetish", "has_boyfriend"],
                    "npc": {"disposition": "ntr", "sub": [], "bl": 1},
                },
            },
            "corruption": True,
            "hardcore": False,
            "sexuality_locked": False,
            "player_trait": "charming",
            "attractiveness": 50,
            "targets": [
                "cuckold_show", "ask_permission", "boundary_broken",
                "full_access", "viral_video", "wingman",
                "double_betrayal", "blackmail", "behind_the_camera",
            ],
        }),

        # ── 2. Hardcore Challenge ─────────────────────────────
        ("CavemanJohnson", {
            "girls": {
                "gwen": {
                    "traits": ["hate_cum", "camera_hater", "public_shy", "cute_sex", "loyal", "virgin", "has_boyfriend"],
                    "npc": {"disposition": "proud", "sub": [], "bl": 0},
                },
                "rogue": {
                    "traits": ["hate_cum", "camera_hater", "public_shy", "cute_sex", "loyal", "virgin", "has_boyfriend"],
                    "npc": {"disposition": "proud", "sub": [], "bl": 0},
                },
                "ntw": {
                    "traits": ["camera_hater", "public_shy", "cute_sex", "loyal", "virgin", "has_girlfriend"],
                    "npc": {"disposition": "proud", "sub": [], "bl": 0},
                },
                # hardcore_player asks EVERY girl for the negatives she can have (_check_hardcore_traits): the
                # girls added after this seed was written have to be here too, or the seed can't reach its target
                "tenny": {
                    "traits": ["hate_cum", "camera_hater", "public_shy", "cute_sex", "loyal", "virgin", "has_boyfriend"],
                    "npc": {"disposition": "proud", "sub": [], "bl": 0},
                },
                # married + experienced canon: no partner, no virgin, no Gentle (blocked); the rest she can have
                "shion": {
                    "traits": ["hate_cum", "camera_hater", "public_shy", "loyal"],
                },
            },
            "corruption": True,
            "hardcore": False,
            "sexuality_locked": False,
            "player_trait": "athlete",
            "attractiveness": 0,
            "targets": [
                "hardcore_player", "say_cheese", "unwanted_gift",
                "iron_will", "fight_fight_fight",
                "stage_fright",
            ],
        }),

        # ── 3. Cheat Path ────────────────────────────────────
        ("NateColds", {
            "girls": {
                "gwen": {
                    "traits": ["loyal", "cum_slut", "camera_lover", "has_boyfriend"],
                    "npc": {"disposition": "proud", "sub": [], "bl": 0},
                },
                "rogue": {
                    "traits": ["loyal", "hardcore_sex", "anal_lover", "has_boyfriend"],
                    "npc": {"disposition": "proud", "sub": [], "bl": 0},
                },
                "ntw": {
                    "traits": ["loyal", "public_shy", "cute_sex", "has_boyfriend"],
                    "npc": {"disposition": "proud", "sub": [], "bl": 0},
                },
            },
            "corruption": True,
            "hardcore": False,
            "sexuality_locked": False,
            "player_trait": "charming",
            "attractiveness": 50,
            "targets": [
                "broken_will", "broken_by_accident", "it_doesnt_count", "double_betrayal",
                "just_the_tip", "she_wants_it",
                "homewrecker",
            ],
        }),

        # ── 4. Dark Domination ────────────────────────────────
        ("Dirty Dix", {
            "girls": {
                "gwen": {
                    "traits": ["cum_slut", "hardcore_sex", "exhibitionist", "public_fetish"],
                },
                "rogue": {
                    "traits": ["hate_cum", "camera_hater", "anal_lover"],
                },
                "ntw": {
                    "traits": ["hardcore_sex", "experienced", "has_boyfriend"],
                    "npc": {"disposition": "neutral", "sub": [], "bl": 0},
                },
            },
            "corruption": True,
            "hardcore": False,
            "sexuality_locked": False,
            "player_trait": "athlete",
            "attractiveness": 50,
            "targets": [
                "no_choice", "iron_will", "until_the_end",
                "unwanted_gift", "red_handed", "acquired_taste",
                "edge_lord",
            ],
        }),

        # ── 5. Camera & Recording ─────────────────────────────
        ("Jman7753", {
            "girls": {
                "gwen": {
                    "traits": ["camera_hater", "cum_slut", "has_boyfriend"],
                    "npc": {"disposition": "neutral", "sub": [], "bl": 0},
                },
                "rogue": {
                    "traits": ["camera_lover", "exhibitionist", "cheater", "has_boyfriend"],
                    "npc": {"disposition": "ntr", "sub": ["voyeur"], "bl": 2},
                },
                "ntw": {
                    "traits": ["camera_hater", "poor", "has_boyfriend"],
                    "npc": {"disposition": "neutral", "sub": [], "bl": 0},
                },
            },
            "corruption": True,
            "hardcore": False,
            "sexuality_locked": False,
            "player_trait": "investor",
            "attractiveness": 50,
            "targets": [
                "say_cheese", "blackmail", "expensive_pie", "viral_video",
                "secret_admirer", "directors_cut",
            ],
        }),

        # ── 6. Financial Path ─────────────────────────────────
        ("Old Mariner", {
            "girls": {
                "gwen": {
                    "traits": ["poor", "camera_hater", "public_shy", "has_boyfriend"],
                    "npc": {"disposition": "neutral", "sub": [], "bl": 0},
                },
                "rogue": {
                    "traits": ["poor", "loyal", "cute_sex", "has_boyfriend"],
                    "npc": {"disposition": "neutral", "sub": [], "bl": 0},
                },
                "ntw": {
                    "traits": ["poor", "hardcore_sex", "has_boyfriend"],
                    "npc": {"disposition": "neutral", "sub": [], "bl": 0},
                },
            },
            "corruption": True,
            "hardcore": False,
            "sexuality_locked": False,
            "player_trait": "investor",
            "attractiveness": 0,
            "targets": [
                "sugar_daddy", "reverse_card", "expensive_pie",
            ],
        }),

        # ── 7. Lesbian Conquest ───────────────────────────────
        ("D D", {
            "girls": {
                "gwen": {
                    "traits": ["cheater", "hardcore_sex", "camera_lover", "has_boyfriend"],
                    "npc": {"disposition": "neutral", "sub": [], "bl": 0},
                },
                "rogue": {
                    "traits": ["bisexual", "exhibitionist", "public_fetish"],
                },
                "ntw": {
                    "traits": ["virgin", "has_girlfriend"],
                    "npc": {"disposition": "ntr", "sub": [], "bl": 1},
                },
            },
            "corruption": True,
            "hardcore": False,
            "sexuality_locked": False,
            "player_trait": "athlete",
            "attractiveness": 50,
            "targets": [
                "first_kiss", "broken_will", "broken_by_accident", "double_betrayal",
                "identity_crisis", "playing_both_sides",
            ],
        }),

        # ── 8. Virgin Romance ─────────────────────────────────
        ("Michael", {
            "girls": {
                "gwen": {
                    "traits": ["virgin", "loyal", "cute_sex", "anal_hater"],
                },
                "rogue": {
                    "traits": ["virgin", "public_shy", "camera_lover", "has_boyfriend"],
                    "npc": {"disposition": "proud", "sub": [], "bl": 0},
                },
                "ntw": {
                    "traits": ["naive"],
                },
            },
            "corruption": True,
            "hardcore": False,
            "sexuality_locked": False,
            "player_trait": "charming",
            "attractiveness": 100,
            "targets": [
                "backdoor_virgin", "wrong_order", "gf_at_the_door",
                "she_wants_it", "just_the_tip",
                "oops_it_broke", "hidden_cream",
                "speedrun",
            ],
        }),

        # ── 9. Social Explorer ────────────────────────────────
        ("Youwa", {
            "girls": {
                "gwen": {
                    "traits": ["cheater", "cum_slut", "camera_lover", "polyamorous", "has_boyfriend"],
                    "npc": {"disposition": "neutral", "sub": [], "bl": 0},
                },
                "rogue": {
                    "traits": ["camera_hater", "anal_lover", "experienced", "has_boyfriend"],
                    "npc": {"disposition": "neutral", "sub": [], "bl": 0},
                },
                "ntw": {
                    "traits": ["has_girlfriend", "hardcore_sex", "exhibitionist"],
                },
                "tenny": {
                    "traits": ["nerd", "virgin", "cute_sex", "lightweight", "poor"],
                },
            },
            "corruption": True,
            "hardcore": False,
            "sexuality_locked": False,
            "player_trait": "charming",
            "attractiveness": 50,
            "targets": [
                "girls_night", "game_night", "not_santa_claus",
                "moonlight_nude", "soap_time", "hot_date",
                "neeeerd", "max_fit", "double_trouble",
                "hidden_menu", "restroom_break", "perfect_fit",
                "fashion_stylist", "fitting_fun", "knock_knock",
                "group_chat", "jurassic_help", "bad_influence",
                "gf_at_the_door", "double_betrayal", "homewrecker",
                "say_cheese", "no_choice", "hidden_cream",
                "speedrun", "identity_crisis", "first_kiss",
                "playing_both_sides", "sugar_daddy", "acquired_taste",
                "party_for_three",
            ],
        }),

        # ── 10. Balanced Mix ──────────────────────────────────
        ("Keggo", {
            "girls": {
                "gwen": {
                    "traits": ["cheater", "cum_slut", "camera_lover", "has_boyfriend"],
                    "npc": {"disposition": "neutral", "sub": [], "bl": 0},
                },
                "rogue": {
                    "traits": ["anal_lover", "public_fetish", "experienced"],
                },
                "ntw": {
                    "traits": ["virgin", "loyal", "cute_sex"],
                },
            },
            "corruption": True,
            "hardcore": False,
            "sexuality_locked": False,
            "player_trait": "none",
            "attractiveness": 50,
            "targets": [
                "persistence_pays", "shower_masturbation", "room_masturbation",
                "oops_it_broke", "hidden_cream", "she_wants_it",
                "red_handed", "soap_time", "knock_knock",
            ],
        }),

        # ── 11. Condom Saboteur ───────────────────────────────
        ("wing", {
            "girls": {
                "gwen": {
                    "traits": ["hate_cum", "public_shy", "loyal"],
                },
                "rogue": {
                    "traits": ["hate_cum", "camera_hater", "cute_sex"],
                },
                "ntw": {
                    "traits": ["hate_cum", "anal_hater", "virgin"],
                },
            },
            "corruption": True,
            "hardcore": False,
            "sexuality_locked": False,
            "player_trait": "charming",
            "attractiveness": 50,
            "targets": [
                "oops_it_broke", "hidden_cream", "unwanted_gift",
                "stealth_master", "change_of_heart",
            ],
        }),

        # ── 12. Athlete's Edge ────────────────────────────────
        ("Dakon", {
            "girls": {
                "gwen": {
                    "traits": ["cum_slut", "hardcore_sex", "exhibitionist"],
                },
                "rogue": {
                    "traits": ["public_fetish", "camera_lover", "experienced"],
                },
                "ntw": {
                    "traits": ["cum_slut", "voyeur"],
                },
            },
            "corruption": True,
            "hardcore": False,
            "sexuality_locked": False,
            "player_trait": "athlete",
            "attractiveness": 50,
            "targets": [
                "iron_will", "fight_fight_fight", "max_fit", "no_choice",
                "hold_steady",
            ],
        }),

        # ── 13. Anal Explorer ─────────────────────────────────
        ("Lordathand", {
            "girls": {
                "gwen": {
                    "traits": ["virgin", "loyal", "cute_sex"],
                },
                "rogue": {
                    "traits": ["anal_lover", "loyal", "has_boyfriend"],
                    "npc": {"disposition": "proud", "sub": [], "bl": 0},
                },
                "ntw": {
                    "traits": ["experienced", "anal_lover", "hardcore_sex"],
                },
            },
            "corruption": True,
            "hardcore": False,
            "sexuality_locked": False,
            "player_trait": "charming",
            "attractiveness": 50,
            "targets": [
                "backdoor_virgin", "wrong_order",
                "it_doesnt_count", "acquired_taste",
                "worst_first_kiss",
            ],
        }),

        # ── 14. Caught in the Act ─────────────────────────────
        ("beh", {
            "girls": {
                "gwen": {
                    "traits": ["exhibitionist", "cum_slut", "camera_lover"],
                },
                "rogue": {
                    "traits": ["voyeur", "public_fetish", "experienced", "has_boyfriend"],
                    "npc": {"disposition": "neutral", "sub": [], "bl": 0},
                },
                "ntw": {
                    "traits": ["exhibitionist", "hardcore_sex", "cheater"],
                },
            },
            "corruption": True,
            "hardcore": False,
            "sexuality_locked": False,
            "player_trait": "charming",
            "attractiveness": 100,
            "targets": [
                "knock_knock", "gf_at_the_door",
                "shower_masturbation", "room_masturbation",
                "red_handed", "persistence_pays",
            ],
        }),

        # ── 15. Ugly Bastard ──────────────────────────────────
        ("A B", {
            "girls": {
                "gwen": {
                    "traits": ["cheater", "cum_slut", "hardcore_sex", "has_boyfriend"],
                    "npc": {"disposition": "ntr", "sub": ["voyeur"], "bl": 3},
                },
                "rogue": {
                    "traits": ["cheater", "exhibitionist", "camera_lover", "has_boyfriend"],
                    "npc": {"disposition": "ntr", "sub": [], "bl": 2},
                },
                "ntw": {
                    "traits": ["cheater", "hardcore_sex", "public_fetish", "has_boyfriend"],
                    "npc": {"disposition": "ntr", "sub": ["camera_lover"], "bl": 2},
                },
            },
            "corruption": True,
            "hardcore": False,
            "sexuality_locked": False,
            "player_trait": "none",
            "attractiveness": 0,
            "targets": [
                "ugly_bastard", "cuckold_show", "boundary_broken",
                "full_access", "viral_video",
            ],
        }),

        # ── 16. Party Night ───────────────────────────────────
        ("Michale", {
            "girls": {
                "gwen": {
                    "traits": ["exhibitionist", "cheater", "cum_slut", "has_boyfriend"],
                    "npc": {"disposition": "neutral", "sub": [], "bl": 0},
                },
                "rogue": {
                    "traits": ["public_fetish", "experienced", "camera_lover"],
                },
                "ntw": {
                    "traits": ["voyeur", "hardcore_sex"],
                },
            },
            "corruption": True,
            "hardcore": False,
            "sexuality_locked": False,
            "player_trait": "charming",
            "attractiveness": 50,
            "targets": [
                "party_for_three", "cups_and_hangout",
                "party_must_go_on", "secret_party",
            ],
        }),

        # ── 17. Triple Threat ────────────────────────────────
        ("Superninja", {
            "girls": {
                "gwen": {
                    "traits": ["exhibitionist", "voyeur", "cum_slut"],
                },
                "rogue": {
                    "traits": ["exhibitionist", "experienced", "camera_lover"],
                },
                "ntw": {
                    "traits": ["voyeur", "hardcore_sex", "exhibitionist"],
                },
            },
            "corruption": True,
            "hardcore": False,
            "sexuality_locked": False,
            "player_trait": "charming",
            "attractiveness": 50,
            "targets": [
                "the_3_way", "shes_my_favorite", "double_trouble",
                "helping_hand", "female_rivalry",
            ],
        }),

        # ── 18. NPC After Dark ───────────────────────────────
        ("Zetsu", {
            "girls": {
                "gwen": {
                    "traits": ["cheater", "cum_slut", "has_boyfriend"],
                    "npc": {"disposition": "neutral", "sub": [], "bl": 0},
                },
                "rogue": {
                    "traits": ["cheater", "public_fetish", "has_boyfriend"],
                    "npc": {"disposition": "neutral", "sub": [], "bl": 0},
                },
                "ntw": {
                    "traits": ["cheater", "has_girlfriend"],
                    "npc": {"disposition": "neutral", "sub": [], "bl": 0},
                },
            },
            "corruption": True,
            "hardcore": False,
            "sexuality_locked": False,
            "player_trait": "charming",
            "attractiveness": 50,
            "targets": [
                "cups_and_hangout", "party_must_go_on",
                "secret_party", "double_betrayal",
            ],
        }),

        # ── 19. Ultimate Party ───────────────────────────────
        ("Moyboy", {
            "girls": {
                "gwen": {
                    "traits": ["exhibitionist", "cum_slut", "has_boyfriend"],
                    "npc": {"disposition": "neutral", "sub": [], "bl": 0},
                },
                "rogue": {
                    "traits": ["voyeur", "experienced", "exhibitionist"],
                },
                "ntw": {
                    "traits": ["exhibitionist", "hardcore_sex"],
                },
            },
            "corruption": True,
            "hardcore": False,
            "sexuality_locked": False,
            "player_trait": "fast_learner",
            "attractiveness": 50,
            "targets": [
                "party_for_three", "the_3_way",
                "shes_my_favorite", "cups_and_hangout",
            ],
        }),

        # ── 20. Femdom Cuckold ────────────────────────────────
        ("Pryor", {
            "girls": {
                "gwen": {
                    "traits": ["exhibitionist", "cheater", "cum_slut", "has_boyfriend"],
                    "npc": {"disposition": "ntr", "sub": ["voyeur"], "bl": 3},
                },
                "rogue": {
                    "traits": ["exhibitionist", "cheater", "hardcore_sex", "has_boyfriend"],
                    "npc": {"disposition": "ntr", "sub": ["camera_lover"], "bl": 2},
                },
                "ntw": {
                    "traits": ["exhibitionist", "cheater", "public_fetish", "has_boyfriend"],
                    "npc": {"disposition": "ntr", "sub": [], "bl": 2},
                },
            },
            "corruption": True,
            "hardcore": False,
            "sexuality_locked": False,
            "player_trait": "charming",
            "attractiveness": 50,
            "targets": [
                "femdom_cuckold", "cuckold_show", "ask_permission",
                "boundary_broken", "double_betrayal", "behind_the_camera",
            ],
        }),

        # ── 21. Family Man ────────────────────────────────────
        # Needs the pregnancy system. Four single, fertile girls (one of them wants it): children with one, two, all of them.
        # Investor: child support is $250 a week per child.
        ("Alinmus", {
            "girls": {
                "gwen": {
                    "traits": ["pregnancy_fetish", "cum_slut", "hardcore_sex"],
                },
                "rogue": {
                    "traits": ["breedable", "cum_slut", "experienced"],
                },
                "ntw": {
                    "traits": ["breedable", "cute_sex"],
                },
                "tenny": {
                    "traits": ["nerd", "breedable", "cute_sex"],
                },
            },
            "corruption": True,
            "hardcore": False,
            "sexuality_locked": False,
            "player_trait": "investor",
            "attractiveness": 100,
            "needs_pregnancy": True,
            "targets": [
                "first_child", "two_cribs", "full_house",
                "baby_fever", "baby_boom", "plan_b", "sugar_pills", "full_term",
            ],
        }),

        # ── 22. Not the Father ────────────────────────────────
        # Needs the pregnancy system. Three cheating girlfriends: a plain boyfriend who can be told the child is his
        # (discovery, choice 4) or forgive her, an NTR boyfriend with no limits ("I'll raise the kid") and a proud
        # one who leaves. Plus a lesbian whose girlfriend can never be the father (2026-09-19).
        ("Totempol13", {
            "girls": {
                "gwen": {
                    "traits": ["cheater", "cum_slut", "breedable", "has_boyfriend"],
                    "npc": {"disposition": "neutral", "sub": [], "bl": 0},
                },
                "rogue": {
                    "traits": ["cheater", "hardcore_sex", "breedable", "has_boyfriend"],
                    "npc": {"disposition": "ntr", "sub": ["voyeur"], "bl": 4},
                },
                "ntw": {
                    "traits": ["cheater", "public_fetish", "has_boyfriend"],
                    "npc": {"disposition": "proud", "sub": [], "bl": 0},
                },
                "tenny": {
                    "traits": ["nerd", "lesbian", "breedable", "has_girlfriend"],
                    "npc": {"disposition": "neutral", "sub": [], "bl": 0},
                },
            },
            "corruption": True,
            "hardcore": False,
            "sexuality_locked": False,
            "player_trait": "charming",
            "attractiveness": 50,
            "needs_pregnancy": True,
            "targets": [
                "not_the_father", "first_child", "two_cribs",
                "the_big_lie", "eyes_wide_open", "against_all_odds", "close_call",
                "not_supposed_to_be_possible", "immaculate_conception",
            ],
        }),
        # ── 23. Heartbreak & Healing ──────────────────────────
        # Romance cycle: date multiple girls, break hearts, reconcile.
        # Covers the relationship achievements no other seed targets.
        ("DD", {
            "girls": {
                "gwen": {
                    "traits": ["cheater", "cum_slut", "camera_lover", "has_boyfriend"],
                    "npc": {"disposition": "neutral", "sub": [], "bl": 0},
                },
                "rogue": {
                    "traits": ["loyal", "cute_sex", "experienced"],
                },
                "ntw": {
                    "traits": ["public_shy", "cute_sex", "has_boyfriend"],
                    "npc": {"disposition": "neutral", "sub": [], "bl": 0},
                },
            },
            "corruption": True,
            "hardcore": False,
            "sexuality_locked": False,
            "player_trait": "charming",
            "attractiveness": 100,
            "targets": [
                "great_good_morning", "second_chances", "she_came_to_me",
                "forgive_and_forget", "trust_rebuilt", "heartbreaker",
                "perfect_gift", "finders_keepers",
            ],
        }),

        # ── 24. Silent Witness ───────────────────────────────────
        # NTR bet event + girl recording during threesome. The partner is right there.
        ("Kri", {
            "girls": {
                "gwen": {
                    "traits": ["cheater", "exhibitionist", "cum_slut", "has_boyfriend"],
                    "npc": {"disposition": "ntr", "sub": ["voyeur"], "bl": 3},
                },
                "rogue": {
                    "traits": ["voyeur", "camera_lover", "exhibitionist", "experienced"],
                },
                "ntw": {
                    "traits": ["cheater", "hardcore_sex", "public_fetish", "has_boyfriend"],
                    "npc": {"disposition": "ntr", "sub": ["camera_lover"], "bl": 2},
                },
            },
            "corruption": True,
            "hardcore": False,
            "sexuality_locked": False,
            "player_trait": "charming",
            "attractiveness": 50,
            "targets": [
                "noisy_bet", "ntr_listening", "girl_behind_camera",
                "behind_the_camera", "cuckold_show", "boundary_broken",
            ],
        }),

        # ── 25. Family Secrets ───────────────────────────────────
        # Needs the stepmother route. Her whole story: either lane to her last step (earned or leveraged: the player
        # picks the lane when both pass), the Hashimoto secret, her money and her lawyers, the rimjob, the ring and
        # the night she "tutors" him. Fast Learner keeps his grades up (her step 1 wants a B). Campus girls single.
        ("Zerafu", {
            "girls": {
                "shion": {
                    "traits": ["hardcore_sex", "breedable"],
                },
                "gwen": {
                    "traits": ["cute_sex", "camera_lover"],
                },
                "rogue": {
                    "traits": ["experienced", "anal_lover"],
                },
                "ntw": {
                    "traits": ["public_shy", "virgin"],
                },
            },
            "corruption": True,
            "hardcore": False,
            "sexuality_locked": False,
            "player_trait": "fast_learner",
            "attractiveness": 50,
            "needs_stepmom_route": True,
            "targets": [
                "won_her_heart", "under_your_thumb", "what_she_hides",
                "till_death", "study_session", "kiss_the_throne",
                "not_for_sale", "lawyers_on_retainer",
            ],
        }),

        # ── 26. Crown Breaker ────────────────────────────────────
        # Two queens on campus, none of them born to it (no story step holds their crown): Rogue to obey until she
        # begs, Gwen (rich) to defy until she breaks, turns Submissive and pays his way. Tenny brings the nerd talk
        # and the footjob; NTW a Submissive from day one. With the pregnancy system on, the turned queen can carry
        # his child too ("pregnancy_targets").
        ("Ray Trevy", {
            "girls": {
                "gwen": {
                    "traits": ["femdom", "rich", "breedable"],
                },
                "rogue": {
                    "traits": ["femdom", "hardcore_sex", "experienced"],
                },
                "ntw": {
                    "traits": ["submissive", "cute_sex"],
                },
                "tenny": {
                    "traits": ["nerd", "public_shy"],
                },
            },
            "corruption": True,
            "hardcore": False,
            "sexuality_locked": False,
            "player_trait": "charming",
            "attractiveness": 50,
            "targets": [
                "the_queen_falls", "beg_for_it", "sugar_baby",
                "best_foot_forward", "nerds_talk",
            ],
            "pregnancy_targets": ["new_management"],
        }),
    ]


    def _rods_choice_pool():
        """Seeds in the draw. A seed built around a system the player turns on or off right before the pick
        (label _pregnancy_setup / _stepmom_setup, script.rpy) is only in it when he turned that system on
        ("needs_pregnancy" / "needs_stepmom_route"). Those systems are HIS choice, a seed never sets them."""
        _preg = store._pregnancy_mode != "off"
        _route = bool(getattr(store, "_stepmom_route", True))
        _pool = [(n, t) for n, t in ROD_TEMPLATES
                 if (_preg or not t.get("needs_pregnancy")) and (_route or not t.get("needs_stepmom_route"))]
        _in = set(n for n, t in _pool)
        _out = [n for n, t in ROD_TEMPLATES if n not in _in]
        print("[ROD'S CHOICE] pregnancy=%s stepmom_route=%s: %d of %d seeds in the draw%s" % (
            store._pregnancy_mode, _route, len(_pool), len(ROD_TEMPLATES),
            " (left out: %s)" % ", ".join(_out) if _out else ""))
        return _pool

    def _rods_choice_targets(tmpl):
        """The achievements a seed aims at in THIS setup: its "pregnancy_targets" count only with the pregnancy
        system on (the seed stays in the draw without it, for its other targets)."""
        _t = list(tmpl["targets"])
        if store._pregnancy_mode != "off":
            _t += tmpl.get("pregnancy_targets", [])
        return _t

    def _rods_choice_pick():
        pool = _rods_choice_pool()
        missing = [k for k in ACHIEVEMENTS if not is_achievement_unlocked(k)]
        if not missing:
            print("[ROD'S CHOICE] All achievements unlocked, random pick")
            return renpy.random.choice(pool)[0]

        missing_set = set(missing)
        scores = []
        for name, tmpl in pool:
            s = len(set(_rods_choice_targets(tmpl)) & missing_set)
            scores.append((name, s))
            print("[ROD'S CHOICE] %s: %d missing targets" % (name, s))

        max_score = max(s for _, s in scores)
        best = [n for n, s in scores if s == max_score]
        pick = renpy.random.choice(best)
        print("[ROD'S CHOICE] Best score %d, picked '%s' from %s" % (max_score, pick, best))
        return pick


    def _rods_choice_apply(template_name):
        tmpl = None
        for n, t in ROD_TEMPLATES:
            if n == template_name:
                tmpl = t
                break
        if tmpl is None:
            print("[ROD'S CHOICE] ERROR: template '%s' not found" % template_name)
            return

        for gid, cfg in tmpl["girls"].items():
            girl = GIRL_BY_ID.get(gid)
            if girl is None:
                print("[ROD'S CHOICE] WARNING: no girl with gid '%s'" % gid)
                continue

            _clear_girl_traits(girl)

            for trait in sorted(cfg["traits"], key=lambda t: 2 if t in ("experienced", "naive") else 0):
                girl.add_trait(trait)
                if trait == "has_boyfriend":
                    girl.set_npc_partner("npc_bf_%s" % gid)
                elif trait == "has_girlfriend":
                    girl.set_npc_partner_female("npc_gf_%s" % gid)
                elif trait == "naive":
                    _apply_naive(girl)
                elif trait == "experienced":
                    _apply_experienced(girl)

            # Pregnancy co-trait, same rule as the manual trait picker (script.rpy): the fetish craves creampies
            if girl.has_trait("pregnancy_fetish"):
                girl.remove_trait("hate_cum")
                if not girl.has_trait("cum_slut"):
                    girl.add_trait("cum_slut")

            # has_girlfriend forces lesbian (unless bisexual)
            if girl.has_npc_partner() and girl.get_flag("partner_is_female"):
                if not girl.has_trait("lesbian") and not girl.has_trait("bisexual"):
                    girl.add_trait("lesbian")

            # Lesbian co-traits: force hate_cum (pregnancy_fetish wins the conflict)
            if girl.has_trait("lesbian") and not girl.has_trait("pregnancy_fetish"):
                girl.remove_trait("cum_slut")
                if not girl.has_trait("hate_cum"):
                    girl.add_trait("hate_cum")

            # Virgin + partner: ensure bf_history is compatible
            if girl.has_trait("virgin") and girl.has_npc_partner():
                if girl.bf_max_tier >= 4:
                    girl.bf_max_tier = 3
                    for key in ("sex", "sex_raw", "creampie", "anal"):
                        if key in girl.bf_history:
                            girl.bf_history[key] = False

            # Set NPC partner config (stored on girl, used by rebuild_npc_partners)
            if "npc" in cfg:
                npc_cfg = cfg["npc"]
                npc_traits = set()
                disp = npc_cfg.get("disposition", "neutral")
                if disp != "neutral":
                    npc_traits.add(disp)
                for sub in npc_cfg.get("sub", []):
                    npc_traits.add(sub)
                girl._npc_partner_traits = npc_traits
                girl._ntr_active = (disp == "ntr")
                # The partner was already rolled at random when assigned: the template replaces that roll.
                # None = create_npc_partner() sets the limit at the rebuild (1 for a non-NTR partner).
                girl._ntr_boundary_level = npc_cfg.get("bl", 1) if disp == "ntr" else None
                print("[ROD'S CHOICE] %s partner: traits=%s ntr_active=%s bl=%s" % (girl.gid, sorted(npc_traits), girl._ntr_active, girl._ntr_boundary_level))

            print("[ROD'S CHOICE] %s traits: %s" % (girl.Name, girl.traits))

        # EVERY girl, in the seed or not: a seed never overrides a canon trait, and a girl the seed leaves out
        # still needs the history of her canon Experienced (the GIRLS_CONFIG loop only adds the trait)
        for _rc_girl in ALL_GIRLS:
            enforce_canon_traits(_rc_girl, "rods_choice", fresh=True)

        # Global settings
        store.corruption_enabled = tmpl["corruption"]
        store.sexuality_locked = tmpl.get("sexuality_locked", False)
        store.hardcore_relationship = tmpl["hardcore"]
        # The pregnancy system is the player's own choice, made before the pick: a seed never sets it
        if tmpl.get("needs_pregnancy") and store._pregnancy_mode == "off":
            print("[ROD'S CHOICE] WARNING: seed '%s' needs the pregnancy system and it is OFF (the pool should have left it out)" % template_name)
        if tmpl.get("needs_stepmom_route") and not getattr(store, "_stepmom_route", True):
            print("[ROD'S CHOICE] WARNING: seed '%s' needs the stepmother route and it is OFF (the pool should have left it out)" % template_name)

        # Player trait (same effects as script.rpy start label)
        _pt = tmpl["player_trait"]
        Player.player_trait = _pt
        if _pt == "athlete":
            Player.energy_max = 4
            Player.energy = 4
        elif _pt == "investor":
            Player.add_cash(400)
        elif _pt == "charming":
            for _g in ALL_GIRLS:
                _g.Love = min(1000, _g.Love + 50)
        elif _pt != "fast_learner":
            Player.player_trait = "none"

        Player.attractiveness = tmpl["attractiveness"]

        # Check hardcore achievement
        if _check_hardcore_traits():
            unlock_achievement("hardcore_player")

        print("[ROD'S CHOICE] Applied template '%s' (corruption=%s, sex_lock=%s, hardcore=%s, trait=%s, attr=%d, pregnancy=%s/%s)" % (
            template_name, tmpl["corruption"], tmpl.get("sexuality_locked", False), tmpl["hardcore"], _pt, tmpl["attractiveness"],
            store._pregnancy_mode, store._pregnancy_duration))

init 1 python:

    # Startup check of the seeds. An achievement added without a seed that can reach it is impossible for whoever
    # only plays Rod's Choice (the four child achievements were, until seeds 21 / 22): the last line lists them.
    def _rods_choice_validate():
        _bad = []
        _names = [_n for _n, _t in ROD_TEMPLATES]
        for _n in sorted(set(_x for _x in _names if _names.count(_x) > 1)):
            _bad.append("seed name '%s' used twice" % _n)
        _targeted = set()
        for _n, _t in ROD_TEMPLATES:
            for _k in list(_t["targets"]) + list(_t.get("pregnancy_targets", [])):
                _targeted.add(_k)
                if _k not in ACHIEVEMENTS:
                    _bad.append("%s: unknown achievement '%s'" % (_n, _k))
            for _gid in _t["girls"]:
                if _gid not in GIRL_BY_ID:
                    _bad.append("%s: unknown girl '%s'" % (_n, _gid))
            for _need in ("needs_pregnancy", "needs_stepmom_route"):
                if not isinstance(_t.get(_need, False), bool):
                    _bad.append("%s: %s must be True / False" % (_n, _need))
            if _t.get("pregnancy_targets") and _t.get("needs_pregnancy"):
                _bad.append("%s: pregnancy_targets is for a seed WITHOUT needs_pregnancy (put them in targets)" % _n)
            for _old_key in ("pregnancy_mode", "pregnancy_duration"):
                if _old_key in _t:
                    _bad.append("%s: '%s' is not a seed key anymore (the player chooses it before the pick)" % (_n, _old_key))
        for _p in _bad:
            print("[ROD'S CHOICE] INVALID seed: " + _p)
        _free = sorted(_k for _k in ACHIEVEMENTS if _k not in _targeted)
        print("[ROD'S CHOICE] %d seeds, %d need the pregnancy system and %d the stepmother route (drawn only when the player turns it on), %d achievement(s) no seed targets: %s" % (
            len(ROD_TEMPLATES), len([1 for _n, _t in ROD_TEMPLATES if _t.get("needs_pregnancy")]),
            len([1 for _n, _t in ROD_TEMPLATES if _t.get("needs_stepmom_route")]), len(_free), ", ".join(_free) or "none"))
        return _bad

    _rods_choice_validate()
