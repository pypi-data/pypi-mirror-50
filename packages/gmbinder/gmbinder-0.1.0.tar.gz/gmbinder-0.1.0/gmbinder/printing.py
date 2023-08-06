import os


# The U.S. Government Printing Office Style Manual
# via https://grammar.yourdictionary.com/capitalization/rules-for-capitalization-in-titles.html
no_caps = [
    'a', 'an', 'the', 'at', 'by', 'for',
    'in', 'of', 'on', 'to', 'up',
    'and', 'as', 'but', 'or', 'nor',
]


def sensible_caps(string, *, no_caps=no_caps, sep=' '):
    words = string.split()
    if len(words) <= 2:
            return ' '.join([w.title() for w in words])
    else:
        return sep.join(
                [words[0].title()] + 
                [w if w in no_caps else w.title() for w in words[1:-1]] +
                [words[-1].title()]
        )


def filename_to_title(filename):
    name, extension = os.path.splitext(os.path.basename(filename))
    name = name.replace('_',' ')
    return sensible_caps(name)


def column_print(rows, *, sep='  ', headers=None, bar_char='-'):
    if headers:
        iterable = (headers, *rows)
    else:
        iterable = rows

    column_widths = [max(len(v) for v in col) for col in zip(*iterable)]
    column_format = sep.join(f'{{:<{w}}}' for w in column_widths)

    print(column_format.format(*headers))
    print(column_format.format(*(bar_char*w for w in column_widths)))
    for row in rows:
        print(column_format.format(*row))