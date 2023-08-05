import re
import os

class Container:

    directory_list = ['1.QVD','2.Config', '3.Include', '4.Export','5.Import','6.Misc']
    container_exception = ['99.Shared_Folders','0.Administration','Documentation']

    def __init__(self, container_path = os.getenv('CI_PROJECT_DIR'), deep=3):

        self.container_path = container_path
        self.container_name = container_path.split('\\')[-1]
        #self.container_name = container_name,
        self.deep_path = len(container_path.split('\\'))

    def set_container_path(self, path):
        self.container_path = path

    def is_valid_container(self):
        list_of_repos = self.container_name.split('.')
        if(list_of_repos[0]!=''):
            if(os.path.isfile(self.container_path)):
                return False
            else:
                return True
        return False

    def get_custom_path(self, directory_index=2):
        return self.container_path + '/' + self.directory_list[directory_index] + '/' + '3.Custom/'

    def get_application_path(self, directory_index=5):
        return self.container_path + '/' + self.directory_list[directory_index] + '/' + 'Application/'

    def get_sub_path(self, directory_index=2):
        return self.container_path + '/' + self.directory_list[directory_index] + '/' + '4.Sub/'

    def get_files(self,path):
        return os.listdir(path)

    def is_container_repository(self):
        container_files = ';'.join(self.get_files(self.container_path))
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


