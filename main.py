from wave_file_manager import wave_file_read_samples, wave_file_write_samples
from exclude_silence_processing import get_samples_without_silences
import sys
from os import path
from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window

Window.size = (400, 300)

# print("arguments", sys.argv)

def check_input_file(filename):
    if len(filename) < 5:
        return "Nom du fichier invalide"

    input_split = filename.split(".")
    if input_split == 1:
        return "Le fichier n'a pas d'extension"

    if input_split[-1].lower() != "wav":
        return "Uniquement les fichiers wav sont supportés"

    if not path.exists(filename):
        return "Le fichier d'entrée n'existe pas"

    return None

'''if len(sys.argv) < 2:
    print("Vous devez donner un nom de fichier Wav à ouvrir")
    exit(0)

input_filename = sys.argv[1]

input_filename_error = check_input_file(input_filename)
if input_filename_error:
    print("ERREUR:", input_filename_error)
    exit(0)

print("Fichier d'entrée:", input_filename)'''


# 1 - Lecture du fichier wav et récupération des samples
#input_filename = "test_anglais.wav"
'''wav_samples = wave_file_read_samples(input_filename)
if wav_samples == None:
    print("ERREUR: Aucun sample à la lecture du fichier wav")
    exit(0)

# 2 - Processing : algorithme pour supprimer les silences
wav_samples_without_silences = get_samples_without_silences(wav_samples)

# 3 - Ecriture du fichier wav de sortie
output_filename = input_filename[:-4] + "_OUT" + input_filename[-4:]
print("Fichier de sortie", output_filename)
wave_file_write_samples(output_filename, wav_samples_without_silences)'''


class SilenceRemoverApp(App):
    def build(self):
        Window.bind(on_dropfile=self._on_file_drop)
        self.message_label = Label(text='Déposez un fichier Wav')
        return self.message_label

    def _on_file_drop(self, window, file_path):
        input_filename = file_path.decode("utf-8")
        print(file_path)

        input_filename_error = check_input_file(input_filename)
        if input_filename_error:
            print("ERREUR:", input_filename_error)
            self.message_label.text = "ERREUR\n" + input_filename_error
            return

        wav_samples = wave_file_read_samples(input_filename)
        if wav_samples is None:
            self.message_label.text = "ERREUR\n" + "Aucun sample à la lecture du fichier wav"
            return

        # 2 - Processing : algorithme pour supprimer les silences
        wav_samples_without_silences = get_samples_without_silences(wav_samples)

        # 3 - Ecriture du fichier wav de sortie
        output_filename = input_filename[:-4] + "_OUT" + input_filename[-4:]
        print("Fichier de sortie", output_filename)

        output_filename_without_path = path.basename(output_filename)

        self.message_label.text = "FICHIER GÉNÉRÉ\n" + output_filename_without_path
        wave_file_write_samples(output_filename, wav_samples_without_silences)


SilenceRemoverApp().run()