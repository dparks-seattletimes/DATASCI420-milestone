SELECT
  question.*
  ,ans.*
  ,user.*
FROM (
  SELECT 
    id as answer_id
--     , body as answer_body
    , comment_count as answer_comments
    , creation_date as answer_creation_date
    , owner_user_id as answer_owner_id
    , parent_id as answer_parent_id
    , post_type_id as answer_post_type_id
    , score as answer_score
    , tags as answer_tags
  FROM `bigquery-public-data.stackoverflow.posts_answers`
) as ans
LEFT OUTER JOIN (
  SELECT
    id as user_id
    , display_name as user_display_name
    , reputation as user_reputation
    , up_votes as user_up_votes
    , down_votes as user_down_votes
    , views as user_views
    , profile_image_url as user_profile_img_url
    , website_url as user_website_url
  FROM `bigquery-public-data.stackoverflow.users`
) as user ON ans.answer_owner_id=user.user_id
INNER JOIN (
  SELECT
    id as question_id
    , title as question_tile
--     , body as question_body
    , accepted_answer_id
    , answer_count
    , creation_date as question_creation_date
    , favorite_count as question_fav_count
    , owner_display_name as question_owner_display_name
    , owner_user_id as question_owner_id
    , post_type_id as question_post_type_id
    , score as question_score
    , tags as question_tags
    , view_count as question_view_count
  FROM `bigquery-public-data.stackoverflow.posts_questions`  
) as question ON ans.answer_parent_id=question.question_id
WHERE ans.answer_owner_id IS NOT NULL
ORDER BY question.question_id
LIMIT 1000

