# ============================================================
# events.rpy
# Event & memory system (witnesses, history, queries)
# ============================================================

init -999 python:
    from collections import defaultdict

    # Py2/Py3 compat for strings (Ren'Py is usually Py2 on older builds)
    try:
        _STR_TYPES = (basestring,)
    except Exception:
        _STR_TYPES = (str,)

    # ------------------------------
    # SceneEvent
    # ------------------------------
    class SceneEvent(python_object):
        """
        A normalized event record.
        - event_type: string ("saw_nude", "cheating", "sex", "kiss", ...)
        - subject: who did it (string id, object with Id/Name, or "Player")
        - target: who it happened to (string id or object)
        - tags: list of strings for extra semantics ("player_nude", "camera", "with_other_girl", ...)
        - day/time: numeric timeline (optional but recommended)
        - location: string code (optional)
        - meta: free dict for anything else
        """
        __slots__ = ("event_type", "subject", "target", "tags", "day", "time", "location", "meta")

        def __init__(self, event_type, subject=None, target=None, tags=None, day=0, time=0, location=None, meta=None):
            self.event_type = str(event_type) if event_type is not None else "unknown"
            self.subject = subject
            self.target = target
            self.tags = list(tags) if tags else []
            self.day = int(day) if day is not None else 0
            self.time = int(time) if time is not None else 0
            self.location = location
            self.meta = dict(meta) if meta else {}

        def has_tag(self, tag):
            return tag in self.tags

        def add_tag(self, tag):
            if tag and tag not in self.tags:
                self.tags.append(tag)

        def __repr__(self):
            return "<SceneEvent %s day=%s time=%s tags=%s>" % (self.event_type, self.day, self.time, self.tags)

    # ------------------------------
    # Small helpers
    # ------------------------------
    def _get_id(x):
        if x is None:
            return None
        if isinstance(x, _STR_TYPES):
            return x
        if hasattr(x, "Id"):
            return x.Id
        if hasattr(x, "Name"):
            return x.Name
        return str(x)

    def _get_name(x):
        if x is None:
            return None
        if isinstance(x, _STR_TYPES):
            return x
        if hasattr(x, "Name"):
            return x.Name
        if hasattr(x, "Id"):
            return x.Id
        return str(x)

    # ------------------------------
    # Memory API (per-girl)
    # ------------------------------
    def ensure_memory(girl):
        if girl is None:
            return []
        if not hasattr(girl, "Memory") or girl.Memory is None:
            girl.Memory = []
        if not hasattr(girl, "MemoryIndex") or girl.MemoryIndex is None:
            # Fast counts by event_type and tag
            girl.MemoryIndex = {
                "type_count": defaultdict(int),
                "tag_count": defaultdict(int),
            }
        return girl.Memory

    def _rebuild_memory_index(girl):
        ensure_memory(girl)
        girl.MemoryIndex["type_count"].clear()
        girl.MemoryIndex["tag_count"].clear()
        for e in girl.Memory:
            girl.MemoryIndex["type_count"][e.event_type] += 1
            for t in e.tags:
                girl.MemoryIndex["tag_count"][t] += 1

    def remember_event(girl, event, max_events=250):
        """
        Append an event into girl's memory with lightweight indexing.
        """
        if girl is None or event is None:
            return

        ensure_memory(girl)

        girl.Memory.append(event)

        # Index counts
        girl.MemoryIndex["type_count"][event.event_type] += 1
        for t in event.tags:
            girl.MemoryIndex["tag_count"][t] += 1

        # Trim oldest (keep index consistent)
        if max_events and len(girl.Memory) > int(max_events):
            girl.Memory = girl.Memory[-int(max_events):]
            _rebuild_memory_index(girl)

    # ------------------------------
    # Queries (per-girl)
    # ------------------------------
    def count_events(girl, event_type=None, tag=None):
        if girl is None:
            return 0
        ensure_memory(girl)

        if event_type is not None:
            return int(girl.MemoryIndex["type_count"].get(event_type, 0))
        if tag is not None:
            return int(girl.MemoryIndex["tag_count"].get(tag, 0))
        return len(girl.Memory)

    def has_event(girl, event_type=None, tag=None):
        return count_events(girl, event_type=event_type, tag=tag) > 0

    def last_event(girl, event_type=None, tag=None):
        if girl is None:
            return None
        ensure_memory(girl)

        for e in reversed(girl.Memory):
            if event_type is not None and e.event_type != event_type:
                continue
            if tag is not None and tag not in e.tags:
                continue
            return e
        return None

    def has_seen_subject_doing(girl, event_type, subject_id):
        if girl is None:
            return False
        ensure_memory(girl)
        sid = _get_id(subject_id)
        for e in reversed(girl.Memory):
            if e.event_type == event_type and _get_id(e.subject) == sid:
                return True
        return False

    def has_seen_pair(girl, event_type, subject_id, target_id):
        if girl is None:
            return False
        ensure_memory(girl)
        sid = _get_id(subject_id)
        tid = _get_id(target_id)
        for e in reversed(girl.Memory):
            if e.event_type == event_type and _get_id(e.subject) == sid and _get_id(e.target) == tid:
                return True
        return False

    # ------------------------------
    # Central dispatcher
    # ------------------------------
    def register_scene_event(
        event_type,
        subject=None,
        target=None,
        witnesses=None,
        tags=None,
        day=0,
        time=0,
        location=None,
        meta=None,
        max_events=250
    ):
        """
        Creates an event and stores it to every witness memory.
        This is the main entry point you should call from scenes.
        """
        ev = SceneEvent(
            event_type=event_type,
            subject=subject,
            target=target,
            tags=tags or [],
            day=day,
            time=time,
            location=location,
            meta=meta
        )

        if witnesses:
            for g in witnesses:
                remember_event(g, ev, max_events=max_events)

        return ev

    # ------------------------------
    # Optional: auto-witness helpers
    # ------------------------------
    def get_witnesses_at_location(girl_list, location_code):
        """
        Returns girls currently at a given location code.
        Only checks girl.loc if present.
        """
        if not girl_list:
            return []
        out = []
        for g in girl_list:
            if g is None:
                continue
            if hasattr(g, "loc") and g.loc == location_code:
                out.append(g)
        return out

    def get_witnesses_except(girl_list, exclude=None):
        """
        Removes exclude (single girl or list) from a girl list.
        """
        if not girl_list:
            return []
        if exclude is None:
            return list(girl_list)

        if not isinstance(exclude, (list, tuple, set)):
            exclude = [exclude]

        excl_ids = set([_get_id(x) for x in exclude])
        return [g for g in girl_list if _get_id(g) not in excl_ids]
