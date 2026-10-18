@echo off
@echo ====================================================
@echo .
@echo Iniciando la descarga de las estadisticas 
@echo de cada rubro de cada jugador por temporada
@echo .
@echo ====================================================
@echo off
@echo ====================================================
@echo .
@echo Iniciando la descarga de las estadisticas 
@echo de cada jugador en la temporada
@echo .
@echo ====================================================
python src/ETL/extraer_estadisticas_tracking.py --temporadas "2015-16" "2016-17" "2017-18" "2018-19" "2019-20" "2020-21" "2021-22" "2022-23" "2023-24" "2024-25"