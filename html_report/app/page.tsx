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
            <p className="eyebrow">RESEARCH PROPOSAL · v0.48 · 2026-08-12</p>
            <h1>绝对适配不等于<em>反事实用户特异性</em></h1>
            <p className="lede">固定 task、evidence、tools 和 budget，只改变目标用户。我们检验最终报告是否双向正确改变，并同时通过绝对合格、相对通用回答收益、共同质量与边界门。</p>
            <div className="heroActions"><a className="button primary" href="#design">看整体框架</a><a className="button ghost" href="/DeepAlign-Bench_正式Proposal精简版.pdf" download>下载正式精简版</a></div>
            <div className="heroMeta"><span>paired-user task family</span><span>2×2 交叉评分</span><span>非补偿 profile</span><span>clarification 是 channel</span></div>
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

      <section className="figureSection" id="design"><div className="shell"><div className="sectionHead light"><h2>一张图看懂元数据、渠道、交叉矩阵、实验结论和五天冻结门</h2><p>SVG 可编辑；PNG 适合直接拿去导师汇报。</p></div><figure><img src="/DeepAlign-Bench_整体框架与PDR压力测试_v0.48.png" alt="DeepAlign-Bench v0.48 整体研究框架与 PDR-compatible 压力测试"/><figcaption>v0.48：本地实验数字不变；GPT-5 复现已预注册，但被 provider terms 拦在 inference 前。</figcaption></figure></div></section>

      <section className="shell gapSection">
        <p className="sectionTag">CASE / TASK / USER TRUTH</p>
        <div className="sectionHead"><h2>同一个隐藏 ledger，生成多种输入渠道</h2><p>Case metadata 记录运行；task metadata 冻结研究构念；user-state ledger 记录每条事实的来源、权限和 decision-node 作用。</p></div>
        <div className="compare" role="table" aria-label="用户信息渠道">
          <div className="compareRow head" role="row"><span>渠道</span><span>Agent 看到什么</span><span>额外测量</span></div>
          <div className="compareRow" role="row"><b>Structured persona</b><span>字段化目标、约束、资源与边界</span><span>信息给到后是否采用</span></div>
          <div className="compareRow" role="row"><b>Natural history</b><span>同一信息放入自然叙述、历史或授权记录</span><span>语义等价渠道稳定性</span></div>
          <div className="compareRow" role="row"><b>Fuzzy query + clarification</b><span>query 可写通用报告，但缺 1–3 个会改变建议的条件</span><span>asked→answered→planned→adopted、负担和隐私</span></div>
          <div className="compareRow" role="row"><b>Task-only</b><span>没有任务相关用户信息</span><span>一般高质量基线与新增收益</span></div>
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
      </div></section>

      <section className="shell gapSection" id="novelty"><p className="sectionTag">NEAREST-NEIGHBOR BOUNDARY</p><div className="sectionHead"><h2>Clarification 不是 novelty；paired-user measurement 才必须用结果证明</h2><p>DeepAlign 不能声称首次研究个性化 Deep Research 或主动澄清。</p></div><div className="sourceGrid">{papers.map(([name, role, url]) => <a key={name} href={url} target="_blank" rel="noreferrer"><b>{name}</b><span>{role}</span></a>)}</div></section>

      <section className="decision shell" id="deadline"><p className="sectionTag">FIVE-DAY THESIS FREEZE</p><div className="sectionHead"><h2>最迟 2026-08-17 冻结方向</h2><p>ICLR 2027 摘要 9 月 11 日 AOE、全文 9 月 16 日 AOE；当前约剩 30/35 天。</p></div><div className="decisionGrid"><article><span>01</span><h3>解除合规访问阻塞</h3><p>使用受支持账户/地区的 GPT-5 key，从已冻结 smoke 断点继续；不绕过 provider terms。</p></article><article><span>02</span><h3>双人盲评</h3><p>独立判断 absolute fit、decision adoption 与 matched/swapped。</p></article><article><span>03</span><h3>补到 3 family</h3><p>至少 2/3 的 paired-user 真值稳定；否则收窄 judge-validity 或换题。</p></article></div></section>

      <section className="editionSection" id="editions"><div className="shell"><p className="sectionTag">READING EDITIONS</p><div className="sectionHead"><h2>DeepAlign-Bench v0.48 四个同步版本</h2><p>ElicitAlign v0.45 已完整归档，不再占用顶层入口。</p></div><div className="editionGrid">
        <article><span>FORMAL</span><h3>正式研究 Proposal</h3><p>完整方法、文献、rubric、环境、风险和实验记录。</p><div className="editionLinks"><a href="/DeepAlign-Bench_正式研究Proposal.pdf" download>PDF</a><a href="/DeepAlign-Bench_正式研究Proposal.docx" download>Word</a></div></article>
        <article className="recommended"><span>CONDENSED · ≤10 PAGES</span><h3>正式 Proposal 精简版</h3><p>适合快速判断 thesis、实验、证据等级和 go/no-go。</p><div className="editionLinks"><a href="/DeepAlign-Bench_正式Proposal精简版.pdf" download>PDF</a><a href="/DeepAlign-Bench_正式Proposal精简版.docx" download>Word</a></div></article>
        <article><span>PLAIN LANGUAGE</span><h3>完整人话版</h3><p>逐步解释 case、task、persona、channel、rubric、公式和统计。</p><div className="editionLinks"><a href="/DeepAlign-Bench_完整人话版.pdf" download>PDF</a><a href="/DeepAlign-Bench_完整人话版.docx" download>Word</a></div></article>
        <article><span>ADVISOR BRIEF</span><h3>汇报精简版</h3><p>15–20 分钟导师汇报结构，含最小实验与五天决策。</p><div className="editionLinks"><a href="/DeepAlign-Bench_汇报精简版.pdf" download>PDF</a><a href="/DeepAlign-Bench_汇报精简版.docx" download>Word</a></div></article>
      </div><div className="schemaDownloads"><a href="/case.schema.yaml" download>Case schema ↓</a><a href="/metric_binding.schema.yaml" download>Metric binding ↓</a><a href="/DeepAlign-Bench_整体框架与PDR压力测试_v0.48.svg" download>可编辑 SVG ↓</a><a href="/PROJECT_MEMORY.md" download>项目记忆 ↓</a></div></div></section>

      <footer className="closing"><div className="shell closingGrid"><div><p className="eyebrow">CLAIM BOUNDARY</p><h2>只主张最终交付物的反事实用户特异性</h2></div><p>不声称模型内部真正理解用户；不把本地 Qwen pilot 写成官方 PDR 失败；不把 clarification 包装成首次研究。</p></div></footer>
    </main>
  );
}
