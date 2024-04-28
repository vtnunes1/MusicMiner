DROP TABLE IF EXISTS tb_track;
DROP TABLE IF EXISTS tb_artist;
DROP TABLE IF EXISTS tb_album;

CREATE TABLE tb_artist (
    `id_artist` VARCHAR(255) PRIMARY KEY,
    `name` VARCHAR(255),
    `followers` INT,
    `popularity` INT
);

CREATE TABLE tb_album (
    `id_album` VARCHAR(255) PRIMARY KEY,
    `name` VARCHAR(255),
    `type` VARCHAR(255),
    `total_tracks` INT, 
    `release_date` VARCHAR(255),
    `release_date_precision` VARCHAR(255)
);

CREATE TABLE tb_track (
    `id_track` VARCHAR(255) PRIMARY KEY,
    `id_artist` VARCHAR(255),
    `id_album` VARCHAR(255),
    `name` VARCHAR(255),
    `disc_number` INT,
    `popularity` INT,
    `duration_ms` INT, 
    `track_number` INT, 
    `acousticness` FLOAT(8,4), 
    `danceability` FLOAT(8,4),
    `energy` FLOAT(8,4),
    `instrumentalness` FLOAT(8,4), 
    `key` INT, 
    `liveness` FLOAT(8,4), 
    `loudness` FLOAT(8,4), 
    `mode` INT, 
    `speechiness` FLOAT(8,4), 
    `tempo` FLOAT(8,4), 
    `time_signature` INT, 
    `valence` FLOAT(12,9),
    `lang` INT, 
    `badwords` TINYINT(1), 
    `lyric` TEXT, 
    `lyric_translate` TEXT,
    FOREIGN KEY (`id_artist`) REFERENCES tb_artist(`id_artist`),
    FOREIGN KEY (`id_album`) REFERENCES tb_album(`id_album`)
);