
with raw_dates as (
    select
        distinct message_date::date as date
    from {{ ref('stg_telegram_messages') }}
),

dim_dates as (
    select
        row_number() over (order by date) as date_id,
        date,
        extract(year from date) as year,
        extract(month from date) as month,
        extract(day from date) as day,
        to_char(date, 'Day') as day_name
    from raw_dates
)

select * from dim_dates
