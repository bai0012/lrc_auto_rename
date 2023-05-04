import sys
import os
import glob
from pydub import AudioSegment
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QPlainTextEdit

class AudioSubtitleRenamer(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('lrc_auto_rename')

        layout = QVBoxLayout()

        self.info_text = QPlainTextEdit()
        self.info_text.setReadOnly(True)
        layout.addWidget(self.info_text)

        select_folder_btn = QPushButton('select folder')
        select_folder_btn.clicked.connect(self.select_folder)
        layout.addWidget(select_folder_btn)

        self.setLayout(layout)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, 'select folder')

        if folder_path:
            audio_files = self.get_audio_files(folder_path)
            subtitle_files = self.get_subtitle_files(folder_path)

            audio_files_durations = self.get_audio_files_durations(audio_files)
            subtitle_files_durations = self.get_subtitle_files_durations(subtitle_files)

            matches = self.match_durations(audio_files_durations, subtitle_files_durations)

            self.rename_files(matches)

            self.display_matches(matches)

    def get_audio_files(self, folder_path):
        audio_extensions = ('*.mp3', '*.wav', '*.flac')
        audio_files = []
        for ext in audio_extensions:
            audio_files.extend(glob.glob(os.path.join(folder_path, ext)))
        return audio_files

    def get_subtitle_files(self, folder_path):
        subtitle_extension = '*.lrc'
        return glob.glob(os.path.join(folder_path, subtitle_extension))

    def get_audio_files_durations(self, audio_files):
        durations = {}
        for audio_file in audio_files:
            audio = AudioSegment.from_file(audio_file)
            durations[audio_file] = audio.duration_seconds
        return durations

    def get_subtitle_files_durations(self, subtitle_files):
        durations = {}
        for subtitle_file in subtitle_files:
            duration = self.get_duration_from_subtitle_file(subtitle_file)
            durations[subtitle_file] = duration
        return durations

    def get_duration_from_subtitle_file(self, subtitle_file):
        with open(subtitle_file, 'r', encoding='utf-8') as f:
            content = f.readlines()
            last_timestamp = content[-1].split(']')[0][1:]
            minutes, seconds = map(float, last_timestamp.split(':'))
            return minutes * 60 + seconds

    def match_durations(self, audio_files_durations, subtitle_files_durations):
        audio_sorted = sorted(audio_files_durations.items(), key=lambda x: x[1])
        subtitle_sorted = sorted(subtitle_files_durations.items(), key=lambda x: x[1])

        return list(zip(audio_sorted, subtitle_sorted))

    def rename_files(self, matches):
        for (audio_file, _), (subtitle_file, _) in matches:
            new_subtitle_name = os.path.splitext(audio_file)[0] + '.lrc'
            os.rename(subtitle_file, new_subtitle_name)

    def display_matches(self, matches):
        self.info_text.clear()
        for (audio_file, audio_duration), (subtitle_file, subtitle_duration) in matches:
            new_subtitle_name = os.path.splitext(audio_file)[0] + '.lrc'
            result = f"{os.path.basename(subtitle_file)} ({subtitle_duration:.2f}s) -> {os.path.basename(new_subtitle_name)} ({audio_duration:.2f}s)"
            self.info_text.appendPlainText(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = AudioSubtitleRenamer()
    widget.show()
    sys.exit(app.exec_())