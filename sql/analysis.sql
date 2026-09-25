-- QUERY: Data quality audit
SELECT COUNT(*) AS records, MIN(date) AS first_date, MAX(date) AS last_date,
       SUM(is_positive_delay) AS positive_delay_records,
       SUM(CASE WHEN delay_min = 0 THEN 1 ELSE 0 END) AS zero_minute_records,
       COUNT(DISTINCT i.code) AS observed_codes,
       SUM(CASE WHEN c.code IS NULL THEN 1 ELSE 0 END) AS unmapped_code_records
FROM incidents i LEFT JOIN delay_codes c ON c.code = i.code;

-- QUERY: Line-level burden (not a per-rider rate)
WITH line_summary AS (
  SELECT line, COUNT(*) AS records, SUM(is_positive_delay) AS positive_events,
         SUM(delay_min) AS total_minutes, ROUND(AVG(CASE WHEN delay_min > 0 THEN delay_min END), 2) AS mean_positive_min
  FROM incidents GROUP BY line
)
SELECT line, records, positive_events, total_minutes, mean_positive_min,
       ROUND(100.0 * total_minutes / SUM(total_minutes) OVER (), 1) AS share_of_minutes_pct,
       RANK() OVER (ORDER BY total_minutes DESC) AS burden_rank
FROM line_summary ORDER BY burden_rank;

-- QUERY: Most impacted stations (minimum 100 positive events)
WITH station_summary AS (
 SELECT line, station, SUM(is_positive_delay) AS positive_events, SUM(delay_min) AS total_minutes
 FROM incidents GROUP BY line, station
)
SELECT line, station, positive_events, total_minutes,
       RANK() OVER (PARTITION BY line ORDER BY total_minutes DESC) AS rank_in_line
FROM station_summary WHERE positive_events >= 100 ORDER BY total_minutes DESC LIMIT 12;

-- QUERY: Top coded reasons among positive-delay records
SELECT i.code, COALESCE(c.description, '[not in reference table]') AS reason,
       COUNT(*) AS positive_events, SUM(i.delay_min) AS total_minutes,
       ROUND(AVG(i.delay_min),1) AS mean_minutes
FROM incidents i LEFT JOIN delay_codes c ON i.code=c.code
WHERE i.delay_min > 0 GROUP BY i.code, c.description ORDER BY total_minutes DESC LIMIT 12;

-- QUERY: Peak vs off-peak (record counts, not service-normalized risk)
SELECT CASE WHEN is_peak=1 THEN '07-09 and 16-18' ELSE 'other hours' END AS period,
       COUNT(*) AS records, SUM(is_positive_delay) AS positive_events,
       SUM(delay_min) AS total_minutes,
       ROUND(100.0*SUM(is_positive_delay)/COUNT(*),1) AS positive_share_pct
FROM incidents GROUP BY is_peak ORDER BY is_peak DESC;

-- QUERY: Monthly trends, same months year-over-year
WITH monthly AS (
 SELECT substr(date,1,4) AS year, substr(date,6,2) AS month,
        SUM(delay_min) AS minutes, SUM(is_positive_delay) AS positive_events
 FROM incidents GROUP BY 1,2
)
SELECT year, month, positive_events, minutes,
       LAG(minutes) OVER (PARTITION BY month ORDER BY year) AS prior_year_same_month_minutes,
       ROUND(100.0 * (minutes - LAG(minutes) OVER (PARTITION BY month ORDER BY year)) /
             NULLIF(LAG(minutes) OVER (PARTITION BY month ORDER BY year),0),1) AS yoy_change_pct
FROM monthly ORDER BY year,month;
