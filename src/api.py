from typing import Union
from fastapi import FastAPI, File, UploadFile
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from faster_whisper import WhisperModel
from dotenv import load_dotenv
from method import *
from lib import *
import time
import os
import concurrent.futures
from asyncio import get_event_loop

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.post('/', responses={
        200: {'model': ClassificationResponse},
        400: {'model': HTTPErrorResult},
        500: {'model': HTTPErrorResult},
    },
)

@catch_error
async def upload_audio(file: UploadFile = File(...), task: str = File('transcribe'), language: Optional[str] = File(None), output_format: str = File('srt')) -> Union[ClassificationResponse, HTTPErrorResult]:
    EXECUTOR = concurrent.futures.ThreadPoolExecutor()
    event_loop = get_event_loop()
    s_time = time.time()

    # check input
    language = None if language == '' else language
    audio_type = file.filename.split('.')[-1]
    if not audio_type in input_format:
        return Errors.UNSUPPORTED_AUDIO_FORMAT
    if not task in task_list:
        return Errors.UNSUPPORTED_TASK_ERROR
    if language:
        if not language in language_list:
            return Errors.UNSUPPORTED_LANGUAGE_ERROR
    if not output_format in output_format_list:
        return Errors.UNSUPPORTED_OUTPUT_FORMAT

    # write file
    file_path = f'audio/{file.filename}'
    with open(file_path, "wb") as audio_file:
        content = await file.read()
        audio_file.write(content)
    
    # execute
    result, info = await event_loop.run_in_executor(EXECUTOR, transcribe_async, MODEL, file_path, task, language)

    match output_format:
        case 'srt':
            new_result = generate_srt(result)
        case 'vtt':
            new_result = generate_vtt(result)

    # with open(f'{file.filename}.srt', "w", encoding="utf-8") as file:
    #     file.write(new_result_srt)

    detect_language = info.language
    language_probability = info.language_probability
    e_time = time.time()
    print(f'execute time {e_time - s_time} s')
    return ClassificationResponse(detect_language=detect_language, language_probability=language_probability, new_result=new_result)


if __name__ == '__main__':
    model_type = 'large-v2'
    device_list = get_available_gpu_with_most_memory()
    load_dotenv()
    use_single_gpu = os.environ['USE_SINGLE_GPU']
    use_single_gpu = False if use_single_gpu == 'false' else True
    if use_single_gpu:
        device_list = device_list[:1]

    print(f'''
            use_single_gpu: {use_single_gpu},
            model_type: {model_type},
            device_list: {device_list}
    ''')
    
    MODEL = WhisperModel(model_type, device='cuda', device_index=device_list, num_workers=4, compute_type="float16")
    uvicorn.run(app, host='0.0.0.0', port=8000, workers=1)