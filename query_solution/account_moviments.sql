/*
		This query consolidates all monthly moviemnts in one table
*/
WITH account_movimentations AS
(
SELECT 
		account_id
      , month(from_unixtime(transaction_completed_at)) as 'month'
      , year(from_unixtime(transaction_completed_at)) as 'year'
      , sum(ifnull(amount, 0)) as 'transfer_in' 
      , 0 as 'transfer_out'
FROM nu_snow_flake_4.transfer_ins
WHERE 
		account_id = 1411654469209523200
        and status = 'completed'
GROUP BY
		account_id
      , month(from_unixtime(transaction_completed_at))
      , year(from_unixtime(transaction_completed_at))

UNION ALL
/*
		All negative moviments from transfer_outs
*/
SELECT 
		account_id
      , month(from_unixtime(transaction_completed_at)) as 'month'
      , year(from_unixtime(transaction_completed_at)) as 'year'
      , 0 as 'transfer_in'
      , sum(ifnull(amount, 0)) * -1 as 'transfer_out'      
FROM nu_snow_flake_4.transfer_outs
WHERE 
		account_id = 1411654469209523200
        and status = 'completed'
GROUP BY
		account_id
      , month(from_unixtime(transaction_completed_at))
      , year(from_unixtime(transaction_completed_at))
UNION ALL
/*
	All transactions from pix moviments
    Positive and Negative
*/
SELECT 
			account_id
          , MONTH(from_unixtime(pix_completed_at)) as 'month'
          , YEAR(from_unixtime(pix_completed_at)) as 'year'
          , CASE WHEN in_or_out = 'pix_in' THEN ifnull(pix_amount, 0) ELSE 0 END as 'transfer_in'
		  , CASE WHEN in_or_out = 'pix_out' THEN ifnull(pix_amount, 0) * -1 ELSE 0 END as 'transfer_out'          
FROM 
		nu_snow_flake_4.pix_movements
WHERE
		account_id = 1411654469209523200
        and status = 'completed'
)
SELECT 
		account_id
	 ,  month
     , year
     , SUM(transfer_in) as 'transfer_in'
     , SUM(transfer_out) as 'transfer_out'
FROM account_movimentations
WHERE month = 3
GROUP BY
		account_id
	 ,  month
     , year
     