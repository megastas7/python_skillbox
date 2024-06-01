select avg(assignment), max(assignment), min(assignment)
from (
select sum(assignments_grades.date > assignments.due_date) as assignment
from assignments
join assignments_grades on assignments_grades.assisgnment_id = assignments.assisgnment_id
group by assignments.group_id
)

