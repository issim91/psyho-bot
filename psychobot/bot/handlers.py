from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode

from psychobot.db.crud import get_or_create_user, get_active_session, get_session_history
from psychobot.db.database import get_session
from psychobot.bot.session_manager import SessionManager

router = Router()
session_manager = SessionManager()

class SessionStates(StatesGroup):
    active = State()

@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    async with get_session() as session:
        # Get or create user
        user = await get_or_create_user(
            session,
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name
        )
        
        # Start new session
        session_id = await session_manager.start_session(session, user.id)
        
        # Get active session
        active_session = await get_active_session(session, user.id)
        
        # Send welcome message
        await message.answer(
            "Добро пожаловать на психологическую консультацию! "
            "Наша сессия длится 1 час. Вы можете завершить её в любой момент командой /end.",
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Send first question
        history = await get_session_history(session, session_id)
        if history:
            await message.answer(history[-1].text, parse_mode=ParseMode.MARKDOWN)
        
        # Set state to active
        await state.set_state(SessionStates.active)

@router.message(Command("end"))
async def end_session_handler(message: Message, state: FSMContext):
    async with get_session() as session:
        # Get user and active session
        user = await get_or_create_user(session, message.from_user.id)
        active_session = await get_active_session(session, user.id)
        
        if active_session:
            # End session
            await session_manager.end_session(session, user.id, active_session.id)
            
            # Send goodbye message
            await message.answer(
                "Спасибо за сессию! Если у вас возникнут вопросы или потребуется помощь, "
                "вы всегда можете начать новую сессию командой /start.",
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Reset state
            await state.clear()
        else:
            await message.answer(
                "У вас нет активной сессии. Начните новую сессию командой /start.",
                parse_mode=ParseMode.MARKDOWN
            )

@router.message(SessionStates.active)
async def message_handler(message: Message, state: FSMContext):
    async with get_session() as session:
        # Get user and active session
        user = await get_or_create_user(session, message.from_user.id)
        active_session = await get_active_session(session, user.id)
        
        if not active_session:
            await message.answer(
                "Ваша сессия завершена. Начните новую сессию командой /start.",
                parse_mode=ParseMode.MARKDOWN
            )
            await state.clear()
            return
        
        # Check if session expired
        if session_manager.is_session_expired(user.id):
            await session_manager.end_session(session, user.id, active_session.id)
            await message.answer(
                "Время сессии истекло. Спасибо за беседу! "
                "Если хотите продолжить, начните новую сессию командой /start.",
                parse_mode=ParseMode.MARKDOWN
            )
            await state.clear()
            return
        
        # Process message
        response = await session_manager.process_message(
            session, user.id, active_session.id, message.text
        )
        
        await message.answer(response, parse_mode=ParseMode.MARKDOWN) 