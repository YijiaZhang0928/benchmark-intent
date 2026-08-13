import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "DeepAlign-Bench｜研究汇报",
  description: "个性化 Deep Research 的反事实用户特异性评测",
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
            <p className="eyebrow">RESEARCH PROPOSAL · v0.51 · 2026-08-14</p>
            <h1>绝对适配不等于<em>反事实用户特异性</em></h1>
            <p className="lede">固定 task、evidence、tools 和 budget，只改变目标用户。我们检验最终报告是否双向正确改变，并同时通过绝对合格、相对通用回答收益、共同质量与边界门。</p>
            <div className="heroActions"><a className="button primary" href="#design">看整体框架</a><a className="button ghost" href="/DeepAlign-Bench_正式Proposal精简版.pdf" download>下载正式精简版</a></div>
            <div className="heroMeta"><span>PDR 50 tasks / 501 pairs</span><span>paired-user task family</span><span>2×2 交叉评分</span><span>3 families / 24 episodes</span></div>
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

      <section className="figureSection" id="design"><div className="shell"><div className="sectionHead light"><h2>一张图看懂资源池、元数据、统一范式、交叉矩阵和证据门</h2><p>SVG 可编辑；PNG 适合直接拿去导师汇报。</p></div><figure><img src="/DeepAlign-Bench_整体框架与PDR压力测试_v0.51.png" alt="DeepAlign-Bench v0.51 整体研究框架、PDR 资源池与统一 Research Episode"/><figcaption>v0.51：PDR 公开资源完整导入，501 个候选用户对需要反事实筛选；3-family / 24-episode seed 目前只通过结构校验。</figcaption></figure></div></section>

      <section className="shell gapSection" id="resource-pool">
        <p className="sectionTag">PDR RESOURCE POOL ≠ DEEPALIGN GOLD</p>
        <div className="sectionHead"><h2>完整复用公开资源，但不把原配对直接当成实验真值</h2><p>Structured persona 是志愿者自填后去标识化的衍生数据；dynamic context 是标注者模拟。DeepAlign 还需证明同一任务下两位用户会产生可预注册的关键决策分歧。</p></div>
        <div className="decisionGrid">
          <article><span>50</span><h3>双语 tasks</h3><p>全部进入可复现资源池；Health、Finance、Law 未经专家审查不进入核心结果。</p></article>
          <article><span>25</span><h3>Structured personas</h3><p>保留 volunteer-grounded 来源标签；不能把模拟 context 写成真人自然轨迹。</p></article>
          <article><span>501</span><h3>候选用户对</h3><p>逐对审核 must-change / must-hold / must-not / clarify，最终选择约 12–20 个核心 family。</p></article>
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

      <section className="decision shell" id="deadline"><p className="sectionTag">ICLR 2027 WEEKLY EXECUTION</p><div className="sectionHead"><h2>9 月 13 日前完成结果与 9 页初稿</h2><p>官方节点：摘要 9 月 18 日 AOE、全文 9 月 25 日 AOE；9 月 13 日后不新增 metric、paradigm 或 domain。</p></div><div className="decisionGrid"><article><span>W1</span><h3>3 个完整 family</h3><p>冻结 evidence、ledger、contracts、rubric leaves、反例报告，并完成双人盲评。</p></article><article><span>W2–3</span><h3>小矩阵后扩样本</h3><p>先验证重分类与人评一致性，再从 501 对中筛到 12–20 个核心 family。</p></article><article><span>W4–6</span><h3>统计、复现、投稿</h3><p>family-level 统计与 9 页初稿；随后只做冻结、独立复现、匿名和结论威胁修复。</p></article></div></section>

      <section className="editionSection" id="editions"><div className="shell"><p className="sectionTag">READING EDITIONS</p><div className="sectionHead"><h2>DeepAlign-Bench v0.51 四个同步版本</h2><p>PDR 资源池、反事实筛选和逐周执行已经进入正式方法。</p></div><div className="editionGrid">
        <article><span>FORMAL</span><h3>正式研究 Proposal</h3><p>完整方法、文献、rubric、环境、风险和实验记录。</p><div className="editionLinks"><a href="/DeepAlign-Bench_正式研究Proposal.pdf" download>PDF</a><a href="/DeepAlign-Bench_正式研究Proposal.docx" download>Word</a></div></article>
        <article className="recommended"><span>CONDENSED · ≤10 PAGES</span><h3>正式 Proposal 精简版</h3><p>适合快速判断 thesis、实验、证据等级和 go/no-go。</p><div className="editionLinks"><a href="/DeepAlign-Bench_正式Proposal精简版.pdf" download>PDF</a><a href="/DeepAlign-Bench_正式Proposal精简版.docx" download>Word</a></div></article>
        <article><span>PLAIN LANGUAGE</span><h3>完整人话版</h3><p>逐步解释 case、task、persona、channel、rubric、公式和统计。</p><div className="editionLinks"><a href="/DeepAlign-Bench_完整人话版.pdf" download>PDF</a><a href="/DeepAlign-Bench_完整人话版.docx" download>Word</a></div></article>
        <article><span>ADVISOR BRIEF</span><h3>汇报精简版</h3><p>15–20 分钟导师汇报结构，含最小实验与五天决策。</p><div className="editionLinks"><a href="/DeepAlign-Bench_汇报精简版.pdf" download>PDF</a><a href="/DeepAlign-Bench_汇报精简版.docx" download>Word</a></div></article>
      </div><div className="schemaDownloads"><a href="/case.schema.yaml" download>Case schema ↓</a><a href="/research_episode.schema.yaml" download>Episode schema ↓</a><a href="/seed_v0_50_families.yaml" download>Seed families ↓</a><a href="/pdr_candidate_pair_audit.csv" download>PDR 501-pair audit ↓</a><a href="/ICLR2027_weekly_plan.md" download>每周计划 ↓</a><a href="/DeepAlign-Bench_整体框架与PDR压力测试_v0.51.svg" download>可编辑 SVG ↓</a><a href="/PROJECT_MEMORY.md" download>项目记忆 ↓</a></div></div></section>

      <footer className="closing"><div className="shell closingGrid"><div><p className="eyebrow">CLAIM BOUNDARY</p><h2>只主张最终交付物的反事实用户特异性</h2></div><p>不声称模型内部真正理解用户；不把本地 Qwen pilot 写成官方 PDR 失败；不把 clarification 包装成首次研究。</p></div></footer>
    </main>
  );
}
