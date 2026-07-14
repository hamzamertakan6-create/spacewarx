"""
Procedural sound effects for SpaceWarx (100% synthesized, royalty-free).
"""
import numpy as np
import wave
import os

OUT = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(OUT, exist_ok=True)
SR = 22050


def env(n, a=0.01, d=0.05, s=0.3, r=0.1):
    a_n, d_n, r_n = int(n * a * n / n or 1), int(n * d), int(n * r)
    a_n = max(1, int(n * a))
    d_n = max(1, int(n * d))
    r_n = max(1, int(n * r))
    s_n = max(0, n - a_n - d_n - r_n)
    e = np.concatenate([
        np.linspace(0, 1, a_n),
        np.linspace(1, s, d_n),
        np.full(s_n, s),
        np.linspace(s, 0, r_n),
    ])
    if len(e) < n:
        e = np.pad(e, (0, n - len(e)))
    return e[:n]


def save_wav(name, data, vol=1.0):
    data = np.clip(data * vol, -1, 1)
    pcm = (data * 32767).astype(np.int16)
    path = os.path.join(OUT, name)
    with wave.open(path, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(pcm.tobytes())
    print(f"saved {name} ({len(data)/SR:.2f}s)")


def sweep(f_start, f_end, dur, wave_type="square", curve="linear"):
    n = int(SR * dur)
    t = np.linspace(0, dur, n, endpoint=False)
    if curve == "exp":
        freq = f_start * (f_end / f_start) ** (t / dur)
    else:
        freq = np.linspace(f_start, f_end, n)
    phase = 2 * np.pi * np.cumsum(freq) / SR
    if wave_type == "square":
        w = np.sign(np.sin(phase))
    elif wave_type == "triangle":
        w = 2 * np.abs(2 * ((np.cumsum(freq) / SR) % 1) - 1) - 1
    else:
        w = np.sin(phase)
    return w


def noise_burst(dur, lowpass_strength=0.0):
    n = int(SR * dur)
    w = np.random.uniform(-1, 1, n)
    if lowpass_strength > 0:
        k = max(1, int(lowpass_strength))
        kernel = np.ones(k) / k
        w = np.convolve(w, kernel, mode="same")
    return w


# ---------------- SFX ----------------

# player laser shot: quick bright downward square blip
def sfx_shoot():
    dur = 0.11
    w = sweep(1100, 500, dur, "square")
    e = env(len(w), 0.01, 0.1, 0.3, 0.5)
    return w * e


# enemy laser shot: slightly lower/rougher
def sfx_enemy_shoot():
    dur = 0.12
    w = sweep(650, 300, dur, "square")
    e = env(len(w), 0.01, 0.1, 0.3, 0.5)
    return w * e * 0.8


# explosion: filtered noise burst with pitch-drop thump
def sfx_explosion():
    dur = 0.4
    noise = noise_burst(dur, lowpass_strength=6)
    thump = sweep(160, 40, dur, "sine")
    e1 = env(len(noise), 0.005, 0.15, 0.25, 0.6)
    e2 = env(len(thump), 0.005, 0.2, 0.3, 0.5)
    return noise * e1 * 0.8 + thump * e2 * 0.6


# player hit / damage taken
def sfx_hit():
    dur = 0.18
    noise = noise_burst(dur, lowpass_strength=3)
    thump = sweep(220, 90, dur, "triangle")
    e = env(len(noise), 0.005, 0.1, 0.2, 0.5)
    return noise * e * 0.5 + thump * e * 0.5


# pickup (coin/diamond): bright ascending twinkle
def sfx_pickup():
    dur = 0.18
    w = sweep(700, 1500, dur, "square")
    e = env(len(w), 0.01, 0.08, 0.4, 0.4)
    return w * e * 0.6


# ability activation: shimmering rising sweep
def sfx_ability():
    dur = 0.35
    w1 = sweep(300, 1000, dur, "triangle")
    w2 = sweep(450, 1300, dur, "sine")
    e = env(len(w1), 0.02, 0.15, 0.5, 0.5)
    return (w1 * 0.5 + w2 * 0.5) * e * 0.6


# boss entrance alarm: descending/ascending siren wobble
def sfx_boss_alarm():
    dur = 1.2
    n = int(SR * dur)
    t = np.linspace(0, dur, n, endpoint=False)
    wobble = 500 + 220 * np.sin(2 * np.pi * 3.2 * t)
    phase = 2 * np.pi * np.cumsum(wobble) / SR
    w = np.sign(np.sin(phase))
    e = env(n, 0.05, 0.1, 0.8, 0.15)
    return w * e * 0.55


# boss special attack: deep dramatic burst
def sfx_boss_attack():
    dur = 0.5
    noise = noise_burst(dur, lowpass_strength=8)
    boom = sweep(200, 60, dur, "sine")
    e1 = env(len(noise), 0.01, 0.2, 0.3, 0.5)
    e2 = env(len(boom), 0.01, 0.25, 0.4, 0.4)
    return noise * e1 * 0.55 + boom * e2 * 0.7


# level complete: short bright victory jingle
def sfx_level_complete():
    notes_hz = [523.25, 659.25, 783.99, 1046.5]  # C5 E5 G5 C6
    dur_each = 0.16
    parts = []
    for f in notes_hz:
        w = sweep(f, f, dur_each, "square")
        e = env(len(w), 0.02, 0.05, 0.6, 0.4)
        parts.append(w * e * 0.5)
    return np.concatenate(parts)


# game over: short descending sad jingle
def sfx_game_over():
    notes_hz = [440.0, 392.0, 349.23, 293.66]  # A4 G4 F4 D4
    dur_each = 0.22
    parts = []
    for f in notes_hz:
        w = sweep(f, f * 0.97, dur_each, "triangle")
        e = env(len(w), 0.02, 0.1, 0.5, 0.5)
        parts.append(w * e * 0.5)
    return np.concatenate(parts)


if __name__ == "__main__":
    save_wav("sfx_shoot.wav", sfx_shoot())
    save_wav("sfx_enemy_shoot.wav", sfx_enemy_shoot())
    save_wav("sfx_explosion.wav", sfx_explosion())
    save_wav("sfx_hit.wav", sfx_hit())
    save_wav("sfx_pickup.wav", sfx_pickup())
    save_wav("sfx_ability.wav", sfx_ability())
    save_wav("sfx_boss_alarm.wav", sfx_boss_alarm())
    save_wav("sfx_boss_attack.wav", sfx_boss_attack())
    save_wav("sfx_level_complete.wav", sfx_level_complete())
    save_wav("sfx_game_over.wav", sfx_game_over())
    print("SFX generation done.")
