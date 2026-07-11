# Brand assets

The icon and logo files here are **obvious `TODO` placeholders**, not final
artwork — a slate box stamped `TODO / replace me`. They exist so the HACS
`brands` check passes, while making it impossible for the agent (or human)
forking this blueprint to mistake them for the real brand and skip the
replacement step.

When you fork this blueprint into a real integration, replace every file here
with your own artwork — use the real brand of the device or service you
integrate, never generated placeholder art:

| File          | Shape                   | Size         |
| ------------- | ----------------------- | ------------ |
| `icon.png`    | square symbol           | 256×256      |
| `icon@2x.png` | square symbol           | 512×512      |
| `icon.svg`    | square vector of `icon` | any, square  |
| `logo.png`    | landscape wordmark      | e.g. 256×128 |
| `logo@2x.png` | landscape wordmark      | e.g. 512×256 |

Once the assets exist, submit the same files to
[home-assistant/brands](https://github.com/home-assistant/brands) so Home
Assistant renders them for every user.
