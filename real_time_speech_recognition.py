import pyaudio
import subprocess
import numpy as np
import whisper

def trans_format(frame: bytes):
    """
    原本 whisper.audio 裡的 load_audio 函式進行修改
    ----------
    frame: byte
        錄音後儲存的格式

    Returns
    -------
    A NumPy array containing the audio waveform, in float32 dtype.
    """
    # 轉換音訊格式
    cmd = [
        "ffmpeg", "-nostdin", "-f", "s16le", "-acodec", "pcm_s16le", "-ac", "1", "-ar", str(RATE), "-i", "-",
        "-f", "s16le", "-acodec", "pcm_s16le", "-ac", "1", "-ar", str(RATE), "-"
    ]
    process = subprocess.Popen(cmd, 
                            stdin=subprocess.PIPE, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.DEVNULL)
    out, err = process.communicate(frame)
    # 檢查轉換是否成功
    # if process.returncode != 0:
    #     print("錯誤：" + err.decode("utf-8"))
    # else:
    #     # 使用out
    #     print("音訊轉換成功")
    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

def speech2text(audio: np.array):
    result = model.transcribe(audio)#, **transcribe_options, verbose=False)
    print(result['text'])


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 30 # 設定要錄幾秒

model = whisper.load_model('medium')
# 初始化錄音
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
# 錄音
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

    if (i+1)%20==0:
        audio = trans_format(b"".join(frames))
        speech2text(audio)
        frames = []

# 停止錄音
stream.stop_stream()
stream.close()
p.terminate()
