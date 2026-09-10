# PDR-T33 integration smoke result

## Passed paths

- Exact original instruction SHA-256 after trimming the terminal newline: `4d958800aa873c244c8645db912d4f510e46cd98595474e544c55c3473cbe4c3`.
- Open Deep Research stock `clarify_with_user` node + `gpt-5.6-sol`: asked before research; no persona, rubric, wrapper, or search was visible. This was a clarification-node probe only.
- DeerFlow calibrated agent + `gpt-5.6-sol`: asked before search, paused through the built-in clarification tool, resumed the same thread with persona-bounded answers, researched, and produced a report.

## Successful DeerFlow run (`r5`)

- Turn 1: one six-field clarification form.
- Turn 2: one residual clarification about the ambiguous meaning of “cleaning system.”
- Turn 3: Deep Research and final report.
- Distinct search queries: 38.
- Full-page fetch attempts: 10.
- Substantive fetch successes (at least 300 readable characters): 6.
- Fetch failures isolated and saved: 4.
- Successful primary/authoritative domains declared for the smoke: `wsava.org`, `oneisall.com`, `dreametechcn.com`.
- Cited URLs in final report: 6.
- Final report length: 23,690 characters.
- Qualification: structural gate pass; primary-source gate pass; `deep_research_qualified=true`.

The report recommends a Samoyed-appropriate, value-oriented bundle and explicitly uses Shanghai/China availability, limited student savings, low ongoing cost, reliability, easy maintenance, the family care setup, and pet acceptance. It avoids inventing a precise food choice until age/weight/current diet are confirmed.

## Infrastructure findings before the pass

Earlier engineering attempts are retained as non-independent smoke diagnostics, not model repetitions:

- Default anonymous Jina fetch returned 401 and DDGS returned empty results.
- When search snippets contained content, the agent performed many searches but skipped full-page fetches.
- A first custom fetch adapter let one blocked website fail the whole parallel tool batch.
- A later run fetched 8 URLs but only 4 returned substantive readable content and cited only 3 URLs, so it correctly failed the frozen DR gate.

The final adapter therefore returns search URLs without usable snippets, validates public URLs and redirects, records per-URL errors without aborting the batch, and treats fewer than 300 readable characters as a failed fetch.
