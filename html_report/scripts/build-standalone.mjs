import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "../..");
const siteRoot = resolve(root, "html_report");
const outPath = resolve(root, "deliverables/AskInfer-Bench_HTML汇报版.html");

const css = (await readFile(resolve(siteRoot, "app/globals.css"), "utf8"))
  .replace(/^@import\s+["']tailwindcss["'];?\s*/m, "");
const flowchart = await readFile(resolve(siteRoot, "public/AskInfer-Bench_评测框架_v0.61.png"));
const flowchartData = `data:image/png;base64,${flowchart.toString("base64")}`;

function localize(body) {
  return body
    .replaceAll('src="/AskInfer-Bench_评测框架_v0.61.png"', `src="${flowchartData}"`)
    .replaceAll('href="/AskInfer-Bench_', 'href="./AskInfer-Bench_')
    .replaceAll('href="/ask_infer_case.schema.yaml"', 'href="../benchmark_schema/ask_infer_case.schema.yaml"')
    .replaceAll('href="/ask_infer_evaluation.protocol.yaml"', 'href="../benchmark_schema/ask_infer_evaluation.protocol.yaml"')
    .replaceAll('href="/ask_infer_benchmark.manifest.yaml"', 'href="../benchmark_schema/ask_infer_benchmark.manifest.yaml"')
    .replaceAll('href="/pdr_screening_50.csv"', 'href="../data/pdr_diagnostic_slice_v0_61/screening_50.csv"')
    .replaceAll('href="/pdr_selection_protocol.yaml"', 'href="../data/pdr_diagnostic_slice_v0_61/selection_protocol.yaml"')
    .replaceAll('href="/pdr_selected_15.jsonl"', 'href="../data/pdr_diagnostic_slice_v0_61/selected_15.jsonl"')
    .replaceAll('href="/pdr_selected_15.md"', 'href="../data/pdr_diagnostic_slice_v0_61/selected_15.md"')
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
  <meta name="description" content="AskInfer-Bench：任务特异的主动偏好获取与 history 推断评测">
  <title>Ask or Infer?｜研究汇报</title>
  <style>${css}</style>
</head>
<body>${localize(bodyMatch[1])}</body>
</html>`;

await writeFile(outPath, standalone, "utf8");
console.log(outPath);
