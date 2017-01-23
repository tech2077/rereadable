from kivy.app import App
from kivy.uix.widget import Widget
import re
import csv

keywords_re = []
with open('quantities.csv', 'r') as f:
    r = csv.reader(f)
    for row in r:
        words = '(' + '|'.join(row[1:] + [w.title() for w in row[1:]]) + ')'
        color = row[0]
        print(words)
        keywords_re.append((color, words))

print(keywords_re)

fix_period = re.compile(u"([a-z0-9 ]{2,})\.[) \n]+([A-Z\(])")
unitnum_re = re.compile(u"([0-9]+[\.]?[0-9]*)([ -_]?)([\w//]*)")


def wrap_color(text, color):
    return r"[color={}]{}[/color]".format(color, text)


class ReReadableRoot(Widget):
    def highlight_text(self, text):
        result = ''.join([x for x in text])
        result.replace('\n', ' ')

        result = fix_period.sub(r"\1.\n\n\2", result)
        result = unitnum_re.sub(
            r"[color=cf0a2b]\1[/color]\2[color=0000ff]\3[/color]", result)
        for sub in keywords_re:
            result = re.compile(sub[1]).sub(wrap_color(r'\1', sub[0]), result)
        # print(text, result)
        return result


class ReReadableApp(App):
    def build(self):
        return ReReadableRoot()


if __name__ == '__main__':
    ReReadableApp().run()
