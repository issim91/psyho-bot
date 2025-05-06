from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from psychobot.db.models import User, Session, Message
from psychobot.settings import SESSION_DURATION

async def get_or_create_user(session: AsyncSession, telegram_id: int, username: str = None, 
                           first_name: str = None, last_name: str = None) -> User:
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
    
    return user

async def create_session(session: AsyncSession, user_id: int) -> Session:
    new_session = Session(user_id=user_id)
    session.add(new_session)
    await session.commit()
    await session.refresh(new_session)
    return new_session

async def get_active_session(session: AsyncSession, user_id: int) -> Session:
    result = await session.execute(
        select(Session)
        .where(Session.user_id == user_id, Session.is_active == True)
    )
    return result.scalar_one_or_none()

async def end_session(session: AsyncSession, session_id: int, summary: str = None):
    await session.execute(
        update(Session)
        .where(Session.id == session_id)
        .values(
            is_active=False,
            ended_at=datetime.utcnow(),
            summary=summary
        )
    )
    await session.commit()

async def add_message(session: AsyncSession, session_id: int, sender: str, text: str) -> Message:
    message = Message(
        session_id=session_id,
        sender=sender,
        text=text
    )
    session.add(message)
    await session.commit()
    await session.refresh(message)
    return message

async def get_session_history(session: AsyncSession, session_id: int) -> list[Message]:
    result = await session.execute(
        select(Message)
        .where(Message.session_id == session_id)
        .order_by(Message.created_at)
    )
    return result.scalars().all()

async def get_user_sessions(session: AsyncSession, user_id: int) -> list[Session]:
    result = await session.execute(
        select(Session)
        .where(Session.user_id == user_id)
        .order_by(Session.started_at.desc())
    )
    return result.scalars().all() 