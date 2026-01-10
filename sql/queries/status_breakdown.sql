SELECT overall_status, COUNT(*) AS n
FROM trials
GROUP BY overall_status
ORDER BY n DESC;