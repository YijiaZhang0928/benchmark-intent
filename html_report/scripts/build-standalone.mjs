import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "../..");
const siteRoot = resolve(root, "html_report");
const outPath = resolve(root, "deliverables/DeepAlign-Bench_HTML汇报版.html");

const css = (await readFile(resolve(siteRoot, "app/globals.css"), "utf8"))
  .replace(/^@import\s+["']tailwindcss["'];?\s*/m, "");
const flowchart = await readFile(resolve(siteRoot, "public/DeepAlign-Bench_真人真值到D-JQS_v0.55.png"));
const flowchartData = `data:image/png;base64,${flowchart.toString("base64")}`;

function localize(body) {
  return body
    .replaceAll('src="/DeepAlign-Bench_真人真值到D-JQS_v0.55.png"', `src="${flowchartData}"`)
    .replaceAll('href="/DeepAlign-Bench_正式研究Proposal.pdf"', 'href="./DeepAlign-Bench_正式研究Proposal.pdf"')
    .replaceAll('href="/DeepAlign-Bench_正式研究Proposal.docx"', 'href="./DeepAlign-Bench_正式研究Proposal.docx"')
    .replaceAll('href="/DeepAlign-Bench_正式Proposal精简版.pdf"', 'href="./DeepAlign-Bench_正式Proposal精简版.pdf"')
    .replaceAll('href="/DeepAlign-Bench_正式Proposal精简版.docx"', 'href="./DeepAlign-Bench_正式Proposal精简版.docx"')
    .replaceAll('href="/DeepAlign-Bench_完整人话版.pdf"', 'href="./DeepAlign-Bench_完整人话版.pdf"')
    .replaceAll('href="/DeepAlign-Bench_完整人话版.docx"', 'href="./DeepAlign-Bench_完整人话版.docx"')
    .replaceAll('href="/DeepAlign-Bench_汇报精简版.pdf"', 'href="./DeepAlign-Bench_汇报精简版.pdf"')
    .replaceAll('href="/DeepAlign-Bench_汇报精简版.docx"', 'href="./DeepAlign-Bench_汇报精简版.docx"')
    .replaceAll('href="/DeepAlign-Bench_Credamo真人Persona问卷方案_v0.59.pdf"', 'href="./DeepAlign-Bench_Credamo真人Persona问卷方案_v0.59.pdf"')
    .replaceAll('href="/DeepAlign-Bench_Credamo真人Persona问卷方案_v0.59.docx"', 'href="./DeepAlign-Bench_Credamo真人Persona问卷方案_v0.59.docx"')
    .replaceAll('href="/DeepAlign-Bench_真人真值到D-JQS_v0.55.svg"', 'href="./DeepAlign-Bench_真人真值到D-JQS_v0.55.svg"')
    .replaceAll('href="/interaction_environment.schema.yaml"', 'href="./interaction_environment.schema.yaml"')
    .replaceAll('href="/interaction_demo_case.json"', 'href="../src/deepalign_bench/data/demo_case.json"')
    .replaceAll('href="/interaction_env_manifest.json"', 'href="../interaction_env/manifest.json"')
    .replaceAll('href="/interaction_env_README.md"', 'href="../interaction_env/README.md"')
    .replaceAll('href="/plhkw_task_catalog.html"', 'href="../data/plhkw_task_pool_v0_59/catalog.html"')
    .replaceAll('href="/plhkw_tasks_60.md"', 'href="../data/plhkw_task_pool_v0_59/tasks_60.md"')
    .replaceAll('href="/plhkw_selected_tasks.jsonl"', 'href="../data/plhkw_task_pool_v0_59/selected_tasks.jsonl"')
    .replaceAll('href="/plhkw_selected_tasks.csv"', 'href="../data/plhkw_task_pool_v0_59/selected_tasks.csv"')
    .replaceAll('href="/plhkw_paper_first_12.csv"', 'href="../data/plhkw_task_pool_v0_59/paper_first_12.csv"')
    .replaceAll('href="/DeepAlign-Bench_PLHKW任务资源池_v0.59.svg"', 'href="./DeepAlign-Bench_PLHKW任务资源池_v0.59.svg"')
    .replaceAll('href="/ICLR2027_weekly_plan.md"', 'href="../proposal/DeepAlign-Bench_ICLR2027每周执行计划.md"')
    .replaceAll('href="/research_episode.schema.yaml"', 'href="../benchmark_schema/research_episode.schema.yaml"')
    .replaceAll('href="/human_ground_truth.protocol.yaml"', 'href="./human_ground_truth.protocol.yaml"')
    .replaceAll('href="/credamo_persona_collection.protocol.yaml"', 'href="../benchmark_schema/credamo_persona_collection.protocol.yaml"')
    .replaceAll('href="/credamo_question_bank.json"', 'href="../data/credamo_persona_survey_v0_59/question_bank.json"')
    .replaceAll('href="/credamo_task_cards.jsonl"', 'href="../data/credamo_persona_survey_v0_59/task_cards.jsonl"')
    .replaceAll('href="/credamo_routing_matrix.jsonl"', 'href="../data/credamo_persona_survey_v0_59/routing_matrix.jsonl"')
    .replaceAll('href="/credamo_quality_rules.json"', 'href="../data/credamo_persona_survey_v0_59/quality_rules.json"')
    .replaceAll('href="/counterfactual_difference_map.schema.yaml"', 'href="./counterfactual_difference_map.schema.yaml"')
    .replaceAll('href="/judge_qualification.protocol.yaml"', 'href="./judge_qualification.protocol.yaml"')
    .replaceAll('href="/case.schema.yaml"', 'href="./case.schema.yaml"')
    .replaceAll('href="/metric_binding.schema.yaml"', 'href="./metric_binding.schema.yaml"')
    .replaceAll('href="/PROJECT_MEMORY.md"', 'href="../PROJECT_MEMORY.md"');
}

const workerUrl = new URL("../dist/server/index.js", import.meta.url);
workerUrl.searchParams.set("standalone", `${process.pid}-${Date.now()}`);
const { default: worker } = await import(workerUrl.href);
const response = await worker.fetch(
  new Request("http://localhost/", { headers: { accept: "text/html" } }),
  { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } },
  { waitUntil() {}, passThroughOnException() {} },
);
if (!response.ok) throw new Error(`Unable to render the home page: ${response.status}`);
const rendered = await response.text();
const bodyMatch = rendered.match(/<body>([\s\S]*?)<script id="_R_">/);
if (!bodyMatch) throw new Error("Rendered body was not found.");

const standalone = `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="DeepAlign-Bench：三类长程知识工作中的反事实个性化评测">
  <title>DeepAlign-Bench｜研究汇报</title>
  <style>${css}</style>
</head>
<body>${localize(bodyMatch[1])}</body>
</html>`;

await writeFile(outPath, standalone, "utf8");
console.log(outPath);
