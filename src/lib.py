from __future__ import annotations
from pydantic import BaseModel
import logging
from dataclasses import dataclass
from pydantic import BaseModel
from functools import wraps
from typing import Any, Callable, Coroutine, Optional, ParamSpec
from fastapi.responses import JSONResponse

input_format = [
    'mp3',
    'wav',
    'flac',
    'm4a',
    'ogg',
    'mp4',
    'wmv',
    'mov'
]

output_format_list = [
    'srt',
    'vtt'
]

task_list = [
    'transcribe',
    'translate'
]

language_list = [
    'zh','vi','ja','en','th','ko','my','pl','jw','nn','tr','ar','ru','ms','it','fr','id','ta','nl',
    'km','cy','hi','es','ml','de','bo','el','sv','pt','fa','la','he','ro','da','sn','hu','fi','te',
    'tl','bn','ur','ne','br','uk','si','yo','haw','tg','sd','gu','am','be','yi','lo','ka','uz','fo',
    'ht','ps','tk','mt','sa','lb','mg','as','ba','tt','su','ln','ha','mk','ca','cs','no','hr','bg',
    'lt','mi','sk','lv','sr','az','sl','kn','et','oc','eu','is','hy','mn','bs','kk','sq','sw','gl',
    'mr','pa','so','af', None,
]

class ClassificationResponse(BaseModel):
    detect_language: str
    language_probability: float
    result: str

class HTTPErrorResult(BaseModel):
    result : str

@dataclass
class Errors:
    UNSUPPORTED_AUDIO_FORMAT = JSONResponse({'result':'UNSUPPORTED_AUDIO_FORMAT'},400)
    UNSUPPORTED_OUTPUT_FORMAT = JSONResponse({'result':'UNSUPPORTED_OUTPUT_FORMAT'},400)
    UNSUPPORTED_TASK_ERROR = JSONResponse({'result':'UNSUPPORTED_TASK_ERROR'},400)
    UNSUPPORTED_LANGUAGE_ERROR = JSONResponse({'result':'UNSUPPORTED_LANGUAGE_ERROR'},400)
    INTERNAL_ERROR = JSONResponse({'result':"INTERNAL_ERROR"},500)

logger = logging.getLogger('uvicorn.error')
P = ParamSpec('P')

def catch_error(func: Callable[P, Coroutine[Any, Any, Any]]) -> Callable[P, Coroutine[Any, Any, Any]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except Exception as ex:
            logger.error(str(ex), exc_info=True, stack_info=True)
            return Errors.INTERNAL_ERROR

    return wrapper