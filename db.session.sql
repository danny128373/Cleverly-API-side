insert into cleverlyapi_community
values (null, "dankmemes", "the best dank memes", "nothing", 2);

delete from cleverlyapi_community
where id = 23;
delete from cleverlyapi_post
where id = 14;

delete from cleverlyapi_profilecommunity
where id = 13;

insert into cleverlyapi_profilecommunity
values (null, 25, 3);

delete from cleverlyapi_comment
where id = 5;

select distinct p.id, p.content, p.created_at, p.title, p.likes, p.community_id, p.profile_id
from cleverlyapi_profilecommunity pc
join cleverlyapi_post p on pc.community_id = p.community_id and pc.profile_id = 3;

delete from cleverlyapi_comment
where id =10;

delete from cleverlyapi_profilecommunity
where id = 19;
delete from cleverlyapi_comment
where id =8;

insert into cleverlyapi_profilelikescomment
values (null, 'like', 20, 3);

delete from cleverlyapi_profilelikescomment
where id = 34;

delete from cleverlyapi_profilelikescomment;