# ============================================================
# scene_lines_nerd.rpy... the nerd trait BEFORE and AT her orgasm (scene_lines.rpy keys, read by scene_pick_line)
#
# Tester 2026-10-11 (the author's go): a nerd came down from her orgasm talking data and grades (Tenny's verdicts,
# her anal pools) with nothing of that voice in the build-up, so the comedown sounded sillier than it is. These are
# the counterparts: she narrates her own arousal like an experiment going off the rails, loses the vocabulary as she
# gets close, and gets it back while she comes down. A scene's own pool beats a bare ".nerd" (event.scene wins over
# event.mod), so the moans and her orgasm are written WITH the scene; the base keys carry the rest.
# Short modifier name "nerd" (scene_lines.rpy header). The cute modifier comes before nerd: a cute nerd keeps her
# cute pools where both exist.
# ============================================================

init 1 python:

    SCENE_LINES.update({

        # ══════════════════════════════════════════════════════════
        #  BUILD-UP MOANS (moan.speedN.<scene>.nerd)
        # ══════════════════════════════════════════════════════════
        "moan.speed1.hj.nerd": [
            _("Okay... so this is the part the textbooks skip entirely..."),
            _("I'm... taking mental notes. For science. Mostly."),
            _("Your pulse is... I can feel it. That's a data point."),
        ],
        "moan.speed2.hj.nerd": [
            _("My grip keeps... adjusting on its own. That's not a conscious variable..."),
            _("I can't keep count of the strokes anymore... and I count everything..."),
            _("This is... way more responsive than any diagram..."),
        ],
        "moan.speed3.hj.nerd": [
            _("I can't... think in sentences... anymore...!"),
            _("Forget the notes... forget... all of it...!"),
            _("My hand's on autopilot and my brain is... gone...!"),
        ],
        "moan.speed1.bj.nerd": [
            _("Mmh... I read about the technique... it's... different in practice..."),
            _("Mm... okay... hypothesis: breathing through the nose... works..."),
            _("Mmh... I'm... adjusting the angle... for... data..."),
        ],
        "moan.speed2.bj.nerd": [
            _("Mmph... I can't... track anything... mmh..."),
            _("Mmh... so much for... controlled conditions... mmph..."),
            _("Mmm... my eyes keep... watering... that's a known... mmh..."),
        ],
        "moan.speed3.bj.nerd": [
            _("Mmph! Mmmh...! Mmph...!"),
            _("Glk... mmh... can't... mmph...!"),
            _("Mmmh! Mmph... mmh...!"),
        ],
        "moan.speed1.tj.nerd": [
            _("I... never thought about the friction coefficient of... this..."),
            _("Okay. Pressure, angle, rhythm. I can optimize this..."),
            _("This is... a lot of surface area to keep track of..."),
        ],
        "moan.speed2.tj.nerd": [
            _("I lost the rhythm I was... counting... ah..."),
            _("The way you look at them... it's messing with my... focus..."),
            _("I'm supposed to be... controlling this... and I'm not..."),
        ],
        "moan.speed3.tj.nerd": [
            _("Faster... I can't... hold the pattern...!"),
            _("Forget optimizing... just... don't stop...!"),
            _("My arms... my head... nothing's working right...!"),
        ],
        "moan.speed1.cowgirl.nerd": [
            _("Okay... I'm in charge of the... variables here... supposedly..."),
            _("Every angle changes... everything... I'm mapping it..."),
            _("I read that this position... ah... gives the girl control... in theory..."),
        ],
        "moan.speed2.cowgirl.nerd": [
            _("My hips aren't... following the plan... anymore..."),
            _("I can't... keep the rhythm... I keep losing the count..."),
            _("This was supposed to be... a controlled experiment...!"),
        ],
        "moan.speed3.cowgirl.nerd": [
            _("I can't... I can't think... I can't...!"),
            _("Forget control... forget... everything...!"),
            _("Oh god... oh god... there's no... word for this...!"),
        ],
        "moan.speed1.full_nelson.nerd": [
            _("I... can't move... which eliminates every variable but... you..."),
            _("I did not read about this one... anywhere..."),
            _("Okay... okay... deep breaths... that's the only thing I control..."),
        ],
        "moan.speed2.full_nelson.nerd": [
            _("I can't move and I can't... think... that's... two systems down..."),
            _("My body's reacting... without asking me... at all..."),
            _("This is... not in any syllabus... ahh..."),
        ],
        "moan.speed3.full_nelson.nerd": [
            _("I CAN'T... I CAN'T... AAAH...!"),
            _("Nothing works... nothing... AAAH...!"),
            _("I'm... gone... I'm gone...!"),
        ],
        "moan.speed1.anal.nerd": [
            _("Okay... this is... very different from the literature..."),
            _("Breathe... relax... the articles all said... relax..."),
            _("I'm... logging this... as inconclusive... so far..."),
        ],
        "moan.speed2.anal.nerd": [
            _("Every study said this shouldn't... feel... ah..."),
            _("I'm revising... the whole... hypothesis..."),
            _("That's... a very unexpected result... ahh..."),
        ],
        "moan.speed3.anal.nerd": [
            _("I can't... explain... any of this...!"),
            _("The data... is... AAAH...!"),
            _("Don't... stop... I don't care what it proves...!"),
        ],
        "moan.speed1.fj.nerd": [
            _("I'm... genuinely curious how this works for you..."),
            _("Okay... pressure, arch, rhythm... I can do this..."),
            _("This is... weirdly fascinating..."),
        ],
        "moan.speed2.fj.nerd": [
            _("My toes keep... curling on their own... that's new data..."),
            _("I'm getting... worked up from... this? That's... not in any paper..."),
            _("I lost the rhythm... I keep... losing the rhythm..."),
        ],
        "moan.speed3.fj.nerd": [
            _("Faster... I can't... track it anymore...!"),
            _("Forget the method... just... don't stop...!"),
            _("I'm... I'm losing it... from this...!"),
        ],
        "moan.speed1.oral.nerd": [
            _("Oh... that's... nobody warned me it feels like... that..."),
            _("I'm... trying to stay objective... I can't..."),
            _("My hands... I don't know what to do with my... hands..."),
        ],
        "moan.speed2.oral.nerd": [
            _("My whole body is... reacting... I can't catalogue it..."),
            _("I can't... think... I can't even... ah..."),
            _("That's... that's... ahh... what are you doing...!"),
        ],
        "moan.speed3.oral.nerd": [
            _("I can't... I can't... AAAH...!"),
            _("Everything's... white... I can't... see...!"),
            _("Don't stop... don't you dare... stop...!"),
        ],
        "moan.speed1.masturbate.nerd": [
            _("I... never do this with someone watching... my hands are shaking..."),
            _("Okay... this is... observational research... for both of us..."),
            _("I'm... narrating it in my head... like a lab report... that's so stupid..."),
        ],
        "moan.speed2.masturbate.nerd": [
            _("I can't... keep the pace I... usually... ah..."),
            _("Having you watch changes... every... variable..."),
            _("I'm losing... my method... I'm just... ahh..."),
        ],
        "moan.speed3.masturbate.nerd": [
            _("I can't... I can't stop... I can't...!"),
            _("Watch me... I don't care... I can't think...!"),
            _("It's... it's happening... AAAH...!"),
        ],

        # ══════════════════════════════════════════════════════════
        #  HER ORGASM (girl_cum.<scene>.nerd; the base girl_cum.nerd exists)
        # ══════════════════════════════════════════════════════════
        "girl_cum.hj.nerd": [
            _("I'm... wait, I'm... from THIS? I'm... AAAH!"),
            _("Something's... building, I can't... AAAH!"),
        ],
        "girl_cum.bj.nerd": [
            _("Mmph... mmh... MMPH...!"),
            _("Mmmh... mmph... MMMH...!"),
        ],
        "girl_cum.tj.nerd": [
            _("I didn't... account for... THIS... AAAH!"),
            _("My body's... tensing... I can't... AAAH!"),
        ],
        "girl_cum.cowgirl.nerd": [
            _("I'm... I'm losing... all of it... AAAH!"),
            _("No control... no control... AAAH!"),
        ],
        "girl_cum.full_nelson.nerd": [
            _("I can't move... I can't... AAAAH!"),
            _("Everything's... going white... AAAH!"),
        ],
        "girl_cum.anal.nerd": [
            _("This... proves... nothing... AAAH!"),
            _("I'm... from... THERE... AAAAH!"),
        ],
        "girl_cum.fj.nerd": [
            _("From my... feet? I'm... AAAH!"),
            _("That's... impossible... AAAH!"),
        ],
        "girl_cum.oral.nerd": [
            _("I can't... I can't... AAAAH!"),
            _("Don't stop... don't... AAAH!"),
        ],
        "girl_cum.masturbate.nerd": [
            _("I'm... I'm cumming... watch me... AAAH!"),
            _("It's... it's... AAAH!"),
        ],
        "girl_cum_intense.nerd": [
            _("I can't... process... AAAAH!"),
            _("My notes... my brain... everything's... AAAH!"),
            _("There's no... word... for... AAAAH!"),
        ],
        "girl_cum_hard.nerd": [
            _("I CAN'T THINK... I CAN'T... EVERYTHING'S WHITE... AAAAAH!"),
            _("MY HEAD... IS... GONE... AAAAH!"),
        ],

        # ══════════════════════════════════════════════════════════
        #  COMING DOWN: the vocabulary comes back first (girl_post_cum[.scene].nerd)
        # ══════════════════════════════════════════════════════════
        "girl_post_cum.nerd": [
            _("Okay. Okay. That was... statistically significant."),
            _("I need a minute. My brain is... rebooting."),
            _("I'm going to need to revise... several assumptions."),
            _("That was... empirically... a lot."),
        ],
        "girl_post_cum.hj.nerd": [
            _("From my hand... on you... that shouldn't... okay. Noted."),
            _("I'm going to be thinking about that during lectures. Great."),
        ],
        "girl_post_cum.bj.nerd": [
            _("Hah... my jaw... and my brain... both need a minute."),
            _("I didn't expect... me... to get anything out of that. Interesting."),
        ],
        "girl_post_cum.tj.nerd": [
            _("I need to... recalibrate. Everything."),
            _("That was... not what the diagrams suggested. At all."),
        ],
        "girl_post_cum.cowgirl.nerd": [
            _("I was supposed to be in control of that. I was not."),
            _("Okay. Hypothesis rejected. I'm not in charge of anything up here."),
        ],
        "girl_post_cum.full_nelson.nerd": [
            _("I couldn't move and I still... okay. That's... going in the notes."),
            _("I'm shaking. All of me. That's... that's a lot of data."),
        ],
        "girl_post_cum.anal.nerd": [
            _("That was... different than I expected. It still proves nothing though."),
            _("Every study says this shouldn't happen to women... so what just happened to me?"),
        ],
        "girl_post_cum.fj.nerd": [
            _("From my feet. I'm going to need to read more about that."),
            _("That's... a very strange result. I'd like to replicate it."),
        ],
        "girl_post_cum.oral.nerd": [
            _("I... have no notes. None. My head is empty."),
            _("That was... I can't even describe the methodology. Just... that."),
        ],
        "girl_post_cum.masturbate.nerd": [
            _("I've... never finished that fast. The observer effect is real."),
            _("Okay. Being watched is... a variable I underestimated."),
        ],
        "girl_post_cum_intense.nerd": [
            _("I'm still shaking... I can't form a... a proper sentence..."),
            _("Give me a... minute. Or ten. My brain's... offline."),
            _("That was... above the scale. I don't have a scale for that."),
        ],
        "girl_post_cum_hard.nerd": [
            _("What... what was that... I've read everything and nothing... nothing covered that..."),
            _("I can't... I can't feel my legs... that's... that's not in any... anything..."),
        ],
        "girl_orgasm_dazed.nerd": [
            _("I can't... hold a thought. Any thought."),
            _("Words are... hard right now. Give me a second."),
        ],
        "girl_orgasm_exhausted.nerd": [
            _("I... I really can't take any more... my data's... all over the place..."),
            _("Please... I'm done... I can't even count anymore..."),
        ],
    })
