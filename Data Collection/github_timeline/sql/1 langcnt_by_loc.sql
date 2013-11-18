SELECT actor_attributes_location as loc, COUNT(repository_language) AS langcnt, repository_language FROM [githubarchive:github.timeline]
WHERE type="PushEvent"
AND repository_language != ""
AND actor_attributes_location != ""
GROUP BY repository_language, loc
ORDER BY langcnt DESC