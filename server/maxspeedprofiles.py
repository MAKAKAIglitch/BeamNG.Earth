"""Passenger-car speed defaults and OSM implicit maxspeed values for the CIS.

Values are km/h. Posted numeric limits always take precedence. These profiles are
used only for the twelve explicitly supported CIS countries; every other
country keeps the pre-existing speed model.
"""

import re


# Profile values for a passenger car without a trailer. "trunk_divided" is
# used only where the national rule distinguishes a divided carriageway.
PROFILES = {
    "AM": {"urban": 60, "rural": 90, "motorway": 110, "trunk": 90, "living_street": 20, "zone30": 30},
    "AZ": {"urban": 60, "rural": 90, "motorway": 110, "trunk": 90, "living_street": 20, "zone30": 30},
    "BY": {"urban": 60, "rural": 90, "motorway": 120, "trunk": 120, "living_street": 20, "zone30": 30},
    "GE": {"urban": 60, "rural": 90, "motorway": 110, "trunk": 90, "living_street": 20, "zone30": 30},
    "KG": {"urban": 60, "rural": 90, "motorway": 110, "trunk": 90, "living_street": 20, "zone30": 30},
    "KZ": {"urban": 60, "rural": 100, "motorway": 140, "trunk": 100, "trunk_divided": 110,
           "living_street": 20, "zone30": 30},
    "MD": {"urban": 50, "rural": 90, "motorway": 110, "trunk": 90, "living_street": 20, "zone30": 30},
    "RU": {"urban": 60, "rural": 90, "motorway": 110, "trunk": 90, "living_street": 20, "zone30": 30},
    "TJ": {"urban": 60, "rural": 90, "motorway": 110, "trunk": 90, "living_street": 20, "zone30": 30},
    # Turkmenistan's published general guidance gives 60 in settlements and
    # 90 outside them; no higher general motorway allowance is assumed.
    "TM": {"urban": 60, "rural": 90, "motorway": 90, "trunk": 90, "living_street": 20, "zone30": 30},
    "UA": {"urban": 50, "rural": 90, "motorway": 130, "trunk": 90, "trunk_divided": 110,
           "living_street": 20, "zone30": 30},
    "UZ": {"urban": 70, "rural": 100, "motorway": 110, "trunk": 100, "living_street": 20, "zone30": 30},
}

COUNTRIES = frozenset(PROFILES)
_TAG = re.compile(r"^([A-Za-z]{2}):([A-Za-z0-9_-]+)$")
# Older local data can contain this transposition. Keep the alias narrow to RU.
_ALIASES = {("RU", "rual"): "rural"}


def resolve_tag(value):
    """Resolve a symbolic OSM maxspeed value (for example 'RU:rural') to km/h.

    Numeric limits are handled by osmtags' numeric parser. Unknown tags,
    country codes and zone names return None rather than guessing.
    """
    if value is None:
        return None
    match = _TAG.fullmatch(str(value).strip())
    if match is None:
        return None
    country, zone = match.group(1).upper(), match.group(2).lower()
    zone = _ALIASES.get((country, zone), zone)
    profile = PROFILES.get(country)
    return profile.get(zone) if profile is not None else None


def default_kmh(country, spec):
    """Default passenger-car limit for a CIS country and a road Spec, else None.

    A divided trunk is recognised from the road's own one-way geometry and
    lane count. Unknown countries deliberately retain the caller's old fallback.
    """
    profile = PROFILES.get(str(country or "").upper())
    if profile is None or spec is None:
        return None

    cls = str(getattr(spec, "cls", "") or "")
    urban = bool(getattr(spec, "urban", False))
    if cls == "living_street":
        return profile["living_street"]
    if cls == "motorway":
        return profile["motorway"]
    if urban:
        return profile["urban"]

    if cls == "trunk":
        lanes = getattr(spec, "lanes", None)
        try:
            divided = bool(getattr(spec, "oneway", False)) and int(lanes or 0) >= 2
        except (TypeError, ValueError):
            divided = False
        if divided and "trunk_divided" in profile:
            return profile["trunk_divided"]
        return profile["trunk"]
    return profile["rural"]
