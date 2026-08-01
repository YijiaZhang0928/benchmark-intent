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
  assert.match(html, /alt="DeepAlign-Bench 总体流程图"/i);
});

test("keeps the machine-readable metadata and downloadable artifacts in sync", async () => {
  const [page, schema, manifest] = await Promise.all([
    readFile(new URL("../app/page.tsx", import.meta.url), "utf8"),
    readFile(new URL("../public/case.schema.yaml", import.meta.url), "utf8"),
    readFile(
      new URL("../../benchmark_schema/coverage_manifest.template.csv", import.meta.url),
      "utf8",
    ),
  ]);

  assert.match(page, /task\.\* · environment\.\* · user_state\.\*/);
  assert.match(page, /must-change · must-hold · must-not · clarify-if-unknown/i);
  assert.match(schema, /^schema_version:\s*0\.12/m);
  assert.match(schema, /evaluation_contract:/);
  assert.match(schema, /counterfactual_partner_id:/);
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
  ]);
});
