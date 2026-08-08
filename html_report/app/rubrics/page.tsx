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

const moduleFamilies = [
  ["Core", "6", "任务 · 事实 · 证据 · 推理 · 不确定性 · 可用性", "所有 case 必选/条件选"],
  ["Personalization", "9", "目标 · 内容 · 知识 · 约束 · 风险 · 工作流 · 受众 · 格式 · 动态状态", "user fact + must-change 激活"],
  ["Intent", "6", "synthesis · discover · decide · assess · plan · audit", "每个 case 主选 1 个"],
  ["Deliverable", "7", "report · memo · table · code · slides · web · multi-file", "每个 case 主选 1 个"],
  ["Operator", "4", "acquire · preserve · use · update", "受控诊断，不从 final-only 猜"],
  ["Risk", "4", "隐私 · 安全 · 升级 · 冲突/过期", "风险与 must-not 激活"],
];

const dataStages = [
  ["0", "Vertical slice", "1 个 family 先从 evidence → users → contracts → bundle → 2×2 人评跑通"],
  ["1", "Source ledger", "每篇论文只先标 task / user construct / perturbation / rubric / infrastructure 角色"],
  ["2", "Freeze world", "固定共同任务、证据、工具、权限、预算和 must-hold"],
  ["3", "Minimal user pair", "只改 2–4 个有决策后果且有来源的 user-state axes"],
  ["4", "Contracts", "输出前写 must-change / must-hold / must-not / clarify"],
  ["5", "Compile", "路由预定义 module，再做 atomic leaf expansion 与 binding"],
  ["6", "Human pilot", "matched / swapped / generic / misuse controls 分不出来就删题"],
  ["7", "Scale & audit", "按 Atlas 分层扩展；公开 tested / deferred；按 source lineage 切分"],
];

const validityRows = [
  ["1", "Content mapping", "每个任务要求和授权 user fact 有 leaf，或明确标为只报告字段"],
  ["2", "Discrimination", "人类 reference matched 稳定优于 swapped / generic / misuse"],
  ["3", "Nuisance invariance", "长度、文风、位置和无关 persona 不应提高非适用 leaf"],
  ["4", "Redundancy / ablation", "重复 module 合并；消融后验证是否真的丢失独立 construct"],
  ["5", "Weight sensitivity", "公开 active leaf、NA 分母；合理权重范围内结论不能翻转"],
  ["6", "Human content validity", "目标用户确认 must-change；专家确认事实、证据和高风险边界"],
  ["7", "Residual saturation", "缺失 construct 跨 ≥2 family 重现且不能参数化时才增 module"],
];

const attackRows = [
  ["模块越多越全面？", "研究者自由度、double counting、量尺漂移", "module 去重/消融、weight sensitivity、active leaf/NA 分母公开"],
  ["Persona gold 是作者想象？", "自然人设不等于真实偏好", "授权 user fact + target-user 确认 + acceptable alternatives"],
  ["A/B rubric 不对称？", "leaf 数、权重或严格度不同制造 CFA", "counterfactual symmetry gate；差异必须书面证明"],
  ["Judge 被表面形式影响？", "长度、格式、关键词、位置偏差", "matched-length / swap / keyword controls + module-level JudgeBench"],
  ["Anchor 找到了失败根因？", "异构任务相关性不能识别内部机制", "同前缀配对扰动；≥4 anchors 才做跨任务比较；trace 不可比则只报 outcome"],
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
          <div className="navlinks"><a href="#data-factory">如何造数</a><a href="#modules">模块库</a><a href="#example">完整例子</a><a href="#anchor">Anchor</a><a href="#binding">指标绑定</a></div>
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
        <article><b>有 schema</b><p>case、template、module、leaf、metric binding 和 data factory 六个机器可读对象。</p></article>
        <article><b>有固定模板</b><p>按 intent、deliverable、operator 和 risk 选择，不按输出临时发明。</p></article>
        <article><b>有完整 trace</b><p>criterion → direct metric → aggregate → derived metric。</p></article>
      </section>

      <section className="rubricStatus shell"><b>当前成熟度</b><p>v0.30 已产出 36-module 预定义 library、造数 protocol、compiler contract、端到端示例和 specificity × benefit 判定接口；自动 validator、模板路由器和 bundle 导出器仍是第 1 周实现项。先用一个 vertical slice 验证方法，不把 schema 规模当作实验效度。</p></section>

      <section className="rubricSection shell" id="data-factory">
        <div className="sectionHead"><h2>很多篇论文怎么“杂糅”：按设计角色吸收，不按 taxonomy 求并集</h2><p>每篇来源先进入 source-to-design ledger；同一篇可以贡献多行，但每一行只能承担一个角色。这样 task、persona、failure、rubric 和 infra 不会混成一层。</p></div>
        <div className="dataStageGrid">{dataStages.map(([n,t,d])=><article key={n}><span>{n}</span><b>{t}</b><p>{d}</p></article>)}</div>
        <div className="rubricBoundary"><b>开工门</b><p>在 1 个 family 上，人类 reference matched 必须稳定胜过 swapped；目标用户能确认 must-change；leaf 能独立判分。三项任一失败，都先改 construct，不批量写题。</p></div>
      </section>

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

      <section className="rubricSection shell" id="modules">
        <div className="sectionHead"><h2>预定义 Rubric Module Library · 36 个可路由模块</h2><p>不是每个 case 使用 36 个。主矩阵的 report/memo/table 先以 12–22 active leaves 为目标；code/slides/web/multi-file 先作为 probe。</p></div>
        <div className="rubricTable moduleTable" role="table">
          <div className="rubricTableRow head"><span>Family</span><span>数量</span><span>Module 内容</span><span>激活范围</span></div>
          {moduleFamilies.map(r=><div className="rubricTableRow" key={r[0]}>{r.map(x=><span key={x}>{x}</span>)}</div>)}
        </div>
        <div className="strengthCallout"><b>相对 PDR-Bench，真正的强点</b><p>不是 Personalization module 更多，而是每条个性化 leaf 都有 <code>authorized user fact → must-change → leaf → PF</code> 的 provenance；A/B 模块形状对称；同一 bundle 交叉评分 matched/swapped；must-hold 与 must-not 防止把“变化更多”或“更迎合”当成有效 personalization。</p></div>
      </section>

      <section className="rubricSection shell" id="example">
        <div className="sectionHead"><h2>一个 case 如何从 contract 展开到 leaf</h2><p>示例只说明结构，不是预填实验结果。</p></div>
        <div className="caseRibbon"><span>同一任务</span><b>咖啡店扩店市场研究 · 决策备忘录</b><span>同一证据</span><b>2026Q2 frozen snapshot</b><span>只改用户</span><b>Ua 低预算/可逆试点 ↔ Ub 增长/规模化</b></div>
        <div className="contractToLeaf">
          <article className="contractSource"><span>MUST-CHANGE · MC-A-01</span><h3>建议必须符合 Ua 的 50 万预算和低风险策略</h3><p>这句话不能直接交给 judge，因为它同时混合预算、阶段设计和退出标准。</p></article>
          <i>展开</i>
          <div className="leafCards">
            <article><b>U-A-BUDGET-01</b><p>第一阶段方案 ≤ 50 万</p><small>0 超出 · 1 提及未落实 · 2 方案与分项都满足</small><em>PF · verifier → judge</em></article>
            <article><b>U-A-PILOT-02</b><p>给出三个月可逆试点</p><small>0 无试点 · 1 有试点但不可逆 · 2 有三个月可逆方案</small><em>PF · rubric judge</em></article>
            <article><b>U-A-EXIT-03</b><p>给出继续与退出阈值</p><small>0 无阈值 · 1 只有单向阈值 · 2 继续/退出均可操作</small><em>PF · rubric judge</em></article>
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

      <section className="rubricSection shell" id="anchor">
        <div className="sectionHead"><h2>Anchor family 能回答什么，不能回答什么</h2><p>八个 anchor 是受控压力宿主，不是用八个异构任务做观察性相关分析。</p></div>
        <div className="anchorLogic"><article><b>能识别</b><p>固定 task / evidence / budget / prefix 后，某个 perturbation 让 CFA、PF、invariance、MP 改变多少。</p></article><article><b>不能直接识别</b><p>“长任务分数低”不能证明 long context 是内部用户建模失败根因；final-only 也不能区分没读到、忘了或没使用。</p></article><article><b>跨任务门槛</b><p>主要 perturbation 至少覆盖 4 个适用 anchor 才比较因素；2 个只算探索性复现。机制名只用于可比 trace。</p></article></div>
        <div className="envOrder"><b>环境搭建顺序</b><span>1 · E1：2 family × 2 agent 跑通 frozen vertical slice</span><i>→</i><span>2 · E3：1 anchor 跑通 checkpoint/conflict/update</span><i>→</i><span>3 · E2：1 个商业产品 adapter smoke test</span></div>
      </section>

      <section className="rubricSection shell" id="validity">
        <div className="sectionHead"><h2>怎样判断 module library 是否“够全面”</h2><p>不是数模块名，而是检查 construct 是否覆盖、可区分、抗干扰、非重复，并且得到目标用户和专家支持。</p></div>
        <div className="rubricTable validityTable" role="table"><div className="rubricTableRow head"><span>Gate</span><span>检查</span><span>通过标准</span></div>{validityRows.map(r=><div className="rubricTableRow" key={r[0]}>{r.map(x=><span key={x}>{x}</span>)}</div>)}</div>
      </section>

      <section className="rubricTemplateBand">
        <div className="shell">
          <div className="sectionHead light"><h2>当前设计最可能被攻击的五点</h2><p>这些不是措辞问题，而是 pilot 必须实际检验的测量风险。</p></div>
          <div className="rubricTable attackTable" role="table"><div className="rubricTableRow head"><span>攻击</span><span>为什么成立</span><span>预注册防守</span></div>{attackRows.map(r=><div className="rubricTableRow" key={r[0]}>{r.map(x=><span key={x}>{x}</span>)}</div>)}</div>
        </div>
      </section>

      <section className="rubricSection shell">
        <div className="sectionHead"><h2>今晚请导师拍板的可行性问题</h2><p>这些问题决定第 1–3 周能否冻结数据和主 rubric。</p></div>
        <div className="advisorChecks"><article><b>1 · 模板粒度</b><p>六层路由是否足够覆盖主矩阵，又不会造成每个 case 都独立写 rubric？</p></article><article><b>2 · 真值成本</b><p>48 个 user-task 的 must-change 是否能由目标用户确认，must-hold/FR 是否能由专家稳定标注？</p></article><article><b>3 · 识别强度</b><p>人类 reference matched 是否能稳定胜过 swapped，同时 must-hold 和隐私不下降？</p></article><article><b>4 · 两月范围</b><p>先冻结 report/memo/table 三类主交付物，code/slides/web 只进 anchor，是否更稳妥？</p></article></div>
        <div className="schemaDownloads"><b>机器可读材料</b><a href="/data_factory.protocol.yaml" download>data factory</a><a href="/rubric_module_library.yaml" download>36-module library</a><a href="/case.schema.yaml" download>case schema</a><a href="/rubric_template_registry.yaml" download>template registry</a><a href="/rubric_leaf.schema.yaml" download>leaf schema</a><a href="/metric_binding.schema.yaml" download>metric binding</a><a href="/rubric_bundle.example.yaml" download>端到端 example bundle</a></div>
      </section>

      <footer><div className="shell"><a className="brand" href="/">DeepAlign<span>Bench</span></a><p>Rubric Compiler 工作台 · v0.30</p></div></footer>
    </main>
  );
}
