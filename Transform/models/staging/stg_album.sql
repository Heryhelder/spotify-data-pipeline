WITH source AS (
    SELECT *
    FROM {{ source('user-read-recently-played', 'album') }}
)

SELECT *
FROM source