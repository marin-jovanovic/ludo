sudo su postgres
psql
\c beyond
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'ludo';
\q
psql
// now connected to postgres
drop database if exists beyond;
\q
exit