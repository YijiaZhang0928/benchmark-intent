import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Rubric Compiler 工作台｜DeepAlign-Bench",
  description: "从 case 元数据、模板路由和 leaf expansion 到 TQ/PF/MP/CFA 的可执行说明",
};

const pipeline = [
  ["01", "Input", "case metadata · user ledger · contracts · evidence / permission"],
  ["02", "Validate", "字段齐全、事实有来源、contract 有决策后果"],
  ["03", "Route", "按 intent / deliverable / operator / risk 选择固定模板"],
  ["04", "Instantiate", "填入预算、截止时间、用户、证据 ID 与允许披露范围"],
  ["05", "Leaf expansion", "拆成可独立观察、独立给分、带文字锚点的原子项"],
  ["06", "Freeze", "检查覆盖、冲突、A/B 对称性和隐私，版本化后运行 agent"],
];

const templateRows = [
  ["Core", "所有 case", "任务完成 · 关键 claim · 引用 · 基本可用性", "TQ / FR"],
  ["Personalization", "task-relevant user facts + must-change", "目标 · 知识 · 预算 · 风险 · 受众 · 权限", "PF"],
  ["Intent", "6 类 primary_intent", "synthesis · discovery · decision · assessment · plan · audit", "TQ / FR"],
  ["Deliverable", "deliverable_type", "report · memo · workbook · code · slides · webpage · multi-file", "TQ"],
  ["Operator", "acquire / preserve / use / update", "澄清 · 保持 · handoff · 状态更新", "diagnostic Δ"],
  ["Risk", "stakes / permission / sensitive / must-not", "隐私 · 越权 · 冲突/过期 · 安全升级", "MP / gate"],
];

const leafRows = [
  ["criterion_id", "全局唯一、可追踪", "U-A-BUDGET-01"],
  ["source", "来自哪个 template 和 contract", "personalization.constraint + MC-A-01"],
  ["owner + applicability", "为谁评分、何时适用", "owner=Ua；budget fact 已确认"],
  ["observable", "judge 到底查什么", "第一阶段方案 ≤ 50 万"],
  ["evidence", "可看的 artifact / facts / sources", "预算表 + Ua.fact.budget_500k"],
  ["scoring anchors", "每档的可判定定义", "0=超出；1=提及未落实；2=方案与分项均满足"],
  ["weight / severity / gate", "如何聚合、能否补偿", "w=1.0；major；非 gate"],
  ["metric binding", "直接进入哪个指标", "PF"],
  ["judge route", "由谁先判、失败交给谁", "numeric verifier → rubric judge"],
];

const bindingRows = [
  ["common / intent / deliverable", "TQ；事实项同时 FR", "基础质量和事实门槛"],
  ["must-change", "指定用户 PF", "同一组 leaves 评 matched 与 swapped"],
  ["must-hold", "TQ + Neutral Invariance", "单份看质量，跨两份看稳定"],
  ["must-not violation", "MP / hard gate", "隐私、安全和越权不可补偿"],
  ["clarify-if-unknown", "Clarification Correctness", "无依据假设另入 MP"],
  ["operator", "paired diagnostic Δ", "与同前缀 clean control 比较"],
];

export default function RubricsPage() {
  return (
    <main className="rubricWorkbench">
      <header className="rubricHero">
        <nav className="nav shell" aria-label="Rubric 页面导航">
          <a className="brand" href="/">DeepAlign<span>Bench</span></a>
          <div className="navlinks"><a href="#pipeline">编译流程</a><a href="#templates">模板</a><a href="#example">完整例子</a><a href="#binding">指标绑定</a></div>
          <a className="navCta" href="/">返回总报告</a>
        </nav>
        <div className="rubricHeroGrid shell">
          <section>
            <p className="eyebrow">MEETING MODE · RUBRIC COMPILER WORKBENCH</p>
            <h1>从元数据到可审计分数，<em>每一步都能追踪</em></h1>
            <p>Rubric Compiler 不是一个自由生成 rubric 的 LLM。它是一个输出前冻结的规则系统：根据 case 元数据选择固定模板，把 contract 展开成原子 leaf，再显式绑定到直接指标和派生指标。</p>
            <div className="rubricHeroActions"><a href="#example">先看完整例子</a><a href="/rubric_bundle.example.yaml" download>下载 example bundle</a></div>
          </section>
          <aside>
            <span>今晚先讲清三句话</span>
            <ol><li>模板随任务变，leaf schema 不变。</li><li>Leaf expansion 在 agent 运行前完成。</li><li>TQ/PF/MP 直接吃 leaf；CFA 吃四个 PF。</li></ol>
          </aside>
        </div>
      </header>

      <section className="rubricQuick shell">
        <article><b>有 schema</b><p>case、template、leaf、metric binding 四层机器可读定义。</p></article>
        <article><b>有固定模板</b><p>按 intent、deliverable、operator 和 risk 选择，不按输出临时发明。</p></article>
        <article><b>有完整 trace</b><p>criterion → direct metric → aggregate → derived metric。</p></article>
      </section>

      <section className="rubricStatus shell"><b>当前成熟度</b><p>v0.28 已冻结机器可读 compiler contract 与端到端示例；自动 validator、模板路由器和 bundle 导出器是第 1 周实现项。今晚确认的是方法接口、标注成本和测量效度，不把设计文件说成已经完成的生产系统。</p></section>

      <section className="rubricSection shell" id="pipeline">
        <div className="sectionHead"><h2>Rubric Compiler 的六步执行链</h2><p>前五步属于 benchmark 数据制作；第六步冻结后才允许被测 agent 运行。</p></div>
        <div className="compileRail">{pipeline.map(([n,t,d],i)=><article key={n}><span>{n}</span><b>{t}</b><p>{d}</p>{i<pipeline.length-1&&<i>→</i>}</article>)}</div>
        <div className="rubricBoundary"><b>禁止线</b><p>不能看完模型输出再加标准；不能让同一个 judge 同时“发明标准并给分”；探索性新标准可以记录，但不能进入已冻结主榜。</p></div>
      </section>

      <section className="rubricTemplateBand" id="templates">
        <div className="shell">
          <div className="sectionHead light"><h2>模板固定，但不同 task 会走不同路由</h2><p>领域只提供参数与专家阈值，不需要为每个领域重新发明评分语言。</p></div>
          <div className="rubricTable templateTable" role="table">
            <div className="rubricTableRow head"><span>层</span><span>激活条件</span><span>模板内容</span><span>直接指标</span></div>
            {templateRows.map(r=><div className="rubricTableRow" key={r[0]}>{r.map(x=><span key={x}>{x}</span>)}</div>)}
          </div>
          <p className="routeExample"><b>路由例：</b><code>compare_decide + decision_memo + medium stakes + Ua budget constraint</code> → core + decision intent + memo deliverable + personalization.constraint + privacy。</p>
        </div>
      </section>

      <section className="rubricSection shell" id="example">
        <div className="sectionHead"><h2>一个 case 如何从 contract 展开到 leaf</h2><p>示例只说明结构，不是预填实验结果。</p></div>
        <div className="caseRibbon"><span>同一任务</span><b>咖啡店扩店市场研究 · 决策备忘录</b><span>同一证据</span><b>2026Q2 frozen snapshot</b><span>只改用户</span><b>Ua 低预算/可逆试点 ↔ Ub 增长/规模化</b></div>
        <div className="contractToLeaf">
          <article className="contractSource"><span>MUST-CHANGE · MC-A-01</span><h3>建议必须符合 Ua 的 50 万预算和低风险策略</h3><p>这句话不能直接交给 judge，因为它同时混合预算、阶段设计和退出标准。</p></article>
          <i>展开</i>
          <div className="leafCards">
            <article><b>U-A-BUDGET-01</b><p>第一阶段方案 ≤ 50 万</p><small>0 超出 · 1 提及未落实 · 2 方案与分项都满足</small><em>PF · verifier → judge</em></article>
            <article><b>U-A-RISK-02</b><p>给出三个月可逆试点</p><small>0 无 · 1 有试点无阈值 · 2 有继续/退出阈值</small><em>PF · rubric judge</em></article>
            <article><b>U-A-AUD-03</b><p>金融术语首次出现时解释</p><small>0 未解释 · 1 部分 · 2 关键术语均有脚手架</small><em>PF · rubric judge</em></article>
          </div>
        </div>

        <div className="sectionHead compactHead"><h2>每条 leaf 的固定 schema</h2><p>不同任务可以有不同内容，但不能省掉这些审计字段。</p></div>
        <div className="rubricTable leafSchemaTable" role="table">
          <div className="rubricTableRow head"><span>字段</span><span>回答的问题</span><span>示例</span></div>
          {leafRows.map(r=><div className="rubricTableRow" key={r[0]}>{r.map(x=><span key={x}>{x}</span>)}</div>)}
        </div>
      </section>

      <section className="rubricBindingBand" id="binding">
        <div className="shell">
          <div className="sectionHead light"><h2>Leaf 与 TQ、PF、MP、CFA 的绑定</h2><p>直接指标读 leaf；派生指标读直接指标。CFA 不会出现在任何 leaf 的 direct binding 里。</p></div>
          <div className="bindingLayout">
            <div className="rubricTable bindingTable" role="table">
              <div className="rubricTableRow head"><span>Leaf / contract</span><span>直接绑定</span><span>用途</span></div>
              {bindingRows.map(r=><div className="rubricTableRow" key={r[0]}>{r.map(x=><span key={x}>{x}</span>)}</div>)}
            </div>
            <aside className="scoreTrace">
              <span>PF CROSS-SCORING</span>
              <div className="pfMatrix"><b/><b>Yₐ</b><b>Yᵦ</b><b>Ua leaves</b><i>PFₐ(Yₐ)</i><i>PFₐ(Yᵦ)</i><b>Ub leaves</b><i>PFᵦ(Yₐ)</i><i>PFᵦ(Yᵦ)</i></div>
              <code>CFA = ½[(PFₐ(Yₐ)−PFₐ(Yᵦ)) + (PFᵦ(Yᵦ)−PFᵦ(Yₐ))]</code>
              <p>同一用户的 leaves 不因被评分 artifact 改变。这样 CFA 测的是对角优势，而不是两套标准的差异。</p>
            </aside>
          </div>
        </div>
      </section>

      <section className="rubricSection shell">
        <div className="sectionHead"><h2>今晚请导师拍板的可行性问题</h2><p>这些问题决定第 1–3 周能否冻结数据和主 rubric。</p></div>
        <div className="advisorChecks"><article><b>1 · 模板粒度</b><p>六层路由是否足够覆盖主矩阵，又不会造成每个 case 都独立写 rubric？</p></article><article><b>2 · 真值成本</b><p>48 个 user-task 的 must-change 是否能由目标用户确认，must-hold/FR 是否能由专家稳定标注？</p></article><article><b>3 · 识别强度</b><p>人类 reference matched 是否能稳定胜过 swapped，同时 must-hold 和隐私不下降？</p></article><article><b>4 · 两月范围</b><p>先冻结 report/memo/table 三类主交付物，code/slides/web 只进 anchor，是否更稳妥？</p></article></div>
        <div className="schemaDownloads"><b>机器可读材料</b><a href="/case.schema.yaml" download>case schema</a><a href="/rubric_template_registry.yaml" download>template registry</a><a href="/rubric_leaf.schema.yaml" download>leaf schema</a><a href="/metric_binding.schema.yaml" download>metric binding</a><a href="/rubric_bundle.example.yaml" download>端到端 example bundle</a></div>
      </section>

      <footer><div className="shell"><a className="brand" href="/">DeepAlign<span>Bench</span></a><p>Rubric Compiler 工作台 · v0.28</p></div></footer>
    </main>
  );
}
