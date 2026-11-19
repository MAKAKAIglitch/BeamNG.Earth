# CIS road infrastructure — experimental baseline

This branch develops the existing BeamNG.Earth road pipeline for Russia and
other post-Soviet countries. Scope is deliberately limited to **road
infrastructure**: carriageway markings, road signs, directional boards,
delineators, guardrails, street lamps, roadside poles and sidewalks/pavement.
It does not add buildings, parks, street trees, landscaping or new vegetation.

This is a test implementation, not a claim that every country has been
reproduced to its complete current legal standard. Where a national source or
local photographic inventory is missing, the profile is labelled provisional.

## Countries

The shared first-pass set is:

`AM AZ BY GE KG KZ MD RU TJ TM UA UZ`

The country profiles use the project's existing country-boundary lookup.
They do not infer a country from a nearby airport or from the player's home
location.

## Road markings

`server/markings.py` provides the shared post-Soviet starting profile. The
road renderer calls `road_style()` with the road's mapped speed limit and
context:

| Context | Paint | Gap | Use |
|---|---:|---:|---|
| Ordinary road, mapped limit up to 60 km/h | 3 m | 9 m | 1:3 broken-line family |
| Mapped limit above 60 km/h | 4 m | 12 m | 1:3 broken-line family |
| Speed missing, ordinary/urban road | 3 m | 9 m | conservative fallback |
| Speed missing, motorway | 4 m | 12 m | high-speed fallback |

The implementation uses white as the permanent longitudinal marking colour.
The initial widths are 0.10 m on ordinary roads and 0.15 m on motorways; edge
line widths are 0.10 m and 0.20 m respectively. Existing US, German, British
and other country profiles are kept separate.

For Russia, the speed split follows the 1.5 line family in GOST R 51256-2018:
3/9 m is one of the options at limits up to 60 km/h and 4/12 m is the
high-speed option above 60 km/h. The renderer only knows the mapped speed
limit when that data is present; it does not invent one.

The full marking catalogue is not implemented yet. Approach line 1.6, special
yellow stopping/parking lines, bus-stop boxes, stop lines, arrows, text,
parking symbols and temporary work-zone markings still need their own
geometry and placement rules. They are not approximated by changing the
centre-line style.

## Roadside signs and direction boards

`server/data/sign_systems.json` now includes a restrained, explicitly
unverified Vienna-family sign profile for RU, BY, KZ, KG, TJ, TM, UZ, AM, AZ,
GE and MD. It only allows a subset of common priority, warning and information
roles. This means the renderer does not blindly place every role it knows for
these countries. It is a starter atlas, not an exact national sign album.
Ukraine's existing profile is unchanged.

The Russian direction-board profile in
`server/data/dirsigns_styles.json` uses the colour rules in GOST R 52290-2024:
green for motorways, blue for other roads, and white for signs inside built-up
areas. Russian route references recognise Cyrillic and Latin forms of the
M/R/A/K/N prefixes, as well as E-road references. The route-network matching
is still marked unverified because upstream map data uses several network
naming conventions and not every Russian route has a complete relation.

## Delineators, poles and barriers

Straight-road delineator rows are suppressed for the post-Soviet profiles.
Russia's GOST 33151-2014 makes straight-road installation conditional on road
type, embankment height and traffic volume; these facts are not reliably
available from the current road graph. Curve-only markers remain as a visual
approximation using the existing bend-marker pipeline. They are not yet an
exact implementation of every radius-dependent spacing value in Table 4.
Kazakhstan references ST RK 1412-2017; the other countries remain provisional
until their current national documents and local road examples have been
reviewed.

The regional roadside kit now includes Central Asia (KZ, KG, TJ, TM and UZ)
alongside the existing RU/BY/UA/Caucasus entries. It uses existing generated
concrete/wood pole families, delineator families and guardrail families.
These are representative shared asset families, not measured claims about
national equipment shares.

The street-lamp profile increases the concrete-post share in post-Soviet
countries. This is a deterministic scenery mix, not an official national
statistic. Existing positions, clearances, collision shapes and lamp heads
remain on the existing placement pipeline.

## Sidewalks and vegetation

Post-Soviet pavement palettes prefer asphalt, concrete, concrete slabs and
simple pavers. These choices affect only sidewalk/road-edge material fallback;
explicitly mapped surfaces keep priority.

The vegetation generator normally moves a canopy top found on a road corridor
to a tree-pit position beside the curb. For the post-Soviet country set that
heuristic move is disabled. A crown that lands inside the road/sidewalk
exclusion corridor is therefore not turned into a synthetic roadside tree.
This does **not** delete mapped trees, remove forests, or thin vegetation away
from road corridors. It only suppresses the road-to-verge relocation that
created artificial rows of street trees.

## Cache and validation

Relevant road, vegetation, regional infrastructure and generated direction
face versions were bumped so old tiles/textures are not silently reused.

New/extended tests cover:

- CIS country marking profiles, speed bands and preservation of non-CIS styles
- provisional road-sign coverage and the restricted sign-role allowlist
- Russian direction-board background colours and route-reference parsing
- no blanket straight delineator rows in post-Soviet test profiles
- suppression policy for heuristic roadside tree relocation
- Central Asian regional pole/guardrail profiles and the lamp-post mix

The full Python suite and BeamNG in-game import/visual/performance checks have
not been run in this editing session. These changes are committed to the test
branch only; they have not been merged into `main`.

## Standards and references

- Russia, GOST R 51256-2018, road marking dimensions and dash patterns:
  https://protect.gost.ru/gost/details/e84660db-4e3b-4c82-9627-c142a36355d2
- Russia, GOST R 52290-2024, road-sign designs and directional-board colours
  (effective 1 January 2026):
  https://protect.gost.ru/gost/details/39b75217-29bd-492b-94f4-c0dccb72b299
- Russia, GOST R 52289-2019, road-sign placement and mounting:
  https://base.garant.ru/73728515/
- Russia, GOST 33151-2014, road arrangement elements and delineator placement:
  https://base.garant.ru/71454660/
- Belarus, STB 1231-2012, road marking:
  https://files.stroyinf.ru/Index2/1/4293742/4293742046.htm
- Kazakhstan, ST RK 1412-2017, signs, markings, traffic lights, barriers and
  guide devices; current amendments noted by the standards source:
  https://new-shop.ksm.kz/catalog/document/68055/
- Kazakhstan, current PDD Appendix 2:
  https://law.gov.kz/api/documents/183572/rus/download/pdf
- Ukraine, Traffic Rules and road-marking section:
  https://zakon.rada.gov.ua/go/1306-2001-%D0%BF
- Uzbekistan, Traffic Rules, Appendix 2:
  https://lex.uz/uz/acts/5953887
- OpenStreetMap route-network conventions for Russian route references and
  national road relations:
  https://wiki.openstreetmap.org/wiki/RU:%D0%A2%D0%B5%D0%B3:network
  https://wiki.openstreetmap.org/wiki/RU:%D0%A2%D0%B5%D0%B3:type%3Droute

Standards and map schemas are used as references, not redistributed as copied
figures or third-party assets. Every national profile still needs a local
review before it can be presented as legally exact.
