from ..Scanner.Scanner import Scanner
from ..utils.Config import Config
from ..utils.Structures import create_new_structure
from ..utils.DB import find_in_db
from ..utils.Structures import PROJECT_STRUCTURES
from ..utils.pdf.pdf import pdf_merge
from ..utils.data import save
from ..gui.UtilsGUI import tk_gui
import os
from ..Scanner import Scanner
from ..utils.Utils import combine_folder
from ..utils.Question import Question

# class RFI:
#         "Class for working with RFI"
#         RFI_DB = Scanner()
#         ANSWERS_DB = Scanner()

#     def update(self, DB, path_list=None):
#         for p in path_list:
#             DB.update(p)

# v 0.2.5
def check_rfi(rfi_list, rfi_db=None, answers_db=None):
    RFI = create_new_structure(*PROJECT_STRUCTURES.RFI)
    rfi_dict = find_in_db(rfi_list, rfi_db)
    # RFI_STRUCT = create_new_structure(*PROJECT_STRUCTURES.RFI_STRUCT)
    # rfi_struct = get_structure_from_dict(rfi_dict, RFI_STRUCT)
    answers_dict = find_in_db(rfi_list, answers_db)
    # ANSWER_STRUCT = create_new_structure(*PROJECT_STRUCTURES.ANS_STRUCT)
    # answers_struct = get_structure_from_dict(answers_dict, ANSWER_STRUCT)
    return RFI._make((rfi_dict, answers_dict))


def check_and_merge(out_file, rfi_list=None, rfi_db=None, answers_db=None, open_on_done=True):
    if rfi_list is None:
        rfi_list = tk_gui("Add rfi's")
    if '.pdf' in out_file:
        save(rfi_list, out_file.replace('.pdf', '.txt'))
    else:
        save(rfi_list, out_file + '.txt')

    paths = check_rfi(rfi_list, rfi_db, answers_db)
    pdf_merge(paths.rfi.values(), out_file)
    if not open_on_done:
        q = Question()
        if q.check(q.view('Open file in editor', Question.YES_NO)):
            os.startfile(os.path.abspath(out_file))
    else:
        os.startfile(os.path.abspath(out_file))    


def check_and_combine(rfi_list=None, folder=None, rfi_db=None, answers_db=None, excludes=None, exactly=None):
    # folder_name = folder_name or ''.join(rfi_list.split('.')[:-1])
    if rfi_list is None:
        rfi_list = tk_gui("Add rfi's")

    if folder is None:
        folder = tk_gui("Add folder name")

    rfi_db = rfi_db or Scanner.load_db(Config.RFI_DB_PATH)
    answers_db = answers_db or Scanner.load_db(Config.ANSWER_DB_PATH)
    # excludes = excludes or load(rfi_list+'.excludes')
    # exactly = exactly or load(rfi_list+'.exactly')
    data = check_rfi(rfi_list, rfi_db, answers_db)
    combine_folder(data.rfi.values(), folder)
    return data