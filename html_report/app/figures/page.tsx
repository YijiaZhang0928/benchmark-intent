import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "论文图表蓝图｜DeepAlign-Bench",
  description: "DeepAlign-Bench 主文五张图、四张表与附录图表的结构规划",
};

const figures = [
  {
    id: "F1",
    title: "Benchmark 总览",
    question: "整套 benchmark 如何从用户信号走到可审计的结论？",
    placement: "Introduction 末尾 · 双栏通栏",
    panels: ["Task + evidence + paired user state", "Signal view + environment", "Agent system", "Matched / swapped artifacts", "Gate + CFA + profiles"],
    rule: "顶部放 Atlas 条件带；底部只放 S0–S3 stress 与 JudgeBench 两条验证支线。不要把 taxonomy 全部塞进主图。",
  },
  {
    id: "F2",
    title: "Counterfactual family 构造与评分",
    question: "persona、真值、输出变化和 CFA 到底如何连接？",
    placement: "Method · 双栏通栏",
    panels: ["A · Ua/Ub invariant core + minimal edits", "B · Persona / history / clarification views", "C · Template routing → leaf expansion → metric binding", "D · 2×2 M[i,j] + CFA / invariance / gates"],
    rule: "必须用一个完整 case 展示复合 contract 如何拆成带锚点 leaf，以及同一用户 leaves 如何同时评分 matched/swapped；不能只画抽象流程。",
  },
  {
    id: "F3",
    title: "主能力与 Leaderboard profile",
    question: "哪些 agent 在哪些任务上产生了用户特异价值？",
    placement: "Results 开头 · 双栏通栏",
    panels: ["A · PF swapped × PF matched signature plot", "B · CFA forest plot + 95% CI + gates", "C · Agent × strata / intents marginal heatmaps", "D · Cost–CFA Pareto scatter"],
    rule: "A 解释 estimand，B 给不确定性，C 显示能力拓扑，D 报告效率。不画雷达图，不给单一总冠军；不同 execution regime 分块。",
  },
  {
    id: "F4",
    title: "渠道稳健性、压力与失败模式",
    question: "能力在什么用户信息来源和压力下断裂，具体错在哪里？",
    placement: "Results / Failure Analysis · 双栏通栏",
    panels: ["A · Agent × eligible signal-condition CFA", "B · S0–S3 stress response curves", "C · Multi-label failure incidence + 95% CI", "D · Anchor × observed outcome-failure heatmap"],
    rule: "Cue Gap 只比较 equivalence-audited views；failure 按多标签 incidence 独立报告。过程机制只有在 trace 可比时进入附录。",
  },
  {
    id: "F5",
    title: "JudgeBench 与人类校准",
    question: "自动 judge 是否真的在测用户价值，而不是长度、位置或关键词？",
    placement: "Human Validity · 双栏通栏",
    panels: ["A · Judge–human agreement by rubric module", "B · Reliability / calibration curve", "C · Order / length / format / keyword bias deltas", "D · Coverage–cost–error cascade"],
    rule: "预注册门槛直接画在图上。若未过门槛，这张图应支持降级为人评，而不是隐藏测量失败。",
  },
];

const tables = [
  ["T1", "相关工作定位", "PDR-Bench、ResearchRubrics、DR Bench、PersonaTrail/APeB、PASB、DeepAlign", "absolute fit、cross-user counterfactual、contracts、multi-cue、longitudinal、human/judge validity"],
  ["T2", "数据与实测覆盖", "task stratum、intent、deliverable、signal、environment、agent、anchor、stakes", "family/episode/user-pair 数与 tested / defined-only / inapplicable / deferred"],
  ["T3", "主 Leaderboard 数值", "每行一个可比的 agent × execution regime", "TQ、FR、PF matched/swapped、MP、CFA、Worst-view CFA、Neutral Invariance、cost、eligibility、CI"],
  ["T4", "对照与替代解释", "task-only、matched、history、clarification、irrelevant cue、swap、无 contracts、长度/风格对照", "ΔCFA、specificity P/R、invariance、TQ/FR、judge coverage 与解释"],
];

export default function FigureBlueprintPage() {
  return (
    <main className="figurePlanPage" id="figure-top">
      <header className="figurePlanHero">
        <nav className="litNav shell"><a className="brand" href="/">DeepAlign<span>Bench</span></a><div><a href="#result-mockups">结果图原型</a><a href="#main-figures">全部主图</a><a href="#main-tables">主表</a></div><a className="navCta" href="/">返回总报告</a></nav>
        <div className="shell figurePlanHeroGrid">
          <section><p className="eyebrow">RESULT VISUAL BLUEPRINT · v0.28</p><h1>结果不是一张总榜，<br/>而是 <em>效应—分布—失效</em></h1><p className="lede">核心先展示 matched 相对 swapped 是否真的形成用户特异价值，再展开到可支持的任务边际、信号稳健性和多标签失败。下方所有点和色块都是结构示意，不是假定实验结果。</p></section>
          <aside className="figurePlanClaim"><span>主文证据顺序</span><b>How it works</b><i>→</i><b>What is measured</b><i>→</i><b>Where it fails</b><i>→</i><b>Can we trust the score</b></aside>
        </div>
      </header>

      <section className="figurePlanSummary shell">
        <article><b>5</b><span>主图</span><p>2 张方法图 + 2 张结果图 + 1 张测量效度图</p></article>
        <article><b>4</b><span>主表</span><p>定位、覆盖、数值主榜与关键消融</p></article>
        <article><b>4–6</b><span>附录图</span><p>逐 family、逐 anchor、longitudinal 与群体切片</p></article>
        <article><b>8–10</b><span>附录表</span><p>case、rubric、agent、成本与完整结果</p></article>
      </section>

      <section className="resultMockSection" id="result-mockups"><div className="shell">
        <div className="sectionHead"><h2>真正跑完 benchmark 后，主结果建议长这样</h2><p>Figure 3 回答“有没有、在哪里”；Figure 4 回答“怎么坏、在哪坏”；Figure 5 只回答这些分数能不能信。</p></div>

        <article className="resultMockCard signatureCard">
          <header><span>RESULT FIGURE 3</span><div><h3>Counterfactual personalization capability</h3><p>这是主结果页，不先排冠军，而先让读者看到 matched 与 swapped 的结构差异。</p></div><b>主文约 0.55 页</b></header>
          <div className="resultPanelGrid mainResultGrid">
            <section className="plotPanel signaturePanel"><h4>A · Matched–swapped signature plot</h4><div className="signaturePlot" role="img" aria-label="PF swapped 横轴、PF matched 纵轴的结果结构示意图"><span className="sigY">PF matched ↑</span><span className="sigX">PF swapped →</span><i className="sigDiagonal"/><i className="sigDot sd1"><small>A</small></i><i className="sigDot sd2"><small>B</small></i><i className="sigDot sd3 hollow"><small>C</small></i><span className="sigGeneric">高 absolute fit<br/>低 user-specific effect</span><span className="sigStrong">强 counterfactual<br/>personalization</span></div><p>45° 线是 CFA≈0。位于线上方且距离更远才表示 matched 版本更适合正确用户；空心点表示未过 TQ/FR gate。</p></section>
            <section className="plotPanel forestPanel"><h4>B · CFA effect-size forest</h4><div className="zeroTag">0 · no effect</div><div className="forestAxis"/><div className="forestRows"><div><b>Commercial DR</b><span className="ci ci1"><i/></span></div><div><b>Controlled agent</b><span className="ci ci2"><i/></span></div><div><b>Open DRA</b><span className="ci ci3"><i/></span></div><div><b>Multi-agent probe</b><span className="ci ci4"><i/></span></div></div><p>每一行给 CFA 点估计、95% CI、样本量和 eligibility；E1/E2/E3 不混排。</p></section>
            <section className="plotPanel taskTopology"><h4>C · Statistically supported capability margins</h4><div className="marginalHeatGroups"><div className="marginalHeatBlock"><b>Agent × task stratum</b><div className="marginalHead"><span/><em>Daily</em><em>Professional</em><em>Frontier</em></div>{["A", "B", "C", "D"].map((agent,r)=><div className="marginalRow strataRow" key={agent}><span>{agent}</span>{[0,1,2].map(c=><i className={`heat h${(r+c)%5}`} key={c}/>)}</div>)}</div><div className="marginalHeatBlock intentsBlock"><b>Agent × research intent</b><div className="marginalHead intentHead"><span/>{["解释", "比较", "决策", "设计", "审计", "探索"].map(x=><em key={x}>{x}</em>)}</div>{["A", "B", "C", "D"].map((agent,r)=><div className="marginalRow intentRow" key={agent}><span>{agent}</span>{[0,1,2,3,4,5].map(c=><i className={`heat h${(r*2+c)%5}`} key={c}/>)}</div>)}</div></div><p>主文分别汇总 3 个 strata 和 6 个 intents，并报告 family 数；完整 18 个交叉格因接近一格一个 family，只在附录作描述性展示。</p></section>
            <section className="plotPanel paretoPanel"><h4>D · Cost–CFA frontier</h4><div className="paretoPlot"><span>高 CFA ↑</span><i className="paretoDot pd1"/><i className="paretoDot pd2"/><i className="paretoDot pd3"/><i className="paretoDot pd4"/><b>cost →</b><svg viewBox="0 0 100 70" preserveAspectRatio="none" aria-hidden="true"><path d="M15 58 C35 52, 47 35, 84 14"/></svg></div><p>只在相同 execution regime、预算口径和 eligibility 下谈 Pareto 前沿。</p></section>
          </div>
        </article>

        <article className="resultMockCard stressCard">
          <header><span>RESULT FIGURE 4</span><div><h3>Signal robustness and outcome failures</h3><p>第二张结果图不再重复总体排名，而是定位能力在哪类输入和压力下断裂。</p></div><b>主文约 0.5 页</b></header>
          <div className="resultPanelGrid stressResultGrid">
            <section className="plotPanel signalMatrix"><h4>A · Eligible signal-condition robustness</h4><div className="signalGroupHead"><span/><b>equivalent provided views</b><b>interactive</b><b>private env.</b><b>equivalence summary</b></div><div className="signalHead"><span/><b>Persona</b><b>History</b><b>Clarify</b><b>Workspace</b><b>Eq.Worst</b><b>Eq.Gap</b></div>{["Agent A", "Agent B", "Agent C", "Agent D"].map((agent,r)=><div className="signalRow" key={agent}><span>{agent}</span>{[0,1,2,3,4,5].map(c=><i className={`heat h${(r*2+c)%5}`} key={c}/>)}</div>)}<p>Cue Gap 与 Worst-view CFA 都只比较通过 equivalence audit 的 persona ↔ history；clarification 与 workspace 分列报告，不冒充语义等价。</p></section>
            <section className="plotPanel stressCurves"><h4>B · S0–S3 stress response</h4><svg viewBox="0 0 300 145" role="img" aria-label="S0 到 S3 的 CFA stress response 曲线结构示意"><path className="axis" d="M34 12V118H282"/><path className="curve c1" d="M40 25 C105 28,155 45,275 61"/><path className="curve c2" d="M40 28 C98 38,170 69,275 96"/><path className="curve c3" d="M40 31 C105 52,190 78,275 112"/><g>{[40,118,196,275].map((x,i)=><text x={x} y="137" key={x}>S{i}</text>)}</g><text x="4" y="18">1.0</text><text x="4" y="118">0</text></svg><p>仅当 CFA_S0≥ε 才画比例 retention；否则画 ΔCFA 和原始 CFA，避免接近零的分母制造夸张跌幅。</p></section>
            <section className="plotPanel failureBars"><h4>C · Multi-label failure incidence</h4><div className="failureDotPlot">{["用户盲", "错误用户绑定", "过度个性化", "共同核心破坏", "冲突/过期误用", "隐私/权限", "澄清失败"].map((mode,m)=><div className="failureDotRow" key={mode}><b>{mode}</b><span>{[0,1,2,3].map(a=><i className={`agentFailureDot afd${a}`} style={{left:`${10+((m*13+a*19)%78)}%`}} key={a}/>)}</span></div>)}</div><div className="agentDotLegend"><i className="afd0"/>A<i className="afd1"/>B<i className="afd2"/>C<i className="afd3"/>D</div><p>每个点是全部 eligible episode 中该 failure 的发生率与 95% CI；类别可共现，因此不做互斥堆叠。共现结构放附录 UpSet 图。</p></section>
            <section className="plotPanel anchorFailure"><h4>D · Anchor × observed outcome failure</h4><div className="anchorFailGrid">{["A1 日常", "A2 学习", "A3 金融", "A4 健康", "A5 企业", "A6 软件", "A7 学术", "A8 政策"].map((a,r)=><div key={a}><b>{a}</b>{[0,1,2,3,4,5,6].map(c=><i className={`heat h${(r+c*2)%5}`} key={c}/>)}</div>)}</div><p>列是可观察的 outcome failure。过程级 acquisition/preservation/use/update 只在 trace 可比时进附录。</p></section>
          </div>
        </article>

        <aside className="judgeResultBoundary"><span>RESULT FIGURE 5 · MEASUREMENT VALIDITY</span><div><h3>JudgeBench 不是第三张模型能力榜</h3><p>它只验证 Figure 3–4 的自动评分是否可用：rubric-module agreement、calibration、nuisance bias 与 human-escalation curve。Judge 未过门槛，主结果必须切换到人评覆盖。</p></div><div className="judgeMiniPanels"><b>agreement</b><b>calibration</b><b>bias Δ</b><b>coverage / cost / error</b></div></aside>
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
        <div className="appendixGrid"><article><span>APPENDIX FIGURES</span><h3>建议 4–6 张</h3><ul><li>逐 family CFA forest plot</li><li>完整 task-cube coverage heatmap</li><li>八个 anchor 的独立 S0–S3 曲线</li><li>clarification value / turn</li><li>retention 与 update 曲线</li><li>语言、用户群和 seed 切片</li></ul></article><article><span>APPENDIX TABLES</span><h3>建议 8–10 张</h3><ul><li>24 family 与 48 user-task 清单</li><li>persona compatibility gate</li><li>完整 rubric leaf bank</li><li>agent / version / tool metadata</li><li>全量结果与置信区间</li><li>成本、失败案例与人工一致性</li></ul></article></div>
        <div className="figurePlanNo"><b>明确不建议</b><span>单一总体排名</span><span>雷达图</span><span>3D 图</span><span>无 CI 柱状榜</span><span>sunburst 冒充覆盖</span><span>expected/observed 混标</span></div>
      </section>
      <footer><div className="shell"><a className="brand" href="#figure-top">DeepAlign<span>Bench</span></a><p>Result visual blueprint · v0.27 · 2026-08-04</p><a href="/">返回完整汇报版 ↑</a></div></footer>
    </main>
  );
}
