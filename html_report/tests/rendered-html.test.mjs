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

test("server-renders the DeepAlign-Bench v0.59 report", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  const html = await response.text();
  assert.match(html, /<html lang="zh-CN">/i);
  assert.match(html, /<title>DeepAlign-Bench｜研究汇报<\/title>/i);
  assert.match(html, /绝对适配不等于/);
  assert.match(html, /HUMAN TRUTH → RELATIONAL GOLD/);
  assert.match(html, /CREDAMO · OPEN FIRST · HUMAN CONFIRMED/);
  assert.match(html, /RUNNABLE PYTHON · RESET \/ STEP · VALUE MINIMIZATION/);
  assert.match(html, /同一 hidden persona，三种可控交互模式/);
  assert.match(html, /Interactive 的 classifier 只看 value-free descriptor/);
  assert.match(html, /3–5 个是候选任务/);
  assert.match(html, /Counterfactual Difference Map/);
  assert.match(html, /D-JQS/);
  assert.match(html, /180 candidate seeds/);
  assert.match(html, /60 provisional families/);
  assert.match(html, /One primary artifact each/);
  assert.match(html, /24 个 DR 只产出检索、核验或综合型 evidence artifact/);
  assert.match(html, /12 families：5 \/ 3 \/ 4/);
  assert.match(html, /CFA_min/);
  assert.match(html, /General-good 近 matched/);
  assert.match(html, /当前没有 GPT-5 completion、criteria 或分数/);
  assert.match(html, /Introduction 证据门/);
  assert.match(html, /PAPER-FIRST EXECUTION/);
  assert.match(html, /src="\/DeepAlign-Bench_真人真值到D-JQS_v0\.55\.png"/i);
  assert.match(html, /href="\/DeepAlign-Bench_正式Proposal精简版\.pdf"/i);
  assert.match(html, /href="\/case\.schema\.yaml"/i);
  assert.match(html, /href="\/counterfactual_difference_map\.schema\.yaml"/i);
  assert.match(html, /href="\/human_ground_truth\.protocol\.yaml"/i);
  assert.match(html, /href="\/credamo_persona_collection\.protocol\.yaml"/i);
  assert.match(html, /href="\/credamo_question_bank\.json"/i);
  assert.match(html, /href="\/DeepAlign-Bench_Credamo真人Persona问卷方案_v0\.59\.pdf"/i);
  assert.match(html, /href="\/judge_qualification\.protocol\.yaml"/i);
  assert.match(html, /href="\/interaction_environment\.schema\.yaml"/i);
  assert.match(html, /href="\/interaction_demo_case\.json"/i);
  assert.match(html, /href="\/interaction_env_manifest\.json"/i);
  assert.match(html, /href="\/plhkw_task_catalog\.html"/i);
  assert.match(html, /href="\/plhkw_tasks_60\.md"/i);
  assert.match(html, /href="\/plhkw_selected_tasks\.jsonl"/i);
  assert.match(html, /href="\/DeepAlign-Bench_PLHKW任务资源池_v0\.59\.svg"/i);
  assert.match(html, /href="\/plhkw_selected_tasks\.csv"/i);
  assert.match(html, /href="\/plhkw_paper_first_12\.csv"/i);
  assert.doesNotMatch(html, /ElicitAlign-Bench/);
});

test("keeps v0.59 resources, schemas and downloadable artifacts in sync", async () => {
  const [schema, metrics, episodeSchema, seed, cdm, humanTruth, judgeQualification, credamoProtocol, questionBank, interactionProtocol, interactionCase] = await Promise.all([
    readFile(new URL("../public/case.schema.yaml", import.meta.url), "utf8"),
    readFile(new URL("../public/metric_binding.schema.yaml", import.meta.url), "utf8"),
    readFile(new URL("../public/research_episode.schema.yaml", import.meta.url), "utf8"),
    readFile(new URL("../public/seed_v0_50_families.yaml", import.meta.url), "utf8"),
    readFile(new URL("../public/counterfactual_difference_map.schema.yaml", import.meta.url), "utf8"),
    readFile(new URL("../public/human_ground_truth.protocol.yaml", import.meta.url), "utf8"),
    readFile(new URL("../public/judge_qualification.protocol.yaml", import.meta.url), "utf8"),
    readFile(new URL("../public/credamo_persona_collection.protocol.yaml", import.meta.url), "utf8"),
    readFile(new URL("../public/credamo_question_bank.json", import.meta.url), "utf8"),
    readFile(new URL("../public/interaction_environment.schema.yaml", import.meta.url), "utf8"),
    readFile(new URL("../public/interaction_demo_case.json", import.meta.url), "utf8"),
  ]);
  assert.match(schema, /schema_version:\s*0\.59/);
  assert.match(schema, /knowledge_work_regime/);
  assert.match(schema, /M7_data_analysis_agent/);
  assert.match(schema, /fuzzy_query_clarification/);
  assert.match(schema, /adopted_in_final_node_ids/);
  assert.match(metrics, /CFA_min/);
  assert.match(metrics, /artifact_specificity_profile_is_primary:\s*true/);
  assert.match(episodeSchema, /P5_memory_retrieval/);
  assert.match(seed, /F0503_research_literature_workflow/);
  assert.match(cdm, /acceptable_equivalence/);
  assert.match(cdm, /no_provenance_node_fails_closed/);
  assert.match(humanTruth, /candidate_tasks_selected_per_participant:\s*3_to_5_unless_fewer_are_truly_relevant/);
  assert.match(humanTruth, /deep_elicitation_tasks_per_participant:\s*1_primary_and_at_most_1_secondary/);
  assert.match(judgeQualification, /short_name:\s*D-JQS/);
  assert.match(judgeQualification, /hidden_qualification/);
  assert.match(credamoProtocol, /protocol_version:\s*0\.59/);
  assert.match(credamoProtocol, /open_first/);
  assert.match(questionBank, /"question_id":\s*"O01"/);
  assert.match(interactionProtocol, /schema_version:\s*0\.58/);
  assert.match(interactionProtocol, /interactive_prompt_minimization:\s*mandatory/);
  assert.match(interactionCase, /"attribute_importance_graph"/);
  assert.match(interactionCase, /"attribute_reveal_policy"/);

  await Promise.all([
    access(new URL("../public/DeepAlign-Bench_真人真值到D-JQS_v0.55.png", import.meta.url)),
    access(new URL("../public/DeepAlign-Bench_真人真值到D-JQS_v0.55.svg", import.meta.url)),
    access(new URL("../public/plhkw_task_catalog.html", import.meta.url)),
    access(new URL("../public/plhkw_tasks_60.md", import.meta.url)),
    access(new URL("../public/plhkw_selected_tasks.jsonl", import.meta.url)),
    access(new URL("../public/DeepAlign-Bench_PLHKW任务资源池_v0.59.svg", import.meta.url)),
    access(new URL("../public/plhkw_selected_tasks.csv", import.meta.url)),
    access(new URL("../public/plhkw_paper_first_12.csv", import.meta.url)),
    access(new URL("../public/pdr_candidate_pair_audit.csv", import.meta.url)),
    access(new URL("../public/ICLR2027_weekly_plan.md", import.meta.url)),
    access(new URL("../public/DeepAlign-Bench_正式研究Proposal.docx", import.meta.url)),
    access(new URL("../public/DeepAlign-Bench_正式研究Proposal.pdf", import.meta.url)),
    access(new URL("../public/DeepAlign-Bench_正式Proposal精简版.docx", import.meta.url)),
    access(new URL("../public/DeepAlign-Bench_正式Proposal精简版.pdf", import.meta.url)),
    access(new URL("../public/DeepAlign-Bench_完整人话版.docx", import.meta.url)),
    access(new URL("../public/DeepAlign-Bench_完整人话版.pdf", import.meta.url)),
    access(new URL("../public/DeepAlign-Bench_汇报精简版.docx", import.meta.url)),
    access(new URL("../public/DeepAlign-Bench_汇报精简版.pdf", import.meta.url)),
    access(new URL("../public/DeepAlign-Bench_Credamo真人Persona问卷方案_v0.59.docx", import.meta.url)),
    access(new URL("../public/DeepAlign-Bench_Credamo真人Persona问卷方案_v0.59.pdf", import.meta.url)),
    access(new URL("../public/credamo_task_cards.jsonl", import.meta.url)),
    access(new URL("../public/credamo_routing_matrix.jsonl", import.meta.url)),
    access(new URL("../public/credamo_quality_rules.json", import.meta.url)),
    access(new URL("../public/PROJECT_MEMORY.md", import.meta.url)),
    access(new URL("../public/interaction_env_README.md", import.meta.url)),
    access(new URL("../public/interaction_env_manifest.json", import.meta.url)),
  ]);
});
