import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "DeepAlign-Bench｜研究汇报",
  description: "三个长程知识工作场景中的反事实用户特异性评测",
};

const papers = [
  ["PDR-Bench", "task/persona-conditioned absolute adaptation", "https://arxiv.org/abs/2509.25106"],
  ["MyScholarQA", "真人揭示合成用户与 LLM judge 漏掉的个性化错误", "https://aclanthology.org/2026.acl-long.723/"],
  ["JudgeBench / JUDGE-BENCH", "judge benchmark 名称与跨任务可靠性已有直接前作", "https://arxiv.org/abs/2410.12784"],
  ["RuVerBench", "长 agentic artifact 的 rubric verification 仍有显著噪声", "https://arxiv.org/abs/2606.29920"],
  ["GAMUT", "two-level meta-rubric → mechanical checks 已有前作", "https://arxiv.org/abs/2607.19322"],
];

export default function Home() {
  return (
    <main>
      <header className="hero" id="top">
        <nav className="nav shell" aria-label="主导航">
          <a className="brand" href="#top">DeepAlign<span>Bench</span></a>
          <div className="navlinks"><a href="#question">问题</a><a href="#design">框架</a><a href="#credamo">真人问卷</a><a href="#interaction">交互环境</a><a href="#metrics">评分</a><a href="#deadline">决策</a></div>
          <a className="navCta" href="#editions">下载文档</a>
        </nav>
        <div className="heroGrid shell">
          <section>
            <p className="eyebrow">RESEARCH PROPOSAL · v0.59 · 2026-08-22</p>
            <h1>绝对适配不等于<em>反事实用户特异性</em></h1>
            <p className="lede">固定 task、evidence/repository/data、tools 和 budget，只改变目标用户。我们在 open-web research、repository software engineering 和 data-centric analysis 三个代表性场景中，检验最终 artifact 是否双向正确改变。</p>
            <div className="heroActions"><a className="button primary" href="#design">看整体框架</a><a className="button ghost" href="/DeepAlign-Bench_正式Proposal精简版.pdf" download>下载正式精简版</a></div>
            <div className="heroMeta"><span>180 candidate seeds</span><span>60 provisional families</span><span>One primary artifact each</span><span>DR / Software / Data = 40 / 30 / 30</span><span>Paper first: 5 / 3 / 4</span></div>
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

      <section className="figureSection" id="design"><div className="shell"><div className="sectionHead light"><h2>一张图看懂真人真值、CDM 与 D-JQS</h2><p>核心是权威分离：用户、标注员、专家、compiler 和 judge 不能越权替彼此决定真值。</p></div><figure><img src="/DeepAlign-Bench_真人真值到D-JQS_v0.55.png" alt="DeepAlign-Bench v0.55 真人 ledger、Counterfactual Difference Map、受约束 rubric 编译与 D-JQS"/><figcaption>v0.55：freeze 只防 post-hoc；真实性来自真人 provenance，执行可靠性来自 validated verifier、slice-qualified judge 与盲化人评。</figcaption></figure></div></section>

      <section className="shell gapSection" id="resource-pool">
        <p className="sectionTag">CANDIDATE POOL ≠ RUNNABLE GOLD</p>
        <div className="sectionHead"><h2>40 / 30 / 30 是抽样结构，不是完成度宣称</h2><p>DR 保留与 PDR-Bench 的 continuity；software 与 data 各自达到能单独分析的规模。五道人工/环境硬门前，所有 family 都只是 provisional。</p></div>
        <div className="decisionGrid">
          <article><span>24</span><h3>Open-web Research</h3><p>find &amp; synthesize；含 10 个 PDR-derived shell，再补 program/resource、literature、prior-art、dataset、conflict、update 与 exhaustive-search 结构。</p></article>
          <article><span>18</span><h3>Repository Software</h3><p>modify &amp; build；只选 multiple acceptable implementations，用 invariant tests + user-conditioned checks。</p></article>
          <article><span>18</span><h3>Data / ML / Spreadsheet</h3><p>analyze &amp; infer；同一数据下允许不同合理分析重点，但共同计算正确性不能下降。</p></article>
        </div>
      </section>

      <section className="shell gapSection">
        <p className="sectionTag">HUMAN TRUTH → RELATIONAL GOLD</p>
        <div className="sectionHead"><h2>先构造成对关系真值，再编译 rubric</h2><p>每位用户从随机化/分层 slate 选 3–5 个真实任务；开放 elicitation 先于结构追问，后台 ledger 不默认暴露给 agent。</p></div>
        <div className="compare" role="table" aria-label="核心 Research Episode 范式">
          <div className="compareRow head" role="row"><span>层</span><span>谁有权决定</span><span>硬门</span></div>
          <div className="compareRow" role="row"><b>真人 ledger</b><span>用户：自己的目标、取舍、不可用条件</span><span>spontaneous/prompted + uncertainty + consent</span></div>
          <div className="compareRow" role="row"><b>CDM</b><span>用户确认 consequence；annotator 审计；expert 判可行性</span><span>no-provenance node fails closed</span></div>
          <div className="compareRow" role="row"><b>Rubric compiler</b><span>只能把 frozen node 拆成 executable leaves</span><span>dependency group + node-first aggregation</span></div>
          <div className="compareRow" role="row"><b>D-JQS / Human</b><span>judge 只应用标准；关键 slice 失败就人评</span><span>grouped hidden qualification + nuisance controls</span></div>
        </div>
      </section>

      <section className="shell gapSection" id="credamo">
        <p className="sectionTag">CREDAMO · OPEN FIRST · HUMAN CONFIRMED</p>
        <div className="sectionHead"><h2>3–5 个是候选任务；每人默认只深采 1 个主任务</h2><p>真人不能直接填写 persona。问卷先确认任务确实相关，再保存开放原话，最后才用 task-family schema 补漏并逐条确认 LLM 规范化事实。</p></div>
        <div className="decisionGrid">
          <article><span>A</span><h3>筛选、路由与选择</h3><p>10–15 分钟；按教育/职业领域和 coding/data/research 经验展示 10–15 张 cards，逐卡核验 relevance、experience、safe-answerability，再选 3–5 个真实候选。</p></article>
          <article><span>B</span><h3>Open-first 深度采集</h3><p>15–22 分钟/任务；后台分配 1 个主任务、最多 1 个次任务。五个开放回答提交锁定后，才显示 DR / Software / Data schema。</p></article>
          <article><span>C</span><h3>LLM 规范化确认</h3><p>5–8 分钟/任务；每张 fact card 必须带原话 source span，用户逐条 approve、edit、delete 或 uncertain，并分别设置三层使用权限。</p></article>
        </div>
        <div className="classificationVerdict"><b>人民币 3,000 元只支持构念验证 pilot</b><p>保留 12 个 paper-first family：每题先取 2 个 confirmed ledger，再只为 6 个跨 vertical anchor 补第 3 人，目标 30 个 user–task records。它不承担 agent 排名或 60-task 总体结论；人口学不参与路由，真实相关任务不足 3 个时不强迫凑数。</p></div>
      </section>

      <section className="shell gapSection" id="interaction">
        <p className="sectionTag">RUNNABLE PYTHON · RESET / STEP · VALUE MINIMIZATION</p>
        <div className="sectionHead"><h2>同一 hidden persona，三种可控交互模式</h2><p>每个 case 固定 Task、hidden persona、attribute importance graph 与 reveal policy。默认 rule backend 完全离线可跑；structured-LLM adapter 可接任意 provider。</p></div>
        <div className="decisionGrid">
          <article><span>A</span><h3>Oracle</h3><p>Agent 在 reset 直接获得完整 persona；全部属性从第 0 步记为已披露。它是信息上限，不保证 agent 会用对。</p></article>
          <article><span>B</span><h3>Naive</h3><p>Agent 起初只见 task；LLM user simulator 能看到完整 persona，且不执行 reveal policy，因而允许无关或过度披露。</p></article>
<article><span>C</span><h3>Interactive</h3><p>Persona 隐藏；Interactive 的 classifier 只看 value-free descriptor，response backend 只拿本轮通过 policy 的属性值。</p></article>
        </div>
        <div className="compare" role="table" aria-label="交互环境每步执行与日志">
          <div className="compareRow head" role="row"><span>Step</span><span>执行</span><span>审计输出</span></div>
          <div className="compareRow" role="row"><b>1 · classify</b><span>判断是不是用户信息问题；匹配 attribute ID + confidence</span><span>is_question / evidence / matched</span></div>
          <div className="compareRow" role="row"><b>2 · reveal</b><span>按 sensitivity、prerequisite、scripted trust、graph rank、probability 与 turn budget 决定</span><span>reveal/withhold reason + random draw</span></div>
          <div className="compareRow" role="row"><b>3 · respond</b><span>只把获准值交给 Interactive response backend；未授权 literal marker 命中则 fail closed</span><span>newly/cumulative revealed + blocked</span></div>
          <div className="compareRow" role="row"><b>4 · persist</b><span>保存 user response；final artifact 用 step(message, final=True) 提交</span><span>matched-unrevealed + still-hidden</span></div>
        </div>
        <div className="classificationVerdict"><b>可运行不等于真人有效</b><p>Naive→Interactive 同时改变 simulator 的信息访问与披露行为，不能解释为纯 agent effect；scripted trust 也不是真人心理模型。正式结果须固定 backend/version/seed/turn budget，并用独立真人轨迹校准 attribute-level match、reveal decision、自然度、事实忠实、语义泄漏与 system-ranking stability。</p></div>
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

      <section className="shell gapSection" id="novelty"><p className="sectionTag">NEAREST-NEIGHBOR BOUNDARY</p><div className="sectionHead"><h2>Compiler 与 judge benchmark 不是 novelty；CDM 必须用结果证明</h2><p>必须比较 PDR-style absolute rubric、独立 A/B rubric、CDM 对称 rubric 与 single-judge/hybrid scoring。若 CDM 既不重分类系统，也不增量预测盲化真人选择，只能称 transparent measurement extension。</p></div><div className="sourceGrid">{papers.map(([name, role, url]) => <a key={name} href={url} target="_blank" rel="noreferrer"><b>{name}</b><span>{role}</span></a>)}</div></section>

      <section className="decision shell" id="deadline"><p className="sectionTag">PAPER-FIRST EXECUTION</p><div className="sectionHead"><h2>先完成 12 个端到端 family，再扩展 60-family release</h2><p>60 题统一为一个提交边界、一个主要交付物。24 个 DR 只产出检索、核验或综合型 evidence artifact，不要求推荐或规划。</p></div><div className="decisionGrid"><article><span>W1</span><h3>3 个 vertical slices</h3><p>DR、Software、Data 各完成一个许可、reset、verifier 和 matched/swapped pilot。</p></article><article><span>PAPER</span><h3>12 families：5 / 3 / 4</h3><p>每个 vertical 内至少两条可比系统；跨 vertical 只比共同 specificity/no-harm profile。</p></article><article><span>RELEASE</span><h3>60 逐个升级</h3><p>完成 source-license、asset binding、two-human screen、contract freeze 与 pilot discrimination。</p></article></div></section>

      <section className="editionSection" id="editions"><div className="shell"><p className="sectionTag">READING EDITIONS</p><div className="sectionHead"><h2>DeepAlign-Bench v0.59 同步版本与任务契约</h2><p>真人真值、Credamo 三轮采集、CDM、受约束 rubric、D-JQS、runnable hidden-persona environment 与单交付物任务池已进入正式方法。</p></div><div className="editionGrid">
        <article><span>FORMAL</span><h3>正式研究 Proposal</h3><p>完整方法、文献、rubric、环境、风险和实验记录。</p><div className="editionLinks"><a href="/DeepAlign-Bench_正式研究Proposal.pdf" download>PDF</a><a href="/DeepAlign-Bench_正式研究Proposal.docx" download>Word</a></div></article>
        <article className="recommended"><span>CONDENSED · ≤10 PAGES</span><h3>正式 Proposal 精简版</h3><p>适合快速判断 thesis、实验、证据等级和 go/no-go。</p><div className="editionLinks"><a href="/DeepAlign-Bench_正式Proposal精简版.pdf" download>PDF</a><a href="/DeepAlign-Bench_正式Proposal精简版.docx" download>Word</a></div></article>
        <article><span>PLAIN LANGUAGE</span><h3>完整人话版</h3><p>逐步解释 case、task、persona、channel、rubric、公式和统计。</p><div className="editionLinks"><a href="/DeepAlign-Bench_完整人话版.pdf" download>PDF</a><a href="/DeepAlign-Bench_完整人话版.docx" download>Word</a></div></article>
        <article><span>ADVISOR BRIEF</span><h3>汇报精简版</h3><p>15–20 分钟导师汇报结构，含最小实验与五天决策。</p><div className="editionLinks"><a href="/DeepAlign-Bench_汇报精简版.pdf" download>PDF</a><a href="/DeepAlign-Bench_汇报精简版.docx" download>Word</a></div></article>
        <article className="recommended"><span>HUMAN STUDY INSTRUMENT</span><h3>Credamo 真人 Persona 问卷</h3><p>21 页、92 题、60-task 路由、精确跳转、质控、时长、报酬和上线门。</p><div className="editionLinks"><a href="/DeepAlign-Bench_Credamo真人Persona问卷方案_v0.59.pdf" download>PDF</a><a href="/DeepAlign-Bench_Credamo真人Persona问卷方案_v0.59.docx" download>Word</a></div></article>
      </div><div className="schemaDownloads"><a href="/interaction_environment.schema.yaml" download>Interaction protocol ↓</a><a href="/interaction_demo_case.json" download>Runnable demo case ↓</a><a href="/interaction_env_manifest.json" download>Package manifest ↓</a><a href="/interaction_env_README.md" download>Python guide ↓</a><a href="/plhkw_task_catalog.html">60-family catalog →</a><a href="/plhkw_tasks_60.md" download>60 full prompts ↓</a><a href="/plhkw_selected_tasks.jsonl" download>Selected 60 JSONL ↓</a><a href="/plhkw_paper_first_12.csv" download>Paper-first 12 CSV ↓</a><a href="/plhkw_selected_tasks.csv" download>Selected 60 CSV ↓</a><a href="/DeepAlign-Bench_PLHKW任务资源池_v0.59.svg" download>Task-pool figure SVG ↓</a><a href="/credamo_persona_collection.protocol.yaml" download>Credamo protocol ↓</a><a href="/credamo_question_bank.json" download>92-question bank ↓</a><a href="/credamo_task_cards.jsonl" download>60 task cards ↓</a><a href="/credamo_routing_matrix.jsonl" download>Routing matrix ↓</a><a href="/credamo_quality_rules.json" download>QC rules ↓</a><a href="/human_ground_truth.protocol.yaml" download>Human truth protocol ↓</a><a href="/counterfactual_difference_map.schema.yaml" download>CDM schema ↓</a><a href="/judge_qualification.protocol.yaml" download>D-JQS protocol ↓</a><a href="/case.schema.yaml" download>Case schema ↓</a><a href="/DeepAlign-Bench_真人真值到D-JQS_v0.55.svg" download>可编辑 SVG ↓</a><a href="/PROJECT_MEMORY.md" download>项目记忆 ↓</a></div></div></section>

      <footer className="closing"><div className="shell closingGrid"><div><p className="eyebrow">CLAIM BOUNDARY</p><h2>三个代表性场景，不是所有知识工作</h2></div><p>不声称模型内部真正理解用户；不把 60 个 provisional shells 写成 60 个 runnable gold；不把显式约束跟随冒充完整个性化。</p></div></footer>
    </main>
  );
}
