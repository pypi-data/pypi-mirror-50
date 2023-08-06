def text_2_output(file_name, lang='Python', line_prefix='', line_suffix='', file_prefix='', file_suffix=''):
    lines = []
    lang_prefix = ''
    lang_suffix = ''
    lang = lang.lower()
    if 'python' in lang:
        if lang == 'python3' or 'python3' in lang.replace(' ', ''):
            lang_prefix = "print(r'"
            lang_suffix = " ')"
        elif lang == 'python2' or 'python2' in lang.replace(' ', ''):
            lang_prefix = "print r'"
            lang_suffix = " '"

    elif lang == 'c' or lang == 'c++' or lang == 'cpp':
        lang_prefix = 'printf("%s","'
        lang_suffix = r'\n");'

    elif lang == 'c#' or lang == 'csharp' or lang == 'cs':
        lang_prefix = 'Console.WriteLine("'
        lang_suffix = r'");'

    with open(file_name, 'r') as f:
        lines = f.readlines()

    lines_better = []
    for i, line in enumerate(lines):
        if i == 0:
            lines_better.append(file_prefix)

        line = line.replace('\n', '')
        if lang_prefix == 'printf("%s","' or lang_prefix == 'Console.WriteLine("':
            line = line.replace('\\', '\\\\')
        lines_better.append(line_prefix + lang_prefix + line + lang_suffix + line_suffix + '\n')

        if i == len(lines)-1:
            lines_better.append(file_suffix)
    with open(file_name.replace('.txt', '') + '_new.txt', 'w') as f_new:
        f_new.writelines(lines_better)
