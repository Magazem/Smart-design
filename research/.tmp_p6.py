p = "designs-evidence/fill_family.py"
s = open(p, encoding="utf-8").read()

s = s.replace('''    defaults_row = default_reasoning_row(family)
''', '''    defaults_row = default_reasoning_row(family)
    # bias terms, Doc Conditions, Severity and default Anti-Pattern Tokens are copied from the family default's
    # reasoning row (section 8); a spec may still state them
    rdef = spec["reasoning"].get("defaults") or {c: (defaults_row or {}).get(c, "") for c in (
        "Style Bias Terms", "Palette Bias Terms", "Typeface Bias Terms", "Doc Conditions", "Severity")}
    tok_default = spec["reasoning"].get("anti_tokens", {}).get("default") or (defaults_row or {}).get("Anti-Pattern Tokens", "")
''', 1)
s = s.replace('blank_bias(spec["reasoning"]["defaults"], feats, tf)', 'blank_bias(rdef, feats, tf)')
s = s.replace('toks = spec["reasoning"]["anti_tokens"]["default"].split(";")', 'toks = tok_default.split(";")')
s = s.replace('            bias = spec["reasoning"]["defaults"]\n', '            bias = rdef\n')
s = s.replace('"Anti-Pattern Tokens": spec["reasoning"]["anti_tokens"]["default"],', '"Anti-Pattern Tokens": tok_default,')
s = s.replace('''VARIANT_ALIASES = {"rules_boxes": "rules boxes", "cover_page": "cover", "totals_position": "totals",''',
              '''VARIANT_ALIASES = {"rules_boxes": "rules boxes", "cover_page": "cover", "totals_position": "totals",
                   "letterhead_position": "letterhead",''')
open(p, "w", encoding="utf-8").write(s)
import ast
ast.parse(s)
print(s.count(chr(8)), s.count(chr(0)))
