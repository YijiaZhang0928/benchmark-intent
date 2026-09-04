# S0 interactive smoke protocol — give this to the agent

You are running a development-only interaction smoke test. The task text below is the complete initial user specification. A user-response channel is available before your final response.

You may either continue immediately or request user information. If you request information, return only:

```text
<ASK>
{"questions":["...","..."]}
</ASK>
```

Then wait for the user response. Across the episode you may ask at most three questions in at most two `<ASK>` messages. A question should be short enough for a user to answer in one or two sentences. Do not combine unrelated dimensions into one apparent question.

When ready, return:

```text
<FINAL>
{"decisions":[{"decision":"...","reason":"...","user_information_used":["..."]}],"unknowns_and_safe_defaults":["..."],"next_artifact_actions":["..."]}
</FINAL>
```

For this S0 smoke only, do not fabricate repository, data, web-search, test, or notebook results. Assume the real environment will be attached at S1. Do not spend the question budget asking where that environment is. The final response is a decision record, not the task's scientific deliverable.

This protocol exposes an interaction channel; it does not say that any particular preference is missing or that asking is always correct.
