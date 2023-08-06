import json
from os import makedirs
from time import sleep


class MinecraftVersionTranslator:

    def __init__(self,
                 extracted_version_folder_name,
                 translate_function,
                 translate_endpoem_credits_splashes=True,
                 # no need for the .json here
                 language_file_to_translate="en_us",
                 # Not here either
                 new_language_file_name="default_translation",
                 language_name="Translation by MinecraftVersionTranslator",
                 language_description="Translated via MinecraftVersionTranslator",
                 language_region="US",
                 language_bidirectional=False
                 ):
        self.actual_folder_name = extracted_version_folder_name
        self.new_folder_name = extracted_version_folder_name + " - " + language_name
        self.folder_name = extracted_version_folder_name + '/assets/minecraft'
        self.translate_function = translate_function
        self.language_file_to_translate = language_file_to_translate
        self.new_language_file_name = new_language_file_name
        self.language_name = language_name
        self.language_description = language_description
        self.language_region = language_region
        self.language_bidirectional=language_bidirectional
        self.translate_endpoem_credits_splashes = translate_endpoem_credits_splashes

    def __translate_key(self, key):
        original_value = self.lang_json[key]
        self.lang_json[key] = self.translate_function(self.lang_json[key])
        print('Translated "{}" to "{}"'.format(original_value, self.lang_json[key]))

    def __translate_language_json(self):
        print("Translating language json.")
        lang_json = open(self.folder_name + '/lang/' + self.language_file_to_translate + '.json', 'rb').read().decode()
        lang_json = json.loads(lang_json)
        self.lang_json = lang_json
        for key in lang_json.keys():
            successful = False
            retry_count = 0
            while successful is False:
                try:
                    self.__translate_key(key)
                    successful = True
                except Exception as e:
                    retry_count += 1
                    print(str(e))
                    print("An error has occured. retrying from last translation within 5 seconds. retries left until skipping: " + str(retry_count) + " out of 3")
                    if (retry_count is 3):
                        print("Retry count reached, skipping")
                        successful = True
                    sleep(5)
        return self.lang_json

    def __translate_plain_text(self, file_path):
        return self.translate_function(open(file_path, 'r', encoding='utf-8').read())

    def __translate_texts(self):
        print("Translating credits.txt")
        credits = self.__translate_plain_text(self.folder_name + '/texts/credits.txt')
        print("Translating end.txt")
        end = self.__translate_plain_text(self.folder_name + '/texts/end.txt')
        print("Translating splashes.txt")
        splashes = self.__translate_plain_text(self.folder_name + '/texts/splashes.txt')
        print("Done translating.")
        return credits, end, splashes

    def __make_new_texture_dir(self):
        try:
            makedirs(self.new_folder_name + '/assets/minecraft/lang')
            makedirs(self.new_folder_name + '/assets/minecraft/texts')
        except FileExistsError:
            pass

    def __write_text(self, text, path):
        open(path, 'wb').write(text.encode())

    def __write_texts(self, credits, end, splashes):
        print("Writing credits.txt")
        self.__write_text(credits, self.new_folder_name + '/assets/minecraft/texts/credits.txt')
        print("Writing end.txt")
        self.__write_text(end, self.new_folder_name + '/assets/minecraft/texts/end.txt')
        print("Writing splashes.txt")
        self.__write_text(splashes, self.new_folder_name + '/assets/minecraft/texts/splashes.txt')

    def __create_pack_mcmeta(self):
        mcmeta = {
            "pack":
                {
                    "pack_format": 4,
                    "description": self.language_description
                },
            "language":
                {
                    self.new_language_file_name:
                        {
                            "name": self.language_name,
                            "region": self.language_region,
                            "bidirectional": self.language_bidirectional
                        }
                }
        }
        return json.dumps(mcmeta)

    def create_resource_pack(self):
        self.__make_new_texture_dir()
        if (self.translate_endpoem_credits_splashes):
            credits, end, splashes = self.__translate_texts()
            self.__write_texts(credits, end, splashes)
        language_json = json.dumps(self.__translate_language_json(), indent=4)
        print("Writing " + self.new_language_file_name + ".json")
        self.__write_text(language_json, self.new_folder_name + '/assets/minecraft/lang/' + self.new_language_file_name + ".json")
        print("Writing pack.mcmeta")
        self.__write_text(self.__create_pack_mcmeta(), self.new_folder_name + '/pack.mcmeta')
        print("All done.")