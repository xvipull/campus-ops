let
    Source = Odbc.DataSource("dsn=CampusOpsSQLite", [HierarchicalNavigation=true]),
    Database = Source{[Name="campus_ops",Kind="Database"]}[Data],
    Enrollment = Value.NativeQuery(
        Database,
        "select * from vw_kpi_enrollment_term_org order by start_date, org_code",
        null,
        [EnableFolding=true]
    )
in
    Enrollment
