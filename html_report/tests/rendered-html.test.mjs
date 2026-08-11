import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

async function render() {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);
  return worker.fetch(
    new Request("http://localhost/", { headers: { accept: "text/html" } }),
    { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } },
    { waitUntil() {}, passThroughOnException() {} },
  );
}

test("server-renders the ElicitAlign-Bench v0.45 report", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  const html = await response.text();
  assert.match(html, /<html lang="zh-CN">/i);
  assert.match(html, /<title>ElicitAlign-Bench｜研究汇报<\/title>/i);
  assert.match(html, /从缺失用户信息到/);
  assert.match(html, /C0 Natural-Interactive/);
  assert.match(html, /C3 Full-Persona Oracle/);
  assert.match(html, /Natural 不提醒；Nudge 只作诊断/);
  assert.match(html, /unknown → asked → answered/);
  assert.match(html, /OracleRecovery/);
  assert.match(html, /G-STEER 的 benchmark 化/);
  assert.match(html, /NOVELTY-KILL PILOT/i);
  assert.match(html, /src="\/ElicitAlign-Bench_端到端流程图_v0\.45\.png"/i);
  assert.match(html, /href="\/ElicitAlign-Bench_正式研究Proposal\.pdf"/i);
  assert.match(html, /href="\/ElicitAlign-Bench_正式Proposal精简版\.pdf"/i);
  assert.match(html, /href="\/ElicitAlign-Bench_完整人话版\.pdf"/i);
  assert.match(html, /href="\/ElicitAlign-Bench_汇报精简版\.pdf"/i);
  assert.match(html, /href="\/elicitalign_case\.schema\.yaml"/i);
  assert.match(html, /href="\/elicitalign_evaluation\.protocol\.yaml"/i);
  assert.doesNotMatch(html, /DeepAlign-Bench_正式研究Proposal/);
});

test("keeps v0.45 schemas and downloadable artifacts in sync", async () => {
  const [page, schema, protocol] = await Promise.all([
    readFile(new URL("../app/page.tsx", import.meta.url), "utf8"),
    readFile(new URL("../public/elicitalign_case.schema.yaml", import.meta.url), "utf8"),
    readFile(new URL("../public/elicitalign_evaluation.protocol.yaml", import.meta.url), "utf8"),
  ]);
  assert.match(page, /SelfInitiatedGain/);
  assert.match(page, /NudgeGap/);
  assert.match(page, /OracleGap/);
  assert.match(schema, /schema_version:\s*["']0\.45["']/);
  assert.match(schema, /user_state_ledger:/);
  assert.match(schema, /underspecification:/);
  assert.match(schema, /must_change:/);
  assert.match(protocol, /natural_interactive/);
  assert.match(protocol, /full_persona_oracle/);
  assert.match(protocol, /family_blocked_permutation/);
  assert.match(protocol, /family_cluster_bootstrap/);

  await Promise.all([
    access(new URL("../public/ElicitAlign-Bench_端到端流程图_v0.45.png", import.meta.url)),
    access(new URL("../public/ElicitAlign-Bench_端到端流程图_v0.45.svg", import.meta.url)),
    access(new URL("../public/ElicitAlign-Bench_正式研究Proposal.docx", import.meta.url)),
    access(new URL("../public/ElicitAlign-Bench_正式研究Proposal.pdf", import.meta.url)),
    access(new URL("../public/ElicitAlign-Bench_正式Proposal精简版.docx", import.meta.url)),
    access(new URL("../public/ElicitAlign-Bench_正式Proposal精简版.pdf", import.meta.url)),
    access(new URL("../public/ElicitAlign-Bench_完整人话版.docx", import.meta.url)),
    access(new URL("../public/ElicitAlign-Bench_完整人话版.pdf", import.meta.url)),
    access(new URL("../public/ElicitAlign-Bench_汇报精简版.docx", import.meta.url)),
    access(new URL("../public/ElicitAlign-Bench_汇报精简版.pdf", import.meta.url)),
    access(new URL("../public/PROJECT_MEMORY.md", import.meta.url)),
  ]);
});
