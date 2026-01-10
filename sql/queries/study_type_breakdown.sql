SELECT study_type, COUNT(*) AS n
FROM trials
GROUP BY study_type
ORDER BY n DESC;
