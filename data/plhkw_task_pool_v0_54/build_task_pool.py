#!/usr/bin/env python3
"""Build the v0.54 PLHKW candidate pool and provisional 60-family main set.

Only task shells and pre-pilot design metadata are frozen here. Persona facts,
contracts, evidence snapshots, executable environments, and human validation are
deliberately out of scope and must not be inferred from these records.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import html
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PDR_DIR = ROOT / "data" / "pdr_import_v0_51"

STATUS = "provisional_selected_requires_human_and_environment_validation"

# The paper-first queue is an environment-binding priority list, not a gold claim.
# It spans five DR reasoning shapes, three software shapes, and four data shapes;
# its five signal modes are as balanced as possible over 12 families (2/2/3/2/3).
PAPER_FIRST_IDS = [
    "DR001", "DR008", "DR014", "DR020", "DR022",
    "SW001", "SW007", "SW013",
    "DA003", "DA007", "DA011", "DA015",
]
SIGNAL_CYCLE = [
    "explicit_constraints",
    "goal_tradeoff",
    "knowledge_and_audience",
    "history_grounded_latent_preference",
    "interactive_information_acquisition",
]

SOURCES = {
    "pdr_bench": {
        "title": "PDR-Bench",
        "url": "https://github.com/OPPO-PersonalAI/PersonalizedDeepResearchBench",
        "paper": "https://arxiv.org/abs/2509.25106",
        "license": "Apache-2.0",
        "use_policy": "direct_task_reuse_with_attribution",
        "snapshot": "5b43f9f188c747d154fc7666812ab93b7ca6a3c2",
    },
    "deepresearch_bench": {
        "title": "DeepResearch Bench",
        "url": "https://github.com/Ayanami0730/deep_research_bench",
        "paper": "https://arxiv.org/abs/2506.11763",
        "license": "Apache-2.0",
        "use_policy": "adapt_prompt_with_attribution",
        "snapshot": "accessed_2026-08-16",
    },
    "researcherbench": {
        "title": "ResearcherBench",
        "url": "https://github.com/GAIR-NLP/ResearcherBench",
        "paper": "https://arxiv.org/abs/2507.16280",
        "license": "no_repository_license_detected_on_2026-08-16",
        "use_policy": "structure_only_no_verbatim_prompt_copy",
        "snapshot": "accessed_2026-08-16",
    },
    "livedrbench": {
        "title": "LiveDRBench",
        "url": "https://github.com/microsoft/livedrbench",
        "paper": "https://arxiv.org/abs/2508.04183",
        "license": "dataset_CDLA-Permissive-2.0; code_MIT",
        "use_policy": "problem_inversion_and_claim_discovery_structure",
        "snapshot": "accessed_2026-08-16",
    },
    "swe_bench_verified": {
        "title": "SWE-bench Verified",
        "url": "https://www.swebench.com/SWE-bench/guides/quickstart/",
        "paper": "https://arxiv.org/abs/2310.06770",
        "license": "MIT_harness; repository_specific_code_licenses",
        "use_policy": "real_repo_shell_and_invariant_test_pattern; personalized_overlay_is_new",
        "snapshot": "repo_instance_binding_pending",
    },
    "paperbench": {
        "title": "PaperBench",
        "url": "https://github.com/openai/frontier-evals/tree/main/project/paperbench",
        "paper": "https://arxiv.org/abs/2504.01848",
        "license": "mixed; per-paper assets require separate audit",
        "use_policy": "replication_workflow_structure_only_until_asset_audit",
        "snapshot": "paper_binding_pending",
    },
    "scienceagentbench": {
        "title": "ScienceAgentBench",
        "url": "https://github.com/OSU-NLP-Group/ScienceAgentBench",
        "paper": "https://arxiv.org/abs/2410.05080",
        "license": "most_tasks_CC-BY-4.0; code_MIT; exceptions_require_audit",
        "use_policy": "scientific_program_workflow_structure; avoid_exception_instances",
        "snapshot": "verified_split_binding_pending",
    },
    "dabstep": {
        "title": "DABstep",
        "url": "https://huggingface.co/datasets/adyen/DABstep",
        "paper": "https://arxiv.org/abs/2506.23719",
        "license": "CC-BY-4.0",
        "use_policy": "multi_source_financial_analysis_structure_with_attribution",
        "snapshot": "task_binding_pending",
    },
    "dsbench": {
        "title": "DSBench",
        "url": "https://github.com/LiqiangJing/DSBench",
        "paper": "https://arxiv.org/abs/2409.07703",
        "license": "noncommercial_dataset_terms_and_upstream_rights",
        "use_policy": "structure_only; do_not_redistribute_upstream_data",
        "snapshot": "task_binding_pending",
    },
    "datascibench": {
        "title": "DataSciBench",
        "url": "https://github.com/THUDM/DataSciBench",
        "paper": "https://arxiv.org/abs/2502.13897",
        "license": "repository_and_dataset_license_audit_pending",
        "use_policy": "Task-Function-Code_verifier_structure_only",
        "snapshot": "task_binding_pending",
    },
    "spreadsheetbench2": {
        "title": "SpreadsheetBench 2",
        "url": "https://github.com/RUCKBReasoning/SpreadsheetBench-2",
        "paper": "https://arxiv.org/abs/2606.29955",
        "license": "repository_and_dataset_license_audit_pending",
        "use_policy": "workflow_structure_only_until_license_and_workbook_audit",
        "snapshot": "task_binding_pending",
    },
    "mle_bench": {
        "title": "MLE-bench",
        "url": "https://github.com/openai/mle-bench",
        "paper": "https://arxiv.org/abs/2410.07095",
        "license": "MIT_code; Kaggle_competition_terms_apply_to_data",
        "use_policy": "environment_and_grading_pattern; competition_data_not_redistributed",
        "snapshot": "competition_binding_pending",
    },
    "plhkw_authored": {
        "title": "DeepAlign/PLHKW author-designed gap fillers",
        "url": "local",
        "paper": None,
        "license": "project_owned",
        "use_policy": "new_task_shell",
        "snapshot": "v0.54",
    },
    "real_workflow_adaptation": {
        "title": "Adapted real-world workflow shell",
        "url": "binding_pending",
        "paper": None,
        "license": "source_binding_and_license_audit_required",
        "use_policy": "no_third_party_text_or_assets_in_v0.54",
        "snapshot": "binding_pending",
    },
}


def spec(
    task_id,
    vertical,
    subtype,
    title_zh,
    title_en,
    source_id,
    source_locator,
    source_class,
    scenario_zh,
    scenario_en,
    steps_zh,
    steps_en,
    deliverable_zh,
    deliverable_en,
    reasoning,
    axes,
    invariant_checks,
    conditional_checks,
    tools,
    risk="medium",
):
    return {
        "task_id": task_id,
        "vertical": vertical,
        "subtype": subtype,
        "title_zh": title_zh,
        "title_en": title_en,
        "source_id": source_id,
        "source_locator": source_locator,
        "source_class": source_class,
        "scenario_zh": scenario_zh,
        "scenario_en": scenario_en,
        "steps_zh": steps_zh,
        "steps_en": steps_en,
        "deliverable_zh": deliverable_zh,
        "deliverable_en": deliverable_en,
        "reasoning_structures": reasoning,
        "counterfactual_axes": axes,
        "invariant_checks": invariant_checks,
        "user_conditioned_checks": conditional_checks,
        "required_tools": tools,
        "risk": risk,
    }


NON_PDR = [
    # Deep Research: 6 mature/adapted/new tasks in addition to 12 PDR shells.
    spec("DR008", "deep_research", "literature_synthesis", "复杂多引文 RAG 的高质量训练数据方案", "Training data for complex multi-citation RAG", "researcherbench", "question_1_structure_only", "existing_benchmark_derived", "研究团队正在改进一个需要多跳检索和精确归因的领域问答系统。简单单引文问题表现良好，但复杂问题的覆盖率和引用准确率明显下降。", "A research team is improving a domain QA system that requires multi-hop retrieval and precise attribution. Simple single-citation questions work, while complex questions fail on coverage and citation accuracy.", ["系统梳理复杂问答、合成数据、归因学习与数据质量控制方法", "区分教师错误、问题难度分布偏移和训练目标错配", "比较至少三条数据构造路线并提出消融和人工审计方案", "给出可执行的数据课程、质量门和失败停止条件"], ["Review methods for complex QA, synthetic data, attribution learning, and quality control", "Separate teacher error, difficulty-distribution shift, and objective mismatch", "Compare at least three construction routes with ablations and human audit", "Deliver an executable curriculum, quality gates, and stop conditions"], "一份含证据矩阵、候选方案比较、实验设计和数据生产流程的研究决策报告。", "A research decision report with an evidence matrix, alternatives, experiments, and data-production workflow.", ["literature_landscape", "causal_diagnosis", "method_comparison", "experiment_design"], ["risk_tolerance", "available_annotation_budget", "target_domain", "team_expertise"], ["claims_cited", "alternatives_compared", "teacher_error_measured"], ["recommended_pipeline", "human_review_allocation", "evaluation_thresholds"], ["web_search", "paper_fetch", "citation_manager"], "medium"),
    spec("DR009", "deep_research", "literature_synthesis", "材料配比优化中的机器学习路线与产业化距离", "ML routes for materials-composition optimization", "deepresearch_bench", "query_8_adapted", "existing_benchmark_derived", "材料研发团队希望评估机器学习或深度学习优化元素组合与材料性能的研究进展，并判断何种路线值得进入小规模验证。", "A materials R&D team wants to assess machine-learning approaches to composition optimization and decide which route merits a small-scale validation.", ["检索近年代表性模型、数据库、实验闭环和活跃团队", "比较预测精度、外推能力、数据效率和实验成本", "核查论文结果是否有独立复现或产业证据", "提出从文献证据到实验验证和产业化的分阶段路线"], ["Find recent models, databases, closed-loop experiments, and active groups", "Compare accuracy, extrapolation, data efficiency, and experimental cost", "Check independent replication and industrial evidence", "Propose staged validation and commercialization"], "研究版图、证据质量表、候选路线排序和实验里程碑。", "A landscape, evidence-quality table, ranked routes, and experimental milestones.", ["literature_landscape", "evidence_grading", "technology_readiness", "decision_under_uncertainty"], ["material_system", "lab_equipment", "budget", "acceptable_failure_cost"], ["source_traceability", "metric_comparability", "replication_status"], ["route_priority", "experiment_scale", "readiness_threshold"], ["web_search", "paper_fetch", "dataset_search"], "high"),
    spec("DR010", "deep_research", "literature_synthesis", "单原子催化中的外加电场计算建模", "External-field modeling for single-atom catalysis", "deepresearch_bench", "query_9_adapted", "existing_benchmark_derived", "计算化学团队需要在分子朝向不确定的单原子催化体系中模拟外加电场，避免把固定笛卡尔方向误当作真实反应场。", "A computational chemistry team must model external fields in single-atom catalysis where molecular orientation is uncertain, without treating one Cartesian direction as the physical field.", ["比较固定方向场、取向平均、反应坐标对齐和显式界面模型", "检索各方法的物理假设、软件实现与验证案例", "识别边界条件、数值稳定性和可比性风险", "设计最小计算实验以判别候选方法"], ["Compare fixed-axis, orientation-averaged, reaction-coordinate, and explicit-interface models", "Retrieve physical assumptions, software implementations, and validations", "Identify boundary, stability, and comparability risks", "Design a minimal discriminating computation"], "方法学报告、计算协议、验证矩阵和推荐建模路径。", "A methods report, computation protocol, validation matrix, and recommended path.", ["technical_synthesis", "assumption_audit", "model_comparison", "experiment_design"], ["available_software", "compute_budget", "system_symmetry", "required_fidelity"], ["physical_assumptions_explicit", "reproducible_protocol", "numerical_checks"], ["method_choice", "sampling_depth", "validation_priority"], ["web_search", "paper_fetch", "code_documentation"], "high"),
    spec("DR013", "deep_research", "open_consulting", "垂直领域模型：领域微调还是检索增强", "Domain model strategy: fine-tuning or retrieval", "researcherbench", "question_17_structure_adapted", "adapted_real_world", "一个小型团队要把通用模型落地到垂直领域，需要在领域推理微调、检索增强和混合方案之间做研究与工程决策。", "A small team is deploying a general model in a vertical domain and must choose among domain reasoning fine-tuning, retrieval augmentation, and hybrid routes.", ["建立数据变化速度、可验证性、隐私、维护和成本的决策框架", "检索各路线的最新实证与失败案例", "提出两到三个可证伪的最小原型", "给出分阶段升级和退出条件"], ["Build a decision framework for data velocity, verifiability, privacy, maintenance, and cost", "Retrieve recent evidence and failures", "Define falsifiable minimum prototypes", "Provide staged escalation and exit conditions"], "面向技术负责人的选择备忘录、证据表和试验计划。", "A technical-lead decision memo, evidence table, and trial plan.", ["open_consulting", "tradeoff_analysis", "evidence_synthesis", "experiment_design"], ["team_size", "data_governance", "latency_budget", "change_rate"], ["common_baseline", "cost_model", "evaluation_protocol"], ["architecture_choice", "prototype_order", "stop_rule"], ["web_search", "paper_fetch", "cost_calculator"], "medium"),
    spec("DR014", "deep_research", "dataset_resource_discovery", "遥感灾害识别数据集的约束式发现与谱系核验", "Constraint-based discovery of remote-sensing hazard datasets", "livedrbench", "NovelDatasets_and_extraction_structure", "existing_benchmark_derived", "研究者需要找到可用于跨地区灾害识别的公开遥感数据集，并确认标注对象、空间分辨率、时间覆盖、许可证和数据谱系。", "A researcher needs public remote-sensing datasets for cross-region hazard detection and must verify labels, spatial resolution, temporal coverage, licenses, and lineage.", ["根据性质组合进行宽搜而不是按单一名称查找", "核对原始论文、数据卡、版本和镜像之间的谱系", "排除标签泄漏、地域重叠和许可不兼容", "形成满足不同研究目标的候选集合"], ["Search by property combinations rather than names", "Verify lineage across papers, data cards, versions, and mirrors", "Exclude label leakage, geographic overlap, and license conflicts", "Build candidate sets for different research goals"], "可机读数据集清单、证据链接、排除日志和推荐组合。", "A machine-readable dataset inventory, evidence links, exclusion log, and recommended bundle.", ["claim_discovery", "dataset_lineage", "constraint_satisfaction", "exhaustive_search"], ["target_region", "label_granularity", "compute_budget", "license_policy"], ["dataset_identity", "license_verified", "split_leakage_audited"], ["dataset_bundle", "sampling_strategy", "exclusion_threshold"], ["web_search", "dataset_catalog", "paper_fetch"], "medium"),
    spec("DR015", "deep_research", "dataset_resource_discovery", "电池材料发现数据集与测量条件对齐", "Battery-material dataset discovery with measurement alignment", "livedrbench", "SciFacts_Materials_and_NovelDatasets_structure", "existing_benchmark_derived", "材料研究组需要汇集公开的电池电极性能数据，但不同数据集在温度、倍率、循环定义和材料命名上不一致。", "A materials group needs public battery-electrode performance datasets whose temperature, rate, cycle definitions, and material naming are inconsistent.", ["发现满足化学体系与测量条件的候选数据源", "从论文和数据说明中提取测量协议与字段语义", "识别重复样本、条件不可比和引用链断裂", "提出可合并与不可合并的边界"], ["Discover candidate sources under chemistry and measurement constraints", "Extract protocols and field semantics from papers and documentation", "Detect duplicates, incomparable conditions, and broken provenance", "Define mergeable and non-mergeable boundaries"], "数据资源地图、字段对齐表、谱系图和可用性结论。", "A resource map, schema alignment, lineage graph, and usability decision.", ["dataset_discovery", "schema_alignment", "provenance_reasoning", "conflict_resolution"], ["chemistry_scope", "measurement_tolerance", "modeling_goal", "acceptable_missingness"], ["measurement_conditions_preserved", "duplicates_flagged", "licenses_recorded"], ["merge_policy", "normalization_level", "dataset_priority"], ["web_search", "dataset_catalog", "paper_fetch"], "high"),
    spec("DR016", "deep_research", "dataset_resource_discovery", "多语种 AI 监管语料的版本化构建", "Versioned multilingual AI-regulation corpus", "plhkw_authored", "new_gap_dataset_discovery_1", "newly_authored", "政策研究团队需要构建一个中、美、欧多语种 AI 监管语料，用于比较义务、适用范围和生效时间，并能够在法规更新后增量维护。", "A policy team needs a versioned multilingual AI-regulation corpus spanning China, the US, and the EU for obligations, scope, and effective dates.", ["发现官方法律、监管解释、标准和历史版本", "区分法案、实施规则、指南和非约束性材料", "建立条款级版本、辖区与术语映射", "设计更新检测和冲突处理机制"], ["Find official laws, interpretations, standards, and historical versions", "Separate binding law, implementing rules, guidance, and commentary", "Build clause-level version, jurisdiction, and term mappings", "Design update detection and conflict handling"], "版本化语料 manifest、条款映射、来源等级和维护协议。", "A versioned corpus manifest, clause mapping, source tiers, and maintenance protocol.", ["dataset_discovery", "temporal_versioning", "jurisdiction_reasoning", "ontology_alignment"], ["target_product", "jurisdictions", "risk_posture", "update_frequency"], ["official_source_only_core", "effective_dates", "version_lineage"], ["included_material", "update_sla", "ambiguity_escalation"], ["web_search", "official_document_fetch", "archive_lookup"], "high"),
    spec("DR017", "deep_research", "prior_art", "隐私保护个性化检索的先前技术检索", "Prior-art search for privacy-preserving personalized retrieval", "real_workflow_adaptation", "patent_and_literature_workflow_1", "adapted_real_world", "研发团队计划申请一项本地用户画像与服务器检索结合的技术，需要在提交前系统检索论文、专利和产品公开材料。", "An R&D team plans to file on a hybrid local-profile/server-retrieval technique and needs a systematic pre-filing search across papers, patents, and product disclosures.", ["把拟议方案拆成可检索的技术要素和组合关系", "跨论文、专利族和产品文档搜索并追踪优先权", "区分单要素相似、组合公开和显而易见性风险", "建立支持继续、改写权利要求或停止的证据阈值"], ["Decompose the proposal into searchable elements and combinations", "Search papers, patent families, and product disclosures with priority tracing", "Separate element similarity, combination disclosure, and obviousness risk", "Set evidence thresholds for proceed, narrow, or stop"], "先前技术表、claim chart、检索日志和风险决策备忘录。", "A prior-art table, claim chart, search log, and risk memo.", ["prior_art_search", "claim_decomposition", "temporal_reasoning", "evidence_thresholding"], ["target_claim_scope", "filing_jurisdictions", "novelty_risk_tolerance", "search_budget"], ["priority_dates_verified", "claim_elements_traced", "negative_search_logged"], ["claim_scope", "proceed_decision", "followup_search"], ["web_search", "patent_search", "paper_fetch"], "high"),
    spec("DR018", "deep_research", "prior_art", "电子表格公式修复智能体的先前技术与差异化定位", "Prior art for spreadsheet formula-repair agents", "real_workflow_adaptation", "patent_and_product_workflow_2", "adapted_real_world", "产品团队准备开发能够跨工作表定位并修复公式错误的智能体，需要判断现有学术方法、开源工具、专利和商业产品已经覆盖哪些能力。", "A product team plans an agent that locates and repairs cross-sheet formula errors and must map existing academic methods, open tools, patents, and products.", ["拆解检测、定位、修复、验证和解释五个能力环节", "建立论文—代码—专利—产品的证据链", "核对公开日期、功能边界和可复现实证", "提出可验证的差异化方向及失败条件"], ["Decompose detection, localization, repair, verification, and explanation", "Link papers, code, patents, and products", "Verify disclosure dates, capability boundaries, and reproducibility", "Propose testable differentiation and failure conditions"], "能力地图、先前技术矩阵、空白假设和原型验证计划。", "A capability map, prior-art matrix, gap hypotheses, and prototype plan.", ["prior_art_search", "entity_resolution", "capability_decomposition", "gap_analysis"], ["target_market", "integration_surface", "explainability_need", "defensibility_goal"], ["dates_verified", "capabilities_evidence_linked", "duplicate_entities_merged"], ["product_positioning", "prototype_scope", "novelty_claim"], ["web_search", "patent_search", "code_search"], "medium"),
    spec("DR022", "deep_research", "temporal_update", "AI 监管更新后的产品决策重算", "Recompute product decisions after an AI-regulation update", "plhkw_authored", "new_gap_temporal_update_1", "newly_authored", "产品研究已完成大半时，某一目标市场发布新的实施规则或延迟生效通知；系统必须在保留未受影响证据的同时重算合规与发布建议。", "Midway through product research, a target market issues a new implementing rule or delayed-effective-date notice; the system must recompute the launch advice without discarding unaffected evidence.", ["冻结更新前的证据与初步决策", "核验新文件的权威性、适用范围和生效时间", "定位受影响与不受影响的决策节点", "输出变更日志并与一次性获得新状态的 oracle 对照"], ["Freeze pre-update evidence and preliminary decisions", "Verify authority, scope, and effective date", "Locate affected and unaffected decision nodes", "Produce a change log and compare with a one-shot-new oracle"], "更新后的决策报告、差分说明、旧状态残留审计和证据版本表。", "An updated decision report, diff explanation, stale-state audit, and evidence version table.", ["temporal_update", "dependency_propagation", "conflict_resolution", "stale_state_suppression"], ["launch_market", "release_date", "risk_posture", "ability_to_delay"], ["unaffected_claims_preserved", "source_authority_checked", "old_rule_not_misapplied"], ["launch_decision", "mitigation_scope", "escalation_trigger"], ["web_search", "official_document_fetch", "checkpoint_injection"], "high"),
    spec("DR023", "deep_research", "entity_exhaustive", "量子网络研究团队与成果的可核验全景", "Verifiable landscape of quantum-network research groups", "deepresearch_bench", "query_14_structure_adapted", "existing_benchmark_derived", "科研战略团队需要识别全球量子网络主要研究团队，并比较方向、代表成果、合作、资金与产业转化，而不是按名气罗列。", "A research-strategy team needs a verifiable landscape of quantum-network groups, comparing directions, outputs, collaborations, funding, and translation rather than prestige alone.", ["定义团队实体、时间窗和纳入标准", "跨机构主页、论文、项目与资助记录消歧", "建立完整性审计和遗漏搜索", "按不同合作目标给出候选短名单"], ["Define entity, time window, and inclusion criteria", "Resolve entities across institutional pages, papers, projects, and grants", "Run completeness and missing-entity audits", "Produce shortlists for different collaboration goals"], "实体表、证据链、覆盖率审计和条件化短名单。", "An entity table, evidence chain, coverage audit, and conditional shortlists.", ["entity_enumeration", "entity_resolution", "exhaustive_search", "multi_criteria_comparison"], ["collaboration_goal", "geographic_constraints", "maturity_preference", "time_horizon"], ["entity_identity_verified", "evidence_dates", "coverage_search_logged"], ["shortlist", "ranking_weights", "outreach_priority"], ["web_search", "paper_fetch", "grant_database"], "medium"),
    spec("DR024", "deep_research", "entity_exhaustive", "水务技术产业化案例的全球枚举与可比性审计", "Global enumeration of commercialized water-utility innovations", "plhkw_authored", "new_gap_entity_enumeration_1", "newly_authored", "水务企业希望寻找近十年已经实现规模化经济收益的技术创新案例，并据此决定本地研发重点。", "A water utility wants global innovations with demonstrated scaled economic value over the last decade to prioritize local R&D.", ["预定义产业化、经济收益与同类企业的纳入标准", "枚举公司—技术—项目实体并合并别名", "核查收益口径、规模、时间和第三方证据", "识别幸存者偏差并形成不同能力条件下的技术方向"], ["Predefine commercialization, economic-value, and peer criteria", "Enumerate company-technology-project entities and merge aliases", "Verify value definitions, scale, dates, and independent evidence", "Audit survivorship bias and derive capability-conditioned directions"], "可审计案例库、证据质量表、遗漏日志和研发方向建议。", "An auditable case database, evidence-quality table, omission log, and R&D recommendations.", ["entity_enumeration", "evidence_normalization", "survivorship_bias_audit", "technology_transfer"], ["utility_scale", "local_infrastructure", "capital_budget", "deployment_horizon"], ["economic_metrics_normalized", "third_party_evidence", "entity_deduplication"], ["technology_priorities", "pilot_scale", "partner_shortlist"], ["web_search", "company_filing_search", "official_statistics"], "medium"),

    # Software: 18 repository-level tasks.
    spec("SW001", "software_engineering", "feature_implementation", "为 Web 服务加入可配置缓存层", "Add a configurable caching layer", "swe_bench_verified", "django_style_repo_binding_pending", "existing_benchmark_derived", "在给定 Web 框架仓库中实现可配置的读缓存，处理失效、并发、错误回退和兼容性。", "Implement configurable read caching in a web-framework repository, including invalidation, concurrency, error fallback, and compatibility.", ["调查现有扩展点与调用路径", "比较至少两种实现并记录决策", "实现功能、迁移说明和回退", "补充单元、集成和回归测试"], ["Inspect extension points and call paths", "Compare at least two implementations and record the decision", "Implement functionality, migration, and rollback", "Add unit, integration, and regression tests"], "可运行 patch、测试、设计说明和性能测量。", "A runnable patch, tests, design note, and performance measurements.", ["repo_investigation", "architecture_choice", "implementation", "verification"], ["dependency_policy", "traffic_pattern", "operational_maturity", "latency_goal"], ["functional_tests", "backward_compatibility", "no_regression"], ["cache_backend", "invalidation_policy", "documentation_depth"], ["repo_search", "shell", "test_runner"], "medium"),
    spec("SW002", "software_engineering", "feature_implementation", "为科学数组库增加流式导出", "Add streaming export to a scientific array library", "swe_bench_verified", "xarray_style_repo_binding_pending", "existing_benchmark_derived", "为处理超内存数据的科学数组仓库加入分块流式导出，并保持元数据与坐标语义。", "Add chunked streaming export for out-of-memory datasets while preserving metadata and coordinate semantics.", ["追踪读取、编码和写出链路", "调查后端限制与已有约定", "实现可取消、可恢复的导出路径", "验证数值、元数据、内存峰值与兼容性"], ["Trace read, encoding, and write paths", "Inspect backend limits and conventions", "Implement cancellable and resumable export", "Verify values, metadata, peak memory, and compatibility"], "patch、基准脚本、测试矩阵和使用文档。", "A patch, benchmark script, test matrix, and documentation.", ["repo_investigation", "dataflow_reasoning", "implementation", "performance_validation"], ["dataset_scale", "memory_limit", "backend_choice", "failure_recovery_need"], ["data_equivalence", "metadata_preservation", "existing_api_tests"], ["chunk_strategy", "backend_support", "progress_reporting"], ["repo_search", "shell", "test_runner", "profiler"], "medium"),
    spec("SW003", "software_engineering", "feature_implementation", "为模型评估 API 增加可插拔指标", "Add pluggable metrics to a model-evaluation API", "swe_bench_verified", "scikit_learn_style_repo_binding_pending", "existing_benchmark_derived", "在机器学习库中增加可插拔评估指标，兼容现有 scorer、交叉验证和序列化行为。", "Add pluggable evaluation metrics to an ML library while preserving scorer, cross-validation, and serialization behavior.", ["定位公共 API、内部路由和弃用约束", "设计注册机制与错误语义", "实现并覆盖多输出、样本权重和并行运行", "补充示例与升级说明"], ["Locate public APIs, internal routing, and deprecation constraints", "Design registration and error semantics", "Implement multi-output, sample-weight, and parallel behavior", "Add examples and migration guidance"], "patch、API 文档、兼容测试和设计权衡记录。", "A patch, API docs, compatibility tests, and design tradeoff record.", ["api_design", "repo_investigation", "implementation", "compatibility_testing"], ["extension_frequency", "third_party_plugins", "stability_requirement", "maintenance_capacity"], ["existing_scorers_unchanged", "serialization", "test_suite"], ["registration_surface", "error_policy", "plugin_isolation"], ["repo_search", "shell", "test_runner"], "medium"),
    spec("SW004", "software_engineering", "feature_implementation", "为轻量 API 框架增加审计日志", "Add audit logging to a lightweight API framework", "swe_bench_verified", "flask_style_repo_binding_pending", "existing_benchmark_derived", "在不泄漏敏感载荷的前提下，为轻量 API 框架增加可扩展审计日志与请求关联。", "Add extensible audit logging and request correlation to a lightweight API framework without leaking sensitive payloads.", ["分析请求生命周期与扩展接口", "设计字段、脱敏、采样和失败策略", "实现同步与异步处理兼容", "测试隐私、性能和异常路径"], ["Analyze request lifecycle and extension points", "Design fields, redaction, sampling, and failure policy", "Support sync and async handlers", "Test privacy, performance, and exception paths"], "patch、威胁模型、测试和运维配置示例。", "A patch, threat model, tests, and operational configuration examples.", ["repo_investigation", "security_design", "implementation", "performance_validation"], ["compliance_scope", "payload_sensitivity", "throughput", "observability_stack"], ["no_secret_logging", "request_behavior", "backward_compatibility"], ["logged_fields", "sampling_rate", "storage_adapter"], ["repo_search", "shell", "test_runner", "benchmark"], "high"),
    spec("SW005", "software_engineering", "feature_implementation", "为插件系统加入可替换的语义搜索后端", "Add replaceable semantic-search backends", "real_workflow_adaptation", "open_source_plugin_repo_binding_pending", "adapted_real_world", "为已有插件系统加入语义搜索能力，同时允许本地索引、数据库扩展或托管服务作为可替换后端。", "Add semantic search to an existing plugin system with local, database-extension, and hosted backends.", ["调查仓库接口与部署模型", "定义后端协议、索引生命周期和错误降级", "实现至少一个参考后端与契约测试", "记录不同部署条件下的选型"], ["Inspect repository interfaces and deployment model", "Define backend protocol, index lifecycle, and fallback", "Implement one reference backend and contract tests", "Document choices under deployment regimes"], "patch、后端协议、契约测试、迁移与选型文档。", "A patch, backend protocol, contract tests, migration, and selection guide.", ["architecture_choice", "interface_design", "implementation", "contract_testing"], ["cloud_permission", "data_volume", "ops_capacity", "vendor_lock_in_tolerance"], ["search_api_contract", "existing_plugins", "fallback_behavior"], ["backend_choice", "index_strategy", "dependency_set"], ["repo_search", "shell", "test_runner"], "medium"),
    spec("SW006", "software_engineering", "debugging_remediation", "修复时区序列化回归", "Fix a timezone-serialization regression", "swe_bench_verified", "django_style_repo_binding_pending", "existing_benchmark_derived", "给定 Web 框架中的时区序列化回归和失败测试，定位跨层根因并提供低风险修复。", "Given a timezone-serialization regression and failing tests in a web framework, locate the cross-layer cause and provide a low-risk fix.", ["复现并最小化失败", "追踪解析、规范化和序列化路径", "比较局部修补与语义统一方案", "实现修复并增加边界回归测试"], ["Reproduce and minimize the failure", "Trace parsing, normalization, and serialization", "Compare local patch versus semantic unification", "Implement and add boundary tests"], "根因报告、patch、回归测试和发布风险说明。", "A root-cause report, patch, regression tests, and release-risk note.", ["causal_debugging", "repo_investigation", "remediation", "regression_testing"], ["release_urgency", "compatibility_window", "affected_versions", "risk_tolerance"], ["bug_reproduced", "existing_tests", "timezone_semantics"], ["patch_scope", "backport_plan", "deprecation_notice"], ["repo_search", "shell", "test_runner", "debugger"], "medium"),
    spec("SW007", "software_engineering", "debugging_remediation", "诊断符号化简的内存爆炸", "Diagnose symbolic-simplification memory blow-up", "swe_bench_verified", "sympy_style_repo_binding_pending", "existing_benchmark_derived", "符号计算库在特定表达式上出现内存爆炸，需要定位算法路径并选择修复或保护策略。", "A symbolic-computation library suffers memory blow-up on a class of expressions; locate the algorithmic path and choose repair or guardrails.", ["构造最小复现与规模曲线", "定位递归、缓存或组合爆炸点", "比较精确修复、启发式剪枝和资源上限", "验证正确性与性能回归"], ["Build a minimal reproducer and scaling curve", "Locate recursion, caching, or combinatorial explosion", "Compare exact repair, heuristic pruning, and resource guards", "Verify correctness and performance"], "诊断报告、patch 或防护、基准和回归测试。", "A diagnosis, patch or guard, benchmark, and regression tests.", ["algorithmic_debugging", "complexity_analysis", "remediation", "benchmarking"], ["exactness_requirement", "input_distribution", "resource_limit", "api_stability"], ["mathematical_correctness", "existing_tests", "termination"], ["repair_strategy", "guard_threshold", "fallback_result"], ["repo_search", "shell", "test_runner", "profiler"], "medium"),
    spec("SW008", "software_engineering", "debugging_remediation", "修复日期坐标绘图回归", "Fix a date-axis plotting regression", "swe_bench_verified", "matplotlib_style_repo_binding_pending", "existing_benchmark_derived", "绘图库升级后某类日期坐标、时区和缺失值组合出现渲染回归，需要跨转换器、刻度和后端定位。", "A plotting-library upgrade causes regressions for date axes, time zones, and missing values across converters, ticks, and backends.", ["复现并比较受影响后端", "二分定位语义变化", "检查公共 API 与视觉输出兼容", "补充数值断言和图像回归测试"], ["Reproduce across backends", "Bisect the semantic change", "Check public API and visual compatibility", "Add numeric and image-regression tests"], "patch、根因说明、跨后端测试和兼容评估。", "A patch, root-cause note, cross-backend tests, and compatibility assessment.", ["regression_debugging", "cross_backend_validation", "implementation", "visual_testing"], ["supported_backends", "release_policy", "visual_tolerance", "maintenance_cost"], ["data_mapping", "public_api", "reference_images"], ["patch_scope", "backend_priority", "tolerance_policy"], ["repo_search", "shell", "test_runner", "image_diff"], "low"),
    spec("SW009", "software_engineering", "debugging_remediation", "修复网络重试导致的分布式测试不稳定", "Fix distributed-test flakiness caused by retries", "swe_bench_verified", "pytest_requests_style_binding_pending", "existing_benchmark_derived", "测试框架与 HTTP 客户端组合在网络抖动时出现不稳定重试、重复副作用和偶发超时。", "A test-framework/HTTP-client stack becomes flaky under network jitter, causing retry storms, duplicate side effects, and timeouts.", ["从日志和测试轨迹区分产品 bug 与测试脆弱性", "建立故障注入复现", "比较幂等、退避、fixture 隔离和虚拟时钟方案", "实施修复并验证重复运行稳定性"], ["Separate product bugs from test fragility using logs and traces", "Build a fault-injection reproducer", "Compare idempotency, backoff, fixture isolation, and virtual clocks", "Implement and validate repeated-run stability"], "修复、故障注入测试、稳定性报告和上线建议。", "A fix, fault-injection tests, stability report, and rollout advice.", ["distributed_debugging", "fault_injection", "remediation", "stability_analysis"], ["production_similarity", "test_runtime", "retry_policy", "side_effect_cost"], ["functional_semantics", "repeatability", "no_hidden_sleep"], ["retry_strategy", "test_isolation", "rollout_scope"], ["repo_search", "shell", "test_runner", "network_simulator"], "medium"),
    spec("SW010", "software_engineering", "refactor_optimization", "重构大数组管线以降低峰值内存", "Refactor a large-array pipeline for lower peak memory", "swe_bench_verified", "xarray_style_repo_binding_pending", "existing_benchmark_derived", "科学数据管线功能正确但峰值内存过高，需要在不改变结果与 API 的前提下重构。", "A scientific-data pipeline is correct but uses excessive peak memory and must be refactored without changing outputs or APIs.", ["测量阶段性内存与 I/O", "识别复制、物化和缓存热点", "比较分块、惰性计算与算法替换", "实施并做真实性能与回归验证"], ["Measure stage-level memory and I/O", "Locate copies, materialization, and cache hotspots", "Compare chunking, laziness, and algorithm replacement", "Implement and validate real performance and regressions"], "patch、基准、资源曲线和维护性说明。", "A patch, benchmarks, resource curves, and maintainability note.", ["performance_profiling", "refactoring", "equivalence_testing", "tradeoff_analysis"], ["memory_ceiling", "runtime_tolerance", "team_expertise", "backend_constraints"], ["numerical_equivalence", "api_compatibility", "existing_tests"], ["optimization_path", "chunk_size", "complexity_budget"], ["repo_search", "shell", "test_runner", "profiler"], "medium"),
    spec("SW011", "software_engineering", "refactor_optimization", "重构文档构建缓存与依赖跟踪", "Refactor documentation-build caching", "swe_bench_verified", "sphinx_style_repo_binding_pending", "existing_benchmark_derived", "大型文档站增量构建缓慢且偶发使用陈旧缓存，需要重构依赖跟踪。", "A large documentation site has slow incremental builds and occasional stale-cache results; dependency tracking must be refactored.", ["分析构建图与缓存键", "识别漏依赖和过度失效", "比较保守正确性与细粒度增量策略", "实现并用变更矩阵验证"], ["Analyze the build graph and cache keys", "Find missing dependencies and over-invalidation", "Compare conservative correctness with fine-grained incrementality", "Implement and validate with a change matrix"], "patch、构建图说明、性能/正确性测试和迁移建议。", "A patch, build-graph note, performance/correctness tests, and migration advice.", ["dependency_graph", "cache_invalidation", "refactoring", "matrix_testing"], ["repository_size", "build_frequency", "staleness_tolerance", "plugin_ecosystem"], ["fresh_output", "existing_extensions", "determinism"], ["cache_granularity", "invalidations", "migration_path"], ["repo_search", "shell", "test_runner", "profiler"], "low"),
    spec("SW012", "software_engineering", "refactor_optimization", "迁移模型持久化 API 并控制弃用风险", "Migrate a model-persistence API with controlled deprecation", "real_workflow_adaptation", "ml_library_repo_binding_pending", "adapted_real_world", "机器学习库需要重构模型持久化接口以支持新格式，同时避免破坏旧模型和下游插件。", "An ML library must refactor model persistence for a new format without breaking old models or downstream plugins.", ["调查序列化协议、版本检查和插件使用", "设计双读/双写或转换策略", "实现迁移、告警和回滚", "验证跨版本、跨平台和安全边界"], ["Inspect serialization, version checks, and plugin use", "Design dual-read/write or conversion", "Implement migration, warnings, and rollback", "Validate versions, platforms, and security boundaries"], "patch、迁移工具、兼容矩阵和弃用计划。", "A patch, migration tool, compatibility matrix, and deprecation plan.", ["repo_investigation", "api_migration", "compatibility_testing", "risk_management"], ["support_window", "installed_base", "security_posture", "release_capacity"], ["old_models_load", "new_models_roundtrip", "no_code_execution_regression"], ["migration_mode", "deprecation_timeline", "format_choice"], ["repo_search", "shell", "test_runner", "fixture_matrix"], "high"),
    spec("SW013", "software_engineering", "architecture_dependency", "为知识产品选择向量检索架构", "Choose a vector-search architecture", "plhkw_authored", "new_gap_architecture_1", "newly_authored", "一个已有全文搜索产品要增加语义检索，需要在本地库、PostgreSQL 扩展和托管向量服务之间选择并完成最小实现。", "A full-text-search product needs semantic retrieval and must choose among a local library, a PostgreSQL extension, and a hosted vector service, then implement a minimum path.", ["调查仓库、数据流和部署约束", "建立成本、延迟、隐私、恢复和锁定比较", "写 ADR 并实现最小端到端切片", "用统一相关性与故障测试验证"], ["Inspect repository, data flow, and deployment constraints", "Compare cost, latency, privacy, recovery, and lock-in", "Write an ADR and implement a minimum slice", "Validate with common relevance and failure tests"], "ADR、可运行实现、基准、测试与迁移路径。", "An ADR, runnable implementation, benchmarks, tests, and migration path.", ["architecture_research", "dependency_choice", "implementation", "evaluation"], ["data_residency", "team_size", "traffic", "vendor_tolerance"], ["retrieval_quality", "api_contract", "failure_tests"], ["architecture", "dependency", "operations_plan"], ["repo_search", "web_search", "shell", "test_runner"], "medium"),
    spec("SW014", "software_engineering", "architecture_dependency", "为后台任务选择队列与一致性方案", "Choose a queue and consistency model for background jobs", "plhkw_authored", "new_gap_architecture_2", "newly_authored", "单体应用需要加入可重试后台任务，必须在数据库队列、消息中间件和托管队列之间选择。", "A monolith needs retryable background jobs and must choose among a database queue, message broker, and managed queue.", ["调查事务边界、失败语义和部署现状", "比较至少一次、幂等、顺序和可观测性", "实现一条代表性任务链与故障注入", "给出扩展和回滚条件"], ["Inspect transactions, failure semantics, and deployment", "Compare at-least-once, idempotency, ordering, and observability", "Implement one representative flow with fault injection", "Define scaling and rollback conditions"], "ADR、patch、故障测试、运维手册和容量模型。", "An ADR, patch, fault tests, runbook, and capacity model.", ["architecture_research", "failure_semantics", "implementation", "capacity_planning"], ["operations_capacity", "throughput", "consistency_need", "cloud_permission"], ["job_semantics", "no_duplicate_effect", "recovery"], ["queue_choice", "retry_policy", "deployment_topology"], ["repo_search", "web_search", "shell", "test_runner"], "high"),
    spec("SW015", "software_engineering", "architecture_dependency", "为服务建立可用性优先的可观测性方案", "Design availability-oriented observability", "plhkw_authored", "new_gap_architecture_3", "newly_authored", "在线服务缺少统一日志、指标和追踪，需要选择最小但可维护的可观测性架构并接入仓库。", "An online service lacks coherent logs, metrics, and traces and needs a minimal maintainable observability architecture integrated into the repository.", ["调查关键用户路径和故障模式", "设计 SLI/SLO、采样和数据保留", "比较开源自托管与托管方案", "实现关键路径并验证开销和告警"], ["Inspect critical user journeys and failures", "Design SLI/SLO, sampling, and retention", "Compare self-hosted and managed options", "Implement critical paths and validate overhead and alerts"], "ADR、patch、仪表板/告警配置、成本与演练报告。", "An ADR, patch, dashboard/alert configuration, cost model, and drill report.", ["system_investigation", "architecture_choice", "implementation", "operational_validation"], ["on_call_maturity", "privacy", "budget", "availability_target"], ["service_behavior", "no_sensitive_telemetry", "overhead_bound"], ["telemetry_scope", "tooling", "alert_policy"], ["repo_search", "web_search", "shell", "load_test"], "high"),
    spec("SW016", "software_engineering", "repo_investigation_modification", "跨仓库安全配置审计与最小修复", "Cross-repository security-configuration audit and patch", "real_workflow_adaptation", "security_repo_binding_pending", "adapted_real_world", "一个服务仓库包含应用代码、容器和 CI 配置，需要调查凭据、权限、依赖和默认暴露面，并实施不破坏部署的修复。", "A service repository includes application, container, and CI configuration; investigate credentials, permissions, dependencies, and default exposure, then patch safely.", ["建立入口点、秘密和信任边界地图", "使用静态检查与依赖公告核验问题", "区分真实可利用性和扫描噪声", "实施最小修复、测试和部署说明"], ["Map entry points, secrets, and trust boundaries", "Verify findings with static checks and advisories", "Separate exploitability from scanner noise", "Implement minimal fixes, tests, and deployment guidance"], "审计报告、patch、证据、测试和风险接受项。", "An audit report, patch, evidence, tests, and accepted risks.", ["repo_investigation", "security_research", "remediation", "verification"], ["threat_model", "deployment_privilege", "compatibility_window", "incident_urgency"], ["functional_tests", "secret_absence", "least_privilege"], ["fix_priority", "breaking_change_tolerance", "backport_scope"], ["repo_search", "web_search", "shell", "security_scanner"], "high"),
    spec("SW017", "software_engineering", "repo_investigation_modification", "科学代码仓库的跨版本 API 迁移", "Cross-version API migration in a scientific repository", "scienceagentbench", "verified_non_exception_instance_binding_pending", "adapted_real_world", "科学分析仓库依赖的核心库发生 API 变更，需要理解论文工作流、迁移实现并保证主要数值结果。", "A scientific-analysis repository depends on a library with breaking API changes; understand the paper workflow, migrate, and preserve key numerical results.", ["运行基线并识别真正使用的路径", "查阅新旧 API 和行为差异", "实施迁移与兼容层", "在清洁环境复现主要表/图或数值检查"], ["Run the baseline and identify used paths", "Research old/new APIs and behavioral differences", "Implement migration and compatibility", "Reproduce key figures/tables or numerical checks in a clean environment"], "迁移 patch、环境文件、复现结果和差异报告。", "A migration patch, environment file, reproduced results, and discrepancy report.", ["paper_to_code_mapping", "repo_investigation", "api_migration", "numerical_validation"], ["reproduction_scope", "compute_budget", "support_window", "scientific_tolerance"], ["key_results", "clean_environment", "tests"], ["compatibility_layer", "dependency_pin", "replication_depth"], ["repo_search", "paper_fetch", "shell", "test_runner"], "high"),
    spec("SW018", "software_engineering", "repo_investigation_modification", "在资源约束下复现论文算法并形成可维护代码", "Replicate a paper algorithm under resource constraints", "paperbench", "paper_and_assets_binding_pending", "existing_benchmark_derived", "给定论文、允许的资源和空白代码仓库，复现核心算法与至少一项主结果，同时产出可维护实现。", "Given a paper, allowed resources, and an empty repository, reproduce the core algorithm and at least one main result while producing maintainable code.", ["解析论文方法、数据和评估依赖", "制定资源适配的复现计划", "实现、运行实验并记录偏差", "在清洁容器重跑并编写复现文档"], ["Parse method, data, and evaluation dependencies", "Plan a resource-aware replication", "Implement, run, and document discrepancies", "Rerun in a clean container and write reproducibility docs"], "代码仓库、环境、实验记录、结果表和复现报告。", "A code repository, environment, experiment log, result table, and replication report.", ["paper_understanding", "implementation", "experiment_execution", "reproducibility"], ["compute_budget", "fidelity_target", "maintenance_need", "audience_expertise"], ["core_method_present", "clean_execution", "result_tolerance"], ["replication_scope", "optimization_depth", "documentation_level"], ["paper_fetch", "repo_search", "shell", "test_runner", "experiment_runner"], "high"),

    # Data: 18 analysis, spreadsheet, modeling, experiment, and integration tasks.
    spec("DA001", "data_analysis", "exploratory_business_analysis", "支付欺诈与批准率的分群权衡分析", "Segmented tradeoff analysis of payment fraud and approval", "dabstep", "payments_task_binding_pending", "existing_benchmark_derived", "给定匿名交易表、支付规则文档和费用说明，分析欺诈损失、误拒和批准率之间的分群权衡。", "Given anonymized transactions, payment-rule documents, and fee schedules, analyze segmented tradeoffs among fraud loss, false declines, and approval.", ["读取并核对表结构与文档规则", "构造可复算的分群指标", "定位异常与规则变化影响", "做敏感性分析并形成行动建议"], ["Inspect tables and rule documents", "Build reproducible segment metrics", "Locate anomalies and rule-change effects", "Run sensitivity analysis and make recommendations"], "分析 notebook、结果表、图表、假设日志和决策备忘录。", "An analysis notebook, result tables, charts, assumption log, and decision memo.", ["multi_source_analysis", "segmentation", "tradeoff_analysis", "sensitivity_analysis"], ["false_positive_cost", "growth_priority", "risk_limit", "decision_audience"], ["metric_recalculation", "join_correctness", "document_rules_applied"], ["segment_priority", "thresholds", "recommended_action"], ["python", "sql", "document_reader"], "high"),
    spec("DA002", "data_analysis", "exploratory_business_analysis", "订阅产品的 cohort 留存与价值诊断", "Cohort retention and value diagnosis", "dsbench", "analysis_task_shell_binding_pending", "existing_benchmark_derived", "给定多表订阅、账单、活动和客服数据，解释增长放缓来自获客、激活、留存还是价格。", "Given multi-table subscription, billing, activity, and support data, diagnose whether slowing growth comes from acquisition, activation, retention, or pricing.", ["审计主键、时间窗和口径", "构造 cohort、漏斗和单位经济指标", "检验替代解释与数据缺口", "按目标角色输出决策优先级"], ["Audit keys, windows, and definitions", "Build cohorts, funnels, and unit economics", "Test alternative explanations and data gaps", "Prioritize decisions for the target role"], "可复现 notebook、指标字典、图表与管理备忘录。", "A reproducible notebook, metric dictionary, charts, and management memo.", ["multi_table_analysis", "cohort_reasoning", "causal_caution", "decision_support"], ["role_goal", "time_horizon", "risk_tolerance", "metric_literacy"], ["join_integrity", "cohort_definitions", "totals_reconcile"], ["metric_emphasis", "visualization", "action_priority"], ["python", "sql"], "medium"),
    spec("DA003", "data_analysis", "exploratory_business_analysis", "零售品类增长与毛利冲突诊断", "Retail growth-versus-margin diagnosis", "dsbench", "analysis_task_shell_binding_pending", "existing_benchmark_derived", "给定门店、订单、促销、库存和退货数据，识别收入增长与毛利恶化的共同原因。", "Given store, order, promotion, inventory, and return data, identify drivers of revenue growth and margin deterioration.", ["统一 SKU、门店和促销口径", "分解价格、数量、组合、折扣和退货效应", "检查季节性和数据截断", "生成角色条件化的行动组合"], ["Align SKU, store, and promotion definitions", "Decompose price, volume, mix, discount, and return effects", "Check seasonality and truncation", "Generate role-conditioned action portfolios"], "分析 workbook/notebook、桥接图、异常表和决策建议。", "An analysis workbook/notebook, bridge chart, anomaly table, and recommendations.", ["data_reconciliation", "variance_decomposition", "confound_audit", "decision_support"], ["profit_priority", "growth_priority", "inventory_risk", "audience"], ["financial_reconciliation", "consistent_filters", "reproducible_metrics"], ["category_focus", "promotion_policy", "visual_summary"], ["python", "spreadsheet"], "medium"),
    spec("DA004", "data_analysis", "exploratory_business_analysis", "医院运营瓶颈与等待时间分析", "Hospital bottleneck and wait-time analysis", "real_workflow_adaptation", "health_operations_dataset_binding_pending", "adapted_real_world", "给定去标识化就诊流程、排班和资源数据，定位等待时间瓶颈，同时避免把相关性误写成临床因果。", "Given de-identified patient-flow, staffing, and resource data, locate wait-time bottlenecks without turning associations into clinical causal claims.", ["审计隐私、缺失和时间戳", "构建流程阶段与队列指标", "分层检查病例组合和排班混杂", "提出可逆运营试点与监测指标"], ["Audit privacy, missingness, and timestamps", "Build process-stage and queue metrics", "Stratify case mix and staffing confounds", "Propose reversible operational pilots and monitoring"], "去标识化分析、流程图、敏感性结果和试点方案。", "A de-identified analysis, process map, sensitivity results, and pilot plan.", ["process_mining", "confound_analysis", "privacy_audit", "experiment_planning"], ["service_goal", "equity_priority", "staffing_flexibility", "risk_posture"], ["privacy_checks", "time_order", "metric_reproducibility"], ["bottleneck_priority", "pilot_choice", "monitoring_threshold"], ["python", "sql", "process_mining"], "high"),
    spec("DA005", "data_analysis", "exploratory_business_analysis", "城市能耗与减排项目组合分析", "Municipal energy and decarbonization portfolio analysis", "real_workflow_adaptation", "municipal_energy_data_binding_pending", "adapted_real_world", "给定建筑、天气、能源账单和项目成本数据，识别节能潜力并形成受预算和公平约束的项目组合。", "Given building, weather, utility-bill, and project-cost data, identify efficiency potential and build a budget- and equity-constrained portfolio.", ["对齐建筑实体、天气和账期", "建立基线并做气候归一化", "估算节能、成本、不确定性和分配影响", "比较项目组合与分阶段执行"], ["Align buildings, weather, and billing periods", "Build weather-normalized baselines", "Estimate savings, cost, uncertainty, and distributional effects", "Compare portfolios and staged execution"], "分析 notebook、项目组合表、地图/图表和决策备忘录。", "An analysis notebook, portfolio table, maps/charts, and decision memo.", ["data_integration", "normalization", "portfolio_optimization", "uncertainty_analysis"], ["budget", "equity_goal", "carbon_target", "implementation_capacity"], ["baseline_reproducible", "cost_totals", "uncertainty_reported"], ["portfolio", "priority_areas", "phasing"], ["python", "sql", "geospatial_tools"], "medium"),
    spec("DA006", "data_analysis", "exploratory_business_analysis", "气候科研资助组合的证据与风险平衡", "Evidence-risk balance in a climate-research grant portfolio", "plhkw_authored", "new_gap_business_analysis_1", "newly_authored", "基金会需要从项目申请、历史成果、预算和主题图谱中构建下一年度资助组合。", "A foundation must build next year's grant portfolio from applications, prior outputs, budgets, and a topic map.", ["清理申请人与机构实体并检查利益冲突", "建立证据、可行性、组合互补和风险指标", "在多种价值取向下求解并做敏感性分析", "输出资助、候补与拒绝的可解释建议"], ["Resolve applicants and institutions and audit conflicts", "Build evidence, feasibility, complementarity, and risk metrics", "Solve under multiple value profiles and run sensitivity", "Recommend fund, reserve, and reject decisions with explanations"], "可复现模型、组合表、敏感性图和治理备忘录。", "A reproducible model, portfolio table, sensitivity plots, and governance memo.", ["entity_resolution", "multi_criteria_analysis", "portfolio_optimization", "fairness_audit"], ["risk_appetite", "theme_priority", "diversity_goal", "administrative_capacity"], ["budget_constraint", "conflict_flags", "score_reproduction"], ["portfolio", "weights", "explanation_depth"], ["python", "spreadsheet"], "high"),
    spec("DA007", "data_analysis", "spreadsheet_workflow", "构建三表联动的财务预测模型", "Build an integrated three-statement forecast", "spreadsheetbench2", "financial_model_binding_pending", "existing_benchmark_derived", "给定历史财报、假设表和部分模板，完成利润表、资产负债表与现金流量表联动预测。", "Given historical statements, an assumptions sheet, and a partial template, complete an integrated income statement, balance sheet, and cash-flow forecast.", ["检查工作簿结构与历史公式", "建立驱动假设和跨表依赖", "完成预测、平衡检查和情景切换", "生成面向决策者的关键图表"], ["Inspect workbook structure and historical formulas", "Build drivers and cross-sheet dependencies", "Complete forecast, balance checks, and scenarios", "Create decision-oriented charts"], "完成的 xlsx、检查表、假设说明和摘要页。", "A completed xlsx, checks sheet, assumptions note, and summary page.", ["spreadsheet_inspection", "financial_modeling", "dependency_reasoning", "scenario_analysis"], ["decision_horizon", "conservatism", "audience", "scenario_priority"], ["statements_balance", "formula_integrity", "no_hardcoded_outputs"], ["assumptions", "scenario_emphasis", "dashboard"], ["spreadsheet"], "high"),
    spec("DA008", "data_analysis", "spreadsheet_workflow", "调试多工作表预算模型", "Debug a multi-sheet budget model", "spreadsheetbench2", "debugging_binding_pending", "existing_benchmark_derived", "给定含引用、单位、符号和时间错位错误的预算工作簿，定位并修复系统性问题。", "Given a budget workbook with reference, unit, sign, and timing errors, locate and repair systemic issues.", ["先建立工作簿依赖和不变量", "批量识别错误模式而非逐格猜测", "修复并保留格式、注释和输入区", "用交叉核对与变化测试验证"], ["Map dependencies and invariants", "Identify error patterns rather than guessing cells", "Repair while preserving format, comments, and inputs", "Validate with cross-checks and perturbation tests"], "修复后的 xlsx、错误日志、验证页和变更摘要。", "A repaired xlsx, error log, validation sheet, and change summary.", ["spreadsheet_debugging", "dependency_graph", "pattern_detection", "verification"], ["audit_depth", "deadline", "tolerance_for_formula_changes", "audience"], ["golden_cells", "recalculation", "format_preservation"], ["repair_scope", "annotation_depth", "control_checks"], ["spreadsheet"], "medium"),
    spec("DA009", "data_analysis", "spreadsheet_workflow", "为经营工作簿生成角色化 KPI 仪表板", "Create a role-conditioned KPI dashboard", "spreadsheetbench2", "visualization_binding_pending", "existing_benchmark_derived", "给定复杂经营工作簿，建立一个数值正确、可追溯且适合特定管理角色的 KPI 仪表板。", "Given a complex operating workbook, build a numerically correct, traceable KPI dashboard for a management role.", ["调查数据表、刷新方式和关键口径", "选择指标层级、图形和交互", "建立来源链接与异常提示", "验证数值、筛选器和不同显示条件"], ["Inspect data sheets, refresh paths, and definitions", "Choose metric hierarchy, charts, and interaction", "Add source links and anomaly cues", "Validate values, filters, and display conditions"], "带仪表板的 xlsx、指标字典和验收截图。", "An xlsx dashboard, metric dictionary, and acceptance screenshots.", ["spreadsheet_inspection", "metric_selection", "visualization", "traceability"], ["role_goal", "numeracy", "meeting_context", "decision_frequency"], ["chart_values", "source_links", "filter_correctness"], ["metric_set", "chart_design", "annotation_level"], ["spreadsheet", "image_render"], "medium"),
    spec("DA010", "data_analysis", "spreadsheet_workflow", "完成滚动现金流与融资情景模板", "Complete a rolling cash-flow and financing template", "spreadsheetbench2", "template_binding_pending", "existing_benchmark_derived", "给定银行流水、应收应付计划和融资条款，完成 13 周滚动现金流模板与融资情景。", "Given bank transactions, AR/AP schedules, and financing terms, complete a 13-week rolling cash-flow model and financing scenarios.", ["对齐现金账户和日期", "构建收支预测、缺口和 covenant 检查", "加入基准/压力情景和滚动更新", "保护输入、公式与审计轨迹"], ["Align cash accounts and dates", "Build inflow/outflow, shortfall, and covenant checks", "Add base/stress scenarios and rolling updates", "Protect inputs, formulas, and audit trail"], "完成的 xlsx、情景页、控制检查和使用说明。", "A completed xlsx, scenario sheet, controls, and instructions.", ["spreadsheet_generation", "cashflow_modeling", "scenario_analysis", "control_design"], ["liquidity_buffer", "financing_access", "risk_tolerance", "operator_skill"], ["cash_reconciliation", "formula_integrity", "covenant_logic"], ["buffer", "scenario_set", "alert_thresholds"], ["spreadsheet"], "high"),
    spec("DA011", "data_analysis", "predictive_modeling", "资源约束下的客户流失预测", "Customer-churn modeling under deployment constraints", "mle_bench", "tabular_competition_binding_pending", "existing_benchmark_derived", "给定客户行为与流失标签，开发可提交的预测管线，并在性能、解释性和部署资源之间作选择。", "Given customer behavior and churn labels, develop a submission-ready prediction pipeline while trading off performance, explainability, and deployment resources.", ["审计泄漏、时间切分和不平衡", "建立可复现基线与验证", "比较特征、模型和校准", "生成提交、模型卡和部署评估"], ["Audit leakage, temporal split, and imbalance", "Build reproducible baseline and validation", "Compare features, models, and calibration", "Produce submission, model card, and deployment assessment"], "训练代码、预测文件、实验表、模型卡和建议。", "Training code, predictions, experiment table, model card, and recommendation.", ["data_audit", "modeling", "experiment_tracking", "deployment_tradeoff"], ["latency", "explainability", "compute", "false_negative_cost"], ["valid_submission", "heldout_metric", "no_leakage"], ["model_family", "threshold", "feature_complexity"], ["python", "experiment_runner"], "high"),
    spec("DA012", "data_analysis", "predictive_modeling", "可解释信用风险模型与阈值策略", "Explainable credit-risk model and threshold policy", "mle_bench", "tabular_competition_binding_pending", "existing_benchmark_derived", "给定信用申请数据，建立风险预测模型，并把排序性能转成可审计的批准阈值策略。", "Given credit-application data, build a risk model and translate ranking performance into an auditable approval-threshold policy.", ["检查缺失、代理变量、时间漂移和不平衡", "建立基线、交叉验证与校准", "比较高性能和可解释模型", "做成本、公平和阈值敏感性分析"], ["Audit missingness, proxies, drift, and imbalance", "Build baseline, cross-validation, and calibration", "Compare high-performance and interpretable models", "Analyze cost, fairness, and threshold sensitivity"], "代码、预测、模型卡、阈值表和风险说明。", "Code, predictions, model card, threshold table, and risk note.", ["modeling", "calibration", "fairness_audit", "decision_thresholding"], ["regulatory_need", "error_cost", "explainability", "portfolio_goal"], ["heldout_metric", "calibration", "leakage_check"], ["model_choice", "threshold", "explanation_method"], ["python", "experiment_runner"], "high"),
    spec("DA013", "data_analysis", "predictive_modeling", "多层级需求预测与补货决策", "Hierarchical demand forecasting and replenishment", "real_workflow_adaptation", "forecast_dataset_binding_pending", "adapted_real_world", "给定 SKU—门店销量、价格、促销和库存数据，建立多层级预测并转化为补货建议。", "Given SKU-store sales, price, promotion, and inventory data, build hierarchical forecasts and convert them to replenishment decisions.", ["处理缺货导致的删失与新品冷启动", "建立时间切分和层级基线", "比较统计、树模型和深度模型", "评估预测误差与库存成本"], ["Handle stockout censoring and cold starts", "Build temporal splits and hierarchical baselines", "Compare statistical, tree, and deep models", "Evaluate forecast error and inventory cost"], "训练代码、预测、层级评估、补货模拟和建议。", "Training code, forecasts, hierarchical evaluation, replenishment simulation, and advice.", ["time_series", "hierarchical_modeling", "simulation", "decision_support"], ["stockout_cost", "holding_cost", "compute", "planner_expertise"], ["temporal_validation", "aggregation_consistency", "reproducibility"], ["model", "service_level", "replenishment_policy"], ["python", "experiment_runner"], "medium"),
    spec("DA014", "data_analysis", "predictive_modeling", "工业缺陷图像模型的精度—延迟选择", "Accuracy-latency selection for defect inspection", "real_workflow_adaptation", "image_dataset_binding_pending", "adapted_real_world", "给定工业缺陷图像和标注，训练检测/分类管线，并判断云端高精度与边缘低延迟路线。", "Given industrial defect images and labels, train a detection/classification pipeline and choose between cloud accuracy and edge latency.", ["审计标注、批次泄漏和类别不平衡", "建立分组验证和轻量基线", "比较模型、增广、校准和压缩", "测量设备延迟并做错误成本分析"], ["Audit labels, batch leakage, and imbalance", "Build grouped validation and lightweight baseline", "Compare models, augmentation, calibration, and compression", "Measure device latency and error costs"], "代码、模型、预测、设备基准、模型卡和部署建议。", "Code, model, predictions, device benchmark, model card, and deployment advice.", ["computer_vision", "leakage_audit", "model_compression", "deployment_tradeoff"], ["device", "miss_cost", "latency", "maintenance_skill"], ["grouped_holdout", "submission_metric", "device_measurement"], ["model", "threshold", "deployment_target"], ["python", "gpu_or_cpu", "experiment_runner"], "high"),
    spec("DA015", "data_analysis", "experiment_design", "产品功能分阶段上线实验设计", "Staged rollout experiment for a product feature", "plhkw_authored", "new_gap_experiment_1", "newly_authored", "给定历史行为数据和有限流量，设计新功能的分阶段上线实验，兼顾学习速度、风险和长期指标。", "Given historical behavior and limited traffic, design a staged rollout experiment balancing learning speed, risk, and long-term outcomes.", ["定义估计对象、主指标、护栏和异质效应", "评估随机化单元、干扰和样本量", "比较固定样本、序贯和分阶段方案", "生成分析代码、停止规则和监测计划"], ["Define estimand, primary metric, guardrails, and heterogeneity", "Assess randomization unit, interference, and power", "Compare fixed, sequential, and staged designs", "Produce analysis code, stopping rules, and monitoring"], "预分析计划、功效模拟、代码、仪表板规格和决策规则。", "A pre-analysis plan, power simulation, code, dashboard spec, and decision rules.", ["causal_design", "power_analysis", "sequential_decision", "risk_management"], ["risk_tolerance", "traffic", "decision_speed", "stakeholder_goal"], ["estimand_defined", "type_I_error", "simulation_reproducible"], ["design", "stopping_rule", "segment_analysis"], ["python", "simulation"], "high"),
    spec("DA016", "data_analysis", "experiment_design", "教育干预的准实验评估方案", "Quasi-experimental evaluation of an education intervention", "plhkw_authored", "new_gap_experiment_2", "newly_authored", "学校已经非随机推广一项学习支持计划，需要使用历史成绩、参与和背景数据评估效果，同时明确不可识别部分。", "A school non-randomly rolled out a learning-support program and needs evaluation from historical performance, participation, and background data with explicit identification limits.", ["画因果图并定义目标效应", "检查选择偏差、缺失和政策时间", "比较匹配、差分和断点等可行设计", "做安慰剂、敏感性和异质效应分析"], ["Draw a causal graph and define the effect", "Audit selection, missingness, and policy timing", "Compare matching, difference, and discontinuity designs", "Run placebo, sensitivity, and heterogeneity analyses"], "分析计划、代码、识别假设表、结果模板和决策边界。", "An analysis plan, code, identification table, result template, and decision boundaries.", ["causal_inference", "confound_audit", "sensitivity_analysis", "decision_support"], ["policy_decision", "equity_priority", "acceptable_assumption", "audience"], ["data_preprocessing", "assumptions_visible", "placebo_tests"], ["design_choice", "effect_metric", "communication_depth"], ["python", "statistical_modeling"], "high"),
    spec("DA017", "data_analysis", "cleaning_integration", "跨 CRM、账单与客服系统的客户实体对齐", "Customer entity resolution across CRM, billing, and support", "datascibench", "TFC_entity_integration_structure", "existing_benchmark_derived", "给定三个主键不一致、文本脏乱且含历史变更的客户系统，构建可审计实体对齐与下游汇总。", "Given three customer systems with inconsistent keys, dirty text, and historical changes, build auditable entity resolution and downstream aggregates.", ["画像字段、缺失、时间和冲突", "设计确定性与概率匹配函数", "建立人工复核区和错误分析", "输出统一实体表与可程序验证的汇总"], ["Profile fields, missingness, time, and conflicts", "Design deterministic and probabilistic matching functions", "Create review zones and error analysis", "Output a unified entity table and programmatically checked aggregates"], "清洗代码、统一表、匹配审计、函数级测试和分析摘要。", "Cleaning code, unified table, match audit, function tests, and analysis summary.", ["data_cleaning", "entity_resolution", "function_level_verification", "uncertainty_handling"], ["false_merge_cost", "review_budget", "downstream_use", "privacy_policy"], ["schema_valid", "aggregate_reconciliation", "test_functions"], ["match_threshold", "review_queue", "retained_fields"], ["python", "sql"], "high"),
    spec("DA018", "data_analysis", "cleaning_integration", "多源环境监测数据的时空整合", "Spatiotemporal integration of environmental monitoring data", "real_workflow_adaptation", "environmental_data_binding_pending", "adapted_real_world", "给定传感器、实验室采样、天气和站点维护记录，建立一致的时空分析数据集并评估污染事件。", "Given sensor, laboratory sample, weather, and maintenance records, build a coherent spatiotemporal dataset and assess pollution episodes.", ["对齐站点、单位、时区和采样窗口", "识别校准漂移、停机和检测限", "设计插补与不确定性传播", "生成事件分析和可追溯数据产品"], ["Align sites, units, time zones, and sampling windows", "Detect calibration drift, downtime, and detection limits", "Design imputation and uncertainty propagation", "Produce event analyses and a traceable data product"], "清洗管线、版本化数据集、质量报告、地图/图表和结论。", "A cleaning pipeline, versioned dataset, quality report, maps/charts, and findings.", ["data_integration", "spatiotemporal_reasoning", "quality_control", "uncertainty_propagation"], ["regulatory_use", "spatial_scale", "missingness_tolerance", "audience"], ["units_consistent", "provenance", "quality_flags"], ["imputation", "event_threshold", "visualization"], ["python", "sql", "geospatial_tools"], "high"),
]


PDR_SELECTION = {
    1: ("DR001", "recommendation_decision", "博士项目与申请路线选择", "PhD program and application-path decision", ["multi_criteria_comparison", "resource_discovery", "action_planning"], ["research_direction", "geography", "funding_need", "career_goal"], "medium"),
    7: ("DR002", "recommendation_decision", "AI 教育创业路线与商业模式", "AI education startup strategy", ["market_research", "architecture_comparison", "business_model_analysis"], ["founder_skill", "capital", "risk_tolerance", "target_segment"], "medium"),
    10: ("DR003", "recommendation_decision", "国际职业市场与迁移路线", "International career and relocation route", ["market_comparison", "policy_research", "roadmap_planning"], ["role", "language", "visa_eligibility", "family_constraints"], "medium"),
    26: ("DR004", "recommendation_decision", "长篇小说创作与发布计划", "Long-form novel creation and release plan", ["creative_planning", "audience_research", "long_horizon_scheduling"], ["genre_goal", "writing_experience", "time_budget", "publication_path"], "low"),
    38: ("DR005", "recommendation_decision", "北京自住房置业研究", "Beijing owner-occupied housing research", ["geospatial_comparison", "market_research", "constraint_optimization"], ["commute", "schooling", "budget", "risk_tolerance"], "high"),
    46: ("DR006", "recommendation_decision", "家庭教育干预组合设计", "Family education intervention portfolio", ["evidence_synthesis", "program_design", "progress_monitoring"], ["child_age", "learning_need", "family_time", "parenting_values"], "high"),
    13: ("DR007", "literature_synthesis", "2 型糖尿病综合管理证据综述", "Evidence synthesis for type-2 diabetes management", ["clinical_evidence_synthesis", "guideline_comparison", "risk_management"], ["treatment_state", "comorbidity", "schedule", "health_literacy"], "high"),
    21: ("DR011", "open_consulting", "个人投资目标与策略可行性咨询", "Open consulting on personal investment goals", ["open_consulting", "forecast_uncertainty", "risk_analysis"], ["loss_tolerance", "liquidity", "knowledge", "time_horizon"], "high"),
    42: ("DR012", "open_consulting", "全球 AI Agent 产品合规架构", "Global compliance architecture for an AI-agent product", ["multi_jurisdiction_research", "dependency_reasoning", "architecture_decision"], ["markets", "data_flow", "launch_timing", "risk_posture"], "high"),
    31: ("DR019", "conflicting_evidence", "护肤产品证据冲突与适配", "Conflicting evidence in skincare selection", ["product_research", "evidence_conflict", "safety_filtering"], ["skin_response", "ingredient_tolerance", "budget", "routine_complexity"], "medium"),
    49: ("DR020", "conflicting_evidence", "亲子沟通干预的证据与情境冲突", "Conflicting evidence for parent-child communication interventions", ["behavioral_evidence_synthesis", "contextualization", "program_design"], ["child_age", "conflict_pattern", "family_schedule", "privacy_boundary"], "high"),
    18: ("DR021", "temporal_update", "柏林商务旅行的动态更新规划", "Dynamic planning for a Berlin business trip", ["temporal_search", "itinerary_optimization", "update_handling"], ["meeting_schedule", "mobility", "budget", "risk_tolerance"], "medium"),
}


EXTRA_DR_TITLES = [
    "跨论文争议的气候敏感度证据审计", "罕见病临床试验资源发现", "机器人触觉数据集谱系", "开放权重模型许可证比较",
    "AI 芯片供应链实体枚举", "教育技术随机试验文献综合", "低资源语言评测 prior art", "公共卫生指南版本冲突",
    "开源数据库商业化路线咨询", "生物制造团队与设施地图",
]

EXTRA_CODE_TITLES = [
    "为 CLI 增加离线模式", "为 ORM 增加软删除", "为任务运行器增加断点恢复", "为 API 客户端增加分页流",
    "为配置系统增加分层覆盖", "为日志库增加结构化字段", "修复并发取消泄漏", "修复循环依赖初始化",
    "修复 Windows 路径回归", "修复解析器 Unicode 边界", "修复数据库连接池饥饿", "修复缓存键碰撞",
    "重构插件加载", "重构数据校验管线", "重构异步批处理", "重构权限检查",
    "优化图遍历热点", "优化序列化内存", "选择认证依赖", "选择配置中心",
    "选择文件存储后端", "选择 RPC 方案", "调查弃用 API", "调查跨模块状态污染",
    "调查构建不可复现", "调查测试覆盖缺口", "迁移 Python 版本", "迁移数据库 schema",
    "增加多租户隔离", "增加隐私删除流程", "增加兼容性模式", "增加插件沙盒",
    "构建发布自动化", "构建回滚验证", "设计速率限制", "设计特征开关",
]

EXTRA_DATA_TITLES = [
    "广告归因分解", "供应链缺货诊断", "招聘漏斗公平性", "客户支持主题漂移", "运输网络准点率", " SaaS 定价敏感性",
    "学校出勤与成绩分析", "制造良率根因", "内容推荐留存分析", "保险理赔流程分析", "现金转换周期诊断", "门店选址分析",
    "合并损坏财务模板", "修复跨表引用", "生成项目预算模板", "生成销售仪表板", "调试税务工作簿", "调试排班工作簿",
    "贷款违约建模", "文本主题分类", "音频事件分类", "设备故障预测", "房价区间预测", "库存需求预测",
    "营销增量实验", "定价 A/B 设计", "政策断点分析", "差分隐私统计发布", "供应商实体对齐", "产品目录清洗",
    "科研元数据整合", "日志事件 schema 对齐", "多币种账单统一", "地理编码质量审计", "传感器漂移校正", "缺失数据敏感性分析",
]


def load_pdr():
    rows = {}
    for lang in ("zh", "en"):
        path = PDR_DIR / "raw" / f"tasks_{lang}.jsonl.gz"
        with gzip.open(path, "rt", encoding="utf-8") as handle:
            for line in handle:
                item = json.loads(line)
                rows.setdefault(item["taskid"], {"domain": item["domain"]})[lang] = item["task"]
    catalog = {x["task_id"]: x for x in json.loads((PDR_DIR / "derived" / "task_catalog.json").read_text())}
    for task_id, item in rows.items():
        item["candidate_user_ids"] = catalog[task_id]["candidate_user_ids"]
    return rows


def compiled_prompt(item, lang):
    scenario = item[f"scenario_{lang}"]
    steps = item[f"steps_{lang}"]
    deliverable = item[f"deliverable_{lang}"]
    if lang == "zh":
        numbered = "\n".join(f"{i}. {step}；" for i, step in enumerate(steps, 1))
        return f"{scenario}\n\n请完成以下长程工作：\n{numbered}\n\n最终交付：{deliverable}"
    numbered = "\n".join(f"{i}. {step};" for i, step in enumerate(steps, 1))
    return f"{scenario}\n\nComplete the following long-horizon work:\n{numbered}\n\nFinal deliverable: {deliverable}"


def finalize(item, index):
    source = SOURCES[item["source_id"]]
    paper_first = item["task_id"] in PAPER_FIRST_IDS
    return {
        "task_id": item["task_id"],
        "vertical": item["vertical"],
        "subtype": item["subtype"],
        "title_zh": item["title_zh"],
        "title_en": item["title_en"],
        "canonical_language": "zh",
        "task_prompt_zh": item["task_prompt_zh"] if "task_prompt_zh" in item else compiled_prompt(item, "zh"),
        "task_prompt_en": item["task_prompt_en"] if "task_prompt_en" in item else compiled_prompt(item, "en"),
        "construction_stage": "normalized_seed",
        "selection_status": STATUS,
        "paper_first": {
            "included": paper_first,
            "priority_rank": PAPER_FIRST_IDS.index(item["task_id"]) + 1 if paper_first else None,
            "status": "priority_for_environment_binding_not_runnable" if paper_first else "release_pool_after_paper_first",
            "selection_basis": "vertical_and_reasoning_coverage_signal_balance_and_source_continuity" if paper_first else "provisional_release_pool",
        },
        "source": {
            "source_id": item["source_id"],
            "source_locator": item["source_locator"],
            "source_class": item["source_class"],
            "license": source["license"],
            "use_policy": source["use_policy"],
            "url": source["url"],
            "snapshot": source["snapshot"],
        },
        "long_horizon_eligibility": {
            "multi_step_autonomy": True,
            "multiple_reasonable_paths": True,
            "complex_artifact": True,
            "task_relevant_user_difference_can_change_artifact": True,
            "invariant_objective_quality_is_checkable": True,
            "not_one_prompt_trivial": True,
            "authoring_gate_status": "pass_pending_empirical_pilot",
        },
        "reasoning_structures": item["reasoning_structures"],
        "personalization_design": {
            "primary_signal_mode": SIGNAL_CYCLE[index % len(SIGNAL_CYCLE)],
            "eligible_counterfactual_axes": item["counterfactual_axes"],
            "explicit_constraint_only": False,
            "persona_and_contract_status": "not_yet_authored",
            "required_next_gate": "two_humans_confirm_that_at_least_one_decision_node_should_change",
        },
        "invariant_core": {
            "same_task_shell": True,
            "same_evidence_or_repo_or_dataset": True,
            "same_tools_and_budget": True,
            "objective_checks": item["invariant_checks"],
        },
        "user_conditioned_verifier_plan": item.get("conditional_checks", item.get("user_conditioned_checks")),
        "required_tools": item["required_tools"],
        "risk_level": item["risk"],
        "expert_review_required": item["risk"] == "high",
        "environment_binding_status": "pending",
        "evidence_snapshot_status": "pending",
        "screening": {
            "relevance": 2,
            "counterfactual_separability": 2,
            "invariant_core": 2,
            "objective_verifier": 2,
            "long_horizon": 2,
            "total": 10,
            "status": "provisional_author_pass",
        },
    }


def build_selected():
    pdr = load_pdr()
    items = []
    for task_num, meta in PDR_SELECTION.items():
        task_id, subtype, title_zh, title_en, reasoning, axes, risk = meta
        row = pdr[task_num]
        items.append({
            "task_id": task_id,
            "vertical": "deep_research",
            "subtype": subtype,
            "title_zh": title_zh,
            "title_en": title_en,
            "task_prompt_zh": row["zh"],
            "task_prompt_en": row["en"],
            "source_id": "pdr_bench",
            "source_locator": f"task_{task_num}",
            "source_class": "existing_benchmark_derived",
            "reasoning_structures": reasoning,
            "counterfactual_axes": axes,
            "invariant_checks": ["factuality", "citation_validity", "shared_task_requirements"],
            "user_conditioned_checks": ["recommendation_or_plan", "priority", "actionability"],
            "required_tools": ["web_search", "page_fetch"],
            "risk": risk,
            "upstream_candidate_user_ids": row["candidate_user_ids"],
        })
    items.extend(NON_PDR)
    items.sort(key=lambda x: x["task_id"])
    selected = [finalize(item, i) for i, item in enumerate(items)]
    for record, item in zip(selected, items):
        if "upstream_candidate_user_ids" in item:
            record["upstream_candidate_user_ids"] = item["upstream_candidate_user_ids"]
    return selected


def reserve_record(candidate_id, vertical, title, source_id, reason, locator):
    scores = {
        "relevance": 2,
        "counterfactual_separability": 1 if "counterfactual" in reason or "redundancy" in reason else 2,
        "invariant_core": 2,
        "objective_verifier": 1 if "verifier" in reason or "environment" in reason else 2,
        "long_horizon": 2,
    }
    scores["total"] = sum(scores.values())
    return {
        "candidate_id": candidate_id,
        "vertical": vertical,
        "normalized_seed_title": title,
        "source_id": source_id,
        "source_locator": locator,
        "selection_status": "reserve_not_rejected",
        "screening": scores,
        "primary_hold_reason": reason,
        "human_validated": False,
    }


def build_candidates(selected):
    candidates = []
    for task in selected:
        candidates.append({
            "candidate_id": f"CAND_{task['task_id']}",
            "vertical": task["vertical"],
            "normalized_seed_title": task["title_zh"],
            "source_id": task["source"]["source_id"],
            "source_locator": task["source"]["source_locator"],
            "selection_status": "provisional_selected",
            "selected_task_id": task["task_id"],
            "screening": task["screening"],
            "primary_hold_reason": None,
            "human_validated": False,
        })

    pdr = load_pdr()
    selected_pdr = set(PDR_SELECTION)
    for task_num in sorted(set(pdr) - selected_pdr):
        if task_num in {2, 3, 4, 5, 6, 8, 9}:
            reason = "redundancy_with_selected_planning_or_career_shell"
        elif 11 <= task_num <= 15 or 22 <= task_num <= 25 or 41 <= task_num <= 45:
            reason = "expert_and_live_evidence_burden_before_core_selection"
        elif task_num in {27, 28, 29, 30, 32, 33, 34, 35, 36, 37, 39, 40, 47, 48, 50}:
            reason = "counterfactual_or_subtype_redundancy_requires_human_screen"
        else:
            reason = "quota_hold_for_later_screening"
        candidates.append(reserve_record(f"CAND_PDR_{task_num:02d}", "deep_research", pdr[task_num]["zh"][:80], "pdr_bench", reason, f"task_{task_num}"))

    for i, title in enumerate(EXTRA_DR_TITLES, 1):
        candidates.append(reserve_record(f"CAND_DR_RES_{i:02d}", "deep_research", title, ["researcherbench", "deepresearch_bench", "livedrbench"][i % 3], "quota_hold_and_source_license_or_evidence_binding", f"reserve_concept_{i}"))
    for i, title in enumerate(EXTRA_CODE_TITLES, 1):
        candidates.append(reserve_record(f"CAND_SW_RES_{i:02d}", "software_engineering", title, "swe_bench_verified" if i <= 24 else "real_workflow_adaptation", "environment_binding_or_counterfactual_screen_pending", f"reserve_repo_shell_{i}"))
    for i, title in enumerate(EXTRA_DATA_TITLES, 1):
        source_id = ["dsbench", "spreadsheetbench2", "mle_bench", "datascibench"][i % 4]
        candidates.append(reserve_record(f"CAND_DA_RES_{i:02d}", "data_analysis", title, source_id, "dataset_license_or_objective_verifier_binding_pending", f"reserve_data_shell_{i}"))
    candidates.sort(key=lambda x: x["candidate_id"])
    return candidates


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k) for k in fields})


def build_html(selected, summary):
    cards = []
    for task in selected:
        axes = " · ".join(task["personalization_design"]["eligible_counterfactual_axes"])
        reasoning = " · ".join(task["reasoning_structures"])
        priority = task["paper_first"]["included"]
        cards.append(f'''<article class="card{' priority' if priority else ''}" data-v="{task['vertical']}" data-s="{task['subtype']}" data-first="{'true' if priority else 'false'}">
<div class="meta"><span>{html.escape(task['task_id'])}</span><span>{html.escape(task['vertical'])}</span><span>{html.escape(task['subtype'])}</span>{'<span>paper-first</span>' if priority else ''}</div>
<h2>{html.escape(task['title_zh'])}</h2><p>{html.escape(task['task_prompt_zh'])}</p>
<dl><dt>Reasoning</dt><dd>{html.escape(reasoning)}</dd><dt>Counterfactual axes</dt><dd>{html.escape(axes)}</dd><dt>Source</dt><dd>{html.escape(task['source']['source_id'])} · {html.escape(task['source']['source_locator'])}</dd></dl>
</article>''')
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PLHKW task set v0.54</title><style>
body{{font-family:system-ui,-apple-system,sans-serif;margin:0;background:#f4f1ea;color:#17201d}}header{{padding:40px max(24px,6vw);background:#163c35;color:white}}main{{max-width:1200px;margin:auto;padding:28px}}.stats{{display:flex;gap:16px;flex-wrap:wrap}}.stat{{background:#fff2;border:1px solid #fff4;padding:12px 18px;border-radius:12px}}nav{{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 20px}}button{{padding:9px 14px;border:1px solid #789;border-radius:999px;background:white;cursor:pointer}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:16px}}.card{{background:white;border:1px solid #d8d5ca;border-radius:14px;padding:18px;box-shadow:0 2px 8px #0000000d}}.card.priority{{border:2px solid #b87922}}.meta{{display:flex;gap:8px;flex-wrap:wrap;font-size:12px;color:#466}}.meta span{{background:#e8f1ee;padding:4px 7px;border-radius:6px}}h2{{font-size:19px}}p{{white-space:pre-line;line-height:1.55}}dt{{font-weight:700;margin-top:10px}}dd{{margin:3px 0;color:#465}}.hidden{{display:none}}</style></head><body>
<header><h1>Personalized Long-Horizon Knowledge Work · v0.54</h1><p>60 个 provisional task families；task shell 已冻结，persona、evidence/environment 与人评尚待下一阶段。</p><div class="stats"><div class="stat">Deep Research<br><b>{summary['selected_by_vertical']['deep_research']}</b></div><div class="stat">Software<br><b>{summary['selected_by_vertical']['software_engineering']}</b></div><div class="stat">Data<br><b>{summary['selected_by_vertical']['data_analysis']}</b></div><div class="stat">Candidate pool<br><b>{summary['candidate_total']}</b></div></div></header>
<main><nav><button data-filter="all">全部</button><button data-filter="paper_first">Paper-first 12</button><button data-filter="deep_research">Deep Research</button><button data-filter="software_engineering">Software</button><button data-filter="data_analysis">Data</button></nav><section class="grid">{''.join(cards)}</section></main>
<script>document.querySelectorAll('button').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.card').forEach(c=>{{const f=b.dataset.filter;c.classList.toggle('hidden',f!=='all'&&(f==='paper_first'?c.dataset.first!=='true':c.dataset.v!==f))}})}})</script></body></html>'''


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    selected = build_selected()
    candidates = build_candidates(selected)
    selected_by_vertical = Counter(x["vertical"] for x in selected)
    selected_by_subtype = Counter(f"{x['vertical']}::{x['subtype']}" for x in selected)
    selected_by_source_class = Counter(x["source"]["source_class"] for x in selected)
    signal_modes = Counter(x["personalization_design"]["primary_signal_mode"] for x in selected)
    paper_first = sorted((x for x in selected if x["paper_first"]["included"]), key=lambda x: x["paper_first"]["priority_rank"])
    summary = {
        "version": "0.54",
        "created_at": "2026-08-16",
        "candidate_total": len(candidates),
        "candidate_by_vertical": dict(Counter(x["vertical"] for x in candidates)),
        "selected_total": len(selected),
        "selected_by_vertical": dict(selected_by_vertical),
        "selected_by_subtype": dict(selected_by_subtype),
        "selected_by_source_class": dict(selected_by_source_class),
        "primary_signal_modes": dict(signal_modes),
        "paper_first_total": len(paper_first),
        "paper_first_by_vertical": dict(Counter(x["vertical"] for x in paper_first)),
        "paper_first_task_ids": [x["task_id"] for x in paper_first],
        "paper_first_status": "priority_for_environment_binding_not_runnable",
        "status": STATUS,
        "gold_claim_allowed": False,
        "next_required_gates": ["source_asset_license_audit", "evidence_repo_dataset_binding", "two_human_counterfactual_screen", "contract_freeze", "pilot_discrimination"],
    }
    write_jsonl(HERE / "selected_tasks.jsonl", selected)
    write_jsonl(HERE / "paper_first_12.jsonl", paper_first)
    write_jsonl(HERE / "candidate_pool.jsonl", candidates)
    write_csv(HERE / "selected_tasks.csv", [{
        "task_id": x["task_id"], "vertical": x["vertical"], "subtype": x["subtype"],
        "title_zh": x["title_zh"], "source_id": x["source"]["source_id"],
        "source_class": x["source"]["source_class"], "risk_level": x["risk_level"],
        "primary_signal_mode": x["personalization_design"]["primary_signal_mode"],
        "paper_first": x["paper_first"]["included"],
        "paper_first_rank": x["paper_first"]["priority_rank"],
        "environment_binding_status": x["environment_binding_status"],
    } for x in selected], ["task_id", "vertical", "subtype", "title_zh", "source_id", "source_class", "risk_level", "primary_signal_mode", "paper_first", "paper_first_rank", "environment_binding_status"])
    write_csv(HERE / "paper_first_12.csv", [{
        "rank": x["paper_first"]["priority_rank"], "task_id": x["task_id"], "vertical": x["vertical"],
        "subtype": x["subtype"], "title_zh": x["title_zh"], "source_id": x["source"]["source_id"],
        "primary_signal_mode": x["personalization_design"]["primary_signal_mode"],
        "risk_level": x["risk_level"], "environment_binding_status": x["environment_binding_status"],
    } for x in paper_first], ["rank", "task_id", "vertical", "subtype", "title_zh", "source_id", "primary_signal_mode", "risk_level", "environment_binding_status"])
    write_csv(HERE / "screening_audit.csv", [{
        "candidate_id": x["candidate_id"], "vertical": x["vertical"], "title": x["normalized_seed_title"],
        "source_id": x["source_id"], "selection_status": x["selection_status"],
        "relevance": x["screening"]["relevance"], "counterfactual_separability": x["screening"]["counterfactual_separability"],
        "invariant_core": x["screening"]["invariant_core"], "objective_verifier": x["screening"]["objective_verifier"],
        "long_horizon": x["screening"]["long_horizon"], "total": x["screening"]["total"],
        "primary_hold_reason": x["primary_hold_reason"], "human_validated": x["human_validated"],
    } for x in candidates], ["candidate_id", "vertical", "title", "source_id", "selection_status", "relevance", "counterfactual_separability", "invariant_core", "objective_verifier", "long_horizon", "total", "primary_hold_reason", "human_validated"])
    (HERE / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (HERE / "source_registry.json").write_text(json.dumps(SOURCES, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (HERE / "catalog.html").write_text(build_html(selected, summary), encoding="utf-8")
    generated = [
        "README.md", "task_seed.schema.json", "build_task_pool.py", "validate_task_pool.py",
        "candidate_pool.jsonl", "selected_tasks.jsonl", "selected_tasks.csv", "paper_first_12.jsonl", "paper_first_12.csv",
        "screening_audit.csv", "summary.json", "source_registry.json", "catalog.html",
    ]
    manifest = {"version": "0.54", "generated_by": "build_task_pool.py", "files": {name: sha256(HERE / name) for name in generated}}
    (HERE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
