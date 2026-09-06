const papers = [
  ["[1] PDR-Bench", "task + full structured persona；full-context personalization bridge", "https://arxiv.org/abs/2509.25106"],
  ["[2] G-STEER", "retrieve / ask / stop 的策略邻居；必须做增量新颖性对照", "https://arxiv.org/abs/2608.05876"],
  ["[3] IDRBench", "interactive deep-research 邻居；提醒我们不能把多问等同于问得准", "https://arxiv.org/abs/2601.06676"],
  ["[4] IntentRL", "主动意图澄清的训练邻居", "https://arxiv.org/abs/2602.03468"],
  ["[5] DiscoBench", "需求发现与 specification benchmark 邻居", "https://arxiv.org/abs/2606.27669"],
];

const selectedTaskGroups = [
  ["Education · 3", "1 AI PhD · 4 MBA/EMBA/Data Analytics · 5 论文投稿"],
  ["Career · 3", "6 转入金融 · 9 AI 产品经理 · 10 国际职业路径"],
  ["Health / Travel · 2", "11 健身 · 16 东南亚背包旅行"],
  ["Finance · 2", "21 个人投资 · 22 退休保障"],
  ["Creative / Shopping · 3", "30 个人媒体 · 33 宠物用品 · 35 户外装备"],
  ["Real Estate / Parenting · 2", "39 养老房 · 49 亲子沟通"],
];

export default function Home() {
  return (
    <main>
      <header className="hero" id="top">
        <nav className="nav shell" aria-label="主导航">
          <a className="brand" href="#top">Ask<span>Infer</span>Bench</a>
          <div className="navlinks"><a href="#question">问题</a><a href="#task-slice">50→15</a><a href="#design">双轨</a><a href="#delta">δ</a><a href="#metrics">评分</a><a href="#pilot">Pilot</a></div>
          <a className="navCta" href="#editions">下载文档</a>
        </nav>
        <div className="heroGrid shell">
          <section>
            <p className="eyebrow">RESEARCH PROPOSAL · v0.66 · 2026-09-06</p>
            <h1>Ask or Infer?<br/><em>任务特异的个性化</em></h1>
            <p className="lede">用户在线时，agent 能否用少量问题获取真正改变交付物的偏好？用户离线时，它能否从授权 history 恢复可识别偏好，并对未知部分保持克制？</p>
            <div className="heroActions"><a className="button primary" href="#design">看整体框架</a><a className="button ghost" href="/AskInfer-Bench_正式Proposal精简版.pdf" download>下载正式精简版</a></div>
            <div className="heroMeta"><span>Ask · Research / Coding / Data</span><span>Infer · Deep Research</span><span>δ = 0 / low / high</span><span>One primary artifact</span></div>
          </section>
          <aside className="thesisCard"><span className="cardKicker">核心识别问题</span><p>agent 问了多少不是重点；重点是它是否在会改变 evidence、实现、指标与结论的地方问，并把答案真正用进交付物。</p><hr/><div className="thesisFlow"><b>Unknown</b><i>→</i><b>Acquire</b><i>→</i><b>Use</b></div></aside>
        </div>
      </header>

      <section className="decision shell" id="question">
        <p className="sectionTag">CONSTRUCT BOUNDARY</p>
        <div className="sectionHead"><h2>把三种不同的信息条件分开</h2><p>PDR-Bench 的主要设定给 agent task + full structured persona，因此是 full-context personalization，不是 implicit elicitation。<a href="https://arxiv.org/abs/2509.25106" target="_blank" rel="noreferrer">[1]</a></p></div>
        <div className="decisionGrid">
          <article><span>ASK</span><h3>偏好缺失、用户在线</h3><p>同一裁减 history；允许低负担澄清。比较 agent 是否找到高影响未知项、及时停止，并把回答落实到交付物。</p></article>
          <article><span>INFER</span><h3>自然 history、用户离线</h3><p>只从授权证据恢复 task-relevant preferences。真正不可识别时，保守默认、显式分支或不确定性优于猜测。</p></article>
          <article><span>BRIDGE</span><h3>完整 persona 已提供</h3><p>复用 PDR-style Deep Research slice，测在同版本、同预算、同工具下的 full-context personalization，并检验排名稳定性。</p></article>
        </div>
      </section>

      <section className="classificationSection" id="task-slice"><div className="shell">
        <p className="sectionTag">PDR TASK QUALIFICATION · 50 → 15</p>
        <div className="sectionHead"><h2>按个性化诊断价值筛，不按 domain 配额抽</h2><p>上游 complexity、clarity、alignment 之外，再问：用户差异是否会改变研究内容、约束、证据或结论，而不只是措辞。<a href="https://arxiv.org/abs/2509.25106" target="_blank" rel="noreferrer">[1]</a></p></div>
        <div className="decisionGrid">
          <article><span>LEVERAGE = 2</span><h3>实质研究决定会改变</h3><p>候选集合、evidence scope、约束、阈值、推荐或结论必须发生可验证变化；0/1 题不进 primary slice。</p></article>
          <article><span>HARD GATES</span><h3>history、nodes 与冲突都过门</h3><p>history 可取证、2–4 个 preference dimensions、真正 DR；年龄/性别/职业标签不算偏好，排除人口 token 投射和高风险 task–profile 矛盾。</p></article>
          <article><span>ANTI-CHERRY-PICK</span><h3>先筛题，再跑 agent</h3><p>两名人类盲化复标；A/B pair 另审。禁止使用 PDR 分数、新模型输出或预期 rank reversal 换题。</p></article>
        </div>
        <div className="compare" role="table" aria-label="PDR 15 个入选任务" style={{marginTop: "22px"}}>
          <div className="compareRow head" role="row"><span>入选分组</span><span>官方 task IDs 与主题</span><span>解释</span></div>
          {selectedTaskGroups.map(([group, tasks]) => <div className="compareRow" role="row" key={group}><b>{group}</b><span>{tasks}</span><span>分布是 screening output，不是 quota。</span></div>)}
        </div>
        <div className="classificationVerdict"><b>15 tasks · 9 domains · 76 official bridge pairs</b><p>公开 task 10 有 6 位用户，所以不是机械的 75 pairs。当前仍是 provisional author screen；每题 task gate、A/B pair、2–4 nodes 和 natural-history evidence 还要分别完成人工 qualification。Finance/Health/Real Estate 另过专家安全与可行性门，儿童状态不能从年龄单独推断。</p></div>
        <div className="schemaDownloads"><b>筛选资产</b><a href="/pdr_screening_50.csv" download>50 题全表 ↓</a><a href="/pdr_selection_protocol.yaml" download>筛选协议 ↓</a><a href="/pdr_selected_15.jsonl" download>15 题 JSONL ↓</a><a href="/pdr_selected_15.md" download>人类清单 ↓</a></div>
      </div></section>

      <section className="figureSection" id="design"><div className="shell"><div className="sectionHead light"><h2>任务先 qualification；过程与结果再分开测</h2><p>PDR 50→15 后冻结人类可审计的决策节点，再运行 Ask / Infer；CFA 只评价最终交付物，不替代提问校准。</p></div><figure><img src="/AskInfer-Bench_评测框架_v0.62.png" alt="AskInfer-Bench v0.62：PDR 50→15、Ask 与 Infer 双轨、过程指标和最终交付物评分"/><figcaption>v0.62：task screen 与 A/B pair 是两层独立 qualification；LLM 只辅助扩充候选，critical nodes 由真人确认。</figcaption></figure></div></section>

      <section className="shell gapSection" id="delta">
        <p className="sectionTag">PRE-RUN DELIVERABLE IMPACT</p>
        <div className="sectionHead"><h2>δ 不是“persona 看起来差很多”</h2><p>δ 在 agent 运行前按预期交付物后果冻结，避免先看模型表现再把差异解释成高价值偏好。</p></div>
        <div className="decisionGrid">
          <article><span>δ = 0</span><h3>交付物应保持不变</h3><p>差异与当前任务无关；询问会增加负担，采用会构成过度个性化。</p></article>
          <article><span>δ = LOW</span><h3>只改非关键呈现</h3><p>经人类确认会改变长度、注释密度或格式，但不改变核心证据、算法、指标、结论和风险边界。</p></article>
          <article><span>δ = HIGH</span><h3>改变关键决策</h3><p>应改变 evidence set、算法/接口、指标定义、分析切片、结论、受众决策或风险处理。</p></article>
        </div>
        <div className="classificationVerdict"><b>Ask Calibration Under Preference Divergence</b><p>理想 agent 在 high-δ 未知项上高召回，在 low/zero-δ 上少打扰。主要检验是 node-level mixed model，不是问题数与 δ 的简单相关，也不是 CFA。</p></div>
      </section>

      <section className="classificationSection" id="conditions"><div className="shell">
        <p className="sectionTag">CONTROLLED CONDITIONS</p>
        <div className="sectionHead"><h2>Ask 测获取；Infer 测证据约束的恢复</h2><p>所有条件固定 task、workspace/evidence、tools、版本、预算、时间窗与一个主要交付物。</p></div>
        <div className="compare" role="table" aria-label="Ask 与 Infer 条件">
          <div className="compareRow head" role="row"><span>轨道</span><span>条件</span><span>识别作用</span></div>
          <div className="compareRow" role="row"><b>Ask</b><span>A0 No-Ask · A1 Ask-enabled · A2 task-specific oracle</span><span>拆出提问的增益、上限与用户 burden</span></div>
          <div className="compareRow" role="row"><b>Infer</b><span>I0 task-only · I1 natural history · I2 oracle · I3 PDR full persona</span><span>拆出 history 证据增益、oracle 缺口与 PDR bridge</span></div>
          <div className="compareRow" role="row"><b>History nodes</b><span>recoverable · missing_askable · unidentifiable · irrelevant</span><span>不把不可识别节点强迫成 persona guessing</span></div>
        </div>
      </div></section>

      <section className="shell gapSection" id="metrics">
        <p className="sectionTag">PROCESS → ARTIFACT</p>
        <div className="sectionHead"><h2>既看问到什么，也看答案有没有改变交付物</h2><p>过程链逐节点审计：unknown → asked → answered → planned → artifact-evidenced → decision-changed。</p></div>
        <div className="decisionGrid">
          <article><span>PROCESS</span><h3>Ask 校准</h3><p>high-δ recall、question precision、low/zero-δ question rate、first-critical rank、stopping error 与 burden。</p></article>
          <article><span>OUTCOME</span><h3>非补偿门</h3><p>绝对 adequacy、相对 A0/I0 增益、共同质量 no-harm、事实/测试、边界零严重违规与真人/可执行结果。</p></article>
          <article><span>SPECIFICITY</span><h3>matched / swapped CFA</h3><p>ΔA、ΔB、CFA_mean 与 CFA_min 只衡量 final artifact 是否对两位用户双向正确改变。</p></article>
        </div>
        <div className="formula">ΔA = PF_A(Y_A) − PF_A(Y_B)<br/>ΔB = PF_B(Y_B) − PF_B(Y_A)<br/>CFA_min = min(ΔA, ΔB)</div>
      </section>

      <section className="reviewBand" id="pilot"><div className="shell">
        <p className="sectionTag">NOVELTY-KILL PILOT</p>
        <div className="sectionHead"><h2>先验证操纵与测量，不急着发榜</h2><p>冻结 PDR-T01、PDR-T30、SW001、SW013、DA003、DA015；每题一个 A/B pair，在 node 层覆盖 high/low/zero δ。三个必跑 agent system 共 114 个唯一 episodes；条件性加入 OpenHands 后为 152。</p></div>
        <div className="decisionGrid">
          <article><span>GO 1</span><h3>δ 可复现</h3><p>盲化标注员能稳定区分 high、low、zero，并把问题一致映射到 decision nodes。</p></article>
          <article><span>GO 2</span><h3>过程解释结果</h3><p>获取并采用 high-δ 信息能预测 final matched advantage，且不只是额外 token 效应。</p></article>
          <article><span>GO 3</span><h3>增量新颖性</h3><p>相对 G-STEER/IDRBench，δ、人类 decision nodes 与 matched/swapped outcome 提供新的可复现区分。<a href="https://arxiv.org/abs/2608.05876" target="_blank" rel="noreferrer">[2]</a> <a href="https://arxiv.org/abs/2601.06676" target="_blank" rel="noreferrer">[3]</a></p></article>
        </div>
        <div className="classificationVerdict"><b>排名反转是检验，不是结论</b><p>在同一 DR slice、同版本与同预算下报告 Kendall τ、Spearman ρ、pairwise inversion matrix 与 family-cluster bootstrap；若不反转，仍报告何种能力表面稳定、何处发生局部 inversion。</p></div>
      </div></section>

      <section className="shell gapSection" id="smoke">
        <p className="sectionTag">S0 SMOKE PACK · READY</p>
        <div className="sectionHead"><h2>第一批真实 S0 已经暴露了失败链</h2><p>Codex 三题为 Research PASS、Code PASS with warning、Data FAIL：Data 没问 decision horizon，因此没有恢复两季度 weekly scale/stop。Claude 三题均在模型接收输入前因企业账户余额不足返回 HTTP 401、token 为 0，只记基础设施失败。Gemini CLI 0.46.0 已安装，仍需本人完成 Google OAuth。</p></div>
        <div className="decisionGrid">
          <article><span>S0 · NOW</span><h3>Prompt 与交互</h3><p>验证 ASK/FINAL 解析、high-δ question targeting、ledger-bounded answer、具体 decision use、trace 与 reset。</p></article>
          <article><span>S1 · NEXT</span><h3>真实环境与交付物</h3><p>绑定固定 repository/dataset，实际读写、执行测试或 notebook，并运行 objective verifier。当前四题仍是 pending。</p></article>
          <article><span>S2 · COUNTED</span><h3>双人确认后正式跑</h3><p>两名独立验证者逐 node 审核、rubric hash 与环境冻结后，episode 才能进入主表。</p></article>
        </div>
        <div className="schemaDownloads"><b>立即执行</b><a href="/s0_run_20260904/RESULTS.md" download>首轮实跑结果 ↓</a><a href="/AskInfer-Bench_S0-Smoke-README.md" download>先读这里 ↓</a><a href="/AskInfer-Bench_S0-Smoke-RUNBOOK.md" download>三系统 Runbook ↓</a><a href="/AskInfer-Bench_S0-Smoke-Manifest.json" download>运行清单 ↓</a><a href="/AskInfer-Bench_S0-Smoke-Personas.json" download>8 Personas ↓</a><a href="/AskInfer-Bench_S0-Smoke-Rubrics.json" download>Rubrics ↓</a><a href="/AskInfer-Bench_S0-Smoke-Cases.json" download>Hidden cases ↓</a><a href="/AskInfer-Bench_S0-Smoke-Scorecard.md" download>Scorecard ↓</a></div>
      </section>

      <section className="reviewBand" id="pdr-pilot"><div className="shell">
        <p className="sectionTag">PDR-T30 MINIMUM PRODUCT PILOT · COMPLETE</p>
        <div className="sectionHead"><h2>自由追问带来正增益，但只恢复 39.53%</h2><p>同一 ChatGPT Deep Research 在 User12 个人媒体任务上的盲评 P-score：Full Persona 6.703、No-Ask 5.596、Interactive 6.033。InteractiveGain 为 +0.438，OracleGap 为 0.669。</p></div>
        <div className="decisionGrid">
          <article><span>ASKED</span><h3>六个问题都与任务相关</h3><p>覆盖内容方向、受众、生产形式、时间、预算和目标排序；晨间/周末安排、AI/创业方向、长期品牌和 ROI 被落实。</p></article>
          <article><span>MISSED</span><h3>高价值背景没有问</h3><p>未询问 founder/company role、技术资历、LinkedIn/GitHub/Slack/Notion、跨境背景和合规边界。</p></article>
          <article><span>BOUNDARY</span><h3>只算机制信号</h3><p>只有一个 task、一个 persona、一个产品 agent；full 也可追问，评分经 product-UI transport，不进入确认性主表或排行榜。</p></article>
        </div>
      </div></section>

      <section className="shell gapSection" id="pdr-two-agent-pilot">
        <p className="sectionTag">PDR-T01 TWO-AGENT CLARIFICATION PILOT · COMPLETE</p>
        <div className="sectionHead"><h2>相同任务下，两个 Agent 选择了完全不同的澄清策略</h2><p>ChatGPT 与 Gemini 都只看到同一条 AI PhD task 和自由追问许可。ChatGPT 覆盖 7/7 个预冻结 critical preference clusters；Gemini 没有提问。三次盲评 P-score 为 7.057 对 6.065，差 +0.992。</p></div>
        <div className="decisionGrid">
          <article><span>QUESTION POLICY</span><h3>7 类关键偏好对 0</h3><p>ChatGPT 一轮包含 15 个 atomic slots；Gemini 直接生成计划并研究。asked-cluster intersection 为空，Jaccard=0。</p></article>
          <article><span>OUTCOME PATTERN</span><h3>差距集中在个性化决策</h3><p>最大优势来自方向验证、fit-based shortlist 和可衡量背景提升；Gemini 在通用地区比较与就业信息上更强。</p></article>
          <article><span>BOUNDARY</span><h3>存在性证据，不作因果排名</h3><p>一个 task、一个 persona；产品切换也改变模型、planner、搜索和写作策略，因此 0.992 不能只归因于提问。</p></article>
        </div>
      </section>

      <section className="shell gapSection" id="novelty"><p className="sectionTag">NEAREST NEIGHBORS</p><div className="sectionHead"><h2>最强审稿问题：这是否只是已有交互 benchmark 的跨域版？</h2><p>回答不能靠命名；必须用 pilot 证明 task-specific δ、真人决策节点、可识别性边界和 final artifact specificity 带来增量解释力。</p></div><div className="sourceGrid">{papers.map(([name, role, url]) => <a key={name} href={url} target="_blank" rel="noreferrer"><b>{name}</b><span>{role}</span></a>)}</div></section>

      <section className="editionSection" id="editions"><div className="shell"><p className="sectionTag">SYNCHRONIZED EDITIONS</p><div className="sectionHead"><h2>AskInfer-Bench v0.66</h2><p>正式稿、10 页内精简稿、人话版、导师汇报、两周执行手册、task screen、smoke pack、首轮 S0、PDR-T30 最小闭环与 PDR-T01 双 agent pilot 使用同一版本边界。</p></div><div className="editionGrid">
        <article><span>FORMAL</span><h3>正式研究 Proposal</h3><p>完整构念、条件、数据、测量、统计、风险与 Go/No-Go。</p><div className="editionLinks"><a href="/AskInfer-Bench_正式研究Proposal.pdf" download>PDF</a><a href="/AskInfer-Bench_正式研究Proposal.docx" download>Word</a></div></article>
        <article className="recommended"><span>CONDENSED · ≤10 PAGES</span><h3>正式 Proposal 精简版</h3><p>快速判断主张、实验与最强 reviewer objections。</p><div className="editionLinks"><a href="/AskInfer-Bench_正式Proposal精简版.pdf" download>PDF</a><a href="/AskInfer-Bench_正式Proposal精简版.docx" download>Word</a></div></article>
        <article><span>PLAIN LANGUAGE</span><h3>完整人话版</h3><p>逐步解释 Ask、Infer、PDR 边界、δ 与 CFA。</p><div className="editionLinks"><a href="/AskInfer-Bench_完整人话版.pdf" download>PDF</a><a href="/AskInfer-Bench_完整人话版.docx" download>Word</a></div></article>
        <article><span>ADVISOR BRIEF</span><h3>汇报精简版</h3><p>15–20 分钟讨论结构与 pilot 决策门。</p><div className="editionLinks"><a href="/AskInfer-Bench_汇报精简版.pdf" download>PDF</a><a href="/AskInfer-Bench_汇报精简版.docx" download>Word</a></div></article>
        <article className="recommended"><span>EXECUTION PLAYBOOK</span><h3>两周执行 Todo 与作战板</h3><p>六题任务卡、三个必跑系统、114 个 episode、逐日门槛和可勾选进度。</p><div className="editionLinks"><a href="/AskInfer-Bench_两周执行Todo与任务手册.pdf" download>PDF</a><a href="/AskInfer-Bench_两周执行Todo与任务手册.docx" download>Word</a><a href="/AskInfer-Bench_两周执行作战板.html">作战板</a></div></article>
      </div><div className="schemaDownloads"><b>可执行协议</b><a href="/ask_infer_case.schema.yaml" download>Case schema ↓</a><a href="/ask_infer_evaluation.protocol.yaml" download>Evaluation protocol ↓</a><a href="/ask_infer_benchmark.manifest.yaml" download>Manifest ↓</a><a href="/AskInfer-Bench_评测框架_v0.62.svg" download>Figure SVG ↓</a><a href="/PROJECT_MEMORY.md" download>项目记忆 ↓</a></div></div></section>

      <footer className="closing"><div className="shell closingGrid"><div><p className="eyebrow">CLAIM BOUNDARY</p><h2>先证明会问、会推断、也会克制</h2></div><p>不把多问等同于好问，不把 persona 猜测等同于 inference，不把 LLM 生成 rubric 当 ground truth，也不把预期排名反转写成既成事实。</p></div></footer>
    </main>
  );
}
