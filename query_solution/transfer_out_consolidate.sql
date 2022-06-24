SELECT 
		account_id
      , month(from_unixtime(transaction_completed_at)) as 'Month'
      , year(from_unixtime(transaction_completed_at)) as 'Year'
	  , sum(amount) as 'Total Transfer Out'
FROM nu_snow_flake_4.transfer_outs
WHERE 
		account_id = 623509224135263
        and status = 'completed'
GROUP BY
		account_id
      , month(from_unixtime(transaction_completed_at))
      , year(from_unixtime(transaction_completed_at))