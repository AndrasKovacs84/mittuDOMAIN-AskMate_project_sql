--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

ALTER TABLE IF EXISTS ONLY public.user_mates DROP CONSTRAINT IF EXISTS pk_user_mates_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question DROP CONSTRAINT IF EXISTS pk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question DROP CONSTRAINT IF EXISTS fk_user_mates_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS pk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS fk_user_mates_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS pk_comment_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_user_mates_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS pk_question_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.tag DROP CONSTRAINT IF EXISTS pk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_tag_id CASCADE;

DROP TABLE IF EXISTS public.user_mates;
DROP SEQUENCE IF EXISTS public.user_mates_id_seq;
CREATE TABLE user_mates (
    id serial NOT NULL,
    user_mates_name varchar(40) NOT NULL,
    reputation int,
    submission_time timestamp without time zone
);

DROP TABLE IF EXISTS public.question;
DROP SEQUENCE IF EXISTS public.question_id_seq;
CREATE TABLE question (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text,
    user_mates_id integer
);

DROP TABLE IF EXISTS public.answer;
DROP SEQUENCE IF EXISTS public.answer_id_seq;
CREATE TABLE answer (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    message text,
    image text,
    user_mates_id integer
);

DROP TABLE IF EXISTS public.comment;
DROP SEQUENCE IF EXISTS public.comment_id_seq;
CREATE TABLE comment (
    id serial NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    user_mates_id integer
);


DROP TABLE IF EXISTS public.question_tag;
CREATE TABLE question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);

DROP TABLE IF EXISTS public.tag;
DROP SEQUENCE IF EXISTS public.tag_id_seq;
CREATE TABLE tag (
    id serial NOT NULL,
    name text
);


ALTER TABLE ONLY answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);

ALTER TABLE ONLY question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);

ALTER TABLE ONLY user_mates
    ADD CONSTRAINT pk_user_mates_id PRIMARY KEY (id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);

ALTER TABLE ONLY tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_user_mates_id FOREIGN KEY (user_mates_id) REFERENCES user_mates(id);

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_user_mates_id FOREIGN KEY (user_mates_id) REFERENCES user_mates(id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY question
    ADD CONSTRAINT fk_user_mates_id FOREIGN KEY (user_mates_id) REFERENCES user_mates(id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES tag(id);

INSERT INTO user_mates VALUES (1, 'Norbi', NULL, '2017-04-25 14:42:00');
INSERT INTO user_mates VALUES (2, 'Attila', NULL, '2017-04-25 14:43:00');
INSERT INTO user_mates VALUES (3, 'Andris', NULL, '2017-04-25 14:44:00');
INSERT INTO user_mates VALUES (4, 'bekor', NULL, '2017-04-25 14:45:00');
SELECT pg_catalog.setval('user_mates_id_seq', 4, true);

INSERT INTO question VALUES (0, '2017-04-28 08:29:00', 29, 7, 'How to make lists in Python?', 'I am totally new to this, any hints?', NULL, 1);
INSERT INTO question VALUES (1, '2017-04-29 09:19:00', 15, 9, 'Wordpress loading multiple jQuery Versions', 'I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(".myBook").booklet();

I could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.

BUT in my theme i also using jquery via webpack so the loading order is now following:

jquery
booklet
app.js (bundled file with webpack, including jquery)', 'images/image1.png', 2);
INSERT INTO question VALUES (2, '2017-05-01 10:41:00', 1364, 57, 'Drawing canvas with an image picked with Cordova Camera Plugin', 'I''m getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I''m on IOS, it throws errors such as cross origin issue, or that I''m trying to use an unknown format.

This is the code I''m using to draw the image (that works on web/desktop but not cordova built ios app)', NULL, 3);
SELECT pg_catalog.setval('question_id_seq', 2, true);

INSERT INTO answer VALUES (1, '2017-04-28 16:49:00', 4, 1, 'You need to use brackets: my_list = []', NULL, 2);
INSERT INTO answer VALUES (2, '2017-04-25 14:42:00', 35, 1, 'Look it up in the Python docs', 'images/image2.jpg', 1);
SELECT pg_catalog.setval('answer_id_seq', 2, true);

INSERT INTO comment VALUES (1, 0, NULL, 'Please clarify the question as it is too vague!', '2017-05-01 05:49:00', 2);
INSERT INTO comment VALUES (2, NULL, 1, 'I think you could use my_list = list() as well.', '2017-05-02 16:55:00', 1);
SELECT pg_catalog.setval('comment_id_seq', 2, true);

INSERT INTO tag VALUES (1, 'python');
INSERT INTO tag VALUES (2, 'sql');
INSERT INTO tag VALUES (3, 'css');
SELECT pg_catalog.setval('tag_id_seq', 3, true);

INSERT INTO question_tag VALUES (0, 1);
INSERT INTO question_tag VALUES (1, 3);
INSERT INTO question_tag VALUES (2, 3);
