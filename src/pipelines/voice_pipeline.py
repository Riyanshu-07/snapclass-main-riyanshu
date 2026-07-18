from resemblyzer import VoiceEncoder,preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st

@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()

def get_voice_embeddings(audio_bytes):
    try:
        encoder = load_voice_encoder()
        audio,sr = librosa.load(io.BytesIO(audio_bytes),sr=16000)
        wav = preprocess_wav(audio)
        embedding = encoder.embed_utterance(wav)
        return embedding.tolist()
    except Exception as e:
        st.error(f"Error processing audio: {e}")
        return None


def indentify_speaker(new_embedding, candidate_dict, threshold=0.65):
    if not candidate_dict or not new_embedding:
        return None, 0

    best_sid = None
    best_score = -1

    for sid,stored_embedding in candidate_dict.items():
        similarity = np.dot(new_embedding,stored_embedding)
        if similarity > best_score:
            best_score = similarity
            best_sid = sid

    if best_score >= threshold:
        return best_sid, best_score

    return None, best_score

# segment mai convert krengae big voice koe
def process_bulk_audio(audio_bytes,candidate_dict,threshold=0.65):
    try:
        encoder = load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        segements = librosa.effects.split(audio, top_db = 30)
        identified_results = {}
        for start,end in segements:

            if (end-start) < sr*0.5:  # joe garbage voice hogi usko skip kro
                continue
            segment_audio = audio[start:end]
            wav = preprocess_wav(segment_audio)
            embedding = encoder.embed_utterance(wav)

            sid,score = indentify_speaker(embedding,candidate_dict,threshold)
            if sid:
                if sid not in identified_results or score > identified_results[sid]:
                    identified_results[sid] = score

        return identified_results
    except Exception as e:
        st.error('bulk audio processing')
        return {}
