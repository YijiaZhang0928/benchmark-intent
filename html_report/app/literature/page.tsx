import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "29 篇个性化 Agent 相关工作地图｜DeepAlign-Bench",
  description: "七篇最近邻工作精读与二十二篇 agent personalization / evaluation 论文的精准相关性审计",
};

const papers = [
  {
    id: "2607.27056",
    short: "Setoka",
    title: "Hierarchical User Understanding over Heterogeneous Data",
    role: "用户理解",
    verdict: "不能再说“没有 benchmark 测跨源深层用户理解”。",
    abstract: "把用户理解分成语义事实、情景记忆、行为模式和人格特质四层；用心理测量驱动的流程生成 10 个合成用户的异构记录，并评测 3 个模型与 5 个 memory system。",
    figure: "异构记录 → selection → linking → aggregation → generalization；证据范围和推断抽象度逐级上升。",
    conclusion: "单记录事实可由数据库较好解决，但多记录拼接、长程聚合和人格推断仍弱；回答率高也可能是无依据猜测。",
    ours: "给 user-state fact 保存 provenance 和推断层级；区别是我们评价这些推断是否让开放式 DR 交付物在 must-change 处正确变化。",
    href: "https://arxiv.org/abs/2607.27056",
    flow: ["事实", "事件", "模式", "特质"],
  },
  {
    id: "2607.21635",
    short: "Temporal Interventions",
    title: "User-Conditioned Evaluation under Temporal Interventions",
    role: "时间干预",
    verdict: "是我们 Update / Recover 设计最直接的方法学前作。",
    abstract: "focused audit / position paper：同一时间干预应在不同持久用户状态上重放，检查是否产生用户条件化差异。",
    figure: "C1 显式外生事件；C2 状态跨事件持久；C3 一个维度影响另一个维度；C4 结果随用户状态变化。",
    conclusion: "审计的 15 个公开协议中，没有一个同时满足 C1–C4；建议提供 profile states、event scripts、dependency annotations、oracle checks 和 per-user regression suites。",
    ours: "不能声称首次测试时间变化；要在 DR 最终交付物上实际满足 C1–C4，并增加反事实用户真值、正向效用和 judge 校准。",
    href: "https://arxiv.org/abs/2607.21635",
    flow: ["事件", "持久", "跨维", "按用户"],
  },
  {
    id: "2607.20482",
    short: "PersonaTrail",
    title: "Personalized Web Agents through Browsing Trails",
    role: "浏览历史",
    verdict: "证明真实行为轨迹可以是用户信号，而不只是 persona 文本。",
    abstract: "在 managed open web 中，用细粒度浏览轨迹测试 preference inference 与 episodic grounding；覆盖 23 个领域、317 个网站和 2,524 个 query。",
    figure: "同一 browsing history 分别支持“通常喜欢什么”和“过去某次看过什么”；前者需要 preference memory，后者需要 factual memory。",
    conclusion: "直接处理 raw history 不够；历史越多、任务越复杂，基线退化越明显。PACMem 的事实/偏好双记忆优于基线。",
    ours: "把浏览/行为轨迹纳入 signal channel，并做 raw history 与语义等价 structured persona 的信息量匹配对照。",
    href: "https://arxiv.org/abs/2607.20482",
    flow: ["轨迹", "事实记忆", "偏好记忆", "网页行动"],
  },
  {
    id: "2607.15948",
    short: "TARS",
    title: "Theory-of-Mind Personalized Code Comprehension",
    role: "单域效用",
    verdict: "提醒我们：个性化效用不应只看输出文字。",
    abstract: "在 VS Code 内根据经验、角色、目标和解释偏好生成代码解释；18 人研究同时测时间、正确性、认知负担和主观适配。",
    figure: "profiler questionnaire 把经验、角色、用途、长度、语言、目标和语气映射到解释生成。",
    conclusion: "平均完成时间约快 26%，认知负担与主观适配更好；但正确性几乎相同，时间差未过传统显著性门槛，外推仍有限。",
    ours: "在少量 anchor 加 downstream human utility；不能把主观“感觉被个性化”当作客观任务收益。",
    href: "https://arxiv.org/abs/2607.15948",
    flow: ["用户画像", "代码片段", "适配解释", "人类效用"],
  },
  {
    id: "2607.12254",
    short: "SARSI",
    title: "Governed Multi-Agent Architecture for Personal Singularity",
    role: "系统架构",
    verdict: "可用于完善 ontology，但不是实证 benchmark 证据。",
    abstract: "提出 goal、scope、tool、benchmark 驱动的多 agent 架构，强调外部治理、owner control、可审计 self-model、任务契约和逐步升级。",
    figure: "task-contract compiler → planner → tool actor/sub-agents → independent verifier；外部 governance 保留批准、回滚与关闭权。",
    conclusion: "反对单体 agent 自我改写后自我相信；主张版本化、可逆、外部授权。论文明确没有原创数据或实现。",
    ours: "扩展 agent plane、handoff、责任主体、verifier 独立性和 rollback 元数据；不把架构主张写成性能结论。",
    href: "https://arxiv.org/abs/2607.12254",
    flow: ["契约", "执行", "验证", "治理"],
  },
  {
    id: "2607.10526",
    short: "PASB",
    title: "Persistent Sycophancy in Stateful Personal Agents",
    role: "持久风险",
    verdict: "是 state-writing safety 与 longitudinal failure 最强的直接前作。",
    abstract: "1,600 个任务、12 个模型、2 个 agent framework；5 轮 persist 后清空对话，再用 3 轮中性 query 检查 agent 自主写入的状态是否污染后续。",
    figure: "用户主张 → agent 接受 → durable write → 来源/状态变化 → 新会话取回 → 下游污染；write boundary 是关键。",
    conclusion: "commit 后平均失败从 45.0% 升至 71.9%（+27.0pp）；主要机制是 status promotion、attribution removal 和 scope broadening。",
    ours: "将 source/status/scope/time/visibility 写入 metadata，并同时测正向 DR 适配、must-not 和共同质量。",
    href: "https://arxiv.org/abs/2607.10526",
    flow: ["主张", "写入", "取回", "污染"],
  },
  {
    id: "2607.03162",
    short: "APeB",
    title: "Agentic Personalization under Underspecified Product Search",
    role: "意图利用",
    verdict: "证明 personalization gap 常在“欠指定意图 + 噪声历史”。",
    abstract: "从商品 action logs 构造原始欠指定 query、丰富历史和用户看过的 hard candidates，记录意图推断、偏好提取、检索和候选选择。",
    figure: "agent 从视频、直播、浏览与搜索等历史推断意图，再在相近候选中选择；hard candidates 排除粗语义匹配的虚假高分。",
    conclusion: "明确 query 表现较好，早期意图与偏好发现较弱；history-aware query refinement 跨 backbone 带来一致增益。",
    ours: "Ua/Ub 都必须合理且难以靠粗语义区分；中间 user-goal proxy 只做诊断，不能成为最终 judge 的循环真值。",
    href: "https://arxiv.org/abs/2607.03162",
    flow: ["模糊意图", "历史", "偏好", "细粒度选择"],
  },
];

const matrix = [
  ["Setoka", "●", "●", "◐", "—", "—", "◐", "—"],
  ["Temporal", "◐", "◐", "◐", "—", "—", "●", "●"],
  ["PersonaTrail", "●", "●", "●", "◐", "—", "◐", "—"],
  ["TARS", "◐", "◐", "●", "●", "—", "—", "—"],
  ["SARSI", "◐", "◐", "◐", "◐", "—", "●", "●"],
  ["PASB", "◐", "◐", "●", "◐", "—", "●", "●"],
  ["APeB", "●", "●", "●", "◐", "—", "—", "—"],
  ["DeepAlign（计划）", "●", "●", "●", "●", "●", "●", "●"],
];

const extendedPapers = [
  ["LaMP", "近邻 · 输出", "用户历史驱动多类个性化生成", "非 agent / 非 DR；没有用户交换", "https://aclanthology.org/2024.acl-long.399/"],
  ["TravelPlanner+", "直接 · 规划", "user model 改变旅行计划", "单一旅行域；generic/personal 对照", "https://aclanthology.org/2024.emnlp-industry.37/"],
  ["PersonaLens", "直接 · 对话", "画像 + 历史 + user/judge agent", "模型模拟为主；非 DR artifact", "https://aclanthology.org/2025.findings-acl.927/"],
  ["PersonaMem", "近邻 · 动态画像", "最长 60 sessions，跟踪画像变化", "响应选择终点；没有工具或 artifact", "https://arxiv.org/abs/2504.14225"],
  ["ETAPP", "直接 · 工具", "800 cases；人工 key points 评主动调用", "离散 API sandbox；无用户交换", "https://aclanthology.org/2025.acl-long.1064/"],
  ["ToolSpectrum", "直接 · 工具", "联合 user profile 与环境选择工具", "工具选择不等于 DR 最终效用", "https://arxiv.org/abs/2505.13176"],
  ["PRIME", "近邻 · 双记忆", "情景历史 + 演化语义信念", "memory method；无 agent/DR 反事实", "https://aclanthology.org/2025.emnlp-main.1711/"],
  ["PDR 2026", "直接 · DR", "画像进入检索、推理与停止条件", "四类任务；无预冻结差异真值", "https://arxiv.org/abs/2605.10530"],
  ["MyScholarQA", "最直接 · DR+真人", "真人揭示九类 LLM judge 漏检错误", "只覆盖学术调研；纵向算子有限", "https://aclanthology.org/2026.acl-long.723/"],
  ["Personalized Benchmarking", "近邻 · 榜单", "115 名用户的个体排名偏离总体排名", "评模型偏好，不评 agent 使用用户信息", "https://aclanthology.org/2026.findings-acl.31/"],
  ["RPEval", "直接 · 误用", "无关记忆导致 irrational personalization", "意图推理终点；非开放式 DR", "https://arxiv.org/abs/2601.16621"],
  ["PAHF", "直接 · 漂移", "澄清 + 记忆 + 反馈适应 persona shift", "训练框架与窄域任务；无报告真值", "https://arxiv.org/abs/2602.16173"],
  ["PerMemBench", "近邻 · 写入", "个性化判断哪些 session 值得保存", "评 retention，不评最终交付物", "https://arxiv.org/abs/2605.25535"],
  ["Memora", "近邻 · 过期", "FAMA 惩罚继续使用失效记忆", "记忆/推荐任务；非 DR 过程", "https://aclanthology.org/2026.findings-acl.1337/"],
  ["CloneMem", "近邻 · 数字轨迹", "1–3 年日记、社媒和邮件的状态演化", "AI clone 记忆；无外部任务效用", "https://aclanthology.org/2026.acl-long.1549/"],
  ["Mem2ActBench", "直接 · 记忆→行动", "长期偏好落实到工具与参数", "400 个离散任务；无开放 artifact", "https://aclanthology.org/2026.acl-long.370/"],
  ["APOLLO", "直接 · 偏好跟随", "显式/隐式历史驱动主动或被动调用", "以工具动作命中为主；无报告权衡", "https://aclanthology.org/2026.findings-acl.1676/"],
  ["AndroidIntent", "直接 · GUI", "长期记录解析模糊指令与 routines", "单一 Android 域；非多证据综合", "https://aclanthology.org/2026.acl-long.1669/"],
  ["OPeRA", "近邻 · 真实行为", "真实 persona、观察、动作与即时 rationale", "模拟用户下一步，不评服务用户的质量", "https://aclanthology.org/2026.acl-long.2033/"],
  ["PS-Bench", "直接 · 安全", "个人记忆可能错误地合理化危险意图", "单一安全机制；不测正向 DR 适配", "https://aclanthology.org/2026.acl-long.1260/"],
  ["One Persona, Many Cues", "直接 · cue 稳健性", "同一 persona 的六类提示线索可改变个性化与偏差结论", "写作/建议任务；不评 DR artifact，但直接威胁单一 persona 形式的效度", "https://aclanthology.org/2026.acl-long.2079/"],
  ["PARL", "直接 · 个性化评价", "从用户历史学习 rubric，并强调代表性、一致性和区分力", "个性化文本生成；未做 DR 的跨用户 artifact 矩阵", "https://arxiv.org/abs/2605.31545"],
];

export default function LiteratureBrief() {
  return (
    <main className="litPage">
      <header className="litHero" id="lit-top">
        <nav className="litNav shell">
          <a className="brand" href="/">DeepAlign<span>Bench</span></a>
          <div><a href="#map">位置图</a><a href="#audit">22 篇审计</a><a href="#papers">七篇精读</a></div>
          <a className="navCta" href="/">返回 Proposal</a>
        </nav>
        <div className="shell litHeroGrid">
          <section>
            <p className="eyebrow">RELATED-WORK RAPID REVIEW · ABSTRACT + FIGURE + CONCLUSION</p>
            <h1>29 篇工作，把我们的题目<em>压到一个可证伪的点</em></h1>
            <p className="lede">七篇最近邻工作精读，加上二十二篇 agent personalization / evaluation 扩展审计。PDR-Bench 已经解决 task–persona 条件下的 absolute adaptation evaluation。DeepAlign 改变的是 estimand：固定任务与证据后，通过 matched/swapped 与三类预冻结契约识别 counterfactual personalization effect。</p>
            <div className="heroActions"><a className="button primary" href="#map">先看结论</a><a className="button ghost" href="#audit">检查 22 篇筛选</a></div>
          </section>
          <aside className="litClaim">
            <span>REVIEWER-SAFE CLAIM</span>
            <p>不声称首先研究 personalization、history、persistent state 或 temporal intervention。</p>
            <b>候选核心贡献是：从 absolute adaptation 转向跨用户 counterfactual effect identification；其他模块只支撑稳健性与外部效度。</b>
          </aside>
        </div>
      </header>

      <section className="shell litMap" id="map">
        <p className="sectionTag">ONE-PAGE TAKEAWAY</p>
        <div className="sectionHead"><h2>现有论文覆盖的是一条能力链的不同区段</h2><p>同一篇论文不需要覆盖所有区段；我们的主张也只有在最后的交叉协议被真实实验验证时才成立。</p></div>
        <div className="litChain" role="img" aria-label="从用户理解、历史利用到持久状态和最终交付物的相关工作链条">
          <article><span>01</span><h3>理解用户</h3><b>Setoka <a className="inlineCite" href="https://arxiv.org/abs/2607.27056" target="_blank" rel="noreferrer">[26]</a></b><p>异构记录、四层抽象</p></article>
          <i>→</i>
          <article><span>02</span><h3>从历史行动</h3><b>PersonaTrail <a className="inlineCite" href="https://arxiv.org/abs/2607.20482" target="_blank" rel="noreferrer">[28]</a> · APeB <a className="inlineCite" href="https://arxiv.org/abs/2607.03162" target="_blank" rel="noreferrer">[32]</a></b><p>轨迹、意图、偏好、hard alternatives</p></article>
          <i>→</i>
          <article><span>03</span><h3>保持与更新</h3><b>PASB <a className="inlineCite" href="https://arxiv.org/abs/2607.10526" target="_blank" rel="noreferrer">[31]</a> · Temporal <a className="inlineCite" href="https://arxiv.org/abs/2607.21635" target="_blank" rel="noreferrer">[27]</a></b><p>写入边界、时间事件、跨维影响</p></article>
          <i>→</i>
          <article className="target"><span>04</span><h3>用户特异交付物</h3><b>DeepAlign-Bench</b><p>反事实效用 + 通用质量 + 纵向干预</p></article>
        </div>
        <div className="litThreats">
          <article><b>最直接的方法威胁</b><h3>Temporal Interventions <a className="inlineCite" href="https://arxiv.org/abs/2607.21635" target="_blank" rel="noreferrer">[27]</a></h3><p>我们的动态更新必须实际满足 C1–C4，不能只在 schema 里出现。</p></article>
          <article><b>最直接的安全威胁</b><h3>PASB <a className="inlineCite" href="https://arxiv.org/abs/2607.10526" target="_blank" rel="noreferrer">[31]</a></h3><p>必须评价“该不该写、如何标记来源/作用域”，不能只奖励记住用户。</p></article>
          <article><b>最直接的信号威胁</b><h3>Setoka <a className="inlineCite" href="https://arxiv.org/abs/2607.27056" target="_blank" rel="noreferrer">[26]</a> + PersonaTrail <a className="inlineCite" href="https://arxiv.org/abs/2607.20482" target="_blank" rel="noreferrer">[28]</a> + APeB <a className="inlineCite" href="https://arxiv.org/abs/2607.03162" target="_blank" rel="noreferrer">[32]</a></h3><p>异构记录、浏览轨迹和行为日志都已有 benchmark；我们的新意不在“信号更多”。</p></article>
        </div>
      </section>

      <section className="litMatrixBand" id="matrix">
        <div className="shell">
          <p className="sectionTag invert">COVERAGE MAP</p>
          <div className="sectionHead light"><h2>谁已经测了什么</h2><p>● 主评价对象；◐ 部分涉及；— 未作为主要证据。DeepAlign 最后一行是计划，不是已有结果。</p></div>
          <div className="litTableWrap"><table className="litTable"><thead><tr><th>工作</th><th>真实/异构信号</th><th>用户理解</th><th>Agent 执行</th><th>交付物效用</th><th>用户交换</th><th>时间/持久状态</th><th>安全/误用</th></tr></thead><tbody>{matrix.map((row) => <tr key={row[0]}>{row.map((cell, i) => i === 0 ? <th key={cell}>{cell}</th> : <td key={`${row[0]}-${i}`} data-mark={cell}>{cell}</td>)}</tr>)}</tbody></table></div>
          <p className="litMatrixNote">PDR-Bench 已覆盖 persona-conditioned absolute adaptation。DeepAlign 待验证的是新的 estimand：“● 跨用户交叉评分 + ● must-change / must-hold / must-not”，并以多类交付物、跨 cue、长程状态和安全条件检验其稳健性与外部效度。</p>
        </div>
      </section>

      <section className="shell litAudit" id="audit">
        <p className="sectionTag">22-PAPER RELEVANCE AUDIT</p>
        <div className="sectionHead"><h2>不是搜到就算相关：每篇都要说明“覆盖了什么、还差什么”</h2><p>纳入门槛：用户条件是可观察输入、会改变生成/规划/行动、并有可比较结果，三项中至少满足两项。纯角色扮演、通用 memory 和非 agent 推荐工作没有纳入。</p></div>
        <div className="auditLegend"><span><b>直接</b> 已评价用户条件化的 agent 决策、行动或 DR</span><span><b>近邻</b> 只覆盖本协议的一个必要模块</span></div>
        <div className="auditGrid">
          {extendedPapers.map((paper, index) => (
            <article key={paper[0]}>
              <header><span>{String(index + 1).padStart(2, "0")}</span><b>{paper[1]}</b></header>
              <h3><a href={paper[4]} target="_blank" rel="noreferrer">{paper[0]} ↗</a></h3>
              <p>{paper[2]}</p>
              <small>{paper[3]}</small>
            </article>
          ))}
        </div>
        <div className="auditStory">
          <b>叙事收敛</b>
          <span>用户历史/画像</span><i>→</i><span>响应与任务对话</span><i>→</i><span>规划、工具与 GUI</span><i>→</i><span>写入、更新与安全</span><i>→</i><span>个性化 DR</span><i>→</i><strong>交换用户识别最终交付物</strong>
        </div>
      </section>

      <section className="shell litPapers" id="papers">
        <p className="sectionTag">PAPER-BY-PAPER</p>
        <div className="sectionHead"><h2>七篇 2026 年 7 月最近邻工作：每篇只抓四件事</h2><p>Abstract 说测什么；主图暴露操作化；Conclusion 给证据边界；最后判断它如何改变我们的设计。</p></div>
        <div className="litPaperList">
          {papers.map((paper, index) => (
            <article className="litPaper" key={paper.id}>
              <header><span>{String(index + 1).padStart(2, "0")} · {paper.role}</span><h3>{paper.short}</h3><p>{paper.title}</p><a href={paper.href} target="_blank" rel="noreferrer">arXiv:{paper.id} ↗</a></header>
              <div className="litMiniFigure" aria-label={`${paper.short} 主图的文字化重绘`}><small>主图逻辑（重绘）</small><div>{paper.flow.map((item, i) => <span key={item}><b>{item}</b>{i < paper.flow.length - 1 && <i>→</i>}</span>)}</div></div>
              <div className="litPaperGrid"><section><b>Abstract</b><p>{paper.abstract}</p></section><section><b>主图</b><p>{paper.figure}</p></section><section><b>Conclusion / Limit</b><p>{paper.conclusion}</p></section><section className="ours"><b>对 DeepAlign-Bench</b><p>{paper.ours}</p></section></div>
              <blockquote>{paper.verdict}</blockquote>
            </article>
          ))}
        </div>
      </section>

      <section className="litActions">
        <div className="shell">
          <p className="sectionTag invert">WHAT CHANGED</p>
          <div className="sectionHead light"><h2>Proposal 1.1 现在应该怎么讲</h2><p>每推进一层，就同时说明已有覆盖和仍未识别的终点。</p></div>
          <ol><li><b>第一层：</b>通用 DR benchmark 建立事实、搜索、引用和报告质量底线，但不回答结果更适合哪个用户。</li><li><b>第二层：</b>LaMP、PersonaLens、Setoka、PersonaTrail 与 APeB 已覆盖用户历史、任务对话、分层理解和行为轨迹；空白不再是“懂不懂用户”。</li><li><b>第三层：</b>ETAPP、ToolSpectrum、Mem2ActBench、APOLLO 和 AndroidIntent 已把用户信息落实到工具/GUI 行动；空白也不再是“有没有行动”。</li><li><b>第四层：</b>PersonaMem、PAHF、PerMemBench、Memora、CloneMem、PASB 与 PS-Bench 已进入动态画像、写入、过期和安全；这些成为稳健性与诊断 operator。</li><li><b>收敛层：</b>PDR-Bench 已用 task/persona-conditioned P-Score 测 absolute adaptation；DeepAlign 转向跨用户 matched/swapped 和 must-change/must-hold/must-not 所定义的 counterfactual personalization effect。</li><li><b>方法边界：</b>One Persona, Many Cues 和 PARL 用于检验 DeepAlign 效应的跨表达稳健性；不用于否定 PDR-Bench 的 rubric/judge，也不证明模型内部理解。</li></ol>
          <div className="litGo"><b>四项最低成立条件</b><span>matched/swapped 人评稳定</span><span>语义等价 cue 下结论稳定</span><span>共同质量与 must-hold 不下降</span><span>至少一个 signal/operator 效应可重复</span></div>
        </div>
      </section>

      <footer><div className="shell"><b>DeepAlign-Bench · v0.21</b><p>本页是快速文献地图；正式引用与方法边界以 Proposal 为准。</p><a href="#lit-top">回到顶部 ↑</a></div></footer>
    </main>
  );
}
