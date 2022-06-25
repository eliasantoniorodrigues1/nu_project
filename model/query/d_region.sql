SELECT
				ci.city_id
			  , st.state
              , co.country
FROM
				city as ci
INNER JOIN		state as st on st.state_id = ci.state_id
INNER JOIN 		country as co on co.country_id = st.country_id