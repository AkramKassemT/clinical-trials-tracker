SELECT has_results, COUNT(*) AS n
FROM trials
GROUP BY has_results
ORDER BY has_results DESC;
