import os
import speech_recognition as sr
from google.cloud import speech

class GoogleSpeech:
  def __init__():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'creds/API-Project-c7afe5505e44.json'

  def listenTranscribe(self):
    audio = self.getAudio()
    return self.transcribeAudio(audio)

  def getAudio(self):
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    print("Got some audio!")
    print(audio)
    return audio
  
  def transcribeAudio(self,audio):
    # Instantiates a client
    print("MAKING SPEECH CLIENT")
    speech_client = speech.Client()

    print("getting audio sample")
    audio_sample = speech_client.sample(
        audio.get_raw_data(),
        source_uri=None,
        encoding='LINEAR16',
        sample_rate=44100)


    # Detects speech in the audio file
    alternatives = speech_client.speech_api.sync_recognize(audio_sample)

    for alternative in alternatives:
      print('Transcript: {}'.format(alternative.transcript))
    
    return alternatives
    
# GoogleSpeech().listenTranscribe()