SELECT repository_language, actor_attributes_location, COUNT(actor_attributes_location) AS loccnt FROM [githubarchive:github.timeline]
WHERE type="PushEvent"
AND (
repository_language == "JavaScript" OR
repository_language == "Java" OR
repository_language == "Ruby" OR
repository_language == "Python" OR
repository_language == "PHP" OR
repository_language == "C" OR
repository_language == "C++" OR
repository_language == "Shell" OR
repository_language == "C#" OR
repository_language == "Objective-C"
)
AND REGEXP_MATCH(actor_attributes_location,r'^[\s\w]+,[\s]*[\s\w]+$')
GROUP BY repository_language, actor_attributes_location
ORDER BY loccnt DESC
#LIMIT 100;
