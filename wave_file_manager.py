import wave

def get_bytes_sample_from_16bits_sample(sample_16bits):
    unsigned_sample = sample_16bits
    if sample_16bits < 0:
        unsigned_sample = sample_16bits + 65536
    byte_ms = unsigned_sample // 256
    byte_ls = unsigned_sample - byte_ms * 256
    return byte_ls, byte_ms


def get_bytes_samples_from_16bits_samples(samples_16bits):
    bytes = []
    for s in samples_16bits:
        ls, ms = get_bytes_sample_from_16bits_sample(s)
        bytes.append(ls)
        bytes.append(ms)
    return bytes


def get_16bits_sample_from_bytes(byte_ls, byte_ms):
    unsigned = byte_ls + byte_ms * 256
    signed = unsigned
    if unsigned > 32767:
        signed = unsigned - 65536
    return signed


def get_16bits_samples_from_bytes(bytes):
    samples = []
    for i in range(0, len(bytes) - 1, 2):
        sample = get_16bits_sample_from_bytes(bytes[i], bytes[i + 1])
        samples.append(sample)
    return samples


WAV_FORMAT_N_CHANNELS = 1
WAV_FORMAT_SAMPLE_WIDTH = 2
WAV_FORMAT_FRAMERATE = 44100


def wave_file_read_samples(filename):
    wr = wave.open(filename, mode="rb")
    if wr.getnchannels() != WAV_FORMAT_N_CHANNELS:
        print("ERREUR: Utilisez un fichier mono")
        return None
    if wr.getsampwidth() != WAV_FORMAT_SAMPLE_WIDTH:
        print("ERREUR: Utilisez le format 16bits")
        return None
    if wr.getframerate() != WAV_FORMAT_FRAMERATE:
        print("ERREUR: Utilisez 44100Hz")
        return None

    nframes = wr.getnframes()
    print("nframes", nframes)
    frames_as_bytes = wr.readframes(nframes)


    samples_16bits = get_16bits_samples_from_bytes(frames_as_bytes)

    wr.close()
    return samples_16bits


def wave_file_write_samples(filename, samples):
    ww = wave.open(filename, mode="wb")

    ww.setnchannels(WAV_FORMAT_N_CHANNELS)
    ww.setsampwidth(WAV_FORMAT_SAMPLE_WIDTH)
    ww.setframerate(WAV_FORMAT_FRAMERATE)

    ww.setnframes(len(samples))
    bytes = get_bytes_samples_from_16bits_samples(samples)
    ww.writeframesraw(bytearray(bytes))

    ww.close()
