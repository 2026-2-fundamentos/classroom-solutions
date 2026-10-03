from pathlib import Path

import pandas as pd


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
# Las columnas esperadas hacen explícito qué debe conservarse para que el resultado sea confiable.

DRIVER_COLUMNS = {"driverId", "name", "certified"}
TIMESHEET_COLUMNS = {"driverId", "hours-logged", "miles-logged"}


def build_certified_driver_totals(
    drivers: pd.DataFrame, timesheet: pd.DataFrame
) -> pd.DataFrame:
    # La transformación se aísla para comprobar el resultado sin leer ni escribir archivos.

    if not DRIVER_COLUMNS.issubset(drivers.columns):
        raise ValueError("La tabla de conductores no contiene las columnas requeridas.")
    if not TIMESHEET_COLUMNS.issubset(timesheet.columns):
        raise ValueError("La tabla de turnos no contiene las columnas requeridas.")

    totals = timesheet.groupby("driverId", as_index=False).agg(
        total_hours=("hours-logged", "sum"), total_miles=("miles-logged", "sum")
    )
    certified_drivers = drivers.loc[drivers["certified"].eq("Y"), ["driverId", "name"]]

    return (
        certified_drivers.merge(totals, on="driverId", how="inner")
        .sort_values("driverId")
        .reset_index(drop=True)
    )


def main() -> None:
    # La ejecución integra las piezas ya probadas y deja un resultado disponible para su consumo.

    data_dir = ACTIVITY_DIR / "data"
    drivers = pd.read_csv(data_dir / "drivers.csv")
    timesheet = pd.read_csv(data_dir / "timesheet.csv")
    summary = build_certified_driver_totals(drivers, timesheet)

    output_path = ACTIVITY_DIR / "submission" / "certified_driver_totals.csv"
    summary.to_csv(output_path, index=False)
    print(f"Resumen generado: {output_path.name}")


if __name__ == "__main__":
    main()
