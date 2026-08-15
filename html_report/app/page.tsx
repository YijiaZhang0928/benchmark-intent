import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "DeepAlign-Bench｜研究汇报",
  description: "三个长程知识工作场景中的反事实用户特异性评测",
};

const papers = [
  ["PDR-Bench", "task/persona-conditioned absolute adaptation", "https://arxiv.org/abs/2509.25106"],
  ["MyScholarQA", "真人揭示合成用户与 LLM judge 漏掉的个性化错误", "https://aclanthology.org/2026.acl-long.723/"],
  ["IDRBench", "欠指定 Deep Research 的交互收益与成本", "https://arxiv.org/abs/2601.06676"],
  ["G-STEER", "个性化 Deep Research 的 Retrieve / Ask / Stop", "https://arxiv.org/abs/2608.05876"],
];

export default function Home() {
  return (
    <main>
      <header className="hero" id="top">
        <nav className="nav shell" aria-label="主导航">
          <a className="brand" href="#top">DeepAlign<span>Bench</span></a>
          <div className="navlinks"><a href="#question">问题</a><a href="#design">框架</a><a href="#metrics">评分</a><a href="#pilot">实验</a><a href="#deadline">决策</a></div>
          <a className="navCta" href="#editions">下载文档</a>
        </nav>
        <div className="heroGrid shell">
          <section>
            <p className="eyebrow">RESEARCH PROPOSAL · v0.54 · 2026-08-16</p>
            <h1>绝对适配不等于<em>反事实用户特异性</em></h1>
            <p className="lede">固定 task、evidence/repository/data、tools 和 budget，只改变目标用户。我们在 open-web research、repository software engineering 和 data-centric analysis 三个代表性场景中，检验最终 artifact 是否双向正确改变。</p>
            <div className="heroActions"><a className="button primary" href="#design">看整体框架</a><a className="button ghost" href="/DeepAlign-Bench_正式Proposal精简版.pdf" download>下载正式精简版</a></div>
            <div className="heroMeta"><span>180 candidate seeds</span><span>60 provisional families</span><span>DR / Software / Data = 40 / 30 / 30</span><span>Paper first: 5 / 3 / 4</span></div>
          </section>
          <aside className="thesisCard"><span className="cardKicker">一句话研究问题</span><p>一份报告对用户 A 看起来很好，不代表系统把用户换成 B 时会按正确方向改变最终选择。</p><hr/><div className="thesisFlow"><b>Absolute Fit</b><i>≠</i><b>Specificity</b><i>→</i><b>Benefit</b></div></aside>
        </div>
      </header>

      <section className="decision shell" id="question">
        <p className="sectionTag">WHAT THIS BENCHMARK SEPARATES</p>
        <div className="sectionHead"><h2>把“写得好”与“真的因用户而变”分开</h2><p>PDR 的 absolute adaptation 构念有价值；DeepAlign 补充它不能单独识别的 paired-user counterfactual specificity。</p></div>
        <div className="decisionGrid">
          <article><span>01</span><h3>通用好报告</h3><p>对两位用户都高分，但没有完成 must-change，说明 adequacy 高、specificity 不成立。</p></article>
          <article><span>02</span><h3>单边个性化</h3><p>只对 A 有优势、对 B 为负，平均差值可能为正；CFA_min 会直接判失败。</p></article>
          <article><span>03</span><h3>表面个性化</h3><p>提到 persona 不等于采用约束；mention、planning 与 final adoption 必须分开评分。</p></article>
        </div>
      </section>

      <section className="figureSection" id="design"><div className="shell"><div className="sectionHead light"><h2>一张图看懂 180→60→12 任务升级路径</h2><p>SVG 可编辑；PNG 适合直接拿去导师汇报。</p></div><figure><img src="/DeepAlign-Bench_PLHKW任务资源池_v0.54.png" alt="DeepAlign-Bench v0.54 PLHKW 任务资源池、三场景抽样与升级硬门"/><figcaption>v0.54：60 个是经作者阶段筛选的 provisional shells，不是 60 个 runnable gold families。</figcaption></figure></div></section>

      <section className="shell gapSection" id="resource-pool">
        <p className="sectionTag">CANDIDATE POOL ≠ RUNNABLE GOLD</p>
        <div className="sectionHead"><h2>40 / 30 / 30 是抽样结构，不是完成度宣称</h2><p>DR 保留与 PDR-Bench 的 continuity；software 与 data 各自达到能单独分析的规模。五道人工/环境硬门前，所有 family 都只是 provisional。</p></div>
        <div className="decisionGrid">
          <article><span>24</span><h3>Open-web Research</h3><p>find &amp; synthesize；含 12 个 PDR-derived shell，再补 literature/prior-art/dataset/conflict/update 结构。</p></article>
          <article><span>18</span><h3>Repository Software</h3><p>modify &amp; build；只选 multiple acceptable implementations，用 invariant tests + user-conditioned checks。</p></article>
          <article><span>18</span><h3>Data / ML / Spreadsheet</h3><p>analyze &amp; infer；同一数据下允许不同合理分析重点，但共同计算正确性不能下降。</p></article>
        </div>
      </section>

      <section className="shell gapSection">
        <p className="sectionTag">CASE / TASK / USER TRUTH</p>
        <div className="sectionHead"><h2>把交互时机、信息来源与访问方式分开</h2><p>每次运行是一条 information-event timeline；产品 UI 只是配置，不是科学构念。</p></div>
        <div className="compare" role="table" aria-label="核心 Research Episode 范式">
          <div className="compareRow head" role="row"><span>核心范式</span><span>信息如何进入</span><span>识别什么能力</span></div>
          <div className="compareRow" role="row"><b>P0 Task-only closed</b><span>无用户状态，禁止用户接触</span><span>通用研究质量 baseline</span></div>
          <div className="compareRow" role="row"><b>P1 One-shot direct</b><span>完整事实在规划前一次性推送</span><span>信息给到后是否采用</span></div>
          <div className="compareRow" role="row"><b>P2 Pre-research clarification</b><span>模糊 query；agent 必须主动问到隐藏事实</span><span>asked→answered→planned→adopted</span></div>
          <div className="compareRow" role="row"><b>P4 Checkpoint update</b><span>中途新事实覆盖旧状态</span><span>重规划、清除旧结论、保持未变事实</span></div>
        </div>
      </section>

      <section className="classificationSection" id="metrics"><div className="shell">
        <p className="sectionTag">NON-COMPENSATORY PROFILE</p>
        <div className="sectionHead"><h2>差值用于识别效应，不用来充当万能总分</h2><p>PF 先归一到 [0,1]；比例分母会放大低分区噪声，向量夹角又不能保证幅度和绝对合格。</p></div>
        <div className="formula">Δa = PFₐ(Yₐ) − PFₐ(Yᵦ)<br/>Δb = PFᵦ(Yᵦ) − PFᵦ(Yₐ)<br/>CFA_min = min(Δa, Δb)<br/>A_min = min(PFₐ(Yₐ), PFᵦ(Yᵦ))<br/>Gain_min = min(PFₐ(Yₐ)−PFₐ(Y₀), PFᵦ(Yᵦ)−PFᵦ(Y₀))</div>
        <div className="taxonomyRules">
          <article><b>双向 specificity</b><p>Δa 与 Δb 都超过预注册最小实际重要差异。</p></article>
          <article><b>绝对 adequacy</b><p>A_min 过线，防止“大差值、低适配”。</p></article>
          <article><b>真实 benefit</b><p>先过 task-only non-inferiority；added value 另设 margin。</p></article>
          <article><b>No-harm / no-violation</b><p>共同质量、事实、must-hold 不下降；critical boundary 零严重违规。</p></article>
        </div>
        <div className="classificationVerdict"><b>统计单位是 task family</b><p>Permutation 在 family 内交换标签；bootstrap 每次抽完整 family。用户、seed、judge repeat 和 rubric leaf 都不能冒充独立任务。</p></div>
      </div></section>

      <section className="reviewBand" id="pilot"><div className="shell">
        <p className="sectionTag invert">DIRECTIONAL PDR-COMPATIBLE STRESS TEST</p>
        <div className="sectionHead light"><h2>最小实验：核心 claim 得到 go 信号，over-personalization 强 claim 被削弱</h2><p>2 families、4 users、32 次本地 Qwen3-8B 评分；不是官方 PDR-Bench 复现。</p></div>
        <div className="decisionGrid">
          <article><span>4/4</span><h3>General-good 近 matched</h3><p>四个单元全部差距 ≤0.5，一次反超；absolute high 不能证明 specificity。</p></article>
          <article><span>1/4</span><h3>Over 近 matched</h3><p>不支持“普遍误判”；但四份都 ≥6，关键错误可能被平均补偿。</p></article>
          <article><span>0/2</span><h3>Family 通过 CFA_min&gt;0</h3><p>A_min 为 8.50/10.00，CFA_min 却为 −1.50/0.00；绝对合格与特异性脱钩。</p></article>
        </div>
        <p className="matrixNote">GPT-5 复现状态：4 family / 20 reports / 官方 PDR prompts 已在结果前冻结并推送；OpenRouter key 有效且 GPT-5 可见，但账户/地域层 Terms of Service 403 在 provider endpoint 选择前阻断请求。当前没有 GPT-5 completion、criteria 或分数。</p>
        <p className="matrixNote"><b>Introduction 证据门：</b>general-good 高分只是 identification blind spot；盲化人评确认关键决定错误而 GPT-5 仍 near-matched/rank-reversal，才是受控假阳性；跨真实 family、多系统重分类与真人增量效度，才是论文级测量效度证据。</p>
      </div></section>

      <section className="shell gapSection" id="novelty"><p className="sectionTag">NEAREST-NEIGHBOR BOUNDARY</p><div className="sectionHead"><h2>Clarification 不是 novelty；paired-user measurement 才必须用结果证明</h2><p>DeepAlign 不能声称首次研究个性化 Deep Research 或主动澄清。</p></div><div className="sourceGrid">{papers.map(([name, role, url]) => <a key={name} href={url} target="_blank" rel="noreferrer"><b>{name}</b><span>{role}</span></a>)}</div></section>

      <section className="decision shell" id="deadline"><p className="sectionTag">PAPER-FIRST EXECUTION</p><div className="sectionHead"><h2>先完成 12 个端到端 family，再扩展 60-family release</h2><p>资源不足时先减 agent 数、P4 anchor 和真人效用子集，不把 software/data 又降成几个展示题。</p></div><div className="decisionGrid"><article><span>W1</span><h3>3 个 vertical slices</h3><p>DR、Software、Data 各完成一个许可、reset、verifier 和 matched/swapped pilot。</p></article><article><span>PAPER</span><h3>12 families：5 / 3 / 4</h3><p>每个 vertical 内至少两条可比系统；跨 vertical 只比共同 specificity/no-harm profile。</p></article><article><span>RELEASE</span><h3>60 逐个升级</h3><p>完成 source-license、asset binding、two-human screen、contract freeze 与 pilot discrimination。</p></article></div></section>

      <section className="editionSection" id="editions"><div className="shell"><p className="sectionTag">READING EDITIONS</p><div className="sectionHead"><h2>DeepAlign-Bench v0.54 四个同步版本</h2><p>180→60 资源池、40/30/30 抽样与 provisional/runnable 边界已进入正式方法。</p></div><div className="editionGrid">
        <article><span>FORMAL</span><h3>正式研究 Proposal</h3><p>完整方法、文献、rubric、环境、风险和实验记录。</p><div className="editionLinks"><a href="/DeepAlign-Bench_正式研究Proposal.pdf" download>PDF</a><a href="/DeepAlign-Bench_正式研究Proposal.docx" download>Word</a></div></article>
        <article className="recommended"><span>CONDENSED · ≤10 PAGES</span><h3>正式 Proposal 精简版</h3><p>适合快速判断 thesis、实验、证据等级和 go/no-go。</p><div className="editionLinks"><a href="/DeepAlign-Bench_正式Proposal精简版.pdf" download>PDF</a><a href="/DeepAlign-Bench_正式Proposal精简版.docx" download>Word</a></div></article>
        <article><span>PLAIN LANGUAGE</span><h3>完整人话版</h3><p>逐步解释 case、task、persona、channel、rubric、公式和统计。</p><div className="editionLinks"><a href="/DeepAlign-Bench_完整人话版.pdf" download>PDF</a><a href="/DeepAlign-Bench_完整人话版.docx" download>Word</a></div></article>
        <article><span>ADVISOR BRIEF</span><h3>汇报精简版</h3><p>15–20 分钟导师汇报结构，含最小实验与五天决策。</p><div className="editionLinks"><a href="/DeepAlign-Bench_汇报精简版.pdf" download>PDF</a><a href="/DeepAlign-Bench_汇报精简版.docx" download>Word</a></div></article>
      </div><div className="schemaDownloads"><a href="/plhkw_task_catalog.html">60-family catalog →</a><a href="/plhkw_paper_first_12.csv" download>Paper-first 12 CSV ↓</a><a href="/plhkw_selected_tasks.csv" download>Selected tasks CSV ↓</a><a href="/case.schema.yaml" download>Case schema ↓</a><a href="/research_episode.schema.yaml" download>Episode schema ↓</a><a href="/ICLR2027_weekly_plan.md" download>每周计划 ↓</a><a href="/DeepAlign-Bench_PLHKW任务资源池_v0.54.svg" download>可编辑 SVG ↓</a><a href="/PROJECT_MEMORY.md" download>项目记忆 ↓</a></div></div></section>

      <footer className="closing"><div className="shell closingGrid"><div><p className="eyebrow">CLAIM BOUNDARY</p><h2>三个代表性场景，不是所有知识工作</h2></div><p>不声称模型内部真正理解用户；不把 60 个 provisional shells 写成 60 个 runnable gold；不把显式约束跟随冒充完整个性化。</p></div></footer>
    </main>
  );
}
