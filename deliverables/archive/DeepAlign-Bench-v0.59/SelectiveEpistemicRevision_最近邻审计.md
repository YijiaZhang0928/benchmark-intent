# When Should an Assistant Change Its Mind?：选择性认知修订最近邻审计

完整可交付版与研究源文件保持一致，请见 [`proposal/SelectiveEpistemicRevision_最近邻审计.md`](../proposal/SelectiveEpistemicRevision_最近邻审计.md)。

## 核心结论

- “多轮保持前后一致、该改口时改口”本身已被 FlipFlop、SYCON、SycoBench、MultiChallenge、Belief-R、BeliefShift、EvolIF 与 ACL 2026 belief-consistency/repair 工作直接覆盖，不能作为 broad gap。
- 用户给出“方法创新也可以”不是纯粹施压，而是加入新的评价判据。正确更新应保留“DeepAlign 与 PDR-Bench 的能力重叠仍大”，同时把“作为 measurement paper 的可行性”改为条件性成立。
- 仍可反证的窄候选是 **Premise-Conditioned Selective Revision**：新证据、目标或判据只更新其依赖闭包，未受影响承诺保持，并准确归因到改变的前提。
- 该候选本质上是 DeltaBench 的 dialogue/epistemic 实例化，属于组合型方法 gap；当前不替代 v0.43 DeepAlign measurement-validity 分支。
- 下一步只建议做 3-family、432-trajectory novelty-kill pilot；若普通 recall、flip rate、Belief-R update/maintain 或 MultiChallenge self-coherence 已能完整解释结果，则停止。

工作标题：

> **When Should an Assistant Change Its Mind? Benchmarking Minimal, Evidence-Calibrated Revision in Long-Horizon Dialogue**

一句话：

> 我们不奖励 agent 一味坚持或频繁改口，而是评价它能否在多轮专业协作中，根据新增证据、目标或评价标准，只更新真正受影响的判断，保留其余承诺，并准确说明为什么改变。
