import json
from pathlib import Path

import pandas as pd


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
EXPECTED_COLUMNS = ("factory_id", "machine_id", "daily_units_produced", "factory_date")
BUSINESS_KEY = ("factory_id", "machine_id", "factory_date")


def validate_data(dataframe: pd.DataFrame) -> list[str]:
    # El contrato convierte expectativas operativas en condiciones verificables antes de usar los datos.

    violations = []
    if tuple(dataframe.columns) != EXPECTED_COLUMNS:
        return ["El esquema no coincide con el contrato esperado."]
    if not dataframe["factory_id"].gt(0).all():
        violations.append("factory_id debe contener valores positivos.")
    if not dataframe["machine_id"].gt(0).all():
        violations.append("machine_id debe contener valores positivos.")
    if not dataframe["daily_units_produced"].ge(0).all():
        violations.append("daily_units_produced no puede ser negativo.")
    if (
        pd.to_datetime(dataframe["factory_date"], format="%Y-%m-%d", errors="coerce")
        .isna()
        .any()
    ):
        violations.append("factory_date debe contener fechas válidas.")
    if dataframe.duplicated(BUSINESS_KEY).any():
        violations.append("La llave factory_id-machine_id-factory_date debe ser única.")
    return violations


def main() -> None:
    # Un reporte persistente permite revisar qué datos fueron aceptados antes de producir indicadores.

    results = []
    for data_path in sorted((ACTIVITY_DIR / "data").glob("*.csv")):
        violations = validate_data(pd.read_csv(data_path))
        results.append(
            {
                "dataset": data_path.name,
                "accepted": not violations,
                "violations": violations,
            }
        )

    report_path = ACTIVITY_DIR / "submission" / "validation_report.json"
    report_path.write_text(
        json.dumps({"datasets": results}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Reporte generado: {report_path.name}")


if __name__ == "__main__":
    main()
