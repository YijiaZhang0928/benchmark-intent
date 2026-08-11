import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "../..");
const siteRoot = resolve(root, "html_report");
const outPath = resolve(root, "deliverables/ElicitAlign-Bench_HTML汇报版.html");

const css = (await readFile(resolve(siteRoot, "app/globals.css"), "utf8"))
  .replace(/^@import\s+["']tailwindcss["'];?\s*/m, "");
const flowchart = await readFile(resolve(siteRoot, "public/ElicitAlign-Bench_端到端流程图_v0.45.png"));
const flowchartData = `data:image/png;base64,${flowchart.toString("base64")}`;

function localize(body) {
  return body
    .replaceAll('src="/ElicitAlign-Bench_端到端流程图_v0.45.png"', `src="${flowchartData}"`)
    .replaceAll('href="/ElicitAlign-Bench_正式研究Proposal.pdf"', 'href="./ElicitAlign-Bench_正式研究Proposal.pdf"')
    .replaceAll('href="/ElicitAlign-Bench_正式研究Proposal.docx"', 'href="./ElicitAlign-Bench_正式研究Proposal.docx"')
    .replaceAll('href="/ElicitAlign-Bench_正式Proposal精简版.pdf"', 'href="./ElicitAlign-Bench_正式Proposal精简版.pdf"')
    .replaceAll('href="/ElicitAlign-Bench_正式Proposal精简版.docx"', 'href="./ElicitAlign-Bench_正式Proposal精简版.docx"')
    .replaceAll('href="/ElicitAlign-Bench_完整人话版.pdf"', 'href="./ElicitAlign-Bench_完整人话版.pdf"')
    .replaceAll('href="/ElicitAlign-Bench_完整人话版.docx"', 'href="./ElicitAlign-Bench_完整人话版.docx"')
    .replaceAll('href="/ElicitAlign-Bench_汇报精简版.pdf"', 'href="./ElicitAlign-Bench_汇报精简版.pdf"')
    .replaceAll('href="/ElicitAlign-Bench_汇报精简版.docx"', 'href="./ElicitAlign-Bench_汇报精简版.docx"')
    .replaceAll('href="/ElicitAlign-Bench_端到端流程图_v0.45.svg"', 'href="./ElicitAlign-Bench_端到端流程图_v0.45.svg"')
    .replaceAll('href="/elicitalign_case.schema.yaml"', 'href="./elicitalign_case.schema.yaml"')
    .replaceAll('href="/elicitalign_evaluation.protocol.yaml"', 'href="./elicitalign_evaluation.protocol.yaml"')
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
  <meta name="description" content="ElicitAlign-Bench：自然欠指定任务中的用户状态发现、澄清与最终利用评测">
  <title>ElicitAlign-Bench｜研究汇报</title>
  <style>${css}</style>
</head>
<body>${localize(bodyMatch[1])}</body>
</html>`;

await writeFile(outPath, standalone, "utf8");
console.log(outPath);
