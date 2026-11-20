# CIS road-marking profiles

Implementation notes for the CIS road-marking work in `server/markings.py`,
`server/secrossings.py` and `server/roads.py`.

## Scope

The renderer now uses country-aware profiles for:
- centre lines and lane dividers, including solid and double-solid cases;
- edge lines and motorway edge widths;
- speed-dependent dash/gap families where verified;
- stop lines and give-way markings at mapped junctions;
- mapped pedestrian crossings, with country-aware interpretation of OSM crossing tags;
- crossing length by road speed where the national document gives a threshold.

The renderer uses a shared crossing texture with country-specific repeat length for Russia and Kazakhstan. More complex
crossing variants (arrows, yellow-filled variants and traffic-signal variants), as well as arrows, hatched islands, bicycle crossings, parking/bus-stop markings and temporary work-zone markings remain follow-up work.

## Verified national references

### Kazakhstan

**СТ РК 1124-2019** and **СТ РК 1412-2017**.

- Narrow longitudinal lines: 0.10–0.15 m.
- Motorway edge marking 1.2: 0.20 m.
- Broken line 1.5: dash/gap ratio 1:3. For speeds up to 60 km/h, the standard gives dash/gap ranges of 1–3 / 3–9 m; above 60 km/h, 3–4 / 9–12 m.
- Stop line 1.12: 0.40 m.
- Give-way triangles 1.13: 0.50 m base, 0.90 m height and 0.30 m spacing.
- Zebra 1.14.1: 0.40 m bars and 0.60 m gaps; crossing width 2.5–4.0 m up to 60 km/h and 4.0–6.0 m above 60 km/h.

Implementation selects representative values inside the standard's allowed ranges. It does not pretend that the standard defines a single dash length for every road.

References:
- [СТ РК 1124-2019 (PDF copy)](https://vostoktranssignal.kz/upload/СТ%20РК%201124-2019.pdf)
- [СТ РК 1412-2017 (PDF copy)](https://www.vostoktranssignal.kz/upload/СТ%20РК%201412-2017.pdf)

### Ukraine

**ДСТУ 2587:2021**, effective 2021-08-01.

- Line width varies by road category: 0.10, 0.15 or 0.20 m.
- Broken line 1.5 uses a 1:2 dash/gap ratio, with speed bands: up to 50 km/h, 50–90 km/h and above 90 km/h.
- Double solid centre marking 1.3 is specified for roads with four or more lanes without a median, with additional use on some 2+1 sections.
- Intersection guide marking 1.7 uses 1 m / 1 m segments and gaps; 0.5 m / 0.5 m is allowed in constrained cases and at marking breaks.
- Stop line 1.12: 0.40 m.
- Give-way triangle: 0.70 m height, 0.50 m base and 0.25 m spacing.
- Pedestrian crossing width: at least 4.0 m on public roads and main streets; 2.5 m is allowed on certain local urban streets.

Implementation uses 0.10 m in urban streets, 0.15 m as the ordinary road width and 0.20 m on motorways. This is a renderer approximation of the standard's road-category choices, not a replacement for a full road-category classifier.

Reference:
- [ДСТУ 2587:2021 (PDF)](https://zakon.isu.net.ua/sites/default/files/normdocs/dstu_2587_2021.pdf)

### Moldova

**CP D.02.33:2024**, approved 2024-03-19 and effective 2024-03-22. Appendix R gives the application dimensions and refers to SM SR 1848-7.

- Narrow lines: 0.15 m.
- Wide motorway markings: 0.25 m.
- Double solid line: two 0.15 m lines with a 0.10 m gap.
- Ordinary broken line A: up to 60 km/h, representative 3/9 m; above 60 km/h, 4/12 m.
- Urban/restricted-speed broken line B: representative 3/1 m up to 60 km/h and 9/3 m above 60 km/h.
- Stop line: 0.40 m.
- Give-way line: 0.40 m wide, 0.80 m dashes and 0.40 m gaps; it may be preceded by a triangle.
- Pedestrian crossing length: at least 3.0 m below 50 km/h and 4.0 m above 50 km/h.

Implementation renders the give-way dashes as triangles in the mesh pipeline (two triangles per dash) so the existing marking renderer can consume them without a new mesh type.

Reference:
- [CP D.02.33:2024 — official Ministry portal PDF](https://ednc.gov.md/wp-content/uploads/2024/06/CP-D.02.33-2024-1.pdf)

### Russia

The Russian profile continues to use **ГОСТ Р 51256-2018** and the existing speed-sensitive road-marking logic. The standard specifies zebra bars 0.40 m wide, 0.60 m gaps and a 4.0–6.0 m crossing length. The renderer uses a 4.0 m minimum and the matching 4.0 m repeat pattern. It now also drives mapped stop lines and give-way markings in the CIS junction path.

The existing research note is:
- [Road-marking standards research, 2026-10-28](2026-10-28-road-markings-standards.md)

## Countries awaiting individual verification

Profiles exist for Armenia, Azerbaijan, Belarus, Georgia, Kyrgyzstan, Tajikistan, Turkmenistan and Uzbekistan, but their dimensions are deliberately left on the conservative white-line fallback until the current national standards are checked. Their profiles are separate objects so national values can be added independently.

A shared marking-number system or a reference to an intergovernmental GOST is not proof that every country's line widths, dash lengths, crossing geometry and application rules are identical.

## OSM interpretation

For CIS countries, an unqualified `highway=crossing` is not automatically rendered as a zebra based on the Swedish map majority. Zebra paint is accepted when the map explicitly says `crossing=zebra`, `crossing=marked`, `crossing=uncontrolled`, or supplies `crossing:markings=zebra/yes`. Unmarked and surface-only crossings remain unpainted. Sweden retains its own existing majority-based fallback; Germany retains its separate `de_paint` interpretation.

## Follow-up

1. Verify current national standards for AM, AZ, BY, GE, KG, TJ, TM and UZ.
2. Add country-specific zebra stripe/gap textures rather than sharing the current texture.
3. Add intersection guide lines, stop bars, give-way lines and box-junction markings as explicit mapped features where the source data supports them.
4. Add arrows, bicycle crossings, islands, bus stops, parking and temporary work-zone markings by national profile.
