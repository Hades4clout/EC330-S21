# Terrenos sin construir por zona (EasyHome)

Fuente: TxGIO StratMap Land Parcels 2025 (colección 0fa04328-872e-481c-b453-126a74777593), 8 condados: Bexar, Guadalupe, Comal, Atascosa, Wilson, Medina, Kendall, Bandera.

- Zona = tract del Censo 2020 del mapa EasyHome. Parcela asignada por su centroide.
- Total = parcelas con LAND_VALUE > $1,000. Sin construir = de esas, IMP_VALUE = 0 y dueño no público/HOA/servicios.
- `vacant_by_tract.csv`: GEOID, vacant, total, pct (tantos/total). `calc_vacant_by_tract.py` lo genera (necesita geopandas y los .gdb descargados).
