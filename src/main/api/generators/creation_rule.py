from dataclasses import dataclass

"""Файл creation_rule.py — это «инструкция» (правило) для генератора случайных данных. 
Он говорит генератору: «Когда будешь создавать значение для этого поля, 
сгенерируй его вот по такому регулярному выражению»."""

@dataclass
class CreationRule:
    regex: str