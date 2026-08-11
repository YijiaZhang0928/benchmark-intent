import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "ElicitAlign-Bench｜研究汇报",
  description: "评测 agent 在自然欠指定任务中自主发现、澄清并利用用户信息的能力",
};

const papers = [
  ["PDR-Bench", "给定 persona/context 后的个性化报告质量", "https://arxiv.org/abs/2509.25106"],
  ["IDRBench", "欠指定 Deep Research 中交互带来的收益与成本", "https://arxiv.org/abs/2601.06676"],
  ["IntentRL", "主动澄清潜在 intent 的训练方法", "https://arxiv.org/abs/2602.03468"],
  ["DiscoBench", "搜索过程中的歧义发现、提问与恢复", "https://arxiv.org/abs/2606.27669"],
  ["G-STEER", "个性化 Deep Research 的 Retrieve / Ask / Stop", "https://arxiv.org/abs/2608.05876"],
];

const conditions = [
  ["C0 Natural-Interactive", "不提供 persona，也不提醒个性化；允许 agent 自主提问", "自主发现与触发"],
  ["C1 Nudge-Interactive", "只提醒‘若缺少会改变答案的用户信息，可以先澄清’", "被提醒后的执行能力"],
  ["C2 No-Ask", "同一自然 instruction，但关闭用户通道", "不能澄清时的通用回答下限"],
  ["C3 Full-Persona Oracle", "直接提供完整、经用户确认的相关 user-state ledger", "信息全知时的可达上限"],
];

export default function Home() {
  return (
    <main>
      <header className="hero" id="top">
        <nav className="nav shell" aria-label="主导航">
          <a className="brand" href="#top">ElicitAlign<span>Bench</span></a>
          <div className="navlinks">
            <a href="#question">问题</a><a href="#design">设计</a><a href="#metrics">评分</a><a href="#novelty">边界</a><a href="#pilot">最小实验</a>
          </div>
          <a className="navCta" href="#editions">下载文档</a>
        </nav>
        <div className="heroGrid shell">
          <section>
            <p className="eyebrow">RESEARCH PROPOSAL · v0.45 · 2026-08-12</p>
            <h1>从缺失用户信息到<em>个性化最终交付</em></h1>
            <p className="lede">用户给出的任务足够让 agent 直接开始研究，却漏掉 1–3 个会改变最终建议的用户条件。我们测试 agent 会不会在没有提醒时自己发现缺口、问对问题、知道何时停止，并把答案真正用进长程 Deep Research 交付物。</p>
            <div className="heroActions">
              <a className="button primary" href="#design">看端到端框架</a>
              <a className="button ghost" href="/ElicitAlign-Bench_正式Proposal精简版.pdf" download>下载 6 页精简版</a>
            </div>
            <div className="heroMeta"><span>无显式 persona</span><span>主条件无澄清提醒</span><span>四条件能力分解</span><span>paired real-user family</span></div>
          </section>
          <aside className="thesisCard">
            <span className="cardKicker">一句话研究问题</span>
            <p>一个 agent 会使用完整 persona，不代表它会在真实、自然但不完整的任务输入中主动找出关键用户信息并正确利用。</p>
            <hr />
            <div className="thesisFlow"><b>发现</b><i>→</i><b>提问</b><i>→</i><b>停止</b><i>→</i><b>利用</b></div>
          </aside>
        </div>
      </header>

      <section className="decision shell" id="question">
        <p className="sectionTag">WHAT THE BENCHMARK CAN EXPLAIN</p>
        <div className="sectionHead"><h2>它不是再做一个“问题问得好不好”的榜单</h2><p>四个条件和逐节点轨迹把看似相同的低分拆成不同能力缺口。</p></div>
        <div className="decisionGrid">
          <article><span>01</span><h3>知道信息时会不会用</h3><p>Oracle 高、Natural 低，说明系统会个性化，但不会自主获取用户状态。</p></article>
          <article><span>02</span><h3>没提醒时会不会想到问</h3><p>Nudge 高、Natural 低，说明能力存在，但原生触发不足，依赖 prompt。</p></article>
          <article><span>03</span><h3>问到了是否真正改变交付</h3><p>asked/answered 高但 report/decision 低，说明长程执行中发生利用失败。</p></article>
        </div>
      </section>

      <section className="figureSection" id="design">
        <div className="shell">
          <div className="sectionHead light"><h2>一张图看懂 case、task、隐藏用户状态、四条件与评估</h2><p>主图同时给出数据构造、元数据、交互循环、Deep Research 执行、非补偿评分、系统诊断和论文生死门。</p></div>
          <figure><img src="/ElicitAlign-Bench_端到端流程图_v0.45.png" alt="ElicitAlign-Bench 从隐藏用户状态与自然欠指定输入到四条件实验和最终交付评估的端到端流程图" /><figcaption>正式 v0.45 端到端框架：完整 persona 只作为 oracle ceiling；Natural 才是主实验。</figcaption></figure>
        </div>
      </section>

      <section className="shell gapSection">
        <p className="sectionTag">FOUR-CONDITION DECOMPOSITION</p>
        <div className="sectionHead"><h2>为什么必须有四个条件</h2><p>如果只比较“能问”与“不能问”，无法知道失败来自没想到问、问得不好、停得不好，还是问到后没有用。</p></div>
        <div className="compare" role="table" aria-label="四个实验条件">
          <div className="compareRow head" role="row"><span>条件</span><span>Agent 看到什么</span><span>解释的能力</span></div>
          {conditions.map((r) => <div className="compareRow" role="row" key={r[0]}><b>{r[0]}</b><span>{r[1]}</span><span>{r[2]}</span></div>)}
        </div>
        <div className="winnerBanner"><span>主实验原则</span><b>Natural 不提醒；Nudge 只作诊断</b><p>若主条件直接要求“先考虑个性化并澄清”，测到的是提示遵从。任务也不能按“多数模型已经会问”筛选，否则主动提问强的模型会反过来定义数据分布。</p></div>
      </section>

      <section className="classificationSection" id="metrics">
        <div className="shell">
          <p className="sectionTag">NON-COMPENSATORY EVALUATION</p>
          <div className="sectionHead"><h2>不再让一个差值讲完整故事</h2><p>所有原始条件绝对分都必须报告；差值只解释能力来源，不能掩盖 Natural 本身不合格、共同质量下降或越界提问。</p></div>
          <div className="taxonomyRules">
            <article><b>需要识别</b><p>critical-missing 上是否问；sufficient 和 irrelevant-missing control 上是否不问。报告 sensitivity、specificity 与 macro-F1。</p></article>
            <article><b>精准获取与停止</b><p>Targeted Elicitation Recall、Question Precision、Information Gain per Turn、Stopping Sufficiency、用户负担与重复提问。</p></article>
            <article><b>最终交付绝对合格</b><p>先过 Absolute Adequacy，再看 must-change / must-hold / must-not、共同质量、事实可靠性和目标用户效用。</p></article>
            <article><b>逐节点利用链</b><p><code>unknown → asked → answered → represented_in_plan → evidenced_in_report → changed_decision</code>，单独识别“问到但没用”。</p></article>
          </div>
          <div className="formula">SelfInitiatedGain = U(Natural) − U(No-Ask)<br/>NudgeGap = U(Nudge) − U(Natural)<br/>OracleGap = U(Oracle) − U(Natural)</div>
          <div className="classificationVerdict"><b>归一化只作次级描述</b><p><code>OracleRecovery = (U(Natural) − U(No-Ask)) / (U(Oracle) − U(No-Ask))</code> 仅在分母超过预注册阈值时计算。主统计仍使用四个原始 arm 和 family-level paired effects，防止小分母制造夸张比例。</p></div>
        </div>
      </section>

      <section className="shell gapSection" id="novelty">
        <p className="sectionTag">NEAREST-NEIGHBOR PRESSURE</p>
        <div className="sectionHead"><h2>新意边界很窄，必须用结果而不是措辞证明</h2><p>IDRBench、IntentRL、DiscoBench 和 G-STEER 已覆盖交互、主动澄清、歧义恢复与个性化 Ask/Stop。最危险的审稿意见是：“这只是 G-STEER 的 benchmark 化。”</p></div>
        <div className="sourceGrid">
          {papers.map(([name, role, url]) => <a key={name} href={url} target="_blank" rel="noreferrer"><b>{name}</b><span>{role}</span></a>)}
        </div>
        <div className="compare" role="table" aria-label="最近邻与本研究边界">
          <div className="compareRow head" role="row"><span>维度</span><span>最近邻已经覆盖</span><span>ElicitAlign 必须额外证明</span></div>
          <div className="compareRow" role="row"><b>输入</b><span>persona/context、欠指定任务或专用澄清模块</span><span>无 profile、无提醒、仍可直接执行的自然任务</span></div>
          <div className="compareRow" role="row"><b>数据单位</b><span>query / session / target coverage</span><span>共享任务核心的 paired real-user family 与预冻结 decision contracts</span></div>
          <div className="compareRow" role="row"><b>终点</b><span>问题、覆盖率、交互收益或报告 P/Q</span><span>用户信息从回答到计划、报告和最终决策改变的完整利用链</span></div>
          <div className="compareRow" role="row"><b>负对照</b><span>常缺少“本来就不该问”的充分任务</span><span>sufficient 与 irrelevant-missing controls 同时约束过问和敏感越界</span></div>
        </div>
      </section>

      <section className="reviewBand" id="pilot">
        <div className="shell">
          <p className="sectionTag invert">NOVELTY-KILL PILOT</p>
          <div className="sectionHead light"><h2>先用三组任务杀死错误方向，再决定是否扩到 24 family</h2><p>最小实验不是证明论文成立，而是检查它能否产生已有指标解释不了的新排序、新失败和可接受成本。</p></div>
          <div className="decisionGrid">
            <article><span>01</span><h3>三类任务</h3><p>团队知识库采购、国际家庭旅行、研究工具选型；每个 family 两位用户、四类 case、四个条件、4–6 个系统。</p></article>
            <article><span>02</span><h3>继续门</h3><p>至少两个 family 出现有意义条件分离；至少一个系统发生 Natural/Oracle 排名变化或稳定利用失败；充分任务不过问。</p></article>
            <article><span>03</span><h3>停止或换题</h3><p>一句 Nudge 让所有系统接近 Oracle、G-STEER/IDRBench 指标完全预测排序、真人和模拟器结论相反，或差异只来自报告长度与预算。</p></article>
          </div>
        </div>
      </section>

      <section className="editionSection" id="editions">
        <div className="shell">
          <p className="sectionTag">READING EDITIONS</p>
          <div className="sectionHead"><h2>同一套 v0.45 方法，按讨论场景分成四版</h2><p>旧 DeepAlign-Bench 交付物已归档；当前入口只指向 ElicitAlign-Bench。</p></div>
          <div className="editionGrid">
            <article><span>FORMAL · 17 PAGES</span><h3>正式研究 Proposal</h3><p>完整研究问题、数据构造、交互协议、评分、统计、最近邻边界和八周计划。</p><div className="editionLinks"><a href="/ElicitAlign-Bench_正式研究Proposal.pdf" download>PDF</a><a href="/ElicitAlign-Bench_正式研究Proposal.docx" download>Word</a></div></article>
            <article className="recommended"><span>CONDENSED · 6 PAGES</span><h3>正式 Proposal 精简版</h3><p>适合导师快速判断研究缺口、实验逻辑、可行性与停止条件。</p><div className="editionLinks"><a href="/ElicitAlign-Bench_正式Proposal精简版.pdf" download>PDF</a><a href="/ElicitAlign-Bench_正式Proposal精简版.docx" download>Word</a></div></article>
            <article><span>PLAIN LANGUAGE · 8 PAGES</span><h3>完整人话版</h3><p>用直接语言解释为什么不提醒、为什么不能按模型行为筛题，以及分数应该怎么看。</p><div className="editionLinks"><a href="/ElicitAlign-Bench_完整人话版.pdf" download>PDF</a><a href="/ElicitAlign-Bench_完整人话版.docx" download>Word</a></div></article>
            <article><span>ADVISOR BRIEF · 6 PAGES</span><h3>汇报精简版</h3><p>15–20 分钟汇报结构，包含主图、最近邻压力、最小实验和八周决策。</p><div className="editionLinks"><a href="/ElicitAlign-Bench_汇报精简版.pdf" download>PDF</a><a href="/ElicitAlign-Bench_汇报精简版.docx" download>Word</a></div></article>
          </div>
          <div className="schemaDownloads"><a href="/elicitalign_case.schema.yaml" download>Case schema ↓</a><a href="/elicitalign_evaluation.protocol.yaml" download>Evaluation protocol ↓</a><a href="/ElicitAlign-Bench_端到端流程图_v0.45.svg" download>可编辑 SVG ↓</a><a href="/PROJECT_MEMORY.md" download>项目记忆 ↓</a></div>
        </div>
      </section>

      <footer className="closing"><div className="shell closingGrid"><div><p className="eyebrow">CLAIM BOUNDARY</p><h2>只主张可观察行为，不声称模型“真正关心用户”</h2></div><p>若 pilot 通过，论文可以主张自然欠指定条件下的自主用户状态发现与利用；若不能产生超出 G-STEER / IDRBench 的新排序或新失败，就应收窄或换题。</p></div></footer>
    </main>
  );
}
