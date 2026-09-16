## Outcome

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

Describe the user-visible problem and the focused result.

## Patch-Y visual change

Delete this section when the PR does not change Patch-Y source.

- Encounter / ability:
- Server profile:
- Exact server realm/build:
- Server-specific DBC IDs, timing, radius or mechanic evidence:
- Affected editions:
- Source operations (`add`, `replace`, `delete`, `dbc`):
- Asset source and applicable permission:
- Development `/pyversion`:
- Test client, locale and difficulty:
- Visual evidence:
- Not tested:

## Validation

- [ ] `python tools/patch_y.py verify-baseline`
- [ ] Every Patch-Y operation names one or more registered servers.
- [ ] `python tools/patch_y.py build --server <server> --label <branch-label>`
- [ ] `python tools/patch_y.py verify --server <server>`
- [ ] `python tools/patch_y.py diff --server <server>`
- [ ] Generated MPQs, extracted baselines, client files and personal data are not committed.
- [ ] Every DBC edit lists the table/member, record ID, named field/index, old/new value and reason.
- [ ] Static validation and in-game acceptance are reported separately.
