import os
import pycparser
from parser import Parser
from pycparser.c_ast import For
import pickle
from visitors import *
from functools import reduce
from fake_headers import fake
from parsing_utils import utils
import re
import json
import tempfile
from multiprocessing import Process, Manager
import tempfile
import shutil

dest_folder = 'temp_folder'

missed_loops = 0
missed_pragmas_header = 0
missed_pragmas_type = 0

redundant_ompts = re.compile("<ompts:testdescription>.*<\/ompts:testdescription>|<ompts:description>.*<\/ompts:description>|<ompts:version>.*<\/ompts:version>|<ompts:ompversion>.*<\/ompts:ompversion>|<ompts:directive>.*<\/ompts:directive>|<ompts:dependences>.*<\/ompts:dependences>|<ompts:.*?>|<\/ompts:.*>")
redundant_directives = re.compile("MAYBE_INLINE|TM_CALLABLE|__block|RESTRICT|__targetConst__|__targetHost__")


def log(file_name, msg):
    with open(file_name, 'a') as f:
        f.write(f'{msg}\n')


def remove_redundants(code):
    '''
    remove lines containing namespace or #error
    '''
    code_buf = []

    for line in code.split('\n'):
        l = line.lower().split()

        if (len(l) > 2 and l[0] == 'using' and l[1] == 'namespace') or \
        line.lstrip().startswith('#error'):
            continue

        code_buf.append(line)

    return '\n'.join(code_buf)


def remove_paren(code):
    flag = False
    num_paren = 0
    idx = 0

    for letter in code:
        if flag and num_paren == 0:
            return code[idx: ]

        if letter == '(':
            flag = True
            num_paren += 1
        elif letter == ')':
            num_paren -= 1

        idx += 1

    return ''


def remove_attribute(code):
    splitted_code = code.split('__attribute__')
    
    if len(splitted_code) == 1:
        return code

    updated_code = list(map(lambda code: remove_paren(code), splitted_code[1:]))

    return ''.join(list(splitted_code[0]) + updated_code)


def remove_ompt(code):
    code = redundant_directives.sub("", code)
    return redundant_ompts.sub("", code)


def update_code_pipline(code):
    FAKE_TYPEDEFS = '_fake_typedefs.h'
    
    code = remove_redundants(code)
    code = remove_attribute(code)
    code = remove_ompt(code)
    code = FAKE_INCLUDE  = f'#include \"{FAKE_TYPEDEFS}\"\n{code}'

    return code


def handle_error(err, code):
    err_pattern = {'*': r'(\w+)\W*$',
                    '=': r'^\W*(\w+)'}

    match = re.search(r'.*:(\d+):(\d+): before: (.*)', err)
    code_buf = code.split('\n')

    if match is None:
        return
    
    line, pos, param = int(match.group(1)), int(match.group(2)), match.group(3)
    sub_line = code_buf[line-1][: pos-1]
    param = param.strip()

    code_segment = "\n".join(code_buf[line-2:line+1])
    log('more_errors.txt', f'{err}\n{code_segment}\n =========================\n')

    if param in err_pattern:
        match = re.search(err_pattern[param], sub_line)

        if match is not None:
            log('typedefs.h', f'typedef int {match.group(1)};')
            return match.group(1)
    # else:
        # code_segment = "\n".join(code_buf[line-2:line+1])
        # log('more_errors.txt', f'{err}\n{code_segment}')

        


class CLoopParser(Parser):
    def __init__(self, repo_path, parsed_path):
        super().__init__(repo_path, parsed_path, ['.c'])

    def is_empty_loop(self, node):
        '''
        precondition - node is a For struct
        '''
        children = dict(node.children())

        try:
            # if there is no 'block_items' attribute than it's another compound struct
            temp = children['stmt'].block_items
        except:
            return False

        if children['stmt'].block_items is None:
            return True
        elif all(type(child) is For for child in children['stmt'].block_items):
             # return true if one of the for loops is empty
            return any(self.is_empty_loop(child) for child in children['stmt'].block_items)
        else:
            return False


    def create_ast(self, file_path, code_buf, result):
        with open('../ENV.json', 'r') as f:
            vars = json.loads(f.read())

        repo_name = file_path[len(self.repo_path + self.root_dir) + 2:]
        repo_name = repo_name[:repo_name.find('/') ]
        cpp_args = ['-nostdinc', '-w', '-E', r'-I' + vars["FAKE_DIR"]]

        _, headers, _ = fake.get_headers(vars['REPOS_DIR'], repo_name)
        # log('headers.txt', str(fake.extract_includes(file_path)))

        # create empty headers
        os.makedirs(dest_folder)
        fake.create_empty_headers(file_path, dest_folder)
        cpp_args.append(r'-I' + dest_folder)

        for header in list(headers)[:50]:
            cpp_args.append(r'-I' + os.path.join(vars['REPOS_DIR'], repo_name, header))

        try:
            with tempfile.NamedTemporaryFile(suffix='.c', mode='w+') as tmp, open(file_path, 'r') as f:    
                code = f.read() 
                code = update_code_pipline(code)    # remove unparsable code
                tmp.write(code)
                tmp.seek(0)
                ast = pycparser.parse_file(tmp.name, use_cpp=True, cpp_path='mpicc', cpp_args = cpp_args)
                result['ast'] = ast

        except pycparser.plyparser.ParseError as e:  
            log('error_logger.txt', f'Parser Error: {file_path} ->\n {e}\n')
            result['missed_type'] = utils.count_for(file_path)
            handle_error(str(e), code)

        except Exception as e:
            log('error_logger.txt', f'Unexpected Error: {file_path} ->\n {e}\n')
            result['missed_header'] = utils.count_for(file_path)

            # if str(e).startswith('Command'): # Capture failures caused by missing headers
            #     print(f'aaaaaaaaaaaaa {utils.count_for(file_path)} -> {file_path}')

        finally:
            shutil.rmtree(dest_folder)

    def parse(self, file_path, code_buf):
        # return_dict = dict()
        # self.create_ast(file_path, code_buf, return_dict)
        log('files.txt', file_path)
        manager = Manager()
        return_dict = manager.dict()
        t = Process(target=self.create_ast, args=(file_path, code_buf, return_dict), daemon=True)

        t.start()
        t.join(120.0)

        if t.is_alive():
            t.terminate()
            shutil.rmtree(dest_folder)
            return
        global missed_loops
        if 'missed_type' in return_dict:
            missed_loops += return_dict['missed_type'][0]
            global missed_pragmas_type
            missed_pragmas_type += return_dict['missed_type'][1]
        elif 'missed_header' in return_dict:
            missed_loops += return_dict['missed_header'][0]
            global missed_pragmas_header
            missed_pragmas_header += return_dict['missed_header'][1]
        elif 'ast' in return_dict:
            return return_dict['ast']

    def parse_file(self, root_dir, file_name, exclusions):
        '''
        Parse the given file into ast and extract the loops associated with omp pargma (or without)
        '''
        pos, neg = 0, 0
        file_path = os.path.join(root_dir, file_name)
        save_dir = os.path.join(self.parsed_path, root_dir[self.split_idx: ])
        name = os.path.splitext(file_name)[0]

        pfv = PragmaForVisitor()
        verify_loops = ForLoopChecker()
        func_call_checker = FuncCallChecker()

        with open(file_path, 'r+') as f:
            
            try:
                code = f.read()
            except UnicodeDecodeError:
                return 0, 0, False

            ast = self.parse(file_path, code)

            if ast is None:                 # file parsing failed
                return 0, 0, False

            pfv.visit(ast)
            pragmas = pfv.pragmas + len(pfv.neg_nodes) * [None]
            nodes = pfv.pos_nodes + pfv.neg_nodes

            for idx, (pragma, loop) in enumerate(zip(pragmas, nodes)):
                verify_loops.reset()
                func_call_checker.reset()

                verify_loops.visit(loop)
                if verify_loops.found:  # undesired tokens found
                    exclusions['bad_case'] += 1
                    continue
                
                generator = pycparser.c_generator.CGenerator()
                code = generator.visit(loop)
                if code in self.memory:
                    exclusions['duplicates'] += 1
                    continue

                if self.is_empty_loop(loop):
                    exclusions['empty'] += 1
                    continue

                func_call_checker.visit(loop)
                if func_call_checker.found:
                    exclusions['func_calls'] += 1

                # print(pragma if not None else 'None')
                # print(f'\n{code}\n==============\n\n')                   
                self.create_directory(save_dir) 
                self.memory.append(code)
                self.save(os.path.join(save_dir, f"{name}{'_neg_' if pragma is None else '_pos_'}{idx}.pickle"), pragma, loop, code)

                if pragma is None:
                    neg += 1
                else:
                    pos += 1

            return pos, neg, True

    def scan_dir(self):
        total_files, num_failed = 0, 0
        total_pos, total_neg = 0, 0
        omp_repo = os.path.join(self.root_dir, self.repo_path)
        exclusions = {'bad_case': 0, 'empty': 0, 'duplicates': 0, 'func_calls':0}

        # iterate over repos
        for idx, repo_name in enumerate(os.listdir(omp_repo)):
            
            for root, dirs, files in os.walk(os.path.join(omp_repo, repo_name)):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    ext = os.path.splitext(file_name)[1].lower()
                    
                    if ext in self.file_extensions:
                        pos, neg, is_parsed = self.parse_file(root, file_name, exclusions)

                        if not is_parsed:
                            num_failed += 1

                        if pos is not None:
                            total_pos += pos
                            total_neg += neg

                        total_files += 1

            if idx % (5) == 0:
                log('success_logger.txt', "{:20}{:10}   |   {:20} {:10}\n\n".format("files processed: ", total_files, "failed to parse: ", num_failed))
                print("{:20}{:10}   |   {:20} {:10}".format("files processed: ", total_files, "failed to parse: ", num_failed))
                print("{:20}{:10}   |   {:20} {:10}".format("pos examples: ", total_pos, "neg examples: ", total_neg))
                print(f'exclusions: {exclusions}\n')

                print(f'missed loops {missed_loops}, missed pragmas type {missed_pragmas_type}, missed pragmas header {missed_pragmas_header}')

        print(f'missed loops {missed_loops}, missed pragmas type {missed_pragmas_type}, missed pragmas header {missed_pragmas_header}')
        print(total_pos, total_neg, exclusions, total_files, num_failed)
        return total_pos, total_neg, exclusions, total_files, num_failed


parser = CLoopParser('../repositories_openMP', '../c_loops')
# parser = CLoopParser('../asd', 'c_loops2')

# data = parser.load('/home/talkad/Downloads/thesis/data_gathering_script/c_loops/357r4bd/2d-heat/src/openmp-2dheat_pos_0.pickle')
# print(f'pragma: {data.omp_pragma}')
# print('code:\n')
# print(data.textual_loop)


total = parser.scan_dir()
print(total)

# missed loops 43864, missed pragmas type 13114, missed pragmas header 275
# 12024 30632 {'bad_case': 6203, 'empty': 77, 'duplicates': 125026, 'func_calls': 18881} 19784 3577

# __attribute__, =, *
# missed loops 37410, missed pragmas type 8415, missed pragmas header 280
# 12076 30709 {'bad_case': 6760, 'empty': 80, 'duplicates': 130848, 'func_calls': 18925} 19784 2378

# fake headers
# missed loops 30812, missed pragmas type 7321, missed pragmas header 278
# 12574 32519 {'bad_case': 6914, 'empty': 89, 'duplicates': 135084, 'func_calls': 19930} 19784 2038

# missed loops 28842, missed pragmas type 6758, missed pragmas header 309
# 12776 33279 {'bad_case': 6982, 'empty': 90, 'duplicates': 135693, 'func_calls': 20522} 19784 1848