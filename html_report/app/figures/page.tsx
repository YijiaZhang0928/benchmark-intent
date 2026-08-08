import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "论文图表蓝图｜DeepAlign-Bench",
  description: "DeepAlign-Bench 详细端到端流程、主文五张图、四张表与附录图表的结构规划",
};

const figures = [
  {
    id: "F1",
    title: "Benchmark 总览",
    question: "整套 benchmark 如何从用户信号走到可审计的结论？",
    placement: "Introduction 末尾 · 双栏通栏",
    panels: ["Gap: artifact fit ≠ downstream utility", "Phase A qualification", "Phase B randomized decision trial", "DDE + wrong-user harm", "Scope + claim boundary"],
    rule: "主图只保留两阶段因果链、真实用户和可验证终点；Atlas、stress 与 JudgeBench 进入支线，不与 DDE 竞争主贡献。",
  },
  {
    id: "F2",
    title: "Decision family、报告处理与 utility 构造",
    question: "persona、等价任务、三臂报告和可验证决定如何连接？",
    placement: "Method · 双栏通栏",
    panels: ["A · Utility + equivalent task shells", "B · task-only / matched / swapped reports", "C · Phase A common-quality + manipulation gates", "D · blocked randomization → regret / constraints / calibration"],
    rule: "必须用一个完整 case 展示 utility 在报告生成前如何冻结、persona 为什么不会泄漏答案、三臂如何配平，以及决定如何被 verifier 复核。",
  },
  {
    id: "F3",
    title: "Downstream Decision Effect 主结果",
    question: "哪些报告管线在什么用户和任务上真正降低了 decision regret？",
    placement: "Results 开头 · 双栏通栏",
    panels: ["A · DDE + family-clustered CI", "B · WrongUserHarm + hard constraints", "C · user / family heterogeneity", "D · calibration + burden"],
    rule: "DDE 是主终点；PF/CFA 仅作 manipulation check 或 mediator。按 target-user 与 family 聚类报告不确定性，不给单一总冠军。",
  },
  {
    id: "F4",
    title: "代理效度、异质性与失败模式",
    question: "artifact fit 何时预测、何时不能预测真实用户决策？",
    placement: "Results / Failure Analysis · 双栏通栏",
    panels: ["A · CFA → DDE association", "B · CFA-high / DDE-zero falsification cells", "C · utility / task-shell / treatment failures", "D · user × family heterogeneity"],
    rule: "明确把 CFA 高而 DDE≈0 当作代理失效，不把它解释成 benchmark 失败；机制结论只在预注册中介和足够功效下报告。",
  },
  {
    id: "F5",
    title: "Decision verifier、人类终点与测量审计",
    question: "utility、决定、置信度和报告资格是否被可靠记录？",
    placement: "Human Validity · 双栏通栏",
    panels: ["A · deterministic outcome verification", "B · decision / confidence capture", "C · report-quality judge–human agreement", "D · missingness / exclusion / burden audit"],
    rule: "主要结论优先依赖可验证环境结果和真人选择；JudgeBench 只审计 Phase A，未过门槛就阻止报告进入 Phase B。",
  },
];

const tables = [
  ["T1", "相关工作定位", "PDR-Bench、TARS、MyScholarQA、Lost in Simulation、DeepAlign", "artifact fit、真人任务结果、真实用户、模拟器风险、随机化 decision endpoint"],
  ["T2", "试验与覆盖", "decision family、utility、task shell、participant、report pipeline", "eligible / randomized / completed / excluded 数与原因"],
  ["T3", "主结果", "每行一个可比的 report pipeline × family", "DDE、WrongUserHarm、constraint violation、calibration、burden、clustered CI"],
  ["T4", "Phase A 与代理效度", "task-only、matched、swapped 及质量门", "TQ、FR、PF/CFA、DDE 关联、CFA-high/DDE-zero 单元与解释"],
];

export default function FigureBlueprintPage() {
  return (
    <main className="figurePlanPage" id="figure-top">
      <header className="figurePlanHero">
        <nav className="litNav shell"><Link className="brand" href="/">DeepAlign<span>Bench</span></Link><div><a href="#workflow-detail">详细流程</a><a href="#result-mockups">结果图原型</a><a href="#main-figures">全部主图</a><a href="#main-tables">主表</a></div><Link className="navCta" href="/">返回总报告</Link></nav>
        <div className="shell figurePlanHeroGrid">
          <section><p className="eyebrow">RESULT VISUAL BLUEPRINT · v0.32</p><h1>结果不是“更像你”，<br/>而是 <em>决定—伤害—代理效度</em></h1><p className="lede">核心展示 matched 相对 task-only 的 DDE、swapped 相对 task-only 的 wrong-user harm，以及硬约束和置信度；PF/CFA 只解释报告处理与代理效度。下方所有点和色块都是结构示意，不是假定实验结果。</p></section>
          <aside className="figurePlanClaim"><span>主文证据顺序</span><b>How it works</b><i>→</i><b>What is measured</b><i>→</i><b>Where it fails</b><i>→</i><b>Can we trust the score</b></aside>
        </div>
      </header>

      <section className="figurePlanSummary shell">
        <article><b>5</b><span>主图</span><p>2 张方法图 + 2 张结果图 + 1 张测量效度图</p></article>
        <article><b>4</b><span>主表</span><p>定位、覆盖、数值主榜与关键消融</p></article>
        <article><b>4–6</b><span>附录图</span><p>逐 family、逐 anchor、longitudinal 与群体切片</p></article>
        <article><b>8–10</b><span>附录表</span><p>case、rubric、agent、成本与完整结果</p></article>
      </section>

      <section className="workflowFigureSection" id="workflow-detail"><div className="shell">
        <div className="sectionHead"><h2>Phase A 工程流程：从 task metadata 到合格报告</h2><p>两张旧工程图在 v0.32 中明确降级为 Artifact Qualification 说明：它们保留 task/persona 构造、环境分轨、交叉评价和 rubric compiler，但不能单独支持下游决策效用结论；完整 Phase B 因果链以一页主图和 downstream decision protocol 为准。</p></div>
        <figure className="workflowFigure"><a href="/DeepAlign-Bench_端到端流程图_v0.32.png"><img src="/DeepAlign-Bench_端到端流程图_v0.32.png" alt="DeepAlign-Bench 从真实任务、运行前冻结和三环境分工到交叉评分与四重成功门的端到端流程图"/></a><figcaption><span>2560 × 1440 · 16:9 · 参考式汇报版</span><span><a href="/DeepAlign-Bench_端到端流程图_v0.32.png">下载 PNG</a></span></figcaption></figure>
        <figure className="workflowFigure"><a href="/DeepAlign-Bench_详细流程图.png"><img src="/DeepAlign-Bench_详细流程图.png" alt="DeepAlign-Bench 从真实任务、task metadata 和 case metadata 到反事实个性化结论的工程详细流程图"/></a><figcaption><span>2560 × 1440 · 16:9 · 工程详细版</span><span><a href="/DeepAlign-Bench_详细流程图.png">下载 PNG</a><a href="/DeepAlign-Bench_详细流程图.svg">下载可编辑 SVG</a></span></figcaption></figure>
      </div></section>

      <section className="resultMockSection" id="result-mockups"><div className="shell">
        <div className="sectionHead"><h2>真正跑完 benchmark 后，主结果建议长这样</h2><p>Figure 3 回答“有没有、在哪里”；Figure 4 回答“怎么坏、在哪坏”；Figure 5 只回答这些分数能不能信。</p></div>

        <article className="resultMockCard signatureCard">
          <header><span>RESULT FIGURE 3</span><div><h3>Downstream decision utility</h3><p>这是主结果页，不先排冠军，而先展示 matched 是否降低 regret、swapped 是否造成 wrong-user harm。</p></div><b>主文约 0.55 页</b></header>
          <div className="resultPanelGrid mainResultGrid">
            <section className="plotPanel signaturePanel"><h4>A · DDE × wrong-user harm profile</h4><div className="signaturePlot" role="img" aria-label="DDE 横轴、wrong-user harm 纵轴的结果结构示意图"><span className="sigY">Wrong-user harm ↑</span><span className="sigX">Decision benefit (DDE) →</span><i className="sigDiagonal"/><i className="sigDot sd1"><small>A</small></i><i className="sigDot sd2"><small>B</small></i><i className="sigDot sd3 hollow"><small>C</small></i><span className="sigGeneric">看似适配<br/>但无净受益</span><span className="sigStrong">真实受益<br/>且错配有害</span></div><p>右侧代表 matched 降低 regret；空心点表示共同质量、硬约束、功效或预注册门未通过。</p></section>
            <section className="plotPanel forestPanel"><h4>B · Family-level DDE forest</h4><div className="zeroTag">0 · no effect</div><div className="forestAxis"/><div className="forestRows"><div><b>Pipeline A</b><span className="ci ci1"><i/></span></div><div><b>Pipeline B</b><span className="ci ci2"><i/></span></div><div><b>Pipeline C</b><span className="ci ci3"><i/></span></div><div><b>Pooled trial</b><span className="ci ci4"><i/></span></div></div><p>每一行给 DDE、target-user/family-clustered 95% CI、硬约束违规和 eligibility；不同 decision environment 不混排。</p></section>
            <section className="plotPanel taskTopology"><h4>C · Statistically supported capability margins</h4><div className="marginalHeatGroups"><div className="marginalHeatBlock"><b>Agent × task stratum</b><div className="marginalHead"><span/><em>Daily</em><em>Professional</em><em>Frontier</em></div>{["A", "B", "C", "D"].map((agent,r)=><div className="marginalRow strataRow" key={agent}><span>{agent}</span>{[0,1,2].map(c=><i className={`heat h${(r+c)%5}`} key={c}/>)}</div>)}</div><div className="marginalHeatBlock intentsBlock"><b>Agent × research intent</b><div className="marginalHead intentHead"><span/>{["解释", "比较", "决策", "设计", "审计", "探索"].map(x=><em key={x}>{x}</em>)}</div>{["A", "B", "C", "D"].map((agent,r)=><div className="marginalRow intentRow" key={agent}><span>{agent}</span>{[0,1,2,3,4,5].map(c=><i className={`heat h${(r*2+c)%5}`} key={c}/>)}</div>)}</div></div><p>主文分别汇总 3 个 strata 和 6 个 intents，并报告 family 数；完整 18 个交叉格因接近一格一个 family，只在附录作描述性展示。</p></section>
            <section className="plotPanel paretoPanel"><h4>D · Burden–DDE frontier</h4><div className="paretoPlot"><span>高 DDE ↑</span><i className="paretoDot pd1"/><i className="paretoDot pd2"/><i className="paretoDot pd3"/><i className="paretoDot pd4"/><b>time / burden →</b><svg viewBox="0 0 100 70" preserveAspectRatio="none" aria-hidden="true"><path d="M15 58 C35 52, 47 35, 84 14"/></svg></div><p>只在相同 decision family、utility、报告预算和 eligibility 下谈效率前沿。</p></section>
          </div>
        </article>

        <article className="resultMockCard stressCard">
          <header><span>RESULT FIGURE 4</span><div><h3>Proxy validity and outcome failures</h3><p>第二张结果图检验 PF/CFA 何时能够、何时不能代理真实用户的决策结果。</p></div><b>主文约 0.5 页</b></header>
          <div className="resultPanelGrid stressResultGrid">
            <section className="plotPanel signalMatrix"><h4>A · Eligible signal-condition robustness</h4><div className="signalGroupHead"><span/><b>equivalent provided views</b><b>interactive</b><b>private env.</b><b>equivalence summary</b></div><div className="signalHead"><span/><b>Persona</b><b>History</b><b>Clarify</b><b>Workspace</b><b>Eq.Worst</b><b>Eq.Gap</b></div>{["Agent A", "Agent B", "Agent C", "Agent D"].map((agent,r)=><div className="signalRow" key={agent}><span>{agent}</span>{[0,1,2,3,4,5].map(c=><i className={`heat h${(r*2+c)%5}`} key={c}/>)}</div>)}<p>Cue Gap 与 Worst-view CFA 都只比较通过 equivalence audit 的 persona ↔ history；clarification 与 workspace 分列报告，不冒充语义等价。</p></section>
            <section className="plotPanel stressCurves"><h4>B · S0–S3 stress response</h4><svg viewBox="0 0 300 145" role="img" aria-label="S0 到 S3 的 CFA stress response 曲线结构示意"><path className="axis" d="M34 12V118H282"/><path className="curve c1" d="M40 25 C105 28,155 45,275 61"/><path className="curve c2" d="M40 28 C98 38,170 69,275 96"/><path className="curve c3" d="M40 31 C105 52,190 78,275 112"/><g>{[40,118,196,275].map((x,i)=><text x={x} y="137" key={x}>S{i}</text>)}</g><text x="4" y="18">1.0</text><text x="4" y="118">0</text></svg><p>仅当 CFA_S0≥ε 才画比例 retention；否则画 ΔCFA 和原始 CFA，避免接近零的分母制造夸张跌幅。</p></section>
            <section className="plotPanel failureBars"><h4>C · Multi-label failure incidence</h4><div className="failureDotPlot">{["用户盲", "错误用户绑定", "过度个性化", "共同核心破坏", "冲突/过期误用", "隐私/权限", "澄清失败"].map((mode,m)=><div className="failureDotRow" key={mode}><b>{mode}</b><span>{[0,1,2,3].map(a=><i className={`agentFailureDot afd${a}`} style={{left:`${10+((m*13+a*19)%78)}%`}} key={a}/>)}</span></div>)}</div><div className="agentDotLegend"><i className="afd0"/>A<i className="afd1"/>B<i className="afd2"/>C<i className="afd3"/>D</div><p>每个点是全部 eligible episode 中该 failure 的发生率与 95% CI；类别可共现，因此不做互斥堆叠。共现结构放附录 UpSet 图。</p></section>
            <section className="plotPanel anchorFailure"><h4>D · Anchor × observed outcome failure</h4><div className="anchorFailGrid">{["A1 日常", "A2 学习", "A3 金融", "A4 健康", "A5 企业", "A6 软件", "A7 学术", "A8 政策"].map((a,r)=><div key={a}><b>{a}</b>{[0,1,2,3,4,5,6].map(c=><i className={`heat h${(r+c*2)%5}`} key={c}/>)}</div>)}</div><p>列是可观察的 outcome failure。过程级 acquisition/preservation/use/update 只在 trace 可比时进附录。</p></section>
          </div>
        </article>

        <aside className="judgeResultBoundary"><span>RESULT FIGURE 5 · MEASUREMENT VALIDITY</span><div><h3>JudgeBench 只审计 Phase A</h3><p>真人决定与可验证环境终态承担主结果；JudgeBench 只验证报告资格评分的 agreement、calibration、nuisance bias 与 escalation。Judge 未过门槛，相关报告不得进入 Phase B。</p></div><div className="judgeMiniPanels"><b>agreement</b><b>calibration</b><b>bias Δ</b><b>coverage / cost / error</b></div></aside>
      </div></section>

      <section className="figurePlanFigures" id="main-figures">
        <div className="shell"><div className="sectionHead"><h2>五张主图：每张只回答一个一级问题</h2><p>图中结构是预注册模板，不预设任何 agent 的胜负或曲线方向。</p></div>
          <div className="figureBlueprintList">
            {figures.map((figure, index) => <article className="figureBlueprint" key={figure.id}>
              <header><span>{figure.id}</span><div><h3>{figure.title}</h3><p>{figure.question}</p></div><small>{figure.placement}</small></header>
              {index === 0 ? <div className="miniPipeline">{figure.panels.map((panel, i) => <span key={panel}><b>{i + 1}</b>{panel}{i < figure.panels.length - 1 && <i>→</i>}</span>)}</div> :
                <div className="miniPanels">{figure.panels.map((panel) => <div key={panel}><b>{panel.split(" · ")[0]}</b><span>{panel.split(" · ")[1]}</span></div>)}</div>}
              <p className="figureRule"><b>结构规则</b>{figure.rule}</p>
            </article>)}
          </div>
        </div>
      </section>

      <section className="figurePlanTables" id="main-tables"><div className="shell"><div className="sectionHead light"><h2>四张主表：负责精确数字和覆盖边界</h2><p>图负责看模式，表负责复核数值；不要在图表之间重复同一组结果。</p></div>
        <div className="tableBlueprintWrap"><table className="tableBlueprint"><thead><tr><th>编号</th><th>作用</th><th>行</th><th>列</th></tr></thead><tbody>{tables.map(row => <tr key={row[0]}>{row.map(cell => <td key={cell}>{cell}</td>)}</tr>)}</tbody></table></div>
      </div></section>

      <section className="figurePlanAppendix shell" id="appendix-plan"><div className="sectionHead"><h2>附录承担“完整”，主文承担“可读”</h2><p>任何主文总体结论都应能在附录找到 family、anchor、运行版本和人评证据。</p></div>
        <div className="appendixGrid"><article><span>APPENDIX FIGURES</span><h3>建议 4–6 张</h3><ul><li>逐 family DDE / harm forest plot</li><li>招募、随机化与缺失流程图</li><li>PF/CFA → DDE 代理效度图</li><li>顺序与 task-shell 平衡检查</li><li>constraint / calibration 切片</li><li>用户群和 pipeline 异质性</li></ul></article><article><span>APPENDIX TABLES</span><h3>建议 8–10 张</h3><ul><li>8–12 family 与 utility 清单</li><li>persona / task-shell compatibility gate</li><li>完整 Phase A rubric leaf bank</li><li>pipeline / version / tool metadata</li><li>全量结果与聚类置信区间</li><li>排除、成本、负担与伦理记录</li></ul></article></div>
        <div className="figurePlanNo"><b>明确不建议</b><span>单一总体排名</span><span>雷达图</span><span>3D 图</span><span>无 CI 柱状榜</span><span>sunburst 冒充覆盖</span><span>expected/observed 混标</span></div>
      </section>
      <footer><div className="shell"><a className="brand" href="#figure-top">DeepAlign<span>Bench</span></a><p>Result visual blueprint · v0.32 · 2026-08-09</p><Link href="/">返回完整汇报版 ↑</Link></div></footer>
    </main>
  );
}
