"""Synthetic smoke tests; run python test_repetition_check.py."""
from repetition_check import analyze
old='The empty chairs seemed to accuse him of arriving late to every important moment in his life. He set the box down beside the door and waited for an answer.'
assert analyze(old,[('001',old)])['screening']=='review_required'
assert any(x['kind']=='similar_paragraph' for x in analyze(old.replace('empty','folded'),[('001',old)])['findings'])
assert analyze('Nora checked the schedule and called the organizer.',[('001',old)])['screening']=='no_lexical_flags'
assert analyze('Draw a card. Draw a card.',[('001','Draw a card.')])['screening']=='no_lexical_flags'
assert analyze(old,[])['approved'] is False
print('5 synthetic tests passed')
