import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const pilotRoot = path.resolve(here, "..");

const readJson = (relativePath) =>
  JSON.parse(fs.readFileSync(path.resolve(here, relativePath), "utf8"));

const mapping = readJson("criterion_preference_unit_map.json");
const units = readJson("preference_units.json");
const questions = readJson("clarification_question_audit.json");
const sourceCriteria = JSON.parse(
  fs.readFileSync(path.resolve(pilotRoot, "task/original_criteria.json"), "utf8"),
);

const assert = (condition, message) => {
  if (!condition) throw new Error(message);
};

const sourceIndex = new Map();
for (const [dimension, criteria] of Object.entries(
  sourceCriteria.personalization_criterions,
)) {
  criteria.forEach((criterion, index) => {
    sourceIndex.set(`${dimension}:${index + 1}`, criterion);
  });
}

assert(mapping.criteria.length === 44, "Expected exactly 44 mapped criteria");
assert(
  new Set(mapping.criteria.map((criterion) => criterion.criterion_id)).size === 44,
  "Criterion IDs must be unique",
);

for (const criterion of mapping.criteria) {
  const source = sourceIndex.get(
    `${criterion.dimension}:${criterion.dimension_index}`,
  );
  assert(source, `Missing source criterion for ${criterion.criterion_id}`);
  assert(
    source.criterion === criterion.criterion,
    `Criterion text mismatch for ${criterion.criterion_id}`,
  );
  assert(
    Math.abs(source.weight - criterion.criterion_weight) < 1e-12,
    `Criterion weight mismatch for ${criterion.criterion_id}`,
  );
  const expectedEffectiveWeight =
    sourceCriteria.personalization_weights[criterion.dimension] * source.weight;
  assert(
    Math.abs(expectedEffectiveWeight - criterion.effective_weight) < 1e-12,
    `Effective weight mismatch for ${criterion.criterion_id}`,
  );
}

const unitIds = new Set(units.units.map((unit) => unit.unit_id));
assert(unitIds.size === 22, "Expected exactly 22 unique preference units");

for (const criterion of mapping.criteria) {
  assert(
    unitIds.has(criterion.primary_unit),
    `Unknown primary unit in ${criterion.criterion_id}`,
  );
  for (const unitId of criterion.secondary_units) {
    assert(
      unitIds.has(unitId),
      `Unknown secondary unit ${unitId} in ${criterion.criterion_id}`,
    );
  }
}

const primaryMassByUnit = new Map([...unitIds].map((unitId) => [unitId, 0]));
const influenceMassByUnit = new Map([...unitIds].map((unitId) => [unitId, 0]));

for (const criterion of mapping.criteria) {
  primaryMassByUnit.set(
    criterion.primary_unit,
    primaryMassByUnit.get(criterion.primary_unit) + criterion.effective_weight,
  );
  for (const unitId of [criterion.primary_unit, ...criterion.secondary_units]) {
    influenceMassByUnit.set(
      unitId,
      influenceMassByUnit.get(unitId) + criterion.effective_weight,
    );
  }
}

for (const unit of units.units) {
  assert(
    Math.abs(primaryMassByUnit.get(unit.unit_id) - unit.primary_rubric_mass) <
      1e-9,
    `Primary rubric mass mismatch for ${unit.unit_id}`,
  );
  assert(
    Math.abs(influenceMassByUnit.get(unit.unit_id) - unit.influence_rubric_mass) <
      1e-9,
    `Influence rubric mass mismatch for ${unit.unit_id}`,
  );
  for (const condition of ["interactive", "full_persona"]) {
    const status = unit.condition_status[condition];
    assert(status, `Missing ${condition} status for ${unit.unit_id}`);
    for (const field of [
      "relevant",
      "known",
      "asked",
      "resolved",
      "reflected",
    ]) {
      assert(
        typeof status[field] === "boolean",
        `${unit.unit_id}.${condition}.${field} must be boolean`,
      );
    }
  }
}

const primaryMass = [...primaryMassByUnit.values()].reduce(
  (sum, value) => sum + value,
  0,
);
assert(Math.abs(primaryMass - 1) < 1e-9, "Primary rubric mass must sum to 1");

assert(questions.questions.length === 11, "Expected exactly 11 questions");
assert(
  questions.questions.filter((question) => question.condition === "interactive")
    .length === 6,
  "Expected six interactive questions",
);
assert(
  questions.questions.filter((question) => question.condition === "full_persona")
    .length === 5,
  "Expected five full-persona questions",
);
assert(
  new Set(questions.questions.map((question) => question.question_id)).size ===
    11,
  "Question IDs must be unique",
);

for (const question of questions.questions) {
  assert(question.asked === true, `${question.question_id} must be observed`);
  for (const unitId of question.preference_units) {
    assert(
      unitIds.has(unitId),
      `Unknown question unit ${unitId} in ${question.question_id}`,
    );
  }
}

console.log(
  JSON.stringify(
    {
      status: "PASS",
      criteria: mapping.criteria.length,
      units: units.units.length,
      questions: questions.questions.length,
      primary_rubric_mass: Number(primaryMass.toFixed(12)),
      source_criterion_text_and_weights_exact: true,
      unit_references_valid: true,
      status_fields_valid: true,
    },
    null,
    2,
  ),
);
