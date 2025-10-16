# Consensual Key Capture

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green)
![Build Status](https://img.shields.io/badge/Status-Active-brightgreen)

Outil éthique Python pour capturer les frappes clavier avec consentement explicite. 
Idéal pour debug, exercice de dactylographie ou démonstration éducative. 
Aucun enregistrement furtif n’est réalisé.

---

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/BlueT0m/consensual-key-capture.git
```

---

## Usage

Run the project with:
```bash
python consensual_keylogger.py
```
Steps in the interface:

- Click Choose file to select where to save keystrokes.

- Click Start recording and confirm explicit consent.

- Type while the window is focused.

- Click Stop recording to finish and save.

---

## Features

- Captures keypresses only when window is focused.

- Requires explicit consent from user.

- Saves keystrokes to a user-selected file (append mode).

- Displays in-memory history in the interface (not automatically saved).

- Start/Stop/Clear buttons with timestamped entries.

---

## Contributing

1. Fork the repository.

2. Create a new branch: `git checkout -b feature-name.`

3. Make your changes.

4. Push your branch: `git push origin feature-name.`

5. Create a pull request.

---

## License
This project is licensed under the [MIT License](LICENSE).
