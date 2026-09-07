# Excel companion

`CampusOps_Decision_Companion.xlsx` is an offline decision workbook generated from `data/campus_ops.db`. It includes executive KPIs, trend analysis, scenario controls, exceptions, data-quality reconciliation, definitions, and governed model data.

The `Scenarios` sheet uses editable amber growth inputs with formula-driven course/faculty/room pressure outputs. `Model Data` supplies the chart and formula ranges. `Power Query` contains an import-ready query; the same query is available as `power_query/CampusOps_Model.m`. Configure the approved SQLite ODBC DSN as `CampusOpsSQLite` before refreshing in Excel.

The workbook uses native charts and formula-driven summaries because PivotTable export is not reliable in the project authoring runtime. Users can create PivotTables/PivotCharts from the Excel `EnrollmentModel` and `PressureModel` tables without changing the governed source data.
