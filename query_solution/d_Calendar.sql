/*
	This query create the dimension calendar for star schema model
*/
SELECT
					t.time_id					    	as 'ID'			
				  , t.action_timestamp					as 'TimeStamp Date'
                  , CAST(t.action_timestamp AS DATE) 	as 'Date'
                  , y.action_year						as 'Year'
                  , m.action_month						as 'Month'
                  , w.action_week						as 'Week Number'
                  , wd.action_weekday					as 'Week Day'
FROM
					d_time 	as 	 t
INNER JOIN 			d_year 	as 	 y on y.year_id = t.year_id
INNER JOIN 			d_month	as 	 m on m.month_id = t.month_id
INNER JOIN			d_week 	as 	 w on w.week_id = t.week_id
INNER JOIN			d_weekday as wd on 	wd.weekday_id = t.weekday_id