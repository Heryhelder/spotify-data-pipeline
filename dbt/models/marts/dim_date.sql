with source_data AS (
    SELECT *
    FROM {{ ref('stg_track') }}
)

SELECT DISTINCT
    MD5(DATE(played_at)::varchar)  AS id
    ,DATE(played_at)               AS date
    ,DATE_PART('month', played_at) AS month
    ,DATE_PART('year', played_at)  AS year
FROM source_data