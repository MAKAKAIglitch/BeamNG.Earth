# Russian road infrastructure — experimental baseline

This branch adds a **Russia-only** regional layer to the existing BeamNG.Earth road pipeline. Every new country-specific rule described here is selected by the existing geographic country lookup and the ISO 3166-1 alpha-2 code `RU`.

The branch does not replace the original project's country profiles. Existing behavior inherited from `main` for every other country remains in place.

## Scope

The Russia-specific additions are limited to road infrastructure and road-edge appearance:

- carriageway and lane marking profiles;
- a restricted road-sign role profile;
- Russian directional-board colours and route-reference parsing;
- bend-only delineator placement;
- sidewalk and road-edge fallback materials;
- the concrete street-lamp share;
- suppression of one synthetic roadside-tree relocation heuristic.

No buildings, building styles, parks, new tree assets or general landscape profiles are added by this regional layer.

## Country selection

The marking, sidewalk, lamp, delineator, sign and vegetation rules use the project's geographic country lookup or the country code already supplied by the road pipeline. The new regional allowlists contain only `RU`.

A tile outside Russia therefore keeps the country behavior it had in `main`; it does not receive the Russian fallback merely because a server or player is located nearby.

## Road markings

`server/markings.py` adds a Russia-only profile. The renderer passes the mapped speed limit and urban/motorway context to `road_style()`.

The initial white longitudinal marking profile uses:

| Context | Dash | Gap |
|---|---:|---:|
| Built-up road, up to 60 km/h | 1 m | 3 m |
| Ordinary road, up to 60 km/h | 3 m | 9 m |
| Road above 60 km/h | 4 m | 12 m |
| Missing speed, built-up road | 1 m | 3 m |
| Missing speed, ordinary road | 3 m | 9 m |
| Missing speed, motorway | 4 m | 12 m |

Initial line widths are 0.10 m on ordinary roads and 0.15 m on motorways; edge-line widths are 0.10 m and 0.20 m respectively. The profile is a conservative visual baseline, not a complete implementation of every Russian marking type.

Approach lines, special yellow stopping/parking lines, bus-stop boxes, stop lines, arrows, text, parking symbols and temporary work-zone markings still need dedicated geometry and placement rules.

## Road signs

`server/data/sign_systems.json` adds a restricted Russian profile. It allows only a subset of common priority, warning, prohibition and information roles, rather than enabling every role known to the renderer.

The profile currently uses the project's Vienna-family atlas and is explicitly marked `verified: false`. It is a placement/role starter profile, not an exact Russian sign-artwork catalogue.

## Direction boards

`server/data/dirsigns_styles.json` defines the Russian directional-board colour scheme:

- green for motorways;
- blue for other roads;
- white for signs inside built-up areas.

Russian route references recognise Cyrillic and Latin forms of the M/R/A/K/N prefixes, as well as E-road references. Route-network matching remains unverified because OSM relations and network naming are not complete or consistent for every route.

## Delineators

`server/delineatorprofiles.py` gives Russia a bend-only policy based on GOST 33151-2014 §4.2.4. Straight-road installation depends on road/site conditions such as embankment and traffic information that the current road graph does not reliably provide.

The generator therefore does not create blanket straight-road rows for Russia. Existing bend-marker geometry remains an approximation; exact radius-dependent spacing and site eligibility still need further validation.

## Sidewalks and road edges

`server/europewalks.py` adds a Russian fallback palette preferring asphalt, concrete, slabs and light asphalt. This is used only where a more specific mapped surface is unavailable. Explicitly mapped surfaces keep priority.

## Street lighting

`server/citylamps.py` sets a deterministic 80% concrete-post share for Russian lamp placements, with the remainder using the steel-post family. This is a scenery mix, not an official national statistic. Existing lamp positions, attachment layout, lamp heads and collision handling remain on the existing placement pipeline.

## Roadside trees

The vegetation generator normally shifts a canopy maximum found over a road corridor into a synthetic tree-pit position beside the curb. That relocation heuristic is disabled for Russia because it can create artificial rows of roadside trees on ordinary roads.

This does not delete mapped trees, remove forests or thin vegetation away from the road. It only prevents that specific synthetic relocation in Russia.

## Existing infrastructure inherited from main

Russia already has a roadside pole kit in the original `europeinfra.py` country table. This branch keeps that existing kit; it does not introduce new non-Russian regional kits. Existing guardrail country profiles are also retained from the base project. The optional European guardrail extension remains controlled by its existing environment switch and is not enabled by this Russia-only layer.

## Cache and validation

Relevant profile/version tokens are updated so cached regional tiles and generated sign faces can be rebuilt when their inputs change.

Tests cover the Russian marking speed bands and renderer integration, Russian sign allowlisting, directional-board rules, bend-only delineator behavior, the Russian sidewalk palette, concrete lamp selection and the tree-relocation policy.

The Python test suite and BeamNG in-game visual/performance checks must still be run against the packaged branch. Passing unit tests alone does not establish exact real-world placement or visual correctness.

## Russian standards and references

- GOST R 51256-2018 — road marking dimensions and dash patterns:  
  https://protect.gost.ru/gost/details/e84660db-4e3b-4c82-9627-c142a36355d2
- ODM 218.6.1.009-2025 — recommended marking lengths in built-up areas:  
  https://base.garant.ru/412371764/
- GOST R 52290-2024 — road-sign designs and directional-board colours:  
  https://protect.gost.ru/gost/details/39b75217-29bd-492b-94f4-c0dccb72b299
- GOST R 52289-2019 — road-sign placement and mounting:  
  https://base.garant.ru/73728515/
- GOST 33151-2014 — road arrangement elements and delineator placement:  
  https://base.garant.ru/71454660/

These standards are references for the visual baseline; the implementation is not presented as a complete legal or engineering reproduction of every Russian road.
