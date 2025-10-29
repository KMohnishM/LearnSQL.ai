-- Comprehensive SQL Cheat Sheet Data
-- Based on SQL standards (ANSI SQL) with common database variations

DELETE FROM cheat_sheet_entries WHERE 1=1;

-- ==== DATA DEFINITION LANGUAGE (DDL) ====
INSERT INTO cheat_sheet_entries (topic, category, syntax, example, description) VALUES
('CREATE DATABASE', 'DDL', 'CREATE DATABASE database_name;', 'CREATE DATABASE company_db;', 'Creates a new database'),
('CREATE TABLE', 'DDL', 'CREATE TABLE table_name (column1 datatype constraints, column2 datatype constraints);', 'CREATE TABLE employees (id INT PRIMARY KEY, name VARCHAR(100) NOT NULL, salary DECIMAL(10,2), hire_date DATE);', 'Creates a new table with specified columns and data types'),
('ALTER TABLE - ADD COLUMN', 'DDL', 'ALTER TABLE table_name ADD COLUMN column_name datatype;', 'ALTER TABLE employees ADD COLUMN department VARCHAR(50);', 'Adds a new column to an existing table'),
('ALTER TABLE - DROP COLUMN', 'DDL', 'ALTER TABLE table_name DROP COLUMN column_name;', 'ALTER TABLE employees DROP COLUMN department;', 'Removes a column from an existing table'),
('ALTER TABLE - MODIFY COLUMN', 'DDL', 'ALTER TABLE table_name ALTER COLUMN column_name datatype;', 'ALTER TABLE employees ALTER COLUMN salary DECIMAL(12,2);', 'Modifies the data type of an existing column'),
('DROP TABLE', 'DDL', 'DROP TABLE table_name;', 'DROP TABLE employees;', 'Deletes an entire table and all its data'),
('CREATE INDEX', 'DDL', 'CREATE INDEX index_name ON table_name (column_name);', 'CREATE INDEX idx_employee_dept ON employees (department);', 'Creates an index to improve query performance'),
('DROP INDEX', 'DDL', 'DROP INDEX index_name;', 'DROP INDEX idx_employee_dept;', 'Removes an index from a table'),
('TRUNCATE TABLE', 'DDL', 'TRUNCATE TABLE table_name;', 'TRUNCATE TABLE employees;', 'Removes all rows from a table but keeps the structure');

-- ==== DATA MANIPULATION LANGUAGE (DML) ====
INSERT INTO cheat_sheet_entries (topic, category, syntax, example, description) VALUES
('SELECT - Basic', 'DML', 'SELECT column1, column2 FROM table_name;', 'SELECT name, salary FROM employees;', 'Retrieves specific columns from a table'),
('SELECT - All Columns', 'DML', 'SELECT * FROM table_name;', 'SELECT * FROM employees;', 'Retrieves all columns from a table'),
('SELECT - DISTINCT', 'DML', 'SELECT DISTINCT column_name FROM table_name;', 'SELECT DISTINCT department FROM employees;', 'Retrieves unique values from a column'),
('WHERE Clause', 'DML', 'SELECT * FROM table_name WHERE condition;', 'SELECT * FROM employees WHERE salary > 50000;', 'Filters rows based on specified conditions'),
('INSERT - Single Row', 'DML', 'INSERT INTO table_name (column1, column2) VALUES (value1, value2);', 'INSERT INTO employees (name, salary, hire_date) VALUES (''John Doe'', 75000, ''2023-01-15'');', 'Adds a new row to a table'),
('INSERT - Multiple Rows', 'DML', 'INSERT INTO table_name (column1, column2) VALUES (value1, value2), (value3, value4);', 'INSERT INTO employees (name, salary) VALUES (''Alice Smith'', 80000), (''Bob Johnson'', 65000);', 'Adds multiple rows to a table in one statement'),
('UPDATE', 'DML', 'UPDATE table_name SET column1 = value1 WHERE condition;', 'UPDATE employees SET salary = 85000 WHERE name = ''John Doe'';', 'Modifies existing data in a table'),
('DELETE', 'DML', 'DELETE FROM table_name WHERE condition;', 'DELETE FROM employees WHERE hire_date < ''2020-01-01'';', 'Removes rows from a table based on a condition');

-- ==== CONSTRAINTS ====
INSERT INTO cheat_sheet_entries (topic, category, syntax, example, description) VALUES
('PRIMARY KEY', 'Constraints', 'column_name datatype PRIMARY KEY', 'CREATE TABLE users (id INT PRIMARY KEY, username VARCHAR(50));', 'Uniquely identifies each record in a table'),
('FOREIGN KEY', 'Constraints', 'FOREIGN KEY (column_name) REFERENCES other_table(column_name)', 'CREATE TABLE orders (id INT PRIMARY KEY, user_id INT, FOREIGN KEY (user_id) REFERENCES users(id));', 'Links two tables together and maintains referential integrity'),
('UNIQUE', 'Constraints', 'column_name datatype UNIQUE', 'CREATE TABLE users (id INT PRIMARY KEY, email VARCHAR(100) UNIQUE);', 'Ensures all values in a column are different'),
('NOT NULL', 'Constraints', 'column_name datatype NOT NULL', 'CREATE TABLE products (id INT PRIMARY KEY, name VARCHAR(100) NOT NULL);', 'Ensures a column cannot have empty values'),
('CHECK', 'Constraints', 'CHECK (condition)', 'CREATE TABLE employees (id INT PRIMARY KEY, age INT CHECK (age >= 18));', 'Ensures values in a column meet a specific condition'),
('DEFAULT', 'Constraints', 'column_name datatype DEFAULT value', 'CREATE TABLE orders (id INT PRIMARY KEY, status VARCHAR(20) DEFAULT ''pending'');', 'Sets a default value for a column when no value is specified');

-- ==== SINGLE ROW FUNCTIONS ====
INSERT INTO cheat_sheet_entries (topic, category, syntax, example, description) VALUES
('UPPER', 'String Functions', 'UPPER(string)', 'SELECT UPPER(name) FROM employees;', 'Converts string to uppercase'),
('LOWER', 'String Functions', 'LOWER(string)', 'SELECT LOWER(email) FROM users;', 'Converts string to lowercase'),
('LENGTH/LEN', 'String Functions', 'LENGTH(string) or LEN(string)', 'SELECT LENGTH(name) FROM employees;', 'Returns the number of characters in a string'),
('SUBSTRING', 'String Functions', 'SUBSTRING(string, start_position, length)', 'SELECT SUBSTRING(name, 1, 5) FROM employees;', 'Extracts a portion of a string'),
('CONCAT', 'String Functions', 'CONCAT(string1, string2, ...)', 'SELECT CONCAT(first_name, '' '', last_name) AS full_name FROM employees;', 'Combines multiple strings into one'),
('TRIM', 'String Functions', 'TRIM(string)', 'SELECT TRIM(name) FROM employees;', 'Removes leading and trailing spaces'),
('REPLACE', 'String Functions', 'REPLACE(string, old_substring, new_substring)', 'SELECT REPLACE(phone_number, ''-'', '''') FROM contacts;', 'Replaces all occurrences of a substring'),
('ROUND', 'Numeric Functions', 'ROUND(number, decimal_places)', 'SELECT ROUND(salary, 2) FROM employees;', 'Rounds a number to specified decimal places'),
('ABS', 'Numeric Functions', 'ABS(number)', 'SELECT ABS(balance) FROM accounts;', 'Returns the absolute value of a number'),
('CEILING/CEIL', 'Numeric Functions', 'CEILING(number) or CEIL(number)', 'SELECT CEILING(price) FROM products;', 'Returns the smallest integer greater than or equal to the number'),
('FLOOR', 'Numeric Functions', 'FLOOR(number)', 'SELECT FLOOR(rating) FROM reviews;', 'Returns the largest integer less than or equal to the number'),
('NOW/GETDATE', 'Date Functions', 'NOW() or GETDATE()', 'SELECT NOW() AS current_timestamp;', 'Returns the current date and time'),
('DATEADD', 'Date Functions', 'DATEADD(interval, number, date)', 'SELECT DATEADD(DAY, 30, hire_date) FROM employees;', 'Adds a specified time interval to a date'),
('DATEDIFF', 'Date Functions', 'DATEDIFF(interval, date1, date2)', 'SELECT DATEDIFF(DAY, hire_date, NOW()) FROM employees;', 'Returns the difference between two dates'),
('YEAR', 'Date Functions', 'YEAR(date)', 'SELECT YEAR(hire_date) FROM employees;', 'Extracts the year from a date'),
('MONTH', 'Date Functions', 'MONTH(date)', 'SELECT MONTH(order_date) FROM orders;', 'Extracts the month from a date'),
('DAY', 'Date Functions', 'DAY(date)', 'SELECT DAY(birth_date) FROM employees;', 'Extracts the day from a date');

-- ==== OPERATORS AND GROUP FUNCTIONS ====
INSERT INTO cheat_sheet_entries (topic, category, syntax, example, description) VALUES
('AND Operator', 'Logical Operators', 'WHERE condition1 AND condition2', 'SELECT * FROM employees WHERE salary > 50000 AND department = ''IT'';', 'Returns records where both conditions are true'),
('OR Operator', 'Logical Operators', 'WHERE condition1 OR condition2', 'SELECT * FROM employees WHERE department = ''HR'' OR department = ''Finance'';', 'Returns records where at least one condition is true'),
('NOT Operator', 'Logical Operators', 'WHERE NOT condition', 'SELECT * FROM employees WHERE NOT department = ''IT'';', 'Returns records where the condition is false'),
('IN Operator', 'Logical Operators', 'WHERE column_name IN (value1, value2, ...)', 'SELECT * FROM employees WHERE department IN (''HR'', ''IT'', ''Finance'');', 'Returns records where column value matches any value in the list'),
('BETWEEN Operator', 'Logical Operators', 'WHERE column_name BETWEEN value1 AND value2', 'SELECT * FROM employees WHERE salary BETWEEN 40000 AND 80000;', 'Returns records where column value is within a range'),
('LIKE Operator', 'Logical Operators', 'WHERE column_name LIKE pattern', 'SELECT * FROM employees WHERE name LIKE ''John%'';', 'Returns records where column value matches a pattern (% = wildcard)'),
('IS NULL', 'Logical Operators', 'WHERE column_name IS NULL', 'SELECT * FROM employees WHERE phone_number IS NULL;', 'Returns records where column value is null'),
('IS NOT NULL', 'Logical Operators', 'WHERE column_name IS NOT NULL', 'SELECT * FROM employees WHERE email IS NOT NULL;', 'Returns records where column value is not null'),
('COUNT', 'Aggregate Functions', 'COUNT(column_name) or COUNT(*)', 'SELECT COUNT(*) FROM employees;', 'Returns the number of rows'),
('SUM', 'Aggregate Functions', 'SUM(column_name)', 'SELECT SUM(salary) FROM employees;', 'Returns the sum of all values in a numeric column'),
('AVG', 'Aggregate Functions', 'AVG(column_name)', 'SELECT AVG(salary) FROM employees;', 'Returns the average value of a numeric column'),
('MIN', 'Aggregate Functions', 'MIN(column_name)', 'SELECT MIN(salary) FROM employees;', 'Returns the smallest value in a column'),
('MAX', 'Aggregate Functions', 'MAX(column_name)', 'SELECT MAX(hire_date) FROM employees;', 'Returns the largest value in a column'),
('GROUP BY', 'Group Functions', 'SELECT column, COUNT(*) FROM table GROUP BY column', 'SELECT department, COUNT(*) FROM employees GROUP BY department;', 'Groups rows with the same values and performs aggregate functions'),
('HAVING', 'Group Functions', 'SELECT column, COUNT(*) FROM table GROUP BY column HAVING condition', 'SELECT department, AVG(salary) FROM employees GROUP BY department HAVING AVG(salary) > 60000;', 'Filters groups based on aggregate function results'),
('ORDER BY - ASC', 'Sorting', 'SELECT * FROM table ORDER BY column ASC', 'SELECT * FROM employees ORDER BY salary ASC;', 'Sorts results in ascending order'),
('ORDER BY - DESC', 'Sorting', 'SELECT * FROM table ORDER BY column DESC', 'SELECT * FROM employees ORDER BY hire_date DESC;', 'Sorts results in descending order'),
('LIMIT/TOP', 'Limiting Results', 'SELECT * FROM table LIMIT number', 'SELECT * FROM employees ORDER BY salary DESC LIMIT 10;', 'Limits the number of rows returned');

-- ==== JOINS ====
INSERT INTO cheat_sheet_entries (topic, category, syntax, example, description) VALUES
('INNER JOIN', 'Joins', 'SELECT * FROM table1 INNER JOIN table2 ON table1.column = table2.column', 'SELECT e.name, d.department_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;', 'Returns records that have matching values in both tables'),
('LEFT JOIN', 'Joins', 'SELECT * FROM table1 LEFT JOIN table2 ON table1.column = table2.column', 'SELECT e.name, d.department_name FROM employees e LEFT JOIN departments d ON e.dept_id = d.id;', 'Returns all records from left table and matched records from right table'),
('RIGHT JOIN', 'Joins', 'SELECT * FROM table1 RIGHT JOIN table2 ON table1.column = table2.column', 'SELECT e.name, d.department_name FROM employees e RIGHT JOIN departments d ON e.dept_id = d.id;', 'Returns all records from right table and matched records from left table'),
('FULL OUTER JOIN', 'Joins', 'SELECT * FROM table1 FULL OUTER JOIN table2 ON table1.column = table2.column', 'SELECT e.name, d.department_name FROM employees e FULL OUTER JOIN departments d ON e.dept_id = d.id;', 'Returns all records when there is a match in either left or right table'),
('CROSS JOIN', 'Joins', 'SELECT * FROM table1 CROSS JOIN table2', 'SELECT p.name, c.color FROM products p CROSS JOIN colors c;', 'Returns the Cartesian product of both tables'),
('SELF JOIN', 'Joins', 'SELECT * FROM table1 t1 INNER JOIN table1 t2 ON condition', 'SELECT e1.name AS employee, e2.name AS manager FROM employees e1 INNER JOIN employees e2 ON e1.manager_id = e2.id;', 'Joins a table with itself to compare rows within the same table');

-- ==== SUBQUERIES AND VIEWS ====
INSERT INTO cheat_sheet_entries (topic, category, syntax, example, description) VALUES
('Subquery in WHERE', 'Subqueries', 'SELECT * FROM table WHERE column = (SELECT column FROM table WHERE condition)', 'SELECT * FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);', 'Uses a subquery result as a condition in WHERE clause'),
('Subquery in FROM', 'Subqueries', 'SELECT * FROM (SELECT columns FROM table WHERE condition) AS alias', 'SELECT * FROM (SELECT name, salary FROM employees WHERE dept_id = 1) AS it_employees;', 'Uses a subquery as a table in FROM clause'),
('EXISTS', 'Subqueries', 'SELECT * FROM table1 WHERE EXISTS (SELECT 1 FROM table2 WHERE condition)', 'SELECT * FROM departments WHERE EXISTS (SELECT 1 FROM employees WHERE employees.dept_id = departments.id);', 'Returns records where the subquery returns at least one row'),
('NOT EXISTS', 'Subqueries', 'SELECT * FROM table1 WHERE NOT EXISTS (SELECT 1 FROM table2 WHERE condition)', 'SELECT * FROM departments WHERE NOT EXISTS (SELECT 1 FROM employees WHERE employees.dept_id = departments.id);', 'Returns records where the subquery returns no rows'),
('IN with Subquery', 'Subqueries', 'SELECT * FROM table WHERE column IN (SELECT column FROM table WHERE condition)', 'SELECT * FROM employees WHERE dept_id IN (SELECT id FROM departments WHERE location = ''New York'');', 'Returns records where column value exists in subquery result'),
('CREATE VIEW', 'Views', 'CREATE VIEW view_name AS SELECT statement', 'CREATE VIEW high_earners AS SELECT name, salary FROM employees WHERE salary > 80000;', 'Creates a virtual table based on a SELECT statement'),
('DROP VIEW', 'Views', 'DROP VIEW view_name', 'DROP VIEW high_earners;', 'Removes a view from the database'),
('UPDATE VIEW', 'Views', 'CREATE OR REPLACE VIEW view_name AS SELECT statement', 'CREATE OR REPLACE VIEW high_earners AS SELECT name, salary, department FROM employees WHERE salary > 90000;', 'Updates the definition of an existing view');

-- ==== ADVANCED CONCEPTS ====
INSERT INTO cheat_sheet_entries (topic, category, syntax, example, description) VALUES
('CASE Statement', 'Conditional Logic', 'CASE WHEN condition THEN result WHEN condition THEN result ELSE result END', 'SELECT name, CASE WHEN salary > 80000 THEN ''High'' WHEN salary > 50000 THEN ''Medium'' ELSE ''Low'' END AS salary_grade FROM employees;', 'Provides conditional logic in SQL queries'),
('UNION', 'Set Operations', 'SELECT columns FROM table1 UNION SELECT columns FROM table2', 'SELECT name FROM employees UNION SELECT name FROM contractors;', 'Combines results from two or more SELECT statements (removes duplicates)'),
('UNION ALL', 'Set Operations', 'SELECT columns FROM table1 UNION ALL SELECT columns FROM table2', 'SELECT name FROM employees UNION ALL SELECT name FROM contractors;', 'Combines results from two or more SELECT statements (keeps duplicates)'),
('Common Table Expression (CTE)', 'Advanced Queries', 'WITH cte_name AS (SELECT statement) SELECT * FROM cte_name', 'WITH high_earners AS (SELECT * FROM employees WHERE salary > 80000) SELECT * FROM high_earners WHERE department = ''IT'';', 'Creates a temporary named result set for use in a query'),
('Window Functions - ROW_NUMBER', 'Window Functions', 'ROW_NUMBER() OVER (PARTITION BY column ORDER BY column)', 'SELECT name, salary, ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rank FROM employees;', 'Assigns a unique sequential integer to rows within a partition'),
('Window Functions - RANK', 'Window Functions', 'RANK() OVER (PARTITION BY column ORDER BY column)', 'SELECT name, salary, RANK() OVER (ORDER BY salary DESC) AS rank FROM employees;', 'Assigns a rank to rows, with gaps for tied values'),
('Window Functions - DENSE_RANK', 'Window Functions', 'DENSE_RANK() OVER (PARTITION BY column ORDER BY column)', 'SELECT name, salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rank FROM employees;', 'Assigns a rank to rows, without gaps for tied values'),
('LAG Function', 'Window Functions', 'LAG(column, offset) OVER (ORDER BY column)', 'SELECT name, salary, LAG(salary, 1) OVER (ORDER BY hire_date) AS previous_salary FROM employees;', 'Accesses data from a previous row in the result set'),
('LEAD Function', 'Window Functions', 'LEAD(column, offset) OVER (ORDER BY column)', 'SELECT name, salary, LEAD(salary, 1) OVER (ORDER BY hire_date) AS next_salary FROM employees;', 'Accesses data from a subsequent row in the result set');