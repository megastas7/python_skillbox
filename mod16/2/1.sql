SELECT customer.full_name,
        manager.full_name,
        manager.purchase_amount,
        'order'.date
FROM customer
JOIN manager ON customer.manager_id = manager.manager_id
JOIN order ON customer.customer_id = order.customer_id