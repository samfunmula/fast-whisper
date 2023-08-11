### Start Fast API
```bash
cd src/
python3 api.py
```

### Start Docker
```
bash runDocker.sh
```
## Support Formats
### Audio / Video
 * mp3
 * wav
 * flac
 * m4a
 * ogg
 * mp4
 * wmv
 * mov

### Task
 * Transcribe (default)
 * Translate

### Support Language
```py
['zh','vi','ja','en','th','ko','my','pl','jw','nn','tr','ar','ru','ms','it','fr','id','ta','nl','km','cy','hi','es','ml','de','bo','el','sv','pt','fa','la','he','ro','da','sn','hu','fi','te','tl','bn','ur','ne','br','uk','si','yo','haw','tg','sd','gu','am','be','yi','lo','ka','uz','fo','ht','ps','tk','mt','sa','lb','mg','as','ba','tt','su','ln','ha','mk','ca','cs','no','hr','bg','lt','mi','sk','lv','sr','az','sl','kn','et','oc','eu','is','hy','mn','bs','kk','sq','sw','gl','mr','pa','so','af']
```
### Output Format
* srt (default)
* vtt

## Request
### Curl
* Task default is transcribe
* Language default is None, it will automatically detect language.
#### pass audio
``` bash 
# task=transcribe： speech -> content
curl -X 'POST' 'http://0.0.0.0:8000/' \
     -H 'accept: application/json' \
     -H 'Content-Type: multipart/form-data' \
     -F 'file=@audio.mp3;type=audio/mpeg' \
     -F 'task=transcribe'

# task=translate： speech -> content(English)
curl -X 'POST' 'http://0.0.0.0:8000/' \
     -H 'accept: application/json' \
     -H 'Content-Type: multipart/form-data' \
     -F 'file=@audio.mp3;type=audio/mpeg' \
     -F 'task=translate'
```

#### pass video
```bash
# task=translate： speech -> content(English)
curl -X 'POST' 'http://0.0.0.0:8000/' \
     -H 'accept: application/json' \
     -H 'Content-Type: multipart/form-data' \
     -F 'file=@video.mp4;type=video/mpeg' \
     -F 'task=translate'
```

#### file and type
* -F 'file=@audio.mp3; type=audio/mpeg' \
* -F 'file=@audio.flac; type=audio/flac' \
* -F 'file=@audio.m4a; type=audio/m4a' \
* -F 'file=@audio.ogg; type=audio/ogg' \
* -F 'file=@audio.wav; type=audio/wav' \
* -F 'file=@video.mp4; type=video/mpeg' \
* -F 'file=@video.wmv; type=video/wmv' \
* -F 'file=@video.mov; type=video/mov' \

### Response
```
{
 'detect_language': 'zh',
 'language_probability': 1.0,
 'new_result': "
    [  0.00s ->   2.00s]  The driver just turned left from the gate of the driving school. 
    ...
    \n[113.00s -> 116.00s]  Apple Action News \n"
}
```

## Errors
### UNSUPPORTED Audio / Video
```json
HTTP/1.1 400

{"result": "UNSUPPORTED_AUDIO_FORMAT"}
```

### UNSUPPORTED TASK
```json
HTTP/1.1 400

{"result": "UNSUPPORTED_TASK_ERROR"}
```

### UNSUPPORTED LANGUAGE
```json
HTTP/1.1 400

{"result": "UNSUPPORTED_LANGUAGE_ERROR"}
```

### UNSUPPORTED OUTPUT FORMAT
```json
HTTP/1.1 400

{"result": "UNSUPPORTED_OUTPUT_FORMAT"}
```

### INTERNAL_ERROR LANGUAGE
```json
HTTP/1.1 500

{"result": "INTERNAL_ERROR"}
```

# Client send request demo code
## JavaScript
POST
```javascript
    const formData = new FormData();
    formData.append('file', file);
    formData.append('task', 'transcribe');

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {console.log(data);})
```

## python
POST
```python
import requests

url = "http://0.0.0.0:8000/"

file_path = "audio.mp3"
task = "transcribe"

with open(file_path, "rb") as file:
    files = {"file": file}
    data = {"task": task}
    response = requests.post(url, files=files, data=data)

print(response.json())
```
