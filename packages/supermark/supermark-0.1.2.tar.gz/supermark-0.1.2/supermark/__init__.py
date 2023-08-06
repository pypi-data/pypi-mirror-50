from enum import Enum
import os
import yaml
import pypandoc

import random
import string
import re

import hashlib

shake = hashlib.shake_128()

ENV_PATTERN = re.compile('[a-zA-Z]*:')

LOG_VERBOSE = False

def random_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

from colorama import init, Fore, Style
init(autoreset=True)

def tell(message, level='info', chunk=None):
    # Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    # Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    # Style: DIM, NORMAL, BRIGHT, RESET_ALL
    if chunk is not None:
        message = '{} line {}: {}'.format(chunk.path, chunk.start_line_number, message)
    if level == 'info':
        if LOG_VERBOSE:
            print(Fore.GREEN + Style.BRIGHT +  ' - ' + Style.RESET_ALL + message)
    elif level == 'warn':
        print(Fore.YELLOW + Style.BRIGHT +  ' - ' + Style.RESET_ALL + message)
    else:
        print(Fore.RED + Style.BRIGHT +  ' - ' + Style.NORMAL + message)


class ParserState(Enum):
    MARKDOWN = 0
    YAML = 1
    CODE = 2
    HTML = 3

def is_empty(s_line):
    return not s_line

class RawChunk:

    def __init__(self, lines, chunk_type, start_line_number, path):
        self.lines = lines
        self.type = chunk_type
        self.start_line_number = start_line_number
        self.path = path
        # check if we only got empty lines
        def all_empty(lines):
            if len(lines) == 0: return True
            for line in lines:
                if line.strip(): return False
            return True
        self._is_empty = all_empty(self.lines)
        # remove blank lines from the beginning
        while (len(self.lines)>0 and is_empty(self.lines[0].strip())):
            self.lines.pop(0)
            self.start_line_number = self.start_line_number + 1
    
    def is_empty(self):
        return self._is_empty

    def get_type(self):
        return self.type

    def get_first_line(self):
        if len(self.lines) == 0:
            return 'empty'
        return self.lines[0]

def yaml_start(s_line):
    return s_line == '---'

def yaml_stop(s_line):
    return s_line == '---'

def has_class_tag(s_line):
    return s_line.startswith(':') and ENV_PATTERN.match(s_line)

def markdown_start(s_line, empty_lines):
    return has_class_tag(s_line) or s_line.startswith('# ') or empty_lines >= 2 or s_line.startswith('Aside:')

def html_start(s_line, empty_lines):
    return s_line.startswith('<') and empty_lines >= 2

def html_stop(empty_lines):
    return empty_lines >= 2

def code_start(s_line):
    return s_line.startswith('```')

def code_stop(s_line):
    return s_line.startswith('```')

def _parse(lines, path):
    chunks = []
    current_lines = []
    empty_lines = 0
    state = ParserState.MARKDOWN
    start_line_number = 0

    for line_number, line in enumerate(lines, start=1):
        s_line = line.strip()
        if state==ParserState.MARKDOWN:
            if is_empty(s_line):
                empty_lines = empty_lines + 1
                current_lines.append(line)
            elif yaml_start(s_line):
                chunks.append(RawChunk(current_lines, ParserState.MARKDOWN, start_line_number, path))
                state = ParserState.YAML
                current_lines = []
                start_line_number = line_number
                empty_lines = 0
            elif code_start(s_line):
                chunks.append(RawChunk(current_lines, ParserState.MARKDOWN, start_line_number, path))
                state = ParserState.CODE
                current_lines = [line]
                start_line_number = line_number
                empty_lines = 0
            elif html_start(s_line, empty_lines):
                chunks.append(RawChunk(current_lines, ParserState.MARKDOWN, start_line_number, path))
                state = ParserState.HTML
                current_lines = []
                current_lines.append(line)
                start_line_number = line_number
                empty_lines = 0
            elif markdown_start(s_line, empty_lines):
                chunks.append(RawChunk(current_lines, ParserState.MARKDOWN, start_line_number, path))
                state = ParserState.MARKDOWN
                current_lines = []
                current_lines.append(line)
                start_line_number = line_number
                empty_lines = 0
            else:
                current_lines.append(line)
                empty_lines = 0
        elif state==ParserState.YAML:
            if yaml_stop(s_line):
                chunks.append(RawChunk(current_lines, ParserState.YAML, start_line_number, path))
                state = ParserState.MARKDOWN
                current_lines = []
                start_line_number = line_number + 1
            else:
                current_lines.append(line)
        elif state==ParserState.CODE:
            if code_stop(s_line):
                current_lines.append(line)
                chunks.append(RawChunk(current_lines, ParserState.CODE, start_line_number, path))
                state = ParserState.MARKDOWN
                current_lines = []
                start_line_number = line_number + 1
            else:
                current_lines.append(line)
        elif state==ParserState.HTML:
            if is_empty(s_line):
                empty_lines = empty_lines + 1
                current_lines.append(line)
            elif html_stop(empty_lines):
                chunks.append(RawChunk(current_lines, ParserState.HTML, start_line_number, path))
                state = ParserState.MARKDOWN
                current_lines = []
                current_lines.append(line)
                start_line_number = line_number
                empty_lines = 0
            else:
                current_lines.append(line)
                empty_lines = 0
    # create last chunk
    chunks.append(RawChunk(current_lines, state, start_line_number, path))
    # remove chunks that turn out to be empty
    chunks = [item for item in chunks if not item.is_empty()]
    return chunks

class Pattern:
     def __init__(self):
        pass

class MarkdownPattern(Pattern):
    
    def match(self, line):
        return False

    def get_css(self):
        return None

    def to_html(self, chunk):
        extra_args = ['--ascii', '--highlight-style', 'pygments']
        extra_args = ['--highlight-style', 'pygments']
        output = pypandoc.convert_text(chunk.get_content(), 'html', format='md', extra_args=extra_args)
        return output

class MarkdownLearningGoalsPattern(MarkdownPattern):

    def match(self, line):
        return line.lower().startswith('# learning goals')

    def to_html(self, chunk):
        return '<div class="goals">' + super().to_html() + '</div>'
    

class Chunk:

    def __init__(self, raw_chunk, page_variables):
        self.raw_chunk = raw_chunk
        self.page_variables = page_variables
        self.aside = False
        self.asides = []

    def is_aside(self):
        return self.aside

    def get_asides(self):
        return self.asides

    def get_first_line(self):
        return self.raw_chunk.lines[0]

    def get_type(self):
        return self.raw_chunk.type
    
    def get_start_line_number(self):
        return self.raw_chunk.start_line_number

    def get_content(self):
        return ''.join(self.raw_chunk.lines)


class YAMLChunk(Chunk):

     def __init__(self, raw_chunk, dictionary, page_variables, required=None, optional=None):
          super().__init__(raw_chunk, page_variables)
          self.dictionary = dictionary
          required = required or []
          optional = optional or []
          for key in required:
               if key not in self.dictionary:
                    tell("YAML section misses required parameter '{}'.".format(key), level='error', chunk=raw_chunk)
          for key in self.dictionary.keys():
               if (key not in required) and (key not in optional) and (key != 'type'):
                    tell("YAML section has unknown parameter '{}'.".format(key), level='warn', chunk=raw_chunk)


class YAMLVideoChunk(YAMLChunk):

    def __init__(self, raw_chunk, dictionary, page_variables):
        super().__init__(raw_chunk, dictionary, page_variables, required=['video'], optional=['start', 'caption', 'position'])
    
    def to_html(self):
        html = []
        video = self.dictionary['video']
        url = 'https://youtu.be/{}'.format(video)
        start = ''
        if 'start' in self.dictionary:
            start = '?start={}'.format(self.dictionary['start'])
            url = url + start
        if 'position' in self.dictionary and self.dictionary['position']=='aside':
            shake.update('{}'.format(video).encode('utf-8'))
            aside_id = shake.hexdigest(3)
            html.append('<span name="{}"></span><aside name="{}">'.format(aside_id, aside_id))
            html.append('<a href="{}"><img width="{}" src="https://img.youtube.com/vi/{}/sddefault.jpg"></img></a>'.format(url, 240, video))
            if 'caption' in self.dictionary:
                html_caption = pypandoc.convert_text(self.dictionary['caption'], 'html', format='md')
                html.append(html_caption)
            html.append('</aside>')
        else:
            html.append('<div class="figure">')
            width = 560
            height = 315
            html.append('<iframe width="{}" height="{}" src="https://www.youtube.com/embed/{}{}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'.format(width, height, video, start))
            if 'caption' in self.dictionary:
                html.append('<span name="{}">&nbsp;</span>'.format(self.dictionary['video']))
                html_caption = pypandoc.convert_text(self.dictionary['caption'], 'html', format='md')
                html.append('<aside name="{}"><p>{}</p></aside>'.format(self.dictionary['video'], html_caption))
            html.append('</div>')
        return '\n'.join(html)


class YAMLFigureChunk(YAMLChunk):

    def __init__(self, raw_chunk, dictionary, page_variables):
        super().__init__(raw_chunk, dictionary, page_variables, required=['source'], optional=['caption', 'link'])
        # TODO: check if image file exists

    def to_html(self):
        html = []
        html.append('<div class="figure">')
        if 'caption' in self.dictionary:
            if 'link' in self.dictionary:
                html.append('<a href="{}"><img src="{}" alt="{}" width="100%"/></a>'.format(self.dictionary['link'], self.dictionary['source'], self.dictionary['caption']))
            else:
                html.append('<img src="{}" alt="{}" width="100%"/>'.format(self.dictionary['source'], self.dictionary['caption']))
            html.append('<span name="{}">&nbsp;</span>'.format(self.dictionary['source']))
            html_caption = pypandoc.convert_text(self.dictionary['caption'], 'html', format='md')
            html.append('<aside name="{}"><p>{}</p></aside>'.format(self.dictionary['source'], html_caption))
        else:
            if 'link' in self.dictionary:
                html.append('<a href="{}"><img src="{}" width="100%"/></a>'.format(self.dictionary['link'], self.dictionary['source']))
            else:
                html.append('<img src="{}" width="100%"/>'.format(self.dictionary['source']))
        html.append('</div>')
        return '\n'.join(html)


class YAMLButtonChunk(YAMLChunk):

    def __init__(self, raw_chunk, dictionary, page_variables):
        super().__init__(raw_chunk, dictionary, page_variables, required=['url', 'text'])

    def to_html(self):
        clazz = 'ntnu-button'
        html = []
        html.append('<a class="{}" href="{}">{}</a>'.format(clazz, self.dictionary['url'], self.dictionary['text']))
        return '\n'.join(html)


class YAMLLinesChunk(YAMLChunk):

    def __init__(self, raw_chunk, dictionary, page_variables):
        super().__init__(raw_chunk, dictionary, page_variables, required=['lines'])

    def to_html(self):
        html = []
        for _ in range(self.dictionary['lines']):
            html.append('<hr class="lines"/>')
        return '\n'.join(html)


class YAMLDataChunk(YAMLChunk):

    def __init__(self, raw_chunk, dictionary, page_variables):
        super().__init__(raw_chunk, dictionary, page_variables, optional=['status'])


HINT = []
HINT.append('</section>')
HINT.append('<section class="content">')
HINT.append('<div class="hint_title">{}')
HINT.append('<button type="button" class="btn btn-dark btn-sm" style="float: right" data-toggle="modal" data-target="#{}Modal">Show</button>')
HINT.append('</div>')
HINT.append('<div class="hint" style="-webkit-filter: blur(5px);" id="{}">{}')
HINT.append('</div>')
HINT.append('<div class="modal fade" id="{}Modal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">')
HINT.append('  <div class="modal-dialog" role="document">')
HINT.append('    <div class="modal-content">')
HINT.append('      <div class="modal-header">')
HINT.append('        <h5 class="modal-title" id="exampleModalLabel">Hint</h5>')
HINT.append('        <button type="button" class="close" data-dismiss="modal" aria-label="Close">')
HINT.append('          <span aria-hidden="true">&times;</span>')
HINT.append('        </button>')
HINT.append('      </div>')
HINT.append('      <div class="modal-body">Are you sure you want to see the hint, or try a bit more on your own?</div>')
HINT.append('      <div class="modal-footer">')
HINT.append('        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>')
HINT.append('        <button type="button" class="btn btn-primary" data-dismiss="modal" onclick="document.getElementById(\'{}\').style.cssText = \'\'">Yes, show me!</button>')
HINT.append('      </div>')
HINT.append('    </div>')
HINT.append('  </div>')
HINT.append('</div>')
HINT.append('</section>')
HINT.append('<section class="content">')

HINT = '\n'.join(HINT)

def apply_hint_template(title, body, element_id):
    return HINT.format(title, element_id, element_id, body, element_id, element_id)

class MarkdownChunk(Chunk):

    def __init__(self, raw_chunk, page_variables):
        super().__init__(raw_chunk, page_variables)
        self.content = ''.join(self.raw_chunk.lines)
        self.is_section = super().get_first_line().startswith('# ')
        if has_class_tag(super().get_first_line().strip()):
            self.class_tag = super().get_first_line().strip().split(':')[1].lower()
            self.aside = self.class_tag=='aside'
            self.content = self.content[len(self.class_tag)+2:].strip()
        else:
            self.class_tag = None
            self.aside = False

    def get_content(self):
        return self.content
    
    def to_html(self):
        if self.aside:
            shake.update(self.content.encode('utf-8'))
            aside_id = shake.hexdigest(3)
            output = []
            output.append('<span name="{}"></span><aside name="{}">'.format(aside_id, aside_id))
            extra_args = ['--ascii', '--highlight-style', 'pygments']
            extra_args = ['--highlight-style', 'pygments']
            output.append(pypandoc.convert_text(self.content, 'html', format='md', extra_args=extra_args))
            output.append('</aside>')
            return ''.join(output)
        else:
            extra_args = ['--ascii', '--highlight-style', 'pygments']
            extra_args = ['--highlight-style', 'pygments']
            if self.class_tag:
                output = pypandoc.convert_text(self.get_content(), 'html', format='md', extra_args=extra_args)
                if self.class_tag=='hint':
                    title = "Hint"
                    body = output
                    shake.update(self.content.encode('utf-8'))
                    element_id = shake.hexdigest(3)
                    output = apply_hint_template(title, body, element_id)
                else:   
                    output = '<div class="{}">{}</div>'.format(self.class_tag, output)
            else:
                output = pypandoc.convert_text(self.get_content(), 'html', format='md', extra_args=extra_args)
            return output


class HTMLChunk(Chunk):

    def __init__(self, raw_chunk, page_variables):
        super().__init__(raw_chunk, page_variables)
    
    def to_html(self):
        return super().get_content()


class CodeChunk(Chunk):

    def __init__(self, raw_chunk, page_variables):
        super().__init__(raw_chunk, page_variables)

    def to_html(self):
        extra_args = ['--highlight-style', 'pygments']
        output = pypandoc.convert_text(self.get_content(), 'html', format='md', extra_args=extra_args)
        return output


def cast(rawchunks):
    chunks = []
    page_variables = {}
    for raw in rawchunks:
        chunk_type = raw.get_type()
        if chunk_type==ParserState.MARKDOWN:
            chunks.append(MarkdownChunk(raw, page_variables))
        elif chunk_type==ParserState.YAML:
            dictionary = yaml.safe_load(''.join(raw.lines))
            if isinstance(dictionary, dict):
                if 'type' in dictionary:
                    yaml_type = dictionary['type']
                    if yaml_type == 'youtube':
                        chunks.append(YAMLVideoChunk(raw, dictionary, page_variables))
                    elif yaml_type == 'figure':
                        chunks.append(YAMLFigureChunk(raw, dictionary, page_variables))
                    elif yaml_type == 'button':
                        chunks.append(YAMLButtonChunk(raw, dictionary, page_variables))
                    elif yaml_type == 'lines':
                        chunks.append(YAMLLinesChunk(raw, dictionary, page_variables))
                    # TODO warn if unknown type
                else:
                    data_chunk = YAMLDataChunk(raw, dictionary, page_variables)
                    try:
                        page_variables.update(data_chunk.dictionary)
                    except ValueError as e:
                        print(e)
                    chunks.append(data_chunk)
            else:
                tell('Something is wrong with the YAML section.', level='error', chunk=raw)
        elif chunk_type==ParserState.HTML:
            chunks.append(HTMLChunk(raw, page_variables))
        elif chunk_type==ParserState.CODE:
            chunks.append(CodeChunk(raw, page_variables))
    return chunks

def arrange_assides(chunks):
    main_chunks = []
    current_main_chunk = None
    for chunk in chunks:
        if chunk.is_aside():
            if current_main_chunk is not None:
                current_main_chunk.asides.append(chunk)
            else:
                tell('Aside chunk cannot be defined as first element.', level='warn')
                main_chunks.append(chunk)
        else:
            main_chunks.append(chunk)
            current_main_chunk = chunk
    return main_chunks

def transform_page_to_html(lines, template, filepath, abort_draft):
    chunks = _parse(lines, filepath)
    chunks = cast(chunks)
    chunks = arrange_assides(chunks)

    content = []
    content.append('<div class="page">')
    if len(chunks)==0:
        pass
    else:
        first_chunk = chunks[0]
        if isinstance(first_chunk, MarkdownChunk) and not first_chunk.is_section:
            content.append('    <section class="content">')

    for chunk in chunks:
        if 'status' in chunk.page_variables and abort_draft and chunk.page_variables['status'] == 'draft':
            content.append('<mark>This site is under construction.</mark>')
            break
        if isinstance(chunk, YAMLDataChunk):
            pass
        elif isinstance(chunk, MarkdownChunk):
            if chunk.is_section:
                # open a new section
                content.append('    </section>')
                content.append('    <section class="content">')
            content.append(chunk.to_html())
            for aside in chunk.asides:
                content.append(aside.to_html())
        else:
            content.append(chunk.to_html())
            for aside in chunk.asides:
                content.append(aside.to_html())

    content.append('    </section>')
    content.append('</div>')
    content = '\n'.join(content)
    parameters = {'content': content}
    html = template.format(**parameters)
    return html

def _create_target(source_file_path, target_file_path, template_file_path, overwrite):
    if not os.path.isfile(target_file_path):
        return True
    if overwrite:
        return True
    if not os.path.isfile(template_file_path):
        return os.path.getmtime(target_file_path) < os.path.getmtime(source_file_path)
    else:
        return os.path.getmtime(target_file_path) < os.path.getmtime(source_file_path) or os.path.getmtime(target_file_path) < os.path.getmtime(template_file_path)

def write_file(html, target_file_path):
    encoding = 'utf-8'
    try:
        with open(target_file_path, "w", encoding=encoding) as html_file:
            html_file.write(html)
    except UnicodeEncodeError as error:
        tell('Encoding error when writing file {}.'.format(target_file_path))
        character = error.object[error.start:error.end]
        line = html.count("\n",0,error.start)+1
        tell('Character {} in line {} cannot be saved with encoding {}.'.format(character, line, encoding))
        with open(target_file_path, "w", encoding=encoding, errors='ignore') as html_file:
            html_file.write(html)

def process_file(source_file_path, target_file_path, template, abort_draft):
     with open(source_file_path, 'r', encoding='utf-8') as file:
          lines = file.readlines()
          tell('{}'.format(source_file_path), 'info')
          html = transform_page_to_html(lines, template, source_file_path, abort_draft)
          write_file(html, target_file_path)

def default_html_template():
    html = []
    html.append('<head><title></title></head>')
    html.append('<body>')
    html.append('{content}')
    html.append('</body>')
    html.append('</html>')
    return '\n'.join(html)

def load_html_template(template_path):
    try:
        with open(template_path, 'r', encoding='utf-8', errors="surrogateescape") as templatefile:
            template = templatefile.read()
            tell('Loading template {}.'.format(template_path), 'info')
            return template
    except FileNotFoundError:
        tell('Template file missing. Expected at {}. Using default template.'.format(template_path), 'warn')
        return default_html_template()

def build(input_path, output_path, template_file, rebuild_all_pages = True, abort_draft = True, verbose=False):
    global LOG_VERBOSE
    LOG_VERBOSE = verbose
    template = load_html_template(template_file)
    for filename in os.listdir(input_path):
        source_file_path = os.path.join(input_path, filename)
        if os.path.isfile(source_file_path) and filename.endswith('.md'):
            target_file_name = os.path.splitext(os.path.basename(filename))[0] + '.html'
            target_file_path = os.path.join(output_path, target_file_name)
            if _create_target(source_file_path, target_file_path, template_file, rebuild_all_pages):
                process_file(source_file_path, target_file_path, template, abort_draft)