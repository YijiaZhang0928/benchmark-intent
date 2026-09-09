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

test("server-renders the AskInfer-Bench v0.71 report", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  const html = await response.text();
  assert.match(html, /<html lang="zh-CN">/i);
  assert.match(html, /<title>Ask or Infer\?｜任务特异的个性化评测<\/title>/i);
  assert.match(html, /Ask Calibration Under Preference Divergence/);
  assert.match(html, /full-context personalization/);
  assert.match(html, /不是 implicit elicitation/);
  assert.match(html, /δ = HIGH/);
  assert.match(html, /recoverable · missing_askable · unidentifiable · irrelevant/);
  assert.match(html, /CFA_min/);
  assert.match(html, /排名反转是检验，不是结论/);
  assert.match(html, /src="\/AskInfer-Bench_评测框架_v0\.62\.png"/i);
  assert.match(html, /PDR TASK QUALIFICATION · 50 → 15/i);
  assert.match(html, /15 tasks · 9 domains · 76 official bridge pairs/i);
  assert.match(html, /三个必跑 agent system 共 114 个唯一 episodes/i);
  assert.match(html, /S0 SMOKE PACK · READY/i);
  assert.match(html, /Gemini CLI 0\.46\.0 已安装/i);
  assert.match(html, /Data FAIL/i);
  assert.match(html, /企业账户余额不足/i);
  assert.match(html, /PDR-T30 MINIMUM PRODUCT PILOT/i);
  assert.match(html, /只恢复 39\.53%/i);
  assert.match(html, /44 CRITERIA → 22 UNITS/i);
  assert.match(html, /问到 11\/22，完整落实 5\/22/i);
  assert.match(html, /0\/5 redundant、5\/5 reasonable residual verification/i);
  assert.match(html, /PDR-T01 TWO-AGENT CLARIFICATION PILOT/i);
  assert.match(html, /7\/7 个预冻结 critical preference clusters/i);
  assert.match(html, /7\.057 对 6\.065/i);
  assert.match(html, /PDR-T35 ASK WHAT MATTERS PILOT/i);
  assert.match(html, /共同 zero-ask floor/i);
  assert.match(html, /5\.5383 对 5\.7033/i);
  assert.match(html, /不直接扩 30 题/i);
  assert.match(html, /FIVE-TASK NATIVE CLARIFICATION MATRIX/i);
  assert.match(html, /PDR-T42 · 全球 AI Agent 数据合规/i);
  assert.match(html, /四个产品系统各跑 native\/oracle-top-2 三次/i);
  assert.match(html, /href="\/s0_run_20260904\/RESULTS\.md"/i);
  assert.match(html, /href="\/AskInfer-Bench_正式Proposal精简版\.pdf"/i);
  assert.match(html, /href="\/ask_infer_case\.schema\.yaml"/i);
  assert.match(html, /href="\/ask_infer_evaluation\.protocol\.yaml"/i);
  assert.match(html, /href="\/ask_infer_benchmark\.manifest\.yaml"/i);
});

test("keeps v0.71 manifest, v0.62 stable schemas, task screen, and downloadable artifacts in sync", async () => {
  const [caseSchema, protocol, manifest] = await Promise.all([
    readFile(new URL("../public/ask_infer_case.schema.yaml", import.meta.url), "utf8"),
    readFile(new URL("../public/ask_infer_evaluation.protocol.yaml", import.meta.url), "utf8"),
    readFile(new URL("../public/ask_infer_benchmark.manifest.yaml", import.meta.url), "utf8"),
  ]);
  assert.match(caseSchema, /schema_version:\s*["']?0\.62/);
  assert.match(caseSchema, /missing_askable/);
  assert.match(caseSchema, /unidentifiable/);
  assert.match(caseSchema, /delta_stratum/);
  assert.match(protocol, /high_delta_recall/);
  assert.match(protocol, /question_precision/);
  assert.match(protocol, /cfa_min/);
  assert.match(manifest, /AskInfer-Bench/);
  assert.match(manifest, /manifest_version:\s*["']?0\.71/);
  assert.match(manifest, /task_specific_preference_units:\s*22/);
  assert.match(manifest, /interactive_asked_units:\s*11/);
  assert.match(manifest, /full_persona_redundant_questions:\s*0/);
  assert.match(manifest, /pdr_minimum_product_pilot_is_n1_and_not_leaderboard_evidence/);
  assert.match(manifest, /pdr_two_agent_pilot_shows_clarification_policy_heterogeneity_only/);
  assert.match(manifest, /ask_what_matters_pilot_has_zero_between_agent_calibration_variance/);
  assert.match(manifest, /h2_forced_policy_gate_decision:\s*ASK/);
  assert.match(manifest, /routed_ask_is_scaffolded_capability_and_must_not_replace_native_ask/);
  assert.match(manifest, /planned_reports:\s*120/);
  assert.match(manifest, /native_prompt_contains_no_clarification_instruction/);
  assert.match(manifest, /original_personalization_criteria_per_repeat:\s*37/);
  assert.match(manifest, /task_specific_questions_agent_a:\s*0/);
  assert.match(manifest, /task_specific_questions_agent_b:\s*0/);
  assert.match(manifest, /pdr_is_full_context_projection_not_implicit_elicitation/);
  assert.match(protocol, /selected_task_ids:\s*\[1, 4, 5, 6, 9, 10, 11, 16, 21, 22, 30, 33, 35, 39, 49\]/);
  assert.match(manifest, /published_bridge_pairs:\s*76/);
  assert.match(protocol, /mandatory_three_agents:\s*114/);

  await Promise.all([
    access(new URL("../public/AskInfer-Bench_评测框架_v0.62.png", import.meta.url)),
    access(new URL("../public/AskInfer-Bench_评测框架_v0.62.svg", import.meta.url)),
    access(new URL("../public/pdr_screening_50.csv", import.meta.url)),
    access(new URL("../public/pdr_selection_protocol.yaml", import.meta.url)),
    access(new URL("../public/pdr_selected_15.jsonl", import.meta.url)),
    access(new URL("../public/pdr_selected_15.md", import.meta.url)),
    access(new URL("../public/AskInfer-Bench_正式研究Proposal.docx", import.meta.url)),
    access(new URL("../public/AskInfer-Bench_正式研究Proposal.pdf", import.meta.url)),
    access(new URL("../public/AskInfer-Bench_正式Proposal精简版.docx", import.meta.url)),
    access(new URL("../public/AskInfer-Bench_正式Proposal精简版.pdf", import.meta.url)),
    access(new URL("../public/AskInfer-Bench_完整人话版.docx", import.meta.url)),
    access(new URL("../public/AskInfer-Bench_完整人话版.pdf", import.meta.url)),
    access(new URL("../public/AskInfer-Bench_汇报精简版.docx", import.meta.url)),
    access(new URL("../public/AskInfer-Bench_汇报精简版.pdf", import.meta.url)),
    access(new URL("../public/AskInfer-Bench_两周执行Todo与任务手册.docx", import.meta.url)),
    access(new URL("../public/AskInfer-Bench_两周执行Todo与任务手册.pdf", import.meta.url)),
    access(new URL("../public/AskInfer-Bench_两周执行作战板.html", import.meta.url)),
    access(new URL("../public/AskInfer-Bench_S0-Smoke-README.md", import.meta.url)),
    access(new URL("../public/AskInfer-Bench_S0-Smoke-RUNBOOK.md", import.meta.url)),
    access(new URL("../public/AskInfer-Bench_S0-Smoke-Manifest.json", import.meta.url)),
    access(new URL("../public/AskInfer-Bench_S0-Smoke-Personas.json", import.meta.url)),
    access(new URL("../public/AskInfer-Bench_S0-Smoke-Rubrics.json", import.meta.url)),
    access(new URL("../public/AskInfer-Bench_S0-Smoke-Cases.json", import.meta.url)),
    access(new URL("../public/AskInfer-Bench_S0-Smoke-Scorecard.md", import.meta.url)),
    access(new URL("../public/s0_run_20260904/RESULTS.md", import.meta.url)),
    access(new URL("../public/s0_run_20260904/run_manifest.json", import.meta.url)),
    access(new URL("../public/PROJECT_MEMORY.md", import.meta.url)),
  ]);
});
