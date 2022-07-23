import os


class Settings():

    encoding = 'UTF-8'
    filename1 = '1.txt'
    filename2 = '2.txt'
    filename3 = '3.txt'
    folder = 'files'
    filename_cook = 'recipes.txt'
    filename_out = 'out.txt'
    path1 = os.path.join(os.getcwd(), folder, filename1)
    path2 = os.path.join(os.getcwd(), folder, filename2)
    path3 = os.path.join(os.getcwd(), folder, filename3)
    path_cook = os.path.join(os.getcwd(), filename_cook)
    path_out = os.path.join(os.getcwd(), folder, filename_out)


class CookBook():

    def __load_cook_book():
        dict_ = dict()
        with open(Settings.path_cook, encoding=Settings.encoding) as f:
            while True:
                dish = f.readline().strip('\n')
                dict_[dish] = []

                ingr_count = int(f.readline().strip('\n'))

                for i in range(ingr_count):
                    ingredient = f.readline().strip('\n',).split('|')
                    dict_[dish] += [{'ингридиент': ingredient[0].strip(), 
                                    'количество': int(ingredient[1].strip()),
                                    'мера': ingredient[2].strip()}]
                                    
                if not f.readline(): break

        return dict_

    cook_book = __load_cook_book()

    def get_shop_list_by_dishes(self, dishes, person_count):
        try:
            shop_list = dict()
            for dish in dishes:
                for v in self.cook_book[dish]:
                    ingredient = list(v.values())[0]
                    measure = list(v.values())[2]
                    quantity = list(v.values())[1] * person_count
                    try:
                        shop_list[ingredient]['количество'] += quantity 
                    except KeyError:
                        shop_list[ingredient] = {'мера': measure, 
                                            'количество': quantity}
        except KeyError: 
            return f'Ошибка. Блюда "{dish}" в списке нет'

        return shop_list 


class FileEditor():

    def __get_file_content(self, filename):
        with open(filename, encoding=Settings.encoding) as f:
            return f.readlines()
    
    def __merge_files(self):
        merged_file = {
            Settings.filename1: self.__get_file_content(Settings.path1), 
            Settings.filename2: self.__get_file_content(Settings.path2), 
            Settings.filename3: self.__get_file_content(Settings.path3)}
        return dict(sorted(merged_file.items(), key=lambda x: len(x[1])))

    def __save_file(self, filename, content):
        with open(filename, 'w', encoding=Settings.encoding) as f:
            f.write(content)

    def file_processing(self):
        final_text = ''

        for filename, rows in self.__merge_files().items():
            final_text += f'{filename}\n'
            for number, row in enumerate(rows):
                final_text += f'строка {number + 1}: ' + row
            final_text += '\n'
        
        self.__save_file(Settings.path_out, final_text)

        return final_text
        

recipes = CookBook()
files = FileEditor()

print(recipes.cook_book, end='\n\n')
print(recipes.get_shop_list_by_dishes(['Фахитос', 'Омлет'], 10), end='\n\n')

print(files.file_processing())