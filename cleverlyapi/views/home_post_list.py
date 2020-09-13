import sqlite3
from rest_framework.response import Response
from .connection import Connection
from ..models import Post
from ..views import PostSerializer


def home_post_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row

            db_cursor = conn.cursor()
            db_cursor.execute("""
                select 
                    distinct p.id, 
                    p.content, p.created_at, 
                    p.title, p.likes, 
                    p.community_id, 
                    p.profile_id
                from cleverlyapi_profilecommunity pc
                join cleverlyapi_post p on pc.community_id = p.community_id and pc.profile_id = ?;
            """, (request.user.id,))

            dataset = db_cursor.fetchall()
            posts = []

            for row in dataset:
                post = Post()
                post.id = row["id"]
                post.created_at = row["create_at"]
                post.community_id = row["community_id"]
                post.profile_id = row["profile_id"]
                post.content = row["content"]
                post.title = row["title"]
                posts.append(posts)

            serializer = PostSerializer(
            posts,
            many=True,
            context={'request':request}
        )
        return Response(serializer.data)
