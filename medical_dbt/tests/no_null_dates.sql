
-- Ensure that no message is missing a date
select *
from {{ ref('fct_messages') }}
where date_id is null
