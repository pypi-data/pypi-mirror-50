import json
import os
import pandas as pd
from sqlalchemy import create_engine
from lmf.dbv2 import db_query, db_command

o_path = os.path.dirname(__file__)


def file_to_db(conp):
    """
    将本地 quyu_time_func.json 文件 同步到目标数据库中的 quyu_time_func 表，覆盖原有的。
    :param conp:
    :return:
    """
    enter_value = input('这是本地 quyu_time_func.json 覆盖数据库的操作，确认（y）?')
    if enter_value.lower() == 'y':
        file_path = os.path.join(o_path, 'quyu_time_func.json')

        with open(file_path, encoding='utf-8') as f:
            quyu_func_dict = json.load(f)
        df = pd.DataFrame.from_dict(quyu_func_dict, orient='index')
        df.reset_index(inplace=True)
        df.columns = ['quyu', 'time_func']
        df['info'] = None
        con = create_engine("postgresql://%s:%s@%s/%s" % (conp[0], conp[1], conp[2], conp[3]), encoding='utf-8')
        df.to_sql('quyu_time_func', con=con, if_exists='replace', index=False, schema=conp[-1])
        return
    else:
        pass


################# 对数据库 quyu_time_func 进行 增删改 #############################
def update(quyu, time_func, conp):
    try:
        select(quyu,conp)
        sql = '''update %s.quyu_time_func set time_func=$$%s$$ where quyu=$$%s$$''' % (conp[-1], time_func, quyu)
        db_command(sql, dbtype='postgresql', conp=conp)
    except:
        insert(quyu, time_func, conp)


def insert(quyu, time_func, conp):
    sql = ''' insert into %s.quyu_time_func (quyu,time_func) values ($$%s$$,$$%s$$)''' % (conp[-1], quyu, time_func)
    db_command(sql, dbtype='postgresql', conp=conp)


def delete(quyu, conp):
    sql = '''delete from %s.quyu_time_func where quyu = $$%s$$''' % (conp[-1], quyu)
    db_command(sql, dbtype='postgresql', conp=conp)


def select(quyu, conp):
    sql = '''select time_func from %s.quyu_time_func where quyu = $$%s$$''' % (conp[-1], quyu)
    df = db_query(sql, dbtype='postgresql', conp=conp)
    func_name = df.values.tolist()[0][0]
    return func_name


################### 对 exec_func_f.py 这个文件进行操作 ##################
def add_time_func(func_name):
    file_path = os.path.join(o_path, 'exec_func_f.py')
    with open(file_path, 'r', encoding='utf-8') as f:
        contents = f.read()
    if func_name not in contents:
        contents = contents.replace('##func_name##:##func_name##', ''''%s':%s,''' % (func_name, func_name) + '''\n    ##func_name##:##func_name##''')

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(contents)
        print('< %s > 函数映射增加成功。' % func_name)
    else:
        print('< %s > 函数映射已经存在。' % func_name)


def del_time_func(func_name):
    file_path = os.path.join(o_path, 'exec_func_f.py')
    new_contents = ''
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.readlines()
    for cont in content:
        if func_name not in cont:
            new_contents += cont
        else:
            print('<%s> 函数在 exec_func_f.py 中删除成功。' % func_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_contents)


################### 对 common.py 这个文件进行操作 ##################
def add_common_func(func):
    file_path = os.path.join(o_path, 'common.py')
    with open(file_path, 'r', encoding='utf-8') as f:
        contents = f.read()
    func_name = ' '.join(func.split()[:2])
    if func_name not in contents:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(func+'\n\n')
        print('<%s> 函数在 common.py 中添加成功' % func_name)
    else:
        print('<%s> 函数已经存在，添加失败。' % func_name)


def del_common_func(func):
    file_path = os.path.join(o_path, 'common.py')
    with open(file_path, 'r', encoding='utf-8') as f:
        contents = f.read()
    func_name = ' '.join(func.split()[:2])
    index1 = int(contents.find(func_name))
    if func_name in contents:
        new_contents = contents[:index1] + contents[index1 + len(func) + 1:]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_contents)
        print('<%s> 函数在 common.py 中删除成功。' % func_name)
    else:
        print('<%s> common.py 中没有此函数，删除失败。' % func_name)


def add_func(func):
    func_name = func.split(' ')[1].split('(')[0]
    add_common_func(func)
    add_time_func(func_name)


def delete_func(func):
    func_name = func.split(' ')[1].split('(')[0]
    del_common_func(func)
    del_time_func(func_name)


#################### 'quyu_time_func.json' 操作本地json文件 ########################
def add_quyu_time_func_json(quyu_name, time_func):
    file_path = os.path.join(o_path, 'quyu_time_func.json')
    with open(file_path, encoding='utf-8') as f:
        quyu_time_func_json = json.load(f)
    if quyu_name not in quyu_time_func_json.keys():
        quyu_time_func_json.update({quyu_name: time_func})
        print('quyu < %s > 添加方法 < %s > 完成！' % (quyu_name, time_func))
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(quyu_time_func_json, f)
    else:
        print('quyu < %s > 已经存在，请确认后再进行操作。' % (quyu_name))


def del_quyu_time_func_json(quyu_name, time_func):
    file_path = os.path.join(o_path, 'quyu_time_func.json')
    with open(file_path, encoding='utf-8') as f:
        quyu_time_func_json = json.load(f)
    if quyu_name not in quyu_time_func_json.keys():
        print('quyu < %s > 不在字典中，请确认后再进行操作。' % (quyu_name))
    else:
        quyu_time_func_json.pop(quyu_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(quyu_time_func_json, f)
        print('quyu < %s > 已删除。' % (quyu_name))


def update_quyu_time_func_json(quyu_name, time_func):
    file_path = os.path.join(o_path, 'quyu_time_func.json')
    with open(file_path, encoding='utf-8') as f:
        quyu_time_func_json = json.load(f)
    if quyu_name in quyu_time_func_json.keys():
        del_quyu_time_func_json(quyu_name, time_func)
    add_quyu_time_func_json(quyu_name, time_func)
    print('quyu < %s > 更新成功。' % (quyu_name))


if __name__ == '__main__':
    funcx1xx = '''def extime_v2xxxxxx(ggstart_time,page):
    if ggstart_time is not None:
        res = ggstart_time
    else:
        res = extime(ggstart_time,page)
    return res'''
    # add_quyu_time_func_json(funcxxx,2)
    # delete_func(funcxxx)
    # update_quyu_time_func_json('shandong_weifang_ggzy','extime_xxsj')
    # del_quyu_time_func_json('xxxxxxxxxxxxx',11111111111111111)
    # conp = ["postgres", "since2015", "192.168.3.171", "anbang", "test"]
    # file_to_db(conp)
    # update('jiangsu_nanjing_gzy','xxxx', conp)
    # print(select('jiangsu_nanjing_gzy', conp))
    # delete('jiangsu_nanjing_gzy',conp)

    funcxxx = r'''def extime_qycg_eps_hnagroup_com(ggstart_time, page):
    soup = BeautifulSoup(page, 'lxml')
    txt = re.sub('[^\u4E00-\u9Fa5a-zA-Z0-9:：\-\\/]', '', soup.text.strip())
    p = "(20[0-2][0-9])[\-\.年\\/]([1-9]|[0][1-9]|[1][0-2])[\-\.\\月/]([0-9]{,2})发布于"
    a = re.findall(p, txt.replace('documentwrite', ''))
    # print(a)
    if a != []:
        return '-'.join(a[0])
    return None'''
    # delete_func(funcxxx)
    add_func(funcxxx)

