SELECT order.order_no,
        manager.full_name,
        customer.full_name
FROM customer
JOIN order ON customer.customer_id = order.customer_id
JOIN manager ON manager.manager_id = customer.manager_id
WHERE customer.city != manager.city