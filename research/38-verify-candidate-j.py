import re

text = open('skill/document-design-intelligence/SKILL.md', encoding='utf-8').read()
m = re.search(r'description: "(.*)"\n', text)
desc = m.group(1)

old_lead = 'Creates and fixes print/office documents:'
new_lead = ('Use whenever the user asks for any of these documents to be written, '
            'drafted, made, structured or fixed, whether the answer is a chat reply or a file:')
triggers_full = ('Triggers: make me a CV, write a note interne, turn this into a brochure, '
                  'I need slides for Monday, format this report, fais-moi une fiche, '
                  'erstelle ein Angebot; ')
triggers_trim = 'Triggers: make me a CV, fais-moi une fiche, erstelle ein Angebot; '

assert desc.count(old_lead) == 1
assert desc.count(triggers_full) == 1

j = desc.replace(old_lead, new_lead).replace(triggers_full, triggers_trim)

assert 'lettre' in j
assert '"' not in j
assert chr(92) not in j
assert '\n' not in j

print('chars', len(j))
print('bytes', len(j.encode('utf-8')))
print('headroom chars', 1023 - len(j))
print()
print(j)
