# ============================================================
# shion_rimjob_lines.rpy... Shion's voice in the rimjob (docs/plan_shion.md Fase 5)
#
# The act key is "rj" (Images/Core_Rimjob.rpy). She kneels behind him: her tongue on him, her hand on his cock.
# Before her step 2 she refuses it whatever her stats (STORY_LADDERS, story_steps.rpy: her step's line); from it
# her "hard_deny" / "offended" are the author's refusals, and his blackmail (the shared blackmail lines,
# _bm_act_lines "rj") can force it. From stage 2 her stats decide: "accepted_first" (the author's lines) the first time,
# "accepted" after (she gives in and hates how much), the deny tiers. Stage 3 = "<mood>.femdom_s3" (she is his).
# A stage line never claims a first time nor a history of this act. "{0}" in the pgf moods = his girlfriend.
#
# Part 1 merges into GIRL_SEX_LINES["shion"][mood]["rj"] (shion_sex_lines.rpy). Part 2 = SCENE_LINES pools
# "<key>.rj.shion" (moans, her orgasm, his cum in her hand / fired away) and their "femdom_s3" pools.
# ============================================================

init 2 python:

    SHION_RJ_SEX_LINES = {
        # the author's lines (College Traits - Development for Shion: "asks Shion for a rimjob, she agrees")
        "accepted_first": [
            _("You come to me with that request? Hmmph... you've grown bold."),
            _("You're lucky I find your audacity... slightly more interesting than irritating."),
            _("Fine... Lose the pants... If you tell a soul about this..."),
        ],
        "accepted": [
            _("Again? ...Fine. Turn around before I change my mind."),
            _("Don't you dare look back at me while I do this."),
            _("Hmmph. Stop grinning, boy. Turn around and shut up."),
        ],
        "accepted.femdom_s3": [
            _("Turn around, my boy. Let me take care of you."),
            _("Your father would never dare ask me for this. You? You only have to say it."),
            _("Pants off. Now. I've been thinking about this all day."),
        ],
        # the author's refusals ("she refuses")
        "offended": [
            _("You want me to put my tongue on your filthy shithole? Get the fuck out of my sight."),
            _("You have some nerve, little bastard. Crawling to me with that request."),
            _("You haven't even earned my hand, and you ask me for THAT? Pathetic."),
        ],
        "hard_deny": [
            _("Ah... ahh... you really thought I'd say yes? Cute. Now get out before I decide your punishment."),
            _("You want me to put my tongue on your filthy shithole? Get the fuck out of my sight."),
            _("You have some nerve, little bastard. Crawling to me with that request."),
        ],
        "soft_deny": [
            _("Not today. Don't push your luck, boy."),
            _("No. I'm not in the mood to kneel for anyone."),
            _("Maybe. When you've earned it. You haven't."),
        ],
        "tempted_deny": [
            _("Don't look at me like that... Not now."),
            _("God, the things you ask me for... No. Not tonight."),
            _("I'm not saying never. I'm saying not now."),
        ],
        "cracking": [
            _("Stop asking... I can feel myself wanting to say yes, and I hate it."),
            _("One more word and I'll... no. No. Not yet."),
            _("You little bastard... you know exactly what you're doing to me. Not yet."),
        ],
        "breaking": [
            _("Next time. Don't make me say it twice."),
            _("I'm this close to dropping to my knees... Not today. Soon."),
            _("Soon, boy. When I decide. And I'm deciding faster than I'd like."),
        ],
        "soft_deny.femdom_s3": [
            _("Not now. I want to, believe me. Just not now."),
            _("Later, my boy. I'll make it worth the wait."),
        ],
        "tempted_deny.femdom_s3": [
            _("Mmm... you're cruel. Ask me again tonight."),
            _("Don't tempt me... if I start now, I won't stop."),
        ],
        # he has a girlfriend (the author's line first)
        "pgf_accepted": [
            _("Tsk... I suppose your whore hasn't been taking good care of you then... fine..."),
            _("Does {0} know what you ask of your stepmother? ...Turn around."),
        ],
        "pgf_denied": [
            _("Disgusting... Ask your fucking whore to do that for you... Bastard."),
            _("Go ask {0}. Let's see if she loves you that much."),
        ],
        "pgf_accepted.femdom_s3": [
            _("{0} would never do this for you. I will. Remember that."),
            _("Turn around. Let me show you what that girl will never give you."),
        ],
        "pgf_denied.femdom_s3": [
            _("Not today. Spend it on {0}... if she even knows how."),
        ],
    }

    def _shion_rj_merge():
        _tbl = GIRL_SEX_LINES.setdefault("shion", {})
        for _mood, _lines in SHION_RJ_SEX_LINES.items():
            _tbl.setdefault(_mood, {})["rj"] = _lines

    _shion_rj_merge()

    SCENE_LINES.update({
        # her moans: her face is in him (head 2) or just pulled back (head 1), so short and muffled
        "moan.speed1.rj.shion": [
            _("Mmmph..."),
            _("Hmmph... don't you dare move."),
            _("Mmh... you taste like sweat and bad decisions."),
        ],
        "moan.speed2.rj.shion": [
            _("Mmph... mmph..."),
            _("Ngh... stay still, you little..."),
            _("Hah... if your father ever..."),
        ],
        "moan.speed3.rj.shion": [
            _("Mmmph! Mmph!"),
            _("Hah... hah... you're throbbing in my hand..."),
            _("Ngh... fuck... fuck..."),
        ],
        "moan.speed1.rj.shion.femdom_s3": [
            _("Mmm... my boy..."),
            _("Relax. I've got you."),
        ],
        "moan.speed2.rj.shion.femdom_s3": [
            _("Mmph... you like that? Your father never got this."),
            _("Hah... tell me it's good..."),
        ],
        "moan.speed3.rj.shion.femdom_s3": [
            _("Mmph... give it to me... in my hand..."),
            _("Hah... come for me, my boy..."),
        ],
        # her orgasm (she touches herself with her free hand, out of sight)
        "girl_cum.rj.shion": [
            _("Ngh...! Don't... don't you dare turn around...!"),
            _("Hah... hah... I came from... from THIS? Fuck..."),
            _("Mmmph...! Fuck... fuck..."),
        ],
        "girl_post_cum.rj.shion": [
            _("Not. One. Word."),
            _("...If you ever tell anyone what just happened, I'll bury you."),
        ],
        "girl_cum.rj.shion.femdom_s3": [
            _("Hah... ahh... only you could make me cum like this..."),
            _("Fuck... I'm cumming with my face buried in you... what have you done to me..."),
        ],
        # his cum: in her hand / fired away (PlayerCumMenu_Hand)
        "cum_hand.rj.shion": [
            _("All over my hand... Hmmph. Look at the mess you made."),
            _("Tsk. My manicure. You'll pay for that."),
            _("There. Satisfied? Hand me a tissue, boy."),
        ],
        "cum_away.rj.shion": [
            _("On the floor? You'll clean that up yourself."),
            _("Hmmph. At least you didn't make a mess of me."),
        ],
        "cum_hand.rj.shion.femdom_s3": [
            _("Mmm... all for me. Good boy."),
            _("Look at that... all over my hand. Good boy."),
        ],
    })
