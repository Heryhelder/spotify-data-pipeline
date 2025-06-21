WITH dim_album AS (
    SELECT *
    FROM {{ ref('dim_album') }}
),

dim_date AS (
    SELECT *
    FROM {{ ref('dim_date') }}
)

SELECT
    a.id AS album_id
    ,d.id AS date_id
    ,COUNT(*) AS total_listenings
FROM {{ ref('stg_track') }} t
INNER JOIN dim_album a ON t.album_id = a.album_id
INNER JOIN dim_date d ON DATE(t.played_at) = d.date
GROUP BY a.id, d.id