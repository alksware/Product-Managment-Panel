from PyQt5 import uic

with open("projectUI.py", "w", encoding="UTF-8") as fout:
    uic.compileUi("project.ui",fout)