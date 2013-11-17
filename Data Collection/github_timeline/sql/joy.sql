SELECT repository_language, COUNT(*) as cntlang
FROM [githubarchive:github.timeline]
WHERE repository_language != ''
AND payload_commit_msg != ''
AND PARSE_UTC_USEC(created_at) < PARSE_UTC_USEC('2012-05-09 00:00:00')
AND REGEXP_MATCH(payload_commit_msg,
r'(?i)\b(yes|yay|hallelujah|hurray|bingo|amused|cheerful|excited|glad|proud)\b')
GROUP BY repository_language
ORDER BY cntlang DESC