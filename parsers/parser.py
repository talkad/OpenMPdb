from abc import ABC, abstractmethod
import os
import pickle
 
class OmpLoop:
    '''
    Define a class that later will be dumped into pickle file
    '''
    def __init__(self, omp_pragma, ast_loop, textual_loop):
        self.omp_pragma = omp_pragma         # omp pragma associated with the given loop
        self.ast_loop = ast_loop             # ast format representing AST structure of loop
        self.textual_loop = textual_loop     # textual representation of code




class Parser(ABC):
    '''
    Abstract class that defines the general behavior of our parsers
    '''

    def __init__(self, repo_path, parsed_path, file_extensions):
        self.root_dir = os.getcwd()
        self.repo_path = repo_path
        self.parsed_path = parsed_path
        self.file_extensions = file_extensions
 
    def create_directory(self, dirs):
        '''
        Create directories if not exists
        '''
        if not os.path.exists(dirs):
            os.makedirs(dirs)

    def save(self, file_path, pragma, ast_loop, textual_loop):
        '''
        Save OmpLoop structure into file_path
        '''
        parsed_loop = OmpLoop(pragma, ast_loop, textual_loop)

        with open(file_path, 'wb') as f:
            pickle.dump(parsed_loop, f)

    def load(self, file_path):
        '''
        Load OmpLoop structure from file_path
        '''
        with open(file_path, 'rb') as f:
            return pickle.load(f)

    @abstractmethod
    def parse(self, code_buf, future):
        '''
        The return value is boolean that indicates the parsing exit status.

        Parameters:
            code_buf - textual representation of the code
            future   - a mutable struct that on success will contain the AST
        Returns:
            True if the parsing succeeded, False otherwise
        '''

        pass

    @abstractmethod
    def parse_file(self, root_dir, file_name, exclusions):
        '''
        Parse file and save for loops into pickles.

        Parameters:
            root_dir - the path absolute path the directory that contains file_name
            file_name - the name of the file to be parsed
            exclusions - dictionary that contains stats about excluded examples
        Returns:
            returns a sequence of three values <num_positive_examples>, <num_negative_examples>, <parsing_status>
        '''
        pass

    def scan_dir(self):
        '''
        Loop over all files in repo and parse them.

        Returns:
            1. the amount of positive examples found
            2. the amount of negative examples found
            3. exclusion stats
            4. number of relevant (with respect to the file extension) files
            total_pos, total_neg, exclusions, total_files, num_failed
        '''

        total_files, num_failed = 0, 0
        total_pos, total_neg = 0, 0
        omp_repo = os.path.join(self.root_dir, self.repo_path)
        exclusions = {'bad_case': 0, 'empty': 0, 'duplicates': 0, 'func_calls':0}

        for idx, (root, dirs, files) in enumerate(os.walk(omp_repo)):
            for file_name in files:
                ext = os.path.splitext(file_name)[1].lower()
                
                if ext in self.file_extensions:
                    pos, neg, is_parsed = self.parse_file(root, file_name, exclusions)

                    if pos is not None:
                        total_pos += pos
                        total_neg += neg

                    if not is_parsed:
                        num_failed += 1
                    total_files += 1

            if idx % (10**2) == 0:
                print("{:20}{:10}   |   {:20} {:10}".format("files processed: ", total_files, "failed to parse: ", num_failed))
                print("{:20}{:10}   |   {:20} {:10}".format("pos examples: ", total_pos, "neg examples: ", total_neg))
                print(f'exclusions: {exclusions}\n')

        return total_pos, total_neg, exclusions, total_files, num_failed