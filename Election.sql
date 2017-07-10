--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.2
-- Dumped by pg_dump version 9.6.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
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


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: has; Type: TABLE; Schema: public; Owner: dbsproject
--

CREATE TABLE has (
    id integer,
    value text
);


ALTER TABLE has OWNER TO dbsproject;

--
-- Name: hashtag; Type: TABLE; Schema: public; Owner: dbsproject
--

CREATE TABLE hashtag (
    value text NOT NULL,
    total_count integer
);


ALTER TABLE hashtag OWNER TO dbsproject;

--
-- Name: tweet; Type: TABLE; Schema: public; Owner: dbsproject
--

CREATE TABLE tweet (
    id integer NOT NULL,
    handle text,
    is_retweet boolean,
    "time" timestamp without time zone,
    is_quote_status boolean,
    retweet_count integer,
    favourite_count integer,
    text text
);


ALTER TABLE tweet OWNER TO dbsproject;

--
-- Data for Name: has; Type: TABLE DATA; Schema: public; Owner: dbsproject
--

COPY has (id, value) FROM stdin;
\.


--
-- Data for Name: hashtag; Type: TABLE DATA; Schema: public; Owner: dbsproject
--

COPY hashtag (value, total_count) FROM stdin;
\.


--
-- Data for Name: tweet; Type: TABLE DATA; Schema: public; Owner: dbsproject
--

COPY tweet (id, handle, is_retweet, "time", is_quote_status, retweet_count, favourite_count, text) FROM stdin;
\.


--
-- Name: hashtag hastag_pkey; Type: CONSTRAINT; Schema: public; Owner: dbsproject
--

ALTER TABLE ONLY hashtag
    ADD CONSTRAINT hastag_pkey PRIMARY KEY (value);


--
-- Name: tweet tweet_pkey; Type: CONSTRAINT; Schema: public; Owner: dbsproject
--

ALTER TABLE ONLY tweet
    ADD CONSTRAINT tweet_pkey PRIMARY KEY (id);


--
-- Name: has has_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbsproject
--

ALTER TABLE ONLY has
    ADD CONSTRAINT has_id_fkey FOREIGN KEY (id) REFERENCES tweet(id);


--
-- Name: has has_value_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbsproject
--

ALTER TABLE ONLY has
    ADD CONSTRAINT has_value_fkey FOREIGN KEY (value) REFERENCES hashtag(value);


--
-- PostgreSQL database dump complete
--

