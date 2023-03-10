# whisper-real-time-speech-to-text-example
A simple example to implement real-time speech recognition using the Whisper speech 


## Requirements
This project requires the following Python packages:

- whisper
- pyaudio
- numpy

## Functionality
This example project demonstrates how to use the Whisper speech recognition model to perform real-time speech recognition. It captures audio input from the microphone using the puaudio package, and then feeds the audio stream into the Whisper model to transcribe the speech in real-time.

In addition, this example implements speech recognition on pre-recorded audio files, which are segmented into fixed-length segments before being fed into the Whisper model for transcription. The transcribed text for each segment is displayed in real-time on the console.
