# ============================================================
# PHONE PHOTO REQUEST SYSTEM
# ============================================================
# Player asks a girl to send a photo via phone.
# The girl decides what to send based on her stats, traits,
# and what acts they've done together.
# ============================================================

init python:

    # ----------------------------------------------------------
    # Location -> background image path
    # ----------------------------------------------------------
    _LOC_TO_BG = {
        "campus":     "images/bg/Campus.jpg",
        "pool":       "images/bg/Pool.jpg",
        "shower":     "images/bg/Shower.png",
        "showers":    "images/bg/Shower.png",
        "room":       "images/bg/Playerroom.jpg",
        "gwen_room":  "images/bg/GwenRoom.png",
        "rogue_room": "images/bg/RogueRoom.jpg",
        "classroom":  "images/bg/Classroom.png",
        "gym":        "images/bg/gym.jpg",
        "apartment":        "images/bg/Apartment.jpg",
        "apartment_room":   "images/bg/ApartmentRoom.jpg",
        "apartment_shower": "images/bg/ApartmentShower.jpg",
    }

    # Phone screen content area (matches Phone.png screen bounds)
    _PHONE_CONTENT_X = 66
    _PHONE_CONTENT_Y = 55
    _PHONE_CONTENT_W = 520
    _PHONE_CONTENT_H = 940

    # ----------------------------------------------------------
    # Pose transforms for inside the phone viewport
    # ----------------------------------------------------------
    # Each pose needs its own mini-transform for the phone frame.

    # ----------------------------------------------------------
    # Photo state (set by decision logic, read by screen)
    # ----------------------------------------------------------
    store._photo_girl = None
    store._photo_pose = "standing"
    store._photo_over = None
    store._photo_chest = None
    store._photo_legs = None
    store._photo_panties = None
    store._photo_expression = "smile"
    store._photo_result = None

    # ----------------------------------------------------------
    # Girl decides the photo
    # ----------------------------------------------------------

    def _photo_decide(girl):
        """
        Girl decides pose, clothing, and expression based on her
        stats, traits, and sexual history with the player.

        Sets store._photo_* variables.

        Returns:
            { "accepted": bool, "reason": str }
        """
        _inbt = getattr(girl, "Inbt", 0)
        _love = getattr(girl, "Love", 0)
        _lust = getattr(girl, "Lust", 0)
        acts = getattr(girl, "Sex_acts", {}) or {}

        store._photo_girl = girl

        # --- DENY CONDITIONS ---

        # she never sends photos, whatever her stats or step (GIRLS_CONFIG "no_photos": Shion, the author's
        # rule 2026-10-10). The ask stays clickable; she refuses in her own voice, before any other reason.
        if not girl_sends_photos(girl):
            print("[PHOTO] %s refuses the photo ask: her config says no_photos" % girl.gid)
            return {"accepted": False, "reason": "no_photos"}

        # her story locks it (story_steps.rpy, act "photo" = flirt tier): refused whatever her stats
        if story_act_locked(girl, "photo"):
            return {"accepted": False, "reason": "story_locked"}

        # camera_hater: hard deny unless very broken in
        if girl.has_trait("camera_hater"):
            if _inbt < 500:
                return {"accepted": False, "reason": "camera_hater"}

        # Must have some Love
        if _love < 100:
            return {"accepted": False, "reason": "low_love"}

        # Basic Inbt gate
        if _inbt < 50:
            return {"accepted": False, "reason": "low_inbt"}

        # --- POSE SELECTION ---
        # Pick the most intimate pose she's willing to show,
        # based on what they've done together.

        _possible_poses = ["standing"]

        if acts.get("tj", 0) > 0 and _inbt >= 300 and girl_has_pose(girl, "titjob"):
            _possible_poses.append("titjob")

        if acts.get("reverse_cowgirl", 0) > 0 and _inbt >= 350 and girl_has_pose(girl, "reverse_cowgirl"):
            _possible_poses.append("reverse_cowgirl")

        if (acts.get("cowgirl", 0) > 0 or acts.get("sex", 0) > 0) and _inbt >= 350 and girl_has_pose(girl, "cowgirl"):
            _possible_poses.append("cowgirl")

        # Higher Inbt/Lust = more likely to pick a bold pose
        if _inbt >= 400 and _lust >= 40 and len(_possible_poses) > 1:
            # Weight toward bolder poses
            _weights = []
            for p in _possible_poses:
                if p == "standing":
                    _weights.append(1)
                elif p == "titjob":
                    _weights.append(3)
                elif p == "reverse_cowgirl":
                    _weights.append(3)
                elif p == "cowgirl":
                    _weights.append(3)
                else:
                    _weights.append(1)
        else:
            _weights = [1] * len(_possible_poses)

        # Trait adjustments
        if girl.has_trait("camera_lover"):
            # camera_lover loves bold photos
            for i, p in enumerate(_possible_poses):
                if p != "standing":
                    _weights[i] *= 3
        elif girl.has_trait("cute_sex"):
            # cute_sex prefers standing
            for i, p in enumerate(_possible_poses):
                if p == "standing":
                    _weights[i] *= 3
        elif girl.has_trait("hardcore_sex"):
            # hardcore prefers action poses
            for i, p in enumerate(_possible_poses):
                if p in ("reverse_cowgirl", "cowgirl"):
                    _weights[i] *= 4

        # Weighted random pick
        _total_w = sum(_weights)
        _r = renpy.random.uniform(0, _total_w)
        _acc = 0.0
        _chosen_pose = _possible_poses[0]
        for i, p in enumerate(_possible_poses):
            _acc += _weights[i]
            if _r <= _acc:
                _chosen_pose = p
                break

        store._photo_pose = _chosen_pose

        # --- CLOTHING SELECTION ---
        # Based on Inbt tier and chosen pose.

        # Get girl's default outfit
        presets = OUTFIT_PRESETS.get(girl.Id, {})
        casual = presets.get("casual", {})
        _default_over = casual.get("over")
        _default_chest = casual.get("chest")
        _default_legs = casual.get("legs")
        _default_panties = casual.get("panties")

        if _chosen_pose in ("titjob",):
            # Titjob: always topless, keep bottom
            store._photo_over = None
            store._photo_chest = None
            store._photo_legs = _default_legs
            store._photo_panties = _default_panties
        elif _chosen_pose in ("reverse_cowgirl", "cowgirl"):
            # Action poses: topless, bottomless or panties down
            store._photo_over = None
            store._photo_chest = None
            store._photo_legs = None
            if _inbt >= 500:
                store._photo_panties = None
            else:
                store._photo_panties = _default_panties
        else:
            # Standing: clothing based on Inbt tier
            if _inbt >= 600:
                # Fully nude
                store._photo_over = None
                store._photo_chest = None
                store._photo_legs = None
                store._photo_panties = None
            elif _inbt >= 450:
                # Topless
                store._photo_over = None
                store._photo_chest = None
                store._photo_legs = _default_legs
                store._photo_panties = _default_panties
            elif _inbt >= 300:
                # No over, chest visible
                store._photo_over = None
                store._photo_chest = _default_chest
                store._photo_legs = _default_legs
                store._photo_panties = _default_panties
            elif _inbt >= 150:
                # Casual but maybe no over
                if renpy.random.random() < 0.5:
                    store._photo_over = None
                else:
                    store._photo_over = _default_over
                store._photo_chest = _default_chest
                store._photo_legs = _default_legs
                store._photo_panties = _default_panties
            else:
                # Full clothes
                store._photo_over = _default_over
                store._photo_chest = _default_chest
                store._photo_legs = _default_legs
                store._photo_panties = _default_panties

        # Trait overrides for clothing
        if girl.has_trait("camera_lover") and _inbt >= 200:
            # camera_lover tends to show more
            if store._photo_over and _inbt >= 200:
                store._photo_over = None
            if store._photo_chest and _inbt >= 300:
                store._photo_chest = None

        if girl.has_trait("public_fetish") and _inbt >= 250:
            # public_fetish: if she's in public, she's bolder
            _loc = getattr(girl, "loc", "room")
            if _is_public_location(_loc):
                if store._photo_over:
                    store._photo_over = None

        if girl.has_trait("cute_sex"):
            # cute_sex: never fully nude unless very high Inbt
            if _inbt < 550:
                if store._photo_chest is None and store._photo_panties is None:
                    store._photo_panties = _default_panties

        if girl.has_trait("loyal") and girl.has_npc_partner():
            # loyal with bf: more conservative
            if _inbt < 400:
                store._photo_over = store._photo_over or _default_over
                store._photo_chest = store._photo_chest or _default_chest

        # --- EXPRESSION SELECTION ---

        if _chosen_pose in ("reverse_cowgirl", "cowgirl"):
            _expr_pool = ["oh", "manic", "smile"]
            if girl.has_trait("cute_sex"):
                _expr_pool = ["shy", "oh", "surprised"]
            elif girl.has_trait("hardcore_sex"):
                _expr_pool = ["manic", "sly", "oh"]
        elif _chosen_pose == "titjob":
            _expr_pool = ["sly", "smile", "oh"]
            if girl.has_trait("cute_sex"):
                _expr_pool = ["shy", "smile", "surprised"]
        else:
            # Standing
            _topless = store._photo_chest is None and store._photo_over is None
            _nude = _topless and store._photo_panties is None

            if _nude:
                _expr_pool = ["sly", "shy", "oh"]
                if girl.has_trait("camera_lover"):
                    _expr_pool = ["smile", "sly", "manic"]
                elif girl.has_trait("cute_sex"):
                    _expr_pool = ["shy", "sad", "surprised"]
                elif girl.has_trait("hardcore_sex"):
                    _expr_pool = ["sly", "manic", "smile"]
            elif _topless:
                _expr_pool = ["smile", "shy", "sly"]
                if girl.has_trait("cute_sex"):
                    _expr_pool = ["shy", "surprised", "smile"]
            else:
                _expr_pool = ["smile", "normal", "sly"]
                if girl.has_trait("cute_sex"):
                    _expr_pool = ["smile", "shy", "normal"]
                elif girl.has_trait("camera_lover"):
                    _expr_pool = ["smile", "sly", "manic"]

        store._photo_expression = _tl(renpy.random.choice(_expr_pool))

        return {"accepted": True, "reason": "normal"}

    def _photo_bg_for_girl(girl):
        """Get the background image path for the girl's current location."""
        loc = getattr(girl, "loc", "room")
        return _LOC_TO_BG.get(loc, "images/bg/Playerroom.png")

    def _photo_build_image_name(girl):
        """
        Build the full layeredimage name for the photo preview.
        Temporarily applies the decided clothing/expression to the girl,
        builds the attributes, then restores.
        """
        # Save real state
        _real_over = girl.Over
        _real_chest = girl.Chest
        _real_legs = girl.Legs
        _real_panties = girl.Panties

        # Apply photo state
        girl.Over = store._photo_over
        girl.Chest = store._photo_chest
        girl.Legs = store._photo_legs
        girl.Panties = store._photo_panties

        # Apply expression
        expr = store._photo_expression or "smile"
        _pose = store._photo_pose or "standing"
        expr_data = get_expression(expr, pose=_pose, gid=girl.Id)
        state = sprite_state.setdefault(girl.Id, {})
        state["brows"] = expr_data.get("brows", "brows_normal")
        state["eyes"] = expr_data.get("eyes", "eyes_normal")
        state["mouth"] = expr_data.get("mouth", "mouth_normal")

        # Build using the decided pose
        _pose = store._photo_pose or "standing"
        attrs = _build_attributes_for_girl(girl, _pose)
        img_name = "%s %s" % (girl.Id, _pose)
        if attrs:
            img_name += " " + " ".join(attrs)

        # Restore real state
        girl.Over = _real_over
        girl.Chest = _real_chest
        girl.Legs = _real_legs
        girl.Panties = _real_panties

        return img_name

    # ----------------------------------------------------------
    # Reaction lines
    # ----------------------------------------------------------
    _PHOTO_ACCEPT_LINES = {
        "camera_lover": {
            "standing_clothed": [
                _("Here~ Just a casual one for now."),
                _("You asked, so here you go. Looking good, right?"),
            ],
            "standing_topless": [
                _("Since you asked so nicely... enjoy the view."),
                _("A little something for your eyes only~"),
                _("Don't screenshot this... just kidding, I know you will."),
            ],
            "standing_nude": [
                _("The full package, just for you. You're welcome."),
                _("No filter, no clothes, no shame~ Here."),
                _("I hope your phone is secure, because this one is HOT."),
            ],
            "titjob": [
                _("Remember these? Here's a reminder."),
                _("Thought you'd appreciate this angle~"),
            ],
            "reverse_cowgirl": [
                _("Missing the view? Here it is again."),
                _("This angle is your favorite, isn't it?"),
            ],
            "cowgirl": [
                _("Remember when I was on top? Here's a preview for next time."),
                _("This pose always gets your attention~"),
            ],
        },
        "cute_sex": {
            "standing_clothed": [
                _("H-Here. It's just a normal photo. Don't read into it."),
                _("You wanted a photo? Fine... but don't share it!"),
            ],
            "standing_topless": [
                _("I can't believe I'm sending this... please don't show anyone."),
                _("This is SO embarrassing... here. Happy now?"),
                _("My heart is pounding just taking this... here."),
            ],
            "standing_nude": [
                _("Oh my god, I actually did it... PLEASE delete this if we ever stop talking."),
                _("I've never sent something like this before... be gentle with it."),
            ],
            "titjob": [
                _("You really want a photo like this? ...Fine. Just for you."),
                _("This is so embarrassing but... I kind of liked taking it."),
            ],
            "reverse_cowgirl": [
                _("I can't believe you want THIS kind of photo... h-here."),
                _("Don't you dare show this to anyone. EVER."),
            ],
            "cowgirl": [
                _("Remembering that makes me blush so much... here."),
                _("I took like ten tries because I kept getting too shy..."),
            ],
        },
        "cheater": {
            "standing_clothed": [
                _("Quick one before my {hint}%(pl)s{/hint} notices. Here."),

                _("Don't tell %(po)s I'm sending you photos. Here."),
            ],
            "standing_topless": [
                _("My {hint}%(pl)s{/hint} would lose it if %(pp)s saw this. Enjoy."),

                _("This stays between us. %(Pp)s can't know."),
            ],
            "standing_nude": [
                _("If %(pp)s ever finds this on your phone, we're both dead. Worth it though."),
                _("Full nude. My {hint}%(pl)s{/hint} has never gotten one of these. You're special."),

            ],
            "titjob": [
                _("%(Pp)s doesn't know I do this for you. Makes it hotter."),
                _("A secret photo for my secret... whatever you are."),
            ],
            "reverse_cowgirl": [
                _("My {hint}%(pl)s{/hint} would never ask for something like this. You're different."),

                _("Sending this from %(poss)s apartment. Living dangerously."),
            ],
            "cowgirl": [
                _("Took this thinking about last time. My {hint}%(pl)s{/hint} was in the next room."),

                _("This one's spicy. Don't get caught with it."),
            ],
        },
        "loyal": {
            "standing_clothed": [
                _("I shouldn't be sending you photos... but here."),
                _("Just a normal photo. Nothing wrong with that... right?"),
            ],
            "standing_topless": [
                _("I can't believe I'm doing this. My {hint}%(pl)s{/hint} would be devastated."),

                _("This is insane. I have a {hint}%(pl)s{/hint} and I'm sending you THIS."),

                _("What is wrong with me... here. Before I change my mind."),
            ],
            "standing_nude": [
                _("I've completely lost my mind. A nude? For YOU? While I have a {hint}%(pl)s{/hint}?"),

                _("This is the craziest thing I've ever done. My body won't listen to reason."),
            ],
            "titjob": [
                _("My {hint}%(pl)s{/hint} has never seen a photo like this from me. And here I am sending one to you."),

                _("I'm supposed to be faithful and I'm sending you THIS. I've lost it."),
            ],
            "reverse_cowgirl": [
                _("This is madness. I'm in a relationship and sending you photos like this."),
                _("%(Pp)s trusts me completely and I'm... ugh. Here. Take it."),
            ],
            "cowgirl": [
                _("%(Pp)s thinks I'm the loyal one. If %(pp)s could see what I'm sending you right now..."),
                _("I can't stop. I know it's wrong but I NEED you to see this."),
            ],
        },
        "hardcore_sex": {
            "standing_clothed": [
                _("Here. Nothing fancy. You want more, you earn it."),
                _("A quick one. Don't expect me to pose all day."),
            ],
            "standing_topless": [
                _("Enjoy the view. I know I look good."),
                _("Here. And yes, they're real."),
            ],
            "standing_nude": [
                _("Full nude. No shame. You wanted it, you got it."),
                _("Here. Now stop asking and come see the real thing."),
            ],
            "titjob": [
                _("Here. A reminder of what's waiting for you."),
                _("Next time, fuck them hard. I want them red after."),
            ],
            "reverse_cowgirl": [
                _("This angle. You know what to do with it."),
                _("Come handle this in person. The photo is just a teaser."),
            ],
            "cowgirl": [
                _("Here. Miss me yet?"),
                _("Next time I'm on top, I'm riding you as hard as I can."),
            ],
        },
        # telling him how to perform is femdom (docs/plan_femdom.md D3); a photo key missing here falls to her next trait
        "femdom": {
            "cowgirl": [
                _("Next time I'm on top, you better last longer."),
                _("Remember this view. Next time you stay on your back until I say you're done."),
                _("This is where I'm sitting tonight. On you. No arguments."),
            ],
        },
        # being used is submissive (docs/plan_femdom.md D3)
        "submissive": {
            "titjob": [
                _("You like these? Come use them properly next time."),
                _("Here. Tell me how you want them next time and I'll do exactly that."),
                _("These are yours to use. I just wanted you to know."),
            ],
        },
        "public_fetish": {
            "standing_clothed": [
                _("Took this right here where someone could see. Thrilling."),
                _("Anyone could have walked by while I was posing for this."),
            ],
            "standing_topless": [
                _("Topless in a semi-public spot. My heart is racing."),
                _("If someone catches me taking this... that kind of makes it better."),
            ],
            "standing_nude": [
                _("Fully nude, right here. The risk makes it so much hotter."),
                _("Someone almost saw me taking this. I almost wanted them to."),
            ],
            "titjob": [
                _("Took this where anyone could see. Imagine if they did."),
                _("The thrill of posing like this out here..."),
            ],
            "reverse_cowgirl": [
                _("This pose, in this location? If someone walks in..."),
                _("The danger of getting caught makes this photo ten times better."),
            ],
            "cowgirl": [
                _("Imagine someone seeing me pose like this right now."),
                _("Public and provocative. Just how I like it."),
            ],
        },
        "_default": {
            "standing_clothed": [
                _("Here, I just took this for you."),
                _("Nothing too wild. Just me. Here."),
            ],
            "standing_topless": [
                _("Here... don't go showing this around."),
                _("A little more than usual. Just for you."),
            ],
            "standing_nude": [
                _("I can't believe I'm sending this. Here."),
                _("Full photo. Keep it safe. And private."),
            ],
            "titjob": [
                _("You really liked this, didn't you? Here's a reminder."),
                _("Took this one for you. Enjoy."),
            ],
            "reverse_cowgirl": [
                _("Since you liked the view so much last time... here."),
                _("This one's for your eyes only."),
            ],
            "cowgirl": [
                _("Remember this? Here's your souvenir."),
                _("Next time won't just be a photo."),
            ],
        },
    }

    _PHOTO_DENY_LINES = {
        "camera_hater": [
            _("No. Absolutely not. I hate having my photo taken."),
            _("Are you serious? No photos. Ever."),
            _("Delete whatever you're thinking. No pictures."),
        ],
        "low_love": [
            _("Why would I send YOU a photo?"),
            _("I don't know you well enough for that."),
            _("No. We're not that close."),
        ],
        "low_inbt": [
            _("I don't think so. Not right now."),
            _("Maybe another time. Not feeling it."),
            _("Nah. Ask me when I'm in a better mood."),
        ],
    }

    def _photo_get_line_key():
        """Determine the line key based on pose and clothing."""
        _pose = store._photo_pose
        if _pose != "standing":
            return _pose

        _topless = store._photo_chest is None and store._photo_over is None
        _nude = _topless and store._photo_panties is None and store._photo_legs is None

        if _nude:
            return "standing_nude"
        elif _topless:
            return "standing_topless"
        else:
            return "standing_clothed"

    def _photo_get_accept_line(girl):
        _key = _photo_get_line_key()
        _line = None
        for _t in ("camera_lover", "cute_sex", "cheater", "loyal", "femdom", "submissive", "hardcore_sex", "public_fetish"):
            if girl.has_trait(_t):
                # "cheater" lines only make sense if she currently has a boyfriend
                if _t == "cheater" and not (hasattr(girl, "has_npc_partner") and girl.has_npc_partner()):
                    continue
                pool = _PHOTO_ACCEPT_LINES.get(_t, {}).get(_key)
                if pool:
                    _line = renpy.random.choice(pool)
                    break
        if _line is None:
            pool = _PHOTO_ACCEPT_LINES["_default"].get(_key)
            _line = renpy.random.choice(pool) if pool else _("Here you go.")
        return _format_partner_line(girl, _line)

    def _photo_get_deny_line(girl, reason):
        # Every return leaves here TRANSLATED: the phone caller feeds phone_add_msg raw (it never translates),
        # and a translated line through Say_Line is the rod_pick_line pattern everywhere else.
        if reason == "no_photos":
            # her own voice, girl -> role -> Global (the stepmom's "photo_never" pool): a permanent rule, not a step
            return rod_pick_line(girl, "photo_never")
        if reason == "story_locked":
            # her step's own voice (story_steps.rpy; the stepmom's cold pools have a "photo" key)
            return _tl(story_locked_line(girl, "photo"))
        pool = _PHOTO_DENY_LINES.get(reason)
        if pool:
            return _tl(renpy.random.choice(pool))
        return _tl(_("I don't think so."))

    def _photo_save(girl):
        """Save the photo to Player.received_photos."""
        loc = getattr(girl, "loc", "room")
        entry = {
            "girl_gid": girl.gid,
            "girl_name": girl.Name,
            "day": store.Day,
            "location": loc,
            "is_public": _is_public_location(loc),
            "pose": store._photo_pose,
            "expression": store._photo_expression,
            "over": store._photo_over,
            "chest": store._photo_chest,
            "legs": store._photo_legs,
            "panties": store._photo_panties,
        }
        if not hasattr(store.Player, "received_photos"):
            store.Player.received_photos = []
        store.Player.received_photos.append(entry)

# ============================================================
# PHOTO DISPLAY SCREEN (shows the received photo in the phone)
# ============================================================

transform _photo_standing_transform:
    anchor (0.5, 1.0)
    zoom 0.42
    xalign 0.5
    yalign 1.0

transform _photo_titjob_transform:
    anchor (0.5, 0.5)
    zoom 0.55
    xalign 0.5
    yalign 0.4

transform _photo_rcg_transform:
    anchor (0.5, 0.5)
    zoom 0.50
    xalign 0.5
    yalign 0.5

transform _photo_cowgirl_transform:
    anchor (0.5, 0.5)
    zoom 0.50
    xalign 0.5
    yalign 0.45

screen phone_show_photo(girl):

    modal True
    zorder 200

    # Dark overlay — click to dismiss
    button:
        xfill True
        yfill True
        background "#00000088"
        action Return()

    frame at phone_slide_in:
        xpos PH_X
        ypos PH_Y
        background None
        padding (0, 0)

        fixed:
            fit_first True

            # Phone frame (first = sets size)
            add _phone_img

            # Photo content (clipped to phone screen)
            viewport:
                xpos _PHONE_CONTENT_X
                ypos _PHONE_CONTENT_Y
                xsize _PHONE_CONTENT_W
                ysize _PHONE_CONTENT_H
                clipping True
                mousewheel False

                fixed:
                    xsize _PHONE_CONTENT_W
                    ysize _PHONE_CONTENT_H

                    # Background (location)
                    $ _photo_bg_path = _photo_bg_for_girl(girl)
                    add im.Scale(_photo_bg_path, _PHONE_CONTENT_W, _PHONE_CONTENT_H)

                    # Girl sprite with pose-appropriate transform
                    $ _photo_img = _photo_build_image_name(girl)
                    if store._photo_pose == "titjob":
                        add _photo_img at _photo_titjob_transform
                    elif store._photo_pose == "reverse_cowgirl":
                        add _photo_img at _photo_rcg_transform
                    elif store._photo_pose == "cowgirl":
                        add _photo_img at _photo_cowgirl_transform
                    else:
                        add _photo_img at _photo_standing_transform

            # Name overlay
            text "[girl.Name]":
                xpos _PHONE_CONTENT_X
                ypos _PHONE_CONTENT_Y + 4
                xsize _PHONE_CONTENT_W
                style "phone_text"
                size PH_FONT_SM
                color "#7dd3fc"
                text_align 0.5

            # Tap to close hint
            text _("Tap to close"):
                xpos _PHONE_CONTENT_X
                ypos _PHONE_CONTENT_Y + _PHONE_CONTENT_H - 28
                xsize _PHONE_CONTENT_W
                style "phone_text"
                size PH_FONT_XXS
                color "#ffffff66"
                text_align 0.5

# ============================================================
# PHOTO REQUEST LABEL — called from contact options
# ============================================================

label phone_request_photo(girl):

    # Girl decides what to send
    $ _approval = _photo_decide(girl)

    if _approval["accepted"]:
        # Save photo
        $ _photo_save(girl)

        # Show the photo in the phone
        call screen phone_show_photo(girl)

        # Acceptance line after viewing
        $ _accept_line = _photo_get_accept_line(girl)
        $ Say_Line(girl, _accept_line)

        # Stat gains
        $ Change_Status(girl, "Inbt", 3)
        if girl.has_trait("camera_lover"):
            $ Change_Status(girl, "Love", 3)

        # Exposure tracking
        if store._photo_chest is None and store._photo_over is None:
            $ girl.RegisterAction("photo_sent_topless")
        if store._photo_panties is None and store._photo_legs is None:
            $ girl.RegisterAction("photo_sent_bottomless")
        $ girl.RegisterAction("photo_sent")

    else:
        # Denial
        $ _deny_line = _photo_get_deny_line(girl, _approval["reason"])
        $ Say_Line(girl, _deny_line)

        if _approval["reason"] == "camera_hater":
            $ Change_Status(girl, "Love", -5)

    $ _phone_restore_others()
    return
