import re

EXC_MSG = 'Недопустимый порядок токенов. "{cur_token}" следует за "{prev_token}"'
LEFT_BRACKET = "("
RIGTH_BRACKET = ")"
WHITESPICE = " "

DIGIT_WITH_SPACE = re.compile(r"(\d+|[ ])")
WITHOUT_DIGIT = re.compile(r"[() ]")
WITHOUT_LEFT_BRACKET = re.compile(r"(\d+|[) ])")
ALLOW_TOKEN = re.compile(r"(\d+|[)( ])")
