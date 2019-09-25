USERS_TABLE = 'users'
TESTS_TABLE = 'tests'
USERS_TESTS_TABLE = 'users_tests'
QUESTIONS_TABLE = 'questions'
QUESTIONS_TESTS_TABLE = 'questions_tests'
RESULTS_TABLE = 'results'

USERS_TABLE_DEFINITIONS = f'''
  CREATE TABLE IF NOT EXISTS {USERS_TABLE} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ci INTEGER UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'user'
  )
'''

TESTS_TABLE_DEFINITIONS = f'''
  CREATE TABLE IF NOT EXISTS {TESTS_TABLE} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mac_addresses TEXT NOT NULL,
    location_code TEXT NOT NULL,
    inscription_start TEXT NOT NULL,
    inscription_end TEXT NOT NULL,
    test_start TEXT NOT NULL,
    test_end TEXT NOT NULL
  )
'''

USERS_TESTS_TABLE_DEFINITIONS = f'''
  CREATE TABLE IF NOT EXISTS {USERS_TESTS_TABLE} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    test_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(test_id) REFERENCES tests(id)
  )
'''

QUESTIONS_TABLE_DEFINITIONS = f'''
  CREATE TABLE IF NOT EXISTS {QUESTIONS_TABLE} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    options TEXT NOT NULL,
    answ_index INTEGER NOT NULL,
    score REAL NOT NULL,
    knowledge_area TEXT NOT NULL,
    test_type TEXT NOT NULL
  )
'''

QUESTIONS_TESTS_TABLE_DEFINITIONS = f'''
  CREATE TABLE IF NOT EXISTS {QUESTIONS_TESTS_TABLE} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    test_id INTEGER NOT NULL,
    FOREIGN KEY(question_id) REFERENCES questions(id),
    FOREIGN KEY(test_id) REFERENCES tests(id)
  )
'''

RESULTS_TABLE_DEFINITIONS = f'''
  CREATE TABLE IF NOT EXISTS {RESULTS_TABLE} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    questions TEXT NOT NULL,
    answers TEXT NOT NULL,
    score_per_question TEXT NOT NULL,
    score REAL NOT NULL,
    user_id INTEGER NOT NULL,
    test_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(test_id) REFERENCES tests(id)
  )
'''

