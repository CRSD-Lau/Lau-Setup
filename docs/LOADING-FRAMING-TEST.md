# Loading-screen framing investigation (superseded)

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

The initial native-framing test for [issue #34](https://github.com/CRSD-Lau/Lau-Setup/issues/34) restored full artwork but exposed the client's 16:10 Wide frame, leaving side bars on a 16:9 display. An ICC-only experiment was subsequently staged but was never installed or released. It is not the production solution.

Lau Setup 1.5.0 / Game 3.1.0 instead uses the native renderer with a 16:9 Wide aspect and the accepted 77-image pack. Eight backgrounds retain their original art. The released executable SHA-256 is `4218fef354f875d1d27aae9cc6a93c75aaadaa1f0beea1204172793cd39e0505`.

Neil approved the pack after representative in-game testing at 16:9. Every scene, locale and other display ratio was not individually accepted. Use the [current loading-pack documentation](LOADING-HD16X9-PACK.md), [archive/DBC proof](dbc/loading-3.1.0.json) and [release validation](VALIDATION-1.5.0.json); do not package an earlier experimental executable or Q archive.
