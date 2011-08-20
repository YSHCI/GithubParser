import xlwt
import xlrd
import urllib
from sgmllib import SGMLParser

class ParseSource(SGMLParser):   # 실제 파싱 클래스
    
    def reset(self):
        SGMLParser.reset(self)
        self.in_a_watchers = 0
        self.in_a_forks = 0
        self.in_div = 0
        self.in_fork_flag = 0
        self.check = 0
        

    def start_a(self, attrs):
        for k, v in attrs:
            if k == "title" and v == "Watchers":
                self.in_a_watchers = 1
            elif k == "title" and v == "Forks":
                self.in_a_forks = 1
            elif k == "href":
                self.in_fork_flag = 0
    def end_a(self):
        self.in_a_watchers = 0
        self.in_a_forks = 0
        self.check = 0
        

    def start_div(self, attrs):
        for k, v in attrs:
            if k == "class" and v == "title-actions-bar":
                    self.in_div = 1
##
##    def end_div(self):
##        self.in_div = 0
##
   # def start_span(self, attrs):
   #     for k, v in attrs:
   #         if k == "class" and v =="fork-from":
   #              self.check = 1
            
   
    def start_span(self, attrs):
        for k, v in attrs:
            if k == "class" and v =="text":
                #if self.check == 1:
                    self.in_fork_flag = 1


           
    #def end_h1(self):
    #    if self.in_div and self.in_fork_flag:
    #        repo_flags.append('1')
    #    if self.in_div == 1 and self.in_fork_flag == 0:
    #        repo_flags.append('0')
            
    #    self.in_fork_flag = 0
    #    self.in_div = 0
   
    #def end_span(self):
    #    self.in_fork_flag = 0
        
    def handle_data(self, data):
        if self.in_a_watchers:
            repo_watchers.append(data)
        elif self.in_a_forks:
            repo_forks.append(data)
        elif self.in_fork_flag == 1:
            repo_flags.append(data.strip())
        
repo_watchers = []
repo_forks = []
repo_flags = []

def parse_source():
    wbk = xlrd.open_workbook('Parse_Repo.xls')
    sheet = wbk.sheet_by_index(0)
    wbk1 = xlwt.Workbook()
    sheet1 = wbk1.add_sheet('sheet1', cell_overwrite_ok=True)

    i = 0
    for i in range(sheet.nrows):
        addr = sheet.cell(i, 2).value  #주소시트를 addr에 저장
        sheet1.write(0, 0, 'address')  
        sheet1.write(i+1, 0, addr)     #새로운 시트에 주소 저장
        sock = urllib.urlopen("https://github.com" + addr) #소켓에 오픈 주소 입력
        htmlSource = sock.read()                           # 열기
        parseSource = ParseSource()                        #parse source class를 불러움
        parseSource.feed(htmlSource)                    
        parseSource.close()                                # 닫음 ,, 1~~~ 쭉 올라감
        flag in repo_flags
        sheet1.write(0, 3, 'No. of Forks')
        sheet1.write(i+1, 3, flag)    

    j = 1
    for watcher in repo_watchers:
        sheet1.write(0, 1, 'No. Watchers')
        sheet1.write(j, 1, watcher)
        j += 1

    k = 1
    for fork in repo_forks:
        sheet1.write(0, 2, 'No. of Forks')
        sheet1.write(k, 2, fork)
        k += 1

    #m = 1
    #for flag in repo_flags:
    #    sheet1.write(0, 3, 'No. of Forks')
    #    sheet1.write(m, 3, flag)
    #    m += 1
        


        
    wbk1.save('Parse_Source.xls')
    
parse_source()
        
                             
