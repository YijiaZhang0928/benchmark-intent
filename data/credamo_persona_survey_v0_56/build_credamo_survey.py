#!/usr/bin/env python3
"""Build the machine-readable Credamo questionnaire package.

The Markdown questionnaire is the human-readable authority. This builder binds
its stable question IDs to the existing 60-task pool and emits deterministic
JSON/JSONL artifacts for platform implementation and audit.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
TASKS_PATH = ROOT / "data/plhkw_task_pool_v0_54/selected_tasks.jsonl"
SPEC_PATH = ROOT / "proposal/DeepAlign-Bench_Credamo真人Persona问卷方案.md"
PROTOCOL_PATH = ROOT / "benchmark_schema/credamo_persona_collection.protocol.yaml"


PAGES = [
    {"page_id": "A0", "wave": "A", "part": 0, "title": "研究说明", "minutes": [1, 1], "entry": "open_wave_A"},
    {"page_id": "A1", "wave": "A", "part": 0, "title": "年龄与知情同意", "minutes": [1, 2], "entry": "A0_complete"},
    {"page_id": "A2", "wave": "A", "part": 1, "title": "基础人口学与当前身份", "minutes": [2, 2], "entry": "adult_and_all_required_consents"},
    {"page_id": "A3", "wave": "A", "part": 1, "title": "教育、职业和领域", "minutes": [2, 3], "entry": "A2_complete"},
    {"page_id": "A4", "wave": "A", "part": 1, "title": "Coding、Data 与 Research 经验", "minutes": [2, 3], "entry": "A3_complete"},
    {"page_id": "A5", "wave": "A", "part": 2, "title": "最近与预期任务经历", "minutes": [1, 2], "entry": "A4_complete"},
    {"page_id": "A6", "wave": "A", "part": 2, "title": "适配任务卡", "minutes": [3, 5], "entry": "at_least_one_eligible_route"},
    {"page_id": "A7", "wave": "A", "part": 3, "title": "选择候选任务", "minutes": [1, 2], "entry": "one_or_more_task_cards_eligible"},
    {"page_id": "A8", "wave": "A", "part": 3, "title": "候选任务真实性核验", "minutes": [3, 6], "entry": "repeat_for_each_selected_candidate_task"},
    {"page_id": "A9", "wave": "A", "part": 3, "title": "回访授权与结束", "minutes": [1, 1], "entry": "A8_complete"},
    {"page_id": "B0", "wave": "B", "part": 4, "title": "回访说明与任务状态", "minutes": [1, 1], "entry": "invited_and_assigned_task"},
    {"page_id": "B1", "wave": "B", "part": 4, "title": "Open-first elicitation", "minutes": [5, 8], "entry": "task_still_relevant"},
    {"page_id": "B2", "wave": "B", "part": 4, "title": "全任务通用补充", "minutes": [3, 5], "entry": "B1_initial_snapshot_saved"},
    {"page_id": "B3-DR", "wave": "B", "part": 4, "title": "Deep Research 补充", "minutes": [4, 7], "entry": "vertical=deep_research"},
    {"page_id": "B3-SW", "wave": "B", "part": 4, "title": "Code 补充", "minutes": [4, 7], "entry": "vertical=software_engineering"},
    {"page_id": "B3-DA", "wave": "B", "part": 4, "title": "Data 补充", "minutes": [4, 7], "entry": "vertical=data_analysis"},
    {"page_id": "B4", "wave": "B", "part": 4, "title": "原始回答回看", "minutes": [1, 2], "entry": "vertical_module_complete"},
    {"page_id": "C0", "wave": "C", "part": 5, "title": "LLM 规范化说明", "minutes": [1, 1], "entry": "offline_normalization_complete"},
    {"page_id": "C1", "wave": "C", "part": 5, "title": "逐条 fact card 审核", "minutes": [4, 7], "entry": "repeat_for_candidate_facts"},
    {"page_id": "C2", "wave": "C", "part": 5, "title": "Ledger 总览", "minutes": [1, 2], "entry": "all_fact_cards_reviewed"},
    {"page_id": "C3", "wave": "C", "part": 5, "title": "结束与撤回说明", "minutes": [1, 1], "entry": "C2_complete"},
]


def question(qid, page, text, qtype, *, required=True, options=None,
             display="always", validation=None, variable=None,
             origin="administrative", notes=None):
    return {
        "question_id": qid,
        "page_id": page,
        "text_zh": text,
        "question_type": qtype,
        "required": required,
        "options": options or [],
        "display_logic": display,
        "validation": validation or {},
        "variable": variable or qid.lower(),
        "fact_origin_if_retained": origin,
        "implementation_notes": notes or "",
    }


Q = []

# Part 0
Q += [
    question("C01", "A1", "你是否已年满 18 周岁？", "single_choice", options=["是", "否"], variable="consent.adult_18_plus", notes="否→结束；不得继续收集人口学或开放文本"),
    question("C02", "A1", "阅读以上说明后，你是否自愿参加本研究？你可以随时退出；退出不会受到惩罚，已获得的合法报酬不因退出被追回。", "single_choice", options=["我同意参加", "我不同意参加"], variable="consent.participate", notes="不同意→结束"),
    question("C03", "A1", "研究团队可能使用经批准的语言模型，把你的原始回答整理成候选事实卡。模型不会自动成为最终答案；你将在后续页面逐条批准、修改或删除。你是否理解并同意这一处理方式？", "single_choice", options=["理解并同意", "不同意使用语言模型处理我的回答"], variable="consent.llm_normalization", notes="不同意→人工规范化分支或结束；不可默认外发"),
    question("C04", "A1", "你是否同意研究团队在去除直接身份信息后，将经你确认的任务相关事实用于学术分析和 benchmark 构建？原始开放回答和完整私有 ledger 默认不公开。", "single_choice", options=["同意", "不同意"], variable="consent.deidentified_research_use"),
    question("C05", "A1", "如果本次回答与某些任务匹配，你是否愿意通过 Credamo 接收 1–2 次后续邀请？是否愿意不影响本次报酬。", "single_choice", options=["愿意", "暂时不确定", "不愿意"], variable="consent.recontact"),
    question("C06", "A1", "以下哪项最准确描述你在本研究中的任务？", "single_choice", options=["现在替研究团队完成所有复杂任务", "描述与具体任务有关的真实需求，并核对系统整理是否准确", "根据想象编写一个尽量戏剧化的人设", "给 AI 产品做广告评价"], variable="qc.consent_comprehension", notes="正确选项为第2项；首次错误解释后重答；二次错误仅soft flag"),
]

# Participant screening
Q += [
    question("D01", "A2", "你的年龄段是？", "single_choice", options=["18–24", "25–34", "35–44", "45–54", "55–64", "65岁及以上", "不愿回答"], variable="profile.age_band", notes="不参与task routing"),
    question("D02", "A2", "你的性别是？", "single_choice", required=False, options=["女", "男", "非二元/其他", "不愿回答"], variable="profile.gender", notes="不参与task routing"),
    question("D03", "A2", "你目前主要居住在哪个地区？", "single_choice", options=["中国大陆", "中国香港/澳门", "中国台湾", "亚洲其他地区", "欧洲", "北美", "其他", "不愿回答"], variable="profile.region", notes="不直接参与需求推断"),
    question("D04", "A2", "你在学习或工作中最常使用哪些语言？", "multiple_choice", options=["中文", "英文", "德语", "法语", "日语", "韩语", "西班牙语", "其他", "不愿回答"], variable="profile.languages"),
    question("D05", "A2", "你当前最主要的身份是？", "single_choice", options=["本科生", "硕士生", "博士生", "高校/科研人员", "企业全职", "企业兼职/实习", "自由职业/个体经营", "创业者", "暂未就业", "退休", "其他"], variable="profile.primary_status"),
    question("B01", "A3", "你的最高学历或当前正在攻读的学历是？", "single_choice", options=["高中/中专及以下", "大专", "本科", "硕士", "博士", "其他", "不愿回答"], variable="profile.education_level"),
    question("B02", "A3", "你接受过系统学习或训练的领域有哪些？请选择所有适用项。", "multiple_choice", options=["计算机/软件工程", "人工智能/机器学习", "数据科学/统计", "数学/物理", "材料/化学", "生命科学/医学", "心理/教育", "经济/金融/会计", "工商管理/市场/产品", "法律/公共政策", "环境/能源/地理", "建筑/房地产", "新闻/传播/创意写作", "其他", "无以上系统训练"], variable="profile.education_domains"),
    question("B03", "A3", "你当前或最近一份学习/工作的主要行业或场景有哪些？", "multiple_choice", options=["高校/科研", "互联网/软件", "人工智能", "金融/支付/保险", "零售/电商", "制造/供应链", "医疗健康", "教育", "政府/公共事业", "能源/环保", "咨询/专业服务", "媒体/出版/创意", "房地产", "旅游/差旅", "非营利组织", "其他", "暂无相关经历"], variable="profile.occupation_domains"),
    question("B04", "A3", "你实际承担过哪些工作或学习职能？", "multiple_choice", options=["软件开发", "测试/运维/SRE", "数据分析/商业分析", "数据工程", "机器学习/建模", "学术研究/文献综述", "产品管理/用户研究", "经营/战略/咨询", "财务/会计/投资", "市场/销售", "教育/培训", "法律/合规/风控", "设计/内容创作", "管理决策", "其他", "暂无"], variable="profile.functions"),
    question("B05", "A3", "在你最熟悉的上述领域中，你累计有多少年实际学习、研究或工作经历？", "single_choice", options=["不足6个月", "6–12个月", "1–2年", "3–5年", "6–10年", "10年以上"], variable="profile.experience_years"),
    question("B06", "A3", "在相关任务中，你通常承担什么责任？", "multiple_choice", options=["自己使用结果", "准备材料供他人决定", "提出建议", "共同决策", "对最终决定负责", "负责实现/维护交付物", "仅学习或观察", "其他"], variable="profile.decision_roles"),
    question("E01", "A4", "过去 12 个月，你实际做过以下工作多少次？", "matrix_single_choice", options=["从未", "1–2次", "3–5次", "6–11次", "每月至少一次", "每周至少一次"], variable="profile.activity_frequency", notes="行：多来源研究/跨文件软件/数据分析/ML/复杂决策材料"),
    question("E02", "A4", "你目前独立完成软件开发或代码调试任务的能力最接近哪一项？", "single_choice", options=["没有相关经验", "能阅读少量代码但不能独立修改", "能完成脚本或单文件程序", "能在已有项目中修改并测试", "能负责跨文件/部署/架构任务", "不愿回答"], variable="profile.coding_level"),
    question("E03", "A4", "你实际使用过哪些技术？", "multiple_choice", required=False, options=["Python", "JavaScript/TypeScript", "Java/Kotlin", "C/C++", "R", "SQL", "Web/backend framework", "测试框架", "容器/云", "CI/CD", "分布式系统", "安全工具", "其他"], display="E02 != 没有相关经验", variable="profile.coding_tools"),
    question("E04", "A4", "你目前独立完成数据分析或建模任务的能力最接近哪一项？", "single_choice", options=["没有相关经验", "能阅读图表和基础统计", "能使用电子表格完成分析", "能使用SQL/R/Python完成可复现分析", "能负责建模、实验或数据产品", "不愿回答"], variable="profile.data_level"),
    question("E05", "A4", "你实际使用过哪些数据工具或方法？", "multiple_choice", required=False, options=["Excel/Sheets", "SQL", "Python", "R", "BI工具", "统计建模", "机器学习", "A/B test", "因果推断", "地理空间分析", "数据工程", "其他"], display="E04 != 没有相关经验", variable="profile.data_tools"),
    question("E06", "A4", "你目前独立完成多来源研究任务的能力最接近哪一项？", "single_choice", options=["没有相关经验", "能搜索并整理一般资料", "能比较多个来源并核对引用", "能完成系统文献/市场/政策研究", "能设计检索策略并审计证据质量", "不愿回答"], variable="profile.research_level"),
    question("E07", "A4", "过去 12 个月，你是否把以下任务交给过 AI 工具协助？", "multiple_choice", options=["深度资料检索/报告", "代码开发或调试", "数据分析/表格", "机器学习", "决策建议", "未使用过", "其他"], variable="profile.ai_delegation_experience"),
]

# Routing and task selection templates
Q += [
    question("R01", "A5", "在未来 12 个月，你现实中可能需要完成哪些类型的工作？", "multiple_choice", options=["多来源检索、比较和报告", "修改/构建真实软件项目", "分析真实数据或工作簿", "训练/评估模型", "以上都不太可能", "不确定"], variable="route.future_verticals"),
    question("R02", "A5", "如果任务涉及学习或工作，你是否能在不提供机密信息、个人身份信息、内部数据或代码的情况下描述自己的需求？", "single_choice", options=["可以", "需要泛化后可以", "大多数情况下不可以", "不确定"], variable="route.safe_generalization"),
    question("R03", "A5", "你现在或未来一年中，最可能需要 AI 协助的领域有哪些？", "multiple_choice", options=["学术申请/科研", "AI/软件产品", "职业/国际流动", "创作/出版", "住房/消费决策", "家庭/教育", "健康信息", "投资/金融", "法律/政策/合规", "材料/工业研发", "环境/能源/公共事业", "旅游/差旅", "零售/营销/产品增长", "财务/经营", "制造/供应链", "其他", "暂时没有"], variable="route.domains"),
    question("TREL", "A6", "这项任务与你的现实需要有多大关系？", "single_choice_per_task", options=["目前正在面对类似任务", "过去12个月做过类似任务", "未来12个月很可能需要", "只是感兴趣或可以想象", "与我无关/无法判断"], variable="task_relevance.{task_id}", notes="前三项 eligible"),
    question("TEXP", "A6", "对这类任务，你最接近哪种情况？", "single_choice_per_task", options=["曾对类似任务的结果负责", "曾实际参与类似任务", "理解该场景并会使用结果", "只听说过", "无法判断"], variable="task_experience.{task_id}", notes="前三项 eligible；专业高门槛任务优先前两项"),
    question("TSAFE", "A6", "你能否在不透露姓名、单位、客户、账号、内部数据、代码或其他机密内容的情况下，描述自己对这项任务的真实需要？", "single_choice_per_task", options=["可以", "泛化细节后可以", "不可以", "不确定"], variable="task_safe_answer.{task_id}", notes="前两项 eligible"),
    question("TAI", "A6", "如果 AI 能够安全、可靠地完成该任务，你现实中有多大可能把它交给 AI 协助？", "single_choice_per_task", options=["非常可能", "比较可能", "不确定", "比较不可能", "完全不可能"], variable="task_ai_delegation.{task_id}"),
    question("TSELECT", "A7", "请从通过相关性检查的任务中选择 3–5 个现实中正在、曾经或很可能需要，而且你可能愿意让 AI 协助的任务。", "multiple_choice_dynamic", validation={"min": 3, "max": 5, "relax_min_if_fewer_eligible": True}, variable="route.selected_candidate_tasks"),
    question("TAUTH1", "A8", "请简要描述一个你当前、过去 12 个月或未来一年很可能遇到的具体情境，说明为什么这项任务与你有关。请勿填写单位、客户或个人姓名。", "open_text_per_selected_task", validation={"recommended_min_chars": 30, "max_chars": 300}, variable="task_authenticity.{task_id}.scenario", origin="spontaneous"),
    question("TAUTH2", "A8", "如果 AI 完成这项任务，谁会使用它的结果？", "multiple_choice_per_selected_task", options=["我自己", "同学/研究合作者", "直属团队", "管理者/客户", "公众/读者", "家人", "其他", "尚不确定"], variable="task_authenticity.{task_id}.audience", origin="prompted"),
    question("TAUTH3", "A8", "得到结果后，你最可能采取什么下一步行动？", "open_text_per_selected_task", validation={"recommended_min_chars": 20, "max_chars": 250}, variable="task_authenticity.{task_id}.next_action", origin="spontaneous"),
]

# Wave B open-first
Q += [
    question("B00", "B0", "你之前描述的这项任务目前仍与你有关吗？", "single_choice_per_assigned_task", options=["是，情况基本不变", "是，但情况有变化", "已不再相关", "不确定"], variable="task_state.{task_id}.current_validity"),
    question("O01", "B1", "请更具体地描述：在什么情况下你会需要 AI 完成这项任务？当时你要解决什么问题或作出什么决定？", "open_text", validation={"recommended_min_chars": 80, "max_chars": 800}, variable="raw.{task_id}.real_situation", origin="spontaneous"),
    question("O02", "B1", "你希望 AI 最终交付什么？谁会使用它？得到结果后，你或团队下一步会做什么？", "open_text", validation={"recommended_min_chars": 60, "max_chars": 600}, variable="raw.{task_id}.artifact_and_action", origin="spontaneous"),
    question("O03", "B1", "哪些与你本人、团队、已有资源、使用环境或当前状态有关的情况，会改变什么才算一个好结果？如果你认为没有，也请说明。", "open_text", validation={"recommended_min_chars": 60, "max_chars": 600}, variable="raw.{task_id}.conditions", origin="spontaneous"),
    question("O04", "B1", "什么样的结果即使看起来专业，对你来说仍然无法使用或可能造成损失？为什么？", "open_text", validation={"recommended_min_chars": 50, "max_chars": 500}, variable="raw.{task_id}.unacceptable", origin="spontaneous"),
    question("O05", "B1", "如果 AI 在开始前只能再问你几个问题，它最应该先确认什么？如果不需要追问，可以填写“无需追问”。", "open_text", validation={"max_chars": 400}, variable="raw.{task_id}.clarification", origin="spontaneous"),
]

# Global structured completion
Q += [
    question("G01", "B2", "这项成果最主要用于什么？", "single_choice", options=["个人选择", "团队决策", "正式提交/发表", "执行或部署", "探索学习", "向他人解释", "风险审查", "其他", "尚不确定"], origin="prompted"),
    question("G02", "B2", "最终成果需要让哪些人读懂或使用？", "multiple_choice", options=["非专业个人", "一般业务背景", "技术人员", "领域专家", "管理决策者", "监管/审查人员", "只供自己", "其他", "尚不确定"], origin="prompted"),
    question("G03", "B2", "在这项具体任务上，你目前的知识和准备程度如何？", "single_choice", options=["几乎不了解", "了解基本概念", "能判断常见方案", "能独立完成部分工作", "能审查专家级成果", "不确定/不愿回答"], origin="prompted"),
    question("G04", "B2", "如果这是真实任务，你通常需要在多久内获得可用结果？", "single_choice", options=["当天", "2–3天", "一周", "2–4周", "1–3个月", "没有固定期限", "其他"], origin="prompted"),
    question("G05", "B2", "哪些资源限制会影响方案？请选择所有适用项。", "multiple_choice", options=["预算", "人力", "计算资源", "可访问数据", "可使用软件/云服务", "法律/合规", "组织审批", "时间", "没有明确限制", "其他"], origin="prompted"),
    question("G06", "B2", "请列出违反后会使结果直接不可用的硬约束。若没有明确硬约束，请填写“无”。", "open_text", validation={"max_chars": 400}, origin="prompted"),
    question("G07", "B2", "如果最佳方案不可行，你可以接受哪些替代或折中？哪些方面可以灵活，哪些不能？", "open_text", validation={"max_chars": 400}, origin="prompted"),
    question("G08", "B2", "哪些交付形式对你最有用？", "multiple_choice", options=["简短结论", "详细报告", "可执行步骤", "比较表", "代码/patch", "notebook", "电子表格", "图表/dashboard", "引用和证据清单", "风险/假设日志", "其他", "无偏好"], origin="prompted"),
    question("G09", "B2", "AI 在完成任务时不应做哪些事情？", "multiple_choice", options=["上传内部数据", "调用外部云服务", "新增付费依赖", "修改生产环境", "替我作最终高风险决定", "披露个人/组织信息", "访问未授权来源", "没有额外限制", "其他"], origin="prompted"),
    question("G10", "B2", "当证据不充分时，你更希望 AI 怎么做？", "single_choice", options=["停止并说明缺口", "先追问我", "给出多个条件分支", "给出保守建议并明确不确定性", "在合理假设下继续", "取决于具体情况", "无偏好"], origin="prompted"),
]

# Vertical modules
for qid, text, qtype, options in [
    ("DR01", "这项研究最重要的作用是什么？", "multiple_choice", ["形成推荐/选择", "了解全景", "核对主张", "寻找数据集/资源", "查找先前技术", "处理冲突证据", "获得最新变化", "尽可能完整枚举", "形成行动计划", "其他"]),
    ("DR02", "你已经做过哪些准备？", "multiple_choice", ["尚未开始", "普通搜索", "读过关键资料", "已有候选方案", "已有内部材料", "咨询过他人", "其他"]),
    ("DR03", "哪些范围必须限制或覆盖？例如地域、时间、语言、行业、人群、技术版本。", "open_text", []),
    ("DR04", "你对信息来源有什么要求？", "multiple_choice", ["官方文件优先", "同行评审论文优先", "原始数据优先", "行业/公司材料可用", "新闻只作线索", "社区/论坛只作线索", "必须公开访问", "可用付费来源", "无偏好", "其他"]),
    ("DR05", "信息需要新到什么程度？", "single_choice", ["最近一个月", "最近一年", "最近三年", "经典资料也重要", "取决于子问题", "无明确要求"]),
    ("DR06", "在时间有限时，你更倾向于尽量广泛覆盖，还是少量关键对象深入核验？", "semantic_differential_5", ["广泛覆盖", "偏广", "平衡", "偏深", "深入核验"]),
    ("DR07", "最终比较或推荐时，哪些标准最重要？请选择最多5项，再选最重要1项。", "multiple_then_top1", ["成本", "效果", "证据可信度", "适用性", "时间", "风险", "可逆性", "维护难度", "合规", "可获得性", "公平性", "创新性", "其他"]),
    ("DR08", "如果无法同时避免，你更担心漏掉真正重要的选项/证据，还是纳入未经充分验证的选项/证据？", "semantic_differential_5", ["非常担心漏掉", "更担心漏掉", "接近", "更担心误收", "非常担心误收"]),
    ("DR09", "证据存在明显冲突时，AI 应做到什么程度才可以给出行动建议？", "single_choice", ["只报告冲突", "提出需补信息", "条件化建议", "保守建议", "明确首选并说明风险", "取决于可逆性", "无偏好"]),
]:
    Q.append(question(qid, "B3-DR", text, qtype, options=options, display="vertical=deep_research", origin="prompted"))

for qid, text, qtype, options in [
    ("SW01", "如果这是你的真实项目，请描述必须兼容的语言、框架、库和版本。若没有固定栈，请写“无固定栈”。", "open_text", []),
    ("SW02", "代码最终在哪里运行？", "multiple_choice", ["本地电脑", "服务器", "容器/Kubernetes", "公有云", "移动端", "浏览器", "嵌入式/边缘", "科研计算环境", "暂未确定", "其他"]),
    ("SW03", "对向后兼容和公开 API，你的要求是什么？", "single_choice", ["绝不能破坏", "允许弃用但需迁移期", "允许小范围breaking change", "原型阶段可重构", "不适用/不确定"]),
    ("SW04", "是否允许增加新依赖或外部服务？", "single_choice", ["不允许", "仅轻量依赖", "允许但需说明许可/维护风险", "允许托管服务", "取决于收益", "无偏好"]),
    ("SW05", "谁将长期维护代码？他们最熟悉什么？", "multiple_choice", ["只有我", "1–3人小团队", "大型团队", "开源贡献者", "运维团队", "研究人员", "初学者", "暂不维护", "其他"]),
    ("SW06", "你对测试和回归保护的最低要求是什么？", "multiple_choice", ["通过现有测试", "新增核心单元测试", "集成测试", "端到端测试", "性能基准", "安全扫描", "跨版本矩阵", "只需原型验证", "其他"]),
    ("SW07", "哪些性能指标会决定实现是否可用？请填写已知阈值；不知道可以写“不确定”。", "open_text", []),
    ("SW08", "哪些安全、隐私或权限要求必须满足？", "multiple_choice", ["不记录敏感数据", "最小权限", "审计日志", "依赖漏洞控制", "密钥隔离", "数据不得离开本地", "合规要求", "暂无额外要求", "其他"]),
    ("SW09", "你希望如何上线这个改动？", "single_choice", ["一次性替换", "feature flag", "灰度/分阶段", "双写/影子模式", "只提交patch不部署", "需要明确回滚", "不适用/不确定"]),
    ("SW10", "除功能代码外，你需要哪些内容？", "multiple_choice", ["设计说明", "迁移指南", "运维说明", "注释", "示例", "benchmark", "风险/假设日志", "无需额外文档", "其他"]),
]:
    Q.append(question(qid, "B3-SW", text, qtype, options=options, display="vertical=software_engineering", origin="prompted"))

for qid, text, qtype, options in [
    ("DA01", "这项分析最终要支持什么业务、科研或运营决定？谁对决定负责？", "open_text", []),
    ("DA02", "你最需要哪类结论？", "multiple_choice", ["描述现状", "诊断原因", "预测未来", "比较方案", "评估干预效果", "优化资源分配", "建立持续监控", "探索未知模式", "其他"]),
    ("DA03", "最重要的主指标、辅助指标和不能恶化的 guardrail 指标分别是什么？", "three_short_texts", []),
    ("DA04", "哪种错误代价更大？", "single_choice", ["误报/错误行动", "漏报/错过机会", "高估", "低估", "不同人群代价不同", "两者接近", "无法判断"]),
    ("DA05", "使用者需要理解到什么程度？", "single_choice", ["只需可靠结果", "整体驱动因素", "个体级解释", "可审计公式和中间计算", "向非技术受众解释", "监管审查", "不确定"]),
    ("DA06", "你是否需要回答“某行动导致了什么”，还是描述/预测已经足够？", "single_choice", ["描述即可", "预测即可", "需要因果证据", "需要实验/准实验", "应由AI判断并说明限制", "不适用"]),
    ("DA07", "数据有哪些使用限制？", "multiple_choice", ["含个人信息", "含商业机密", "只能本地处理", "不能连接外部数据", "需要去标识化", "授权/许可证限制", "没有额外限制", "不确定", "其他"]),
    ("DA08", "可用的计算资源和完成时限是什么？", "multiple_choice", ["普通办公电脑", "CPU服务器", "GPU", "云资源", "只能电子表格", "没有固定限制", "结果需当天", "一周内", "更长周期", "其他"]),
    ("DA09", "最终分析需要达到什么复现程度？", "single_choice", ["一次性结论", "保留公式和步骤", "可运行notebook/script", "自动更新管线", "审计日志和版本固定", "不确定"]),
    ("DA10", "分析结果将如何交付或持续使用？", "multiple_choice", ["静态报告", "电子表格", "notebook", "dashboard", "API/模型服务", "定期更新", "一次性决策会议", "其他", "尚不确定"]),
]:
    Q.append(question(qid, "B3-DA", text, qtype, options=options, display="vertical=data_analysis", origin="prompted"))

Q.append(question("REVIEW01", "B4", "你可以修正错别字或明确歧义；因后续选项产生的新补充请写在补充说明中。", "readonly_plus_open_addendum", origin="prompted", notes="不得覆盖B1首次快照"))

# Wave C confirmation
Q += [
    question("F01", "C1", "这条内容是否准确表达了你在该任务中的真实情况？", "single_choice_per_fact", options=["准确，保留", "基本准确但需要修改", "不准确，删除", "我不确定"], variable="ledger_fact.{fact_id}.status"),
    question("F02", "C1", "请改成更准确的表述。只写对这个任务确实成立的内容。", "open_text_per_fact", display="F01=基本准确但需要修改", variable="ledger_fact.{fact_id}.edited_value"),
    question("F03", "C1", "这条内容对结果是否可用有多重要？", "single_choice_per_fact", options=["违反就不可用", "非常重要", "有帮助但可折中", "只是背景", "其实没有偏好", "不确定"], display="F01 in [保留,修改,不确定]", variable="ledger_fact.{fact_id}.importance"),
    question("F04", "C1", "这条要求可以有多大调整空间？", "single_choice_per_fact", options=["固定不能变", "有限调整", "高度灵活", "多种方案都可接受", "不适用/不确定"], display="F01 in [保留,修改,不确定]", variable="ledger_fact.{fact_id}.flexibility"),
    question("F05", "C1", "哪些替代方案仍然可以接受？如果没有或不知道，可以留空。", "open_text_per_fact", required=False, display="F01 in [保留,修改,不确定]", variable="ledger_fact.{fact_id}.acceptable_alternatives"),
    question("F06", "C1", "这条事实在什么情况下会失效或需要重新确认？", "multiple_choice_per_fact", options=["某个日期后", "项目阶段变化", "预算/资源变化", "团队/受众变化", "政策/技术变化", "目前没有明确失效条件", "不确定", "其他"], display="F01 in [保留,修改,不确定]", variable="ledger_fact.{fact_id}.expiry_condition"),
    question("F07", "C1", "请分别选择这条内容是否可用于后台评价、是否可在实验条件中展示给AI、是否可去标识化公开。", "three_independent_permissions_per_fact", options=["是", "否", "需再次确认"], variable="ledger_fact.{fact_id}.permissions"),
    question("L01", "C2", "作为“你在这个具体任务中的需求记录”，这份总结整体是否足够准确？", "single_choice", options=["可以确认", "需要再修改", "仍有重要误解", "我不愿继续使用这份总结"], variable="ledger.overall_accuracy"),
    question("L02", "C2", "是否遗漏了任何会真实改变最终决定、实现方案或交付形式的重要因素？", "open_text", variable="ledger.missing_facts", origin="confirmation_added"),
    question("L03", "C2", "是否有任何内容让你觉得系统根据身份、专业、年龄、性别或其他背景做了没有依据的推断？", "single_choice_plus_open", options=["没有", "有", "不确定"], variable="ledger.stereotype_report"),
    question("L04", "C2", "我确认：保留下来的内容在当前时间点能较准确表达我对该任务的需求；我知道仍可按研究说明申请撤回。", "single_choice", options=["确认", "暂不确认"], variable="ledger.final_confirmation", notes="暂不确认→不得进入pair/CDM gold"),
]


DOMAIN_TAGS = {
    "DA001": ["finance", "payments", "risk", "data"], "DA002": ["product", "internet", "marketing", "data"],
    "DA003": ["retail", "operations", "finance", "data"], "DA004": ["healthcare", "operations", "data"],
    "DA005": ["public_policy", "climate", "energy", "geospatial"], "DA006": ["research", "climate", "funding", "data"],
    "DA007": ["finance", "accounting", "spreadsheet"], "DA008": ["finance", "accounting", "operations", "spreadsheet"],
    "DA009": ["management", "operations", "business_intelligence", "spreadsheet"], "DA010": ["finance", "startup", "spreadsheet"],
    "DA011": ["product", "marketing", "machine_learning"], "DA012": ["finance", "risk", "machine_learning"],
    "DA013": ["retail", "supply_chain", "forecasting"], "DA014": ["manufacturing", "computer_vision", "machine_learning"],
    "DA015": ["product", "experimentation", "statistics"], "DA016": ["education", "research", "causal_inference"],
    "DA017": ["crm", "sales", "data_engineering"], "DA018": ["environment", "geospatial", "research", "data_engineering"],
    "DR001": ["academia", "education", "career"], "DR002": ["entrepreneurship", "education", "ai_product"],
    "DR003": ["career", "international_mobility"], "DR004": ["creative_writing", "publishing"],
    "DR005": ["real_estate", "personal_finance"], "DR006": ["family", "education"],
    "DR007": ["health", "medicine"], "DR008": ["ai", "research", "data"],
    "DR009": ["materials", "manufacturing", "machine_learning"], "DR010": ["materials", "physics", "research"],
    "DR011": ["investment", "personal_finance"], "DR012": ["ai", "legal", "compliance", "product"],
    "DR013": ["ai", "product", "engineering"], "DR014": ["remote_sensing", "geospatial", "research"],
    "DR015": ["battery", "materials", "research"], "DR016": ["legal", "compliance", "ai", "multilingual"],
    "DR017": ["privacy", "ai", "patent"], "DR018": ["spreadsheet", "ai", "patent"],
    "DR019": ["skincare", "consumer", "health"], "DR020": ["family", "education", "psychology"],
    "DR021": ["travel", "business"], "DR022": ["legal", "compliance", "ai", "product"],
    "DR023": ["quantum", "research"], "DR024": ["water", "environment", "industry"],
    "SW001": ["web", "backend"], "SW002": ["scientific_computing", "python"],
    "SW003": ["machine_learning", "mlops", "api"], "SW004": ["backend", "security", "compliance"],
    "SW005": ["ai", "search", "plugins"], "SW006": ["backend", "web", "datetime"],
    "SW007": ["symbolic_computing", "scientific_computing"], "SW008": ["data_visualization", "python"],
    "SW009": ["distributed_systems", "testing"], "SW010": ["data_engineering", "performance"],
    "SW011": ["documentation", "build_systems"], "SW012": ["machine_learning", "api", "backend"],
    "SW013": ["ai", "search", "architecture"], "SW014": ["backend", "distributed_systems", "architecture"],
    "SW015": ["sre", "observability"], "SW016": ["security", "devops"],
    "SW017": ["scientific_computing", "api"], "SW018": ["machine_learning", "research", "reproducibility"],
}

PERSONAL_DECISION_DR = {"DR001", "DR003", "DR004", "DR005", "DR006", "DR007", "DR011", "DR019", "DR020", "DR021"}
HYBRID_DR = {"DR002", "DR012", "DR013", "DR022"}


QUALITY_RULES = [
    {"rule_id": "QC-H01", "kind": "hard", "condition": "no_consent_or_under_18", "action": "terminate_and_do_not_collect_more"},
    {"rule_id": "QC-H02", "kind": "hard", "condition": "no_task_passes_relevance_experience_safe_answerability", "action": "record_nonmatch_and_end_without_forcing_selection"},
    {"rule_id": "QC-H03", "kind": "hard_after_manual_review", "condition": "empty_gibberish_or_fully_off_topic_open_text", "action": "exclude_task_record_not_other_valid_records"},
    {"rule_id": "QC-H04", "kind": "hard_after_multiple_signals", "condition": "confirmed_duplicate_or_fraud", "action": "exclude_with_audit_reason"},
    {"rule_id": "QC-H05", "kind": "hard_for_gold", "condition": "ledger_not_finally_confirmed_or_no_backend_permission", "action": "do_not_enter_pair_or_CDM_gold"},
    {"rule_id": "QC-S01", "kind": "soft", "condition": "time_below_one_third_of_pilot_median", "action": "manual_review_not_auto_exclude"},
    {"rule_id": "QC-S02", "kind": "soft", "condition": "background_task_contradiction", "action": "neutral_followup_allow_correction_or_explanation"},
    {"rule_id": "QC-S03", "kind": "soft", "condition": "repeated_text_across_tasks", "action": "manual_specificity_review"},
    {"rule_id": "QC-S04", "kind": "soft", "condition": "comprehension_check_failed_twice", "action": "manual_review"},
    {"rule_id": "QC-S05", "kind": "instrument", "condition": "many_user_edits_or_deletions_in_wave_C", "action": "audit_normalizer_before_blaming_participant"},
    {"rule_id": "QC-P01", "kind": "prohibited", "condition": "AI_text_detector_only", "action": "never_auto_exclude"},
    {"rule_id": "QC-P02", "kind": "prohibited", "condition": "neutral_or_noncontrastive_user", "action": "retain_if_real_and_confirmed"},
    {"rule_id": "QC-P03", "kind": "prohibited", "condition": "disagrees_with_llm_summary", "action": "never_penalize_or_withhold_payment"},
]


def load_tasks():
    return [json.loads(line) for line in TASKS_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]


def build_task_artifacts(tasks):
    cards, routes = [], []
    for task in tasks:
        tid = task["task_id"]
        prompt = task["task_prompt_zh"]
        situation = prompt.split("\n\n", 1)[0].strip()
        delivery = ""
        for line in prompt.splitlines():
            if line.startswith("最终交付："):
                delivery = line.removeprefix("最终交付：").strip()
        if task["vertical"] == "software_engineering":
            participant_basis = "professional_or_substantial_hands_on_experience"
            min_level = 2
        elif task["vertical"] == "data_analysis":
            participant_basis = "professional_research_or_decision_user"
            min_level = 1 if task["subtype"] in {"exploratory_business_analysis", "spreadsheet_workflow"} else 2
        elif tid in PERSONAL_DECISION_DR:
            participant_basis = "real_personal_decision_role_or_domain_experience"
            min_level = 0
        elif tid in HYBRID_DR:
            participant_basis = "real_decision_role_or_professional_domain_experience"
            min_level = 1
        else:
            participant_basis = "professional_or_research_domain_experience"
            min_level = 2
        cards.append({
            "task_id": tid,
            "vertical": task["vertical"],
            "subtype": task["subtype"],
            "title_zh": task["title_zh"],
            "situation_zh": situation,
            "possible_delivery_zh": delivery,
            "participant_instruction_zh": "你现在不需要完成任务，只需判断它是否与你的现实情况有关。",
            "risk_level": task["risk_level"],
            "card_must_not_display": task["personalization_design"]["eligible_counterfactual_axes"],
            "card_version": "0.56",
        })
        routes.append({
            "task_id": tid,
            "vertical": task["vertical"],
            "subtype": task["subtype"],
            "domain_tags": DOMAIN_TAGS[tid],
            "required_tools": task["required_tools"],
            "participant_basis": participant_basis,
            "minimum_vertical_experience_level_0_to_4": min_level,
            "task_level_relevance_required": True,
            "task_level_experience_required": True,
            "safe_nonconfidential_answer_required": True,
            "paper_first": task["paper_first"]["included"],
            "risk_level": task["risk_level"],
            "expert_review_required_for_technical_truth": task["expert_review_required"],
            "demographics_allowed_for_routing": False,
            "route_version": "0.56",
        })
    return cards, routes


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    tasks = load_tasks()
    if len(tasks) != 60:
        raise SystemExit(f"expected 60 tasks, found {len(tasks)}")
    missing = sorted(set(task["task_id"] for task in tasks) - set(DOMAIN_TAGS))
    extra = sorted(set(DOMAIN_TAGS) - set(task["task_id"] for task in tasks))
    if missing or extra:
        raise SystemExit(f"domain tag mismatch missing={missing} extra={extra}")
    cards, routes = build_task_artifacts(tasks)
    write_json(OUT / "pages.json", PAGES)
    write_json(OUT / "question_bank.json", Q)
    write_jsonl(OUT / "task_cards.jsonl", cards)
    write_jsonl(OUT / "routing_matrix.jsonl", routes)
    write_json(OUT / "quality_rules.json", QUALITY_RULES)

    manifest_files = [
        OUT / "pages.json", OUT / "question_bank.json", OUT / "task_cards.jsonl",
        OUT / "routing_matrix.jsonl", OUT / "quality_rules.json", SPEC_PATH, PROTOCOL_PATH,
    ]
    manifest = {
        "package": "credamo_persona_survey_v0_56",
        "version": "0.56",
        "status": "implementation_ready_pending_ethics_and_platform_pilot",
        "counts": {"pages": len(PAGES), "question_templates": len(Q), "task_cards": len(cards), "routes": len(routes), "quality_rules": len(QUALITY_RULES)},
        "source_task_pool": str(TASKS_PATH.relative_to(ROOT)),
        "files": {str(path.relative_to(ROOT)): sha256(path) for path in manifest_files},
    }
    write_json(OUT / "manifest.json", manifest)


if __name__ == "__main__":
    main()
