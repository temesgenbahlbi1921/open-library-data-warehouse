SQL Query for tables 

=========================================================================



CREATE TABLE fact_book_ratings
(
    book_id VARCHAR,
    title VARCHAR(255),
    work_id VARCHAR,
    author_id VARCHAR,
    author_name VARCHAR(255),
    rating NUMERIC,
    CONSTRAINT fact_book_ratings_author_id_fkey FOREIGN KEY (author_id)
        REFERENCES dim_authors (author_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fact_book_ratings_book_id_fkey FOREIGN KEY (book_id)
        REFERENCES dim_editions (book_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fact_book_ratings_work_id_fkey FOREIGN KEY (work_id)
        REFERENCES dim_works (work_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
);



CREATE TABLE dim_editions
(
    type VARCHAR(255),,
    book_id VARCHAR(255),NOT NULL,
    revision BIGINT,
    last_modified TIMESTAMP WITHOUT TIME ZONE,
    title VARCHAR(255),,
    publish_date TIMESTAMP WITHOUT TIME ZONE,
    number_of_pages DOUBLE PRECISION,
    physical_format VARCHAR,
    isbn_13 VARCHAR(255),,
    isbn_10 VARCHAR(255),,
    publishers VARCHAR,
    authors VARCHAR(255),,
    latest_revision DOUBLE PRECISION,
    works VARCHAR(255),,
    CONSTRAINT dim_editions_pkey PRIMARY KEY (book_id)
);




CREATE TABLE dim_ratings
(
    work_id VARCHAR,
    book_id VARCHAR,
    rating BIGINT,
    date TIMESTAMP WITHOUT TIME ZONE,
    rating_id BIGINT NOT NULL DEFAULT           nextval('dim_ratings_rating_id_seq'::regclass),
    CONSTRAINT dim_ratings_pkey PRIMARY KEY (rating_id),
    CONSTRAINT dim_ratings_work_id_fkey FOREIGN KEY (work_id)
        REFERENCES dim_works (work_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT g FOREIGN KEY (book_id)
        REFERENCES dim_editions (book_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);



CREATE TABLE dim_works
(
    type VARCHAR,
    work_id VARCHAR NOT NULL,
    revision BIGINT,
    last_modified TIMESTAMP WITHOUT TIME ZONE,
    title VARCHAR,
    created TIMESTAMP WITHOUT TIME ZONE,
    subjects VARCHAR,
    authors VARCHAR,
    covers VARCHAR,
    latest_revision BIGINT,
    CONSTRAINT dim_works_pkey PRIMARY KEY (work_id)
);



CREATE TABLE dim_authors
(
    type VARCHAR,
    author_id VARCHAR NOT NULL,
    revision BIGINT,
    created_at TIMESTAMP WITHOUT TIME ZONE,
    name VARCHAR,
    key VARCHAR,
    source_records VARCHAR,
    latest_revision DOUBLE PRECISION,
    last_modified TIMESTAMP WITHOUT TIME ZONE,
    CONSTRAINT dim_authors_pkey PRIMARY KEY (author_id)
);


