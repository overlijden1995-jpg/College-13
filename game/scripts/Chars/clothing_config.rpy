# ============================================================
# CLOTHING REGISTRY — Single source of truth for all clothing
# ============================================================
#
# Each item maps slot, supported states, and per-pose attributes.
# States: "full" = worn normally, "up" = pulled up/displaced,
#         "down" = pulled down, "side" = pulled to side
# Poses that are absent = item has no art for that pose (skip).
# Each state maps to a LIST of layeredimage attribute strings.
#
# To add a new clothing item:
#   1. Add entry here
#   2. Add art + attributes to the relevant layeredimage files
#   3. Done. No other code changes needed.
# ============================================================

init -998 python:

    CLOTHING_REGISTRY = {

        # ====================================================
        # GWEN
        # ====================================================
        "gwen": {

            # ---------- OVER ----------
            "long_shirt": {
                "slot": "over",
                "states": ["full"],
                "poses": {
                    "standing": {"full": ["over_long_shirt"]},
                    "handjob":  {"full": ["over_long_shirt"]},
                    "blowjob":  {"full": ["over_long_shirt"]},
                    "reverse_cowgirl":    {"full": ["torso_over_long_shirt"]},
                    "cowgirl":  {"full": ["torso_over_long_shirt"]},
                    "doggy":    {"full": ["torso_over_long_shirt"]},
                },
                "layers": {
                    "standing": {
                        "body": "Standing/Clothes/Over/Long Shirt/Gwen Arms 1 Long Shirt.png",
                    },
                    "handjob": {
                        "body": "Handjob/Clothes/Over/Long Shirt/HJ.png",
                    },
                    "blowjob": {
                        "body":   "Blowjob/Clothes/Over/Long Shirt/BJ Body.png",
                        "torso":  "Blowjob/Clothes/Over/Long Shirt/BJ Torso.png",
                        "arm":    "Blowjob/Clothes/Over/Long Shirt/BJ Arm.png",
                    },
                    "titjob": {
                        "arms_1": "Titjob/Clothes/Over/Long Shirt/TJ Arms 1.png",
                        "arms_2": "Titjob/Clothes/Over/Long Shirt/TJ Arms 2.png",
                        "arms_3": "Titjob/Clothes/Over/Long Shirt/TJ Arms 3.png",
                    },
                    "cowgirl": {
                        "arms_1":        "Cowgirl/Clothes/Over/Long Shirt/CG Arms 1.png",
                        "masturbation":  "Cowgirl/Clothes/Over/Long Shirt/CG Masturbation.png",
                    },
                    "reverse_cowgirl": {
                        "body":   "RCG/Clothes/Over/Long Shirt/DG Body.png",
                        "arms_1": "RCG/Clothes/Over/Long Shirt/DG Arms 1.png",
                        "arms_2": "RCG/Clothes/Over/Long Shirt/DG Arms 2.png",
                    },
                    "doggy": {
                        "arms": "Doggy/Clothes/Over/Long Shirt/Gwen Doggy Blue Shirt 2 .png",
                    },
                },
            },
            "towel": {
                "slot": "over",
                "states": ["full"],
                "poses": {
                    "standing": {"full": ["over_towel"]},
                },
            },

            # ---------- CHEST ----------
            "corset": {
                "slot": "chest",
                "states": ["full", "up"],
                "poses": {
                    "standing": {"full": ["chest_corset"],           "up": ["chest_corset_down"]},
                    "handjob":  {"full": ["chest_corset", "chest_base_on"], "up": ["chest_clothes_none", "chest_base_on"]},
                    "blowjob":  {"full": ["corset", "boobs_clothes_1"],        "up": ["torso_corset_none", "boobs_clothes_none"]},
                    "reverse_cowgirl":    {"full": ["torso_chest_corset"],     "up": ["torso_chest_corset"]},
                    "cowgirl":  {"full": [],                         "up": []},
                    "titjob":   {"full": ["corset_up_on", "chest_base_on"], "up": ["corset_up_on"]},
                    "doggy":    {"full": ["torso_chest_corset"],     "up": ["torso_chest_corset"]},
                },
                "layers": {
                    "standing": {
                        "base":  "Standing/Clothes/Chest/Corset/Base.png",
                        "cover": "Standing/Clothes/Chest/Corset/Cover.png",
                    },
                    "handjob": {
                        "base":  "Handjob/Clothes/Chest/Corset/Base.png",
                        "cover": "Handjob/Clothes/Chest/Corset/Cover.png",
                    },
                    "blowjob": {
                        "base":  "Blowjob/Clothes/Chest/Corset/Base.png",
                        "cover": "Blowjob/Clothes/Chest/Corset/Cover.png",
                    },
                    "titjob": {
                        "base":  "Titjob/Clothes/Chest/Corset/Base.png",
                        "cover": "Titjob/Clothes/Chest/Corset/Cover.png",
                    },
                    "cowgirl": {
                        "base":  "Cowgirl/Clothes/Chest/Corset/Base.png",
                        "cover": "Cowgirl/Clothes/Chest/Corset/Cover.png",
                    },
                    "reverse_cowgirl": {
                        "base":  "RCG/Clothes/Chest/Corset/Base.png",
                    },
                },
            },

            # ---------- CHEST: BIKINI TOP ----------
            "bikini_top": {
                "slot": "chest",
                "states": ["full", "up"],
                "poses": {
                    "standing": {"full": ["chest_bikini_top"],      "up": ["chest_bikini_top_up"]},
                    "handjob":  {"full": ["chest_bikini_top"],      "up": ["chest_bikini_top_up"]},
                    "blowjob":  {"full": ["boobs_bikini_top"],      "up": ["boobs_bikini_top_up"]},
                    "titjob":   {"full": ["chest_base_bikini"],   "up": ["chest_base_bikini"]},
                    "reverse_cowgirl":    {"full": ["torso_chest_bikini_top"], "up": ["torso_chest_bikini_top"]},
                    "cowgirl":  {"full": [],                         "up": []},
                    "doggy":    {"full": ["torso_chest_bikini_top"], "up": ["torso_chest_bikini_top"]},
                },
                "layers": {
                    "cowgirl": {
                        "full": "Cowgirl/Clothes/Chest/Black Bikini Top/Black bikini Top.png",
                        "up":   "Cowgirl/Clothes/Chest/Black Bikini Top/Black bikini Top Up.png",
                    },
                },
            },

            # ---------- SKIRT (was "legs") ----------
            "blue_skirt": {
                "slot": "skirt",
                "states": ["full", "up"],
                "poses": {
                    "standing": {"full": ["legs_blue_skirt"],  "up": ["legs_blue_skirt_up"]},
                    "blowjob":  {"full": ["legs_blue_skirt"],  "up": ["legs_blue_skirt"]},
                    "cowgirl":  {"full": ["skirt_up"],         "up": ["skirt_up"]},
                    "reverse_cowgirl":    {"full": ["skirt_on"],         "up": ["skirt_up"]},
                    "doggy":    {"full": [],                   "up": []},
                },
                "layers": {
                    "reverse_cowgirl": {
                        "rcg_skirt": "RCG/Clothes/Legs/Blue Skirt/Blue Skirt.png",
                    },
                },
            },

            # ---------- PANTIES ----------
            "purple": {
                "slot": "panties",
                "states": ["full", "side", "down"],
                "poses": {
                    "standing": {"full": ["panties_purple"],         "side": ["panties_purple_side"],  "down": ["panties_purple_down"]},
                    "blowjob":  {"full": ["panties_purple"],         "side": ["panties_purple"],       "down": []},
                    "reverse_cowgirl":    {"full": ["panties_1"],         "side": ["panties_side"],  "down": ["panties_down"]},
                    "cowgirl":  {"full": ["panties_top_1", "panties_bottom_1"], "side": ["panties_top_2", "panties_bottom_none"], "down": ["panties_top_down", "panties_bottom_none"]},
                    "doggy":    {"full": [],  "side": [],  "down": []},
                },
                "layers": {
                    "reverse_cowgirl": {
                        "rcg_panties": "RCG/Clothes/Panties/Purple Panties/Purple Panties.png",
                    },
                },
            },

            # ---------- PANTIES: BIKINI ----------
            "bikini_panties": {
                "slot": "panties",
                "states": ["full", "side", "down"],
                "poses": {
                    "standing": {"full": ["panties_bikini"],      "side": ["panties_bikini_side"],  "down": ["panties_bikini_down"]},
                    "blowjob":  {"full": ["panties_bikini"],      "side": ["panties_bikini"],       "down": []},
                    "reverse_cowgirl":    {"full": ["panties_bikini_up"],    "side": ["panties_bikini_side"],  "down": ["panties_bikini_down"]},
                    "cowgirl":  {"full": ["panties_top_bikini", "panties_bottom_bikini"], "side": ["panties_top_bikini_side", "panties_bottom_none"], "down": ["panties_top_bikini_down", "panties_bottom_none"]},
                    "doggy":    {"full": [],  "side": [],  "down": []},
                },
            },

            # ---------- SHOES ----------
            "thigh_highs": {
                "slot": "shoes",
                "states": ["full"],
                "poses": {
                    "standing": {"full": ["shoes_thigh_highs"]},
                    "blowjob":  {"full": ["legs_thigh_highs"]},
                    "reverse_cowgirl":    {"full": ["thigh_highs_on"]},
                    "cowgirl":  {"full": ["thigh_highs_on"]},
                    "doggy":    {"full": []},
                },
            },
        },

        # ====================================================
        # ROGUE
        # ====================================================
        "rogue": {

            # ---------- OVER ----------
            "towel": {
                "slot": "over",
                "states": ["full"],
                "poses": {
                    "standing": {"full": ["over_towel"]},
                },
            },

            "long_shirt": {
                "slot": "over",
                "states": ["full"],
                "poses": {
                    "standing": {"full": ["over_long_shirt"]},
                    "handjob":  {"full": ["over_long_shirt"]},
                    "blowjob":  {"full": ["over_long_shirt"]},
                    "doggy":    {"full": ["torso_over_mesh_top"]},
                },
                "layers": {
                    "blowjob": {
                        "bj_torso": "Blowjob/Clothes/Rogue BJ Shirt 2.png",
                        "bj_arms":  "Blowjob/Clothes/Rogue BJ Shirt 1.png",
                    },
                },
            },

            # ---------- CHEST ----------
            "crop_top": {
                "slot": "chest",
                "states": ["full", "up"],
                "poses": {
                    "standing": {"full": ["chest_corset", "chest_base_on"], "up": ["chest_clothes_none", "chest_base_on"]},
                    "handjob":  {"full": ["chest_corset"],           "up": ["chest_corset_down"]},
                    "blowjob":  {"full": ["crop_top_bottom", "crop_top_braces", "crop_top_top"], "up": ["crop_top_bottom", "crop_top_braces"]},
                    "reverse_cowgirl":    {"full": ["torso_chest_corset"],     "up": ["torso_chest_corset"]},
                    "cowgirl":  {"full": ["torso_clothing_corset"],  "up": ["torso_clothing_corset_up"]},
                    "doggy":    {"full": ["torso_chest_corset"],     "up": ["torso_chest_corset"]},
                },
            },

            # ---------- CHEST: BIKINI TOP ----------
            "bikini_top": {
                "slot": "chest",
                "states": ["full", "up"],
                "poses": {
                    "standing": {"full": ["chest_bikini_top"],      "up": ["chest_bikini_top_up"]},
                    "handjob":  {"full": ["chest_bikini_top"],      "up": ["chest_bikini_top_up"]},
                    "blowjob":  {"full": ["boobs_bikini_top"],      "up": ["boobs_bikini_top_up"]},
                    "titjob":   {"full": ["chest_base_bikini"],     "up": ["chest_base_bikini"]},
                    "cowgirl":  {"full": [],                        "up": []},
                    "reverse_cowgirl": {"full": ["torso_chest_bikini_top"], "up": ["torso_chest_bikini_top"]},
                    "doggy":    {"full": ["torso_chest_bikini_top"], "up": ["torso_chest_bikini_top"]},
                },
            },

            # ---------- SKIRT ----------
            "blue_skirt": {
                "slot": "skirt",
                "states": ["full", "up"],
                "poses": {
                    "standing": {"full": ["legs_blue_skirt"], "up": ["legs_blue_skirt_up"]},
                    "blowjob":  {"full": ["legs_blue_skirt"]},
                    "reverse_cowgirl":    {"full": ["skirt_on"], "up": ["skirt_up"]},
                    "doggy":    {"full": [],                   "up": []},
                },
            },

            # ---------- PANTIES ----------
            "purple": {
                "slot": "panties",
                "states": ["full", "side", "down"],
                "poses": {
                    "standing": {"full": ["panties_purple"],         "side": ["panties_purple_side"], "down": ["panties_purple_down"]},
                    "blowjob":  {"full": ["panties_purple"],         "side": ["panties_purple"],       "down": []},
                    "reverse_cowgirl":    {"full": ["panties_1"], "side": ["panties_side"], "down": ["panties_down"]},
                    "cowgirl":  {"full": ["panties_top_1", "panties_bottom_1"], "side": ["panties_top_2", "panties_bottom_none"], "down": ["panties_top_down", "panties_bottom_none"]},
                    "doggy":    {"full": [],  "side": [],  "down": []},
                },
            },

            # ---------- PANTIES: BIKINI ----------
            "bikini_panties": {
                "slot": "panties",
                "states": ["full", "side", "down"],
                "poses": {
                    "standing": {"full": ["panties_bikini"],      "side": ["panties_bikini_side"],  "down": ["panties_bikini_down"]},
                    "blowjob":  {"full": ["panties_bikini"],      "side": ["panties_bikini"],       "down": []},
                    "cowgirl":  {"full": ["panties_top_bikini", "panties_bottom_bikini"], "side": ["panties_top_bikini_side", "panties_bottom_none"], "down": ["panties_top_bikini_down", "panties_bottom_none"]},
                    "reverse_cowgirl": {"full": ["panties_bikini_up"], "side": ["panties_bikini_side"], "down": ["panties_bikini_down"]},
                    "doggy":    {"full": [],  "side": [],  "down": []},
                },
            },

            # ---------- SHOES ----------
            "thigh_highs": {
                "slot": "shoes",
                "states": ["full"],
                "poses": {
                    "standing": {"full": ["shoes_thigh_highs"]},
                    "blowjob":  {"full": ["legs_thigh_highs"]},
                    "reverse_cowgirl":    {"full": ["thigh_highs_on"]},
                    "cowgirl":  {"full": ["thigh_highs_on"]},
                    "doggy":    {"full": []},
                },
            },
        },

        # ====================================================
        # NEGASONIC (NTW)
        # ====================================================
        "ntw": {

            # ---------- OVER ----------
            "yellow_jacket": {
                "slot": "over",
                "hides_chest": True,
                "states": ["full"],
                "poses": {
                    "standing":        {"full": ["over_long_shirt"]},
                    "handjob":         {"full": ["over_long_shirt"]},
                    "blowjob":         {"full": ["over_long_shirt", "legs_over_clothed", "boobs_over_clothed", "chest_hidden"]},
                    "titjob":          {},
                    "reverse_cowgirl": {"full": ["torso_over_long_shirt"]},
                },
                "layers": {
                    "reverse_cowgirl": {
                        "arms_1": "RCG/Clothes/Over/Default Uniform/Arms 1 Clothed.png",
                    },
                },
            },

            "towel": {
                "slot": "over",
                "states": ["full"],
                "poses": {
                    "standing": {"full": ["over_towel"]},
                },
            },

            # ---------- CHEST ----------
            "yellow_bra": {
                "slot": "chest",
                "states": ["full", "up"],
                "poses": {
                    "standing": {"full": ["chest_corset"], "up": ["chest_corset_up"]},
                    "handjob":  {"full": ["chest_corset"], "up": ["chest_corset_up"]},
                    "blowjob":  {"full": ["boobs_clothes_1", "chest_hidden"], "up": ["boobs_clothes_1_up"]},
                    "titjob":   {"full": ["chest_base_none"], "up": ["chest_base_none"]},
                    "cowgirl":  {"full": ["torso_clothing_corset"], "up": ["torso_clothing_corset_up"]},
                    "full_nelson": {"full": ["yellow_top_down"], "up": ["yellow_top_up"]},
                },
            },

            # ---------- PANTIES ----------
            "yellow_panties": {
                "slot": "panties",
                "states": ["full", "side", "down"],
                "poses": {
                    "standing":        {"full": ["panties_yellow"],  "side": ["panties_yellow_side"],  "down": ["panties_yellow_down"]},
                    "blowjob":         {"full": ["panties_yellow"],  "side": ["panties_yellow"],       "down": []},
                    "cowgirl":         {"full": ["panties_top_1", "panties_bottom_1"], "side": ["panties_top_2", "panties_bottom_none"], "down": ["panties_top_down", "panties_bottom_none"]},
                    "reverse_cowgirl": {"full": ["panties_1"], "side": ["panties_side"], "down": ["panties_down"]},
                    "full_nelson":     {"full": ["yellow_bottom_on"]},
                },
            },

            # ---------- CHEST: BIKINI TOP ----------
            "bikini_top": {
                "slot": "chest",
                "states": ["full", "up"],
                "poses": {
                    "standing": {"full": ["chest_bikini_top"],      "up": ["chest_bikini_top_up"]},
                    "handjob":  {"full": ["chest_bikini_top"],      "up": ["chest_bikini_top_up"]},
                    "blowjob":  {"full": ["boobs_bikini_top", "chest_hidden"],      "up": ["boobs_bikini_top_up"]},
                    "cowgirl":  {"full": [],                        "up": []},
                    "reverse_cowgirl": {"full": ["torso_chest_bikini_top"], "up": ["torso_chest_bikini_top"]},
                    "full_nelson": {"full": ["bikini_top_down"], "up": ["bikini_top_up"]},
                },
                "layers": {
                    "cowgirl": {
                        "full": "Cowgirl/Clothes/Chest/Pink Bikini Top/Pink Bikini Top.png",
                        "up":   "Cowgirl/Clothes/Chest/Pink Bikini Top/Pink Bikini Top Up.png",
                    },
                },
            },

            # ---------- PANTIES: BIKINI ----------
            "bikini_panties": {
                "slot": "panties",
                "states": ["full", "side", "down"],
                "poses": {
                    "standing": {"full": ["panties_bikini"],      "side": ["panties_bikini_side"],  "down": ["panties_bikini_down"]},
                    "blowjob":  {"full": ["panties_bikini"],      "side": ["panties_bikini"],       "down": []},
                    "cowgirl":  {"full": ["panties_top_bikini", "panties_bottom_bikini"], "side": ["panties_top_bikini_side", "panties_bottom_none"], "down": ["panties_top_bikini_down", "panties_bottom_none"]},
                    "reverse_cowgirl": {"full": ["panties_bikini_up"], "side": ["panties_bikini_side"], "down": ["panties_bikini_down"]},
                    "full_nelson":     {"full": ["bikini_bottom_on"]},
                },
            },
        },

        # ====================================================
        # TENNY
        # ====================================================
        "tenny": {

            # ---------- OVER ----------
            "blue_jacket": {
                "slot": "over",
                "hides_chest": ["full"],
                "states": ["full", "up"],
                "poses": {
                    "standing":   {"full": ["over_body_blue_jacket", "over_blue_jacket"], "up": ["over_body_none", "over_blue_jacket_up"]},
                    "blowjob":    {"full": ["over_blue_jacket"]},
                    "handjob":    {"full": ["over_blue_jacket"]},
                    "laying_down": {"full": []},
                },
            },
            "blue_shirt": {
                "slot": "mid",
                "hides_chest": ["full"],
                "states": ["full", "up"],
                "poses": {
                    "standing":   {"full": ["mid_body_blue_shirt", "mid_blue_shirt"], "up": ["mid_body_none", "mid_blue_shirt_up"]},
                    "blowjob":    {"full": ["over_blue_shirt"]},
                    "handjob":    {"full": ["over_blue_shirt"]},
                    "laying_down": {"full": []},
                },
            },
            "towel": {
                "slot": "over",
                "states": ["full"],
                "poses": {
                    "standing": {"full": ["over_towel"]},
                },
            },

            # ---------- CHEST ----------
            "white_bra": {
                "slot": "chest",
                "states": ["full", "up"],
                "poses": {
                    "standing":   {"full": ["chest_white_bra"], "up": ["chest_white_bra_up"]},
                    "blowjob":    {"full": ["boobs_white_top", "chest_hidden"], "up": ["boobs_white_top_up"]},
                    "handjob":    {"full": ["boobs_white_top", "chest_hidden"], "up": ["boobs_white_top_up"]},
                    "laying_down": {"full": []},
                    "full_nelson": {"full": ["white_top_down"], "up": ["white_top_up"]},
                },
            },
            "blue_bikini_top": {
                "slot": "chest",
                "states": ["full", "up"],
                "poses": {
                    "standing":   {"full": ["chest_blue_bikini_top"], "up": ["chest_blue_bikini_top_up"]},
                    "blowjob":    {"full": ["boobs_bikini_top", "chest_hidden"], "up": ["boobs_bikini_top_up"]},
                    "handjob":    {"full": ["boobs_bikini_top", "chest_hidden"], "up": ["boobs_bikini_top_up"]},
                    "laying_down": {"full": []},
                    "full_nelson": {"full": ["bikini_top_down"], "up": ["bikini_top_up"]},
                },
            },

            # ---------- LEGS ----------
            "white_legs": {
                "slot": "skirt",
                "strip_name": "pants",
                "states": ["full", "up"],
                "poses": {
                    "standing": {"full": ["legs_white_legs"], "up": ["legs_white_legs_down"]},
                    "blowjob":  {"full": ["legs_white_pants"]},
                    "handjob":  {"full": ["legs_white_pants"]},
                },
                "wet_attrs": {"legs_white_legs": "legs_white_legs_wet"},
            },

            # ---------- PANTIES ----------
            "striped_panties": {
                "slot": "panties",
                "states": ["full", "side", "down"],
                "poses": {
                    "standing":   {"full": ["panties_striped"], "side": ["panties_striped_side"], "down": ["panties_striped_down"]},
                    "blowjob":    {"full": ["panties_striped"]},
                    "handjob":    {"full": ["panties_striped"]},
                    "laying_down": {"full": [], "side": [], "down": []},
                    "full_nelson": {"full": ["striped_bottom_on"]},
                },
            },
            "blue_bikini_bottom": {
                "slot": "panties",
                "states": ["full", "side", "down"],
                "poses": {
                    "standing":   {"full": ["panties_blue_bikini"], "side": ["panties_blue_bikini_side"], "down": ["panties_blue_bikini_down"]},
                    "blowjob":    {"full": ["panties_bikini"]},
                    "handjob":    {"full": ["panties_bikini"]},
                    "laying_down": {"full": [], "side": [], "down": []},
                    "full_nelson": {"full": ["bikini_bottom_on"]},
                },
            },

            # ---------- SHOES ----------
            "thigh_highs": {
                "slot": "shoes",
                "states": ["full"],
                "poses": {
                    "standing": {"full": ["shoes_thigh_highs"]},
                },
            },
        },

        # ====================================================
        # SHION
        # ====================================================
        "shion": {

            # ---------- OVER ----------
            # No "titjob" on the jacket or the vest: her titjob is only done in a bra / bikini top or bare (author's
            # rule), both come off at TITJOB_Launch.
            "jacket": {
                "slot": "over",
                "states": ["full"],
                "poses": {
                    "standing": {"full": ["over_body_jacket"]},
                    "handjob":  {"full": ["over_jacket"]},
                    "blowjob":  {"full": ["over_jacket_1"]},
                },
            },
            "towel": {
                "slot": "over",
                "states": ["full"],
                "poses": {
                    "standing": {"full": ["over_towel"]},
                },
            },

            # ---------- MID ----------
            "vest": {
                "slot": "mid",
                "states": ["full"],
                "poses": {
                    "standing": {"full": ["mid_body_vest"]},
                    "handjob":  {"full": ["over_vest"]},
                    "blowjob":  {"full": ["over_vest"]},
                },
            },

            # ---------- CHEST ----------
            # Titjob: her bra / bikini top are full cups drawn to the boobs, shown ABOVE them as standalone
            # "shion tj_bra" / "shion tj_bikini_top" (Core_Titjob, z 9984); nothing of them in the layeredimage.
            "bra": {
                "slot": "chest",
                "states": ["full", "up"],
                "poses": {
                    "standing": {"full": ["chest_bra"],       "up": ["chest_bra_semi"]},
                    "handjob":  {"full": ["boobs_bra"]},
                    "blowjob":  {"full": ["boobs_bra"]},
                    "titjob":   {"full": ["chest_base_none"], "up": ["chest_base_none"]},
                },
            },
            "bikini_top": {
                "slot": "chest",
                "states": ["full"],
                "poses": {
                    "standing": {"full": ["chest_bikini_top"]},
                    "handjob":  {"full": ["boobs_bikini_top"]},
                    "blowjob":  {"full": ["boobs_bikini_top"]},
                    "titjob":   {"full": ["chest_base_none"]},
                },
            },

            # ---------- PANTIES ----------
            "panties": {
                "slot": "panties",
                "states": ["full", "side"],
                "poses": {
                    "standing": {"full": ["panties_on"],     "side": ["panties_semi"]},
                    "handjob":  {"full": ["panties_on"]},
                    "blowjob":  {"full": ["panties_on"]},
                },
            },
            "bikini_bottom": {
                "slot": "panties",
                "states": ["full"],
                "poses": {
                    "standing": {"full": ["panties_bikini"]},
                    "handjob":  {"full": ["panties_bikini"]},
                    "blowjob":  {"full": ["panties_bikini"]},
                },
            },

            # ---------- SKIRT (pants) ----------
            "pants": {
                "slot": "skirt",
                "states": ["full", "down"],
                "poses": {
                    "standing": {"full": ["pants_on"],   "down": ["pants_semi"]},
                    "blowjob":  {"full": ["pants_on"]},
                },
            },
        },
    }

    # ============================================================
    # POSE_SLOTS — which clothing slots each pose can render
    # ============================================================
    POSE_SLOTS = {
        "standing": ["shoes", "panties", "skirt", "chest", "mid", "over"],
        "handjob":  ["shoes", "panties", "skirt", "chest", "mid", "over"],
        "blowjob":  ["shoes", "panties", "skirt", "chest", "mid", "over"],
        "titjob":   ["chest"],
        "cowgirl":  ["shoes", "panties", "skirt", "chest", "mid", "over"],
        "reverse_cowgirl":    ["shoes", "panties", "skirt", "chest", "mid", "over"],
        "reverse_cowgirl_anal": ["shoes", "panties", "skirt", "chest", "mid", "over"],
        "doggy":    ["shoes", "panties", "skirt", "chest", "mid", "over"],
        "full_nelson": ["panties", "chest"],
        "full_nelson_anal": ["panties", "chest"],
        "laying_down": ["panties", "chest", "mid", "over"],
        "laying_anal": ["panties", "chest", "mid", "over"],
    }

    def _strip_name_for_slot(girl, slot):
        """Return display name for strip menu (e.g. 'pants' instead of 'skirt')."""
        item = getattr(girl, "clothes", {}).get(slot)
        if item:
            cfg = CLOTHING_REGISTRY.get(getattr(girl, "gid", ""), {}).get(item, {})
            sn = cfg.get("strip_name")
            if sn:
                return sn
        _SLOT_DEFAULTS = {"skirt": "skirt", "over": "top", "chest": "chest", "mid": "shirt", "panties": "panties", "shoes": "shoes"}
        return _SLOT_DEFAULTS.get(slot, slot)

    # The name of a clothing ITEM as the player reads it (strip menus), by item id (one id = one name for every girl).
    # _strip_name_for_slot above is the slot WORD the code compares ("pants" / "skirt"); this one is only shown.
    CLOTHING_ITEM_NAMES = {
        "long_shirt": _("long shirt"),
        "towel": _("towel"),
        "corset": _("corset"),
        "crop_top": _("crop top"),
        "bikini_top": _("bikini top"),
        "blue_bikini_top": _("blue bikini top"),
        "bikini_bottom": _("bikini bottom"),
        "blue_bikini_bottom": _("blue bikini bottom"),
        "bikini_panties": _("bikini panties"),
        "blue_skirt": _("blue skirt"),
        "purple": _("purple panties"),
        "yellow_panties": _("yellow panties"),
        "striped_panties": _("striped panties"),
        "panties": _("panties"),
        "thigh_highs": _("thigh highs"),
        "yellow_jacket": _("yellow jacket"),
        "blue_jacket": _("blue jacket"),
        "jacket": _("jacket"),
        "yellow_bra": _("yellow bra"),
        "white_bra": _("white bra"),
        "bra": _("bra"),
        "blue_shirt": _("blue shirt"),
        "vest": _("vest"),
        "white_legs": _("white pants"),
        "pants": _("pants"),
    }

    def clothing_item_name(girl, slot):
        """The item she wears in that slot, named for the player and translated ("" when the slot is empty). An id not in
        CLOTHING_ITEM_NAMES shows as the id with spaces (logged: give it a name)."""
        item = getattr(girl, "clothes", {}).get(slot)
        if not item or item == "none":
            return ""
        if item not in CLOTHING_ITEM_NAMES:
            print("[CLOTHING] no CLOTHING_ITEM_NAMES entry for %r (%s)" % (item, getattr(girl, "gid", "?")))
            return item.replace("_", " ")
        return _tl(CLOTHING_ITEM_NAMES[item])

    # ============================================================
    # Unified clothing attribute builder
    # ============================================================
    def _build_clothing_attributes(girl, pose):
        """Build layeredimage attribute list from girl's clothing state.
        Reads girl.clothes / girl.clothes_state + CLOTHING_REGISTRY."""
        attrs = []
        gid = getattr(girl, "gid", getattr(girl, "Id", ""))
        registry = CLOTHING_REGISTRY.get(gid, {})
        slots_for_pose = POSE_SLOTS.get(pose, [])

        # Ensure clothes dict exists
        if not hasattr(girl, "clothes") or not isinstance(getattr(girl, "clothes", None), dict):
            girl.clothes = {"over": None, "mid": None, "chest": None, "skirt": None, "panties": None, "shoes": None}
        if not hasattr(girl, "clothes_state") or not isinstance(getattr(girl, "clothes_state", None), dict):
            girl.clothes_state = {"over": "full", "mid": "full", "chest": "full", "skirt": "full", "panties": "full", "shoes": "full"}

        # Shower override: force shower-specific clothing
        # For "nude" state, apply to ALL poses (not just standing) so RCG/cowgirl
        # massage scenes in the shower correctly show nude body.
        _sh_state = getattr(girl, "shower_state", None)
        _in_showers = (getattr(store, "CurrentLocation", "") in SHOWER_SPOTS)
        _shower_override = (_sh_state and _sh_state != "dressed" and _in_showers and (pose == "standing" or _sh_state == "nude"))

        # Check if over or mid item hides chest for this pose
        # hides_chest: True = always, ["full"] = only in listed states
        _over_hides_chest = False
        for _hc_slot in ("over", "mid"):
            _hc_code = girl.clothes.get(_hc_slot)
            if _hc_code:
                _hc_cfg = registry.get(_hc_code, {})
                _hc_hides = _hc_cfg.get("hides_chest")
                if _hc_hides and _hc_cfg.get("poses", {}).get(pose) is not None:
                    if _hc_hides is True or girl.clothes_state.get(_hc_slot, "full") in _hc_hides:
                        _over_hides_chest = True
                        break

        debug_log("[DEBUG] _build_clothing_attributes: gid=%s pose=%s clothes=%s states=%s shower_state=%s shower_override=%s over_hides_chest=%s" % (gid, pose, str(girl.clothes), str(girl.clothes_state), str(_sh_state), str(_shower_override), str(_over_hides_chest)))

        for slot in slots_for_pose:
            if _shower_override:
                # Force shower clothing regardless of girl.clothes
                _shower_attrs = _get_shower_slot_attrs(girl, slot, _sh_state, registry, pose)
                if _shower_attrs is not None:
                    attrs.extend(_shower_attrs)
                    continue

            if slot == "chest" and _over_hides_chest and not _shower_override:
                attrs.extend(_none_attrs_for_slot("chest", pose, girl))
                continue

            item_code = girl.clothes.get(slot)
            if not item_code:
                # No item — only emit none attrs if the girl has ANY item
                # that renders in this slot+pose (i.e. the layeredimage has the group). An item whose entry for
                # the pose is {} (NTW's jacket in the titjob) draws nothing there: no group to reset.
                _slot_has_pose_art = False
                for _rc in registry.values():
                    if _rc.get("slot") == slot and _rc.get("poses", {}).get(pose):
                        _slot_has_pose_art = True
                        break
                if _slot_has_pose_art:
                    attrs.extend(_none_attrs_for_slot(slot, pose, girl))
                continue

            item_cfg = registry.get(item_code)
            if not item_cfg:
                continue

            pose_map = item_cfg.get("poses", {}).get(pose)
            if pose_map is None:
                # Item with no art for this pose (a towel in a sex pose): render the slot BARE.
                # Skipping silently left the layeredimage group on its DEFAULT garment, so she
                # "gained" clothes she was not wearing. Same group guard as the empty-slot path.
                _slot_has_pose_art = False
                for _rc in registry.values():
                    if _rc.get("slot") == slot and _rc.get("poses", {}).get(pose):
                        _slot_has_pose_art = True
                        break
                if _slot_has_pose_art:
                    print("[CLOTHING] %s: %r has no %s art, slot %s rendered bare" % (gid, item_code, pose, slot))
                    attrs.extend(_none_attrs_for_slot(slot, pose, girl))
                continue

            state = girl.clothes_state.get(slot, "full")
            # Clamp to supported states
            if state not in item_cfg.get("states", ["full"]):
                state = "full"

            attr_list = pose_map.get(state, [])
            _wet_map = item_cfg.get("wet_attrs")
            if _wet_map and "dripping" in getattr(girl, "Cum", []):
                attr_list = [_wet_map.get(a, a) for a in attr_list]
            attrs.extend(attr_list)

        return attrs

    def _none_attrs_for_slot(slot, pose, girl=None):
        """Return ALL 'none' attributes needed when a slot is empty.
        Derives from CLOTHING_REGISTRY: finds what attrs the character's item
        would emit for this slot+pose, then returns the none version of each group."""

        # Default fallback (standing/handjob/generic)
        _NONE_MAP = {
            "over":    ["over_none"],
            "mid":     ["mid_none"],
            "chest":   ["chest_clothes_none"],
            "skirt":   ["legs_none"],
            "panties": ["panties_none"],
            "shoes":   ["shoes_none"],
        }

        # Pose-specific defaults (Gwen-compatible fallbacks)
        _POSE_NONE = {
            "reverse_cowgirl":   {"over": ["torso_over_none"], "chest": ["torso_chest_none"], "skirt": ["skirt_none"], "shoes": ["thigh_highs_none"]},
            "cowgirl": {"over": ["torso_over_none"], "chest": ["torso_clothing_none"], "skirt": ["skirt_none"], "panties": ["panties_top_none", "panties_bottom_none"], "shoes": ["thigh_highs_none"]},
            "doggy":   {"over": ["torso_over_none"], "chest": ["torso_chest_none"]},
            "titjob":  {"chest": ["chest_base_none"]},
        }

        # For complex poses (BJ, RCG, cowgirl, TJ, FN), derive nones from registry
        # because group names vary per character. Standing/HJ use standard defaults.
        if girl and pose in ("blowjob", "reverse_cowgirl", "reverse_cowgirl_anal", "cowgirl", "titjob", "full_nelson", "full_nelson_anal"):
            gid = getattr(girl, "gid", getattr(girl, "Id", ""))
            registry = CLOTHING_REGISTRY.get(gid, {})

            all_attrs = set()
            for item_cfg in registry.values():
                if item_cfg.get("slot") != slot:
                    continue
                pose_map = item_cfg.get("poses", {}).get(pose, {})
                for state_attrs in pose_map.values():
                    for a in state_attrs:
                        all_attrs.add(a)

            if all_attrs:
                _ATTR_TO_NONE = {
                    # Gwen BJ
                    "corset":           "torso_corset_none",
                    "boobs_clothes_1":  "boobs_clothes_none",
                    "boobs_clothes_2":  "boobs_clothes_none",
                    "boobs_bikini_top": "boobs_clothes_none",
                    "boobs_bikini_top_up": "boobs_clothes_none",
                    "boobs_white_top":  "boobs_clothes_none",
                    "boobs_white_top_up": "boobs_clothes_none",
                    "over_long_shirt":  "torso_arms_none",
                    "legs_over_clothed":"legs_over_none",
                    "boobs_over_clothed":"boobs_over_none",
                    # Rogue BJ
                    "crop_top_bottom":  "chest_bottom_none",
                    "crop_top_braces":  "chest_braces_none",
                    "crop_top_top":     "chest_top_none",
                    # RCG
                    "torso_chest_corset": "torso_chest_none",
                    "torso_chest_bikini_top": "torso_chest_none",
                    "torso_over_long_shirt": "torso_over_none",
                    # Cowgirl
                    "torso_clothing_corset": "torso_clothing_none",
                    "torso_clothing_corset_up": "torso_clothing_none",
                    # Titjob
                    "corset_up_on":     "corset_up_none",
                    "chest_base_bikini":"chest_base_none",
                    "chest_base_on":    "chest_base_none",
                    # Generic (shared across poses)
                    "panties_top_1":    "panties_top_none",
                    "panties_top_2":    "panties_top_none",
                    "panties_top_bikini":      "panties_top_none",
                    "panties_top_bikini_side": "panties_top_none",
                    "panties_top_bikini_down": "panties_top_none",
                    "panties_bottom_1": "panties_bottom_none",
                    "panties_bottom_bikini":   "panties_bottom_none",
                    "panties_1":        "panties_none",
                    "panties_bikini_up":       "panties_none",
                    "legs_blue_skirt":  "legs_clothes_none",
                    "legs_thigh_highs": "legs_thighs_none",
                    "thigh_highs_on":   "thigh_highs_none",
                    "skirt_on":         "skirt_none",
                    # NTW Full Nelson
                    "yellow_top_down":  "yellow_top_none",
                    "yellow_top_up":    "yellow_top_none",
                    "yellow_bottom_on": "yellow_bottom_none",
                    "bikini_top_down":  "bikini_top_none",
                    "bikini_top_up":    "bikini_top_none",
                    "bikini_bottom_on": "bikini_bottom_none",
                }
                none_attrs = set()
                for a in all_attrs:
                    n = _ATTR_TO_NONE.get(a)
                    if n:
                        none_attrs.add(n)
                if none_attrs:
                    return list(none_attrs)

        # Fallback: pose-specific or default
        if pose in _POSE_NONE and slot in _POSE_NONE[pose]:
            return list(_POSE_NONE[pose][slot])
        result = list(_NONE_MAP.get(slot, ["%s_none" % slot]))

        # Standing/HJ: check registry for extra chest groups (e.g. chest_base, boobs_clothes)
        if girl and pose in ("standing", "handjob") and slot == "chest":
            gid = getattr(girl, "gid", getattr(girl, "Id", ""))
            _reg = CLOTHING_REGISTRY.get(gid, {})
            _all_chest_attrs = set()
            for _ic in _reg.values():
                if _ic.get("slot") != "chest":
                    continue
                for _sa in _ic.get("poses", {}).get(pose, {}).values():
                    _all_chest_attrs.update(_sa)
            if any("chest_base" in a for a in _all_chest_attrs):
                if "chest_base_none" not in result:
                    result.append("chest_base_none")
            if any(a.startswith("boobs_") for a in _all_chest_attrs):
                if "boobs_clothes_none" not in result:
                    result.append("boobs_clothes_none")

        # Standing: include towel arm nones when clearing over
        if girl and pose == "standing" and slot == "over":
            gid = getattr(girl, "gid", getattr(girl, "Id", ""))
            _reg = CLOTHING_REGISTRY.get(gid, {})
            result.extend(_towel_arm_nones(_reg))

        # Standing: include body group nones for mid/over
        if girl and pose == "standing" and slot in ("mid", "over"):
            gid = getattr(girl, "gid", getattr(girl, "Id", ""))
            _reg = CLOTHING_REGISTRY.get(gid, {})
            result.extend(_body_group_nones(_reg, slot, pose))

        return result

    def _slot_renderable(girl, slot, pose):
        """True if the girl's item in this slot has art for this pose."""
        if slot not in POSE_SLOTS.get(pose, []):
            return False
        gid = getattr(girl, "gid", getattr(girl, "Id", ""))
        item_code = girl.clothes.get(slot)
        if not item_code:
            return False
        item_cfg = CLOTHING_REGISTRY.get(gid, {}).get(item_code)
        if not item_cfg:
            return False
        return bool(item_cfg.get("poses", {}).get(pose))

    def _body_group_nones(registry, slot, pose):
        """Return body group none attrs if any registry item uses them."""
        _prefix = "%s_body_" % slot
        for _ic in registry.values():
            if not isinstance(_ic, dict) or _ic.get("slot") != slot:
                continue
            for _sa in _ic.get("poses", {}).get(pose, {}).values():
                if any(a.startswith(_prefix) for a in _sa):
                    return ["%s_body_none" % slot]
        return []

    def _towel_arm_nones(registry):
        """Return none attrs for towel arm re-render layers."""
        if "towel" not in registry:
            return []
        return ["towel_arm_left_none"]

    def _over_none_attrs(registry):
        """Return full none list for over slot including towel arm nones."""
        result = ["over_none"]
        result.extend(_towel_arm_nones(registry))
        return result

    def _get_shower_slot_attrs(girl, slot, sh_state, registry, pose="standing"):
        """Return forced attrs for a slot during shower, or None to use normal logic."""
        if sh_state == "towel":
            if slot == "over":
                tcfg = registry.get("towel", {})
                pm = tcfg.get("poses", {}).get("standing", {}).get("full", [])
                return pm if pm else ["over_towel", "towel_arms"]
            elif slot in ("mid", "chest", "panties", "skirt", "shoes"):
                return _none_attrs_for_slot(slot, pose, girl)
        elif sh_state == "nude":
            if slot == "over":
                return _none_attrs_for_slot("over", pose, girl)
            return _none_attrs_for_slot(slot, pose, girl)
        elif sh_state == "underwear":
            if slot in ("over", "mid"):
                return _none_attrs_for_slot(slot, "standing", girl)
            if slot in ("skirt", "shoes"):
                return _none_attrs_for_slot(slot, "standing", girl)
            return None  # keep chest/panties from girl.clothes
        elif sh_state == "missing_top":
            if slot in ("over", "mid"):
                return _none_attrs_for_slot(slot, "standing", girl)
            if slot in ("chest", "shoes"):
                return _none_attrs_for_slot(slot, "standing", girl)
            return None
        elif sh_state == "missing_bottom":
            if slot in ("over", "mid", "skirt", "panties", "shoes"):
                return _none_attrs_for_slot(slot, "standing", girl)
            return None
        return None

    # ============================================================
    # Panties state rotation helper
    # ============================================================
    def _panties_next_state(girl):
        """Returns the next displacement state for panties ('side' or 'down'),
        or None if already at max displacement or no panties.
        Skips 'side' if it's visually identical to 'full' in the current pose
        (e.g. RCG bikini has no separate normal image)."""
        if not girl.Panties:
            return None
        current = girl.clothes_state.get("panties", "full")
        gid = getattr(girl, "gid", getattr(girl, "Id", ""))
        item_cfg = CLOTHING_REGISTRY.get(gid, {}).get(girl.Panties, {})
        supported = item_cfg.get("states", ["full"])

        # Check current pose to detect visually identical states
        pose = sprite_state.get(girl.Id, {}).get("pose", "standing")
        pose_map = item_cfg.get("poses", {}).get(pose, {})

        if current == "full":
            if "side" in supported:
                # Skip side if this pose has no side visual or same visual as full
                if "side" not in pose_map or pose_map.get("full", []) == pose_map.get("side", []):
                    if "down" in supported:
                        return "down"
                    return None
                return "side"
            elif "down" in supported:
                return "down"
        elif current == "side":
            if "down" in supported:
                return "down"
        return None

    def _item_has_state(girl, slot, state):
        """Check if the current item in a slot supports a given state
        AND the current pose has a visual for it."""
        item = girl.clothes.get(slot)
        if not item:
            print("[_item_has_state] %s slot=%s state=%s -> NO ITEM" % (getattr(girl, "gid", "?"), slot, state))
            return False
        gid = getattr(girl, "gid", getattr(girl, "Id", ""))
        cfg = CLOTHING_REGISTRY.get(gid, {}).get(item, {})
        if state not in cfg.get("states", ["full"]):
            print("[_item_has_state] %s item=%s slot=%s state=%s -> NOT IN STATES %s" % (gid, item, slot, state, cfg.get("states", ["full"])))
            return False
        pose = sprite_state.get(girl.Id, {}).get("pose", "standing")
        pose_map = cfg.get("poses", {}).get(pose, {})
        result = state in pose_map
        print("[_item_has_state] %s item=%s slot=%s state=%s pose=%s pose_keys=%s -> %s" % (gid, item, slot, state, pose, list(pose_map.keys()), result))
        return result

    def _bottom_accessible(girl):
        """True if pussy is accessible: panties removed or displaced (side/down),
        AND skirt removed or displaced (up). Used for penetration checks."""
        _skirt_ok = girl.Legs is None or girl.clothes_state.get("skirt") in ("up",)
        _pan_ok = girl.Panties is None or girl.clothes_state.get("panties") in ("side", "down")
        return _skirt_ok and _pan_ok

    # ============================================================
    # Strip / Displace / Dress helpers
    # ============================================================
    def cloth_strip(girl, slot, pose=None):
        """Remove item from slot."""
        girl.clothes[slot] = None
        girl.clothes_state[slot] = "full"
        if pose is not False:
            _p = pose or getattr(girl, "default_pose", "standing")
            set_girl_sprite(girl, pose=_p)

    def cloth_displace(girl, slot, target_state, pose=None):
        """Change clothing state without removing (e.g. panties to 'side')."""
        item = girl.clothes.get(slot)
        if not item:
            return
        gid = getattr(girl, "gid", getattr(girl, "Id", ""))
        registry = CLOTHING_REGISTRY.get(gid, {})
        cfg = registry.get(item, {})
        if target_state in cfg.get("states", ["full"]):
            girl.clothes_state[slot] = target_state
        if pose is not False:
            _p = pose or getattr(girl, "default_pose", "standing")
            set_girl_sprite(girl, pose=_p)

    def cloth_dress(girl, slot, item_code, pose=None):
        """Put an item on a slot."""
        girl.clothes[slot] = item_code
        girl.clothes_state[slot] = "full"
        if pose is not False:
            _p = pose or getattr(girl, "default_pose", "standing")
            set_girl_sprite(girl, pose=_p)

    # ============================================================
    # Extra layers — for sub-parts shown at different z-orders
    # ============================================================
    def get_clothing_layers(girl, slot, pose):
        """Returns dict {layer_tag: full_image_path} for extra layers.
        Returns empty dict if item has no extra layers for this pose."""
        gid = getattr(girl, "gid", getattr(girl, "Id", ""))
        item = girl.clothes.get(slot)
        if not item:
            return {}
        registry = CLOTHING_REGISTRY.get(gid, {})
        cfg = registry.get(item, {})
        pose_layers = cfg.get("layers", {}).get(pose)
        if not pose_layers:
            return {}
        base = "images/characters/%s" % girl_asset_folder(girl)
        return {tag: "%s/%s" % (base, path) for tag, path in pose_layers.items()}

    def get_clothing_layer_path(girl, slot, pose, layer_tag):
        """Returns image path for a specific extra layer, or None.
        Use this in ConditionSwitch or renpy.show() calls."""
        layers = get_clothing_layers(girl, slot, pose)
        return layers.get(layer_tag)

    def has_clothing_layer(girl, slot, pose, layer_tag):
        """Returns True if this layer exists for the current clothing item."""
        return get_clothing_layer_path(girl, slot, pose, layer_tag) is not None
