from datetime import datetime
from typing import Dict, Optional
from psychobot.settings import SESSION_DURATION
from psychobot.db.crud import get_active_session, end_session, add_message, create_session, get_session_history
from psychobot.core.dialogue_engine import PsychologistAI
from psychobot.core.chatgpt_client import ChatGPTClient
from sqlalchemy.ext.asyncio import AsyncSession

class SessionManager:
    def __init__(self):
        self.psychologist = PsychologistAI()
        self.chatgpt = ChatGPTClient()
        self.active_sessions: Dict[int, datetime] = {}  # user_id: session_start_time

    async def start_session(self, session: AsyncSession, user_id: int) -> Optional[int]:
        # Check if user already has an active session
        active_session = await get_active_session(session, user_id)
        if active_session:
            return active_session.id

        # Create new session
        new_session = await create_session(session, user_id)
        self.active_sessions[user_id] = datetime.utcnow()

        # Add opening message
        opening_questions = self.psychologist.get_opening_questions()
        await add_message(session, new_session.id, "psychologist", 
                         "**Здравствуйте!** Я рада вас видеть. " + opening_questions[0])
        
        return new_session.id

    async def end_session(self, session: AsyncSession, user_id: int, session_id: int):
        # Get session history for summary
        history = await get_session_history(session, session_id)
        messages = self.psychologist.prepare_messages("", history)
        
        # Generate session summary
        summary = await self.chatgpt.summarize_session(messages)
        
        # End session in database
        await end_session(session, session_id, summary)
        
        # Remove from active sessions
        if user_id in self.active_sessions:
            del self.active_sessions[user_id]

    def is_session_expired(self, user_id: int) -> bool:
        if user_id not in self.active_sessions:
            return True
        
        session_start = self.active_sessions[user_id]
        return datetime.utcnow() - session_start > SESSION_DURATION

    async def process_message(self, session: AsyncSession, user_id: int, session_id: int, 
                            user_message: str) -> str:
        # Get conversation history
        history = await get_session_history(session, session_id)
        
        # Prepare messages for ChatGPT
        messages = self.psychologist.prepare_messages(user_message, history)
        
        # Get response from ChatGPT
        response = await self.chatgpt.generate_response(messages)
        
        # Save both messages to database
        await add_message(session, session_id, "user", user_message)
        await add_message(session, session_id, "psychologist", response)
        
        return response 
