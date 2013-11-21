/*
notepad++ regex for metacharactors escape in word list
*/
find: (\.|\^|\$|\*|\+|\?|\(|\)|\[|\{|\\)
replace with: \\\1

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
get word count of all words(\b([^ ]*)\b) from 10 languages. Table Saved as [repostitory_description_hottest_techs_list]
*/

SELECT word, count(word) as count, repository_language as language 
FROM(
	SELECT LOWER(REGEXP_EXTRACT(repository_description, r'(?i)\b(J2SE|J2EE|J2ME|JavaFX|JavaCard|Swing|JSP|JSF|Servlets|EJB|JPA|JMS|JNDI|JDBC|Spring|Struts|Hibernate|JMX|JavaMail|AccDC|Dojo|Glow|jQuery|midori|MooTools|Prototype|YUI|Ample SDK|DHTMLX|Ext JS|Ext\.js|iX Framework|jQuery UI|Lively Kernel|qooxdoo|Script\.aculo\.us|SmartClient|Webix|AlloyUI|D3|InfoVis|Kinetic\.js|Processing\.js|Raphael|SWFObject|Three\.js|EaselJS|Highcharts\.js|AngularJS|Backbone\.js|Chaplin\.js|Cappuccino|Echo|Ember\.js|Enyo|Google Web Toolkit|JavaScriptMVC|Kendo UI|Knockout|Rialto Toolkit|SproutCore|Web Atoms JS|FuncJS|Google Closure Library|Joose|jsPHP|MochiKit|PDF\.js|Rico|Socket\.IO|Spry framework|Underscore\.js|Wakanda|Handlebars|jQuery Mobile|Mustache|Bootstrap|ZURB Foundation|Cascade Framework|Jasmine|QUnit|Modernizr|Mocha|BaseX|Cloudant|Clusterpoint|Couchbase|CouchDB|djondb|ElasticSearch|eXist|Jackrabbit|Lotus|MarkLogic|MongoDB|Oracle NoSQL|CoreFoundation|Property list|Sedna|SimpleDB|TokuMX|Virtuoso|AllegroGraph|DB2|DEX|FlockDB|InfiniteGraph|Neo4j|OrientDB|GraphDB|Enterprise|OWLIM|VelocityGraph|ASP\.NET|BFC|CSLA|MonoRail|OpenRasta|Nancy|CppCMS|Poco|Tntnet|Wt|ColdBox|ColdFusion on Wheels|ColdSpring|Fusebox|FW|Mach-II|Model-Glue|onTap|Yesod|Happstack|Apache Click|Apache OFBiz|Apache Shale|Apache Sling|Apache Struts|Apache Tapestry|Apache Wicket|AppFuse|Eclipse RAP|FormEngine|Grails|Google Web Toolkit|Hamlets|ItsNat|JavaServer Faces|JBoss Seam|Jspx-bay|JVx|OpenLaszlo|OpenXava|Oracle ADF|Play!|RIFE|SmartGWT|Spring|Stripes|ThinWire|Vaadin|Wavemaker|WebObjects|WebWork|ZK|ztemplates|Meteor|SmartClient|node\.js|qooxdoo|SproutCore|Wakanda|WaveMaker|Play!|Lift|Scalatra|Circumflex|Catalyst|Dancer|Mason|Maypole|Mojolicious|Agavi|Aiki Framework|AppFlower|CakePHP|Cgiapp|CodeIgniter|Drupal|Fat-Free|FuelPHP|Hazaar MVC|Kajona|Laravel|Lithium|osBlast|PHPixie|PRADO|Qcodo|SilverStripe|Seagull|Solodev CMS|Symfony|TYPO3|Xyster|Yii|Zend|BlueBream|Bottle|CherryPy|CubicWeb|Django|web2py|Flask|Grok|Nagare|Pyjamas|Pylons|Pyramid|TACTIC|Tornado|TurboGears|Webware|Zope|Project|Camping|Rails|Ramaze|Sinatra|Merb|PureMVC|AIDA|Application Express|Compojure|Flex|Grails|Kepler|Morfik|Ocsigen|Opa|OpenACS|Seaside|Zotonic)\b')) AS word, repository_language
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
			AND REGEXP_MATCH(repository_description, r'(?i)\b(J2SE|J2EE|J2ME|JavaFX|JavaCard|Swing|JSP|JSF|Servlets|EJB|JPA|JMS|JNDI|JDBC|Spring|Struts|Hibernate|JMX|JavaMail|AccDC|Dojo|Glow|jQuery|midori|MooTools|Prototype|YUI|Ample SDK|DHTMLX|Ext JS|Ext\.js|iX Framework|jQuery UI|Lively Kernel|qooxdoo|Script\.aculo\.us|SmartClient|Webix|AlloyUI|D3|InfoVis|Kinetic\.js|Processing\.js|Raphael|SWFObject|Three\.js|EaselJS|Highcharts\.js|AngularJS|Backbone\.js|Chaplin\.js|Cappuccino|Echo|Ember\.js|Enyo|Google Web Toolkit|JavaScriptMVC|Kendo UI|Knockout|Rialto Toolkit|SproutCore|Web Atoms JS|FuncJS|Google Closure Library|Joose|jsPHP|MochiKit|PDF\.js|Rico|Socket\.IO|Spry framework|Underscore\.js|Wakanda|Handlebars|jQuery Mobile|Mustache|Bootstrap|ZURB Foundation|Cascade Framework|Jasmine|QUnit|Modernizr|Mocha|BaseX|Cloudant|Clusterpoint|Couchbase|CouchDB|djondb|ElasticSearch|eXist|Jackrabbit|Lotus|MarkLogic|MongoDB|Oracle NoSQL|CoreFoundation|Property list|Sedna|SimpleDB|TokuMX|Virtuoso|AllegroGraph|DB2|DEX|FlockDB|InfiniteGraph|Neo4j|OrientDB|GraphDB|Enterprise|OWLIM|VelocityGraph|ASP\.NET|BFC|CSLA|MonoRail|OpenRasta|Nancy|CppCMS|Poco|Tntnet|Wt|ColdBox|ColdFusion on Wheels|ColdSpring|Fusebox|FW|Mach-II|Model-Glue|onTap|Yesod|Happstack|Apache Click|Apache OFBiz|Apache Shale|Apache Sling|Apache Struts|Apache Tapestry|Apache Wicket|AppFuse|Eclipse RAP|FormEngine|Grails|Google Web Toolkit|Hamlets|ItsNat|JavaServer Faces|JBoss Seam|Jspx-bay|JVx|OpenLaszlo|OpenXava|Oracle ADF|Play!|RIFE|SmartGWT|Spring|Stripes|ThinWire|Vaadin|Wavemaker|WebObjects|WebWork|ZK|ztemplates|Meteor|SmartClient|node\.js|qooxdoo|SproutCore|Wakanda|WaveMaker|Play!|Lift|Scalatra|Circumflex|Catalyst|Dancer|Mason|Maypole|Mojolicious|Agavi|Aiki Framework|AppFlower|CakePHP|Cgiapp|CodeIgniter|Drupal|Fat-Free|FuelPHP|Hazaar MVC|Kajona|Laravel|Lithium|osBlast|PHPixie|PRADO|Qcodo|SilverStripe|Seagull|Solodev CMS|Symfony|TYPO3|Xyster|Yii|Zend|BlueBream|Bottle|CherryPy|CubicWeb|Django|web2py|Flask|Grok|Nagare|Pyjamas|Pylons|Pyramid|TACTIC|Tornado|TurboGears|Webware|Zope|Project|Camping|Rails|Ramaze|Sinatra|Merb|PureMVC|AIDA|Application Express|Compojure|Flex|Grails|Kepler|Morfik|Ocsigen|Opa|OpenACS|Seaside|Zotonic)\b')
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
query [repostitory_description_hottest_techs_list] with a group of word
*/
SELECT word, SUM(count) as total 
FROM [github_timeline.repostitory_description_words]
WHERE REGEXP_MATCH(word, r'(?i)^(
	J2SE|J2EE|J2ME
	)$')
GROUP BY word