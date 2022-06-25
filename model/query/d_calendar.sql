/*
	This query create the dimension calendar for star schema model
*/
SELECT
					t.time_id					    	as 'date_id'			
				  , t.action_timestamp					as 'timestamp_date'
                  , CAST(t.action_timestamp AS DATE) 	as 'date'
                  , y.action_year						as 'year'
                  , m.action_month						as 'month'
                  , w.action_week						as 'week_number'
                  , wd.action_weekday					as 'week_day'
FROM
					d_time 	as 	 t
INNER JOIN 			d_year 	as 	 y on y.year_id = t.year_id
INNER JOIN 			d_month	as 	 m on m.month_id = t.month_id
INNER JOIN			d_week 	as 	 w on w.week_id = t.week_id
INNER JOIN			d_weekday as wd on 	wd.weekday_id = t.weekday_id