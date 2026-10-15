# ============================================================
# shion_sex_lines.rpy... Shion's own voice in the sex menu and inside the scenes
# (docs/plan_shion.md, Fase 2 items 6 and 7)
# ============================================================
#
# Her voice: the player's stepmother, married to his father. Cold, contemptuous, narcissistic, possessive. She
# calls him "boy" / "little bastard" / "you little shit", talks like a CEO ("results", "I don't reward
# mediocrity") and threatens more than she asks. Before a scene she is ALWAYS in charge: she allows, or she refuses
# with contempt. Inside a scene she slips (the author's canon lines below), and only her hardest orgasm
# (girl_cum_hard) gets the fully broken "This pussy belongs to you now".
# Her femdom ORDERS (pace, "don't cum yet", where to cum, "me first", take over...) live in femdom_lines_shion.rpy:
# nothing here repeats those moments.
# Traits she always has: experienced, femdom, married, rich. experienced makes her a veteran of every eager trait
# from the start (trait_is_new is False), so there are no "_first" / "_new" pools here.
#
# Her TURN (Actions/femdom_turn.rpy): everything above the "HER TURN" marks is her voice BEFORE it (stages 0-1).
# femdom_stage_mod(girl) = "femdom_s2" / "femdom_s3" is her stage modifier, and it comes FIRST:
#   - stage 2: she is giving in to him and hates how much she wants it ("accepted.femdom_s2"; her other moods and
#     her scenes stay the before voice).
#   - stage 3: she is his, behind his father's back. Proud, possessive, filthy in bed, her cruel tongue intact, few
#     orders; she calls him "my boy". A no is about the risk or her mood, never that he doesn't deserve her.
#     Moods "accepted.femdom_s3", "soft_deny.femdom_s3", "tempted_deny.femdom_s3", "pgf_accepted.femdom_s3",
#     "pgf_denied.femdom_s3" and the scene pools "<key>.<scene>.shion.femdom_s3". (Her hard_deny / cracking / breaking
#     and her other scene moments keep the before voice.)
#   A stage line is about her and him NOW: it never claims a first time, nor a history of one act (she can reach a
#   stage without having done every act).
#
# ── Part 1: the sex menu (GIRL_SEX_LINES["shion"], read by girl_sex_voice_line in Chat/interactions.rpy) ──
# Moods: "accepted", "accepted_first" (first time she does that act with him), "offended", _DENY_TIERS (hard_deny,
# soft_deny, tempted_deny, cracking, breaking), "pgf_accepted" / "pgf_denied" (he has a girlfriend: "{0}" = her
# name), and "<mood>.femdom" (beats the shared TRAIT_SINGLE_LINES["femdom"]).
# Acts: kiss, masturbate (she touches herself, he watches), hj, tj, bj, sex, anal, oral (HE eats HER out).
# No fj: she has no footjob art. "flirt" only in the pgf moods (Flirty.rpy asks _player_gf_sex_line for it).
# Slots left out on purpose (they can never play):
#   - accepted / accepted_first hj and bj: femdom is canon (and canon-locked in check_corruption), so
#     "accepted.femdom" always answers first, and the first-time check only runs for the plain "accepted" mood.
#     Her femdom hj / bj lines therefore never claim a first time or a repeat.
#   - hard_deny sex and hj: "hard_deny.femdom" always answers first.
#   - offended kiss / masturbate / hj / oral: sex_denial_line only goes "offended" when the act is 4+ intimacy ranks
#     above anything done (INTIMACY_RANK); those four ranks (0 / 1 / 2 / 1) can never be.
#   What "offended" says is TRUE by that same rank rule: tj = nothing done yet (not even a kiss), bj = no handjob
#   yet, sex = no handjob yet, anal = no sex yet.
#
# ── Part 2: her voice inside the scenes (SCENE_LINES, read by scene_pick_line in scene_lines.rpy) ──
# Her gid is the FIRST modifier, and the pose beats the modifiers, so every pool here is "<key>.<scene>.shion"
# (step 2 of the picker: only a 2-modifier pool of the same pose outranks it). The scene is the LINE scene:
# reverse_cowgirl reads "cowgirl" (_SCENE_LINE_ALIAS), doggy anal is "anal". "doggy" has no pools of its own:
# "<key>.doggy.shion" is still asked by the picker, so it only plays in doggy (never in oral / rub / tip).
# The only pools without a scene are the catch-alls whose event has no scene pool at all (girl_cum_intense,
# girl_post_cum_intense, cum_inside_consented / cum_inside_forced for the vaginal poses, cum_mouth_accepted); their
# lines are true in every pose (the intense ones even when she is alone: secret masturbation, shower).
# Moments, heard most first: the moans (every sex tick rolls one), her orgasm (girl_cum / _intense / _hard) and what
# she says right after it, then his cum (inside with or without her permission, mouth, face).
# "<key>.<scene>.shion.player_cheating" = he has a girlfriend (the "player_cheating" modifier): the only pools that
# talk about her (at stage 3 her "<key>.<scene>.shion.femdom_s3" pools come first: _detect_line_modifiers puts the
# stage right after her gid, so they never talk about the girlfriend).
# "<key>.<scene>.shion.femdom_s3" (her stage 3, step 1 of the picker: the first candidate of all); where her before
# pool has no scene, "<key>.shion.femdom_s3" (step 4: it beats "<key>.shion", and only a pool of the scene outranks it,
# exactly as for the before pool). "cum_inside_forced.shion.cum_slut" = the forced creampie a cum_slut liked anyway (Cum.rpy
# _cream_liked_line reads the forced key for it).
# Her anal lines never say she loves or hates it (anal_lover / anal_hater can roll), her cum lines never say she
# loves or hates cum (cum_slut / hate_cum can roll).
# ============================================================

init 1 python:

    GIRL_SEX_LINES["shion"] = {

        # ══════════════════════════════════════════════════════════
        #  ACCEPTED
        # ══════════════════════════════════════════════════════════
        "accepted": {
            "kiss": [
                _("One kiss. Don't make it clumsy, and don't make it mean anything."),
                _("Hmmph. Come here, then. And wipe that stupid grin off your face first."),
                _("Fine. Quickly, before I remember whose son you are."),
            ],
            "masturbate": [
                _("You want a show? Watch, then. And keep your hands to yourself."),
                _("Fine. Look all you like, boy. Looking is all you get."),
                _("Sit down and watch how a woman does it. Take notes."),
            ],
            "tj": [
                _("You're lucky I'm in a generous mood. Sit down."),
                _("Fine. Stay still and appreciate what you're being given."),
                _("Hmmph. Eyes on me, boy. I want to see your face while I do this."),
            ],
            "sex": [
                _("You're lucky I find your audacity... slightly more interesting than irritating."),
                _("Fine. But understand this, boy: I'm the one taking you, not the other way around."),
                _("Hmmph. Very well. Try to be worth the risk I'm taking."),
            ],
            "anal": [
                _("Fine. Slowly. The moment I say stop, you stop."),
                _("Of all the things you could ask of me... fine. Don't make me regret it, boy."),
                _("Hmmph. You've earned a little indulgence. A little. Don't waste it."),
            ],
            "oral": [
                _("Finally, a request I approve of. Get down there, boy."),
                _("Down you go. And you don't stop until I tell you to."),
                _("Use that mouth for something useful for once."),
            ],
        },

        # First time she does this act with him (she is experienced: first with HIM, never "my first time")
        "accepted_first": {
            "kiss": [
                _("So you finally worked up the nerve. Hmmph. Come here."),
                _("Your father kisses like he files his taxes. Let's see if you're any better."),
                _("One kiss. If you tell anyone, I'll deny it, and they'll believe me."),
            ],
            "masturbate": [
                _("You want to watch me? How bold. Sit, and don't you dare touch yourself."),
                _("Consider this a privilege, boy. Very few men have earned a seat for this."),
                _("Fine. Watch closely. And not a word of this to anyone."),
            ],
            "tj": [
                _("You want these? Of course you do. Sit down."),
                _("Hmmph. A privilege most men only dream about. Stay still."),
                _("Fine. And don't you dare get any ideas about what this means."),
            ],
            "sex": [
                _("So it comes to this. Fine. And not a word to your father."),
                _("Hmmph. Look at you, finally brave enough to ask. Fine."),
                _("Don't look so shocked that I said yes. I'm the one taking you, boy. Remember that."),
            ],
            "anal": [
                _("You come to me with that request? Hmmph... you've grown bold."),
                _("My ass? You really have no shame. ...Fine. Slowly, you animal."),
                _("Hmmph. Bold. I'll allow it. And once you're in, you do exactly as I say."),
            ],
            "oral": [
                _("Finally, a request that makes sense. Get down there, and don't disappoint me."),
                _("You want to taste me? Good answer. Down you go."),
                _("Let's see if that mouth is good for more than talking back."),
            ],
        },

        # Femdom is canon: these replace the shared TRAIT_SINGLE_LINES["femdom"] (first time AND repeats)
        "accepted.femdom": {
            "hj": [
                _("Fine... lose the pants... if you tell a soul about this..."),
                _("Sit back and keep your hands to yourself. My hand, my pace."),
                _("Hmmph. Look at me while I do this. I want to watch you fall apart."),
            ],
            "bj": [
                _("Stay still. Don't you dare touch my hair. I set the pace, boy."),
                _("Fine. Keep your hands to yourself, and enjoy what you'll never deserve."),
                _("Hmmph. You'll take it exactly the way I give it, and you'll thank me."),
            ],
        },

        # ══════════════════════════════════════════════════════════
        #  OFFENDED: he skipped far ahead (only tj / bj / sex / anal can get here)
        # ══════════════════════════════════════════════════════════
        "offended": {
            "tj": [
                _("You haven't so much as kissed me, and you ask for THAT? Know your place, boy."),
                _("Excuse me? You skip every step and expect a reward? That's not how I do business."),
                _("The audacity. Ask me something like that again and you'll regret it."),
            ],
            "bj": [
                _("My mouth? You haven't even earned my hand, you little bastard."),
                _("You have some nerve, little bastard. Crawling to me with that request."),
                _("Do you have any idea who you're talking to? Get that thought out of your head."),
            ],
            "sex": [
                _("You haven't even had my hands, and you want my body? Pathetic."),
                _("Excuse me? I'm married to your father. Say that again and I'll make you regret it."),
                _("Do you hear yourself? Skipping straight to that? Get out of my sight."),
            ],
            "anal": [
                _("You haven't even had my pussy, and you ask for my ass? You've lost your mind."),
                _("That? From you? Crawl back to wherever you found the courage, boy."),
                _("Disgusting. Ask me that again and your father hears about it."),
            ],
        },

        # ══════════════════════════════════════════════════════════
        #  DENIALS, from coldest to hottest (_DENY_TIERS). She stays in charge even when she is close.
        # ══════════════════════════════════════════════════════════
        "hard_deny": {
            "kiss": [
                _("Kiss you? Don't be ridiculous."),
                _("No. Go wipe that look off your face."),
                _("I'm your stepmother, boy. Remember that before you embarrass yourself further."),
            ],
            "masturbate": [
                _("A show? For you? You couldn't afford the ticket."),
                _("No. What I do in private is none of your business."),
                _("Absolutely not. Go back to your homework."),
            ],
            "tj": [
                _("No. Keep your eyes off my chest, boy."),
                _("You're not getting anywhere near these."),
                _("No. Ask me again and see what happens."),
            ],
            "bj": [
                _("My mouth? On you? Not in this lifetime."),
                _("No. I don't hand out rewards for nothing, boy."),
                _("Don't insult me. The answer is no."),
            ],
            "anal": [
                _("Don't even think about it. Get that idea out of your head."),
                _("My ass? For you? You must have hit your head, boy."),
                _("No. Ask again, and you'll find out what my punishments look like."),
            ],
            "oral": [
                _("Your mouth anywhere near me? I don't think so."),
                _("No. You haven't earned the privilege."),
                _("Not today. Maybe when you learn some manners."),
            ],
        },

        # Femdom is canon: these replace the shared TRAIT_SINGLE_LINES["femdom"]
        "hard_deny.femdom": {
            "sex": [
                _("Ah... ahh... you really thought I'd say yes? Cute. Now get out before I decide your punishment."),
                _("No. You don't get my body because you asked. You get it when I decide."),
                _("Not happening. I choose who gets me, boy, and today it isn't you."),
            ],
            "hj": [
                _("My hand is a reward. You haven't produced a single result worth one."),
                _("No. You'll get my hand when I feel like giving it, not when you beg."),
                _("Beg all you want. The answer is no, and I enjoy saying it."),
            ],
        },

        "soft_deny": {
            "kiss": [
                _("Not now. Don't sulk, it's unattractive."),
                _("Hmmph. Maybe. When I feel like it."),
                _("Not yet. You'll know when I want to be kissed."),
            ],
            "masturbate": [
                _("Not now. Maybe if you behave."),
                _("You'd like that, wouldn't you? Not yet."),
                _("Maybe someday. Keep hoping, it's cute."),
            ],
            "hj": [
                _("Not yet. Show me you're worth my time first."),
                _("Maybe. When you've earned it. You haven't."),
                _("Patience, boy. I haven't decided you deserve it."),
            ],
            "tj": [
                _("Not yet. Keep dreaming about them."),
                _("Hmmph. You've barely earned a look, let alone that."),
                _("Not now. Ask me again when I'm in a better mood."),
            ],
            "bj": [
                _("Not yet. You haven't earned my mouth."),
                _("Hmmph. That's a lot to ask of a woman like me. Not today."),
                _("Maybe. Someday. If you're very, very good."),
            ],
            "sex": [
                _("Not yet. I haven't decided if you're worth the risk."),
                _("Hmmph. Don't rush me, boy. I set the timeline."),
                _("Not today. Keep trying, it's entertaining."),
            ],
            "anal": [
                _("Not yet. You're getting ahead of yourself."),
                _("Hmmph. That one you'll have to work much harder for."),
                _("No. Maybe when you've proven you can be trusted with it."),
            ],
            "oral": [
                _("Not yet. I don't let just anyone near me like that."),
                _("Maybe. When you've learned some patience."),
                _("Hmmph. Tempting. Still no."),
            ],
        },

        "tempted_deny": {
            "kiss": [
                _("Don't look at me like that... no. Not now."),
                _("I said no. Stop standing so close."),
                _("Hmmph. Ask me again later. Maybe I'll be less sensible."),
            ],
            "masturbate": [
                _("Don't tempt me... No. Not in front of you."),
                _("You'd enjoy that far too much. Which is exactly why not."),
                _("Hmmph... no. Not yet. Stop smiling."),
            ],
            "hj": [
                _("My hand is itching to... no. Not yet. Don't look so pleased."),
                _("You're making this annoying. The answer is still no."),
                _("Tsk... not now. And stop looking at me like you already won."),
            ],
            "tj": [
                _("You'd like that far too much. No. Not yet."),
                _("Stop staring at them. ...No. Not today."),
                _("Hmmph. Tempting, I admit. Still no."),
            ],
            "bj": [
                _("Don't give me that look... no. Not yet."),
                _("I know exactly what you want. And I'm still saying no."),
                _("Tsk. You're persistent, I'll give you that. Still no."),
            ],
            "sex": [
                _("Don't push me... I'm your stepmother, for God's sake. Not today."),
                _("You have no idea how close you... no. Get out of my face."),
                _("Tsk... ask me another day. When I'm less... sensible."),
            ],
            "anal": [
                _("Hmmph. I'm thinking about it. That's all you get today."),
                _("Don't smile. Thinking about it isn't a yes."),
                _("Not yet. But I'll admit you're persistent."),
            ],
            "oral": [
                _("Tempting... your mouth on me... no. Not yet."),
                _("Don't tempt me, boy. Not today."),
                _("Hmmph. You'd love that. Which is why you'll wait."),
            ],
        },

        "cracking": {
            "kiss": [
                _("Stop... one more word and I'll... no. Not yet."),
                _("Don't come any closer. I mean it. For now."),
                _("Tsk. You're getting under my skin, and I hate it. No."),
            ],
            "masturbate": [
                _("God, you're insufferable... no. Not yet. Almost."),
                _("Stop asking... I'm this close to showing you, and I hate that."),
                _("No... not yet. Don't you dare smirk at me."),
            ],
            "hj": [
                _("My hand was already reaching for... no. Not yet."),
                _("Tsk... one more push and I'll give in. Don't you dare push."),
                _("I'm almost tempted to... no. You'll wait, boy."),
            ],
            "tj": [
                _("Stop looking at them... God... no. Not yet."),
                _("Tsk. You're wearing me down. Not today... almost."),
                _("Ask me again, and I might forget who I am. Not now."),
            ],
            "bj": [
                _("Don't... I can almost taste... no. No. Not yet."),
                _("Tsk. I'm losing my patience with myself. Not today."),
                _("One more time and I'm... no. Get out of my sight before I change my mind."),
            ],
            "sex": [
                _("I'm married to your father... and I almost said yes. Get out. Now."),
                _("Don't touch me. If you touch me now... no. Don't."),
                _("Tsk... you little bastard... Not yet. Don't make me say it again."),
            ],
            "anal": [
                _("I can't believe I'm even considering... no. Not yet."),
                _("Stop... I'm thinking about it far too much. Not today."),
                _("Tsk. You're wearing me down, boy. Don't get used to it."),
            ],
            "oral": [
                _("Your mouth on me... God... no. Not yet."),
                _("Stop looking at me like that... I almost said yes."),
                _("Tsk... one more ask and I'll pull you down there myself. Not now."),
            ],
        },

        "breaking": {
            "kiss": [
                _("Next time you ask... I won't say no. Don't let it go to your head."),
                _("Not now... but soon. When I decide. And I've almost decided."),
                _("Get away from me before I kiss you myself."),
            ],
            "masturbate": [
                _("Next time. I'll decide when, and it will be soon. Now go."),
                _("I'm this close to letting you watch... no. Next time."),
                _("Tsk... don't ask again today. Tomorrow I might say yes."),
            ],
            "hj": [
                _("Next time I'll take you in my hand. Now leave me alone."),
                _("Don't ask again today. Tomorrow I won't be this sensible."),
                _("Almost... almost. Next time, and it'll be on my terms."),
            ],
            "tj": [
                _("Next time. Now get out before I change my mind."),
                _("Tsk... I'm about to give in, and I hate it. Next time."),
                _("Ask me again tomorrow. I doubt I'll refuse you."),
            ],
            "bj": [
                _("Next time you ask, I'll say yes. Now leave before I do it anyway."),
                _("God... not today. Tomorrow. And you'll thank me properly."),
                _("Tsk... my mouth is already watering. Next time. Go."),
            ],
            "sex": [
                _("Next time... next time I'll take you. On my terms. Now get out."),
                _("Don't push. I've already decided, boy. Just not today."),
                _("Tomorrow. And when I say yes, you'll do exactly as I say."),
            ],
            "anal": [
                _("Next time. Maybe. Don't make me say it twice."),
                _("Ask me again tomorrow... I don't think I'll refuse."),
                _("Tsk... you're this close to getting what you want. Not today."),
            ],
            "oral": [
                _("Next time I'll have you down there. Now go, before I do it today."),
                _("God... not now. Tomorrow. And you'll stay down there until I'm satisfied."),
                _("Almost. Next time you ask, I won't send you away."),
            ],
        },

        # ══════════════════════════════════════════════════════════
        #  HE HAS A GIRLFRIEND (_player_gf_sex_line): she despises her and pushes him to end it.
        #  "{0}" = the girlfriend's name.
        # ══════════════════════════════════════════════════════════
        "pgf_accepted": {
            "flirt": [
                _("Flirting with me while you have a girlfriend? Hmmph. Go on. I'm listening."),
                _("Tsk. Does {0} know how you talk to me? Continue."),
                _("Careful, boy. I'm far more interesting than she is, and you know it."),
            ],
            "kiss": [
                _("Tsk... I suppose your little girlfriend doesn't kiss you properly. Come here."),
                _("Kissing me when you have {0}? Hmmph. Come here."),
                _("Fine. Let's see if you still remember her name afterwards."),
            ],
            "masturbate": [
                _("Fine. Watch closely. I doubt {0} has ever given you a show like this."),
                _("Hmmph. Sit and watch, and forget that little girl for a while."),
                _("Fine. Look at a real woman for once."),
            ],
            "hj": [
                _("Tsk... I suppose your whore hasn't been taking good care of you then... fine..."),
                _("Fine. Let me show you what {0} can't do with her hands."),
                _("Hmmph. When I'm done, you'll wonder why you're still with her."),
            ],
            "tj": [
                _("Fine. I doubt that little girl of yours has anything worth putting there."),
                _("Tsk. Poor {0}. Sit down."),
                _("Hmmph. Sit. You can compare later, if you still remember her."),
            ],
            "bj": [
                _("Tsk... your little girlfriend isn't doing her job, is she? Stay still."),
                _("Fine. And afterwards, you'll think very hard about why you're still with {0}."),
                _("Hmmph. I'll show you what you've been settling for."),
            ],
            "sex": [
                _("Fine. But when I'm done with you, you'll end it with her. Understood?"),
                _("Tsk... {0} really can't satisfy you, can she? Fine."),
                _("Fine. And you'll dump that little whore, do you hear me?"),
            ],
            "anal": [
                _("Hmmph. So your little girlfriend isn't enough for you. Fine. Slowly."),
                _("Fine. Remember who gave you this, the next time you look at {0}."),
                _("Tsk... you want from me what you should be getting from her. Fine."),
            ],
            "oral": [
                _("Get down there. Let's see what that little girl has taught you."),
                _("Fine. And forget about {0} while you're down there."),
                _("Hmmph. At least you know which woman deserves it."),
            ],
        },

        "pgf_denied": {
            "flirt": [
                _("You have a girlfriend. Don't waste my time. Or better, get rid of her."),
                _("Flirting with me while you're with {0}? Pathetic."),
                _("Hmmph. Come back when you're single. Then we'll see how charming you are."),
            ],
            "kiss": [
                _("Kiss me? Go kiss your little girlfriend, bastard."),
                _("No. Go home to {0} and pretend you're happy."),
                _("Tsk. You have a girlfriend, and you come to me? Disgusting."),
            ],
            "masturbate": [
                _("Ask your girlfriend for a show. Oh, right. She's far too boring for that."),
                _("No. Go watch {0} if you're so desperate."),
                _("Hmmph. Not while you're still running around with that girl."),
            ],
            "hj": [
                _("No. Get rid of {0} first, then maybe we'll talk."),
                _("Tsk. Let your little girlfriend handle it. If she knows how."),
                _("My hand, while you still crawl back to her? No."),
            ],
            "tj": [
                _("No. Go stare at your girlfriend's chest instead."),
                _("Not while {0} is still in the picture."),
                _("Tsk. Ask her. I'm sure she'll disappoint you."),
            ],
            "bj": [
                _("Disgusting... ask your fucking whore to do that for you... bastard."),
                _("No. My mouth is not a consolation prize for a boy with a girlfriend."),
                _("Hmmph. Dump {0}, and then come back and ask me properly."),
            ],
            "sex": [
                _("You have a girlfriend, and you come to ME for that? No."),
                _("End it with {0}. Then we'll see."),
                _("Tsk. Go home to your little whore, bastard."),
            ],
            "anal": [
                _("Ask your girlfriend for that. Watch her say no, too."),
                _("No. And not while {0} is still around."),
                _("Disgusting. Go crawl back to her."),
            ],
            "oral": [
                _("Use that mouth on your girlfriend. Not on me. Not until she's gone."),
                _("No. Not while you still belong to {0}."),
                _("Tsk. Go please her. If she even lets you."),
            ],
        },

        # ══════════════════════════════════════════════════════════
        #  HER TURN, stage 2 (femdom_s2): she gives in, and hates how much she wants it
        # ══════════════════════════════════════════════════════════
        "accepted.femdom_s2": {
            "kiss": [
                _("Tsk... come here. And don't you dare look so pleased with yourself."),
                _("I hate that I was hoping you'd ask. Kiss me before I come to my senses."),
                _("Fine. God, what are you doing to me... come here."),
            ],
            "masturbate": [
                _("You want to watch? ...Fine. I was thinking about you anyway. Forget I said that."),
                _("Sit. Watch. And stop smiling, boy, I can feel it from here."),
                _("Hmmph... I shouldn't want you watching this much. Sit down before I change my mind."),
            ],
            "hj": [
                _("Give it here... Tsk. I've been wanting my hands on you, and I hate it."),
                _("Fine. Pants down. And stop looking at me like you've won something."),
                _("My hand is already reaching for you... tsk. Not one word, boy."),
            ],
            "tj": [
                _("Sit. I'm not doing this because you asked. I'm doing it because I want to, and that's worse."),
                _("Tsk. Stare all you like. I know you've been dreaming about these."),
                _("Hmmph... sit down. Why is it so hard to say no to you lately?"),
            ],
            "bj": [
                _("Don't touch my hair... or do. God, I don't even know anymore. Stand still."),
                _("Fine... my mouth is already watering. You didn't hear that."),
                _("Hmmph. I keep telling myself I'm still in charge. Stay still and let me believe it."),
            ],
            "sex": [
                _("Fine. Take me. ...I can't believe I just said that to you."),
                _("Tsk... I'm married to your father, and I want this more than I should. Come here."),
                _("Don't gloat. I'd say no if I could... I just can't seem to anymore."),
            ],
            "anal": [
                _("Fine... slowly. God, why do I keep saying yes to you?"),
                _("Not long ago I'd have slapped you for asking. Now look at me. Fine."),
                _("Hmmph... fine. Don't you dare mention how easily I gave in."),
            ],
            "oral": [
                _("Down you go... I've been thinking about your mouth more than I'd like to admit."),
                _("Fine. Get down there. And if I moan your name, you didn't hear it."),
                _("Tsk. Get down there before I start begging. I refuse to beg."),
            ],
        },

        # ══════════════════════════════════════════════════════════
        #  HER TURN, stage 3 (femdom_s3): she is his, behind his father's back
        # ══════════════════════════════════════════════════════════
        "accepted.femdom_s3": {
            "kiss": [
                _("Come here, my boy. Kiss me like you own me. You do."),
                _("Mmm. Your father gets a peck on the cheek. You get this."),
                _("You never have to ask for that anymore. Come here."),
            ],
            "masturbate": [
                _("You want a show? Sit. Every second of this is for you."),
                _("Watch closely, my boy. Your father has never seen me like this."),
                _("Hmmph. Sit down and enjoy it. I'll be thinking about you the whole time, and you'll know it."),
            ],
            "hj": [
                _("Give it to me. Mmm... this belongs in my hand, and you know it."),
                _("Lean back, my boy. Let me take care of what's mine."),
                _("Your father has to beg for this. You never do."),
            ],
            "tj": [
                _("Sit down. These are yours now. Try not to look so smug about it."),
                _("Your father gets to look at these. You get to use them."),
                _("Sit back, my boy, and enjoy what your father will never have again."),
            ],
            "bj": [
                _("Come here. Hands in my hair, if you want. I don't mind anymore."),
                _("On my knees for my husband's son. If the board could see me now... Mmm. Stand still."),
                _("Give it to me, boy. I want you in my mouth, and I'm done pretending I don't."),
            ],
            "sex": [
                _("Take me, my boy. This body stopped being your father's a while ago."),
                _("Come here. I want to feel you through my whole next board meeting."),
                _("You don't even have to ask anymore. ...Ask anyway. I like hearing it."),
            ],
            "anal": [
                _("My ass? Mmm... yes. Your father never even dared to ask."),
                _("Fine, my boy. Slowly at first... and then however you like."),
                _("Hmmph. Take it. Every part of me is yours now, that one too."),
            ],
            "oral": [
                _("Get down there, my boy. I've been thinking about your mouth all day."),
                _("Mmm. Your father never learned where to put his tongue. Show me you know better."),
                _("Yes. Use that clever mouth on something better than arguing with me."),
            ],
        },

        # Her no at stage 3: the risk or her mood, never that he doesn't deserve her
        "soft_deny.femdom_s3": {
            "kiss": [
                _("Later, my boy. I'm not in the mood to be careless today."),
                _("Not now. I've had a horrible day, and I'd bite your lip off."),
                _("Later. I'm still yours, I'm just not in the mood."),
            ],
            "masturbate": [
                _("Not today. I'm tired, and I don't perform when I'm tired."),
                _("Hmmph. Another time. I'm not in the mood to be watched."),
                _("Later, my boy. Today my head is full of board members, not you."),
            ],
            "hj": [
                _("Not right now. I'm in a foul mood, and my hand would be cruel to you."),
                _("Later, my boy. It's not that you don't deserve it. I just don't feel like it."),
                _("Hmmph. Ask me tomorrow. Today I'd rather strangle someone."),
            ],
            "tj": [
                _("Not now. I'm not in the mood, and for once it isn't your fault."),
                _("Later. I just had my hair done, and I'm not ruining it for anyone."),
                _("Hmmph. Not today, my boy. Try me again after a glass of wine."),
            ],
            "bj": [
                _("Not now. I'm in no mood to be on my knees for anyone today. Even you."),
                _("Later, my boy. My jaw still hurts from shouting at my staff."),
                _("Hmmph. Not today. Don't sulk, I'll make it up to you."),
            ],
            "sex": [
                _("Not today. Too risky. We get careless once, and your father finds out everything."),
                _("Later, my boy. I'm not in the mood, and I won't fake it. Not with you."),
                _("Hmmph. Not now. I want you, I just don't want it rushed and nervous."),
            ],
            "anal": [
                _("Not today. I'm not in the mood for that, so you'll wait like a good boy."),
                _("Hmmph. Another time. That one needs me in the right mood."),
                _("Later, my boy. Not today. Ask me again when I'm feeling wicked."),
            ],
            "oral": [
                _("Not now. I'm too wound up to relax, and I'd only snap at you."),
                _("Later. I don't want anyone between my legs today. Not even you."),
                _("Hmmph. Not today, my boy. Save that mouth for when I'm in a better mood."),
            ],
        },

        "tempted_deny.femdom_s3": {
            "kiss": [
                _("Don't... if I kiss you now, I won't stop, and now is not the time."),
                _("God, I want to. Not now. Someone always notices when I look at you like this."),
                _("Tsk... you make it so hard to be careful. Not now, my boy."),
            ],
            "masturbate": [
                _("You have no idea how much I want to... not now. Too risky."),
                _("Don't tempt me. If I start, I won't care who hears. Later."),
                _("Hmmph... later. When I can take my time and you can't look away."),
            ],
            "hj": [
                _("Not now. One of us has to be careful, and it's never you."),
                _("Don't look at me like that. I want to, God knows. Just not now."),
                _("Tsk... later, my boy. When nobody can interrupt us."),
            ],
            "tj": [
                _("Stop staring... I want to, you know I do. Not right now."),
                _("Tsk. Later. When I can take my time with you."),
                _("Don't tempt me, my boy. It's a bad moment, and I hate that it is."),
            ],
            "bj": [
                _("My mouth is watering... no. Not now. Too many things could go wrong."),
                _("God, don't ask me like that... later. I promise, later."),
                _("Tsk. I want you in my mouth so badly... but not now. Be patient for me."),
            ],
            "sex": [
                _("I want you so badly it's stupid... and that's exactly why not now. One of us has to think."),
                _("Don't... if you touch me now, I'll forget your father exists. Not today. It's too risky."),
                _("Tsk... later, my boy. When I can scream and nobody hears."),
            ],
            "anal": [
                _("Mmm... don't tempt me. Not now, I can't afford to be that reckless today."),
                _("Later. For you, I'd say yes. Just not today."),
                _("Tsk... ask me that when there's time to do it properly. Not now."),
            ],
            "oral": [
                _("Your mouth on me... God, yes... but not now. I wouldn't be quiet."),
                _("Don't kneel. If you kneel, I'll say yes, and this is a terrible moment."),
                _("Tsk. Later, my boy. When I can take my time and keep you down there."),
            ],
        },

        # He has a girlfriend ("{0}" = her name): she is his, and she doesn't share
        "pgf_accepted.femdom_s3": {
            "flirt": [
                _("Flirting with me while {0} waits for you? Mmm. Good. Keep going."),
                _("Go on, my boy. She gets the leftovers. I get the best of you."),
            ],
            "kiss": [
                _("Come here. Let's see if you can still kiss her after this."),
                _("Mmm. Kiss me, and taste the difference between a woman and {0}."),
            ],
            "masturbate": [
                _("Watch me, my boy. I doubt {0} could hold your attention like this."),
                _("Sit. Look at me, and forget that little girl exists for a while."),
            ],
            "hj": [
                _("Give it to me. Your girlfriend's hands are wasted on you. Mine aren't."),
                _("Mmm. Let me show you everything {0} has been doing wrong."),
            ],
            "tj": [
                _("Sit down. Compare me to {0} all you like. It isn't a contest."),
                _("Mmm. These are yours, my boy. Hers are a rumor."),
            ],
            "bj": [
                _("Stand still. Next time she kisses you, I want you thinking of my mouth."),
                _("Mmm. {0} would cry if she saw where you put this. Good."),
            ],
            "sex": [
                _("Take me. Then go back to {0} and try to look her in the eye."),
                _("Yes, my boy. She has your title. I have you."),
            ],
            "anal": [
                _("Mmm. Fine. Whatever she gives you, I give you better."),
                _("Take it, my boy. And don't you dare think of {0} while you do."),
            ],
            "oral": [
                _("Down you go, my boy. Show me the mouth she doesn't deserve."),
                _("Mmm. Forget {0}. Right now your mouth belongs to the woman who matters."),
            ],
        },

        "pgf_denied.femdom_s3": {
            "flirt": [
                _("Not now. I'm in no mood to flirt while {0} is still in your life."),
                _("Save it, my boy. I'm yours, but I don't share well. Not today."),
            ],
            "kiss": [
                _("Not now. I'm too jealous of {0} to kiss you. I'd bite."),
                _("Tsk. Later. I'm in no mood to be your secret's secret today."),
            ],
            "masturbate": [
                _("Not today. I'm not putting on a show while I'm this angry about {0}."),
                _("Hmmph. No. I'm in a foul mood, and that girl of yours is the reason."),
            ],
            "hj": [
                _("Not now. If I touch you while I'm thinking about her, I'll be cruel."),
                _("Later, my boy. Today I'm too jealous to be gentle."),
            ],
            "tj": [
                _("Not today. Go and ask yourself why you're still with {0}."),
                _("Hmmph. Not now. I'm not in the mood to share you, even in my head."),
            ],
            "bj": [
                _("Not today. I won't get on my knees while that girl still thinks you're hers."),
                _("Later, my boy. I'm too angry about {0} to do this properly."),
            ],
            "sex": [
                _("Not today. Too risky. If {0} ever smells me on you, we both lose."),
                _("Hmmph. Not now. I'm yours, but I'm not in the mood to be the other woman today."),
            ],
            "anal": [
                _("Not today. I'm too jealous to relax, and that matters for this."),
                _("Tsk. Later, my boy. Get {0} out of my head first."),
            ],
            "oral": [
                _("Not now. I can't enjoy anything while I'm picturing her face."),
                _("Hmmph. Later. Today I want you to miss me, not her."),
            ],
        },
    }

    SCENE_LINES.update({

        # ══════════════════════════════════════════════════════════
        #  MOANS: handjob (her hand, her control: she never begs here)
        # ══════════════════════════════════════════════════════════
        "moan.speed1.hj.shion": [
            _("Slowly... look at you, twitching already. Pathetic."),
            _("Mmm. So hard for your stepmother. You should be ashamed of yourself."),
            _("Look at me, boy. I want to see exactly what I'm doing to you."),
        ],
        "moan.speed2.hj.shion": [
            _("Such a desperate little thing in my hand. It suits you."),
            _("Don't you dare squirm. You stay still and take it."),
            _("Mmh... every inch of this answers to me now. Remember that."),
        ],
        "moan.speed3.hj.shion": [
            _("Look at you... throbbing in my hand, you little shit."),
            _("Is this all it takes to break you? My hand? Pathetic, boy."),
            _("That's it... twitch for me. Every drop of this belongs to me."),
        ],

        # ══════════════════════════════════════════════════════════
        #  MOANS: cowgirl (reverse cowgirl reads these too: she looks back over her shoulder)
        # ══════════════════════════════════════════════════════════
        "moan.speed1.cowgirl.shion": [
            _("Mmm... slowly. I decide how deep you go, boy."),
            _("Don't move. You lie there and let me use you."),
            _("Hmm... not bad. Don't let it go to your head."),
        ],
        "moan.speed2.cowgirl.shion": [
            _("S-shut up... don't look at me like that... fuck... fuck... I'm still your stepmother, you son of a bitch... ogghhh..."),
            _("Hahh... don't you dare move... I set the pace... mmh..."),
            _("Ahh... this is mine... every inch of it... you hear me?"),
        ],
        "moan.speed3.cowgirl.shion": [
            _("F-fuck... you little bastard... where did you learn to... ahh!... fuck like this..."),
            _("Ahh... ahh... don't you dare stop... I'm not done with you..."),
            _("Ogghhh... fuck... look at me... look at who's riding you, boy..."),
        ],
        # He has a girlfriend
        "moan.speed2.cowgirl.shion.player_cheating": [
            _("Hahh... can your little girlfriend ride you like this?... no... of course not..."),
            _("Mmh... look at me... not her... never her again..."),
            _("Ahh... you'll end it with her... you hear me?... you're mine..."),
        ],

        # ══════════════════════════════════════════════════════════
        #  MOANS: doggy (vaginal; "doggy" has no shared pools, the picker still asks "<key>.doggy.shion")
        # ══════════════════════════════════════════════════════════
        "moan.speed1.doggy.shion": [
            _("Hmmph... slowly. Don't you dare rush this."),
            _("Mmh... you like me like this, don't you? Don't get used to it."),
            _("Ahh... careful, boy. I'm letting you do this. Never forget that."),
        ],
        "moan.speed2.doggy.shion": [
            _("Ogghhh... deeper, you little shit... hahh... at least you know how to fuck a cunt properly..."),
            _("Hahh... harder... what are you waiting for, an invitation?..."),
            _("Mmh... ahh... don't you stop... don't you dare stop now..."),
        ],
        "moan.speed3.doggy.shion": [
            _("Hit me harder!... c'mon, you coward... make me hurt... your father was too fucking scared to even try..."),
            _("Ahh!... ahh!... fuck... you animal... you fucking animal... don't stop..."),
            _("Ogghhh... fuck... fuck... you're going to ruin me, you little bastard..."),
        ],
        # He has a girlfriend
        "moan.speed2.doggy.shion.player_cheating": [
            _("Does your little toy... fuck... let you do this... to her?"),
            _("Hahh... does she moan like this for you?... no... I didn't think so..."),
            _("Ahh... think of her now... go on... think of her while you're inside me..."),
        ],

        # ══════════════════════════════════════════════════════════
        #  MOANS: anal (never says she loves or hates it: anal_lover / anal_hater can roll)
        # ══════════════════════════════════════════════════════════
        "moan.speed1.anal.shion": [
            _("Nnh... slowly, you animal... you don't just shove it in a woman's ass..."),
            _("Hahh... careful... I'm letting you have this. Remember that."),
            _("Mmh... easy... easy, boy... I'll tell you when you can move."),
        ],
        "moan.speed2.anal.shion": [
            _("Ahh... fuck... so deep in my ass... hahh... you little shit..."),
            _("Nnh... ahh... if you tell a soul about this, I'll bury you..."),
            _("Hahh... deeper... no... slower... fuck, don't listen to me..."),
        ],
        "moan.speed3.anal.shion": [
            _("Ogghhh... fuck... my ass... you little shit... you're splitting me open..."),
            _("Ahh!... ahh!... you bastard... you absolute bastard... don't stop..."),
            _("Fuck... fuck... your father would die if he saw this... ogghhh..."),
        ],

        # ══════════════════════════════════════════════════════════
        #  HER ORGASM (GirlCumming: tier 1 girl_cum, tier 2 girl_cum_intense, tier 3 girl_cum_hard)
        # ══════════════════════════════════════════════════════════
        "girl_cum.cowgirl.shion": [
            _("Ahh!... fuck... fuck!... don't you dare move... I'm... ogghhh!..."),
            _("Nnh... you little... bastard... I'm cumming... on my stepson's cock... ahh!..."),
            _("Shut up... shut up... don't look at me... ahh... AHH!..."),
        ],
        "girl_cum.doggy.shion": [
            _("Don't you fucking stop... don't you dare... ahh... ahh... I'm gonna... ogghhh... gonna squirt all over this fat dick..."),
            _("Ogghhh... fuck... you little shit... I'm cumming... I'm... ahh!..."),
            _("Ahh!... not from you... not from you... fuck... FUCK!..."),
        ],
        "girl_cum.anal.shion": [
            _("Ahh!... from my ass... you bastard... you made me... ogghhh!..."),
            _("Fuck... fuck... not there... not like this... AHH!..."),
            _("Nnh... you little shit... I'm cumming... don't you dare stop now..."),
        ],
        # Tier 2 has no pose pools anywhere: one pool for every pose, true even when she is alone
        "girl_cum_intense.shion": [
            _("Ogghhh... fuck... fuck... this is too much... AHH!..."),
            _("Hahh... damn it... damn it... I'm... ogghhh!..."),
            _("Nnh... no... not like this... fuck... FUCK!..."),
        ],
        # Tier 3, her hardest orgasm: the only moment she breaks completely
        "girl_cum_hard.cowgirl.shion": [
            _("This pussy belongs to you now... fuck... fuck... hmmphh... fuck your father..."),
            _("Ogghhh... I can't... I can't stop... you've ruined me, you little bastard... AHH!..."),
            _("Fuck... fuck... I'm your stepmother... and I'm cumming on your... OGGHHH!..."),
        ],
        "girl_cum_hard.doggy.shion": [
            _("This pussy belongs to you now... fuck... fuck... hmmphh... fuck your father..."),
            _("AHH!... fuck me... fuck me like your father never could... OGGHHH!..."),
            _("I can't... think... I'm cumming so hard... you little shit... AHHH!..."),
        ],

        # ══════════════════════════════════════════════════════════
        #  RIGHT AFTER HER ORGASM: she takes back control
        # ══════════════════════════════════════════════════════════
        "girl_post_cum.cowgirl.shion": [
            _("Hahh... hahh... wipe that look off your face. You didn't do that. I did."),
            _("That... never happened. Do you understand me, boy?"),
            _("Mmh... don't get comfortable. I'm not finished with you."),
        ],
        "girl_post_cum.doggy.shion": [
            _("Hahh... not a word about this. Not to anyone. Especially not your father."),
            _("Tsk... I can feel you smirking back there. Stop it."),
            _("Hmmph... acceptable. For a boy. Now don't you dare stop."),
        ],
        "girl_post_cum.anal.shion": [
            _("Hahh... from my ass... you little bastard... this never happened."),
            _("Tsk... don't you dare look so proud. You'll pay for that later."),
            _("Hahh... hahh... not a word. Not one word, boy."),
        ],
        # Tier 2, every pose, true even when she is alone
        "girl_post_cum_intense.shion": [
            _("Hahh... hahh... get a grip, Shion..."),
            _("Hmmph... hahh... that was... acceptable..."),
            _("Nnh... damn it... my legs are still shaking..."),
        ],

        # ══════════════════════════════════════════════════════════
        #  HIS CUM
        # ══════════════════════════════════════════════════════════
        # Inside, she allowed it (cowgirl / reverse cowgirl / doggy: those poses have no pool of their own; anal does)
        "cum_inside_consented.shion": [
            _("Hmmph. Every drop, exactly where I allowed it. Don't make me regret my generosity."),
            _("There. Now you've left something of yours inside your father's wife. Think about that."),
            _("Hahh... warm... Hmmph. Don't look so proud. I let you."),
        ],
        # Inside, without her permission (she may have said no, or never been asked: no "I told you", no "without asking")
        "cum_inside_forced.shion": [
            _("Did I give you permission to do that? Did I?!"),
            _("You came inside me... without my permission... You are going to regret that, boy."),
            _("Get out of me. You don't take things from me. Ever. I give them."),
        ],
        # Same moment for a cum_slut who had said no (Cum.rpy _cream_liked_line reads "cum_inside_forced" and treats
        # it as a load she liked anyway): still the disobedience, never "I didn't want it"
        "cum_inside_forced.shion.cum_slut": [
            _("I said no... and you did it anyway... Hmmph. I'll punish you for that. Later."),
            _("You disobeyed me... and I... tsk. Don't you dare smile about it."),
            _("Did I say you could?... hahh... No. And yet... Hmmph. Don't make a habit of it."),
        ],
        # He asks to cum in her mouth and she allows it (any pose)
        "cum_mouth_accepted.shion": [
            _("Fine. In my mouth. And you'll look me in the eye while you do it."),
            _("Hmmph. Go on, then. Consider it a loan. I always collect."),
            _("Fine. Give it to me. And not a word about this, ever."),
        ],
        # On her face, after a blowjob
        "cum_face.bj.shion": [
            _("On my face? You little shit... do you have any idea what my skin care costs?"),
            _("Look at what you did... get me a towel. Now. And wipe that grin off your face."),
            _("Hmmph. Marking your territory, boy? Cute. You'll pay for this later."),
        ],

        # ══════════════════════════════════════════════════════════
        #  HER TURN, stage 3 (femdom_s3): she is his. Proud, possessive, filthy, few orders.
        #  Same moments and same truth rules as her before pools above (her anal lines never say she loves or hates
        #  it, her cum lines never say she loves or hates cum; the intense ones are true even when she is alone).
        # ══════════════════════════════════════════════════════════
        # Moans: handjob
        "moan.speed1.hj.shion.femdom_s3": [
            _("Mmm... look at you. All mine, every inch."),
            _("Your father never got this hard for me. Not once."),
            _("Slowly, my boy... I like feeling you twitch for me."),
        ],
        "moan.speed2.hj.shion.femdom_s3": [
            _("Mmh... I could do this for hours, and your father would never know."),
            _("Look at me while I stroke you... I want to see what I do to you."),
            _("Throbbing in my hand like a good boy... fuck, I love this cock."),
        ],
        "moan.speed3.hj.shion.femdom_s3": [
            _("That's it... fuck my hand, you little bastard... it's all yours."),
            _("Hahh... look how close you are... and I'm the one who got you there."),
            _("Come on, my boy... show me what my hand does to you."),
        ],
        # Moans: cowgirl (and reverse cowgirl)
        "moan.speed1.cowgirl.shion.femdom_s3": [
            _("Mmm... slowly... I want to feel every inch of what's mine."),
            _("Look at you under me... your father never once looked at me like that."),
            _("Hahh... I told myself I was only using you. What a liar I was."),
        ],
        "moan.speed2.cowgirl.shion.femdom_s3": [
            _("Ahh... fuck... this cock was made for me... you hear me?"),
            _("Hahh... push up into me, my boy... fuck... yes..."),
            _("Mmh... if your father could see his wife now... riding his son... ahh..."),
        ],
        "moan.speed3.cowgirl.shion.femdom_s3": [
            _("Fuck... fuck... deeper... you've ruined me for every other man, you little shit..."),
            _("Ahh!... ahh!... I'm yours... I'm fucking yours... don't stop..."),
            _("Ogghhh... look at your father's wife bouncing on your cock... look at her..."),
        ],
        # Moans: doggy (vaginal)
        "moan.speed1.doggy.shion.femdom_s3": [
            _("Mmm... slowly... I like it when you take your time with me."),
            _("Hahh... taking me from behind like a little animal... I don't even mind anymore."),
            _("Mmh... your hands on my hips... right where they belong."),
        ],
        "moan.speed2.doggy.shion.femdom_s3": [
            _("Ahh... fuck... deeper... you fuck me better than any man I've ever had..."),
            _("Hahh... slap my ass... go on... your father would never dare..."),
            _("Mmh... ahh... fuck me like I'm yours... because I am..."),
        ],
        "moan.speed3.doggy.shion.femdom_s3": [
            _("Harder!... fuck... ruin me, my boy... your father never even came close..."),
            _("Ahh!... ahh!... fuck... your filthy stepmother... and she fucking loves it..."),
            _("Ogghhh... fuck... fuck... this pussy is yours... take it... take it..."),
        ],
        # Moans: anal
        "moan.speed1.anal.shion.femdom_s3": [
            _("Nnh... slowly, my boy... let me feel all of it."),
            _("Hahh... your father never got anywhere near this... only you..."),
            _("Mmh... easy... easy... I'm giving you everything, you know that?"),
        ],
        "moan.speed2.anal.shion.femdom_s3": [
            _("Ahh... fuck... so deep... you filthy little bastard... don't stop..."),
            _("Nnh... ahh... your father's wife... taking it in the ass from his son... hahh..."),
            _("Hahh... fuck... nothing of me is off limits to you... nothing..."),
        ],
        "moan.speed3.anal.shion.femdom_s3": [
            _("Ogghhh... fuck... harder... I don't care if it hurts... I'm yours..."),
            _("Ahh!... ahh!... you animal... you beautiful fucking animal..."),
            _("Fuck... fuck... if your father could hear me now... let him... ogghhh..."),
        ],

        # Her orgasm
        "girl_cum.cowgirl.shion.femdom_s3": [
            _("Ahh!... fuck... I'm cumming... on my boy's cock... ogghhh!..."),
            _("Nnh... yes... yes... look what you do to me... AHH!..."),
            _("Fuck... fuck!... your father never... not once... AHH!..."),
        ],
        "girl_cum.doggy.shion.femdom_s3": [
            _("Ahh!... don't stop... I'm cumming... I'm cumming for you... ogghhh!..."),
            _("Ogghhh... yes... yes... this is why I'm yours... AHH!..."),
            _("Fuck... right there... you little shit... right there... AHH!..."),
        ],
        "girl_cum.anal.shion.femdom_s3": [
            _("Ahh!... fuck... you're making me cum... like this... ogghhh!..."),
            _("Nnh... I'm cumming, my boy... all for you... AHH!..."),
            _("Fuck... fuck... only you... only you can do this to me... AHH!..."),
        ],
        # Tier 2: every pose, true even when she is alone (she thinks of him)
        "girl_cum_intense.shion.femdom_s3": [
            _("Ogghhh... fuck... my boy... my boy... AHH!..."),
            _("Hahh... God... God... I'm ruined... completely ruined... AHH!..."),
            _("Nnh... fuck... nobody else... nobody else ever... ogghhh!..."),
        ],
        # Tier 3, her hardest
        "girl_cum_hard.cowgirl.shion.femdom_s3": [
            _("It's yours... all of it... my pussy, my ass, my fucking life... AHH!..."),
            _("Ogghhh... look at me... your father's wife... cumming like a whore for you... AHHH!..."),
            _("Fuck... fuck... my boy... I'd leave him for this... I'd leave him tonight... OGGHHH!..."),
        ],
        "girl_cum_hard.doggy.shion.femdom_s3": [
            _("AHH!... yes... yes... fuck me like you own me... you do... OGGHHH!..."),
            _("I can't... I can't stop cumming... my boy... my fucking boy... AHHH!..."),
            _("Ogghhh... fuck... every man before you... nothing... NOTHING... AHHH!..."),
        ],

        # Right after her orgasm: no more taking back control, she is proud of what he does to her
        "girl_post_cum.cowgirl.shion.femdom_s3": [
            _("Hahh... hahh... look what you did to me. Don't you dare look humble about it."),
            _("Mmm... stay inside me a little longer. I'm not done being yours."),
            _("Hahh... your father has never once made me shake like this."),
        ],
        "girl_post_cum.doggy.shion.femdom_s3": [
            _("Hahh... hahh... God. Whatever you're doing to me, don't stop doing it."),
            _("Mmm... look at me, still shaking. Proud of yourself? You should be."),
            _("Hahh... your father's wife, bent over and ruined. Happy now, my boy?"),
        ],
        "girl_post_cum.anal.shion.femdom_s3": [
            _("Hahh... from my ass... you've ruined me for anyone else. I hope you know that."),
            _("Mmm... still shaking... don't look so proud. ...No. Go on. Be proud."),
            _("Hahh... hahh... nobody else gets this from me. Nobody. Remember that."),
        ],
        # Tier 2, every pose, true even when she is alone
        "girl_post_cum_intense.shion.femdom_s3": [
            _("Hahh... hahh... look at me... shaking like a schoolgirl..."),
            _("Mmm... God... that boy is going to be the death of me..."),
            _("Hahh... get a grip, Shion... no... no, let it shake..."),
        ],

        # His cum inside, she allowed it (cowgirl / reverse cowgirl / doggy, like her before pool)
        "cum_inside_consented.shion.femdom_s3": [
            _("Mmm... that's where you belong. Inside me. Not a drop for anyone else."),
            _("Hahh... your father's wife, full of his son. If he only knew."),
            _("Hmmph. Warm... Don't look so proud, my boy. ...Fine. Look proud. You earned it."),
        ],
    })
