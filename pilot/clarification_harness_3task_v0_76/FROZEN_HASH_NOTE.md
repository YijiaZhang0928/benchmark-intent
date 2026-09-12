# Frozen-hash note

`FROZEN_HASHES.sha256` was written before generation. It intentionally remains
unchanged. The listed hash for `README.md` no longer matches because the README
received a post-run result summary. The immutable design, cases, simulator
protocol, and six model-input files must still match their listed hashes and
are checked by `validate.py`.

Future packages should keep mutable status documentation out of the frozen
input hash manifest.
