# Power BI decision product

This folder contains a source-controlled Power BI Project scaffold, theme, governed SQLite Power Query connection, DAX measures, and build specification for the six-page decision report. The model uses the SQLite star schema built by `src/run_pipeline.py`.

Use an approved SQLite ODBC driver and create the `CampusOpsSQLite` DSN before refresh. Follow `report_build.md` to wire the semantic model, use the proper Date table, create report pages, enable drill-through and tooltips, and publish through the institution’s governed Power BI workspace.
