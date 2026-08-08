import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

async function render() {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);

  return worker.fetch(
    new Request("http://localhost/", {
      headers: { accept: "text/html" },
    }),
    {
      ASSETS: {
        fetch: async () => new Response("Not found", { status: 404 }),
      },
    },
    {
      waitUntil() {},
      passThroughOnException() {},
    },
  );
}

async function renderPath(pathname) {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}-${pathname}`);
  const { default: worker } = await import(workerUrl.href);
  return worker.fetch(new Request(`http://localhost${pathname}`, { headers: { accept: "text/html" } }), { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } }, { waitUntil() {}, passThroughOnException() {} });
}

test("server-renders the DeepAlign-Bench research report", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);

  const html = await response.text();
  assert.match(html, /<html lang="zh-CN">/i);
  assert.match(html, /<title>DeepAlign-Bench｜研究汇报<\/title>/i);
  assert.match(html, /DEEP RESEARCH EVALUATION ATLAS/i);
  assert.match(html, /Coverage manifest/i);
  assert.match(html, /24 个任务 family/);
  assert.match(html, /48 个 user-task/);
  assert.match(html, /MUST CHANGE/i);
  assert.match(html, /href="\/case\.schema\.yaml"/i);
  assert.match(html, /href="\/DeepAlign-Bench_正式研究Proposal\.pdf"/i);
  assert.match(html, /href="\/DeepAlign-Bench_正式Proposal精简版\.pdf"/i);
  assert.match(html, /href="\/DeepAlign-Bench_完整人话版\.pdf"/i);
  assert.match(html, /href="\/DeepAlign-Bench_汇报精简版\.pdf"/i);
  assert.match(html, /同一套方法，按阅读场景分成四版/);
  assert.match(html, /8 个 anchor 是固定实验宿主；扰动才是处理变量/);
  assert.match(html, /href="\/literature"/i);
  assert.match(html, /href="\/figures"/i);
  assert.match(html, /href="\/rubrics"/i);
  assert.match(html, /class="inlineCite"[^>]+2607\.27056/i);
  assert.match(html, /class="inlineCite"[^>]+2509\.25106/i);
  assert.match(html, /task\/persona-conditioned rubric/i);
  assert.match(html, /2×2 矩阵 Mij = PFi\(Yj\)/i);
  assert.match(html, /absolute adaptation evaluation/i);
  assert.match(html, /counterfactual personalization effect/i);
  assert.match(html, /must-change \/ must-hold \/ must-not/i);
  assert.match(html, /不证明内部“理解用户”/i);
  assert.match(html, /cue-equivalence robustness/i);
  assert.match(html, /Task family 与 persona 不是靠写 prompt 拼出来的/);
  assert.match(html, /S0 clean/);
  assert.match(html, /E1 · Controlled Frozen Harness/);
  assert.match(html, /A1 日常决策/);
  assert.match(html, /PCA=\.43/);
  assert.match(html, /PROFILE D/);
  assert.match(html, /Boundary &amp; Governance/i);
  assert.doesNotMatch(html, /re-anchor|S4 恢复|Recovery &amp; Governance/i);
  assert.match(html, /href="\/PROJECT_MEMORY\.md"/i);
  assert.match(html, /alt="DeepAlign-Bench 总体流程图"/i);
});

test("server-renders the rubric compiler workbench", async () => {
  const response = await renderPath("/rubrics");
  assert.equal(response.status, 200);
  const html = await response.text();
  assert.match(html, /Rubric Compiler 的六步执行链/);
  assert.match(html, /Leaf expansion/);
  assert.match(html, /CFA 不会出现在任何 leaf/);
  assert.match(html, /U-A-BUDGET-01/);
  assert.match(html, /href="\/rubric_leaf\.schema\.yaml"/i);
  assert.match(html, /href="\/metric_binding\.schema\.yaml"/i);
  assert.match(html, /href="\/rubric_bundle\.example\.yaml"/i);
});

test("server-renders the 29-paper related-work map", async () => {
  const response = await renderPath("/literature");
  assert.equal(response.status, 200);
  const html = await response.text();
  assert.match(html, /29 篇工作，把我们的题目/);
  assert.match(html, /Setoka/);
  assert.match(html, /PersonaTrail/);
  assert.match(html, /PASB/);
  assert.match(html, /APeB/);
  assert.match(html, /MyScholarQA/);
  assert.match(html, /Mem2ActBench/);
  assert.match(html, /22-PAPER RELEVANCE AUDIT/);
  assert.match(html, /四项最低成立条件/);
  assert.match(html, /One Persona, Many Cues/);
  assert.match(html, /PARL/);
  assert.match(html, /class="inlineCite"[^>]+2607\.21635/i);
  assert.match(html, /class="inlineCite"[^>]+2607\.10526/i);
});

test("server-renders the paper figure and table blueprint", async () => {
  const response = await renderPath("/figures");
  assert.equal(response.status, 200);
  const html = await response.text();
  assert.match(html, /2 张方法图 \+ 2 张结果图 \+ 1 张测量效度图/);
  assert.match(html, /Counterfactual family 构造与评分/);
  assert.match(html, /PF swapped/);
  assert.match(html, /Multi-label failure incidence/);
  assert.match(html, /完整 18 个交叉格/);
  assert.match(html, /JudgeBench 与人类校准/);
  assert.match(html, /主 Leaderboard 数值/);
  assert.match(html, /明确不建议/);
});

test("keeps the machine-readable metadata and downloadable artifacts in sync", async () => {
  const [page, schema, leafSchema, templateRegistry, metricBinding, exampleBundle, manifest] = await Promise.all([
    readFile(new URL("../app/page.tsx", import.meta.url), "utf8"),
    readFile(new URL("../public/case.schema.yaml", import.meta.url), "utf8"),
    readFile(new URL("../public/rubric_leaf.schema.yaml", import.meta.url), "utf8"),
    readFile(new URL("../public/rubric_template_registry.yaml", import.meta.url), "utf8"),
    readFile(new URL("../public/metric_binding.schema.yaml", import.meta.url), "utf8"),
    readFile(new URL("../public/rubric_bundle.example.yaml", import.meta.url), "utf8"),
    readFile(
      new URL("../../benchmark_schema/coverage_manifest.template.csv", import.meta.url),
      "utf8",
    ),
  ]);

  assert.match(page, /task\.\* · environment\.\* · user_state\.\*/);
  assert.match(page, /must-change · must-hold · must-not · clarify-if-unknown/i);
  assert.match(schema, /^schema_version:\s*0\.28/m);
  assert.match(schema, /evaluation_contract:/);
  assert.match(schema, /counterfactual_partner_id:/);
  assert.match(schema, /estimand:\s*counterfactual_personalization_effect/);
  assert.match(schema, /execution_regime:/);
  assert.doesNotMatch(schema, /S4_recovery_pair|reanchor|recovery_prompt|recovery_policy/);
  assert.match(schema, /stage: \[S0_clean, S1_single_light, S2_single_strong, S3_compound\]/);
  assert.match(schema, /minimal_counterfactual_edit:/);
  assert.match(schema, /rubric_compilation:/);
  assert.match(leafSchema, /direct_metric_bindings:/);
  assert.doesNotMatch(leafSchema, /^\s+- CFA\s*$/m);
  assert.match(templateRegistry, /expand_to_atomic_leaves/);
  assert.match(metricBinding, /CFA:/);
  assert.match(metricBinding, /CFA is not a leaf score/);
  assert.match(exampleBundle, /U-A-BUDGET-01/);
  assert.match(exampleBundle, /apply unchanged to both Y_a and Y_b/);
  assert.match(manifest, /coverage_status/);
  assert.match(manifest, /tested/);
  assert.match(manifest, /defined_only/);

  await Promise.all([
    access(new URL("../public/DeepAlign-Bench_主图.png", import.meta.url)),
    access(
      new URL("../public/DeepAlign-Bench_正式研究Proposal.docx", import.meta.url),
    ),
    access(
      new URL("../public/DeepAlign-Bench_正式研究Proposal.pdf", import.meta.url),
    ),
    access(new URL("../public/DeepAlign-Bench_正式Proposal精简版.docx", import.meta.url)),
    access(new URL("../public/DeepAlign-Bench_正式Proposal精简版.pdf", import.meta.url)),
    access(new URL("../public/DeepAlign-Bench_完整人话版.docx", import.meta.url)),
    access(new URL("../public/DeepAlign-Bench_完整人话版.pdf", import.meta.url)),
    access(new URL("../public/DeepAlign-Bench_汇报精简版.docx", import.meta.url)),
    access(new URL("../public/DeepAlign-Bench_汇报精简版.pdf", import.meta.url)),
    access(new URL("../public/PROJECT_MEMORY.md", import.meta.url)),
    access(new URL("../public/og.png", import.meta.url)),
  ]);
});
