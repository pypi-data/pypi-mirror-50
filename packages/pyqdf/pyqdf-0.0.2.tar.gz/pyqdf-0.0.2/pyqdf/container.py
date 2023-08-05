import re
import os

class Container:

    directory_list = ['1.QVD','2.Config', '3.Include', '4.Export','5.Import','6.Misc']
    container_exception = ['99.Shared_Folders','0.Administration','Documentation']
    container_map_directory =  '1.BaseVariable\\ContainerMap.csv'

    def __init__(self, container_path = os.getenv('CI_PROJECT_DIR'), directory_path=os.getenv('CI_PROJECT_DIR')):
        self.directory_path = directory_path.replace('\\','/')
        self.container_fullpath = container_path.replace('\\','/')
        self.container_name = container_path.split('/')[-1]
        self.deep_path = len(container_path.split('/'))
        self.container_map_path = self.container_fullpath + '/' + self.directory_list[2] + '/' + self.container_map_directory

    def set_container_path(self, path):
        self.container_fullpath = path

    def is_valid_container(self):
        list_of_repos = self.container_name.split('.')
        if(list_of_repos[0]!=''):
            if(os.path.isfile(self.container_fullpath)):
                return False
            else:
                return True
        return False

    def get_container_path(self):
        if(self.is_valid_container()):
            if(self.is_container_repository()):
                return re.sub(self.directory_path,'', self.container_fullpath)[1:]
                

    def get_custom_path(self, directory_index=2):
        return self.container_fullpath + '/' + self.directory_list[directory_index] + '/' + '3.Custom/'

    def get_application_path(self, directory_index=5):
        return self.container_fullpath + '/' + self.directory_list[directory_index] + '/' + 'Application/'

    def get_sub_path(self, directory_index=2):
        return self.container_fullpath + '/' + self.directory_list[directory_index] + '/' + '4.Sub/'

    def get_files(self,path):
        return os.listdir(path)

    def is_container_repository(self):
        container_files = ';'.join(self.get_files(self.container_fullpath))
        return len(re.findall(self.directory_list[0], container_files)) > 0 if True else False

    def is_container_exception(self):
        has_exception = False
        for exception in self.container_exception:
            if (self.container_name == exception):
               has_exception = True

        return has_exception

    def get_custom_files(self):
        return ';'.join(os.listdir(self.get_custom_path())).lower()

    def get_sub_files(self):
        return ';'.join(os.listdir(self.get_sub_path())).lower()

    def get_application_files(self):
        return ';'.join(os.listdir(self.get_application_path())).lower()

    def has_application_qvf(self):
        return len(re.findall('.qvf', self.get_application_files()))>0 if True else False

    def has_custom_scripts(self):
        return len(re.findall('.qvs', self.get_custom_files()))>0 if True else False

    def has_transform_scripts(self):
        return len(re.findall('(?<=transform).*?.qvs', self.get_custom_files()))>0 if True else False
    
    def has_extraction_scripts(self):
        return len(re.findall('(?<=extract).*?.qvs', self.get_custom_files()))>0 if True else False

    def has_load_scripts(self):
        return len(re.findall('(?<=load).*?.qvs', self.get_custom_files()))>0 if True else False


    def get_container_prefix(self):
        
        self.container_map = open(self.container_map_path,'r', encoding='utf8').read()
        search_term = r'(?<!,).*{}?'.format(self.get_container_path().replace('/', r'\\'))
       
        return ''.join(re.findall(search_term, self.container_map)).split(',')[0]
       

