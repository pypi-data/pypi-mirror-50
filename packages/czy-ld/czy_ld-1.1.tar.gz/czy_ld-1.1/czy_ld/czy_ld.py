'''
@File       : czy_ld.py
@Copyright  : Rainbol
@Date       : 2019/8/13
@Desc       :
'''
import os
import platform
import re
import sys


class Rec_del_of_files(object):
    '''递归删除指定目录下的所有文件,所有文件夹不会删除,可以指定过滤条件'''

    def __init__(self, profile_load, keep_files=None):
        '''

        :param profile_load: 要删除的文件目录地址
        :param keep_files: 过滤文件 或者 文件夹 名称
        '''
        self.profile_load = profile_load
        self.keep_files = keep_files

    def is_file(self, upload):
        return os.path.isfile(upload)

    def split_plus(self, path):
        '''全路径分割'''
        if platform.system().lower() == 'linux':
            return path.split(os.path.sep)
        else:
            return path.split(os.path.sep)[1:]

    def little_regular(self, args, files_str):
        _list = ''
        for l in args:
            if l in ['/', '\\', '\\\\']:
                raise ('不支持完成路径')
            if l == '*':
                l = '.*'
            elif l == '?':
                l = '.'
            else:
                pass
            _list = _list + l
        res = re.findall(_list, files_str)
        if not res: return None
        l = self.split_plus(files_str)
        for y in res:
            if os.path.split(y)[1] in l:
                return True
            else:
                return None

    def walk_run(self):
        res = input("是否要进行递归删除目录为: %s 内的文件" % self.profile_load)
        if res == 'y' or 'yes' or 'ok' or 'okey':

            for path, dirs, files in os.walk(self.profile_load):
                for specify_file in files:
                    rule = False
                    split_path = self.split_plus(path + os.path.sep + specify_file)
                    keep_list = self.keep_files
                    if self.keep_files:  # 走过滤条件
                        if isinstance(self.keep_files, str):
                            if keep_list == specify_file or self.little_regular(keep_list,
                                                                                path + os.path.sep + specify_file):  # or keep_list in split_path:
                                print(path + os.path.sep + specify_file, '=====>skip')
                                rule = True
                        else:
                            keep_list = [_file for _file in self.keep_files]
                            for split_file in keep_list:
                                if self.little_regular(split_file,
                                                       path + os.path.sep + specify_file) or split_file == specify_file or split_file in split_path:
                                    print(path + os.path.sep + specify_file, '=====>skip')
                                    rule = True
                    if not rule:
                        if keep_list not in files:  # 该文件没有在过滤文件内
                            print(path + os.path.sep + specify_file, '=====>is_delete')
                            os.remove(path + os.path.sep + specify_file)  # 删除文件


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) >= 2:
        fit = None
        if '-f' in args:
            value = args.count('-f')
            fit = args[value]
        if '-p' in args:
            value = args.count('-p')
            upload = args[value]
        else:
            quit('-p为必填参数')
        print(1)
        if '-h' in args or '--help' in args:
            quit('-v\tversion 1.0 \n-p\t["路径"] 如:\t"/usr/local/bin"\n-k\t过滤条件 如:\t"*.py"\n\t\t\t["index.html","index.php"]')
        print('x')
        try:
            ex = Rec_del_of_files(upload, fit)
            ex.walk_run()
        except Exception as e:
            quit(e)
    else:
        quit('请输入参数 --help 帮助')
