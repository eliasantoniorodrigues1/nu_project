/*
		This query consolidates all transactions to build a fact table
*/
WITH account_movimentations AS
(
/*
	All positive moviments from transfer_ins
*/
SELECT 
		id as transaction_id
	  , account_id
      , transaction_completed_at as date_id
      , case when status = 'completed' then 1 else 0 end as status_id
      , amount
      , 1 as type_moviment_id
      , 'transfer_in' as type_moviment
FROM 	transfer_ins

UNION ALL
/*
		All negative moviments from transfer_outs
*/
SELECT 
		id as transaction_id
	  , account_id
      , transaction_completed_at as date_id
      , case when status = 'completed' then 1 else 0 end as status_id
      , amount
      , 2 as type_moviment_id
      , 'transfer_out' as type_moviment      
FROM 	transfer_outs

UNION ALL
/*
	All transactions from pix moviments
    Positive and Negative
*/
SELECT 
		    id as transaction_id
          , account_id
          , pix_completed_at as date_id
		  , case when status = 'completed' then 1 else 0 end as status_id
          , pix_amount as amount
          , case 
				when in_or_out = 'pix_in' then 3
                when in_or_out = 'pix_out' then 4 end as type_moviment_id
          , in_or_out as 'type_moviment'         
FROM 
			pix_movements
UNION ALL
/*
	All moviments from investments
*/
SELECT 
		transaction_id
      ,	account_id
	  , investment_completed_at as date_id
      , case when status = 'completed' then 1 else 0 end as status_id
      , amount
	  , case 
			when type = 'investment_transfer_in' then 5
			when type = 'investment_transfer_out' then 6 end as type_moviment_id
      , type as type_moviment
FROM 	investments
)
SELECT 
		distinct
		type_moviment_id
        , type_moviment
FROM 
		account_movimentations


     