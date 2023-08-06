# Insert your code here. 

class File:

    @staticmethod
    def readlines(file_name):
        lines = []
        with open(file_name, encoding="utf_8_sig") as f: # 默认为utf8编码
            for line in f.readlines():
                line = line.strip() # 去掉无关空白
                if line: # 去掉空行
                    lines.append(line)
        return lines
    
    @staticmethod
    def writelines(file_name:str, lines:[]):
        with open(file_name, "w", encoding='utf_8_sig') as f:
            f.write('\n'.join(lines))
    