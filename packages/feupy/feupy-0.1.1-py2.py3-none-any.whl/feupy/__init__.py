# -*- coding: utf-8 -*-

"""Top-level package for feupy."""

__author__ = """Daniel Filipe Amaro Monteiro"""
__email__ = 'up201806185@fe.up.pt'
__version__ = '0.1.1'

from . _Student import Student
from . _Teacher import Teacher
from . _CurricularUnit import CurricularUnit
from . _Course import Course

from . _Credentials import Credentials
from . _User import User

from . import exams
from . import timetable