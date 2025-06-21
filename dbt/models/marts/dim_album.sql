with source_data AS (
    SELECT *
    FROM {{ ref('stg_album') }}
)

SELECT DISTINCT
    MD5(CONCAT(id, name, release_date))  AS id
    ,id                                  AS album_id
    ,name                                AS name
    ,release_date                        AS release_date
    ,total_tracks                        AS total_tracks
FROM source_data