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
FROM 			transfer_ins

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
FROM 	
		transfer_outs

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
FROM 
		investments
)
SELECT 
			 ac_m.transaction_id
		   , ac_m.account_id
           , ac.customer_id
           , cu.customer_city as customer_city_id
		   , ac_m.date_id
		   , ac_m.status_id
		   , ac_m.type_moviment_id
		   , ac_m.amount
FROM 		account_movimentations as ac_m
LEFT JOIN 	accounts as ac on ac.account_id = ac_m.account_id 
LEFT JOIN 	customers as cu on cu.customer_id = ac.customer_id
LEFT JOIN	city as ci on ci.city_id = cu.customer_city
LEFT JOIN   state as st on st.state_id = ci.state_id



     