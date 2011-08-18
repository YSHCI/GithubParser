#parseSouce v1.0
##사용방법 : parse_Repo.xls(파싱대상 주소)와 같은 폴더에 저장-> 실행 -> Parse_Source.xls로 출력

#완료목록
## no. of watch
## no. of fork
## Forked form

#Todo list
## 주석 추가
## 필요업는 항목 삭제
## 모듈 분리 (재사용을 위한)
## 주소 리스트에는 있는데 없는 페이지 이면 어쩐다???

import xlwt  #외부 라이브러리
import xlrd  #외부 라이브러리
import urllib
from sgmllib import SGMLParser



#### 파싱 클래스 (ParseSource) ######(한번 실행되면 그 페이지 내에서 루핑한다)########################################################################
class ParseSource(SGMLParser):


    #######리셋##############################################################################################################################
    def reset(self): 
        SGMLParser.reset(self)
        self.in_a_watchers = 0
        self.in_a_forks = 0
        self.in_div = 0
        self.in_fork_flag = 0
        self.in_a_branch = 0 #
        self.in_a_tag = 0 #
        self.exist_in_fork_flag = 0                             ##### 유뮤 체크 (만에하나라도 없을수 있는 것은 유무 체크를 해야한다) 모듈화 해서 쓸수 있는 방법이 없을려나... ㅜ
        
    #######스위치 목록########################################################################################################################
    def start_a(self, attrs):
        for k, v in attrs:
            if k == "title" and v == "Watchers":
                self.in_a_watchers = 1
            elif k == "title" and v == "Forks":
                self.in_a_forks = 1   
            elif k == "href":
                self.in_fork_flag = 0
            elif k == "class" and v == "dropdown":  #
                self.in_a_branch = 1                #
            elif k == "class" and v == "dropdown ":  #
                self.in_a_tag = 1                #
            elif k == "class" and v == "dropdown defunct":  #
                self.in_a_tag = 1                #

                
    def end_a(self):
        self.in_a_watchers = 0
        self.in_a_forks = 0
        self.in_a_branch = 0  #
        self.in_a_tag = 0  #
                

    def start_div(self, attrs):
        for k, v in attrs:
            if k == "class" and v == "title-actions-bar":
                    self.in_div = 1
            
   
    def start_span(self, attrs):
        for k, v in attrs:
            if k == "class" and v =="text":
                    self.in_fork_flag = 1
                    self.exist_in_fork_flag = 1                                          ##### 유뮤 체크 (열릴때 열렸었다는 사인을 보냄) 닫는 시기는 없다, 리셋외에는


         
    #######핸들러 (데이터를 리스트에 삽입)##############################################################################################################    
    def handle_data(self, data):
        if self.in_a_watchers:
            repo_watchers.append(data)
            if self.exist_in_fork_flag == 0:                               ##### 유뮤 체크
               repo_flags.append("core-repo")                      ##### (무조건 1번씩 존재하는 변수에 기생하여 들어가야한다.)
        elif self.in_a_forks:
            repo_forks.append(data)
        elif self.in_fork_flag == 1:
            repo_flags.append(data.strip())
        elif self.in_a_branch == 1:   #
            repo_branch.append(data)  #
        elif self.in_a_tag == 1:   #
            repo_tag.append(data)  # 
        
            
#######리스트 생성############################################################################################################################         
repo_watchers = []
repo_forks = []
repo_flags = []
repo_branch = [] #
repo_tag = [] #



#######리스트 <-> 엑셀 ############################################################################################################################
def parse_source():
    wbk = xlrd.open_workbook('Parse_Repo.xls') ## 주소 목록 불러오기 (wbk)
    sheet = wbk.sheet_by_index(0)              ## 시트 선택 (sheet)

    wbk1 = xlwt.Workbook()                                     ##새로운 엑셀 생성 (wbk1)
    sheet1 = wbk1.add_sheet('sheet1', cell_overwrite_ok=True)  ## 시트 선택 (sheet1)

    i = 0
    for i in range(sheet.nrows):
        addr = sheet.cell(i, 2).value  #주소시트를 addr에 저장 (sheet -> addr)
        sheet1.write(0, 0, 'address')  #새로운 시트에 주소 저장 (addr -> sheet1)
        sheet1.write(i+1, 0, addr)     #새로운 시트에 주소 저장 (addr -> sheet1)
        sock = urllib.urlopen("https://github.com" + addr) ####페이지 불러오기 #소켓에 오픈 주소 입력
        htmlSource = sock.read()                           # 열기
        parseSource = ParseSource()                        ####파싱실행 #parse source class를 불러움
        parseSource.feed(htmlSource)                       #잘모르겟음
        parseSource.close()                                #닫음 ,, 1~~~ 쭉 올라감

        print i                      ### 상황 모니터링용(한페이지 볼때마다 카운트)

    #####파싱 결과물 입력 (list -> 엑셀 시트)#####################################################################################################
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

    m = 1
    for flag in repo_flags:
        sheet1.write(0, 3, 'Core')
        sheet1.write(m, 3, flag)
        m += 1

    q = 1                                  # 
    for branch in repo_branch:             #     
        sheet1.write(0, 4, 'No. of Branch')# 
        sheet1.write(q, 4, branch)         # 
        q += 1                             # 

    r = 1                                  # 
    for branch in repo_branch:             #     
        sheet1.write(0, 5, 'No. of tag')   # 
        sheet1.write(r, 5, branch)         # 
        r += 1                             # 


    ##### 저장    
    wbk1.save('Parse_Source.xls')


####바로위 parse_source() 실행 ##################################################################################################################    
parse_source()
        
                             
