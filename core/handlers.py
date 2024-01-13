from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import core.locale
import core.keyboards
from core.states import UploadFile
router = Router()


@router.message(Command('start'))
async def start(message: types.Message):
    await message.answer(
        core.locale.start,
        reply_markup=core.keyboards.main_table)


@router.message(F.text == 'Меню')
@router.message(F.text == 'В меню')
@router.message(F.text == 'В главное меню')
async def menu(message: types.Message):
    await message.answer(
        core.locale.in_the_menu,
        reply_markup=core.locale.main_table)

# @rounter.message(F.text == 'Настройки')
# @router.message(F.text == '⚙️ Настройки')
# async def settings(message: types.Message):
#     await message.answer(core.locale.settings, reply_markup=)


@router.callback_query(F.data == 'add_file')
async def file_options_choice(callback: types.CallbackQuery, state=FSMContext):
    state.set_state(UploadFile.type_choice)
    await callback.message.edit_text(
        core.locale.file_options,
        reply_markup=core.keyboards.file_choice_table)


@router.callback_query(F.data in [
    'add_photo', 'add_video', 'add_document', 'add_audio'])
async def file_chosen(callback: types.CallbackQuery, state=FSMContext):
    state.set_state(UploadFile.file_await)
    if F.data == 'add_photo':
        await callback.message.answer(core.locale.photo_awaiting)
    elif F.data == 'add_video':
        await callback.message.answer(core.locale.video_awaiting)
    elif F.data == 'add_document':
        await callback.message.answer(core.locale.document_awaiting)
    elif F.data == 'add_audio':
        await callback.message.answer(core.locale.audio_awaiting)


# @router.message(F.photo)
# async def get_photo(message: types.Message, state=FSMContext):

#     state.finish()
