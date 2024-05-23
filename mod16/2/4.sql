SELECT customer.full_name,
        customer.order_no
FROM customer
JOIN order ON customer.customer_id = order.customer_id
WHERE order.manager_id IS NULL