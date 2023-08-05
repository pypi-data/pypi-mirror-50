import sys
import os
from zlairflow.dag.data import data_common
from zlairflow.dag.data import data_diqu_db_a
from zlairflow.dag.data import data_diqu_db_b
from zlairflow.dag.data import data_diqu_db_c


def write_dag(quyu, dirname, conp="kunming",pool="abc_a",**krg):
    para = {
        "tag": "cdc",
        "start_date": "(2019,7,26)",
        "cron": "0 0/12 * * *",
        "timeout": 'minutes=240',

    }
    para.update(krg)
    tag = para["tag"]
    start_date = para["start_date"]

    cron = para["cron"]

    timeout = para["timeout"]


    filename = "%s_f.py" % quyu
    path1 = os.path.join(os.path.dirname(__file__), 'template', 'common.txt')
    path2 = os.path.join(dirname, filename)

    with open(path1, 'r', encoding='utf8') as f:
        content = f.read()

    # from ##zlsrc.anqing## import ##task_anqing##

    content = content.replace("##task_anqing##", quyu)

    # tag='##cdc##'
    # datetime##(2019,4,27)##, }

    content = content.replace("##cdc##", tag)
    content = content.replace("##(2019,1,1)##", start_date)


    content = content.replace("##quyuName##", "%s" % quyu)

    content = content.replace("##kunming##", "%s" % conp)

    content = content.replace("##0 0/12 * * *##", cron)
    content = content.replace("##abc_a##", pool)

    content = content.replace("##anqing_a1##", "%s_a1" % quyu)

    content = content.replace("##minutes=60##", timeout)

    content = content.replace("##anqing_b1##", "%s_b1" % quyu)

    content = content.replace("##anhui_anqing##", quyu)

    with open(path2, 'w', encoding='utf-8') as f:
        f.write(content)


# write_dag('anhui_bozhou',sys.path[0])

def write_dags_common(dirname, conp="kunming",pool="abc_a4",**krg):
    for w in data_common.para:
        quyu = w[0]
        timeout = w[1]
        krg.update({"timeout": timeout})

        write_dag(quyu, dirname,conp,pool=pool, **krg)

def write_dags_a(dirname, conp="kunming",pool="abc_a1", **krg):
    for w in data_diqu_db_a.para:
        quyu = w[0]
        timeout = w[1]
        krg.update({"timeout": timeout})

        write_dag(quyu, dirname, conp,pool=pool, **krg)

def write_dags_b(dirname, conp="kunming", pool="abc_a2",**krg):
    for w in data_diqu_db_b.para:
        quyu = w[0]
        timeout = w[1]
        krg.update({"timeout": timeout})

        write_dag(quyu, dirname, conp,pool=pool, **krg)

def write_dags_c(dirname, conp="kunming",pool="abc_a3", **krg):
    for w in data_diqu_db_c.para:
        quyu = w[0]
        timeout = w[1]
        krg.update({"timeout": timeout})

        write_dag(quyu, dirname, conp,pool=pool, **krg)


# write_dag('guandong_dongguan',r'C:\Users\jacky\Desktop\zhulongall\zlairflow\zlairflow\data',start_date='(2019,6,17)',tiemout='minutes=120')