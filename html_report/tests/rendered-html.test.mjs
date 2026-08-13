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

test("server-renders the DeepAlign-Bench v0.50 report", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  const html = await response.text();
  assert.match(html, /<html lang="zh-CN">/i);
  assert.match(html, /<title>DeepAlign-Bench｜研究汇报<\/title>/i);
  assert.match(html, /绝对适配不等于/);
  assert.match(html, /P2 Pre-research clarification/);
  assert.match(html, /P4 Checkpoint update/);
  assert.match(html, /3-family \/ 24-episode/);
  assert.match(html, /CFA_min/);
  assert.match(html, /General-good 近 matched/);
  assert.match(html, /当前没有 GPT-5 completion、criteria 或分数/);
  assert.match(html, /Introduction 证据门/);
  assert.match(html, /FIVE-DAY THESIS FREEZE/);
  assert.match(html, /src="\/DeepAlign-Bench_整体框架与PDR压力测试_v0\.50\.png"/i);
  assert.match(html, /href="\/DeepAlign-Bench_正式Proposal精简版\.pdf"/i);
  assert.match(html, /href="\/case\.schema\.yaml"/i);
  assert.match(html, /href="\/research_episode\.schema\.yaml"/i);
  assert.match(html, /href="\/seed_v0_50_families\.yaml"/i);
  assert.doesNotMatch(html, /ElicitAlign-Bench/);
});

test("keeps v0.50 schemas, seed and downloadable artifacts in sync", async () => {
  const [schema, metrics, episodeSchema, seed] = await Promise.all([
    readFile(new URL("../public/case.schema.yaml", import.meta.url), "utf8"),
    readFile(new URL("../public/metric_binding.schema.yaml", import.meta.url), "utf8"),
    readFile(new URL("../public/research_episode.schema.yaml", import.meta.url), "utf8"),
    readFile(new URL("../public/seed_v0_50_families.yaml", import.meta.url), "utf8"),
  ]);
  assert.match(schema, /schema_version:\s*0\.50/);
  assert.match(schema, /fuzzy_query_clarification/);
  assert.match(schema, /adopted_in_final_node_ids/);
  assert.match(metrics, /CFA_min/);
  assert.match(metrics, /artifact_specificity_profile_is_primary:\s*true/);
  assert.match(episodeSchema, /P5_memory_retrieval/);
  assert.match(seed, /F0503_research_literature_workflow/);

  await Promise.all([
    access(new URL("../public/DeepAlign-Bench_整体框架与PDR压力测试_v0.50.png", import.meta.url)),
    access(new URL("../public/DeepAlign-Bench_整体框架与PDR压力测试_v0.50.svg", import.meta.url)),
    access(new URL("../public/DeepAlign-Bench_正式研究Proposal.docx", import.meta.url)),
    access(new URL("../public/DeepAlign-Bench_正式研究Proposal.pdf", import.meta.url)),
    access(new URL("../public/DeepAlign-Bench_正式Proposal精简版.docx", import.meta.url)),
    access(new URL("../public/DeepAlign-Bench_正式Proposal精简版.pdf", import.meta.url)),
    access(new URL("../public/DeepAlign-Bench_完整人话版.docx", import.meta.url)),
    access(new URL("../public/DeepAlign-Bench_完整人话版.pdf", import.meta.url)),
    access(new URL("../public/DeepAlign-Bench_汇报精简版.docx", import.meta.url)),
    access(new URL("../public/DeepAlign-Bench_汇报精简版.pdf", import.meta.url)),
    access(new URL("../public/PROJECT_MEMORY.md", import.meta.url)),
  ]);
});
