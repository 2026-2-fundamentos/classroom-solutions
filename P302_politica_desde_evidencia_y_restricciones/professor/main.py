from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ACTIVITY_DIR / "data"
SUBMISSION_DIR = ACTIVITY_DIR / "submission"
SLOT_COLUMNS = ["grade_1_slots", "grade_2_slots", "grade_3_slots"]
VALUE_COLUMNS = ["value_grade_1", "value_grade_2", "value_grade_3"]


def evaluate_policies(policies: pd.DataFrame) -> pd.DataFrame:
    assessment = policies.copy()
    assessment["allocated_slots"] = assessment[SLOT_COLUMNS].sum(axis=1)
    assessment["expected_learning_gain"] = sum(
        assessment[slot] * assessment[value]
        for slot, value in zip(SLOT_COLUMNS, VALUE_COLUMNS)
    )
    assessment["capacity_ok"] = assessment["allocated_slots"].eq(
        assessment["total_slots"]
    )
    assessment["minimum_ok"] = assessment[SLOT_COLUMNS].ge(
        assessment["min_slots_per_grade"], axis=0
    ).all(axis=1)
    assessment["feasible"] = assessment["capacity_ok"] & assessment["minimum_ok"]
    return assessment


def select_policy(assessment: pd.DataFrame) -> pd.Series:
    feasible_policies = assessment.loc[assessment["feasible"]]
    if feasible_policies.empty:
        raise ValueError("No hay una política factible para la capacidad y el mínimo definidos.")

    return feasible_policies.nlargest(1, "expected_learning_gain").iloc[0]


def explain_selection(assessment: pd.DataFrame, selected_policy_id: str) -> pd.DataFrame:
    explanation = assessment.copy()
    explanation["decision_status"] = "descartada"
    explanation["decision_reason"] = "Ofrece menor ganancia esperada que la política seleccionada."

    infeasible = ~explanation["feasible"]
    explanation.loc[infeasible, "decision_reason"] = (
        "No cumple la capacidad disponible o el mínimo garantizado por grado."
    )

    selected = explanation["policy_id"].eq(selected_policy_id)
    explanation.loc[selected, "decision_status"] = "seleccionada"
    explanation.loc[selected, "decision_reason"] = (
        "Maximiza la ganancia esperada entre las políticas factibles."
    )
    return explanation


def build_policy_contract(selected: pd.Series, assessment: pd.DataFrame) -> dict:
    discarded = assessment.loc[assessment["policy_id"].ne(selected["policy_id"])]
    return {
        "analytical_question": (
            "¿Cómo deben asignarse 40 cupos de tutoría para maximizar la "
            "ganancia esperada sin incumplir el mínimo por grado?"
        ),
        "decision_context": "Asignación de cupos de tutoría antes de cada periodo académico.",
        "decision_cadence": "Una vez por periodo académico, antes de abrir las tutorías.",
        "response_need": "La asignación debe estar aprobada antes de la matrícula del periodo.",
        "decision_owner": "Dirección académica",
        "execution_mode": "Aprobación humana de una recomendación computable.",
        "selected_policy": {
            "policy_id": selected["policy_id"],
            "policy": selected["policy"],
            "grade_1_slots": int(selected["grade_1_slots"]),
            "grade_2_slots": int(selected["grade_2_slots"]),
            "grade_3_slots": int(selected["grade_3_slots"]),
        },
        "objective": "Maximizar la ganancia esperada de aprendizaje.",
        "expected_learning_gain": int(selected["expected_learning_gain"]),
        "constraints": {
            "total_slots": int(selected["total_slots"]),
            "minimum_slots_per_grade": int(selected["min_slots_per_grade"]),
        },
        "safeguards": [
            "No asignar más cupos que la capacidad disponible.",
            "Garantizar el mínimo de cupos definido para cada grado.",
        ],
        "exception_and_human_authority": (
            "Escalar a la Dirección académica si cambia la capacidad o si no existe "
            "una política factible."
        ),
        "review_trigger": "Revisar la política si la asistencia por grado es menor a 70%.",
        "outcome_monitor": "Asistencia por grado y ganancia de aprendizaje observada.",
        "discarded_policies": [
            {
                "policy_id": row["policy_id"],
                "policy": row["policy"],
                "reason": row["decision_reason"],
            }
            for _, row in discarded.iterrows()
        ],
        "data_limitation": (
            "Los valores del caso son parámetros hipotéticos de una reducción "
            "pedagógica; no son estimaciones publicadas de Project STAR."
        ),
    }


def build_recommendation(selected: pd.Series) -> pd.DataFrame:
    recommendation = pd.DataFrame([selected]).copy()
    recommendation["decision_owner"] = "Dirección académica"
    recommendation["execution_mode"] = "Aprobación humana de una recomendación computable."
    recommendation["review_trigger"] = "Revisar si la asistencia por grado es menor a 70%."
    return recommendation


def main() -> None:
    policies = pd.read_csv(DATA_DIR / "policy_options.csv")
    assessment = evaluate_policies(policies)
    selected = select_policy(assessment)
    explained_assessment = explain_selection(assessment, selected["policy_id"])
    policy_contract = build_policy_contract(selected, explained_assessment)

    explained_assessment.to_csv(SUBMISSION_DIR / "policy_assessment.csv", index=False)
    build_recommendation(selected).to_csv(
        SUBMISSION_DIR / "policy_recommendation.csv", index=False
    )
    (SUBMISSION_DIR / "policy_contract.json").write_text(
        json.dumps(policy_contract, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
