select students_groups.group_id, count(distinct students.student_id), avg(assignments_grades.grade), sum(case when assignments_grades.grade is null then 1 else 0 end), sum(case when assignments.due_date < assignments_grades.date then 1 else 0 end), count(assignments_grades.student_id) - count(distinct assignments_grades.student_id)
from students_groups
left join students on students.group_id = students_groups.group_id
left join assignments on assignments.group_id = students_groups.group_id
left join assignments_grades on assignments_grades.assisgnment_id = assignments.assisgnment_id
group by students_groups.group_id


