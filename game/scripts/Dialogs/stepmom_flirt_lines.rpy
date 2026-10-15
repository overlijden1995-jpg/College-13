# ============================================================
# stepmom_flirt_lines.rpy... the stepmom ROLE voice for the trait / context flirt pools (docs/plan_shion.md)
# ============================================================
#
# rod_lines["role:stepmom"]: the block of a ROLE, not of a girl. A girl gets it from GIRLS_CONFIG[gid]["role"]
# (girl_role / girl_role_key in characters_stats.rpy). Today only Shion holds the role, but any character can take it.
# rod_flirt_line(girl, action, mode) tries, in order: her own "<key>.<modifier>", her ROLE's "<key>.<modifier>" (this
# block), the Global "<key>.<modifier>", her own "<key>", her role's "<key>", the Global "<key>".
#
# Why it exists (the author's decision): the Global modifier pools speak like a college student ("my boyfriend", "I'm
# not into that...", giggles, "*blushes*"). A stepmother must never say them, so every Global "<key>.<modifier>" she
# can reach has an exclusive variant here: "exclusive variants for characters with the stepmom profile; in the future
# other characters can take that role, so the lines must be specific".
#
# Rules for this block:
#   - Same key, same situation / fact as the Global pool it replaces; only the voice changes. _FLIRT_PUBLIC_ONLY_TRAITS
#     (exhibitionist, public_fetish, public_shy) only speak in public; _FLIRT_CAMERA_TRAITS (camera_lover,
#     camera_hater) in public OR while he records; ".player_cheating" = he has a girlfriend who is not her.
#   - The ROLE, not Shion: a mature woman married to his father. The taboo ("your father", "your stepmother", "your
#     father's wife"), authority, experience, composure. No name, no job, no money, nothing only one woman would say.
#     It must fit a cold, commanding stepmom AND a warmer one: confident, teasing, in control. Never giggly, never shy
#     like a college girl (a cute_sex stepmom is tender and gentle, not bashful), never "my boyfriend".
#   - Modifiers covered: camera_hater, camera_lover, cum_slut, cute_sex, exhibitionist, hardcore_sex, hate_cum,
#     public_fetish, public_shy, player_cheating. Not covered: virgin (a stepmom is never a virgin), loyal / cheater /
#     both_cheating (they need her own NPC partner; the father is not an NPCPartner, a stepmom never has one).
#   - The hand flirts in normal modes (normal_yes, enthusiastic_yes...) never reach a femdom stepmom (she only gets
#     commanding_no / commanding_yes there: FEMDOM_FLIRT_PENALTY) but do reach a future non-femdom one: kept all.
#   - A girl's own pools still win: Shion's shion_flirt_lines.rpy ".player_cheating" pools speak before these.
#   - No %(pl)s placeholders (no partner). [Player.Name] is fine.
# ============================================================

init 1 python:

    rod_lines["role:stepmom"] = {

        # ==========================
        # SHE DECIDES FOR HER HUSBAND (family_wife_overrules): the errand ask (_family_errand) and the
        # dessert run of the Sunday dinner (_apartment_dinner_weekly). The woman who runs boardrooms runs
        # the house: her order is calm, final, and he never hears what it is for.
        # ==========================
        "family_errand_order": [
            _("Actually, dear, go. We're out of the sparkling water I like, and the walk will do you good."),
            _("Go on, darling. Take the list on the fridge while you're at it. We'll manage without you."),
            _("He asked nicely, and I'm asking better. Shoes, coat, store. We'll hold the fort."),
        ],
        "family_errand_alone": [
            _("There. Fifteen minutes, maybe twenty if he reads the labels. Use your time wisely."),
            _("And just like that, the apartment is mine again. ...Ours. For a little while."),
            _("He walks slowly on the way back. I know, because I have eyes and he has a wife."),
        ],
        "family_dessert_order": [
            _("You know what, he's right. The ones with the chestnut cream, from the stand. Three blocks, dear."),
            _("Mm. Now that he's said it, nothing in this kitchen will taste right. Go, darling. The stand on the corner."),
        ],
        "family_dessert_backs_him": [
            _("Sit down, [Player.Name]. The dessert on this table was chosen, paid for, and will be eaten."),
            _("Nobody is walking three blocks for sugar. Eat what's in front of you."),
        ],

        # ==========================
        # NO PHOTOS, EVER (girl_sends_photos, GIRLS_CONFIG "no_photos"): her answer when he asks for one.
        # Not a step refusal: a permanent rule of hers, true at every step. A married woman of her standing
        # leaves nothing with her face on it on anyone's phone. Works cold AND surrendered: firm, final,
        # no apology, no promise of later.
        # ==========================
        "photo_never": [
            _("No. I don't send photos. Not to you, not to anyone."),
            _("A photo of me, on a phone I don't control? That will never happen."),
            _("Photos outlive the moment, and they always surface. You get nothing with my face on it."),
        ],

        # ==========================
        # DORM HANGOUT INVITE, STUDENTS ONLY (hangout_girl_accepts / hangout_send_invite): her group-chat
        # decline when he invites her to the drinking night in his room. Other girls read this message:
        # composed, adult, nothing intimate, true at every step.
        # ==========================
        "hangout_not_student": [
            _("I think I'm a little past dorm parties. Have fun, and behave."),
            _("That invitation was not meant for me, surely. Enjoy your night, kids."),
            _("Adults have work in the morning. Keep the noise where I can't hear it."),
        ],

        # ==========================
        # FIRST SIGHT OF HIM (PlayerExposure, her first sexual look at him): the stepmom measures the
        # son against the husband (author 2026-10-10: "maior que o do pai"). Any stepmom can say these.
        # ==========================
        "penis_first_sight": [
            _("...Well. You did not get THAT from your father."),
            _("Oh my. So the son outgrew the man of the house. Noted."),
            _("...Hm. Your father should pray I never make comparisons out loud."),
        ],

        # ==========================
        # HER FIRST ANAL EVER (_anal_first_story_beat, GIRLS_CONFIG "anal_untouched"): nobody came
        # before, her husband never dared to ask (author 2026-10-10). Line 1 then line 2, once.
        # ==========================
        "anal_her_first": [
            _("Wait. Slow. ...Whatever you think I have done before, not this. Never this."),
            _("Stop. ...Listen to me. Nobody has ever had me there. Nobody."),
        ],
        "anal_her_first_2": [
            _("Your father never even dared to ask. So you will go slow, and you will be grateful."),
            _("Not even my husband dared to ask for this. Remember that, every single second of it."),
        ],

        # ==========================
        # ANAL LOCKED + ANAL LOVER (story_locked_line's exception, author 2026-10-11): she wants it
        # too, so the refusal turns into a dangled promise. The step stays shut; she just enjoys the
        # dangling. Works at any step, no act described beyond the hint.
        # ==========================
        "anal_locked_tease": [
            _("There? No. ...Not yet. Keep earning, and one day I might let you have the one thing your father never even dared to dream of."),
            _("Mm. Bold. The answer is no... for now. Behave, and someday I may open the one door nobody has walked through."),
            _("Not tonight, greedy. But keep looking at me like that and one day... maybe. MAYBE."),
        ],

        # ==========================
        # NIGHT, NOT THE WHOLE NIGHT (sleepover_offer, husband home): the rule that keeps her life
        # standing. Plain, final, true at every step.
        # ==========================
        "sleepover_husband_home": [
            _("No. Whatever this is, it ends before his alarm does. I am home when he wakes. Always."),
        ],

        # ==========================
        # LEFT ON THE EDGE (scene_full_cleanup): the scene ends with her at the top and no release.
        # Warm = she drops the mask and demands it; cold = she rebuilds her composure on the spot.
        # ==========================
        "edge_end_beg": [
            _("...You are not leaving this room. Finish what you started. That is an order."),
            _("Stop. Come back here. I was... you KNOW exactly where I was. Finish it."),
        ],
        "edge_end_hide": [
            _("...Go. Now. Before I say something we will both regret."),
            _("That will be all. ...Do not look at me like that. I said that will be all."),
        ],

        # ==========================
        # BLACKMAIL, STORY-LOCKED (his video against an act her step has not opened, _blackmail_attempt):
        # the woman of the house answers from above (author, 2026-10-09). The threat IS the no: she could
        # have him handled and chooses not to. Never a real beating, never a word of fear.
        # ==========================
        "blackmail_story_locked": [
            _("Blackmail? Me? Sweetheart, I keep lawyers on retainer and people far less polite than lawyers. If I wanted you limping, it would already be arranged. Put the phone away."),
            _("Think very hard about this. Women like me make one call and problems like you get walked home by two very large men. Lucky for you, I find this more funny than insulting."),
            _("A video. Against ME. I could have someone teach you manners by dinner and still make my morning meetings. No. You earn things in this house, you don't extort them."),
        ],

        # ==========================
        # CAMERA HATER (in public or while he records): a camera, a stare, a photo that reaches his father
        # ==========================
        "flirt_safe_touch_cheek_soft_no.camera_hater": [
            _("Hand down. I won't have a picture of my stepson touching my face going around."),
            _("Subtle, [Player.Name]. I don't like eyes on me, and I like cameras even less."),
        ],
        "flirt_safe_kiss_cheek_soft_no.camera_hater": [
            _("Not like that. The last thing I need is a picture of my husband's son kissing me."),
            _("Save it. Everyone carries a camera now, and I refuse to end up on one of them."),
            _("If I see a single phone pointed at us, this ends. Understood?"),
        ],
        "flirt_safe_hug_soft_no.camera_hater": [
            _("Not like this. A hug from your stepmother looks innocent right up until someone gets it on camera."),
            _("Let go, [Player.Name]. I hate being looked at like this, and I hate being filmed even more."),
        ],
        "flirt_lewd_slap_ass_hard_no.camera_hater": [
            _("Have you lost your mind? If someone records that, your father sees it by dinner."),
            _("If that ends up on anyone's phone, you'll answer to me. And then to your father."),
            _("If anyone caught that on camera, I will never forgive you. Never."),
        ],
        "flirt_lewd_grab_tits_hard_no.camera_hater": [
            _("Hands off. Now. Do you know what one photo of this would do to your father?"),
            _("I will not be anyone's video, [Player.Name]. Least of all with my stepson's hands on me."),
        ],
        "flirt_lewd_grab_ass_hard_no.camera_hater": [
            _("If anyone filmed that, you'll be the one explaining it to your father. Not me."),
            _("Let go. A married woman doesn't need that kind of attention, and neither do you."),
        ],

        # ==========================
        # CAMERA LOVER (in public or while he records): she wants it on camera
        # ==========================
        "flirt_safe_touch_cheek_enthusiastic_yes.camera_lover": [
            _("Mm. Hold it there. That would make a lovely picture, don't you think?"),
            _("If you're going to touch me like that, have the decency to put it on camera."),
            _("Your hand on your stepmother's face... that would photograph beautifully."),
        ],
        "flirt_safe_kiss_cheek_enthusiastic_yes.camera_lover": [
            _("Sweet. I hope someone caught that on camera. I'd like a copy."),
            _("Next time, we film it. For the family album, of course."),
            _("On video, that would look far more scandalous than it was. I like that."),
        ],
        "flirt_safe_hug_enthusiastic_yes.camera_lover": [
            _("Closer. A proper hug. This is the kind of picture I'd keep."),
            _("Hold still. Someone ought to be capturing this, and I'd like it to be flattering."),
        ],
        "flirt_lewd_slap_ass_enthusiastic_yes.camera_lover": [
            _("Mm. Again, and this time I want it on video."),
            _("If someone filmed that, I wouldn't even be angry. I'd ask for the file."),
            _("A stepmother taking a slap from her stepson... people would pay to watch that."),
        ],
        "flirt_lewd_grab_tits_enthusiastic_yes.camera_lover": [
            _("Hold that. Right there. That's the shot."),
            _("You know, if there were a camera on us right now, I wouldn't mind in the least."),
        ],
        "flirt_lewd_grab_ass_enthusiastic_yes.camera_lover": [
            _("Again. Slower. Make it worth watching back."),
            _("You appreciate the view, I see. Record it, and I'll appreciate you even more."),
        ],

        # ==========================
        # CUM SLUT: a sweet touch is never enough, she wants all of it
        # ==========================
        "flirt_safe_touch_cheek_enthusiastic_yes.cum_slut": [
            _("Sweet. But a woman my age knows exactly where she'd rather have those hands."),
            _("Mm, gentle. I know you have more in you than that, and I intend to get all of it."),
        ],
        "flirt_safe_kiss_cheek_enthusiastic_yes.cum_slut": [
            _("A kiss on the cheek? From you I expect a great deal more than that."),
            _("Too high, [Player.Name]. Try lower. Your stepmother will tell you when to stop."),
            _("That's a start. Now kiss me somewhere your father would never forgive."),
        ],
        "flirt_lewd_slap_ass_enthusiastic_yes.cum_slut": [
            _("Mm. Harder. I want to feel it the next time I sit down at dinner with your father."),
            _("That's nothing. I can take a great deal more than that, [Player.Name]."),
            _("You're holding back. Don't. Not with me."),
        ],
        "flirt_lewd_grab_tits_enthusiastic_yes.cum_slut": [
            _("Good hands. Now imagine what else they could be doing to your stepmother."),
            _("Don't just grab them. Use your mouth too. I'll show you how."),
        ],
        "flirt_lewd_grab_ass_enthusiastic_yes.cum_slut": [
            _("Grab me like that and you'd better follow through later."),
            _("Mm. You know exactly what I'll want from you after this, don't you?"),
            _("Keep going. I'm already getting ideas, and none of them are motherly."),
        ],
        "flirt_lewd_ask_panties_enthusiastic_yes.cum_slut": [
            _("You want them? They're already a little wet. You did that to your stepmother."),
            _("Take them. I wasn't planning on keeping them on much longer anyway."),
        ],

        # ==========================
        # CUTE SEX: tender and gentle (a grown woman, never bashful); rough hands get a gentle no
        # ==========================
        "flirt_safe_touch_cheek_shy_yes.cute_sex": [
            _("Mm... your hand is warm. Leave it there a moment longer."),
            _("That was sweet of you. Gentle suits you, [Player.Name]."),
        ],
        "flirt_safe_hold_hands_shy_yes.cute_sex": [
            _("Your fingers are warm... Stay like this with me for a while."),
            _("Hm. Our hands fit together better than they should."),
        ],
        "flirt_safe_hug_shy_yes.cute_sex": [
            _("You smell nice... Don't let go yet, [Player.Name]."),
            _("Just stay like this for a bit. Nobody needs to know."),
        ],
        "flirt_safe_kiss_cheek_shy_yes.cute_sex": [
            _("Hm... my heart is beating faster than it should for a stepson's kiss."),
            _("You can't do that so softly and expect me to stay composed, [Player.Name]."),
        ],
        "flirt_lewd_slap_ass_soft_no.cute_sex": [
            _("Ow. That stung. Gently, [Player.Name]. I don't like being handled roughly."),
            _("No slapping. If you want to touch me, do it slowly. That's how I like it."),
        ],
        "flirt_lewd_grab_tits_soft_no.cute_sex": [
            _("Not like that. Gently, please. Grabbing isn't how you touch a woman."),
            _("Easy. Slow hands, [Player.Name], or none at all."),
        ],

        # ==========================
        # EXHIBITIONIST (public only): she wants to be seen
        # ==========================
        "flirt_safe_kiss_cheek_enthusiastic_yes.exhibitionist": [
            _("Again. Let them all wonder why a stepson kisses his stepmother like that."),
            _("I hope everyone saw that. Let them talk."),
        ],
        "flirt_lewd_slap_ass_enthusiastic_yes.exhibitionist": [
            _("Louder. I want every head here to turn."),
            _("Again. Let them watch your father's wife enjoy it."),
        ],
        "flirt_lewd_grab_tits_enthusiastic_yes.exhibitionist": [
            _("Right here, in front of everyone? Good. Let them see."),
            _("I don't care who's watching. Keep going, [Player.Name]."),
        ],
        "flirt_lewd_grab_ass_enthusiastic_yes.exhibitionist": [
            _("Good. I want everyone here to know I'm not behaving like a stepmother."),
            _("Grab it like you own it. People are watching, so give them something to see."),
        ],
        "flirt_lewd_touch_thighs_enthusiastic_yes.exhibitionist": [
            _("Right here, where anyone can see? I love it."),
            _("Let them see your hand on your stepmother's thigh. I want them to."),
        ],
        "flirt_lewd_touch_tits_enthusiastic_yes.exhibitionist": [
            _("Let them watch. I stopped caring what people think years ago."),
            _("Go on. If they're staring, they might as well get a good look."),
        ],
        "flirt_lewd_touch_pussy_enthusiastic_yes.exhibitionist": [
            _("In public? With people all around us? Oh, that's delicious."),
            _("Your hand there, out here in the open... You're bolder than I thought."),
        ],

        # ==========================
        # HARDCORE SEX: gentle is not enough, she wants it hard
        # ==========================
        "flirt_safe_touch_cheek_enthusiastic_yes.hardcore_sex": [
            _("Is that all? Touch me like you mean it, [Player.Name]."),
            _("Gentle is for girls your age. I'm a grown woman. Try harder."),
        ],
        "flirt_safe_hug_enthusiastic_yes.hardcore_sex": [
            _("Harder. Squeeze. I won't break."),
            _("That's a hug? Your father shakes hands harder than that."),
        ],
        "flirt_safe_shoulder_massage_enthusiastic_yes.hardcore_sex": [
            _("Harder. Don't be timid with me, [Player.Name]."),
            _("You call that pressure? Dig in. I can take it."),
        ],
        "flirt_lewd_slap_ass_enthusiastic_yes.hardcore_sex": [
            _("Now that's more like it. Don't you dare hold back with me next time."),
            _("You can hit harder than that. I'm not one of your fragile little college girls."),
        ],
        "flirt_lewd_grab_tits_enthusiastic_yes.hardcore_sex": [
            _("Use your hands properly. Your father's wife is not made of glass."),
            _("If you're going to touch your stepmother, commit to it. No half measures."),
        ],
        "flirt_lewd_grab_ass_enthusiastic_yes.hardcore_sex": [
            _("Now we're talking. Don't go shy on me now."),
            _("Good grip. Keep it. I like a man who holds on."),
        ],
        "flirt_lewd_touch_thighs_enthusiastic_yes.hardcore_sex": [
            _("Higher. I'm too old to be teased, [Player.Name]."),
            _("Stop being polite about it. Higher."),
        ],
        "flirt_lewd_touch_tits_enthusiastic_yes.hardcore_sex": [
            _("Squeeze harder. Your stepmother can take it."),
            _("Harder than that. I'll tell you if it's too much. It won't be."),
        ],
        "flirt_lewd_touch_pussy_enthusiastic_yes.hardcore_sex": [
            _("Finally. A man who doesn't ask permission first."),
            _("No asking, no hesitating. Good. That's how you touch me."),
        ],

        # ==========================
        # HATE CUM: sweat, hands, anything messy disgusts her
        # ==========================
        "flirt_safe_touch_cheek_normal_yes.hate_cum": [
            _("That's nice. Just keep it clean, [Player.Name]. Nothing messy."),
            _("Sweet. As long as it stays this innocent, you may."),
        ],
        "flirt_lewd_slap_ass_hard_no.hate_cum": [
            _("Don't get handsy with me, [Player.Name]. It's crude, and it's unhygienic."),
            _("Keep your sweaty hands to yourself, young man."),
            _("What's next, drooling on your stepmother? Disgusting."),
        ],
        "flirt_lewd_grab_tits_hard_no.hate_cum": [
            _("Hands off. I don't want your sweat on my skin, or on my clothes."),
            _("That was vile. Don't ever do that to me again."),
        ],
        "flirt_lewd_grab_ass_hard_no.hate_cum": [
            _("Your hands are clammy, I can feel it. Let go of me."),
            _("Disgusting. Did your father never teach you any hygiene?"),
        ],
        "flirt_lewd_ask_panties_hard_no.hate_cum": [
            _("That is the most revolting thing anyone has ever asked me. And from my stepson."),
            _("My panties? What would you even do with them? No, don't answer. Disgusting."),
            _("Absolutely not. The very idea turns my stomach."),
        ],
        "flirt_lewd_pinch_ass_hard_no.hate_cum": [
            _("Keep your fingers off me. I don't know where they've been."),
            _("Don't pinch me. Don't touch me at all. It's repulsive."),
        ],

        # ==========================
        # PUBLIC FETISH (public only): the risk of being caught is the thrill
        # ==========================
        "flirt_safe_kiss_cheek_enthusiastic_yes.public_fetish": [
            _("Again. Right here, in front of all these people."),
            _("Mm. Knowing someone might be watching you kiss your stepmother makes it so much better."),
            _("Next time, somewhere other than my cheek. And don't wait until we're alone."),
        ],
        "flirt_safe_hold_hands_enthusiastic_yes.public_fetish": [
            _("I love this. Everyone can see us, and nobody knows if we're family or something else."),
            _("Tighter. I want people to notice, and to wonder."),
        ],
        "flirt_lewd_slap_ass_enthusiastic_yes.public_fetish": [
            _("God, yes. In front of everyone, and from my own stepson."),
            _("That sound turned heads. Good. Let them stare at your stepmother."),
            _("Again. Louder. I want them to hear it."),
        ],
        "flirt_lewd_grab_tits_enthusiastic_yes.public_fetish": [
            _("Right here, where anyone could walk by and see my stepson's hands on me? ...Perfect."),
            _("You don't care who sees, and neither do I. Imagine one of your father's friends walking by right now."),
        ],
        "flirt_lewd_grab_ass_enthusiastic_yes.public_fetish": [
            _("Mm. Where everyone can see. Go on, I dare you."),
            _("A stepmother caught with her stepson's hand on her ass... the risk makes it ten times better."),
            _("Is anyone watching? Good. Let them see what your stepmother lets you do."),
        ],
        "flirt_lewd_ask_panties_enthusiastic_yes.public_fetish": [
            _("Here? With all these people around? ...That's exactly what makes it exciting."),
            _("What if I slipped them off right here, in front of everyone? Would you like that, [Player.Name]?"),
        ],
        "flirt_lewd_touch_thighs_enthusiastic_yes.public_fetish": [
            _("Mm... anyone could walk by right now and see where your hand is."),
            _("Out here, where anyone could see us? Don't stop."),
        ],
        "flirt_lewd_touch_tits_enthusiastic_yes.public_fetish": [
            _("The thought of someone catching us like this..."),
            _("If anyone catches your stepmother like this, there's no explaining it. Keep going."),
        ],
        "flirt_lewd_touch_pussy_enthusiastic_yes.public_fetish": [
            _("Oh... if anyone sees where your hand is right now..."),
            _("Right here in public? God. I'm your father's wife, and you're touching me there."),
        ],

        # ==========================
        # PUBLIC SHY (public only): being seen with her stepson like this alarms her (composed, never squealing)
        # ==========================
        "flirt_safe_kiss_cheek_soft_no.public_shy": [
            _("Not here. Someone might see us, [Player.Name]."),
            _("People are watching. Kiss your stepmother in public and they'll start asking questions."),
        ],
        "flirt_safe_hold_hands_soft_no.public_shy": [
            _("Let go. People will talk if they see me holding my stepson's hand like this."),
            _("Not out here. Somewhere private, if you must."),
        ],
        "flirt_lewd_slap_ass_hard_no.public_shy": [
            _("Have you lost your mind? People can see us."),
            _("Someone heard that. Everyone heard that. God, [Player.Name]..."),
        ],
        "flirt_lewd_grab_tits_hard_no.public_shy": [
            _("Not here. What if someone walks by? What if someone who knows your father walks by?"),
            _("Are you trying to get us caught? Hands off. Now."),
        ],
        "flirt_lewd_touch_thighs_hard_no.public_shy": [
            _("Someone could see. Are you out of your mind?"),
            _("Hand off my leg. We're in public, and I'm your stepmother."),
        ],
        "flirt_lewd_touch_tits_hard_no.public_shy": [
            _("Not here. People are watching us."),
            _("Stop. Right now. Do you want the whole place to see that?"),
        ],
        "flirt_lewd_touch_pussy_hard_no.public_shy": [
            _("Are you out of your mind? We're in public."),
            _("Here? In front of all these people? Take your hand away before someone sees."),
        ],

        # ==========================
        # PLAYER CHEATING: he has a girlfriend who is not her
        # ==========================
        "flirt_safe_touch_cheek_soft_no.player_cheating": [
            _("Don't you have a girlfriend? Go touch her face, not your stepmother's."),
            _("You're taken, [Player.Name], and I'm married to your father. Hand down."),
        ],
        "flirt_safe_touch_cheek_normal_yes.player_cheating": [
            _("Does your girlfriend know you touch your stepmother like this?"),
            _("If she saw you right now, she'd never look at you the same way. Or at me."),
        ],
        "flirt_safe_steal_kiss_soft_no.player_cheating": [
            _("Have you lost your mind? You have a girlfriend."),
            _("Not while you're with someone. A girlfriend and a stepmother is one secret too many."),
        ],
        "flirt_safe_steal_kiss_normal_yes.player_cheating": [
            _("Your girlfriend would hate this. Your father would hate it more. And I don't care."),
            _("I hope she never finds out. Then again... that's your problem, not mine."),
        ],
        "flirt_lewd_slap_ass_normal_yes.player_cheating": [
            _("Does your girlfriend let you do that? I doubt it."),
            _("Careful. Your girlfriend might get jealous of your stepmother."),
        ],
        "flirt_lewd_grab_tits_normal_yes.player_cheating": [
            _("I bet your girlfriend doesn't let you grab hers like this."),
            _("Wash your hands before you touch her again. She'd smell my perfume on you."),
        ],

        # ==========================
        # A flirt her step does not open yet (story_steps.rpy: mode "story_locked", every flirt). Face to face AND
        # on the phone: nothing physical in the line. "<key>.<trait>" = that trait's tone (rod_flirt_line tries the
        # trait variants of each key first; femdom / hardcore_sex speak only once she is a veteran: trait_line_keys)
        # ==========================
        # ...and with her husband in the room (husband_in_room): face to face only. This shared pool is the two of
        # them hiding something ("behave, he's watching"): steps 1+ only. On her FIRST step there is nothing to
        # hide and the nerve itself offends: "flirt_story_locked_husband.cold" speaks instead (rod_flirt_line)
        "flirt_story_locked_husband": [
            _("Hands. Off. Your father is right there."),
            _("Behave. He's looking at us."),
            _("Not here. Not with him in the room."),
        ],
        "flirt_story_locked_husband.cold": [
            _("Did you really just do that? In front of your own father?"),
            _("Careful, boy. One more stunt like that and he hears about it, word for word."),
            _("Your father is sitting right there. Think very hard about what you just did."),
            _("Whatever that was, it ends now. Unless you'd like to explain it to him yourself."),
        ],
        "flirt_story_locked_husband.cold.femdom": [
            _("Look at him. That's your father. Now look at me and consider how stupid that just was."),
            _("Bold, trying that with him in the room. Stupid, but bold. Sit down."),
            _("One word from me and he deals with you himself. Choose silence, boy."),
        ],
        # ...on her first step ("cold"): she has no interest in him, and says so. No "yet", no promise, no hint
        "flirt_story_locked.cold": [
            _("Don't. Ever."),
            _("Save the charm for girls your age."),
            _("Are you trying to be funny? Don't."),
            _("I'm not one of your little college friends. Keep your distance."),
            _("Flattery? From you? Go study."),
            _("I'm your father's wife. Whatever you think this is, it isn't."),
            _("That's the kind of thing you say once. There won't be a second time."),
        ],
        "flirt_story_locked.cold.femdom": [
            _("Who exactly do you think you're talking to? Know your place, boy."),
            _("No. And watch that mouth when you speak to me."),
            _("I'm not one of your little classmates. I'm the woman who runs this house. Act like you know it."),
            _("That mouth is going to cost you. Allowance or curfew, pick one."),
        ],
        "flirt_story_locked.cold.hardcore_sex": [
            _("One more word and you'll wish you'd kept your mouth shut."),
            _("You want to test me? Don't. You'd lose."),
            _("Say that again. I dare you."),
        ],
        "flirt_story_locked.cold.cute_sex": [
            _("No. And I'm only saying it kindly once."),
            _("I'll pretend I didn't hear that. For your sake."),
            _("You're getting a polite 'no' exactly once. Use it well."),
        ],
        "flirt_story_locked.cold.submissive": [
            _("That is not appropriate. It will never be appropriate. Are we clear?"),
            _("I'm going to walk away now, and we will both pretend that never happened."),
            _("Please don't make this house strange. I live here. So do you."),
        ],
        "flirt_story_locked": [
            _("Not so fast. You haven't earned that."),
            _("Cute. Try that again and see what happens."),
            _("We're not there, boy. Keep talking, though. You're almost interesting."),
        ],

        # ==========================
        # Her step's voice outside the locks (story_steps.rpy reads these through story_rod_line):
        #   talk_greet.<step>            her first word when he opens the talk, once a day (_story_talk_greet)
        #   talk_greet.after.<step>.<route>  the STORY_AFTER_DAYS days after an unlock: the route colors it
        #   gift_react.<step>            one extra word for a gift from HIM (give_gift), once a day
        #   outing_accept.<step>         her word when she agrees to follow him (the act "outing")
        # Trait variants ("<key>.<trait>") resolve first. No promise and no warmth on the cold keys.
        # ==========================
        "talk_greet.cold": [
            _("Make it quick. I have a day, and you're not on it."),
            _("What. Speak or move along."),
            _("You have thirty seconds. Spend them well."),
        ],
        "talk_greet.cold.femdom": [
            _("Posture. Then speak."),
            _("Quickly, boy. I don't repeat myself and I don't wait."),
        ],
        "talk_greet.she_decides": [
            _("...You again. Fine. Two minutes."),
            _("Hm. I was starting to wonder when you'd show up."),
            _("Talk. I'm listening. That's already more than most people get."),
        ],
        "talk_greet.giving_in": [
            _("There you are. Come here, let me look at you."),
            _("Finally. Today was endless, and you're the first tolerable thing in it."),
            _("Closer, [Player.Name]. I don't talk across rooms."),
        ],
        "talk_greet.his": [
            _("There's my boy. Come here."),
            _("I was about to go looking for you. Don't make me do that. I always find what I look for."),
            _("Mm. Come stand where I can reach you."),
        ],
        # the days right after an unlock: how she climbed colors her first word (love is never bought,
        # blackmail is never won over)
        "talk_greet.after.she_decides.love": [
            _("...About the dinner. Nothing changed. Stop looking at me like something changed."),
            _("You keep smiling at me since Sunday. Stop it. ...Not entirely."),
        ],
        "talk_greet.after.she_decides.inbt": [
            _("What happened at that table stays at that table. God, I must have been insane."),
            _("Wine. It was the wine. We'll call it the wine and never discuss it."),
        ],
        "talk_greet.after.she_decides.obed": [
            _("You put my hand where you wanted it, and I let you. I'm still deciding what that makes us."),
            _("Don't get used to giving orders. ...Don't stop either. I haven't decided."),
        ],
        "talk_greet.after.she_decides.evidence": [
            _("You know what you know. I keep what I keep. As long as that balance holds, we're fine."),
            _("Every time you look at me now, I see that window. Careful what you do with what you saw."),
        ],
        "talk_greet.after.giving_in.love": [
            _("The other night... I'm not sorry. That's the problem. I'm not even a little sorry."),
            _("I came to you a mess and left... not a mess. We're not discussing what that means yet."),
        ],
        "talk_greet.after.giving_in.inbt": [
            _("I drove home at four in the morning with my coat over my pajamas. Me. ...And I'd do it again."),
            _("If anyone had seen me leave your dorm... don't let me think about it. Distract me."),
        ],
        "talk_greet.after.giving_in.obed": [
            _("'Take off your coat', you said. And I did. I keep hearing it. ...Say something else like that."),
            _("I'm tired of deciding everything, everywhere. With you I don't have to. That's new."),
        ],
        "talk_greet.after.giving_in.blackmail": [
            _("You collected your price. I paid it. Don't expect me to smile about it, boy."),
            _("I know exactly what you have on me. One day it won't be enough. Enjoy today."),
        ],
        "talk_greet.after.his.love": [
            _("I woke up in his bed thinking about you in it. I'm past saving, aren't I."),
            _("Say nothing. Just... stay close today."),
        ],
        "talk_greet.after.his.inbt": [
            _("I set our wedding photo back up before I left. My hands didn't even shake. ...What have you made of me."),
            _("His pillow, your name in my head. I should be terrified. I'm not."),
        ],
        "talk_greet.after.his.obed": [
            _("You pointed at the bed and I lay down. I run a household, boy, and I lay DOWN. ...Do it again sometime."),
            _("Whatever this is now, you steer it. I'm done pretending I want the wheel."),
        ],
        # a gift from HIM, by step (an extra word after the usual reaction)
        "gift_react.cold": [
            _("Put it on the table. ...It's not terrible."),
            _("A gift. Hm. Buying goodwill is a strategy, I suppose. A transparent one."),
            _("Fine, I'll keep it. Don't read anything into that."),
        ],
        "gift_react.cold.femdom": [
            _("Tribute? Good instinct, boy. Leave it there."),
            _("You may put it down. And no, this doesn't buy you anything."),
        ],
        "gift_react.she_decides": [
            _("...You remembered what I like. Dangerous skill. Keep it."),
            _("Hm. Acceptable. More than acceptable, and that annoys me."),
        ],
        "gift_react.giving_in": [
            _("You keep doing things my husband stopped doing fifteen years ago. It's unfair, really."),
            _("I'll keep it where he won't ask about it. ...Thank you, [Player.Name]."),
        ],
        "gift_react.his": [
            _("From my boy. ...I'll treasure it, and I'll ruin anyone who touches it."),
            _("Come here. Gifts get thanked properly in this house."),
        ],
        # she agrees to follow him (the act "outing", step 1+)
        "outing_accept.she_decides": [
            _("Ten minutes. I pick the route, you keep the pace."),
            _("Fine. Walk on my left and don't dawdle."),
        ],
        "outing_accept.giving_in": [
            _("...Alright. Somewhere quiet, where nobody knows your father."),
            _("Lead on. If anyone asks, I'm supervising you."),
        ],
        "outing_accept.his": [
            _("Anywhere. As long as I'm back before he starts calling. ...Actually, let him call."),
            _("Mm. Take me somewhere I can hold your arm without doing math about it."),
        ],

        # ==========================
        # Found in the shower (Shower.rpy SHOWER_STORY_STEPS / _shower_story_caught): her STEP speaks, never a college
        # girl's blush or "did you like it". Cold: outrage and authority, he is thrown out. She decides: she lets him
        # look as long as SHE wants, then sends him away. Giving in: she doesn't cover, he stays. His: she wants him in.
        #   shower_caught.<cat>.<step>             her first word (nude / partial = in underwear, half dressed / towel)
        #   shower_caught.reply.<route>.<step>     her answer to his (love / obed / inbt: his lines in SHOWER_STORY_STEPS);
        #                                          on cold / she_decides every one ends with him out
        #   shower_knock.<step>                    he knocks on the closed bathroom door (cold / she_decides: it stays
        #                                          shut; giving_in: she opens in a towel; his: she opens naked)
        #   shower_knock_open.<step>               when she opens it
        # Never a word on where her husband is: he may be out (a line only says what is true).
        # ==========================
        "shower_caught.nude.cold": [
            _("Eyes on the floor. Keep them there and back out of my bathroom. NOW."),
            _("You walked in on your father's wife. Think very carefully about what you do next."),
            _("Out. You have three seconds before I call your father in here."),
            _("Do you have any idea whose bathroom this is? Turn around."),
        ],
        "shower_caught.partial.cold": [
            _("I'm getting dressed, and you're still standing there. Turn around."),
            _("Does this look like your room to you? Eyes on the wall, boy."),
            _("Turn around. If you're still facing me when I count to three, your father hears about this tonight."),
        ],
        "shower_caught.towel.cold": [
            _("I'm in a towel and you're in my bathroom. One of us is leaving, and it isn't me."),
            _("Knocking. It's a simple concept, boy. You'll practice it on your way out."),
            _("Whatever you came for, it can wait until I'm dressed and you're gone."),
        ],
        "shower_caught.reply.love.cold": [
            _("Sorry is for spilled coffee. This was my bathroom. Get out."),
            _("Then learn to knock. Close the door on your way out."),
            _("You didn't know. That door has a handle and a lock for a reason. Out."),
        ],
        "shower_caught.reply.obed.cold": [
            _("No? Then you can explain yourself to your father tonight. Out."),
            _("Brave. Let's see how brave you are when your allowance stops. Get out of my sight."),
            _("Say that again and you'll be ringing the bell of this house like a stranger. Out."),
        ],
        "shower_caught.reply.inbt.cold": [
            _("A body. Your father's WIFE's body. Get out before I make this a family discussion."),
            _("Don't tell me to relax in my own bathroom. Out."),
            _("Just a body. Then you won't mind never seeing it again. Out."),
        ],
        "shower_knock.cold": [
            _("What the hell do you want? I'm busy. Go away."),
            _("Are you deaf? It's occupied! Get lost, boy."),
            _("I don't care what it is. Walk away before I lose my patience."),
            _("Who told you to come bother me? Leave. Now."),
        ],
        # the locked bathroom door: first try, she yells through the door
        "shower_locked.cold": [
            _("It's locked. Figure it out. Go away."),
            _("What part of 'locked' do you not understand? Leave."),
            _("The door is locked for a reason. Walk away, boy."),
        ],
        # retry: she thinks it's her husband, loses all patience
        "shower_locked_retry.cold": [
            _("Are you an idiot? I already said it's locked. Go finish your paperwork or something."),
            _("Did you not hear me the first time? It's locked. Go away before I come out there and make you."),
            _("Twice? Are you stupid or just deaf? Get out of my sight."),
        ],
        # she decides: no scream, no towel in a hurry. He looks because she allows it, and only that long
        "shower_caught.nude.she_decides": [
            _("Well. Look who forgot how doors work. ...Go on, look. You have five seconds."),
            _("You again. I decide how much of this you get to see, and today it isn't much."),
            _("Don't stammer. If you're going to stare, at least do it with some dignity."),
        ],
        "shower_caught.partial.she_decides": [
            _("Halfway dressed, and you halfway into my bathroom. Careful which half you pick."),
            _("Seen enough? Don't answer. I'll tell you when you have."),
        ],
        "shower_caught.towel.she_decides": [
            _("A towel. That's what you get today. Be grateful it's a small one."),
            _("Next time, knock. Then I decide whether you come in."),
        ],
        "shower_caught.reply.love.she_decides": [
            _("Polite. I like polite. Now go, before I change my mind about liking it."),
            _("Good manners. Keep them. ...Out, [Player.Name]."),
        ],
        "shower_caught.reply.obed.she_decides": [
            _("Are you. ...Fine. Ten more seconds, because I allow it. Then out."),
            _("Bold. I'll let it slide once. Now get out of my bathroom."),
        ],
        "shower_caught.reply.inbt.she_decides": [
            _("Nothing in here happens on your account, boy. It happens on mine. Now go."),
            _("Cheeky. Take that thought back to your own bed. Out."),
        ],
        "shower_knock.she_decides": [
            _("Not now. When I want company in here, you'll know."),
            _("It's occupied. Wait your turn, boy."),
        ],
        # giving in: she doesn't cover, and she doesn't send him away
        "shower_caught.nude.giving_in": [
            _("...You should leave. You won't, will you. ...Close the door."),
            _("There you are. Don't just stand there. Close the door before someone sees you looking at me like that."),
            _("I should be screaming at you. ...I'm not. Draw your own conclusions."),
        ],
        "shower_caught.partial.giving_in": [
            _("Caught me halfway. Which way do you think I was going, [Player.Name]?"),
            _("Don't look away. You came all this way to see something."),
        ],
        "shower_caught.towel.giving_in": [
            _("Just a towel between us. Funny how thin it suddenly feels."),
            _("I was about to get dressed. ...Maybe I'll take my time."),
        ],
        "shower_caught.reply.love.giving_in": [
            _("Say that again. Slowly. Nobody has said it to me like that in a long time."),
            _("...Don't say things like that to me in here. I'll start believing you."),
        ],
        "shower_caught.reply.obed.giving_in": [
            _("Bossy. ...Fine. Look."),
            _("You give orders in my bathroom now? ...Alright. Look all you want."),
        ],
        "shower_caught.reply.inbt.giving_in": [
            _("Then lock the door. Or don't. I'm done pretending I care."),
            _("I know. My heart is pounding. Don't you dare move."),
        ],
        "shower_knock.giving_in": [
            _("...One moment."),
            _("Is that you? ...Give me a second."),
        ],
        "shower_knock_open.giving_in": [
            _("Well? Come in before I change my mind."),
            _("Quickly. Close it behind you."),
        ],
        # his: she wants him in there
        "shower_caught.nude.his": [
            _("There's my boy. Come here, the water's warm."),
            _("Mm, perfect timing. I was just thinking about you."),
            _("Don't just stand there looking. Get in here or hand me a towel, and I know which one you'll pick."),
        ],
        "shower_caught.partial.his": [
            _("Help me with this, would you? Or the opposite. Your call."),
            _("You always find me at the best moments."),
        ],
        "shower_caught.towel.his": [
            _("You're late. I was hoping you'd catch me in the water."),
            _("This towel is coming off either way. Want to be the reason?"),
        ],
        "shower_caught.reply.love.his": [
            _("Only for you. Remember that."),
            _("Come here and say it against my neck."),
        ],
        "shower_caught.reply.obed.his": [
            _("Like this? ...Slowly enough for you?"),
            _("Mm. Take your time. I'm not going anywhere."),
        ],
        "shower_caught.reply.inbt.his": [
            _("Open? ...God, you'll be the end of me. Leave it open."),
            _("Anyone could see. ...Leave it."),
        ],
        "shower_knock.his": [
            _("Is that you? Get in here."),
            _("It's open for you. Come in."),
        ],
        "shower_knock_open.his": [
            _("Took you long enough."),
            _("Close the door. Come here."),
        ],
        # after the break (trait submissive): she waits for his word, even in there
        "shower_caught.nude.his.submissive": [
            _("Oh. It's you. ...Do you want me to stay like this?"),
            _("I hoped it would be you. Tell me what you want."),
        ],
        "shower_caught.towel.his.submissive": [
            _("Should I keep the towel on? ...You decide."),
            _("I waited. I didn't know if you'd come. ...You came."),
        ],
        "shower_knock.his.submissive": [
            _("Yes? ...Come in. Please."),
        ],

        # ════ AFTER THE BREAK (trait submissive): the one who waits for his word ════
        "talk_greet.his.submissive": [
            _("You're here. ...Tell me what you need. Please."),
            _("I kept the evening open. In case you wanted it."),
            _("Good timing. I was about to invent a reason to call you."),
        ],
        "gift_react.his.submissive": [
            _("For me? You don't have to buy me anything. I'm already... you know what I am."),
            _("...Thank you. I'll keep it where he won't ask about it."),
        ],
        "outing_accept.his.submissive": [
            _("Yes. Wherever you decide. I like not deciding."),
            _("Give me ten minutes and I'm yours for the day. ...I'll tell him something."),
        ],
    }
