# CIS passenger-car speed profiles

These profiles cover passenger cars without trailers. All values are km/h.

The order of precedence is:

1. A numeric OSM `maxspeed` value or a numeric `max_speed_kmh` rule.
2. A recognised symbolic OSM value such as `RU:rural` or `KZ:motorway`.
3. The country profile below, selected from the road's country and road type.
4. The existing BeamNG.Earth fallback for countries outside this list.

| Country | Built-up area | Ordinary roads outside settlements | Motorway | Special case |
|---|---:|---:|---:|---|
| Armenia (AM) | 60 | 90 | 110 | Residential/courtyard areas: 20 |
| Azerbaijan (AZ) | 60 | 90 | 110 | Residential/courtyard areas: 20; local signed urban exceptions can be higher |
| Belarus (BY) | 60 | 90 | 120 | The law also allows 120 on roads for automobiles; current Layercake data has no `motorroad` column, so that road type is not inferred separately |
| Georgia (GE) | 60 | 90 | 110 | Residential areas: 20 |
| Kyrgyzstan (KG) | 60 | 90 | 110 | Residential areas: 20 |
| Kazakhstan (KZ) | 60 | 100 | up to 140 | Divided carriageway: 110; motorway cap depends on the applicable sign; residential areas: 20 |
| Moldova (MD) | 50 | 90 | 110 | Residential areas: 20 |
| Russia (RU) | 60 | 90 | 110 | Residential/courtyard areas: 20 |
| Tajikistan (TJ) | 60 | 90 | 110 | Residential/courtyard areas: 20 |
| Turkmenistan (TM) | 60 | 90 | 90* | Published country guidance documents 60/90; no separate higher general motorway value was verified |
| Ukraine (UA) | 50 | 90 | 130 | Divided trunk roads: 110; residential areas: 20 |
| Uzbekistan (UZ) | 70 | 100 | 110 | Some cities/centres use 60 by local regime; residential areas: 20 |

`divided` is applied to one-way trunk, primary, or secondary features with at least two mapped lanes in Kazakhstan and Ukraine. It models the divided-carriageway exception; an explicit numeric OSM limit always overrides it.


The symbolic resolver recognises only suffixes explicitly present in the relevant country profile: `urban`, `rural`, `motorway`, `trunk`, and `living_street`. It also accepts the historical/transposed Russian spelling `RU:rual` as an alias for `RU:rural`.

**Source limitation:** the current [Layercake Highways schema](https://layercake.openstreetmap.us/layers/highways/) exposes `maxspeed` and `motor_vehicle`, but not `motorroad`. The implementation therefore assigns Belarus's 120 km/h default to `highway=motorway`; roads for automobiles can only get 120 when their numeric OSM `maxspeed` is present. Other Belarusian `trunk` roads default to 90.

## Sources and qualifications

- Armenia: [Decision 955-N speed rules](https://ert.am/en/traffic-rules/speed) — passenger-car limits 60 / 90 / 110.
- Azerbaijan: [Ministry of Internal Affairs, Road Traffic Law](https://mia.gov.az/ru/legislation/1/view/9/) — 60 in settlements, 90 on other roads, 110 on motorways.
- Belarus: [Traffic Rules, paragraph 89](https://legaris.by/legal-base/traffic-rules-of-the-republic-of-belarus/) — 120 on motorways and roads for motor vehicles, 90 on other roads; the cited text reflects amendments to Presidential Decree No. 145.
- Georgia: [Law on Road Traffic](https://pdd.ge/en/documents/road-traffic-law) — current consolidated text dated 25 June 2026; category B limits 60 / 90 / 110.
- Kazakhstan: [Official legal text of the 2023 Traffic Rules](https://law.gov.kz/api/documents/183572/rus/download/pdf) — 60 in settlements; outside, 100 on ordinary roads, 110 on divided roads and up to 140 on motorways when set by the applicable sign.
- Kyrgyzstan: [GUOBDD, Traffic Rules, section 10](https://guobdd.kg/trafficregulationsitem/10) — 60 in settlements, 90 on ordinary roads and 110 on motorways for passenger cars.
- Moldova: [General Police Inspectorate FAQ](https://igp.gov.md/en/frequently-asked-questions) — 50 in settlements, 90 outside; residential areas 20. The motorway value 110 follows the OSM country default-limit table.
- Russia: [OpenStreetMap's Russian maxspeed guidance](https://wiki.openstreetmap.org/wiki/RU:Key:maxspeed) — `RU:urban=60`, `RU:rural=90`, `RU:motorway=110`, `RU:living_street=20`.
- Tajikistan: [Ministry of Transport country statement to UNESCAP](https://www.unescap.org/sites/default/files/Country%20statement%20-%20Tajikistan%20-%20Speeding%20%26%20Road%20Safety.pdf) — 60 in populated areas, 90 on other roads and 110 on motorways for passenger cars up to 3.5 tonnes.
- Turkmenistan: [Russian MFA country information](https://www.kdmid.ru/docs/turkmenistan/information-about-the-country/) — 60 in towns and 90 on main roads. The 90 motorway value is conservative because a separate higher general allowance was not verified.
- Ukraine: [National Patrol Police speed-limit guidance](https://patrolpolice.gov.ua/avtomatychna-fiksatsiya/) — 50 in settlements, 90 on ordinary roads, 110 on divided roads and 130 on motorways.
- Uzbekistan: [LexUZ, Traffic Rules, paragraphs 78–79](https://lex.uz/en/docs/5953887?ONDATE=01.04.2026) — 70 in settlements (60 in named cities/centres by local regime), 100 on other roads and 110 on motorways for passenger cars up to 3.5 tonnes.

* Turkmenistan's motorway value is intentionally conservative and should be revisited if a current national legal text establishing a separate motorway limit is found. The profile does not override posted signs or vehicle-specific limits.
