# Advanced Decision-Support Analytics

## Resource-pressure scenario model

The model turns governed term/department scenarios into a ranked planning queue for course sections, faculty instructional effort, and rooms. Source inputs are in `data/raw/resource_scenarios.csv`; cleaned inputs load to `fact_resource_scenario`. Reproducible calculations are exposed by `vw_resource_pressure` and persisted to `fact_resource_pressure` on each pipeline run.

## Grain and measures

- Input grain: **term × academic organization × named scenario**.
- Output grain: the same input grain, ranked within **term × scenario**; rank 1 is greatest composite pressure.
- Demand applies the scenario growth rate to current active enrollment and active student credit hours (SCH).
- Required sections are `ceil(projected enrollment / seats per room)`.
- Course-section pressure is required sections divided by planned sections.
- Faculty pressure is projected SCH divided by `faculty FTE × SCH capacity per FTE`.
- Room pressure is required sections divided by `room count × available slots per room`.
- Composite pressure is `40% course-section + 35% faculty + 25% room`. A score above 1.00 means the weighted capacity requirement exceeds the available plan.

## Assumptions and limitations

1. Current active enrollment and SCH are a suitable baseline for the selected planning term; seasonality, new-program launch effects, and long-run trends are not modeled.
2. Growth applies uniformly within an organization. It is a scenario input, not a statistical forecast.
3. One required section is modeled from projected headcount and a representative room-seat count. Course-level prerequisites, cross-listing, waitlists, modality constraints, and meeting patterns are not yet modeled.
4. Faculty capacity is expressed in planning SCH/FTE and does not represent contractual workload, individual qualifications, or availability.
5. Room slots are fungible within an organization; time conflicts, specialized rooms, accessibility requirements, and campus travel are excluded.
6. Rankings prioritize relative pressure; they do not authorize hiring, room assignment, or section cancellation. Planning teams must validate flagged items.

## Governance

Registrar owns section and room-planning inputs; the Provost Office owns faculty-capacity assumptions; IRE owns calculation definitions and release validation. Scenario changes require a named version, owner approval, and pipeline rerun. The output is aggregate planning data and remains subject to the access and suppression controls in the project charter.
