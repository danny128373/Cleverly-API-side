insert into cleverlyapi_community
values (null, "dankmemes", "the best dank memes", "nothing", 2);

delete from cleverlyapi_community
where id = 22;
delete from cleverlyapi_post
where id = 12;

delete from cleverlyapi_profilecommunity
where id = 12;

insert into cleverlyapi_profilecommunity
values (null, 25, 3);

delete from cleverlyapi_comment
where id = 5;

select distinct p.id, p.content, p.created_at, p.title, p.likes, p.community_id, p.profile_id
from cleverlyapi_profilecommunity pc
join cleverlyapi_post p on pc.community_id = p.community_id and pc.profile_id = 3;
