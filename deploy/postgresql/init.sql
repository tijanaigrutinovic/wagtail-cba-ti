-- Reference PostgreSQL setup for production (runbook section 5.3).
-- Run as postgres: sudo -u postgres psql -f deploy/postgresql/init.sql

CREATE DATABASE cba_wagtail;
CREATE USER cba_wagtail_user WITH PASSWORD 'CHANGE_THIS_STRONG_PASSWORD';
ALTER ROLE cba_wagtail_user SET client_encoding TO 'utf8';
ALTER ROLE cba_wagtail_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE cba_wagtail_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE cba_wagtail TO cba_wagtail_user;
