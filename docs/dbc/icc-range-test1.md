# ICC range circles — Test 1 DBC changes

<!-- Author: Neil Mitchell; Creator: Neil Mitchell; Last Modified By: Neil Mitchell -->

Baseline: exact Lau game 3.0.8, compared separately for all six editions. This experimental branch does not change the stable release or `/pyversion`.

All field numbers below are zero-based. Seven existing Spell records change only field 131 (first SpellVisual link); spell strings and every gameplay field are preserved. Four visual tables receive three new rows each. Every original row in those tables remains byte-identical. The full [JSON evidence](icc-range-test1.json) contains complete added-row values, decoded model paths, build input hashes and member hashes.

Three private model/skin/texture sets are added under `Spells\Lau_ICC_RangeTest`. Exactly five DBC members change per archive; all unrelated members pass exact StormLib readback comparison. Runtime player attachment, timing and intended 12-yard radius remain unverified.

## Y-HD-NewSpells-Off-Consecration-Off

- Baseline archive SHA-256: `0a7f2eef34085785b72f1d18b83108c25dac2c2deada412738182fee5e738a80`
- Test archive SHA-256: `416d062addf4209158d636993df2bbda60c9a61a154c6e649f89e56678170c5c`
- Test archive bytes: 67913649

| Spell ID | Field | Before | After |
| --- | --- | --- | --- |
| 72038 | 131 | 15204 | 20022 |
| 72378 | 131 | 15283 | 20023 |
| 72815 | 131 | 15204 | 20022 |
| 72816 | 131 | 15204 | 20022 |
| 72817 | 131 | 15204 | 20022 |
| 73001 | 131 | 15404 | 20021 |
| 73058 | 131 | 15283 | 20023 |

| Cue | Visual donor → new | Kit donor → new | Effect donor → new | Attachment donor → new |
| --- | --- | --- | --- | --- |
| shadow prison | 15404 → 20021 | 90002 → 90060 | 9002 → 9176 | 8003 → 8075 |
| empowered vortex | 15204 → 20022 | 14056 → 90061 | 9002 → 9177 | 8003 → 8076 |
| blood nova | 15283 → 20023 | 14140 → 90062 | 9002 → 9178 | 8003 → 8077 |

| Table | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| Spell | `a4461f995967a45f3f8a73ecf576d9534685a3a775b0342828fa5c19fb369a21` | `635b2ca811d1b411bf8b919c3f6b6f914c8644d56379f1e37f0995f747e9ebaa` |
| SpellVisual | `b347de3e848d5abcae32b1f98a0caf6b9e733294b514ce2aff2f3f65e75aaee8` | `8d8981f617b31a90681bd7638ec2c8770ce9f83e4f3c686cce60f8443b52648e` |
| SpellVisualKit | `3d29c55eaadae9cf4c0e42db1fed865e97eaaddbfc2e138a243fcd5d2e6b6b71` | `ee2b091e208ac90e3039ebf7cd3bcbb203514f1b8530e9f494b7b122b9f69632` |
| SpellVisualEffectName | `e721c563cd0c6283f8b9091cba7c7bcd1a35b70527d537a1bba30271ec1a3f0f` | `88de4ff664313fe7f172f1aa9afdb8258ec13b113f20bbf260a9092ba59a39fa` |
| SpellVisualKitModelAttach | `b3c222987215cdeb5987c24fbf81c2664e9920c8c9d3ee1e00fcf915afa5f652` | `604c7c001283c8c8119253018d3284f4acd9afd9f4df22914b3c2dd076610fbf` |

## Y-HD-NewSpells-Off-Consecration-On

- Baseline archive SHA-256: `2941cbbf61bebcabd2e0ff51361268447e7b6739fafef7da175b2a31662991a3`
- Test archive SHA-256: `c9a83086115c4dcc34eb7407651145f48d33b4686aa646e871bdb44e2d7b4227`
- Test archive bytes: 67913677

| Spell ID | Field | Before | After |
| --- | --- | --- | --- |
| 72038 | 131 | 15204 | 20022 |
| 72378 | 131 | 15283 | 20023 |
| 72815 | 131 | 15204 | 20022 |
| 72816 | 131 | 15204 | 20022 |
| 72817 | 131 | 15204 | 20022 |
| 73001 | 131 | 15404 | 20021 |
| 73058 | 131 | 15283 | 20023 |

| Cue | Visual donor → new | Kit donor → new | Effect donor → new | Attachment donor → new |
| --- | --- | --- | --- | --- |
| shadow prison | 15404 → 20021 | 90002 → 90060 | 9002 → 9176 | 8003 → 8075 |
| empowered vortex | 15204 → 20022 | 14056 → 90061 | 9002 → 9177 | 8003 → 8076 |
| blood nova | 15283 → 20023 | 14140 → 90062 | 9002 → 9178 | 8003 → 8077 |

| Table | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| Spell | `a4461f995967a45f3f8a73ecf576d9534685a3a775b0342828fa5c19fb369a21` | `635b2ca811d1b411bf8b919c3f6b6f914c8644d56379f1e37f0995f747e9ebaa` |
| SpellVisual | `b347de3e848d5abcae32b1f98a0caf6b9e733294b514ce2aff2f3f65e75aaee8` | `8d8981f617b31a90681bd7638ec2c8770ce9f83e4f3c686cce60f8443b52648e` |
| SpellVisualKit | `3d29c55eaadae9cf4c0e42db1fed865e97eaaddbfc2e138a243fcd5d2e6b6b71` | `ee2b091e208ac90e3039ebf7cd3bcbb203514f1b8530e9f494b7b122b9f69632` |
| SpellVisualEffectName | `3e48ac693588cce058754a562f5681c3b72a1ff5062ff0c63cadff1d1e75d23c` | `19288c912dbd67177c97627b4c243cb37ebf771ed4a77c5879f5c8e60e286ded` |
| SpellVisualKitModelAttach | `b3c222987215cdeb5987c24fbf81c2664e9920c8c9d3ee1e00fcf915afa5f652` | `604c7c001283c8c8119253018d3284f4acd9afd9f4df22914b3c2dd076610fbf` |

## Y-HD-NewSpells-On-Consecration-Off

- Baseline archive SHA-256: `270afe55b5d517ea4f0b976437b00c663da5bee52d9fb7f9969a5042e8d3fd8e`
- Test archive SHA-256: `9cf59d9c584e5b7b9c4bda47b0e6dd93734a568d2ef47cc709c317283108e596`
- Test archive bytes: 83898456

| Spell ID | Field | Before | After |
| --- | --- | --- | --- |
| 72038 | 131 | 15204 | 20022 |
| 72378 | 131 | 15283 | 20023 |
| 72815 | 131 | 15204 | 20022 |
| 72816 | 131 | 15204 | 20022 |
| 72817 | 131 | 15204 | 20022 |
| 73001 | 131 | 15404 | 20021 |
| 73058 | 131 | 15283 | 20023 |

| Cue | Visual donor → new | Kit donor → new | Effect donor → new | Attachment donor → new |
| --- | --- | --- | --- | --- |
| shadow prison | 15404 → 20021 | 90002 → 90059 | 9002 → 9176 | 8003 → 8075 |
| empowered vortex | 15204 → 20022 | 14056 → 90060 | 9002 → 9177 | 8003 → 8076 |
| blood nova | 15283 → 20023 | 14140 → 90061 | 9002 → 9178 | 8003 → 8077 |

| Table | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| Spell | `9580b7fede77586c26da1083557808061805b782beadee06b651c8f3c72f6a11` | `604f222a31a1615a3239cc7c4deaa88be077566bb865d750a26c3c2562ad6e71` |
| SpellVisual | `4914fac2eec4ff43f66821efacbb81719c872cf58bffdfa99a7d7a3abd7096d4` | `7c0e126fac1bd6274f5d812b86bc00c53deb0bb17cf5c0959ec05b995dd21791` |
| SpellVisualKit | `6e2c83cbeb73e139d3c8a7284140c25466d84947a2c2dfb1255612ce01210c91` | `246adee00464017b1ba17a7ebeac63471685defaf745fd9c94677785f8e442ff` |
| SpellVisualEffectName | `8964ecb47f85bd873abfe54c971d58722c3467de3f6084b945c2bf8e2250e4fa` | `aa9509caf20a867f0a25a24ed443d748e1e44823ca6c75cc6e82cc758bc14239` |
| SpellVisualKitModelAttach | `daf235cd73624762af76ce1ece369420a2dafbd49027c67e6771d93fdbcf6a35` | `ed0b8c399dcd51d97aaf9b8346e98a1b5cb5ba8c534262fd95e23c3568b5ad67` |

## Y-HD-NewSpells-On-Consecration-On

- Baseline archive SHA-256: `508020eb056d73597d0d64fed17662018cbbe7236a401623b2088b051664d9f2`
- Test archive SHA-256: `5d634f73cc8981d20a68e571b8622ae24c6167df365a2e297928afeed9b562a4`
- Test archive bytes: 83898470

| Spell ID | Field | Before | After |
| --- | --- | --- | --- |
| 72038 | 131 | 15204 | 20022 |
| 72378 | 131 | 15283 | 20023 |
| 72815 | 131 | 15204 | 20022 |
| 72816 | 131 | 15204 | 20022 |
| 72817 | 131 | 15204 | 20022 |
| 73001 | 131 | 15404 | 20021 |
| 73058 | 131 | 15283 | 20023 |

| Cue | Visual donor → new | Kit donor → new | Effect donor → new | Attachment donor → new |
| --- | --- | --- | --- | --- |
| shadow prison | 15404 → 20021 | 90002 → 90059 | 9002 → 9176 | 8003 → 8075 |
| empowered vortex | 15204 → 20022 | 14056 → 90060 | 9002 → 9177 | 8003 → 8076 |
| blood nova | 15283 → 20023 | 14140 → 90061 | 9002 → 9178 | 8003 → 8077 |

| Table | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| Spell | `9580b7fede77586c26da1083557808061805b782beadee06b651c8f3c72f6a11` | `604f222a31a1615a3239cc7c4deaa88be077566bb865d750a26c3c2562ad6e71` |
| SpellVisual | `4914fac2eec4ff43f66821efacbb81719c872cf58bffdfa99a7d7a3abd7096d4` | `7c0e126fac1bd6274f5d812b86bc00c53deb0bb17cf5c0959ec05b995dd21791` |
| SpellVisualKit | `6e2c83cbeb73e139d3c8a7284140c25466d84947a2c2dfb1255612ce01210c91` | `246adee00464017b1ba17a7ebeac63471685defaf745fd9c94677785f8e442ff` |
| SpellVisualEffectName | `d130ea47602eb6d17e2d676dad0e0dece477fdb6ffc7c79e184ec038769d094b` | `f71708496a7bc78c0f7b8b0efbf5eafe5009dd2487eb72a9aa7ee2e5d2d64636` |
| SpellVisualKitModelAttach | `daf235cd73624762af76ce1ece369420a2dafbd49027c67e6771d93fdbcf6a35` | `ed0b8c399dcd51d97aaf9b8346e98a1b5cb5ba8c534262fd95e23c3568b5ad67` |

## Y-Non-HD-Consecration-Off

- Baseline archive SHA-256: `e841709e455f70dd3255a691b337b28ecf1761fef8e758570db4038ba7a2d062`
- Test archive SHA-256: `027cb8a105200a6ceaa97a16bbb44180311d7930f3b6d91511ff785eebd0c98f`
- Test archive bytes: 71082577

| Spell ID | Field | Before | After |
| --- | --- | --- | --- |
| 72038 | 131 | 15204 | 20022 |
| 72378 | 131 | 15283 | 20023 |
| 72815 | 131 | 15204 | 20022 |
| 72816 | 131 | 15204 | 20022 |
| 72817 | 131 | 15204 | 20022 |
| 73001 | 131 | 15404 | 20021 |
| 73058 | 131 | 15283 | 20023 |

| Cue | Visual donor → new | Kit donor → new | Effect donor → new | Attachment donor → new |
| --- | --- | --- | --- | --- |
| shadow prison | 15404 → 20021 | 90002 → 90059 | 9002 → 9176 | 8003 → 8075 |
| empowered vortex | 15204 → 20022 | 14056 → 90060 | 9002 → 9177 | 8003 → 8076 |
| blood nova | 15283 → 20023 | 14140 → 90061 | 9002 → 9178 | 8003 → 8077 |

| Table | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| Spell | `a4461f995967a45f3f8a73ecf576d9534685a3a775b0342828fa5c19fb369a21` | `635b2ca811d1b411bf8b919c3f6b6f914c8644d56379f1e37f0995f747e9ebaa` |
| SpellVisual | `371fb949d76a38445ee6fe34d113c5c6e248c4d780a4f8e1d8cb3c79bbf814d8` | `69b87a1f29e776ee5c4a8d4ad39ef0925290aa283e68446564c5cc90d5aecf89` |
| SpellVisualKit | `eda6ef622b65c21827ab3f77364f68291841d436f55dd01d815c6543e2932a37` | `c44f66c8def2f8b869275bdbc94c7cbe1a7090775dcaf2afcb61a2c0cf128b6e` |
| SpellVisualEffectName | `611608dd4c605970bf5b9ecfc4ea99037d56620607fd32449234c5036b953b30` | `7b19a388fdec8c9799535c3347dc2319addc7ae543b4e18d831c421ea0d4841f` |
| SpellVisualKitModelAttach | `c6c76bd30b3b5622fea6ba994121e6f38652b2e1ca1370011bc9624daf740f0d` | `bc15857a88e73de8b81c1e4588874c0e306a6efcd93596b827cfc70c15d5e5a7` |

## Y-Non-HD-Consecration-On

- Baseline archive SHA-256: `177445dee261bf6bea06fd8ca8cf1398b64c231ee26878329ff8faebfb1bce17`
- Test archive SHA-256: `87691884691ba54e070b3f2351dfae7b0efc9e6d65ddd9907c5b081801962aeb`
- Test archive bytes: 71082577

| Spell ID | Field | Before | After |
| --- | --- | --- | --- |
| 72038 | 131 | 15204 | 20022 |
| 72378 | 131 | 15283 | 20023 |
| 72815 | 131 | 15204 | 20022 |
| 72816 | 131 | 15204 | 20022 |
| 72817 | 131 | 15204 | 20022 |
| 73001 | 131 | 15404 | 20021 |
| 73058 | 131 | 15283 | 20023 |

| Cue | Visual donor → new | Kit donor → new | Effect donor → new | Attachment donor → new |
| --- | --- | --- | --- | --- |
| shadow prison | 15404 → 20021 | 90002 → 90059 | 9002 → 9176 | 8003 → 8075 |
| empowered vortex | 15204 → 20022 | 14056 → 90060 | 9002 → 9177 | 8003 → 8076 |
| blood nova | 15283 → 20023 | 14140 → 90061 | 9002 → 9178 | 8003 → 8077 |

| Table | Before SHA-256 | After SHA-256 |
| --- | --- | --- |
| Spell | `a4461f995967a45f3f8a73ecf576d9534685a3a775b0342828fa5c19fb369a21` | `635b2ca811d1b411bf8b919c3f6b6f914c8644d56379f1e37f0995f747e9ebaa` |
| SpellVisual | `371fb949d76a38445ee6fe34d113c5c6e248c4d780a4f8e1d8cb3c79bbf814d8` | `69b87a1f29e776ee5c4a8d4ad39ef0925290aa283e68446564c5cc90d5aecf89` |
| SpellVisualKit | `eda6ef622b65c21827ab3f77364f68291841d436f55dd01d815c6543e2932a37` | `c44f66c8def2f8b869275bdbc94c7cbe1a7090775dcaf2afcb61a2c0cf128b6e` |
| SpellVisualEffectName | `738892c59e16e99afee3656d6a72f80da9753a5e43dca497fe9b31218a6fd7c5` | `ed481c4a39c97d4033ebaa8d3afb37b7e0b07281e54bab6bd3edd23e4b95f338` |
| SpellVisualKitModelAttach | `c6c76bd30b3b5622fea6ba994121e6f38652b2e1ca1370011bc9624daf740f0d` | `bc15857a88e73de8b81c1e4588874c0e306a6efcd93596b827cfc70c15d5e5a7` |
