import os

from module import string_util
from module import file_util
from module import container_util

class SejongFreqMaker :
    def __init__(self) :
        self.encoding = "UTF-8"

        self.delim_morph = " + "
        self.delim_morph_lex_tag = "/"

        self.sentence_dict = {}
        self.eojeol_dict = {}
        self.emjeol_dict = {}
        self.morph_tag_lex_dict = {}

    def make_freq_folder(self, in_dir: str, encoding: str, delim_key: str) :
        self.encoding = encoding

        in_file_paths = file_util.get_file_paths(in_dir, True)

        for in_file_path in in_file_paths :
            self.make_freq_file(in_file_path, encoding, delim_key)
            print(f"in_file_path : {os.path.basename(in_file_path)} make freq complet")
    
    def make_freq_file(self, in_file_path: str, encoding: str, delim_key: str) :
        in_file = file_util.open_file(in_file_path, encoding, 'r')

        while 1 :
            line = in_file.readline()
            if not line :
                break

            line = file_util.preprocess(line)
            if string_util.is_empty(line, True) :
                continue

            # 문장 빈도 계산
            if line[:3] == "#%#" :
                line = line[3:].strip()
                container_util.add_str_int(self.sentence_dict, line, 1)
            
            # 문장이 아니라면, '어절 단위 형태소 분석 결과'
            else :
                temp = line.split(delim_key)
                temp = string_util.trim(temp, True)

                if len(temp) != 2 :
                    print(f"SejongFreqMaker.make_freq_file() input error : {line}")
                    continue

                eojeol = temp[0]
                ma_result_str = temp[1]

                # 어절 빈도 계산
                container_util.add_str_int(self.eojeol_dict, eojeol, 1)

                # 음절 빈도 계산
                emjeol_list = list(eojeol)
                for emjeol in emjeol_list :
                    container_util.add_str_int(self.emjeol_dict, emjeol, 1)
                
                # 형태소 분석 결과를 형태소 단위로 1차 분리
                # 형태소 단위를 어휘와 품사로 2차 분리하여, 어휘 리스트와 품사 리스트 반환
                morph_lex_list, morph_tag_list = self.parsing_ma_result(ma_result_str)

                for i in range(len(morph_lex_list)) :
                    morph_lex = morph_lex_list[i]
                    morph_tag = morph_tag_list[i]

                    self.add_morph_tag_lex_dict(morph_tag, morph_lex)

    '''
        형태소 분석 결과를 형태소 단위로 1차 분리
        형태소 단위를 어휘와 품사로 2차 분리하여, 어휘 리스트와 품사 리스트 반환

            input   :   [웅가로는	웅가로/NNP + 는/JX]

            return  :   [웅가로, 는], [NNP, JX]
    '''
    def parsing_ma_result(self, ma_result_str: str) :
        morph_lex_list = []
        morph_tag_list = []

        morph_units = ma_result_str.split(self.delim_morph)
        for morph_unit in morph_units :
            idx = morph_unit.rindex(self.delim_morph_lex_tag)
            
            if idx != -1 :
                morph_lex = morph_unit[:idx]
                morph_tag = morph_unit[idx+1:]

                morph_lex_list.append(morph_lex)
                morph_tag_list.append(morph_tag)
        
        return morph_lex_list, morph_tag_list

    # 품사 별로 어휘의 빈도를 계산
    # 예를 들어, '웅가로'가 'NNP'일 때, 빈도를 계산한다면, 'NNP' 중에서 '웅가로'의 빈도를 계산
    def add_morph_tag_lex_dict(self, morph_tag: str, morph_lex: str) :
        morph_lex_dict = {}

        if morph_tag in self.morph_tag_lex_dict :
            morph_lex_dict = self.morph_tag_lex_dict[morph_tag]
        else :
            self.morph_tag_lex_dict[morph_tag] = morph_lex_dict
        
        container_util.add_str_int(morph_lex_dict, morph_lex, 1)
    
    # 빈도 계산이 완료된 dict들을 out_dir의 파일로 생성
    # 빈도 순으로, 동일한 빈도라면 문자 순으로 정렬하여 파일을 생성합니다.
    def write_freq_dict(self, out_dir: str, delim_key: str) :
        print(f"\twrite_freq_dict() start")

        out_file_path = out_dir + "/sentence_freq.dict"
        file_util.write_dict(out_file_path, self.encoding, container_util.sorted_dict(self.sentence_dict), delim_key)

        out_file_path = out_dir + "/eojeol_freq.dict"
        file_util.write_dict(out_file_path, self.encoding, container_util.sorted_dict(self.eojeol_dict), delim_key)

        out_file_path = out_dir + "/emjeol_freq.dict"
        file_util.write_dict(out_file_path, self.encoding, container_util.sorted_dict(self.emjeol_dict), delim_key)

        for morph_tag in self.morph_tag_lex_dict.keys() :
            out_file_path = out_dir + "/morph_tag_lex_freq/" + morph_tag + "_freq.dict"
            morph_lex_dict = self.morph_tag_lex_dict[morph_tag]
            file_util.write_dict(out_file_path, self.encoding, container_util.sorted_dict(morph_lex_dict), delim_key)
        
        print(f"\twrite_freq_dict() end")

###########################################################################################

if __name__ == "__main__" :
    work_dir = "../"

    in_dir = work_dir + "/input_sejong/"
    out_dir = work_dir + "/output_freq/"
    encoding = "UTF-8"
    delim_key = "\t"

    sejong_freq_maker = SejongFreqMaker()
    sejong_freq_maker.make_freq_folder(in_dir, encoding, delim_key)
    sejong_freq_maker.write_freq_dict(out_dir, delim_key)
