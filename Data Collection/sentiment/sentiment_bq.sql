/*
get word count of joyful exclamation from 10 languages
*/
SELECT word, count(word) as count, repository_language as language 
FROM(
	SELECT LOWER(REGEXP_EXTRACT(payload_commit_msg, r'(?i)\b(ass|asshole|bastard|bitch|bloody|cunt|damn|fuck|hell|Jesus|shit|suck|mad|crazy|jerk|crap|piss|fag|bastard|screw|cranky|annoying|bitter|kill|dye|messy|oops|shoot|evil|wicked)\b')) AS word, repository_language
	FROM(
		SELECT payload_commit_msg, repository_language 
		FROM [githubarchive:github.timeline] 
		WHERE 
			repository_language != ''
			AND(	
						repository_language == "JavaScript" 
						OR repository_language == "Java" 
						OR repository_language == "Ruby" 
						OR repository_language == "Python" 
						OR repository_language == "PHP" 
						OR repository_language == "C" 
						OR repository_language == "C++" 
						OR repository_language == "Shell" 
						OR repository_language == "C#" 
						OR repository_language == "Objective-C"
					) 
			AND payload_commit_msg != '' 
			AND PARSE_UTC_USEC(created_at) < PARSE_UTC_USEC('2013-11-18 00:00:00')
			AND REGEXP_MATCH(payload_commit_msg, r'(?i)\b(ass|asshole|bastard|bitch|bloody|cunt|damn|fuck|hell|Jesus|shit|suck|mad|crazy|jerk|crap|piss|fag|bastard|screw|cranky|annoying|bitter|kill|dye|messy|oops|shoot|evil|wicked)\b')
	)
)
GROUP BY word, language 

/*
get word count of swear words from 10 languages
*/

SELECT word, count(word) as count, repository_language as language 
FROM(
	SELECT LOWER(REGEXP_EXTRACT(payload_commit_msg, r'(?i)\b(blessed|beautiful|delightful|enjoyable|excellent|exciting|fabulous|great|lovely|peaceful|perfect|amazing|sweet|bingo|hilarious|hallelujah|amused|yeah|yo|hah|cheers|eureka|hurray|wow|yippee|yay)\b')) AS word, repository_language
	FROM(
		SELECT payload_commit_msg, repository_language 
		FROM [githubarchive:github.timeline] 
		WHERE 
			repository_language != ''
			AND(	
						repository_language == "JavaScript" 
						OR repository_language == "Java" 
						OR repository_language == "Ruby" 
						OR repository_language == "Python" 
						OR repository_language == "PHP" 
						OR repository_language == "C" 
						OR repository_language == "C++" 
						OR repository_language == "Shell" 
						OR repository_language == "C#" 
						OR repository_language == "Objective-C"
					) 
			AND payload_commit_msg != '' 
			AND PARSE_UTC_USEC(created_at) < PARSE_UTC_USEC('2013-11-18 00:00:00')
			AND REGEXP_MATCH(payload_commit_msg, r'(?i)\b(blessed|beautiful|delightful|enjoyable|excellent|exciting|fabulous|great|lovely|peaceful|perfect|amazing|sweet|bingo|hilarious|hallelujah|amused|yeah|yo|hah|cheers|eureka|hurray|wow|yippee|yay)\b')
	)
)
GROUP BY word, language 

/*
get word count of all words(\b([^ ]*)\b) from 10 languages. Table Saved as [github_timeline.commit_msg_all]
*/

SELECT word, count(word) as count, repository_language as language 
FROM(
	SELECT LOWER(REGEXP_EXTRACT(payload_commit_msg, r'(?i)\b([^ ]*)\b')) AS word, repository_language
	FROM(
		SELECT payload_commit_msg, repository_language 
		FROM [githubarchive:github.timeline] 
		WHERE 
			repository_language != ''
			AND(	
						repository_language == "JavaScript" 
						OR repository_language == "Java" 
						OR repository_language == "Ruby" 
						OR repository_language == "Python" 
						OR repository_language == "PHP" 
						OR repository_language == "C" 
						OR repository_language == "C++" 
						OR repository_language == "Shell" 
						OR repository_language == "C#" 
						OR repository_language == "Objective-C"
					) 
			AND payload_commit_msg != '' 
			AND PARSE_UTC_USEC(created_at) < PARSE_UTC_USEC('2013-11-18 00:00:00')
			AND REGEXP_MATCH(payload_commit_msg, r'(?i)\b([^ ]*)\b')
	)
)
GROUP BY word, language 

/*
get word count of all words(\b([^ ]*)\b) from 10 languages. Table Saved as [github_timeline.commit_msg_all]
*/

SELECT word, count(word) as count, repository_language as language 
FROM(
	SELECT LOWER(REGEXP_EXTRACT(repository_description, r'(?i)\b([^ ]*)\b')) AS word, repository_language
	FROM(
		SELECT repository_description, repository_language 
		FROM [githubarchive:github.timeline] 
		WHERE 
			repository_language != ''
			AND(	
						repository_language == "JavaScript" 
						OR repository_language == "Java" 
						OR repository_language == "Ruby" 
						OR repository_language == "Python" 
						OR repository_language == "PHP" 
						OR repository_language == "C" 
						OR repository_language == "C++" 
						OR repository_language == "Shell" 
						OR repository_language == "C#" 
						OR repository_language == "Objective-C"
					) 
			AND repository_description != '' 
			AND PARSE_UTC_USEC(created_at) < PARSE_UTC_USEC('2013-11-18 00:00:00')
			AND REGEXP_MATCH(repository_description, r'(?i)\b([^ ]*)\b')
	)
)
GROUP BY word, language 


/* 
query [github_timeline.commit_msg_all] with a group of word
*/
SELECT * 
FROM [github_timeline.commit_msg_all]
WHERE 
	count>10
	AND REGEXP_MATCH(word, r'(?i)^(
		hello|world|foo|
	)$')
	
/* 
query [github_timeline.repostitory_description_words] with a group of word
*/
SELECT * 
FROM [github_timeline.repostitory_description_words]
WHERE REGEXP_MATCH(word, r'(?i)^(
	django|vaadin
	)$')