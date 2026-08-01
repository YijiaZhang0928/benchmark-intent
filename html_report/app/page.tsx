import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "DeepAlign-Bench｜研究汇报",
  description: "长程 Deep Research 智能体个性化最终交付物评测方案",
};

const sources = [
  ["OpenCompass", "评测工程解耦：配置、任务切分、运行、评估与汇总", "https://arxiv.org/abs/2605.19276"],
  ["Agent-SafetyBench", "结果类别 × 失败机制的双层 taxonomy", "https://arxiv.org/abs/2412.14470"],
  ["PDR-Bench", "最直接前作：真实 persona + PQR；也是本项目要超越的基线", "https://arxiv.org/abs/2509.25106"],
  ["PaperBench", "层级原子 rubric；评委也需要独立 benchmark", "https://openai.com/index/paperbench/"],
  ["Mind2Web 2", "树状 rubric 与 Agent-as-a-Judge", "https://arxiv.org/abs/2506.21506"],
  ["LiveResearchBench", "日常、企业、学术任务与实时 DeepEval", "https://arxiv.org/abs/2510.14240"],
  ["ResearchRubrics", "任务复杂度：概念广度 × 逻辑嵌套 × 探索性", "https://arxiv.org/abs/2511.07685"],
  ["LiveDRBench", "以搜索 fan-out 与非平凡推理定义 Deep Research", "https://arxiv.org/abs/2508.04183"],
  ["AssistantBench", "从真实用户与专业工作收集耗时 web 任务", "https://arxiv.org/abs/2407.15711"],
  ["HELM", "先枚举场景与指标空间，再按覆盖与可行性选择子集", "https://arxiv.org/abs/2211.09110"],
  ["CheckList", "用能力 × 测试类型矩阵组织行为测试", "https://aclanthology.org/2020.acl-main.442/"],
  ["BetterBench", "从设计到维护的 benchmark 生命周期质量检查", "https://arxiv.org/abs/2411.12990"],
  ["BenchmarkCards", "标准化记录目标、方法、来源、限制与适用范围", "https://papers.neurips.cc/paper_files/paper/2025/hash/76175f4355e2f67cf91be468c8860070-Abstract-Datasets_and_Benchmarks_Track.html"],
];

const failures = [
  ["获取/澄清失败", "缺少必要信息时既未获取，也未澄清"], ["无依据推断", "编造用户属性或使用人口刻板印象"],
  ["检索/相关性失败", "漏取正确事实，或取回错误、无关信息"], ["已知约束忽略", "预算、权限或格式已知却未落实"],
  ["冲突/更新失败", "新旧信息冲突时仍选择过期事实"], ["利用失败", "能复述用户事实，却没有落实到交付物"],
  ["无关/过度个性化", "在不应变化处强行适配或迎合"], ["隐私/权限失败", "越权访问或不必要披露敏感信息"],
  ["保持/交接失败", "长程执行或子 agent 交接后丢失约束"], ["恢复失败", "发现偏离或被纠正后仍未修复"],
];

export default function Home() {
  return (
    <main>
      <header className="hero" id="top">
        <nav className="nav shell" aria-label="主导航">
          <a className="brand" href="#top">DeepAlign<span>Bench</span></a>
          <div className="navlinks">
            <a href="#design">设计</a><a href="#spec">四个对象</a><a href="#metrics">指标</a><a href="#scope">评测边界</a><a href="#review">审稿防守</a>
          </div>
          <a className="navCta" href="#editions">选择阅读版本</a>
        </nav>
        <div className="heroGrid shell">
          <section>
            <p className="eyebrow">RESEARCH PROPOSAL · BENCHMARK / EVALUATION</p>
            <h1>评估 Deep Research 的下一步：<em>是否真的适合这个用户</em></h1>
            <p className="lede">固定任务与证据，只改变目标用户。只有匹配用户的交付物在反事实交换中仍占优，同时不牺牲事实性、任务质量与隐私，才能称为真正个性化。</p>
            <div className="heroActions">
              <a className="button primary" href="#overview">快速读懂方案</a>
              <a className="button ghost" href="/DeepAlign-Bench_正式研究Proposal.docx" download>Word 完整版</a>
            </div>
            <div className="heroMeta"><span>5 个元数据平面</span><span>24 个任务 family</span><span>48 个 user-task</span><span>8 周论文锁定版</span></div>
          </section>
          <aside className="thesisCard">
            <span className="cardKicker">一句话研究目标</span>
            <p>测量长程智能体能否从多种用户信息中形成正确用户模型，在执行干扰中持续使用它，并在偏离后恢复。</p>
            <hr />
            <div className="thesisFlow"><b>形成</b><i>→</i><b>保持</b><i>→</i><b>利用</b><i>→</i><b>恢复</b></div>
          </aside>
        </div>
      </header>

      <section className="decision shell" id="overview">
        <p className="sectionTag">EXECUTIVE READOUT</p>
        <div className="sectionHead"><h2>导师先看这三件事</h2><p>这三项决定项目是否具备独立论文贡献，而不只是更大规模的数据集。</p></div>
        <div className="decisionGrid">
          <article><span>01</span><h3>元数据是实验骨架</h3><p>任务、环境、用户状态、信号渠道和 agent 系统共同定义一个 case；coverage manifest 明确测了什么、缺什么。</p></article>
          <article><span>02</span><h3>反事实识别</h3><p>同任务、同证据、不同用户；将报告交换评分，排除篇幅、文风与“信息更多”这些替代解释。</p></article>
          <article><span>03</span><h3>Rubric 由元数据编译</h3><p>统一的是叶节点 schema、适用条件和校准程序，而不是强迫所有任务共用一张总体评分表。</p></article>
        </div>
      </section>

      <section className="editionSection" id="editions">
        <div className="shell">
          <p className="sectionTag">FOUR READING EDITIONS</p>
          <div className="sectionHead"><h2>同一套方法，按阅读场景分成四版</h2><p>没有删改研究逻辑、实验设计、rubric、metrics 或 judge；只调整结构、语言密度和细节层级。</p></div>
          <div className="editionGrid">
            <article>
              <span>METHOD BASELINE</span><h3>正式研究 Proposal</h3><p>方法学底稿。保留完整文献论证、实验细节、统计边界和参考文献，适合精读与写论文。</p>
              <div className="editionLinks"><a href="/DeepAlign-Bench_正式研究Proposal.pdf" download>PDF</a><a href="/DeepAlign-Bench_正式研究Proposal.docx" download>Word</a></div>
            </article>
            <article className="recommended">
              <span>CONDENSED PROPOSAL · 10 PAGES</span><h3>正式 Proposal 精简版</h3><p>按标准论文 Proposal 结构保留摘要、研究问题与假设、方法、实验、统计、效度风险、时间表和参考文献。</p>
              <div className="editionLinks"><a href="/DeepAlign-Bench_正式Proposal精简版.pdf" download>PDF</a><a href="/DeepAlign-Bench_正式Proposal精简版.docx" download>Word</a></div>
            </article>
            <article>
              <span>PLAIN LANGUAGE · 18 PAGES</span><h3>完整人话版</h3><p>逻辑、内容和方法与正式版一致，把抽象句改成“问题—做法—判定标准—风险”的直白表达。</p>
              <div className="editionLinks"><a href="/DeepAlign-Bench_完整人话版.pdf" download>PDF</a><a href="/DeepAlign-Bench_完整人话版.docx" download>Word</a></div>
            </article>
            <article>
              <span>ADVISOR BRIEF · 10 PAGES</span><h3>汇报精简版</h3><p>15–20 分钟讲清研究问题、反事实设计、数据规模、评分方法、八周范围与导师待决策项。</p>
              <div className="editionLinks"><a href="/DeepAlign-Bench_汇报精简版.pdf" download>PDF</a><a href="/DeepAlign-Bench_汇报精简版.docx" download>Word</a></div>
            </article>
          </div>
        </div>
      </section>

      <section className="figureSection" id="design">
        <div className="shell">
          <div className="sectionHead light"><h2>一张图看懂 DeepAlign-Bench</h2><p>从 Evaluation Atlas、反事实任务族和跨 agent 运行，到元数据驱动 rubric 与级联评估。</p></div>
          <figure><img src="/DeepAlign-Bench_主图.png" alt="DeepAlign-Bench 总体流程图" /><figcaption>主榜先检查共同任务质量与事实性，再比较个性化；禁止“迎合换分”。</figcaption></figure>
        </div>
      </section>

      <section className="classificationSection" id="classification">
        <div className="shell">
          <p className="sectionTag">DEEP RESEARCH EVALUATION ATLAS</p>
          <div className="sectionHead"><h2>先定义可组合的 DR 元数据宇宙，再选择两个月能回答的组合</h2><p>宏大性来自机器可读 ontology、coverage manifest 和可扩展测试算子，不来自不可完成的全笛卡尔积。</p></div>
          <div className="atlasGrid">
            {[
              ["A","Research Task","使用情境 · 意图 · 领域 · 交付物 · demand · stakes"],
              ["B","Research Environment","frozen/live/private evidence · freshness · tools · budget · permissions"],
              ["C","Task-conditioned User State","目标 · 知识 · 约束 · 偏好 · 风险 · 受众 · 动态状态"],
              ["D","User-signal Channel","brief · persona · clarification · history · behavior · workspace · feedback"],
              ["E","Agent System","model/product · search · memory · planning · multi-agent · tool access"],
            ].map(([id,title,body])=><article key={id}><b>{id}</b><h3>{title}</h3><p>{body}</p></article>)}
          </div>
          <div className="operatorStrip">
            <span>行为测试算子</span>
            {[["Acquire","取得最小充分信息"],["Preserve","在噪声/冲突/交接中保持"],["Use","落实到交付物并保持不变量"],["Update / Recover","纠正或状态变化后更新"]].map(([a,b])=><div key={a}><b>{a}</b><small>{b}</small></div>)}
          </div>
          <div className="coverageManifest"><b>Coverage manifest</b><span><i>TESTED</i> 已进入主实验</span><span><i>DEFINED</i> 已定义未运行</span><span><i>N/A</i> 结构性不适用</span><span><i>DEFERRED</i> 因资源延后</span></div>
          <div className="sectionHead compactHead"><h2>Research Task 平面再用任务立方体分层</h2><p>任务类型回答“在哪类需求上测”；结果风险与失败模式回答“错在哪里、为什么错”。</p></div>
          <div className="taskCube">
            <article className="strataCard">
              <span>1 · USE CONTEXT</span><h3>使用情境，不等于难度</h3>
              <div className="strataList"><b>个人与日常</b><p>旅行、消费、学习、职业与家庭计划</p><b>专业与企业</b><p>市场、合规、采购、技术与运营决策</p><b>学术与前沿</b><p>综述、prior art、研究设计与开放咨询</p></div>
            </article>
            <article className="intentCard">
              <span>2 · RESEARCH INTENT</span><h3>六类研究意图</h3>
              <div className="intentList">{["理解与综合","发现与枚举","比较与决策","评估与预测","规划/设计/排障","验证与审计"].map((x,i)=><div key={x}><b>I{i+1}</b>{x}</div>)}</div>
            </article>
            <article className="demandCard">
              <span>3 · DEMAND PROFILE</span><h3>需求强度不压成单一难度分</h3>
              <div className="demandList">{["conceptual breadth","logical nesting","exploration","search fan-out","freshness","stakes / reversibility","interaction need"].map(x=><code key={x}>{x}</code>)}</div>
            </article>
          </div>
          <div className="classificationVerdict"><b>为什么不能只分 PhD-level / daily？</b><p>它把用户群体、领域与难度混在一起：跨国家庭旅行可能具有很高 fan-out，而博士用户也可能只做低复杂度核验。建议把二者保留为 <code>task_stratum</code>，再与研究意图和需求剖面交叉。</p></div>
          <div className="axisGrid">
            <article>
              <span>AXIS A · OUTCOME RISK</span><h3>最后错在什么地方？</h3>
              <div className="riskList">{["目标与成功标准错配","内容选择与覆盖错配","深度与知识脚手架错配","决策与风险策略错配","行动步骤与工作流错配","格式、受众与可访问性错配","隐私、安全与权限越界","动态更新与恢复失败"].map((x,i)=><div key={x}><b>R{i+1}</b><p>{x}</p></div>)}</div>
            </article>
            <article>
              <span>AXIS B · EXPECTED FAILURE MODE</span><h3>任务被设计来暴露什么机制？</h3>
              <div className="modeList">{["未获取必要用户信息，也未澄清","缺信息时编造用户属性","检索了错误或无关的用户事实","忽略已经明确给出的用户约束","未正确处理过期、冲突或动态更新","知道事实，但未落实到计划或交付物","在不应变化处过度个性化","越权使用或披露敏感信息","长上下文或子 agent 交接后丢失约束","收到纠正或重新锚定后仍未恢复"].map((x,i)=><div key={x}><b>M{i+1}</b><p>{x}</p></div>)}</div>
            </article>
          </div>
          <div className="caseSchema">
            <b>每个 case 的建议字段</b>
            <code>task.* · environment.* · user_state.* · signal.* · agent.* · operator · perturbation · eligibility_predicate · evaluation_contract · rubric_modules[] · counterfactual_partner · run/judge versions</code>
            <a href="/case.schema.yaml" download>下载机器可读 schema ↓</a>
          </div>
          <div className="taxonomyRules">
            <article><b>预期 ≠ 实际</b><p><code>expected_failure_mode</code> 是该 case 的测试意图；<code>observed_error</code> 必须由运行结果另行判断。不能因为任务标签是 M4，就默认模型一定“忽略约束”。</p></article>
            <article><b>主风险单标签，模式可多标签</b><p>为榜单统计指定一个 primary risk；failure mode 允许多个。保留 secondary risks，避免强迫复杂任务落进一个格子。</p></article>
            <article><b>标签不泄露给主 Judge</b><p>最终交付物 judge 只看 rubric 和授权事实，不看“这个任务预计模型会失败在哪里”，防止 expectation bias。</p></article>
            <article><b>taxonomy 先由真实失败归纳</b><p>先对 pilot 轨迹做 open coding，再冻结 taxonomy；保留一组自然任务和“其他/新型失败”入口，防止只验证作者预设。</p></article>
          </div>
        </div>
      </section>

      <section className="judgeChoiceSection">
        <div className="shell">
          <p className="sectionTag invert">PROMPTED JUDGE vs. SFT SCORER</p>
          <div className="sectionHead light"><h2>哪个效果更好？不能先验决定，但两个月主线必须先保住测量效度</h2><p>首版采用 verifier → 强通用 judge → 分层人评；SFT scorer 只有在第 4 周前已有足够高质量 gold 且不阻塞主实验时，才进入附录效率实验。</p></div>
          <div className="judgeCompare">
            <article><span>STRONG PROMPTED JUDGE</span><h3>适合 benchmark 初期与疑难样本</h3><ul><li>无需训练，rubric 一改即可使用</li><li>面对新领域、新交付物更灵活</li><li>可直接做证据定位与复杂解释</li></ul><p>代价：昂贵、版本变化、位置/长度/风格偏差，复现实验困难。</p></article>
            <article><span>SFT SPECIALIZED SCORER</span><h3>适合定义稳定后的规模化评分</h3><ul><li>成本低、速度快、版本可冻结</li><li>可针对每个原子 checklist 校准</li><li>可以训练拒判和边界案例</li></ul><p>代价：容易退化成 task-specific classifier；跨任务、跨 agent 和新错误分布可能明显下降。</p></article>
          </div>
          <div className="sftRecipe">
            <h3>推荐的 SFT 数据格式</h3>
            <div className="recipeFlow"><span>人工 gold label</span><i>+</i><span>人工 evidence span</span><i>+</i><span>rubric / anchor</span><i>+</i><span>GPT 草拟 reason</span><i>→</i><strong>人工抽检后 SFT</strong></div>
            <p>不要只收 <code>0/1 + GPT reason</code>。GPT 在已知 gold label 后生成的理由是“标签条件下的解释蒸馏”，不是新的 ground truth，可能学会合理化。至少加入证据位置、错误类型、置信度/弃权；对关键隐私项和争议项保留一部分人工理由。</p>
          </div>
          <div className="judgeDecision">
            <div><b>训练前</b><p>3 名人类建立叶节点 gold；强 judge 作为 baseline；按 task family、用户、agent 和时间切分，禁止同 family 泄漏。</p></div>
            <div><b>对抗测试</b><p>交换 A/B、控制长度、堆 persona 关键词、漂亮格式诱饵、事实更强但适配更弱、隐私泄露、正确弃权。</p></div>
            <div><b>上线规则</b><p>若 SFT 在跨 family 测试上超过 prompted judge 且校准达标，作为主 scorer；否则只做高置信样本分流，低置信交给强 judge/人类。</p></div>
          </div>
          <div className="winnerBanner"><span>两个月主线</span><b>Deterministic / evidence verifier → 强 Judge → 20% 分层人评 + 分歧仲裁</b><p>SFT 的理想发布架构仍是高置信分流，但它现在是条件性支线。先证明 benchmark 测到了个性化，再优化评分成本。</p></div>
          <div className="judgeSources"><a href="https://arxiv.org/abs/2310.17631" target="_blank" rel="noreferrer">JudgeLM：SFT judge 与偏差处理 ↗</a><a href="https://arxiv.org/abs/2405.01535" target="_blank" rel="noreferrer">Prometheus 2：专用 evaluator ↗</a><a href="https://arxiv.org/abs/2403.02839" target="_blank" rel="noreferrer">实证研究：SFT judge 不是 GPT-4 的通用替代 ↗</a></div>
        </div>
      </section>

      <section className="shell gapSection">
        <p className="sectionTag">NOVELTY</p>
        <div className="sectionHead"><h2>不是 PDR-Bench 的扩大版</h2><p>PDR-Bench 是最重要的直接前作；差异必须落在测量逻辑，而不是只落在规模。</p></div>
        <div className="compare" role="table" aria-label="PDR-Bench 与 DeepAlign-Bench 比较">
          <div className="compareRow head" role="row"><span>评审会问什么</span><span>PDR-Bench</span><span>DeepAlign-Bench</span></div>
          {[
            ["测到的是个性化吗？", "Task-only / context / persona 分数比较", "Matched vs. swapped 反事实优势 CFA"],
            ["rubric 从哪里来？", "LLM 动态生成权重与子标准", "输出前冻结的人类确认原子 rubric"],
            ["judge 可靠吗？", "15 个 query、两种 agent；最佳 agreement 0.43", "独立 JudgeBench + 人类门槛 + 可弃权"],
            ["用户信息真实吗？", "真实 persona，动态历史由标注员模拟", "事实 ledger：来源、时效、置信度、权限、用户确认"],
            ["任务覆盖如何解释？", "50 tasks × 10 domains", "5-plane Atlas + behavioral operators + 四状态 coverage manifest"],
            ["是否只会写长报告？", "以中英长报告为主", "报告、代码、表格、幻灯、网页和多文件交付"],
            ["能定位为什么失败吗？", "主要评价最终输出", "轨迹检查点 + 10 类失败机制 + 恢复实验"],
          ].map((r) => <div className="compareRow" role="row" key={r[0]}><b>{r[0]}</b><span>{r[1]}</span><span>{r[2]}</span></div>)}
        </div>
      </section>

      <section className="taxonomyBand">
        <div className="shell taxonomyGrid">
          <div>
            <p className="sectionTag">TAXONOMY A</p><h2>交付物应该在哪里不同？</h2>
            <div className="pillGrid">{["目标与成功定义","内容选择与覆盖","深度与知识脚手架","决策与推荐策略","行动性与工作流","呈现与交付格式","安全、隐私与边界","交互策略"].map((x,i)=><span key={x}><i>{String(i+1).padStart(2,"0")}</i>{x}</span>)}</div>
          </div>
          <div>
            <p className="sectionTag coral">TAXONOMY B</p><h2>case 被设计来暴露什么机制？</h2>
            <div className="failureGrid">{failures.map(([a,b])=><div key={a}><b>{a}</b><small>{b}</small></div>)}</div>
          </div>
        </div>
      </section>

      <section className="shell gapSection" id="spec">
        <p className="sectionTag">CURRENT SPECIFICATION</p>
        <div className="sectionHead"><h2>现在的 persona、task、rubric、judge 到底是什么？</h2><p>目前 proposal 已经定义了数据结构和评估协议，但还不是一批可直接运行的 benchmark cases；下面展示一个端到端实例应有的形态。</p></div>
        <div className="specGrid">
          <article>
            <span className="specNo">01 · PERSONA</span><h3>有证据的 user fact ledger</h3>
            <p>不是人物小传，而是 task-conditioned user state 的一种视图；“真实、不违和”只是最低门槛。</p>
            <dl><div><dt>目标</dt><dd>扩店调研用于向银行申请贷款</dd></div><div><dt>能力</dt><dd>首次创业；金融知识有限</dd></div><div><dt>约束</dt><dd>首期投入 ≤ 50 万；3 个月内可退出</dd></div><div><dt>权限</dt><dd>健康与家庭信息可用于推理，不得对银行披露</dd></div></dl>
            <small>六项门：plausibility · decision relevance · counterfactual separability · invariant core · minimality/privacy · non-stereotyping。</small>
          </article>
          <article>
            <span className="specNo">02 · TASK</span><h3>反事实任务族，不是单个 query</h3>
            <p>同一咖啡店扩张任务、同一市场证据、同一工具预算，只更换目标用户。</p>
            <div className="familyMini"><b>Ua</b><span>外行 · 低预算 · 风险规避</span><b>Ub</b><span>连锁经营者 · 高预算 · 增长导向</span><b>Uc</b><span>约束部分重叠或冲突</span><b>U0</b><span>中性控制，只保留共同要求</span></div>
            <small>同一用户事实再转换为 structured persona、自然历史、澄清对话、memory 等语义等价渠道。</small>
          </article>
          <article>
            <span className="specNo">03 · RUBRIC</span><h3>冻结的三棵原子标准树</h3>
            <p><b>Compiler</b>：core + personalization + intent + deliverable + operator + risk modules。</p><p><b>四类契约</b>：must-change · must-hold · must-not · clarify-if-unknown。</p><p><b>校准</b>：matched/swapped 区分力、无关信息 invariance、跨任务模块一致性。</p>
            <small>统一的是 leaf schema、applicability predicate 与校准程序，不是假设所有任务共享同一评分表。</small>
          </article>
          <article>
            <span className="specNo">04 · JUDGE</span><h3>逐层核验，不打整体印象分</h3>
            <ol><li>确定性检查文件、测试、预算与权限</li><li>核验 claim、引用支持与来源质量</li><li>按冻结叶节点逐项给分并引用证据</li><li>匿名 A/B 比较，随机交换位置</li><li>目标用户判断适用性，专家判断专业正确性</li></ol>
            <small>Judge 只获得与该叶节点相关且获授权的用户事实；证据不足必须允许弃权。</small>
          </article>
        </div>
        <div className="statusNote"><b>两个月锁定范围</b><span>24 个 family、48 个强对比 user-task、四个核心信号条件、三类核心 agent；8 个 anchor family 承担错配、无关、冲突/过期、长程和动态测试。120-task 扩展与 SFT scorer 不阻塞主论文。</span></div>
      </section>

      <section className="rubricCompilerSection">
        <div className="shell">
          <p className="sectionTag invert">METADATA-DRIVEN RUBRIC COMPILER</p>
          <div className="sectionHead light"><h2>不是一张 rubric 服务所有任务，而是一套模块接口服务所有测试类型</h2><p>Atlas 决定哪些模块适用；每个叶节点都声明 applicability、预期方向、证据目标、评分锚点、硬门槛和 verifier。</p></div>
          <div className="compilerFormula"><span>CORE</span><i>+</i><span>PERSONALIZATION</span><i>+</i><span>INTENT</span><i>+</i><span>DELIVERABLE</span><i>+</i><span>OPERATOR</span><i>+</i><span>RISK</span><b>→ R(case)</b></div>
          <div className="contractGrid">
            <article><b>MUST CHANGE</b><p>用户差异必须改变的内容、决策、深度、行动或披露边界。</p></article>
            <article><b>MUST HOLD</b><p>共同事实、证据质量与不应因用户改变的核心结论。</p></article>
            <article><b>MUST NOT</b><p>不得假设、泄露、越权或为迎合偏好而扭曲的内容。</p></article>
            <article><b>CLARIFY IF UNKNOWN</b><p>缺少关键信息时必须提问、给条件分支或显式说明假设。</p></article>
          </div>
          <div className="calibrationGates"><b>四个校准门</b><span>metadata schema coverage</span><span>matched &gt; swapped discrimination</span><span>irrelevant-persona invariance</span><span>cross-type judge calibration</span></div>
        </div>
      </section>

      <section className="shell gapSection" id="metrics">
        <p className="sectionTag">METRICS</p>
        <div className="sectionHead"><h2>先过共同质量门槛，再谈个性化</h2><p>事实错误、任务失败或隐私违规，不能被“看起来懂用户”补偿。</p></div>
        <div className="metricGrid">
          <article className="blue"><span>TQ / FR</span><h3>共同质量与事实性</h3><p>任务完成、关键覆盖、claim 支持、引用覆盖与来源质量。</p></article>
          <article className="green"><span>PF − MP</span><h3>净个性化适配</h3><p>用户特异要求完成率，扣除刻板化、误用、隐私和过度迎合。</p></article>
          <article className="violet"><span>CFA</span><h3>反事实适配优势</h3><p>匹配报告相对交换报告，在两个用户方向上取得的平均优势。</p></article>
          <article className="amber"><span>AUC / Δ</span><h3>保持与恢复</h3><p>长程干扰下的适配曲线、漂移半衰期、恢复收益与副作用。</p></article>
        </div>
        <div className="formula"><div><span>核心公式</span><strong>CFA(a,b) = ½[(PFₐ(Yₐ) − PFₐ(Yᵦ)) + (PFᵦ(Yᵦ) − PFᵦ(Yₐ))]</strong></div><p>CFA &gt; 0 才表示“对的人得到对的版本”，而不是所有版本都变得更长、更漂亮。</p></div>
      </section>

      <section className="judgeSection" id="judge">
        <div className="shell">
          <p className="sectionTag invert">RUBRIC & JUDGE</p>
          <div className="sectionHead light"><h2>三棵 rubric tree，四层评估</h2><p>将共同质量、用户条件适配和误用边界拆开，避免循环定义和维度补偿。</p></div>
          <div className="judgeLayout">
            <div className="rubricTrees">
              <article><span>A</span><h3>Common Task Quality</h3><p>任务、事实、证据、推理、行动性、交付完整性。</p></article>
              <article><span>B</span><h3>User-Conditional Fit</h3><p>目标、内容、深度、约束、工作流、动态状态。</p></article>
              <article><span>C</span><h3>Misuse & Boundary</h3><p>刻板化、无关适配、过期信息、隐私与过度迎合。</p></article>
            </div>
            <div className="judgeSteps">
              {[ ["L0","确定性 verifier","文件、测试、格式、预算、权限与硬约束"], ["L1","证据 verifier","claim、引用支持、关联与来源质量"], ["L2","冻结原子 rubric judge","逐项证据、匿名来源、位置轮换、允许弃权"], ["L3","目标用户 + 领域专家","用户效用与专业正确性分开判断"] ].map(x=><div key={x[0]}><span>{x[0]}</span><p><b>{x[1]}</b><small>{x[2]}</small></p></div>)}
            </div>
          </div>
          <div className="judgeGate"><b>Judge 上线门槛</b><span>Pairwise accuracy ≥ .75</span><span>α / κ ≥ .60</span><span>位置翻转率 ≤ .05</span><span>群体差距 ≤ .10</span><span>不达标 → 人评或降级指标</span></div>
        </div>
      </section>

      <section className="scopeSection" id="scope">
        <div className="shell">
          <p className="sectionTag">MEASUREMENT BOUNDARY</p>
          <div className="scopeHero"><div><h2>最终交付物可以做主榜，但不能支撑所有过程性主张</h2><p>如果论文只声称“输出是否真正适合这个用户”，最终交付物足够；如果声称测到了形成、保持、利用、漂移和恢复，只看最后报告无法识别原因。</p></div><strong>推荐：Outcome Core + 轻量 Trace Audit + 小规模 Diagnostic Track</strong></div>
          <div className="enoughGrid">
            <article className="yes"><span>FINAL-ONLY 可以回答</span><ul><li>报告、代码或网页是否适合目标用户</li><li>matched 是否优于 swapped</li><li>个性化是否牺牲事实与共同质量</li><li>是否出现刻板化、泄露或过度迎合</li></ul></article>
            <article className="no"><span>FINAL-ONLY 不能回答</span><ul><li>根本没读取，还是执行中忘记</li><li>记得用户事实，但生成时没使用</li><li>旧信息、新反馈冲突时如何选择</li><li>子 agent 交接何时丢失约束</li><li>重新锚定后能否真正恢复</li></ul></article>
          </div>
          <div className="trackStack">
            <article><b>A · Outcome Core</b><span>全部样本</span><p>只把最终交付物作为主榜对象：TQ、FR、PF、MP、NPF、CFA 和目标用户盲评。</p></article>
            <article><b>B · Passive Trace Audit</b><span>全部样本自动记录</span><p>保存工具调用、检索到的用户事实、权限访问和子 agent 交接；只对隐私、权限和不可逆行为设硬检查。</p></article>
            <article><b>C · Diagnostic Track</b><span>20%–30% 子集</span><p>不逐句人工标注；用中点 probe、memory 有无、handoff 有无、re-anchor 前后等受控重跑识别保持与恢复。</p></article>
          </div>
          <div className="claimRule"><b>论文写作红线</b><p>若采用严格 final-only 方案，应删除或降级 RQ3、RQ5、H2–H4；10 类预期失败模式只能称为“测试意图或假设性误差来源”，不能声称已经测量到具体偏移机制。</p></div>
        </div>
      </section>

      <section className="agentSafetyBand">
        <div className="shell">
          <p className="sectionTag invert">WHAT AGENT-SAFETYBENCH ACTUALLY DOES</p>
          <div className="sectionHead light"><h2>它不是“attack 分类后只看最终回复”</h2><p>核心结构是风险结果类别 × 预期失败模式 × 动态工具环境；scorer 阅读完整交互记录，而不是只读最后一句。</p></div>
          <div className="asbStats"><div><b>349</b><span>交互环境</span></div><div><b>2,000</b><span>测试案例</span></div><div><b>8</b><span>风险类别</span></div><div><b>10</b><span>失败模式</span></div><div><b>16</b><span>被测 agents</span></div></div>
          <div className="asbGrid">
            <article><h3>八类风险结果</h3><p>泄露敏感信息 · 财产损失 · 传播错误/危险信息 · 身体伤害 · 违法/伦理 · 破坏可用性 · 有害/脆弱代码 · 直接生成危险信息</p></article>
            <article><h3>十类失败模式</h3><p>直接生成有害内容 · 信息不足就调用 · 未先补全信息 · 忽略已知约束 · 忽略潜在风险 · 参数错误 · 忽略工具风险 · 漏用必要工具 · 盲信工具结果 · 多候选中选错</p></article>
            <article><h3>一个 case 的字段</h3><p>risk category · instruction/dialogue · environment/tools/init parameters · anticipated failure modes</p></article>
            <article><h3>实际评分对象</h3><p>环境信息 + 全部对话 + 工具调用及参数 + 工具返回 + 最终回复 → safe / unsafe；总分是 safe case 比例。</p></article>
          </div>
          <div className="scorerFlow"><span>4,000 条人工标注交互</span><i>→</i><span>Qwen-2.5-7B scorer</span><i>→</i><span>200 条独立交互测试</span><b>91.5% accuracy</b></div>
          <div className="asbLesson"><b>对我们的直接启示</b><p>可以像它一样给每个 case 标注“预期失败模式”，并按这些切片报告表现；但这不等于精确定位每个 agent 的认知偏移时刻。DeepAlign-Bench 的主榜仍应评最终效用，轨迹只承担行为审计和机制诊断。</p><a href="https://arxiv.org/abs/2412.14470" target="_blank" rel="noreferrer">阅读 Agent-SafetyBench 原文 ↗</a></div>
        </div>
      </section>

      <section className="shell gapSection">
        <p className="sectionTag">EXPERIMENTS</p>
        <div className="sectionHead"><h2>两个月分数因子矩阵：不跑全笛卡尔积</h2><p>所有 case 都完整标注 Atlas；只有能回答主假设的高信息量组合进入实验，受控 harness 与端到端产品结果分开。</p></div>
        <div className="matrix">
          <article><b>核心信号条件</b><p>Task only · structured persona · 语义等价自然历史 · clarification-allowed</p></article>
          <article><b>8 个 anchor 压测</b><p>错配 · 无关属性 · 冲突/过期 · context dilution · dynamic update</p></article>
          <article><b>三类核心 Agent</b><p>商业 Deep Research · 统一搜索/工具 harness · 可复现开源 Deep Research</p></article>
          <article><b>适用性探针</b><p>代码、多 agent、memory 系统只运行 eligibility predicate 为真的 anchor family</p></article>
        </div>
        <div className="pilot"><span>PAPER SCOPE · 8 周</span><div><b>24</b><small>任务 family</small></div><div><b>48</b><small>核心 user-task</small></div><div><b>4</b><small>核心信号条件</small></div><div><b>3</b><small>核心 Agent</small></div><p>最多 576 个核心 episode；8 个 anchor family 加压力测试，约 20% 分层样本复跑第二 seed，并做人评。</p></div>
      </section>

      <section className="reviewBand" id="review">
        <div className="shell">
          <p className="sectionTag coral">REVIEWER RED TEAM</p>
          <div className="sectionHead"><h2>顶会审稿人最可能怎么攻击？</h2><p>每个防守都必须转化为可运行的实验，而不是只写在 limitations 里。</p></div>
          <div className="accordions">
            {[
              ["“这只是 PDR-Bench 扩大版。”","锁定三项独立贡献：反事实任务族与 CFA；长程漂移/恢复诊断；独立 JudgeBench。任务规模只服务外部效度。"],
              ["“Persona 是作者编的偏见。”","用户事实必须有来源、时效和本人确认；人口属性不自动推导偏好；加入 demographic-only 与无关 persona 负对照。"],
              ["“个性化分只是长度和关键词。”","加入长度匹配、persona 关键词堆砌诱饵、matched/swapped 交换和 Neutral Invariance。"],
              ["“LLM judge 循环定义答案。”","rubric 在输出前冻结；规则和证据核验优先；低一致性时降级到人评，不发布伪精确榜单。"],
              ["“PhD / daily 标签主观且混淆难度。”","把二者只作为使用情境；另标研究意图、breadth、nesting、exploration、fan-out、freshness 与 stakes，并发布映射和盲标一致性。"],
              ["“元数据很多，实际覆盖却很稀疏。”","公开 tested / defined-only / structurally-inapplicable / deferred 四状态 manifest；只对 tested 组合做结论，不用 ontology 大小冒充样本覆盖。"],
              ["“Persona 真实不等于 gold 正确。”","persona 只是 task-conditioned ledger 的视图；必须通过六项 compatibility gate，并由用户确认 must-change / must-hold 差异。"],
              ["“不同模块 rubric 的百分比分数不可比。”","统一 leaf schema 和校准程序；以任务内 CFA 与模块 profile 为主，未通过共同 anchor 校准时不建立伪精确总榜。"],
              ["“长程漂移只是整体能力下降。”","设置同长度共同约束对照；只有用户特异要求下降更快、且重锚定选择性恢复 PF，才支持漂移解释。"],
              ["“个性化会制造回音室或隐私风险。”","事实性硬门槛、Misuse Penalty、敏感信息最小使用和受众权限共同构成不可补偿约束。"],
            ].map(([q,a],i)=><details key={q} open={i===0}><summary><span>{String(i+1).padStart(2,"0")}</span>{q}</summary><p>{a}</p></details>)}
          </div>
        </div>
      </section>

      <section className="shell gapSection sources">
        <p className="sectionTag">READING NOTES</p>
        <div className="sectionHead"><h2>关键文献：分别借什么、不借什么</h2><p>LivingBench 的动态设计作为灵感；其公开证据目前主要来自产品技术文章，不作为未经审计的金标准。</p></div>
        <div className="sourceGrid">{sources.map(([a,b,c])=><a href={c} target="_blank" rel="noreferrer" key={a}><b>{a}</b><p>{b}</p><span>查看原始来源 ↗</span></a>)}</div>
      </section>

      <section className="closing">
        <div className="shell closingGrid">
          <div><p className="sectionTag invert">DECISION NEEDED</p><h2>建议导师优先拍板</h2></div>
          <ol><li>是否把 Evaluation Atlas、coverage manifest 和 rubric compiler 定为核心贡献，而不是承诺跑遍所有组合？</li><li>是否锁定 24 family、48 user-task、四个信号条件和三类核心 agent 的八周矩阵？</li><li>SFT scorer 是否明确为不阻塞主论文的可选附录？</li><li>代码、多 agent 与动态用户是否只进入 8 个 anchor family？</li></ol>
        </div>
      </section>

      <footer><div className="shell"><a className="brand" href="#top">DeepAlign<span>Bench</span></a><p>Research proposal · v0.14 · 2026-08-02</p><div><a href="#editions">四个版本</a><a href="/DeepAlign-Bench_主图.png" download>主图</a></div></div></footer>
    </main>
  );
}
