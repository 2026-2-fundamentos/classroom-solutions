from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def evaluate_policies(options: pd.DataFrame) -> pd.DataFrame:
    result = options.copy()
    result["expected_conversions"] = result.contacts * result.expected_conversion
    result["expected_net_value"] = (
        result.expected_conversions * result.net_value_per_conversion
        - result.contacts * result.contact_cost
    )
    result["capacity_ok"] = result.contacts <= result.capacity_limit
    result["exposure_ok"] = result.high_contact_share <= result.max_high_contact_share
    result["feasible"] = result.capacity_ok & result.exposure_ok
    return result


def make_decision_brief(options: pd.DataFrame) -> pd.DataFrame:
    evaluated = evaluate_policies(options)
    recommendation = evaluated.loc[evaluated.feasible].nlargest(1, "expected_net_value")
    brief = recommendation.loc[
        :, [
            "policy_id",
            "policy",
            "contacts",
            "expected_conversions",
            "expected_net_value",
            "capacity_ok",
            "exposure_ok",
        ]
    ].copy().reset_index(drop=True)
    brief["decision_owner"] = "Responsable comercial"
    brief["review_trigger"] = "Revisar si la conversión observada cae por debajo de 10%."
    return brief


def make_policy_contract(brief: pd.DataFrame) -> pd.DataFrame:
    contract = brief.copy()
    contract["decision_cadence"] = "Antes de cada campaña de depósito"
    contract["response_need"] = "Antes de iniciar la campaña"
    contract["execution_mode"] = "Recomendación con aprobación humana"
    contract["objective"] = "Maximizar el valor neto esperado de la campaña"
    contract["capacity_constraint"] = "No superar 1.000 contactos"
    contract["exposure_safeguard"] = (
        "No superar el límite de exposición del segmento con contacto intenso"
    )
    contract["exception_rule"] = (
        "Escalar a la responsable comercial si ninguna política es factible"
    )
    contract["outcome_metric"] = "Conversión observada y valor neto realizado"
    return contract


def main() -> None:
    options = pd.read_csv(ROOT / "data" / "policy_options.csv")
    brief = make_decision_brief(options)
    policy_contract = make_policy_contract(brief)
    brief.to_csv(ROOT / "submission" / "decision_brief.csv", index=False)
    policy_contract.to_csv(ROOT / "submission" / "policy_contract.csv", index=False)


if __name__ == "__main__":
    main()
