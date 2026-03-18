"""
Docstring for game project
"""

import random
from wordfreq import top_n_list

import sys
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
        self.new_letters_button = QPushButton("Reset word generation", self)
        self.reset_button = QPushButton("New word", self)
        self.print_button = QPushButton("Print word", self)
        self.words = top_n_list("en", 10000)
        self.fail_count = QLabel(self)
        self.init_ui()
        self.init_widgets()
        self.init_connections()
        self.set_guess()

    def init_ui(self):
        """UI initialization function"""
        self.word_label.setStyleSheet("font-size: 40px;")
        self.word_line_edit.setStyleSheet("font-size: 30px;")
        self.fail_count.setStyleSheet("font-size: 25px")

    def init_connections(self):
        """Widgets connections initialization function"""
        self.word_line_edit.returnPressed.connect(self.guess_letter)
        self.reset_button.clicked.connect(self.set_guess)
        self.print_button.clicked.connect(self.print_word)
        self.new_letters_button.clicked.connect(self.reset_word)

    def init_widgets(self):
        """Widgets initialization function"""
        # Add main widgets to the vertical layout
        self.hbox.addWidget(self.word_label)
        self.vbox.addWidget(self.word_line_edit)
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.fail_count)
        self.vbox.addWidget(self.print_button)
        self.vbox.addWidget(self.reset_button)
        self.vbox.addWidget(self.new_letters_button)

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
        self.word_label.clear()
        self.misses = 0
        self.fail_count.setText(f"Fail count: {self.misses}/4")
        self.showed_letters()

    def set_guess(self):
        self.word_line_edit.setEnabled(True)
        self.word_line_edit.setFocus()
        self.word_label.setStyleSheet("font-size: 40px")
        self.word_label.clear()
        self.misses = 0
        self.fail_count.setText(f"Fail count: {self.misses}/4")
        self.word = random.choice(self.words)
        self.showed_letters()

    def showed_letters(self):
        self.used_letters = []
        self.answer = ["_"] * len(self.word)
        if len(self.word) > 3:
            string_list = list(self.word)
            random.shuffle(string_list)
            shuffled_string = "".join(string_list)
            candidate_letters = ""
            for a in shuffled_string:
                if a not in candidate_letters:
                    candidate_letters += a
            if 3 <= len(self.word) <= 5:
                reveal = 1
            elif 6 <= len(self.word) <= 9:
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
        self.word_label.setText(" ".join(self.answer))

    def guess_letter(self):
        user_letter = self.word_line_edit.text()
        found = False
        if not user_letter:
            return
        for i, letter in enumerate(self.word):
            if letter == user_letter:
                self.answer[i] = user_letter
                found = True
        self.word_line_edit.clear()
        if not found:
            self.misses += 1
        else:
            self.word_label.setText(" ".join(self.answer))
            if user_letter not in self.used_letters:
                if self.misses != 0:
                    self.misses -= 1
        if user_letter not in self.used_letters:
            self.used_letters.append(user_letter)
        self.fail_count.setText(f"Fail count: {self.misses}/4")
        if "_" not in self.answer:
            self.word_label.setStyleSheet("font-size: 30px")
            self.word_label.setText(f"You Won. The word was: {self.word}")
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
