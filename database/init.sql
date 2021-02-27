--
-- PostgreSQL database dump
--

-- Dumped from database version 10.15 (Debian 10.15-1.pgdg90+1)
-- Dumped by pg_dump version 10.15 (Debian 10.15-1.pgdg90+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: evidences; Type: TABLE; Schema: public; Owner: admin_dip
--

CREATE TABLE public.evidences (
    uuid character varying NOT NULL,
    source_type character varying,
    parent character varying,
    keywords character varying,
    keywords_found character varying,
    urls_found text,
    urls_queryable text,
    title character varying,
    url character varying
);


ALTER TABLE public.evidences OWNER TO admin_dip;

--
-- Name: utenti; Type: TABLE; Schema: public; Owner: admin_dip
--

CREATE TABLE public.utenti (
    uuid character varying NOT NULL,
    email character varying NOT NULL
);


ALTER TABLE public.utenti OWNER TO admin_dip;

--
-- Data for Name: utenti; Type: TABLE DATA; Schema: public; Owner: admin_dip
--

COPY public.utenti (uuid, email) FROM stdin;
\.


--
-- PostgreSQL database dump complete
--

