SELECT EXTRACT(YEAR FROM start_date) AS year, COUNT(*) AS n
FROM trials
WHERE start_date IS NOT NULL
GROUP BY year
ORDER BY year;