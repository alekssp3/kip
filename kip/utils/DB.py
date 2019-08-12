from ..Scanner.Scanner import Scanner
from ..gui.UtilsGUI import tk_gui
from ..utils.Utils import combine_data
from ..utils.Structures import create_new_structure, PROJECT_STRUCTURES


# v 0.1
def find_in_db(data: list = None, db: Scanner = None):
    if data is None:
        data = tk_gui('Add data for finding')
    if db is None:
        print('No DB for finding')
        return
    data_dict = dict([(i, None) for i in data])
    combine_data(db, data_dict)
    return data_dict


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
