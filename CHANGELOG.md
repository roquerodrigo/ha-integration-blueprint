# Changelog

## [0.1.8](https://github.com/roquerodrigo/ha-integration-blueprint/compare/v0.1.7...v0.1.8) (2026-08-07)


### Documentation

* define the canonical README header layout ([f322831](https://github.com/roquerodrigo/ha-integration-blueprint/commit/f322831d92b499e6ea0159327c8b51600606dc49))
* normalize README header layout ([d117447](https://github.com/roquerodrigo/ha-integration-blueprint/commit/d117447f8b7d9afeb2c9fdcaf78756249ee6b42f))

## [0.1.7](https://github.com/roquerodrigo/ha-integration-blueprint/compare/v0.1.6...v0.1.7) (2026-08-07)


### Features

* absorb short API outages before marking entities unavailable ([30b6ec2](https://github.com/roquerodrigo/ha-integration-blueprint/commit/30b6ec2b275cf02f213819d7edf9aa684983d14f))
* add a scaffold for the companion SDK repository ([14c17f7](https://github.com/roquerodrigo/ha-integration-blueprint/commit/14c17f7016263ee41cb7ee006715f74ad0fbb35b))
* allow removing devices the config entry no longer provides ([aa0fcf5](https://github.com/roquerodrigo/ha-integration-blueprint/commit/aa0fcf50f99e44fb6a555478378f10bca00f351d))
* move the sample sensor icon to icons.json and declare integration_type ([1760b4e](https://github.com/roquerodrigo/ha-integration-blueprint/commit/1760b4e605fb0b8db1456c0ddc10d95877ca2c59))


### Bug Fixes

* **coordinator:** pass config_entry explicitly to DataUpdateCoordinator ([4891900](https://github.com/roquerodrigo/ha-integration-blueprint/commit/4891900e18f331376d7898445d4eca05d6a489d8))
* guard reauth and reconfigure against switching accounts ([418e8af](https://github.com/roquerodrigo/ha-integration-blueprint/commit/418e8af8461f8a69b832dcc0deb0a017a2fc9037))
* redact URL query strings from API error messages ([5a3ea84](https://github.com/roquerodrigo/ha-integration-blueprint/commit/5a3ea842abc37d94ac6f039d48367f4a877accbe))


### Development Dependencies

* **deps-dev:** bump ruff ([b3085da](https://github.com/roquerodrigo/ha-integration-blueprint/commit/b3085da0e8a70cd5b8e8e1e455a0e21c0605165b))


### Documentation

* align README, CONTRIBUTING and style guides with the actual repo ([23dad32](https://github.com/roquerodrigo/ha-integration-blueprint/commit/23dad326b327948f868204dbead1ff6b3a28a046))
* update CLAUDE.md ([33790df](https://github.com/roquerodrigo/ha-integration-blueprint/commit/33790dfab84bbe60eaaef8ec03daa7b2948c59d8))


### Build System

* **deps-dev:** bump mypy from 2.2.0 to 2.3.0 in the python-deps group ([66ef39d](https://github.com/roquerodrigo/ha-integration-blueprint/commit/66ef39df04ae55933817e5087d191e13bd9e4f73))
* **deps-dev:** bump mypy from 2.2.0 to 2.3.0 in the python-deps group ([0ede3e3](https://github.com/roquerodrigo/ha-integration-blueprint/commit/0ede3e328eadb3e9ed83d0141d8649c19a02d789))
* **deps-dev:** bump pre-commit ([0cf0a82](https://github.com/roquerodrigo/ha-integration-blueprint/commit/0cf0a822ab0fd0f04dc2e8d88e3fe59c698a5a93))
* **deps-dev:** bump ruff in the python-deps group ([ba47345](https://github.com/roquerodrigo/ha-integration-blueprint/commit/ba473455bae3f38b618d5fa0764c3a9dbdd7a581))


### Continuous Integration

* assign open issues and pull requests to the repository owner ([896bc90](https://github.com/roquerodrigo/ha-integration-blueprint/commit/896bc90570db60ea84a7c572abd9e6f007d56391))
* call the shared auto-assign workflow instead of duplicating it ([7f394cf](https://github.com/roquerodrigo/ha-integration-blueprint/commit/7f394cf773e3ff45cb85d9a79d5da0190a804a22))
* drop the auto-assign job now handled by its own workflow ([e7e6e49](https://github.com/roquerodrigo/ha-integration-blueprint/commit/e7e6e49c7afe98efec5b4a7e21fd3fc7393bd2b8))
* drop the blank line left by the removed job ([cd6a50c](https://github.com/roquerodrigo/ha-integration-blueprint/commit/cd6a50cd935aa1992c884d73ccfc663b36da600b))
* run checks on pull requests targeting any branch ([5959338](https://github.com/roquerodrigo/ha-integration-blueprint/commit/5959338d35b5d4d321166c03c64a3cd99e1615b5))
* run code scanning on pull requests targeting any branch ([bfb5d0f](https://github.com/roquerodrigo/ha-integration-blueprint/commit/bfb5d0f0d15c5faa17e30bec5e024fa7e0388451))
* run template checks on pull requests targeting any branch ([592f1f4](https://github.com/roquerodrigo/ha-integration-blueprint/commit/592f1f4481b266db651bf7ebcf5e3f3983eb4f6f))
* split the CI workflow into one file per concern ([2061c3d](https://github.com/roquerodrigo/ha-integration-blueprint/commit/2061c3d4b53b0fe69a6de70dc1023b6f22866c4a))


### Tests

* verify entity translation keys through the entity registry ([33ba56d](https://github.com/roquerodrigo/ha-integration-blueprint/commit/33ba56d30bb57c18f3ec910eae0881423afc6de6))


### Miscellaneous Chores

* **deps-dev:** bump ruff to 0.16.0 ([173e60a](https://github.com/roquerodrigo/ha-integration-blueprint/commit/173e60abc81634a55f3ae29ef6c311a48a6aa249))
* drop the Dependabot devcontainers ecosystem ([994ac52](https://github.com/roquerodrigo/ha-integration-blueprint/commit/994ac525baafca8b200ddd9874532d1ddb3e8113))
* move CI to the shared workflows repository ([7b86f46](https://github.com/roquerodrigo/ha-integration-blueprint/commit/7b86f46d2e953071b2c6e8da441c6334757c352e))
* release on every conventional commit type ([8b08b91](https://github.com/roquerodrigo/ha-integration-blueprint/commit/8b08b91c7e7bfa9b23580706888c41122a0db66b))
* run pre-commit ruff and mypy as local uv hooks ([accf137](https://github.com/roquerodrigo/ha-integration-blueprint/commit/accf137d9c70ae1fcc241e680fba1ea12fa82f2f))

## [0.1.6](https://github.com/roquerodrigo/ha-integration-blueprint/compare/v0.1.5...v0.1.6) (2026-07-11)


### Dependencies

* update dev and lint dependencies ([ba82136](https://github.com/roquerodrigo/ha-integration-blueprint/commit/ba821363f58de8e8156d6c045b490eddd2f3c6bb))


### Documentation

* align guides with data package and brand placeholder policy ([02052ed](https://github.com/roquerodrigo/ha-integration-blueprint/commit/02052edf40e9eee6d6916c2866884c739c8b2bdf))

## [0.1.5](https://github.com/roquerodrigo/ha-integration-blueprint/compare/v0.1.4...v0.1.5) (2026-06-21)


### Documentation

* drop stale scripts/lint and config-file references from CLAUDE.md ([339fd70](https://github.com/roquerodrigo/ha-integration-blueprint/commit/339fd707fe87e0f0c5dd3dff5bc4746fde645977))
* fix stale brand-assets location in CODE_STYLE.md ([a0e1dde](https://github.com/roquerodrigo/ha-integration-blueprint/commit/a0e1dde688ae35b92a4718410f2c650d1c2c2553))

## [0.1.4](https://github.com/roquerodrigo/ha-integration-blueprint/compare/v0.1.3...v0.1.4) (2026-05-25)


### Documentation

* fix CI badge and drop license badge ([fd89f13](https://github.com/roquerodrigo/ha-integration-blueprint/commit/fd89f13f8205f9786a8a0fa10b7c54be71717929))
* fix CI badge and drop license badge ([0ba71ff](https://github.com/roquerodrigo/ha-integration-blueprint/commit/0ba71fff8e9da4b48d907a16d8ef580004ce6e75))

## [0.1.3](https://github.com/roquerodrigo/ha-integration-blueprint/compare/v0.1.2...v0.1.3) (2026-05-19)


### Features

* **sensor:** make entity name translatable via translation_key ([174c345](https://github.com/roquerodrigo/ha-integration-blueprint/commit/174c3455f4127420f56ad97ccec510a69a8c0c4e))


### Performance Improvements

* **coordinator:** skip redundant state writes via always_update=False ([dab9085](https://github.com/roquerodrigo/ha-integration-blueprint/commit/dab9085dd3f2aecb36269e2dc53b00ce4151fb8a))


### Documentation

* document quality scale tiers, coordinator details, and HACS requirements ([cd5b9fa](https://github.com/roquerodrigo/ha-integration-blueprint/commit/cd5b9fab5ef5742e5615d58f8dbb6a4158de428d))
* **quality-scale:** add quality_scale.yaml tracking platinum progress ([8cfeac4](https://github.com/roquerodrigo/ha-integration-blueprint/commit/8cfeac4a366a981176feb168c64a6c93510fbb00))

## [0.1.2](https://github.com/roquerodrigo/ha-integration-blueprint/compare/v0.1.1...v0.1.2) (2026-05-11)


### Dependencies

* bump Home Assistant to 2026.5.1 ([2ee9412](https://github.com/roquerodrigo/ha-integration-blueprint/commit/2ee9412994763b3e29611de78f1a0108ba02d258))

## [0.1.1](https://github.com/roquerodrigo/ha-integration-blueprint/compare/v0.1.0...v0.1.1) (2026-05-09)


### Dependencies

* bump mypy and pytest-homeassistant-custom-component ([9b4e67d](https://github.com/roquerodrigo/ha-integration-blueprint/commit/9b4e67d13ad21ee7ee2010e89d1444af0a30261c))


### Documentation

* standardize CODE_STYLE.md template ([9877550](https://github.com/roquerodrigo/ha-integration-blueprint/commit/9877550c96ac032a5d170fcaa01d593742b35dad))
* standardize CODE_STYLE.md template ([1b69040](https://github.com/roquerodrigo/ha-integration-blueprint/commit/1b69040a6954fb942dc6b74657994df4e0a075da))
