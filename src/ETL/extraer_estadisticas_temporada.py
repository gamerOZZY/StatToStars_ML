import argparse
import time
from pathlib import Path

import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats


# Directorio raíz del proyecto
RAIZ_PROYECTO = Path(__file__).resolve().parent.parent.parent

DIRECTORIO_BRONZE = (
    RAIZ_PROYECTO
    / "data"
    / "bronze"
    / "league_dash_player_stats"
)

# Pausa entre peticiones
PAUSA_SEGUNDOS = 2

# Número máximo de intentos
MAX_INTENTOS = 5


def obtener_estadisticas(temporada, tipo_medicion):
    """
    Extrae todas las estadísticas de los jugadores de una temporada.

    tipo_medicion:
        Base
        Advanced
    """

    ultimo_error = None

    for intento in range(MAX_INTENTOS):
        try:
            respuesta = leaguedashplayerstats.LeagueDashPlayerStats(
                season=temporada,
                season_type_all_star="Regular Season",
                per_mode_detailed="PerGame",
                measure_type_detailed_defense=tipo_medicion,
                timeout=60
            )

            dataframes = respuesta.get_data_frames()

            if not dataframes:
                raise ValueError(
                    f"Sin DataFrames para {temporada}, "
                    f"MeasureType={tipo_medicion}"
                )

            return dataframes[0]

        except Exception as error:
            ultimo_error = error

            espera = min(2 ** intento * 2, 60)

            print(
                f"Error en {temporada} ({tipo_medicion}). "
                f"Intento {intento + 1}/{MAX_INTENTOS}: {error}"
            )

            if intento < MAX_INTENTOS - 1:
                print(f"Esperando {espera} segundos...")
                time.sleep(espera)

    raise RuntimeError(
        f"No fue posible extraer {temporada}, "
        f"MeasureType={tipo_medicion}"
    ) from ultimo_error


def guardar_csv(dataframe, temporada, tipo_medicion):
    """
    Guarda el DataFrame sin transformar sus columnas.
    """

    directorio = DIRECTORIO_BRONZE / tipo_medicion.lower()
    directorio.mkdir(parents=True, exist_ok=True)

    ruta = directorio / f"season_{temporada}.csv"

    dataframe.to_csv(
        ruta,
        index=False,
        encoding="utf-8"
    )

    print(f"Archivo guardado: {ruta}")
    print(f"Registros: {len(dataframe)}")
    print(f"Columnas: {len(dataframe.columns)}")


def extraer_temporada(temporada):
    """
    Extrae las estadísticas Base y Advanced de una temporada.
    """

    for tipo_medicion in ["Base", "Advanced"]:

        print(
            f"\nExtrayendo temporada {temporada} "
            f"| MeasureType={tipo_medicion}"
        )

        dataframe = obtener_estadisticas(
            temporada,
            tipo_medicion
        )

        guardar_csv(
            dataframe,
            temporada,
            tipo_medicion
        )

        time.sleep(PAUSA_SEGUNDOS)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Extrae estadísticas generales y avanzadas "
            "de jugadores de la NBA."
        )
    )

    parser.add_argument(
        "--temporadas",
        nargs="+",
        required=True,
        help='Temporadas, por ejemplo: "2022-23" "2023-24"'
    )

    argumentos = parser.parse_args()

    for temporada in argumentos.temporadas:
        extraer_temporada(temporada)


if __name__ == "__main__":
    main()
