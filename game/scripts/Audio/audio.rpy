# ============================================================
# audio.rpy
# Centralised music management.
#
# Rules:
#   gym      → Gym.mp3            (always, regardless of time)
#   showers  → Shower.mp3         (always)
#   classroom→ Before Class.mp3   (always; overridden to During Exam
#                                   by exam_event while the exam runs)
#   pool     → Night Sound.mp3 at night / Day Sound.mp3 during the day
#   night    → Night Sound.mp3    (any other location at Night)
#   default  → Day Sound.mp3      (any other location, daytime)
# ============================================================

init python:

    def get_scene_music(location, time_index):
        """Return the audio track path for a given location + time slot."""
        if location == "gym":
            return "audio/Gym.mp3"
        if location in SHOWER_SPOTS:
            return "audio/Shower.mp3"
        if location == "classroom":
            return "audio/Before Class.mp3"
        if location == "pool":
            if time_index == NIGHT_INDEX:
                return "audio/Night Sound.mp3"
            return "audio/Day Sound.mp3"
        if time_index == NIGHT_INDEX:
            return "audio/Night Sound.mp3"
        return "audio/Day Sound.mp3"
