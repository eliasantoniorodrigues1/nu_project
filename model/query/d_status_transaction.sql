
WITH d_status_transactions as
(
SELECT 
		distinct 
        status
FROM transfer_ins
UNION ALL

SELECT 
		distinct
        status
FROM transfer_outs
UNION ALL
SELECT 
		distinct
        status
FROM pix_movements
)
SELECT
			CASE WHEN status = 'completed' then 1 else 0 end as status_id
		  , status
FROM
		d_status_transactions
GROUP BY
		  CASE WHEN status = 'completed' then 1 else 0 end
		, status
