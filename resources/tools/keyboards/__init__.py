from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup


__all__ = ['Call', 'Url', 'InlineKeyboard', 'ReplyKeyboard']


# Button Types
class ButtonType:
    # Common functions for Button types (need for the future updates)
    def check(self, *args):
        for i in args:
            if type(i) is not str:
                raise ValueError('Wrong values.')
        return args


class Call(ButtonType):
    def __new__(cls, text: str, callback_data: str):
        '''
        Call type button. Pressing sending a callback.

        :param text: Text for the front of the button.
        :param callback_data: Callback sent to servers and handlers.
        :return: Already done button for InlineKeyboard.
        '''
        return InlineKeyboardButton(**dict(zip(('text', 'callback_data'), super().check(text, callback_data))))


class Url(ButtonType):
    def __new__(cls, text: str, url: str):
        '''
        Url type button. Clicking redirects to the link.

        :param text: Text for the front of the button.
        :param url: Redirect link.
        :return: Already done button for InlineKeyboard.
        '''
        return InlineKeyboardButton(**dict(zip(('text', 'url'), super().check(text, url))))


# Custom Inline Keyboard Constructor
class InlineKeyboard:
    def __new__(cls, *args: List[InlineKeyboardButton], row_width: int = 5):
        '''
        Class to easy construct your own keyboard.

        :param args: Buttons (Call() and Url() only now available).
        :param row_width: Max width of keyboard in row.
        :return: Already done inline keyboard.
        '''
        return InlineKeyboardMarkup(row_width=row_width).add(args)


# Custom Reply Keyboard Constructor (While nothing special)
class ReplyKeyboard:
    def __new__(cls, *args: List[str], row_width: int = 3):
        '''
        Class to easy construct you own keyboard. (Nothing interesting now)

        :param args: String values of button text.
        :param row_width: Max width of keyboard in row.
        :return: Already done reply keyboard.
        '''
        return ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=row_width).add(args)