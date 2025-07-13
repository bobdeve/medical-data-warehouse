
with base as (
    select
        distinct channel
    from {{ ref('stg_telegram_messages') }}
),

dim_channels as (
    select
        row_number() over (order by channel) as channel_id,
        channel
    from base
)

select * from dim_channels
