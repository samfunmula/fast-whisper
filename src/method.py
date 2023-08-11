from typing import Generator
import nvidia_smi
from lib import *
from faster_whisper import transcribe

def transcribe_async(model:transcribe.WhisperModel, file_path: str, task: str, language: str = None) -> tuple[Generator, transcribe.TranscriptionInfo]:
    result, info = model.transcribe(file_path, beam_size=5, task=task, language=language)
    return result, info

def handle_ms(time):
    ms = str(time).split('.')[-1]
    if len(ms) < 3:
        ms += '0'
    elif len(ms) > 3:
        ms = ms[:3]
    return ms

def generate_srt(result: Generator) -> str:
    srt_content = ""
    for index, _dict in enumerate(result):
        start_time = _dict.start
        end_time = _dict.end
        text = _dict.text

        s_h, e_h = int(start_time//(60 * 60)), int(end_time//(60 * 60))
        s_m, e_m = int((start_time % (60 * 60))//60), int((end_time % (60 * 60))//60)
        s_s, e_s = int(start_time % 60), int(end_time % 60)
        s_ms, e_ms = handle_ms(start_time), handle_ms(end_time)

        s_time = f'{s_h:02}:{s_m:02}:{s_s:02},{s_ms:03}'
        e_time = f'{e_h:02}:{e_m:02}:{e_s:02},{e_ms:03}'
        srt_content += f'{index+1}\n'

        srt_content +=  f'{s_time} --> {e_time}\n'
        srt_content += f'{text}\n\n\n'
    return srt_content

def generate_vtt(result: Generator) -> str:
    vtt_content = "WEBVTT\n\n"
    for index, _dict in enumerate(result):
        start_time = _dict.start
        end_time = _dict.end
        text = _dict.text

        s_h, e_h = int(start_time//(60 * 60)), int(end_time//(60 * 60))
        s_m, e_m = int((start_time % (60 * 60))//60), int((end_time % (60 * 60))//60)
        s_s, e_s = int(start_time % 60), int(end_time % 60)
        s_ms, e_ms = handle_ms(start_time), handle_ms(end_time)

        s_time = f'{s_h:02}:{s_m:02}:{s_s:02}.{s_ms:03}'
        e_time = f'{e_h:02}:{e_m:02}:{e_s:02}.{e_ms:03}'

        vtt_content += f"{s_time} --> {e_time}\n"
        vtt_content += f"{text}\n\n"
    return vtt_content


def get_available_gpu_with_most_memory() -> list[str]:
    nvidia_smi.nvmlInit()
    deviceCount = nvidia_smi.nvmlDeviceGetCount()
    devices = []
    for i in range(deviceCount):
        handle = nvidia_smi.nvmlDeviceGetHandleByIndex(i)
        mem = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
        free_m = mem.free/1024**2
        devices.append((i, free_m))
    devices.sort(key=lambda x: x[1], reverse=True)
    return [i[0] for i in devices]
