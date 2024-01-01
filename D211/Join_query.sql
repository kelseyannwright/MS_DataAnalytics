SELECT * FROM customer
JOIN services
ON customer.customer_id = services.customer_id
JOIN location 
ON customer.location_id = location.location_id
JOIN broadband
ON location.county = broadband.county_name AND location.state = broadband.state