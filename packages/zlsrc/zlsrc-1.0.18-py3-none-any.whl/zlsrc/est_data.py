import os
import json
from collections import OrderedDict
from pprint import pprint


def get_quyu_dict_diqu():
    dir = os.path.dirname(__file__)

    dir_list = os.listdir(dir)
    quyu_dict=OrderedDict()
    dir_delete_list = ['zlshenpi', 'zljianzhu', 'zlcommon', 'lib', 'util']
    file_delete_list = ['__init__.py', 'yzm_model.m']

    ndir_list = [x for x in dir_list if x not in dir_delete_list and os.path.isdir(os.path.join(dir,x))]

    for d in ndir_list:
        ndir = os.path.join(dir, d)
        file_list = os.listdir(ndir)
        nfile_list = [x for x in file_list if x not in file_delete_list]
        nfile_list = [x for x in nfile_list if x.endswith('.py')]
        fileList = [x.split('.py')[0] for x in nfile_list]
        quyu_dict[d]=fileList

    return quyu_dict


def get_quyu_dict_common():
    dir = os.path.dirname(__file__)
    zlcommon_dir = os.path.join(dir, 'zlcommon')
    file_list = os.listdir(zlcommon_dir)
    quyu_dict=OrderedDict()
    file_delete_list = ['__init__.py']

    nfile_list = [x for x in file_list if x not in file_delete_list]
    nfile_list = [x for x in nfile_list if x.endswith('.py')]

    fileList = [x.split('.py')[0] for x in nfile_list]

    quyu_dict['zlcommon']=fileList
    return quyu_dict

def get_quyu_dict_shenpi():
    dir = os.path.dirname(__file__)
    zlcommon_dir = os.path.join(dir, 'zlshenpi')
    file_list = os.listdir(zlcommon_dir)
    quyu_dict=OrderedDict()
    file_delete_list = ['__init__.py','default_path.txt','util_qgsp']

    nfile_list = [x for x in file_list if x not in file_delete_list]
    nfile_list = [x for x in nfile_list if x.endswith('.py')]

    fileList = [x.split('.py')[0] for x in nfile_list]

    quyu_dict['zlshenpi']=fileList
    return quyu_dict



def create_data():
    quyu_dict=OrderedDict()
    diqu_dict=get_quyu_dict_diqu()
    common_dict=get_quyu_dict_common()
    shenpi_dict=get_quyu_dict_shenpi()

    quyu_dict.update(diqu_dict)
    quyu_dict.update(common_dict)
    quyu_dict.update(shenpi_dict)
    h="quyu_dict={\n"
    ed="\n}"
    # shengs=list(quyu_dict.keys())
    # shengs.sort()

    sheng_union=[]
    for sf in quyu_dict.keys():
        sheng_prt1="""   "%s":[\n"""%sf
        sheng_prt2=',\n'.join(['''      "%s"'''%shi for shi in quyu_dict[sf]])+'\n   ]'
        sheng=sheng_prt1+sheng_prt2
        sheng_union.append(sheng)

    result=h+',\n'.join(sheng_union)+ed

    quyu_dict_str=result

    dir=os.path.dirname(__file__)
    data_path=os.path.join(dir,'data.py')

    with open(data_path,'w',encoding='utf8') as f:
        f.write(quyu_dict_str)



# create_data()

