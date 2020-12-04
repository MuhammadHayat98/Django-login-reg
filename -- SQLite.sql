-- SQLite
SELECT user_id FROM accounts_profile_following WHERE (profile_id=3) UNION SELECT user_id FROM accounts_profile_following WHERE (profile_id=1);