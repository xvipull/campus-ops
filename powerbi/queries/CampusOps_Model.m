let
    Source = Odbc.DataSource("dsn=CampusOpsSQLite", [HierarchicalNavigation=true]),
    Database = Source{[Name="campus_ops",Kind="Database"]}[Data],
    Enrollment = Value.NativeQuery(Database, "select * from fact_enrollment", null, [EnableFolding=true]),
    Terms = Value.NativeQuery(Database, "select * from dim_term", null, [EnableFolding=true]),
    AcademicOrg = Value.NativeQuery(Database, "select * from dim_academic_org", null, [EnableFolding=true]),
    Students = Value.NativeQuery(Database, "select * from dim_student", null, [EnableFolding=true]),
    CourseSections = Value.NativeQuery(Database, "select * from fact_course_section", null, [EnableFolding=true]),
    Plan = Value.NativeQuery(Database, "select * from fact_plan", null, [EnableFolding=true]),
    ResourcePressure = Value.NativeQuery(Database, "select * from vw_resource_pressure", null, [EnableFolding=true]),
    Quality = Value.NativeQuery(Database, "select * from vw_reconciliation", null, [EnableFolding=true])
in
    [Enrollment=Enrollment, Terms=Terms, AcademicOrg=AcademicOrg, Students=Students, CourseSections=CourseSections, Plan=Plan, ResourcePressure=ResourcePressure, Quality=Quality]
