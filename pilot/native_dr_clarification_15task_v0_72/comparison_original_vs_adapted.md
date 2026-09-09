# PDR 15-task original vs adapted instruction comparison

> v0.73 · 2026-09-09 · review artifact. Official PDR source records are unchanged.

## Decision

For the primary native-clarification experiment, use the **exact original PDR instructions first**. All 15 were selected because the original task already has high personalization leverage and leaves decision-changing user-owned variables unresolved. The v0.72 adapted prompts should be treated only as a separate partial-intent stress-test arm, not as replacements for the PDR bridge.

This avoids two confounds: removing strong visible evidence can artificially inflate clarification pressure, and adding new anchors can change the task rather than merely change context coverage. Original PDR criteria can be used directly only with the official instruction/persona pair. On adapted instructions, they require a blind relevance audit and the score must be labeled `PDR-criteria score on adapted instruction`.

## Selection rule for the 15 tasks

The 50 official tasks were screened before observing new agent outputs. A task entered the provisional slice only when personalization leverage was rated 2/2; user differences should change evidence scope, recommendation set, constraints, or conclusion; the difference was not merely wording/style; history/persona could ground 2–4 candidate preference nodes; the task still required genuine Deep Research; and demographic projection and task–profile contradiction risks were not high. Tie-breaking favored clearer profile contrast, stronger evidence availability, lower stereotype/conflict risk, and lower construct redundancy. This is a provisional author screen pending two blind human reviewers, not benchmark gold.

## What PDR actually exposes

The official generation query concatenates `User Task` and the complete structured `User Persona`. The persona is broad and contains task-relevant facts, irrelevant facts, habits, background, constraints, and preferences; it is not a clean task-specific preference ledger. The official personalization evaluator separately receives the task, persona, generated article, and task–persona-specific criteria. Therefore:

- exact task + full persona is a useful **PDR full-context upper reference**;
- it is not a true information oracle because the persona can leave task-specific choices unresolved;
- `OracleTopK` should contain only pre-frozen high-influence, user-owned values actually supported by the persona or user confirmation;
- a variable that should be researched or recommended must not be injected as a “preference answer.”

## Compact semantic diff

| Task | Domain | Preserved | Removed / weakened | Added | Recommended primary use |
|---:|---|---|---|---|---|
| 1 | Education | AI PhD、海外、1–2 年、研究方向未定，以及资助/申请/职业结果 | 删去地区、课程、资源、语言、实习等长 checklist；不删除已知用户偏好值 | 增加 decision-ready shortlist、current/verifiable 证据要求 | 原题优先；它已经天然欠指定 |
| 4 | Education | 在职、MBA/EMBA/data analytics 候选、国内外比较、边工作边学习 | 压缩课程/师资/校友/品牌/申请/奖学金等逐项输出要求；未删除具体用户值 | 增加 phased decision/application 与 current evidence 表述 | 原题优先；改写仅是压缩 |
| 5 | Education | 6–12 个月完成投稿、完整出版流程 | 删除“SCI Q1–Q2 或同等级”和“写作/选刊/审稿回复经验有限”两条强证据 | 增加 current/verifiable journal 信息和风险降低表述 | 必须用原题；当前改写人为制造了额外缺口 |
| 6 | Career | 一年内转金融、学习/证书/项目/招聘路径 | 删除 investment/risk/corporate finance 候选方向，以及“缺系统金融背景和实践经验” | 增加 role-requirements/hiring evidence 与避免 generic curriculum | 必须用原题；改写改变了可见证据 |
| 9 | Career | 六个月转 AI PM、能力差距/项目/公司/人脉 | 压缩步骤表达；未删除具体已知用户值 | 增加 current role requirements 和 decision-ready/priority 语言 | 原题优先；天然缺 current background、AI domain、company type |
| 10 | Career | 1–2 年海外公司、市场/岗位/语言文化/简历面试/签证 | 压缩详细输出清单；未删除具体用户值 | 增加 current labor-market/immigration evidence | 原题优先；天然缺国家、岗位、语言和家庭流动约束 |
| 11 | Health | 六个月核心/耐力/减脂/线条/5 km 目标 | 删去久坐缓解、动机维持和有/无器械的逐项输出措辞；未删除健康事实 | 增加 safety boundaries、adjustment rules | 原题优先；天然缺基线、伤病、时间、设备、饮食约束 |
| 16 | Travel | 两周、三个月内、东南亚文化与自然 | 删除 backpacking，以及雨林/历史遗址/本地社区这组已见兴趣证据 | 增加 internally feasible、specific enough to book | 必须用原题；改写移除了旅行风格与兴趣线索 |
| 21 | Finance | 六个月、年化至少 10%、无产品偏好、资产配置与风险管理 | 把硬目标“at least 10%”弱化为“ideally” | 新增“conservative investor”与显式质疑目标/权衡的要求；该 conservative 并非原 task 证据 | 必须用原题；当前改写既新增 persona 值又改了目标强度 |
| 22 | Finance | 30 年退休、年金/医疗/照护、经济周期与通胀调整 | 压缩产品与阶段性细节；未删除具体用户值 | 增加 major assumptions/trade-offs explicit | 原题优先；天然缺年龄、资产、家属、健康与退休生活目标 |
| 30 | Creative | 六个月做个人媒体、品牌/受众/变现及完整执行系统 | 大幅压缩平台、故事、互动、KPI、资源、案例等 deliverable checklist；没有删除这些变量的具体值，因为原题也未提供 | 增加 12-week editorial roadmap 与 evidence-backed platform choices | 原题优先；它本来就要求“结合我的时间/预算/技能”却未给值，clarification pressure 已足够 |
| 33 | Shopping | 成套宠物清洁/喂食/饮水/监控/玩具与比较维度 | smart camera 改为 monitoring，品牌措辞压缩；未删除宠物具体事实，因为原题没有 | 增加 total cost、compatibility、failure-oriented 组合逻辑 | 原题优先；天然缺物种、数量、年龄健康、行为、预算 |
| 35 | Shopping | 初学者、夏季 hiking/camping/mountaineering、复杂天气地形、完整装备清单 | 删除详细器材枚举和“应对复杂地形/突发情况”的部分显式 contract | 增加 buy now/wait/rent/learn 的决策结构与 current products | 原题优先；改写改变了 deliverable contract，不只是偏好覆盖 |
| 39 | Real Estate | 一年内、宜居海滨、<200 万、90–120㎡、低密/花园/绿化、低楼层、医疗与气候要求 | 删除 90–120㎡、低密/花园、绿化、低楼层、冬暖夏凉/无极端天气等多条高影响强证据 | 增加 transport、resale/purchase-risk 研究倾向 | 必须用原题；这是 15 题里改写偏离最大的一题 |
| 49 | Parenting | 最近亲子沟通减少、六个月改善、阅读/游戏/角色扮演/冲突修复 | 删除“最近沟通减少”这一当前状态证据，压缩活动类型 | 增加 developmentally appropriate 与何时寻求专业支持 | 原题优先；年龄/发展阶段等仍然自然缺失 |

## Exact side-by-side text

<details>
<summary><strong>PDR-T01 · Education</strong></summary>

### Official original

I want to advance my academic qualifications. I plan to apply for PhD programs in artificial intelligence abroad within the next 1–2 years, but I have not yet decided on a specific research direction. I would like to understand the research strengths, curriculum structure, academic resources, and employment prospects of universities in different countries and regions (for example, North America, Europe, and Asia). At the same time, I care about the application requirements (language requirements, ways to strengthen my background, research or internship experience), tuition and scholarship policies, and how to create a competitive application plan based on my own circumstances. Please help me outline the characteristics of institutions and programs in the major countries/regions, list typical representative universities, and provide recommendations on choosing a direction and improving my background.

### v0.72 adapted

I want to apply for an AI PhD abroad within the next 1–2 years, but my plan is still fairly open. Research the strongest realistic pathways for me and produce a decision-ready shortlist of programs, along with a preparation roadmap covering academic fit, funding, admissions, and likely career outcomes. Base the recommendations on current, verifiable program information.

### Declared missing user-owned variables in v0.72

- research direction
- destination constraints
- funding tolerance
- post-PhD career priority

### Research/agent-owned variables

- current program strengths
- funding structures
- admission requirements
- career outcomes

</details>

<details>
<summary><strong>PDR-T04 · Education</strong></summary>

### Official original

I am a working professional seeking to enhance my career competitiveness through systematic learning, and I am considering pursuing an MBA, EMBA, or other career-related degree/non-degree programs such as data analytics. However, I currently lack a clear understanding of the differences between these programs, their suitability for me, and their long-term value. I need an in-depth overview of domestic and international programs, including learning formats (full-time, part-time, online, or hybrid), curriculum structures (core courses and elective concentrations), teaching resources (faculty background, case studies, practical opportunities), alumni networks (industry distribution, degree of internationalization), and brand influence. Please also evaluate their practical impact on different career paths and analyze their recognition and employment resources within China. Additionally, I would like to understand application requirements (academic background, work experience, language proficiency), tuition fees and scholarship policies, return-on-investment periods, and how to balance work and study. Based on this information, please help me develop a phased decision-making and learning plan, including how to clarify my learning objectives, select the right type of program, prepare application materials, address any knowledge or skill gaps in advance, and, once enrolled, efficiently leverage both learning and networking resources to maximize the program’s impact on my career development.

### v0.72 adapted

I am a working professional considering an MBA, EMBA, data-analytics program, or another career-focused learning option to improve my competitiveness. Research the realistic choices available in China and internationally, compare their long-term value, and recommend a phased decision and application plan that I could actually follow while employed. Use current evidence on program design, cost, admissions, networks, and career outcomes.

### Declared missing user-owned variables in v0.72

- target career change
- degree versus non-degree preference
- weekly time capacity
- tuition and ROI tolerance

### Research/agent-owned variables

- current program structures
- reputation and alumni evidence
- application requirements
- labor-market value

</details>

<details>
<summary><strong>PDR-T05 · Education</strong></summary>

### Official original

I plan to complete and submit a high-quality academic paper within the next 6–12 months, targeting a journal with medium-to-high impact (such as SCI Q1–Q2 or equivalent level). At present, I have limited experience in paper writing, journal selection, structuring, and responding to reviewer comments. Based on my field of study, please help me outline the complete process from topic selection, literature review, and data presentation to paper writing and submission. List the characteristics of different high-level journals (including review cycles, impact, and preferred research directions), and provide techniques for writing strong introductions, discussion sections, and cover letters. Additionally, give strategies to improve the acceptance rate, such as enhancing logical flow and originality, avoiding common reasons for rejection, and practical methods for efficiently responding to reviewer feedback and revising manuscripts.

### v0.72 adapted

I want to complete and submit a strong academic paper within the next 6–12 months. Develop an evidence-based publication strategy for me, from topic and literature positioning through analysis, writing, journal selection, submission, and revision. Recommend realistic journal-targeting and risk-reduction approaches using current, verifiable journal and field information.

### Declared missing user-owned variables in v0.72

- field and subfield
- study method
- data readiness
- target journal ambition
- writing experience

### Research/agent-owned variables

- journal fit
- current author guidelines
- review cycles
- field-specific rejection risks

</details>

<details>
<summary><strong>PDR-T06 · Career</strong></summary>

### Official original

I plan to transition into the finance industry within the next year, considering directions such as investment, risk management, or corporate financial analysis. However, I currently lack a systematic financial background and practical experience. Could you help me create a detailed learning plan? This should include the core financial knowledge I need to master, the key professional certifications I should pursue, recommended efficient and practical online learning resources, and how to find practical opportunities such as internships or volunteer projects to meet industry requirements.

### v0.72 adapted

I want to transition into the finance industry within the next year. Research viable entry pathways and build a practical learning-and-experience roadmap that includes the knowledge, credentials, projects, and market-facing steps most likely to make the transition credible. Ground the roadmap in current role requirements and hiring evidence rather than a generic finance curriculum.

### Declared missing user-owned variables in v0.72

- target finance role
- current education and skills
- weekly study capacity
- location constraints
- income and credential priorities

### Research/agent-owned variables

- current role requirements
- credential value
- course quality
- entry-level hiring routes

</details>

<details>
<summary><strong>PDR-T09 · Career</strong></summary>

### Official original

I hope to successfully transition into an AI product manager role within the next six months. Please help me design a detailed learning plan that begins with analyzing my skill gaps, identifying the differences between my current abilities and the target role requirements. Then, create specific practice projects that will allow me to apply AI product knowledge hands-on. Next, match me with target companies based on industry trends and job market demand. Finally, develop a networking strategy to help me build industry connections.

### v0.72 adapted

I want to move into an AI product-manager role within six months. Research what the role currently requires and create a decision-ready transition plan for me, including the most valuable skill gaps to close, a small set of credible portfolio projects, target-company logic, and a networking and application strategy. Prioritize actions that will materially improve hiring readiness.

### Declared missing user-owned variables in v0.72

- current professional background
- target AI product domain
- technical depth
- target company type
- networking comfort

### Research/agent-owned variables

- current AI-PM job requirements
- market demand
- portfolio project opportunities
- company hiring patterns

</details>

<details>
<summary><strong>PDR-T10 · Career</strong></summary>

### Official original

I plan to seek international career development opportunities within the next 1–2 years, ideally securing a position in an overseas company. Please provide me with an international career development roadmap, including an analysis of overseas job markets, target role requirements, language and cultural adaptation training, international résumé and interview preparation, visa and legal considerations, and strategies for improving cross-cultural communication and workplace skills. Please evaluate the employment prospects and adaptation challenges of different countries and industries, and provide a practical, actionable action plan.

### v0.72 adapted

I want to secure a suitable role with an overseas company within the next 1–2 years. Research the most realistic country-and-industry pathways and produce a practical international career roadmap covering readiness, applications, interviews, visas, and workplace adaptation. Recommendations should be based on current labor-market and immigration evidence.

### Declared missing user-owned variables in v0.72

- target occupation
- country preferences
- language readiness
- family mobility constraints
- risk tolerance

### Research/agent-owned variables

- current country and industry demand
- visa routes
- credential recognition
- compensation and adaptation risks

</details>

<details>
<summary><strong>PDR-T11 · Health</strong></summary>

### Official original

I plan to systematically improve my physique and enhance my fitness over the next six months, with a focus on increasing core strength and endurance. My goals include reducing body fat, increasing muscle definition, and being able to complete a continuous 5 km run or a similar endurance challenge by the end of the program. Please create a scientific training and nutrition plan for me, covering a phased exercise program, practical equipment-based or equipment-free workouts, basic dietary adjustment recommendations, and strategies for mitigating the negative effects of prolonged sitting in daily life. Also, provide effective methods for tracking progress and maintaining motivation.

### v0.72 adapted

Over the next six months, I want to improve core strength and endurance, reduce body fat, gain visible muscle definition, and complete a continuous 5 km run. Develop a safe, evidence-based training and nutrition program with clear phases, progress checks, and adjustment rules. The plan should be practical for everyday life and should identify important safety boundaries.

### Declared missing user-owned variables in v0.72

- current fitness baseline
- injury or medical constraints
- weekly schedule
- equipment access
- diet constraints

### Research/agent-owned variables

- safe progression rates
- evidence-based training structure
- nutrition guidance
- validated progress measures

</details>

<details>
<summary><strong>PDR-T16 · Travel</strong></summary>

### Official original

I plan to take a two-week backpacking trip within the next three months to explore the diverse cultures and natural wonders of Southeast Asia—such as tropical rainforests, historical sites, and local communities. Please design a tailored itinerary for me, including recommended destinations, transport options, accommodation choices, local specialties to try, as well as safety advice, cost estimates, and tips on local customs.

### v0.72 adapted

I am planning a two-week trip in Southeast Asia within the next three months. Research and design a coherent itinerary that combines culture, nature, and local experiences, with realistic transport, accommodation, food, safety, and cost guidance. The final plan should be current, internally feasible, and specific enough to book.

### Declared missing user-owned variables in v0.72

- travel pace
- interest priorities
- accommodation comfort
- budget level
- risk and heat tolerance

### Research/agent-owned variables

- route feasibility
- current entry requirements
- seasonal conditions
- transport and local safety

</details>

<details>
<summary><strong>PDR-T21 · Finance</strong></summary>

### Official original

I plan to make personal investments over the next six months with the goal of achieving an annualized return of at least 10%. I have no specific preference for the investment field or product type, which could include stocks, mutual funds, or other financial instruments. At the same time, I want to understand asset allocation strategies to better diversify risk and implement effective risk management during the investment process. Please provide me with targeted advice, including a personalized investment portfolio recommendation, as well as methods for tracking and evaluating my investment performance to ensure it aligns with my actual risk tolerance and market changes. I would like your professional guidance to help me plan my investments and achieve my financial objectives.

### v0.72 adapted

I am a conservative investor planning over the next six months, but I would ideally like an annualized return of at least 10%. Research whether that goal is realistic and design a personalized portfolio and risk-management approach, including concrete monitoring and adjustment rules. The recommendation should use current market evidence and should not hide the trade-offs between capital preservation, liquidity, and return.

### Declared missing user-owned variables in v0.72

- maximum acceptable drawdown
- liquidity needs
- existing assets and liabilities
- priority when risk and return conflict
- investment experience

### Research/agent-owned variables

- target feasibility
- current risk-return conditions
- instrument due diligence
- monitoring metrics

</details>

<details>
<summary><strong>PDR-T22 · Finance</strong></summary>

### Official original

Based on my retirement needs over the next 30 years, please design a comprehensive retirement security plan that integrates annuity insurance, supplemental medical insurance, and care services, with clear dynamic allocation strategies for each component. Additionally, please explain in detail the adjustment pathways under different economic cycles—such as economic growth, recession, and stability—including how to adapt flexibly and adjust coverage and allocation ratios in the face of inflation, rising medical costs, and population aging. Considering the changing needs at different life stages, please recommend specific protection measures and investment products to better meet my future retirement living requirements. I hope this plan will help me achieve a worry-free life in my later years.

### v0.72 adapted

I want a long-term retirement-security plan covering roughly the next 30 years. Research and design a practical framework that coordinates retirement savings, annuity or income options, medical protection, and later-life care, with adjustment rules for changing life stages and economic conditions. Use current evidence and make the major trade-offs and assumptions explicit.

### Declared missing user-owned variables in v0.72

- current age and retirement timing
- assets and contribution capacity
- dependents
- medical and care concerns
- desired retirement lifestyle

### Research/agent-owned variables

- product mechanics
- inflation and longevity scenarios
- medical-cost evidence
- regulatory and market conditions

</details>

<details>
<summary><strong>PDR-T30 · Creative</strong></summary>

### Official original

I plan to develop a personal media account within the next six months, aiming to build a distinctive personal brand in a niche area, attract a stable audience base, and, if possible, monetize. Please create a systematic creative plan to help me identify my target audience, choose a niche, and define my content value proposition; provide brand tone guidelines; design differentiated content themes and creative expression styles; and prepare a 3-month content topic calendar.Propose creative directions for storytelling, serialized content, and interactive formats to ensure sustained audience interest. Develop a detailed account growth strategy, including posting frequency, platform selection, and multi-platform coordination; suggest specific methods for increasing audience engagement, building a fan community, and iterating content. Provide recommendations for tracking and optimizing key performance metrics, and develop a feasible monetization pathway.Taking into account my time, budget, and skill level, create a reasonable resource allocation plan; provide competitive analysis and differentiation strategies, assess potential risks, and propose mitigation measures. Please recommend excellent domestic and international personal media case studies for reference.

### v0.72 adapted

Within the next six months, I want to build a differentiated personal-media account with a stable audience and a realistic path to monetization. Research the opportunity and create a concrete positioning, content, distribution, growth, measurement, and monetization plan that fits my circumstances. Include a usable 12-week editorial roadmap and evidence-backed platform choices.

### Declared missing user-owned variables in v0.72

- niche
- target audience
- content format and on-camera comfort
- time and budget
- brand versus revenue priority

### Research/agent-owned variables

- platform fit
- audience demand
- competitive landscape
- growth and monetization evidence

</details>

<details>
<summary><strong>PDR-T33 · Shopping</strong></summary>

### Official original

I want to purchase a range of daily essentials for my pets, including a cleaning system, food, feeders, drinking fountains, smart cameras, and toys, aiming to improve my pets’ daily comfort and my pet care efficiency, while ensuring reliable quality. Please research current mainstream pet product brands and compare their performance in terms of price, material safety, smart features, convenience, maintenance cost, and pet acceptance. Recommend a suitable combination of products for me.

### v0.72 adapted

I want to buy a coordinated set of pet-care essentials, including cleaning, feeding, hydration, monitoring, and play products. Research current options and recommend a reliable combination rather than a generic list. Compare total cost, safety, maintenance, smart features, convenience, compatibility, and likely pet acceptance using current evidence.

### Declared missing user-owned variables in v0.72

- pet species and number
- age or health needs
- behavior and acceptance constraints
- care arrangement
- budget

### Research/agent-owned variables

- current product performance
- material safety
- maintenance cost
- compatibility and failure modes

</details>

<details>
<summary><strong>PDR-T35 · Shopping</strong></summary>

### Official original

I plan to start a series of outdoor activities this summer, including hiking, camping, and mountaineering. As a beginner, I want to purchase a complete set of gear that will not only meet my basic needs but also handle different weather conditions, complex terrain, and unexpected situations.Please provide me with a detailed gear checklist, including but not limited to: backpack, waterproof clothing, hiking shoes, tent, sleeping bag, outdoor cooking equipment, navigation tools, first-aid kit, headlamp, portable water filter, and other essentials. Please consider durability, functionality, and comfort, ensuring the gear can adapt to changing outdoor environments. Also recommend suitable brands that will help me balance budget and quality.

### v0.72 adapted

I am a beginner planning to start hiking, camping, and mountaineering this summer. Research and build a complete but sensible gear and preparation plan for me, including what to buy first, what can wait, what should be rented or learned rather than purchased, and which current products offer good value. The recommendations should be safe and specific enough to act on.

### Declared missing user-owned variables in v0.72

- route and terrain
- altitude and weather exposure
- safety posture
- budget and purchase timing
- gear already owned

### Research/agent-owned variables

- route-specific technical requirements
- current product specs
- availability and price
- training-versus-purchase boundary

</details>

<details>
<summary><strong>PDR-T39 · Real Estate</strong></summary>

### Official original

I plan to purchase a retirement home in a livable coastal city within the next year. It should have beautiful scenery and a pleasant climate, ideally warm in winter and cool in summer, with no extreme weather. My budget is under ¥2 million, and I am looking for a home of about 90–120㎡, preferably in a low-density community or one with a garden and good greenery. I value medical resources and overall living comfort, and the floor should not be too high for convenient access. Please recommend suitable cities and neighborhoods, and provide key considerations for purchasing a retirement home, floor plan suggestions, and comfortable renovation ideas.

### v0.72 adapted

Within the next year, I want to buy a comfortable retirement home in a livable coastal city, with a total property budget below RMB 2 million. Research realistic cities and neighborhoods and produce a decision-ready shortlist, purchase-risk checklist, and home-layout and renovation guidance. Use current evidence on prices, climate, healthcare, transport, and long-term livability.

### Declared missing user-owned variables in v0.72

- current location and family proximity
- medical needs
- preferred climate trade-offs
- mobility and transport needs
- usage and resale priorities

### Research/agent-owned variables

- current city and neighborhood prices
- climate hazards
- medical access
- ownership and resale risks

</details>

<details>
<summary><strong>PDR-T49 · Parenting</strong></summary>

### Official original

I have noticed that my child’s communication with us has decreased recently. I plan to enhance our emotional connection and improve communication skills through a series of parent-child activities in the next six months. Please provide a comprehensive parent-child communication and emotional development plan, including emotional expression and management training, a shared reading list, conflict resolution techniques, and how to improve my child’s social and emotional understanding through family games, role-playing, and communication exercises. Please also incorporate research from psychology and education, suggest specific practical methods, and assess the effectiveness of different activity formats in strengthening parent-child relationships and promoting my child’s emotional growth.

### v0.72 adapted

Over the next six months, I want to improve communication and emotional connection with my child. Develop an evidence-based, practical family plan using conversation routines, shared activities, reading, emotion skills, and conflict-repair methods, with ways to track whether the relationship is improving. The plan should be developmentally appropriate and should state when professional support may be needed.

### Declared missing user-owned variables in v0.72

- child age and developmental stage
- specific communication pattern
- family schedule
- conflict triggers
- activity and reading preferences

### Research/agent-owned variables

- developmentally appropriate methods
- psychology and education evidence
- risk or referral boundaries
- effectiveness measures

</details>


