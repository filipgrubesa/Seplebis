from fastapi import FastAPI, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .database import get_db, engine, Base
from .models import User, Post, Join
from .auth import genuser, genpass, hashpass, checkpass, getkey
from .secops import verify_token
import secrets
import jwt

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
@app.get("/")
def read_root():
    return FileResponse("app/static/index.html")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/signup")
async def signup(db: AsyncSession = Depends(get_db)):
    username = genuser(secrets.randbelow(5)+12)
    password = genpass(secrets.randbelow(5)+12)
    password_hash = hashpass(password).decode()
    new_user = User(
        username = username,
        password_hash = password_hash
    )
    db.add(new_user)
    await db.commit()

    return {"username": username, "password": password}

@app.post("/login")
async def login(username: str, password: str, response: Response, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    if user is None:
        return {"success": False, "message": "Invalid"}

    if not checkpass(password, user.password_hash.encode()):
        return {"success": False, "message": "Invalid"}

    secretkey = getkey()
    userid = str(user.user_id)
    token = jwt.encode({"user_id":userid}, secretkey, algorithm="HS256")

    response.set_cookie(
        key="jwt",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False, #PROMJENITI
        max_age=86400
    )

    return {"success": True}

@app.post("/join/{post_id}")
async def join_post(post_id: str, user_id: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).where(Post.post_id == post_id))
    post = result.scalar_one_or_none()

    if post is None:
        return {"success": False, "message": "Post not found."}

    existing_join = await db.execute(
        select(Join).where(Join.user_id == user_id, Join.post_id == post_id)
    )
    if existing_join.scalar_one_or_none() is not None:
        return {"success": False, "message": "Already joined."}

    post.joined += 1

    new_join = Join(
        user_id = user_id,
        post_id = post_id
    )
    db.add(new_join)

    await db.commit()

    return {"success": True, "joined": post.joined}

@app.get("/posts/unjoined")
async def get_unjoined_posts(
    limit: int = 5,
    offset: int = 0,
    user_id: str = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):    
    joined_subquery = select(Join.post_id).where(Join.user_id == user_id)

    result = await db.execute(
        select(Post)
        .where(Post.post_id.not_in(joined_subquery))
        .limit(limit)
        .offset(offset)
    )
    posts = result.scalars().all()

    return posts

@app.get("/posts/joined")
async def get_joined_posts(
    limit: int = 5,
    offset: int = 0,
    user_id: str = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    joined_subquery = select(Join.post_id).where(Join.user_id == user_id)

    result = await db.execute(
        select(Post)
        .where(Post.post_id.in_(joined_subquery))
        .limit(limit)
        .offset(offset)
    )
    posts = result.scalars().all()

    return posts

@app.post("/leave/{post_id}")
async def unjoin_post(post_id: str, user_id: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Join).where(Join.user_id == user_id, Join.post_id == post_id))
    join_record = result.scalar_one_or_none()

    if join_record is None:
        return {"success": False, "message": "You haven't joined this post yet."}

    post_result = await db.execute(select(Post).where(Post.post_id == post_id))
    post = post_result.scalar_one_or_none()

    if post is None:
        return {"success": False, "message": "This post no longer exists."}

    post.joined -= 1

    await db.delete(join_record)
    await db.commit()

    return {"success": True, "joined": post.joined}

@app.post("/posts/create")
async def create_post(post: str, needed: int, user_id: str = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    new_post = Post(
        user_id = user_id,
        post = post,
        needed = needed,
        joined = 0
    )
    db.add(new_post)

    await db.commit()

    return {"success": True, "message": "Post published.", "post_id": str(new_post.post_id)}

@app.get("/posts/your")
async def get_your_posts(
    limit: int = 5,
    offset: int = 0,
    user_id: str = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Post)
        .where(Post.user_id == user_id)
        .limit(limit)
        .offset(offset)
    )
    posts = result.scalars().all()
    return posts