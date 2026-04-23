"""
Docstring for game project
"""

import sys
import random
from wordfreq import top_n_list
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QWidget,
    QLineEdit,
)


class MainWindow(QMainWindow):
    """Main window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hangman game")
        self.setGeometry(700, 300, 500, 500)
        self.hbox = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.word_label = QLabel(self)
        self.word_line_edit = QLineEdit(self)
        self.regen_but = QPushButton("Reset word generation", self)
        self.new_word_but = QPushButton("New word", self)
        self.print_but = QPushButton("Print word", self)
        self.words = top_n_list("fi", 10000)
        self.fail_count = QLabel(self)
        self.score_label = QLabel(self)
        self.score = 0
        self.misses = 0
        self.used_letters = []
        self.answer = []
        self.init_ui()
        self.init_widgets()
        self.init_connections()
        self.reset_word()
        self.set_guess()

    def init_ui(self):
        """UI initialization function"""
        self.word_label.setStyleSheet("font-size: 40px;")
        self.word_line_edit.setStyleSheet("font-size: 30px;")
        self.fail_count.setStyleSheet("font-size: 25px")
        self.score_label.setStyleSheet("font-size: 25px;")

    def init_connections(self):
        """Widgets connections initialization function"""
        self.word_line_edit.returnPressed.connect(self.guess_letter)
        self.new_word_but.clicked.connect(self.set_guess)
        self.new_word_but.clicked.connect(self.reset_word)
        self.regen_but.clicked.connect(self.showed_letters)
        self.regen_but.clicked.connect(self.reset_word)
        self.print_but.clicked.connect(self.print_word)

    def init_widgets(self):
        """Widgets initialization function"""
        # Add main widgets to the vertical layout
        self.hbox.addWidget(self.word_label)
        self.vbox.addWidget(self.word_line_edit)
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.fail_count)
        self.vbox.addWidget(self.score_label)
        self.vbox.addWidget(self.print_but)
        self.vbox.addWidget(self.new_word_but)
        self.vbox.addWidget(self.regen_but)

        central_widget = QWidget()
        central_widget.setLayout(self.vbox)
        self.setCentralWidget(central_widget)

    # Functions
    def print_word(self):
        print(self.word, len(self.word))

    def reset_word(self):
        self.word_line_edit.setEnabled(True)
        self.word_line_edit.setFocus()
        self.word_label.setStyleSheet("font-size: 40px")
        self.word_label.setText(" ".join(self.answer))
        self.misses = 0
        self.fail_count.setText(f"Fail count: {self.misses}/4")
        self.score_label.setText(f"Guessed words:{self.score}")
        self.word_label.setText(" ".join(self.answer))

    def set_guess(self):
        self.word = random.choice(self.words)
        self.answer = ["_"] * len(self.word)
        self.showed_letters()
        self.word_label.setText(" ".join(self.answer))

    def showed_letters(self):
        self.answer = ["_"] * len(self.word)
        self.used_letters = []
        if len(self.word) > 2:
            string_list = list(self.word)
            print(string_list)
            random.shuffle(string_list)
            shuffled_string = "".join(string_list)
            candidate_letters = ""
            for letter in shuffled_string:
                if letter not in candidate_letters:
                    candidate_letters += letter
            if 2 <= len(self.word) <= 6:
                reveal = 1
            elif 7 <= len(self.word) <= 11:
                reveal = 2
            else:
                reveal = 3
            print(reveal)
            print(candidate_letters)
            for letter in candidate_letters:
                candidate_letter_count = self.word.count(letter)
                if reveal >= candidate_letter_count:
                    reveal -= candidate_letter_count
                    for i, l in enumerate(self.word):
                        if l == letter:
                            self.answer[i] = letter
                            if letter not in self.used_letters:
                                self.used_letters.append(letter)

    def guess_letter(self):
        user_letter = self.word_line_edit.text().lower().strip()
        found = False
        if not user_letter:
            return
        for i, letter in enumerate(self.word):
            if letter == user_letter:
                self.answer[i] = user_letter
                found = True
        self.word_line_edit.clear()
        if not found:
            if user_letter not in self.used_letters:
                self.misses += 1
                print(1)
        else:
            self.word_label.setText(" ".join(self.answer))
            if user_letter not in self.used_letters:
                if self.misses != 0:
                    self.misses -= 1
        if user_letter not in self.used_letters:
            self.used_letters.append(user_letter)
        self.fail_count.setText(f"Fail count: {self.misses}/4")
        if "_" not in self.answer:
            self.score += 1
            self.word_label.setStyleSheet("font-size: 30px")
            self.word_label.setText(f"You Won. The word was: {self.word}")
            self.score_label.setText(f"Guessed words:{self.score}")
        if self.misses == 4:
            self.word_line_edit.setEnabled(False)
            self.word_label.setStyleSheet("font-size: 30px")
            self.word_label.setText(f"You lost. The word was: {self.word}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    STYLE = """
    QPushButton {
    font-size: 15px
    }
    """
    app.setStyleSheet(STYLE)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
