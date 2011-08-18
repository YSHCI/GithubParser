#parseSouce v1.0
##����� : parse_Repo.xls(�Ľ̴�� �ּ�)�� ���� ������ ����-> ���� -> Parse_Source.xls�� ���

#�Ϸ���
## no. of watch
## no. of fork
## Forked form

#Todo list
## �ּ� �߰�
## �ʿ���� �׸� ����
## ��� �и� (������ ����)
## �ּ� ����Ʈ���� �ִµ� ���� ������ �̸� ��¾��???

import xlwt  #�ܺ� ���̺귯��
import xlrd  #�ܺ� ���̺귯��
import urllib
from sgmllib import SGMLParser



#### �Ľ� Ŭ���� (ParseSource) ######(�ѹ� ����Ǹ� �� ������ ������ �����Ѵ�)########################################################################
class ParseSource(SGMLParser):


    #######����##############################################################################################################################
    def reset(self): 
        SGMLParser.reset(self)
        self.in_a_watchers = 0
        self.in_a_forks = 0
        self.in_div = 0
        self.in_fork_flag = 0
        self.in_a_branch = 0 #
        self.in_a_tag = 0 #
        self.exist_in_fork_flag = 0                             ##### ���� üũ (�����ϳ��� ������ �ִ� ���� ���� üũ�� �ؾ��Ѵ�) ���ȭ �ؼ� ���� �ִ� ����� ��������... ��
        
    #######����ġ ���########################################################################################################################
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
                    self.exist_in_fork_flag = 1                                          ##### ���� üũ (������ ���Ⱦ��ٴ� ������ ����) �ݴ� �ñ�� ����, ���¿ܿ���


         
    #######�ڵ鷯 (�����͸� ����Ʈ�� ����)##############################################################################################################    
    def handle_data(self, data):
        if self.in_a_watchers:
            repo_watchers.append(data)
            if self.exist_in_fork_flag == 0:                               ##### ���� üũ
               repo_flags.append("core-repo")                      ##### (������ 1���� �����ϴ� ������ ����Ͽ� �����Ѵ�.)
        elif self.in_a_forks:
            repo_forks.append(data)
        elif self.in_fork_flag == 1:
            repo_flags.append(data.strip())
        elif self.in_a_branch == 1:   #
            repo_branch.append(data)  #
        elif self.in_a_tag == 1:   #
            repo_tag.append(data)  # 
        
            
#######����Ʈ ����############################################################################################################################         
repo_watchers = []
repo_forks = []
repo_flags = []
repo_branch = [] #
repo_tag = [] #



#######����Ʈ <-> ���� ############################################################################################################################
def parse_source():
    wbk = xlrd.open_workbook('Parse_Repo.xls') ## �ּ� ��� �ҷ����� (wbk)
    sheet = wbk.sheet_by_index(0)              ## ��Ʈ ���� (sheet)

    wbk1 = xlwt.Workbook()                                     ##���ο� ���� ���� (wbk1)
    sheet1 = wbk1.add_sheet('sheet1', cell_overwrite_ok=True)  ## ��Ʈ ���� (sheet1)

    i = 0
    for i in range(sheet.nrows):
        addr = sheet.cell(i, 2).value  #�ּҽ�Ʈ�� addr�� ���� (sheet -> addr)
        sheet1.write(0, 0, 'address')  #���ο� ��Ʈ�� �ּ� ���� (addr -> sheet1)
        sheet1.write(i+1, 0, addr)     #���ο� ��Ʈ�� �ּ� ���� (addr -> sheet1)
        sock = urllib.urlopen("https://github.com" + addr) ####������ �ҷ����� #���Ͽ� ���� �ּ� �Է�
        htmlSource = sock.read()                           # ����
        parseSource = ParseSource()                        ####�Ľ̽��� #parse source class�� �ҷ���
        parseSource.feed(htmlSource)                       #�߸𸣰���
        parseSource.close()                                #���� ,, 1~~~ �� �ö�

        print i                      ### ��Ȳ ����͸���(�������� �������� ī��Ʈ)

    #####�Ľ� ����� �Է� (list -> ���� ��Ʈ)#####################################################################################################
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


    ##### ����    
    wbk1.save('Parse_Source.xls')


####�ٷ��� parse_source() ���� ##################################################################################################################    
parse_source()
        
                             
