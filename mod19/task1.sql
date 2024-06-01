select avg(assignments_grades.grade), teachers.full_name
from assignments_grades
join assignments on assignments.assisgnment_id = assignments_grades.assisgnment_id
join teachers on teachers.teacher_id = assignments.teacher_id
group by teachers.teacher_id
order by avg(assignments_grades.grade)
limit 1
