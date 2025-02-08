

open cli py sqlite3

``` bash
py -m sqlite3 .\tutorial.db
```


Querying the sqlite_master Table
For more control, you can query the ‘sqlite_master’ table directly, which stores the metadata of the database, including table definitions.

For example:
```sql
SELECT name FROM sqlite_master WHERE type='table';
```


Another approach in SQLite is to use the PRAGMA command, which provides different characteristics of the SQLite database. One useful PRAGMA command is ‘table_info’, which can be used to get information about the columns in a table.

While ‘table_info’ does not list all the tables, it can be used alongside table listing commands to understand table structures immediately after finding their names.

Example:

```sql
PRAGMA table_info('actor');
```


