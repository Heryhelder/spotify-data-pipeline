WITH source AS (
    SELECT *
    FROM {{ source('user-read-recently-played', 'track') }}
)

SELECT *
FROM source