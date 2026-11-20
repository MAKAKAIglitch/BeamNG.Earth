"""Passenger-car speed defaults and OSM implicit maxspeed values for the CIS.

Values are km/h. Posted numeric limits always take precedence. The implicit
zone values follow OSM's country guidance; road-class defaults are kept
separately where national rules distinguish classes.
"""
import re


PROFILES = {
    "AM": {"urban": 60, "rural": 90, "motorway": 110, "trunk": 90, "living_street": 20},
    "AZ": {"urban": 60, "rural": 90, "motorway": 110, "trunk": 90, "living_street": 20},
    "BY": {"urban": 60, "rural": 90, "motorway": 120, "trunk": 90, "motorroad": 120, "living_street": 20,
           "classes": {"service": 20}},
    "GE": {"urban": 60, "rural": 90, "motorway": 110, "trunk": 90, "living_street": 20},
    "KG": {"urban": 60, "rural": 90, "motorway": 110, "trunk": 90, "living_street": 20},
    "KZ": {"urban": 60, "rural": 100, "motorway": 140, "trunk": 100, "divided": 110,
           "living_street": 20},
    "MD": {"urban": 50, "rural": 90, "motorway": 110, "trunk": 90, "living_street": 20},
    "RU": {"urban": 60, "rural": 90, "motorway": 110, "trunk": 90, "living_street": 20},
    "TJ": {"urban": 60, "rural": 90, "motorway": 110, "trunk": 90, "living_street": 20},
    # Turkmenistan's published general guidance gives 60 in settlements and
    # 90 outside them; no higher general motorway allowance is verified.
    "TM": {"urban": 60, "rural": 90, "motorway": 90, "trunk": 90, "living_street": 20},
    # UA:trunk is the OSM implicit value (110); a non-divided trunk defaults
    # to 90, while divided roads with separated directions may reach 110.
    "UA": {"urban": 50, "rural": 90, "motorway": 130, "trunk": 110, "trunk_default": 90,
           "divided": 110, "living_street": 20},
    "UZ": {"urban": 70, "rural": 100, "motorway": 110, "trunk": 100, "living_street": 30},
}

COUNTRIES = frozenset(PROFILES)
_TAG = re.compile(r"^([A-Za-z]{2}):([A-Za-z0-9_-]+)$")
# Some local data contains this transposition. Keep the alias narrow to RU.
_ALIASES = {("RU", "rual"): "rural"}


def resolve_tag(value):
    """Resolve a symbolic OSM maxspeed value (for example 'RU:rural') to km/h."""
    if value is None:
        return None
    match = _TAG.fullmatch(str(value).strip())
    if match is None:
        return None
    country, zone = match.group(1).upper(), match.group(2).lower()
    zone = _ALIASES.get((country, zone), zone)
    profile = PROFILES.get(country)
    return profile.get(zone) if profile is not None else None


def default_kmh(country, spec, motorroad=False):
    """Default passenger-car limit for a CIS country and road Spec, else None.

    A divided carriageway is recognised from its own one-way geometry and
    mapped lane count. Unknown countries keep the existing global fallback.
    """
    profile = PROFILES.get(str(country or "").upper())
    if profile is None or spec is None:
        return None

    cls = str(getattr(spec, "cls", "") or "")
    urban = bool(getattr(spec, "urban", False))
    if cls == "living_street":
        return profile["living_street"]
    if getattr(spec, "link", False):
        return profile.get("link", profile["rural"])
    if cls == "motorway":
        return profile["motorway"]
    if urban:
        return profile["urban"]
    if motorroad and "motorroad" in profile:
        return profile["motorroad"]

    if cls in {"trunk", "primary", "secondary"} and "divided" in profile:
        lanes = getattr(spec, "lanes", None)
        try:
            divided = bool(getattr(spec, "oneway", False)) and int(lanes or 0) >= 2
        except (TypeError, ValueError):
            divided = False
        if divided:
            return profile["divided"]
    if cls == "trunk":
        return profile.get("trunk_default", profile["trunk"])
    return profile.get("classes", {}).get(cls, profile["rural"])
