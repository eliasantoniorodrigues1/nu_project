/*
	All transactions from pix moviments
    Positive and Negative
*/
SELECT 
			account_id
          , MONTH(from_unixtime(pix_completed_at)) as 'Month'
          , YEAR(from_unixtime(pix_completed_at)) as 'Year'
          , in_or_out as 'Type Moviment'
		  , CASE WHEN in_or_out = 'pix_in' THEN pix_amount ELSE pix_amount * -1 END as amount          
FROM 
		nu_snow_flake_4.pix_movements
WHERE
		account_id = 623509224135263
        and status = 'completed'
        