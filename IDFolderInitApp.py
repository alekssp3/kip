'Сборщик комплекта исполнительной документации'

import os
import sys
import shutil
# import sys

from pathlib import Path
from kip.Scanner.Scanner import Scanner, loadOrCreateScanner
from kip.utils.Config import Config
from kip.utils.data import load
from kip.utils.Structures import get_findings_lists
from kip.utils.Utils import pl
from kip.utils.Structures import get_projects_structure, get_last_projects_structure
from kip.utils.Structures import get_journals_structure, get_last_journals_structure
from kip.utils.Errors import StructFieldError


app_path = Path()
print(f'app path: {app_path}')
print(f'os getcwd: {os.getcwd()}')
print(f'sys path: {sys.path}')


config = Config(path=app_path.joinpath('IDFolderInit.conf'))
path_to_save_id = Path(config.ID_SAVE_PATH)
path_to_find_projects = Path(config.PROJECTS_FINDING_PATH)
path_to_find_journals = Path(config.JOURNALS_FINDING_PATH)
path_to_current_ids = Path(config.CURRENT_IDS_FILE_PATH)
path_to_projects_db = Path(config.PROJECTS_DB_PATH)
path_to_journals_db = Path(config.JOURNALS_DB_PATH)
path_to_templates = Path(config.TEMPLATES_PATH)
projects = loadOrCreateScanner(path_to_projects_db, path_to_find_projects)
journals = loadOrCreateScanner(path_to_journals_db, path_to_find_journals)
current_ids = load(path_to_current_ids)


def get_param_by_field(struct, field:str, condition:str, param:str=None):
    for s in struct:
        try:
            if s.__getattribute__(field) == condition:
                return str(s.__getattribute__(param))
        except Exception:
            # raise StructFieldError
            return ''


def get_struct_by_field(struct, field:str, condition:str):
    for s in struct:
        try:
            if s.__getattribute__(field) == condition:
                return s
        except Exception:
            return


def init_id_kit(proj_struct, jrn_struct, path:Path):
    for ids in current_ids:
        try:
            ps = get_struct_by_field(proj_struct, 'name', ids)
            js = get_struct_by_field(jrn_struct, 'name', ids)
            cur_path = path.joinpath('_'.join([ids, str(ps.rev)]))
            # print(f'cur_path: {cur_path}')
            cur_path.mkdir()
            cur_sub_path = cur_path.joinpath('-'.join([ids, '001']))
            # print(f'cur_sub_path: {cur_sub_path}')
            cur_sub_path.mkdir()
            cur_proj_path = cur_path.joinpath('projects')
            # print(f'cur_proj_path: {cur_proj_path}')
            # print(js)
            cur_proj_path.mkdir()
            shutil.copy(ps.path, cur_proj_path)
            shutil.copy(js.path, cur_sub_path.joinpath(' '.join(['ЖВК', ids]) + js.path.suffix))
            for t in path_to_templates.iterdir():
                if '.xlsm' in str(t):
                    shutil.copy(str(t), cur_sub_path.joinpath('-'.join([ids, '001']) + '.xlsm'))
                else:
                    shutil.copy(str(t), cur_sub_path)


        except Exception:
            print(f'Problem with project {ids}')
        

def debug():
    # for file in path_to_find_projects.iterdir():
    #     print(file)
    # print(path_to_find_projects)
    # print(path_to_find_journals)

    # for line in current_ids:
    #     print(line)
    
    # all_projects = get_findings_lists(current_ids, projects)
    # all_journals = get_findings_lists(current_ids, journals)
    print('Projects')
    print(f'Len current projects: {len(current_ids)}')
    ps = get_projects_structure(current_ids, projects)
    print(f'Len ps: {len(ps)}')
    filtered_ps = [i for i in ps if 'pdf' in i.path.suffix]
    print(f'Len filtered_ps: {len(filtered_ps)}')
    lps = get_last_projects_structure(current_ids, filtered_ps)
    print(f'Len lps: {len(lps)}')
    # pl(lps)
    print('Journals')
    js = get_journals_structure(current_ids, journals)
    # filtered_js = [i for i in js if '.xlsx' in i.path]
    print(f'Len js: {len(js)}')
    ljs = get_last_journals_structure(current_ids, js)
    print(f'Len jps: {len(ljs)}')
    # pl(ljs)

    # print('get_param_by_field')
    # print(get_param_by_field(lps, 'nam', current_ids[0], 'rev'))
    init_id_kit(lps, ljs, path_to_save_id)
debug()

# TODO
# get last rev for journals
# create repository tree
# copy project and journal
# rename journal
# template for project tree