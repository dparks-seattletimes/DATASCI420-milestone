SELECT
  id
  , title
  --, body
  , accepted_answer_id
  , answer_count
  , creation_date
  , favorite_count
  , owner_user_id
  , post_type_id
  , score
  , tags
  , view_count
FROM `bigquery-public-data.stackoverflow.posts_questions`
LIMIT 1000
