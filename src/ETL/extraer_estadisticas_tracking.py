import argparse
import time
from pathlib import Path

from nba_api.stats.endpoints import leaguedashptstats


RAIZ_PROYECTO = Path(__file__).resolve().parent.parent

DIRECTORIO_BRONZE = (
    RAIZ_PROYECTO
    / "data"
    / "bronze"
    / "league_dash_pt_stats"
)

PAUSA_SEGUNDOS = 2
MAX_INTENTOS = 5



def obtener_tipos_medicion():
    """
    Devuelve los tipos de estadísticas Player Tracking
    admitidos por LeagueDashPtStats.
    """

    return [
        "SpeedDistance",
        "Rebounding",
        "Possessions",
        "CatchShoot",
        "PullUpShot",
        "Defense",
        "Drives",
        "Passing",
        "ElbowTouch",
        "PostTouch",
        "PaintTouch",
        "Efficiency"
    ]




def obtener_estadisticas(temporada, tipo_medicion):
    """
    Obtiene las estadísticas de seguimiento de todos los jugadores
    para una temporada y un tipo de medición.
    """

    ultimo_error = None

    for intento in range(MAX_INTENTOS):
        try:
            respuesta = leaguedashptstats.LeagueDashPtStats(
                season=temporada,
                season_type_all_star="Regular Season",
                per_mode_simple="PerGame",
                player_or_team="Player",
                pt_measure_type=tipo_medicion,
                timeout=60
            )

            dataframes = respuesta.get_data_frames()

            if not dataframes:
                raise ValueError(
                    f"Respuesta vacía para {tipo_medicion}"
                )

            return dataframes[0]

        except Exception as error:
            ultimo_error = error

            espera = min(2 ** intento * 2, 60)

            print(
                f"Error en {temporada}, "
                f"tipo {tipo_medicion}. "
                f"Intento {intento + 1}/{MAX_INTENTOS}: {error}"
            )

            if intento < MAX_INTENTOS - 1:
                print(f"Esperando {espera} segundos...")
                time.sleep(espera)

    raise RuntimeError(
        f"No fue posible obtener {tipo_medicion} "
        f"para {temporada}"
    ) from ultimo_error


def guardar_csv(dataframe, temporada, tipo_medicion):
    """
    Guarda la respuesta del endpoint en un CSV independiente.
    """

    directorio = (
        DIRECTORIO_BRONZE
        / f"season_{temporada}"
    )

    directorio.mkdir(parents=True, exist_ok=True)

    nombre_archivo = (
        tipo_medicion.lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
    )

    ruta = directorio / f"{nombre_archivo}.csv"

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
    Extrae todas las familias de estadísticas disponibles.
    """

    tipos_medicion = obtener_tipos_medicion()

    print(f"\nTemporada: {temporada}")
    print(f"Tipos disponibles: {tipos_medicion}")

    for tipo_medicion in tipos_medicion:

        print(
            f"\nExtrayendo {tipo_medicion} "
            f"para la temporada {temporada}"
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
            "Extrae estadísticas Player Tracking "
            "de la NBA por temporada."
        )
    )

    parser.add_argument(
        "--temporadas",
        nargs="+",
        required=True,
        help='Ejemplo: "2022-23" "2023-24"'
    )

    argumentos = parser.parse_args()

    for temporada in argumentos.temporadas:
        extraer_temporada(temporada)


if __name__ == "__main__":
    main()

