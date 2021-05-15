from sqlalchemy import and_, text
from sqlalchemy.orm import Session
import models
import schema


def get_user(db: Session, user_id: int):
    return db.query(models.User).get(models.User.id == user_id)


def get_user_by_name(db: Session, user_name: str):
    return db.query(models.User).get(models.User.name == user_name)


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).get(models.User.email == email)


def insert_user(db: Session, user: schema.UserCreate):
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=user.hashed_password,
        profile=user.profile
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def insert_tweet(db: Session, user_tweet: schema.TweetsCreate):
    db_tweets = models.Tweets(
        user_id=user_tweet.user_id,
        tweet=user_tweet.tweet
    )
    db.add(db_tweets)
    db.commit()
    db.refresh(db_tweets)
    return db_tweets


def insert_follow(db: Session, user_follow: schema.UserFollowListCreate):
    db_follow = models.UserFollowList(
        user_id=user_follow.user_id,
        follow_user=user_follow.follow_user
    )
    db.add(db_follow)
    db.commit()
    db.refresh(db_follow)
    return db_follow


def insert_unfollow(db: Session, user_unfollow: schema.UserFollowListCreate):
    follow_target = db.query(models.UserFollowList).get(and_(
        models.UserFollowList.user_id == user_unfollow.user_id,
        models.UserFollowList.follow_user == user_unfollow.follow_user)
    )
    return follow_target.delete(synchronize_session=True)


def get_timeline(db: Session, user_id: int):

    timeline = db.execute(text("""
    SELECT t.user_id, t.tweet FROM tweets t LEFT JOIN users_follow_list ufl on ufl.user_id = :user_id
    WHERE t.user_id = :user_id OR t.user_id = ufl.follow_user_id
    """), {'user_id': user_id}).fetch_all()
    return [{'user_id': tweet["user_id"], 'tweet': tweet['tweet']} for tweet in timeline]

