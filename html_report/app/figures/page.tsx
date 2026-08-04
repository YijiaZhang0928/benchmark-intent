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
    panels: ["A · Ua/Ub invariant core + minimal edits", "B · Persona / history / clarification views", "C · 2×2 M[i,j] 交叉评分矩阵", "D · must-change / hold / not / clarify"],
    rule: "必须使用一个完整真实 case。它是论文方法最关键的细节图，不能只画抽象流程。",
  },
  {
    id: "F3",
    title: "主能力与 Leaderboard profile",
    question: "哪些 agent 在哪些任务上产生了用户特异价值？",
    placement: "Results 开头 · 双栏通栏",
    panels: ["A · CFA forest plot + 95% CI + TQ/FR gate", "B · Agent × research intent heatmap", "C · Agent × task stratum heatmap", "D · Cost–CFA Pareto scatter"],
    rule: "不画雷达图，不给单一总冠军；商业产品、受控 harness 和开源 DRA 按 execution regime 分块。",
  },
  {
    id: "F4",
    title: "渠道稳健性、压力与失败模式",
    question: "能力在什么用户信息来源和压力下断裂，具体错在哪里？",
    placement: "Results / Failure Analysis · 双栏通栏",
    panels: ["A · Worst-view CFA + Cue Gap", "B · S0–S3 dose-response curves", "C · Result risk × observed failure heatmap", "D · TQ / FR / MP / privacy collateral damage"],
    rule: "expected failure 与 observed failure 分开；保留 other/emergent。逐 anchor 曲线移到附录，主文显示汇总与最差切片。",
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
  ["T3", "主 Leaderboard 数值", "每行一个可比的 agent × execution regime", "TQ、FR、PF、MP、CFA、Worst-view CFA、Neutral Invariance、cost、eligibility、CI"],
  ["T4", "对照与替代解释", "task-only、matched、history、clarification、irrelevant cue、swap、无 contracts、长度/风格对照", "ΔCFA、specificity P/R、invariance、TQ/FR、judge coverage 与解释"],
];

export default function FigureBlueprintPage() {
  return (
    <main className="figurePlanPage" id="figure-top">
      <header className="figurePlanHero">
        <nav className="litNav shell"><a className="brand" href="/">DeepAlign<span>Bench</span></a><div><a href="#main-figures">五张主图</a><a href="#main-tables">四张主表</a><a href="#appendix-plan">附录</a></div><a className="navCta" href="/">返回总报告</a></nav>
        <div className="shell figurePlanHeroGrid">
          <section><p className="eyebrow">PAPER VISUAL BLUEPRINT · v0.25</p><h1>主文用 <em>5 张图 + 4 张表</em><br/>讲完一条证据链</h1><p className="lede">先解释 benchmark 和 estimand，再给主能力、压力失败和 judge 有效性证据。Atlas 的宏大范围放在元数据与 coverage 表里，不靠一张拥挤的“大而全”主图证明。</p></section>
          <aside className="figurePlanClaim"><span>主文证据顺序</span><b>How it works</b><i>→</i><b>What is measured</b><i>→</i><b>Where it fails</b><i>→</i><b>Can we trust the score</b></aside>
        </div>
      </header>

      <section className="figurePlanSummary shell">
        <article><b>5</b><span>主图</span><p>2 张方法图 + 2 张结果图 + 1 张测量效度图</p></article>
        <article><b>4</b><span>主表</span><p>定位、覆盖、数值主榜与关键消融</p></article>
        <article><b>4–6</b><span>附录图</span><p>逐 family、逐 anchor、longitudinal 与群体切片</p></article>
        <article><b>8–10</b><span>附录表</span><p>case、rubric、agent、成本与完整结果</p></article>
      </section>

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
      <footer><div className="shell"><a className="brand" href="#figure-top">DeepAlign<span>Bench</span></a><p>Paper visual blueprint · v0.25 · 2026-08-04</p><a href="/">返回完整汇报版 ↑</a></div></footer>
    </main>
  );
}
