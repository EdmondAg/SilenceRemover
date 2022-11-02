from wave_file_manager import *
import matplotlib.pyplot as plt

SILENCE_THRESHOLD = 50
GLITCH_MAX_LEN = int(441 * 0.6)  # 6 ms |||||| 1 ms = 44100 / 1000
SILENCE_MIN_LEN = 4410 * 4  # 400 ms
MARGIN_START = 4410
MARGIN_END = 4410


def normalize_sample(sample, max_value):
    # On couvre tous les cas, meme s'il n'y a que des samples negatif
    max_sample = max(abs(max(sample)), abs(min(sample)))

    rapport = max_value / max_sample

    # On return une liste normalisé.
    return [e * rapport for e in sample]


def get_silence_points(samples, threshold, glitch_max_len, silence_min_len, margin_start, margin_end):
    points = []
    in_silence_zone = False
    chunk_count = 0
    chunk_len = 441  # 441 samples  = 10 ms  ; 1 second = 1000 ms
    start = 0

    if margin_start + margin_end >= silence_min_len:
        print("Error, margin sum bigger than silence length.")
        return None

    for i in range(len(samples)):
        s = abs(samples[i])
        if not in_silence_zone:
            if s <= threshold:
                if chunk_count == 0:
                    start = i
                chunk_count += 1
                if chunk_count >= chunk_len:
                    in_silence_zone = True


            else:
                chunk_count = 0
        else:
            if s > threshold:
                in_silence_zone = False
                #  GLITCH_MAX_LEN = int(441 * 0.6)
                if len(points) > 0 and start - points[-1][1] <= glitch_max_len:
                    points[-1] = (points[-1][0], i)
                else:
                    points.append((start, i))

    # SILENCE_MIN_LEN = 4410 * 4  # 400 ms
    points = [(point[0] + margin_start, point[1] - margin_end) for point in points
              if point[1] - point[0] >= silence_min_len]

    return points


#filename = "test_glitch.wav"
filename = "test1.wav"


wav_samples = wave_file_read_samples(filename)
if wav_samples is None:
    print("ERREUR: Aucun sample à la lecture du fichier wav")
    exit(0)

wav_samples_norm = normalize_sample(wav_samples, 1000)

silence_points = get_silence_points(wav_samples_norm, SILENCE_THRESHOLD, GLITCH_MAX_LEN,
                                    SILENCE_MIN_LEN, MARGIN_START, MARGIN_END)
print(silence_points)


def delete_silence_pointes(samples, silence_points):
    outsample = []

    start = 0
    for p in silence_points:
        if p[0] > start:
            outsample += samples[:p[0]]
            start = p[1]

        if start < len(samples)-1:
            outsample += samples[start:]
    return outsample


wav_samples_without_silence = delete_silence_pointes(wav_samples, silence_points)

inserttxt = "_OUT"
# Trouver l'index du premier point:
idx = filename.index(".")
# Cree une variable qui est formé du filename jusqu'a index-1 du "." + inserttxt et la partie restante du filename
outputFilename = filename[:idx] + inserttxt + filename[idx:]

wave_file_write_samples(outputFilename, wav_samples_without_silence)

plt.plot(wav_samples_norm)
plt.axhline(y=SILENCE_THRESHOLD, color='r')
for p in silence_points:
    plt.axvline(x=p[0], color='r')
    plt.axvline(x=p[1], color='y')

plt.show()

