sudo su postgres
psql
\c ludo
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'ludo';
\q
psql
// now connected to postgres
drop database if exists ludo;
\q
exit