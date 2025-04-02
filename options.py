import configparser
from cryptography.fernet import Fernet

class Options():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('options.ini')


    def decode(self, password):   #Дешифровка пароля
        try:
            strong = 'btsbrest'
            key = f"{strong}{self.config.get('MAIN','key')}"   # загрузка ключа из внешнего источника
            cipher = Fernet(key)
            return cipher.decrypt(password).decode()
        except:
            return password


    def read_config_json(self):
        pass



    def read_config(self):
        option = {}

        values = {}
        values['gs1'] = self.config.get('MAIN','gs1')
        values['work'] = self.config.get('MAIN','workfolder')
        values['output'] = self.config.get('MAIN','output')
        values['theme'] = self.config.get('MAIN','theme')
        values['printer'] = self.config.get('MAIN','printer')
        option['MAIN'] = values

        values = {}
        values['rows'] = self.config.getint('PDF','rows')
        values['cols'] = self.config.getint('PDF','cols')
        values['zoom_x'] = self.config.getint('PDF','zoom_x')
        values['zoom_y'] = self.config.getint('PDF','zoom_y')
        values['anchor_x'] = self.config.getint('PDF','anchor_x')
        values['anchor_y'] = self.config.getint('PDF','anchor_y')
        values['frame_x'] = self.config.getint('PDF','frame_x')
        values['frame_y'] = self.config.getint('PDF','frame_y')
#        values['code_x'] = self.config.getint('PDF','code_x')
#        values['code_y'] = self.config.getint('PDF','code_y')
        values['dx'] = self.config.getint('PDF','dx')
        values['dy'] = self.config.getint('PDF','dy')
        option['PDF'] = values

        values = {}
        values['host'] = self.config.get('MYSQL','host')
        values['database'] = self.config.get('MYSQL','database')
        values['user'] = self.config.get('MYSQL','user')
        values['password'] = self.decode(self.config.get('MYSQL','password'))  
        option['MYSQL'] = values

        values = {}
        values['back'] = self.config.get('LABEL','back')
        values['label'] = self.config.getboolean('LABEL','label')
        values['left'] = self.config.getint('LABEL','left')
        values['top'] = self.config.getint('LABEL','top')
        values['width'] = self.config.getint('LABEL','width')
        values['height'] = self.config.getint('LABEL','height')
        values['font_size'] = self.config.getint('LABEL','font_size')
        values['label_rotate'] = self.config.getint('LABEL','label_rotate')
        values['label_align'] = self.config.getint('LABEL','label_align')
        values['label_left'] = self.config.getint('LABEL','label_left')
        values['label_top'] = self.config.getint('LABEL','label_top')
        option['LABEL'] = values

        values = {}
        values['code_quality'] = self.config.get('ZPL','code_quality')
        values['zpl'] = self.config.getboolean('ZPL','zpl')
        values['code_size'] = self.config.getint('ZPL','code_size')
        values['code_rotation'] = self.config.getint('ZPL','code_rotation')
        option['ZPL'] = values

        return option   #получить значение из конфигурационного файла

    def save_config(self):
        try:
            with open('confin_new.ini', 'w') as configfile:
                self.config.write(configfile)
            self.statusBar().showMessage(f'Сохранение конфигурации выполнено успешно...', 5000)
        except:
            self.statusBar().showMessage(f'Ошибка сохранения конфигурации...', 5000)



