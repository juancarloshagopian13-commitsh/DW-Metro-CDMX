from pathlib import Path
import numpy as np
import pandas as pd


def resolver_ols_algebra_lineal(X_raw: np.ndarray, y_raw: np.ndarray, nombres_vars: list[str]) -> dict:
    y = np.asarray(y_raw, dtype=float).reshape(-1, 1)
    n = y.shape[0]

    X = np.hstack([np.ones((n, 1), dtype=float), np.asarray(X_raw, dtype=float)])

    Xt = X.T
    XtX = Xt @ X
    Xty = Xt @ y

    beta_hat = np.linalg.pinv(XtX) @ Xty

    y_hat = X @ beta_hat
    residuos = y - y_hat

    ss_res = float(np.sum(residuos ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
    rmse = float(np.sqrt(np.mean(residuos ** 2)))
    mae = float(np.mean(np.abs(residuos)))

    etiquetas = ["intercepto_beta_0"] + nombres_vars
    coeficientes = {
        etiquetas[i]: float(beta_hat[i, 0]) for i in range(len(etiquetas))
    }

    return {
        "X": X,
        "beta_hat": beta_hat,
        "coeficientes": coeficientes,
        "y_hat": y_hat.flatten(),
        "residuos": residuos.flatten(),
        "r2": r2,
        "rmse": rmse,
        "mae": mae,
    }


def localizar_csv_operacion(data_dir: Path) -> Path:
    candidatos = [
        data_dir / "fact_operacion.csv",
        data_dir / "operacion.csv",
        data_dir / "operaciones.csv",
    ]
    for ruta in candidatos:
        if ruta.exists():
            return ruta

    for ruta in sorted(data_dir.glob("*.csv")):
        if "operacion" in ruta.stem.lower() and not ruta.stem.lower().startswith("dashboard_"):
            return ruta

    raise FileNotFoundError(f"No se encontró ningún CSV de operación en: {data_dir}")


def main() -> None:
    data_dir = Path(r"C:\Users\juanh\OneDrive\Escritorio\DW-Metro-CDMX\data")
    archivo_csv = localizar_csv_operacion(data_dir)

    df = pd.read_csv(archivo_csv)

    if "Id_fecha" in df.columns and "id_fecha" not in df.columns:
        df = df.rename(columns={"Id_fecha": "id_fecha"})

    df["fecha"] = pd.to_datetime(df["id_fecha"].astype(str), format="%Y%m%d", errors="coerce")

    variables_predictoras = [
        "afluencia_pasajeros",
        "porcentaje_ocupacion",
        "velocidad_operativa_real_kmh",
        "intervalo_headway_seg",
        "distancia_intertren_m",
        "alerta_dosificacion",
        "id_incidencia",
    ]
    variable_objetivo = "tiempo_retraso_min"

    df_limpio = df.dropna(subset=["fecha", variable_objetivo] + variables_predictoras).copy()

    modelo_multiple = resolver_ols_algebra_lineal(
        X_raw=df_limpio[variables_predictoras].to_numpy(),
        y_raw=df_limpio[variable_objetivo].to_numpy(),
        nombres_vars=variables_predictoras,
    )

    df_limpio["retraso_estimado_min"] = np.round(modelo_multiple["y_hat"], 4)
    df_limpio["residuo_retraso"] = np.round(modelo_multiple["residuos"], 4)

    salida_detalle = data_dir / "dashboard_operacion_regresion.csv"
    df_limpio.to_csv(salida_detalle, index=False, encoding="utf-8")

    df_coeficientes = pd.DataFrame(
        [
            {
                "parametro": k,
                "valor_beta": round(v, 6),
                "r2_modelo": round(modelo_multiple["r2"], 6),
                "rmse_min": round(modelo_multiple["rmse"], 4),
                "mae_min": round(modelo_multiple["mae"], 4),
            }
            for k, v in modelo_multiple["coeficientes"].items()
        ]
    )
    salida_coef = data_dir / "dashboard_coeficientes_ols.csv"
    df_coeficientes.to_csv(salida_coef, index=False, encoding="utf-8")

    df_diario = (
        df_limpio.groupby("fecha", as_index=False)
        .agg(
            retraso_promedio_min=("tiempo_retraso_min", "mean"),
            afluencia_total=("afluencia_pasajeros", "sum"),
            ocupacion_promedio=("porcentaje_ocupacion", "mean"),
            velocidad_promedio_kmh=("velocidad_operativa_real_kmh", "mean"),
            total_dosificaciones=("alerta_dosificacion", "sum"),
            registros_con_incidencia=("id_incidencia", lambda s: int((s > 1).sum())),
        )
        .sort_values("fecha")
        .reset_index(drop=True)
    )
    df_diario["t_dias"] = np.arange(len(df_diario), dtype=float)

    for metrica in ["retraso_promedio_min", "afluencia_total", "registros_con_incidencia"]:
        reg_t = resolver_ols_algebra_lineal(
            X_raw=df_diario[["t_dias"]].to_numpy(),
            y_raw=df_diario[metrica].to_numpy(),
            nombres_vars=["t_dias"],
        )
        df_diario[f"{metrica}_tendencia"] = np.round(reg_t["y_hat"], 4)

    salida_tendencia = data_dir / "dashboard_tendencia_diaria.csv"
    df_diario.to_csv(salida_tendencia, index=False, encoding="utf-8")

    print(f"Archivo leído: {archivo_csv.name}")
    print("=== Coeficientes OLS (Álgebra Lineal) ===")
    for k, v in modelo_multiple["coeficientes"].items():
        print(f"  {k:<30}: {v:.6f}")
    print(f"  R^2: {modelo_multiple['r2']:.4f} | RMSE: {modelo_multiple['rmse']:.4f} min")
    print(f"\nArchivos generados en {data_dir}:")
    print(f"  1. {salida_detalle.name}")
    print(f"  2. {salida_coef.name}")
    print(f"  3. {salida_tendencia.name}")


if __name__ == "__main__":
    main()