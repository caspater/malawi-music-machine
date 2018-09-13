
create table artists (
    id serial primary key,
    mm_artist_id integer,
    name character varying(100),
    artist_url text,
    real_name character varying(100), -- String 
    biography text,
    city character varying(50),
    country character varying(50),
    profile_pic_url text,
    registered_on timestamp without time zone, 
    website_url text,
    created timestamp without time zone,
    modified timestamp without time zone
);

create table albums (
    id serial primary key,
    mm_album_id integer,
    artist_id integer,
    title character varying(100) not null,
    year integer,
    label character varying(100),
    country character varying(50),
    genres varchar[],
    album_type character varying(20),
    album_url text,
    no_of_views integer,
    no_of_songs integer,
    review text,
    created timestamp without time zone,
    modified timestamp without time zone
);


create table songs (
    id serial primary key,
    mm_song_id integer,
    artist_id integer,
    album_id integer,
    title character varying(100) not null,
    lyrics text,
    genres varchar[],
    no_of_downloads integer,
    no_of_plays integer,
    size_bytes integer,
    size_human character varying(10),
    duration_millis integer,
    duration_human character varying(10),
    song_url text,
    download_url text,
    uploaded_on date,
    created timestamp without time zone,
    modified timestamp without time zone
);

create table songs_artists (
    id serial primary key,
    song_id integer,
    artist_id integer
);

create table bundle_requests (
    id serial primary key,
    bundle_name character varying(100) not null,
    request_id character varying(64),
    song_ids varchar[] not null,
    archive_as character varying(8) not null,
    requested_on timestamp without time zone not null,
    download_file text, -- url to the file for download
    created timestamp without time zone
);
