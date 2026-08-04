import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "../..");
const siteRoot = resolve(root, "html_report");
const outPath = resolve(root, "deliverables/DeepAlign-Bench_HTML汇报版.html");
const literatureOutPath = resolve(root, "deliverables/DeepAlign-Bench_七篇相关论文速览.html");
const figuresOutPath = resolve(root, "deliverables/DeepAlign-Bench_论文图表蓝图.html");

const css = (await readFile(resolve(siteRoot, "app/globals.css"), "utf8"))
  .replace(/^@import\s+["']tailwindcss["'];?\s*/m, "");
const figure = await readFile(resolve(siteRoot, "public/DeepAlign-Bench_主图.png"));
const figureData = `data:image/png;base64,${figure.toString("base64")}`;

function localizeMainBody(body) {
  return body
  .replaceAll('src="/DeepAlign-Bench_主图.png"', `src="${figureData}"`)
  .replaceAll('href="/DeepAlign-Bench_主图.png"', `href="${figureData}"`)
  .replaceAll('href="/DeepAlign-Bench_正式研究Proposal.pdf"', 'href="./DeepAlign-Bench_正式研究Proposal.pdf"')
  .replaceAll('href="/DeepAlign-Bench_正式研究Proposal.docx"', 'href="./DeepAlign-Bench_正式研究Proposal.docx"')
  .replaceAll('href="/DeepAlign-Bench_正式Proposal精简版.pdf"', 'href="./DeepAlign-Bench_正式Proposal精简版.pdf"')
  .replaceAll('href="/DeepAlign-Bench_正式Proposal精简版.docx"', 'href="./DeepAlign-Bench_正式Proposal精简版.docx"')
  .replaceAll('href="/DeepAlign-Bench_完整人话版.pdf"', 'href="./DeepAlign-Bench_完整人话版.pdf"')
  .replaceAll('href="/DeepAlign-Bench_完整人话版.docx"', 'href="./DeepAlign-Bench_完整人话版.docx"')
  .replaceAll('href="/DeepAlign-Bench_汇报精简版.pdf"', 'href="./DeepAlign-Bench_汇报精简版.pdf"')
  .replaceAll('href="/DeepAlign-Bench_汇报精简版.docx"', 'href="./DeepAlign-Bench_汇报精简版.docx"')
  .replaceAll('href="/case.schema.yaml"', 'href="./case.schema.yaml"')
  .replaceAll('href="/PROJECT_MEMORY.md"', 'href="../PROJECT_MEMORY.md"')
  .replaceAll('href="/literature"', 'href="./DeepAlign-Bench_七篇相关论文速览.html"')
  .replaceAll('href="/figures"', 'href="./DeepAlign-Bench_论文图表蓝图.html"');
}

function localizeLiteratureBody(body) {
  return body.replaceAll('href="/"', 'href="./DeepAlign-Bench_HTML汇报版.html"');
}

function localizeFiguresBody(body) {
  return body.replaceAll('href="/"', 'href="./DeepAlign-Bench_HTML汇报版.html"');
}

async function renderedBody(pathname) {
  const response = await fetch(`http://localhost:3001${pathname}`);
  if (!response.ok) throw new Error(`Unable to fetch ${pathname}: ${response.status}`);
  const rendered = await response.text();
  const bodyMatch = rendered.match(/<body>([\s\S]*?)<script id="_R_">/);
  if (!bodyMatch) throw new Error(`Rendered body was not found for ${pathname}.`);
  return bodyMatch[1];
}

const body = localizeMainBody(await renderedBody("/"));
const literatureBody = localizeLiteratureBody(await renderedBody("/literature"));
const figuresBody = localizeFiguresBody(await renderedBody("/figures"));

const standalone = `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="长程 Deep Research 智能体个性化最终交付物评测方案">
  <title>DeepAlign-Bench｜研究汇报</title>
  <style>${css}</style>
</head>
<body>${body}</body>
</html>
`;

await writeFile(outPath, standalone, "utf8");
const literatureStandalone = `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="七篇最近邻工作精读与二十篇个性化 Agent 论文相关性审计">
  <title>29 篇个性化 Agent 相关工作地图｜DeepAlign-Bench</title>
  <style>${css}</style>
</head>
<body>${literatureBody}</body>
</html>
`;
await writeFile(literatureOutPath, literatureStandalone, "utf8");
const figuresStandalone = `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="DeepAlign-Bench 主文五张图、四张表与附录图表规划">
  <title>论文图表蓝图｜DeepAlign-Bench</title>
  <style>${css}</style>
</head>
<body>${figuresBody}</body>
</html>
`;
await writeFile(figuresOutPath, figuresStandalone, "utf8");
console.log(`${outPath}\n${literatureOutPath}\n${figuresOutPath}`);
