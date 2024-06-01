select avg(assignments_grades.grade), students.full_name
from assignments_grades
join students on students.student_id = assignments_grades.student_id
group by students.student_id
order by avg(assignments_grades.grade) desc
limit 10

