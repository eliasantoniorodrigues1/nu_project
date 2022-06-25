/*
	This query create the d_customers dimension
*/
SELECT
		cu.customer_id
	  , cu.cpf
	  , concat(cu.first_name, ' ' ,cu.last_name) as customer
      , ac.account_number
	  , ac.account_branch
      , ac.account_check_digit      
      , ac.created_at
      , ac.status
      
FROM
				customers as cu
LEFT JOIN 		city ci on ci.city_id = cu.customer_city
LEFT JOIN		state st on st.state_id = ci.state_id
LEFT JOIN		accounts ac on ac.customer_id = cu.customer_id

ORDER BY
		cu.customer_id