# Individual Patch-Y DBC edits: Andre baseline to retained multilingual Lau build

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

## Read the chronology first

Andre intentionally omitted **Spell.dbc** because of localization conflicts, according to Lau. The retained Andre 3.0.3 archives do contain six visual/model DBCs; they do not contain Spell.dbc. The initial Lau addition introduced the language dependency. Lau and Andre debugged the problem together, and the multilingual rebuild resolved it.

Lau identifies these development milestones as 3.0.4 (initial addition) and 3.0.5 (multilingual fix), with 3.0.6–3.0.8 being hotfixes whose version numbers were bumped. Retained artifacts do not map cleanly to that recollection: the published baseline labelled 3.0.4 already contains the multilingual fix. This report names artifacts and hashes explicitly rather than silently assigning an early broken build to that published label.

[Localization-stage proof](localization-stage.json) compares four retained pre-localization v35 archives against the multilingual versions: only Spell.dbc changes, all numeric fields remain identical, and existing visual links are preserved. HD New Spells Off was assembled separately using stock numeric data.

## Format and scope

This is the Patch-Y handoff comparison, not an audit of every separate Q/S/map localization pipeline. Six edition CSVs list individual table/record/field edits and all added record values. Two shared JSON gzip files hold decoded spell text changes without duplicating text for Consecration variants. Each text cell is `[record_id, zero_based_field, old_string_index, new_string_index]`; resolve the last two through that file’s `strings` array.

Numeric values are raw unsigned 32-bit words, including float bit patterns; unknown schema names are not guessed. Spell.dbc field 131 is the visual link used by the build scripts. String offsets are decoded before comparison. The added Spell.dbc uses retained HD Patch-S data for HD New Spells On, and stock server-extracted data for HD New Spells Off and Non-HD. Inherited rows are not credited as newly authored records.

### What the edit groups mean

- Spell field 131: fifteen accepted raid-indicator visual links in every edition.
- Spell text cells: multilingual/fallback slot population; these counts are not counts of newly authored translations.
- SpellVisual, SpellVisualKit and attachment rows: indicator routing, kits and model attachment setup.
- SpellVisualEffectName: added model references and Consecration appearance differences.
- CreatureDisplayInfo and CreatureModelData: unchanged from the corresponding Andre baseline.
- HD New Spells Off: private Rimefang kit uses 90059 to preserve the upstream 90046 kit.

## Y-HD-NewSpells-Off-Consecration-On

| Table | Changed/added records | Field-value differences | Added IDs | Removed IDs |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | None | None |
| creaturemodeldata.dbc | 0 | 0 | None | None |
| spell.dbc | 49839 | 824619 | None | None |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | None |
| spellvisualeffectname.dbc | 12 | 79 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | None |
| spellvisualkit.dbc | 14 | 495 | 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058, 90059 | None |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | None |

| Table | Record ID | Field [0-based] | Old | New |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualeffectname.dbc | 2542 | 2 | spells\consecration_impact_base.mdx | spells\Flamezone.mdx |
| spellvisualeffectname.dbc | 2542 | 4 | 1065353216 | 1075838976 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[All record/field edits and added records](Y-HD-NewSpells-Off-Consecration-On.csv) · [Decoded text changes](spell-text-nonhd.json.gz)

## Y-HD-NewSpells-Off-Consecration-Off

| Table | Changed/added records | Field-value differences | Added IDs | Removed IDs |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | None | None |
| creaturemodeldata.dbc | 0 | 0 | None | None |
| spell.dbc | 49839 | 824619 | None | None |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | None |
| spellvisualeffectname.dbc | 11 | 77 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | None |
| spellvisualkit.dbc | 14 | 495 | 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058, 90059 | None |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | None |

| Table | Record ID | Field [0-based] | Old | New |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[All record/field edits and added records](Y-HD-NewSpells-Off-Consecration-Off.csv) · [Decoded text changes](spell-text-nonhd.json.gz)

## Y-HD-NewSpells-On-Consecration-On

| Table | Changed/added records | Field-value differences | Added IDs | Removed IDs |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | None | None |
| creaturemodeldata.dbc | 0 | 0 | None | None |
| spell.dbc | 33950 | 227113 | None | None |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | None |
| spellvisualeffectname.dbc | 12 | 79 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | None |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | None |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | None |

| Table | Record ID | Field [0-based] | Old | New |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualeffectname.dbc | 2542 | 2 | spells\consecration_impact_base.mdx | spells\Flamezone.mdx |
| spellvisualeffectname.dbc | 2542 | 4 | 1065353216 | 1075838976 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[All record/field edits and added records](Y-HD-NewSpells-On-Consecration-On.csv) · [Decoded text changes](spell-text-hd.json.gz)

## Y-HD-NewSpells-On-Consecration-Off

| Table | Changed/added records | Field-value differences | Added IDs | Removed IDs |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | None | None |
| creaturemodeldata.dbc | 0 | 0 | None | None |
| spell.dbc | 33950 | 227113 | None | None |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | None |
| spellvisualeffectname.dbc | 11 | 77 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | None |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | None |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | None |

| Table | Record ID | Field [0-based] | Old | New |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[All record/field edits and added records](Y-HD-NewSpells-On-Consecration-Off.csv) · [Decoded text changes](spell-text-hd.json.gz)

## Y-Non-HD-Consecration-On

| Table | Changed/added records | Field-value differences | Added IDs | Removed IDs |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | None | None |
| creaturemodeldata.dbc | 0 | 0 | None | None |
| spell.dbc | 49839 | 824619 | None | None |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | None |
| spellvisualeffectname.dbc | 12 | 79 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | None |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | None |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | None |

| Table | Record ID | Field [0-based] | Old | New |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualeffectname.dbc | 2542 | 2 | spells\consecration_impact_base.mdx | spells\Flamezone.mdx |
| spellvisualeffectname.dbc | 2542 | 4 | 1065353216 | 1075838976 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[All record/field edits and added records](Y-Non-HD-Consecration-On.csv) · [Decoded text changes](spell-text-nonhd.json.gz)

## Y-Non-HD-Consecration-Off

| Table | Changed/added records | Field-value differences | Added IDs | Removed IDs |
| --- | ---: | ---: | --- | --- |
| creaturedisplayinfo.dbc | 0 | 0 | None | None |
| creaturemodeldata.dbc | 0 | 0 | None | None |
| spell.dbc | 49839 | 824619 | None | None |
| spellvisual.dbc | 9 | 165 | 20016, 20017, 20018, 20019, 20020 | None |
| spellvisualeffectname.dbc | 11 | 77 | 9165, 9166, 9167, 9168, 9169, 9170, 9171, 9172, 9173, 9174, 9175 | None |
| spellvisualkit.dbc | 14 | 495 | 90046, 90047, 90048, 90049, 90050, 90051, 90052, 90053, 90054, 90055, 90056, 90057, 90058 | None |
| spellvisualkitmodelattach.dbc | 2 | 20 | 8073, 8074 | None |

| Table | Record ID | Field [0-based] | Old | New |
| --- | ---: | ---: | --- | --- |
| spell.dbc | 56908 | 131 | 12413 | 20017 |
| spell.dbc | 58956 | 131 | 12413 | 20017 |
| spell.dbc | 71386 | 131 | 14711 | 20016 |
| spell.dbc | 74403 | 131 | 12413 | 20018 |
| spell.dbc | 74404 | 131 | 12413 | 20018 |
| spell.dbc | 74712 | 131 | 13670 | 20019 |
| spell.dbc | 74713 | 131 | 15689 | 20020 |
| spell.dbc | 74717 | 131 | 13670 | 20019 |
| spell.dbc | 74718 | 131 | 13670 | 20019 |
| spell.dbc | 75947 | 131 | 13670 | 20019 |
| spell.dbc | 75948 | 131 | 13670 | 20019 |
| spell.dbc | 75949 | 131 | 13670 | 20019 |
| spell.dbc | 75950 | 131 | 13670 | 20019 |
| spell.dbc | 75951 | 131 | 13670 | 20019 |
| spell.dbc | 75952 | 131 | 13670 | 20019 |
| spellvisual.dbc | 12413 | 1 | 4451 | 90051 |
| spellvisual.dbc | 14711 | 1 | 12852 | 90056 |
| spellvisual.dbc | 15013 | 1 | 0 | 90057 |
| spellvisual.dbc | 15013 | 6 | 13868 | 90058 |
| spellvisual.dbc | 15711 | 1 | 14512 | 90052 |
| spellvisualkit.dbc | 13448 | 14 | 6388 | 9172 |

[All record/field edits and added records](Y-Non-HD-Consecration-Off.csv) · [Decoded text changes](spell-text-nonhd.json.gz)

