SELECT STRFTIME_UTC_USEC(TIMESTAMP(repository_pushed_at), "%Y-%m-%d") as days,
repository_language,
count(repository_language) as lang_count
FROM [githubarchive:github.timeline]
WHERE type="PushEvent" AND repository_language is not null
AND PARSE_UTC_USEC(created_at) < PARSE_UTC_USEC('2013-11-18 00:00:00')
GROUP BY days, repository_language
ORDER BY repository_language DESC;