SELECT repository_language, count(repository_language) AS repos_by_lang
FROM [githubarchive:github.timeline]
WHERE repository_fork == "false"
AND type == "CreateEvent"
AND PARSE_UTC_USEC(repository_created_at) >= PARSE_UTC_USEC('2013-01-01 00:00:00')
AND PARSE_UTC_USEC(repository_created_at) < PARSE_UTC_USEC('2013-11-19 00:00:00')
GROUP BY repository_language
ORDER BY repos_by_lang DESC
LIMIT 20