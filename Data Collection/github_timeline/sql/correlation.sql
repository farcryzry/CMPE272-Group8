select * from (
select actor, repository_language, count(repository_language) as pushes
  from [githubarchive:github.timeline]
  where
  REGEXP_MATCH(repository_language,r'(?i)\b(JavaScript|Ruby|Java|PHP|Python|C\+\+|C|CSS|Objective\-C|C\#|Shell|Perl|CoffeeScript|Go|Scala|VimL|Clojure|Haskell|Lua|Prolog)\b')
	and type='PushEvent'
  and PARSE_UTC_USEC(created_at) >= PARSE_UTC_USEC('2013-01-01 00:00:00')
  and PARSE_UTC_USEC(created_at) < PARSE_UTC_USEC('2013-11-19 00:00:00')
  and actor in (
  select actor from (
	  select * from (
	    select actor, COUNT(DISTINCT repository_language, 10000) as languages
	    from [githubarchive:github.timeline]
	    where REGEXP_MATCH(repository_language,r'(?i)\b(JavaScript|Ruby|Java|PHP|Python|C\+\+|C|CSS|Objective\-C|C\#|Shell|Perl|CoffeeScript|Go|Scala|VimL|Clojure|Haskell|Lua|Prolog)\b')
	    and type='PushEvent'
	    and PARSE_UTC_USEC(created_at) >= PARSE_UTC_USEC('2013-01-01 00:00:00')
	    and PARSE_UTC_USEC(created_at) < PARSE_UTC_USEC('2013-11-19 00:00:00')
	    group EACH by actor ) as t
	  where languages > 1))
  group by actor, repository_language)
  where pushes >=10