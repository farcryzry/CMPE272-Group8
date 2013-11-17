SELECT
 ForkTable.repository_url,
 COUNT(DISTINCT ForkTable.url) AS f2p_number,
 AVG(PARSE_UTC_USEC(PullTable.created_at)-PARSE_UTC_USEC(ForkTable.created_at))/3600000000 AS f2p_interval_hour
FROM
 (SELECT
   url,
   repository_url,
   MIN(created_at) AS created_at
  FROM
   [githubarchive:github.timeline]
  WHERE type='ForkEvent'
  AND PARSE_UTC_USEC(created_at) >= PARSE_UTC_USEC('2012-04-01 00:00:00')
  AND PARSE_UTC_USEC(created_at) < PARSE_UTC_USEC('2012-05-01 00:00:00')
  GROUP BY
   repository_url,
   url)
 AS ForkTable
 INNER JOIN
 (SELECT
   repository_url,
   payload_pull_request_head_repo_html_url,
   MIN(created_at) AS created_at
  FROM
   [githubarchive:github.timeline]
  WHERE type='PullRequestEvent'
  AND PARSE_UTC_USEC(created_at) >= PARSE_UTC_USEC('2012-04-01 00:00:00')
  AND PARSE_UTC_USEC(created_at) < PARSE_UTC_USEC('2012-05-01 00:00:00')
  GROUP BY
   repository_url,
   payload_pull_request_head_repo_html_url)
 AS PullTable
 ON
  ForkTable.repository_url=PullTable.repository_url AND
  ForkTable.url=PullTable.payload_pull_request_head_repo_html_url
GROUP BY
 ForkTable.repository_url
ORDER BY
 f2p_number DESC