# README standard for integrations

Every integration made from this template opens its repository with a README
written to this standard. The README is read in two places:

| Where                                     | Who                                              | What they need                                      |
|-------------------------------------------|--------------------------------------------------|-----------------------------------------------------|
| GitHub                                    | Users deciding to install, contributors          | Everything                                          |
| Home Assistant Marketplace (HA 2026.11+)  | A user already inside Home Assistant, one click from **Install** | What it does, what it needs, how to set it up and use it |

Write it for the Home Assistant user. Describe what they get, never how the
code is built or the brief it was built from.

## Marketplace exclusion markers

Parts that only make sense on GitHub go between these markers. GitHub hides
HTML comments, so the GitHub page does not change:

```markdown
<!-- ha-marketplace:exclude-start -->
GitHub-only content
<!-- ha-marketplace:exclude-end -->
```

- A section runs from a start marker to the next end marker. A marker left
  open hides everything to the end of the file. Markers inside code blocks
  are plain text.
- Exclude the badge block and the "open in Home Assistant" button,
  **Installation**, **Contributing** and **License**. Keep **Support**
  visible.
- Headings get no ids in the Marketplace, so a link such as
  `[Configuration](#configuration)` leads nowhere there. Name the section in
  words instead ("see Configuration below"). Anchor links are fine only
  inside excluded blocks.
- Relative links to `.md` files open on GitHub, and relative images load from
  the released version. Use relative paths for repository files.
- `#123` becomes a link to issue 123. Avoid a bare `#` followed by a number
  that is not an issue.

## Section order

Use only the sections that apply, in this order, with these headings. A
repository whose `hacs.json` declares `"country": ["BR"]` uses the heading in
brackets and writes all prose in Brazilian Portuguese.

| Section                                       | Content                                                         |
|-----------------------------------------------|-----------------------------------------------------------------|
| `# <name>`                                    | The `name` from `hacs.json`, without "for Home Assistant"       |
| Header (excluded)                             | Badges and the "open in Home Assistant" button                  |
| Lead paragraph                                | What it does, local or cloud, a link to the companion SDK       |
| `## Supported devices` [Dispositivos suportados] | A model table, when there is more than one model             |
| `## Features` [Recursos]                      | Short bullets with the value for the user, not the internals   |
| `## Requirements` [Requisitos]                | Home Assistant version (as in `hacs.json`), hardware, accounts, network |
| `## Installation` [Instalação] (excluded)     | Marketplace and manual, from the template below                 |
| `## Configuration` [Configuração]             | UI path, fields table, Reconfigure and reauthentication         |
| `## Options` [Opções]                         | Setting, default, range and effect                              |
| `## Entities` [Entidades]                     | One table per kind of device                                    |
| `## Actions` [Ações]                          | One `###` per action, a fields table and a YAML example         |
| `## Events` [Eventos]                         | Event types, payload and an automation example                  |
| `## Dashboard card` [Card de dashboard]       | A bundled card: YAML and its options table                      |
| `## How it works` [Como funciona]             | Where the data comes from, how often, what is local or cloud    |
| `## Troubleshooting` [Solução de problemas]   | Symptom, cause and fix. Diagnostics download, debug logging     |
| `## Known limitations` [Limitações conhecidas] |                                                                |
| `## Support` [Apoie o projeto]                | The fixed text below and a line pointing to the issue tracker   |
| `## Contributing` [Contribuindo] (excluded)   | Two lines pointing to `CONTRIBUTING.md` and `CODE_STYLE.md`     |
| `## License` [Licença] (excluded)             |                                                                 |

## Header

No `---` line after the header: the badges are hidden in the Marketplace, so
the line would open the page.

```markdown
# <Name>

<!-- ha-marketplace:exclude-start -->
[![CI](https://github.com/<owner>/<repo>/actions/workflows/ci.yml/badge.svg)](https://github.com/<owner>/<repo>/actions/workflows/ci.yml)
[![GitHub release](https://img.shields.io/github/v/release/<owner>/<repo>)](https://github.com/<owner>/<repo>/releases/latest)
[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-db61a2?logo=githubsponsors&logoColor=white)](https://github.com/sponsors/<owner>)

[![Open your Home Assistant instance and open a repository in the Marketplace.](https://my.home-assistant.io/badges/marketplace_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=<owner>&repository=<repo>&category=integration)
<!-- ha-marketplace:exclude-end -->
```

- The `hacs_repository` redirect opens HACS before Home Assistant 2026.11 and
  the Marketplace from 2026.11 on. A repository whose minimum version is
  2026.11 or later may use `marketplace_repository` in the link too.
- Do not add the orange "HACS Custom" badge.
- A private repository gets no button: Home Assistant cannot install from it.
  Add the button when the repository becomes public.

## Installation

```markdown
<!-- ha-marketplace:exclude-start -->
## Installation

### Home Assistant Marketplace (recommended)

1. Select the **Open your Home Assistant instance** button above, or go to
   **Settings → Marketplace**, select **Add from link** in the upper right
   corner, enter `<owner>/<repo>` and select **Add**.
2. Select **Install**.
3. Restart Home Assistant.

The Marketplace comes with Home Assistant 2026.11 and later. On older
versions, add this repository to HACS as a custom repository of type
**Integration** and install it from there.

### Manual

1. Download `<domain>.zip` from the [latest release](https://github.com/<owner>/<repo>/releases/latest).
2. Extract it into `config/custom_components/<domain>/`.
3. Restart Home Assistant.
<!-- ha-marketplace:exclude-end -->
```

Drop the HACS paragraph when `hacs.json` requires Home Assistant 2026.11 or
later.

## Configuration, options and entities

- No "add integration" button. The Marketplace page already leads to setup,
  and a reader on GitHub has not installed yet. Give the path instead:
  **Settings → Devices & services → Add integration**.
- Field and entity names exactly as `translations/en.json` shows them (or
  `pt-BR.json` for a Brazilian repository).
- Ranges in words ("from 10 to 600"), never with a dash.
- Say in plain sentences what **Reconfigure** and reauthentication do.
- Entities go in tables with the entity, its type, its unit or states and
  notes. Mark the ones that are diagnostic or disabled by default.
- Check every entity, default, range, action and version against the code,
  `const.py`, `hacs.json` and `manifest.json`. Document nothing the code does
  not do.

## Support text

Pick the variant that fits. An integration for a physical device keeps the
hardware clause:

```markdown
## Support

This integration is built and maintained on personal time, on hardware bought
for the purpose. If it is useful to you, consider
[sponsoring the work](https://github.com/sponsors/<owner>). It keeps the
devices, the testing and the releases coming.
```

An integration that uses no device of its own (a cloud or public API, Docker,
a theme) drops it:

```markdown
## Support

This integration is built and maintained on personal time. If it is useful
to you, consider [sponsoring the work](https://github.com/sponsors/<owner>).
It keeps the fixes, the testing and the releases coming.
```

In Brazilian Portuguese, under `## Apoie o projeto`, with and without the
hardware clause:

```markdown
Esta integração é desenvolvida e mantida no meu tempo livre, com aparelhos
comprados para isso. Se ela for útil para você, considere
[patrocinar o trabalho](https://github.com/sponsors/<owner>). É o que mantém
os aparelhos, os testes e as novas versões.
```

```markdown
Esta integração é desenvolvida e mantida no meu tempo livre. Se ela for
útil para você, considere
[patrocinar o trabalho](https://github.com/sponsors/<owner>). É o que
garante as correções, os testes e as novas versões.
```

Follow it with one line pointing to the issue tracker for bugs and requests.

## Brazilian Portuguese labels

Use the labels of the Home Assistant interface in Brazilian Portuguese, in
bold: **Configurações → Marketplace**, **Adicionar a partir de link**, the
field **Link do GitHub**, **Adicionar**, **Instalar** and **Configurações →
Dispositivos e serviços → Adicionar integração**. The Marketplace heading is
`### Marketplace do Home Assistant (recomendado)`.

## Writing

- Lead with what the user gets ("See who is connected to your network"), not
  with how it works inside. Words such as coordinator, registry or SDK
  internals stay out of the visible part.
- Plain words, short sentences, second person, present tense. UI labels in
  bold, UI paths with `→`.
- No em dash or en dash anywhere, ranges included. Use a period, a comma,
  parentheses or a colon.
- No bold lead-in on every bullet and no bold for emphasis. Bold is for UI
  labels.
- None of "out of the box", "seamless", "effortless", "robust", "leverage",
  "simply", "just", "Note that", "Whether you" or "No X required".
- No forced groups of three, no emoji, no questions as headings, no chains of
  clauses joined by semicolons.
- Troubleshooting entries start with the symptom in bold, as the user would
  describe it, followed by the cause and the fix in one or two sentences.
- Nothing about the maintainer's own setup or tools.

## Repository description and topics

The Marketplace catalog needs both. The description is one or two plain
sentences in the README language saying what the user gets, without dashes.
The topics always include `home-assistant`, `homeassistant`, `hacs` and
`home-assistant-integration`, plus the brand, the product and the use case
(for example `presence-detection`).

## Checking the result

1. `grep -n '—\|–' README.md CONTRIBUTING.md` prints nothing.
2. Read the README with the excluded blocks removed. Nothing left may depend
   on a badge, the Installation section or an in-page link.
3. Every relative link points to a file that exists.
