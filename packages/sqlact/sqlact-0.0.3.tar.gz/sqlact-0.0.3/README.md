SQLACT (SQL Auto-complete)
============================

A python command-line client for composing SQL queries with content-based and history-aware input prediction

# Get it
pip: ``pip3 install sqlact``
Docker: ``docker build -t sqlact .``
Brew: ``brew update && brew install sqlact``

# Run it
Run: ``sqlact postgresql://[user[:password]@][netloc][:port][/dbname][?extra=value[&other=other-value]]``

# Use it
TODO

# Enjoy it
 * Suggests SQL keywords as you type a SQL query
 * Schema-based auto-completion (suggests table columns)
 * Content-based completion (suggests predicate values based on sample)
 * History-aware completion

