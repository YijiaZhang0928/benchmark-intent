#!/usr/bin/env ruby
# frozen_string_literal: true

require "csv"
require "json"
require "zlib"
require "yaml"

ROOT = File.expand_path("../..", __dir__)
DIR = __dir__
SCREEN = File.join(DIR, "screening_50.csv")
PROTOCOL = File.join(DIR, "selection_protocol.yaml")
TASKS_GZ = File.join(ROOT, "data/pdr_import_v0_51/raw/tasks_en.jsonl.gz")
FAMILY = File.join(ROOT, "data/pdr_import_v0_51/derived/family_intake.csv")

rows = CSV.read(SCREEN, headers: true)
raise "expected 50 task rows" unless rows.length == 50

ids = rows.map { |row| Integer(row["task_id"]) }
raise "task ids must be 1..50 exactly" unless ids.sort == (1..50).to_a
raise "duplicate task ids" unless ids.uniq.length == 50

selected_rows = rows.select { |row| row["selected"] == "yes" }
raise "expected exactly 15 selected tasks" unless selected_rows.length == 15

selected_rows.each do |row|
  raise "selected task #{row['task_id']} is not leverage 2" unless row["personalization_leverage"] == "2"
  %w[non_surface_change history_groundability dr_requirement].each do |field|
    raise "selected task #{row['task_id']} fails #{field}" unless row[field] == "pass"
  end
  dims = Integer(row["preference_dimension_count"])
  raise "selected task #{row['task_id']} has invalid node count" unless (2..4).cover?(dims)
  %w[demographic_token_risk profile_contradiction_risk].each do |field|
    raise "selected task #{row['task_id']} has high #{field}" if row[field] == "high"
  end
end

protocol = YAML.safe_load(File.read(PROTOCOL))
protocol_ids = protocol.fetch("selected_task_ids").map(&:to_i)
raise "protocol selected ids mismatch" unless protocol_ids == selected_rows.map { |row| Integer(row["task_id"]) }
raise "domain quota is prohibited" unless protocol.fetch("explicitly_not_used").include?("equal quota per domain")

tasks = {}
Zlib::GzipReader.open(TASKS_GZ) do |gz|
  gz.each_line do |line|
    item = JSON.parse(line)
    tasks.fetch(item.fetch("taskid"), nil).nil? or raise "duplicate upstream task"
    tasks[item.fetch("taskid")] = item
  end
end
raise "upstream task count mismatch" unless tasks.length == 50

families = CSV.read(FAMILY, headers: true).to_h { |row| [Integer(row["source_task_id"]), row] }
raise "family inventory mismatch" unless families.length == 50

selected_path = File.join(DIR, "selected_15.jsonl")
File.open(selected_path, "w") do |file|
  selected_rows.each do |row|
    task_id = Integer(row["task_id"])
    upstream = tasks.fetch(task_id)
    family = families.fetch(task_id)
    file.puts JSON.generate({
      "slice_version" => "0.61",
      "source" => "PDR-Bench",
      "source_commit" => protocol.dig("upstream", "commit"),
      "task_id" => task_id,
      "family_id" => format("PDR_T%02d", task_id),
      "domain" => upstream.fetch("domain"),
      "task" => upstream.fetch("task"),
      "candidate_user_ids" => family.fetch("candidate_user_ids").split("|"),
      "personalization_leverage" => Integer(row["personalization_leverage"]),
      "candidate_preference_nodes" => row.fetch("candidate_preference_nodes").split("|"),
      "screen_reason" => row.fetch("screen_reason"),
      "selection_status" => "provisional_author_screen",
      "pair_gold_status" => "not_selected_requires_separate_human_audit"
    })
  end
end

domain_counts = selected_rows.group_by { |row| row["domain"] }.transform_values(&:length)
leverage_counts = rows.group_by { |row| row["personalization_leverage"] }.transform_values(&:length)
exact_pair_count = selected_rows.sum do |row|
  families.fetch(Integer(row["task_id"])).fetch("candidate_user_ids").split("|").length
end
raise "selected exact published-pair count mismatch" unless exact_pair_count == protocol.fetch("published_pair_count_if_all_official_pairs_retained")

summary = {
  "schema_version" => "0.61",
  "source_task_count" => rows.length,
  "selected_task_count" => selected_rows.length,
  "selected_task_ids" => selected_rows.map { |row| Integer(row["task_id"]) },
  "selected_domain_counts" => domain_counts,
  "leverage_counts_all_50" => leverage_counts,
  "selected_published_task_user_pair_count" => exact_pair_count,
  "selection_status" => "provisional_author_screen",
  "human_validation_pending" => true
}
File.write(File.join(DIR, "summary.json"), JSON.pretty_generate(summary) + "\n")

md = +"# PDR-Bench 50 → 15 个性化诊断任务切片\n\n"
md << "> v0.61 · 2026-09-03 · provisional author screen；不是已完成人工确认的 benchmark gold。\n\n"
md << "本切片不按 domain 均匀抽样。先对官方 50 题标注 `Personalization leverage=0/1/2`，再要求非表面内容改变、history 可取证、2–4 个候选偏好节点和真实 Deep Research 需求全部过门。超过 15 题时才按 profile 对比、冲突风险、可验证性和构念冗余排序。\n\n"
md << "## 入选 15 题\n\n"
md << "| ID | Domain | Task | 候选 preference nodes |\n|---:|---|---|---|\n"
selected_rows.each do |row|
  md << "| #{row['task_id']} | #{row['domain']} | #{row['short_label']} | #{row['candidate_preference_nodes'].split('|').join('；')} |\n"
end
md << "\nDomain 分布为：#{domain_counts.map { |key, value| "#{key} #{value}" }.join('、')}。这是筛选结果，不是预设配额。\n\n"
md << "若保留官方全部 task–user 映射，15 题对应 #{exact_pair_count} 个 bridge pair，而不是机械的 75：公开数据中 task 10 有 6 位候选用户。Ask/Infer 的 matched/swapped A/B gold 仍须另做双人 profile-pair 审计。\n\n"
md << "## 解释边界\n\n"
md << "- `selected=yes` 只表示优先进入人工 qualification，不表示 task、history、偏好节点或用户配对已经成为 gold。\n"
md << "- PDR 的模拟 memory/chat 只能作 bridge 或 stress test，不能称为自然 history。\n"
md << "- `Personalization leverage=2` 是必要非充分条件；高风险冲突、缺失 floor plan、法律证据依赖或与已选构念冗余仍可导致不入选。\n"
md << "- 完整逐题理由见 `screening_50.csv`；机器规则见 `selection_protocol.yaml`。\n"
File.write(File.join(DIR, "selected_15.md"), md)

puts JSON.generate(summary)
