# relais-spec

The shared contract of Relais, with no code to run:

| File | What it defines |
|---|---|
| `schema/memo.schema.json` | The common format of a memo, whatever the country it comes from: firm, author, date, validity, jurisdictions, domains, numbered passages, sources, mode (`auto` or `contact_only`) |
| `taxonomy/countries.json` | Countries listed on kpmg.com (137, retrieved on 23 November 2026). KPMG states 138 countries and territories, so the list is incomplete |
| `taxonomy/domains.json` | A small flat list of Tax & Legal domains |
| `api/openapi.yaml` | The API used by every client (macOS, Windows, Outlook/Teams) |
| `examples/` | A format example. Its content is invented |

`mode` is chosen by the author for each memo. `auto` allows a level-1 answer that quotes the memo and pays the author a commission. `contact_only` keeps the content private: the memo only tells Relais who to route the question to (level 2).

## Check

```bash
uv run --with jsonschema --with pyyaml --with rfc3339-validator python scripts/validate.py            # the spec itself
uv run --with jsonschema --with pyyaml --with rfc3339-validator python scripts/validate.py ../relais-data/memos   # a set of memos
```
