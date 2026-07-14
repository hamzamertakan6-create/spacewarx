"""
Procedural chiptune-style music generator for SpaceWarx.
100% original / royalty-free since it's synthesized from scratch (no samples).
Produces: assets/music_menu.wav (calm ambient loop)
          assets/music_game.wav  (slightly more driving, still relaxing loop)
"""
import numpy as np
import wave
import os

OUT = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(OUT, exist_ok=True)
SR = 22050

NOTE_FREQ = {}
_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
for octave in range(1, 7):
    for i, n in enumerate(_names):
        NOTE_FREQ[f"{n}{octave}"] = 440.0 * 2 ** ((octave - 4) + (i - 9) / 12)


def env_adsr(n, a=0.05, d=0.1, s=0.7, r=0.2):
    a_n, d_n, r_n = int(n * a), int(n * d), int(n * r)
    s_n = max(0, n - a_n - d_n - r_n)
    env = np.concatenate([
        np.linspace(0, 1, max(a_n, 1)),
        np.linspace(1, s, max(d_n, 1)),
        np.full(max(s_n, 1), s),
        np.linspace(s, 0, max(r_n, 1)),
    ])
    if len(env) < n:
        env = np.pad(env, (0, n - len(env)))
    return env[:n]


def tone(freq, dur, wave_type="triangle", vol=0.2, adsr=(0.05, 0.1, 0.7, 0.2)):
    n = int(SR * dur)
    t = np.linspace(0, dur, n, endpoint=False)
    if wave_type == "sine":
        w = np.sin(2 * np.pi * freq * t)
    elif wave_type == "square":
        w = np.sign(np.sin(2 * np.pi * freq * t))
    elif wave_type == "triangle":
        w = 2 * np.abs(2 * ((t * freq) % 1) - 1) - 1
    else:
        w = np.sin(2 * np.pi * freq * t)
    env = env_adsr(n, *adsr)
    return (w * env * vol).astype(np.float64)


def silence(dur):
    return np.zeros(int(SR * dur))


def mix(*tracks):
    maxlen = max(len(t) for t in tracks)
    out = np.zeros(maxlen)
    for t in tracks:
        out[:len(t)] += t
    peak = np.max(np.abs(out))
    if peak > 0.95:
        out = out / peak * 0.9
    return out


def save_wav(name, data):
    data = np.clip(data, -1, 1)
    pcm = (data * 32767).astype(np.int16)
    path = os.path.join(OUT, name)
    with wave.open(path, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(pcm.tobytes())
    print(f"saved {name} ({len(data)/SR:.1f}s)")


def sequence(notes_durs, wave_type="triangle", vol=0.2, adsr=(0.05, 0.1, 0.7, 0.2)):
    """notes_durs: list of (note_name_or_None, duration_seconds)"""
    parts = []
    for note, dur in notes_durs:
        if note is None:
            parts.append(silence(dur))
        else:
            parts.append(tone(NOTE_FREQ[note], dur, wave_type, vol, adsr))
    return np.concatenate(parts)


# =================================================================
# MENU THEME: calm ambient pad + gentle arpeggio (relaxing space vibe)
# Chords: Am7 - Fmaj7 - Cmaj7 - G   (4 bars, each 4s = 16s loop)
# =================================================================
def build_menu_theme():
    bar = 4.0

    def pad_chord(notes, dur):
        return mix(*[tone(NOTE_FREQ[n], dur, "sine", vol=0.09,
                           adsr=(0.6, 0.3, 0.8, 0.8)) for n in notes])

    chords = [
        (["A3", "C4", "E4", "G4"], bar),
        (["F3", "A3", "C4", "E4"], bar),
        (["C3", "E3", "G3", "B3"], bar),
        (["G3", "B3", "D4", "F4"], bar),
    ]
    pad_track = np.concatenate([pad_chord(c, d) for c, d in chords])

    arp_notes = [
        "A4", "C5", "E4", "C5", "F4", "A4", "C5", "A4",
        "C4", "E4", "G4", "E4", "G4", "B4", "D5", "B4",
    ]
    step = bar * 4 / len(arp_notes)
    arp_track = sequence([(n, step) for n in arp_notes], "triangle", vol=0.1,
                          adsr=(0.02, 0.05, 0.4, 0.15))

    bass_notes = ["A2", None, "F2", None, "C2", None, "G2", None]
    step_b = bar * 4 / len(bass_notes)
    bass_track = sequence([(n, step_b) for n in bass_notes], "sine", vol=0.14,
                           adsr=(0.02, 0.1, 0.6, 0.3))

    return mix(pad_track, arp_track, bass_track)


# =================================================================
# GAMEPLAY THEME: a bit more rhythmic/driving but still chill
# Chords: Dm7 - Am7 - Fmaj7 - C  (steady pulse, soft percussion)
# =================================================================
def kick(vol=0.25):
    n = int(SR * 0.12)
    t = np.linspace(0, 0.12, n, endpoint=False)
    freq = np.linspace(120, 40, n)
    w = np.sin(2 * np.pi * np.cumsum(freq) / SR)
    env = env_adsr(n, 0.005, 0.05, 0.2, 0.3)
    return w * env * vol


def hat(vol=0.06):
    n = int(SR * 0.05)
    w = np.random.uniform(-1, 1, n)
    env = env_adsr(n, 0.001, 0.02, 0.1, 0.2)
    return w * env * vol


def build_game_theme():
    bar = 3.2
    beat = bar / 8

    def pad_chord(notes, dur):
        return mix(*[tone(NOTE_FREQ[n], dur, "sine", vol=0.08,
                           adsr=(0.3, 0.2, 0.8, 0.5)) for n in notes])

    chords = [
        (["D3", "F3", "A3", "C4"], bar),
        (["A2", "C3", "E3", "G3"], bar),
        (["F2", "A2", "C3", "E3"], bar),
        (["C3", "E3", "G3", "B3"], bar),
    ]
    pad_track = np.concatenate([pad_chord(c, d) for c, d in chords])

    arp_notes = ["D4", "F4", "A4", "F4"] * 2 + ["A3", "C4", "E4", "C4"] * 2 + \
                ["F3", "A3", "C4", "A3"] * 2 + ["C4", "E4", "G4", "E4"] * 2
    arp_track = sequence([(n, beat) for n in arp_notes], "square", vol=0.055,
                          adsr=(0.01, 0.03, 0.3, 0.1))

    bass_notes = ["D2", None, "D2", None, "A1", None, "A1", None,
                  "F1", None, "F1", None, "C2", None, "C2", None]
    bass_track = sequence([(n, beat) for n in bass_notes], "triangle", vol=0.16,
                           adsr=(0.01, 0.05, 0.6, 0.15))

    total_beats = int((bar * 4) / beat)
    perc_parts = []
    for i in range(total_beats):
        seg = silence(beat)
        if i % 4 == 0:
            k = kick()
            seg[:len(k)] += k
        if i % 2 == 1:
            h = hat()
            seg[:len(h)] += h
        perc_parts.append(seg)
    perc_track = np.concatenate(perc_parts)

    return mix(pad_track, arp_track, bass_track, perc_track)


# =================================================================
# MENU THEME variant 2: different progression, slightly brighter mood
# Chords: Cmaj7 - Em7 - Fmaj7 - Dm7  (16s loop)
# =================================================================
def build_menu_theme_variant():
    bar = 4.0

    def pad_chord(notes, dur):
        return mix(*[tone(NOTE_FREQ[n], dur, "sine", vol=0.09,
                           adsr=(0.6, 0.3, 0.8, 0.8)) for n in notes])

    chords = [
        (["C4", "E4", "G4", "B4"], bar),
        (["E3", "G3", "B3", "D4"], bar),
        (["F3", "A3", "C4", "E4"], bar),
        (["D3", "F3", "A3", "C4"], bar),
    ]
    pad_track = np.concatenate([pad_chord(c, d) for c, d in chords])

    arp_notes = [
        "G4", "C5", "E4", "C5", "B4", "D5", "G4", "B4",
        "A4", "C5", "E4", "C5", "F4", "A4", "D5", "A4",
    ]
    step = bar * 4 / len(arp_notes)
    arp_track = sequence([(n, step) for n in arp_notes], "triangle", vol=0.1,
                          adsr=(0.02, 0.05, 0.4, 0.15))

    bass_notes = ["C2", None, "E2", None, "F2", None, "D2", None]
    step_b = bar * 4 / len(bass_notes)
    bass_track = sequence([(n, step_b) for n in bass_notes], "sine", vol=0.14,
                           adsr=(0.02, 0.1, 0.6, 0.3))

    return mix(pad_track, arp_track, bass_track)


# =================================================================
# GAMEPLAY THEME variant 2: slightly different groove/progression
# Chords: Em7 - C - G - D  (steady pulse)
# =================================================================
def build_game_theme_variant():
    bar = 3.2
    beat = bar / 8

    def pad_chord(notes, dur):
        return mix(*[tone(NOTE_FREQ[n], dur, "sine", vol=0.08,
                           adsr=(0.3, 0.2, 0.8, 0.5)) for n in notes])

    chords = [
        (["E3", "G3", "B3", "D4"], bar),
        (["C3", "E3", "G3", "B3"], bar),
        (["G2", "B2", "D3", "F3"], bar),
        (["D3", "F3", "A3", "C4"], bar),
    ]
    pad_track = np.concatenate([pad_chord(c, d) for c, d in chords])

    arp_notes = ["E4", "G4", "B4", "G4"] * 2 + ["C4", "E4", "G4", "E4"] * 2 + \
                ["G3", "B3", "D4", "B3"] * 2 + ["D4", "F4", "A4", "F4"] * 2
    arp_track = sequence([(n, beat) for n in arp_notes], "square", vol=0.055,
                          adsr=(0.01, 0.03, 0.3, 0.1))

    bass_notes = ["E2", None, "E2", None, "C2", None, "C2", None,
                  "G1", None, "G1", None, "D2", None, "D2", None]
    bass_track = sequence([(n, beat) for n in bass_notes], "triangle", vol=0.16,
                           adsr=(0.01, 0.05, 0.6, 0.15))

    total_beats = int((bar * 4) / beat)
    perc_parts = []
    for i in range(total_beats):
        seg = silence(beat)
        if i % 4 == 0:
            seg[:len(kick())] += kick()
        if i % 2 == 1:
            seg[:len(hat())] += hat()
        perc_parts.append(seg)
    perc_track = np.concatenate(perc_parts)

    return mix(pad_track, arp_track, bass_track, perc_track)


# =================================================================
# MENU THEME variant 3: lo-fi/dreamy mood, slow arpeggio
# Chords: Fmaj7 - Am7 - Dm7 - G7  (16s loop)
# =================================================================
def build_menu_theme_variant3():
    bar = 4.0

    def pad_chord(notes, dur):
        return mix(*[tone(NOTE_FREQ[n], dur, "sine", vol=0.085,
                           adsr=(0.7, 0.3, 0.8, 0.9)) for n in notes])

    chords = [
        (["F3", "A3", "C4", "E4"], bar),
        (["A2", "C3", "E3", "G3"], bar),
        (["D3", "F3", "A3", "C4"], bar),
        (["G2", "B2", "D3", "F3"], bar),
    ]
    pad_track = np.concatenate([pad_chord(c, d) for c, d in chords])

    arp_notes = [
        "F4", "A4", "C5", "A4", "E4", "G4", "C5", "G4",
        "D4", "F4", "A4", "F4", "G4", "B4", "D5", "B4",
    ]
    step = bar * 4 / len(arp_notes)
    arp_track = sequence([(n, step) for n in arp_notes], "sine", vol=0.095,
                          adsr=(0.05, 0.08, 0.5, 0.25))

    bass_notes = ["F2", None, "A1", None, "D2", None, "G1", None]
    step_b = bar * 4 / len(bass_notes)
    bass_track = sequence([(n, step_b) for n in bass_notes], "triangle", vol=0.13,
                           adsr=(0.03, 0.1, 0.6, 0.35))

    return mix(pad_track, arp_track, bass_track)


# =================================================================
# GAMEPLAY THEME variant 3: upbeat, brighter major-key energy
# Chords: G - D - Em - C  (steady pulse)
# =================================================================
def build_game_theme_variant3():
    bar = 3.0
    beat = bar / 8

    def pad_chord(notes, dur):
        return mix(*[tone(NOTE_FREQ[n], dur, "sine", vol=0.08,
                           adsr=(0.25, 0.15, 0.8, 0.4)) for n in notes])

    chords = [
        (["G3", "B3", "D4"], bar),
        (["D3", "F#3", "A3"], bar),
        (["E3", "G3", "B3"], bar),
        (["C3", "E3", "G3"], bar),
    ]
    pad_track = np.concatenate([pad_chord(c, d) for c, d in chords])

    arp_notes = ["G4", "B4", "D5", "B4"] * 2 + ["D4", "F#4", "A4", "F#4"] * 2 + \
                ["E4", "G4", "B4", "G4"] * 2 + ["C4", "E4", "G4", "E4"] * 2
    arp_track = sequence([(n, beat) for n in arp_notes], "square", vol=0.06,
                          adsr=(0.01, 0.03, 0.3, 0.1))

    bass_notes = ["G2", None, "G2", None, "D2", None, "D2", None,
                  "E2", None, "E2", None, "C2", None, "C2", None]
    bass_track = sequence([(n, beat) for n in bass_notes], "triangle", vol=0.15,
                           adsr=(0.01, 0.05, 0.6, 0.15))

    total_beats = int((bar * 4) / beat)
    perc_parts = []
    for i in range(total_beats):
        seg = silence(beat)
        if i % 4 == 0:
            seg[:len(kick())] += kick()
        if i % 2 == 1:
            seg[:len(hat())] += hat()
        perc_parts.append(seg)
    perc_track = np.concatenate(perc_parts)

    return mix(pad_track, arp_track, bass_track, perc_track)
# Chords: Dm - Dm - Bb - A  (tense, urgent, 2.4s bars)
# =================================================================
def build_boss_theme():
    bar = 2.4
    beat = bar / 8

    def pad_chord(notes, dur):
        return mix(*[tone(NOTE_FREQ[n], dur, "sine", vol=0.1,
                           adsr=(0.05, 0.1, 0.85, 0.2)) for n in notes])

    chords = [
        (["D3", "F3", "A3"], bar),
        (["D3", "F3", "A3"], bar),
        (["A#2", "D3", "F3"], bar),
        (["A2", "C#3", "E3"], bar),
    ]
    pad_track = np.concatenate([pad_chord(c, d) for c, d in chords])

    lead_notes = ["D4", "F4", "D4", "A4", "F4", "D4", "A3", "D4"] * 2 + \
                 ["A#3", "D4", "A#3", "F4", "D4", "A#3", "G3", "A#3"] * 2
    lead_track = sequence([(n, beat) for n in lead_notes], "square", vol=0.075,
                           adsr=(0.005, 0.02, 0.4, 0.08))

    bass_notes = (["D2", "D2", "D2", None] * 2 + ["A#1", "A#1", "A#1", None] * 1 +
                  ["A1", "A1", "A1", None] * 1)
    bass_track = sequence([(n, beat) for n in bass_notes], "triangle", vol=0.2,
                           adsr=(0.005, 0.03, 0.7, 0.1))

    total_beats = int((bar * 4) / beat)
    perc_parts = []
    for i in range(total_beats):
        seg = silence(beat)
        if i % 2 == 0:
            k = kick(vol=0.3)
            seg[:len(k)] += k
        seg[:len(hat(vol=0.05))] += hat(vol=0.05)
        perc_parts.append(seg)
    perc_track = np.concatenate(perc_parts)

    return mix(pad_track, lead_track, bass_track, perc_track)


if __name__ == "__main__":
    save_wav("music_menu.wav", build_menu_theme())
    save_wav("music_game.wav", build_game_theme())
    save_wav("music_menu2.wav", build_menu_theme_variant())
    save_wav("music_game2.wav", build_game_theme_variant())
    save_wav("music_menu3.wav", build_menu_theme_variant3())
    save_wav("music_game3.wav", build_game_theme_variant3())
    save_wav("music_boss.wav", build_boss_theme())
    print("Music generation done.")
