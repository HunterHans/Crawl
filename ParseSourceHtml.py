import requests 
from bs4 import BeautifulSoup 
import os 
import json 
import pymysql 
import re

class ParseSourceHtml():
    def __init__(self):
        self.new_urls_css=''
        self.data_css=''
        self.box_key_css=''
        self.box_value_css=''   
        self.box_item_css=''
        self.rubbish=''

        self.path=os.getcwd()
        os.chdir(self.path)

  
        self.input_path=self.path+'\\output\\html'
        self.output_path=self.path+'\\output\\xml'
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

        self.file_lst=os.listdir(self.input_path)

    def extract_table(self,table):
        
        text=''
        
        for i in table.select('tr'):
            for j in i.select('th,td'):
                
                # print([k+' '+str(ord(k)) for k in j.text.strip()])

                info=j.text.strip().replace(chr(10),';').replace(chr(13),'').replace(chr(12288),' ')

                if info==';' or info =='':
                    continue
                text+=info+','

            if len(i.select('th,td'))==0:
                continue

            text+='\n'

        
        return text

    def clear_rubbish(self,tag):
        rubbish=tag.select(self.rubbish)
        for j in rubbish:
            j.extract()
    def clear_tab(self,text):
        return text.replace(chr(160),'').strip()
    
    def catch_data(self,soup):
        try:
            title=soup.select('h1')[0].text.strip()
        except Exception as e:
            print('[ERROR] catch title')
            title='null'

        
        #文本数据
        result=soup.select('h1,.level-2,.level-3,.para,table')
        #半结构化数据
        key=soup.select('.basicInfo-block  dt')
        val=soup.select('.basicInfo-block dd')


        with open('huawei'+'.xml','w',encoding='utf-8') as f:
            f.write('<?xml version="1.0" ?>'+'\n')
            f.write("<body>\n")
            if self.data_css!='':
                #文本数据
                result=soup.select(self.data_css)
                for i in result:
                    self.clear_rubbish(i)
                    info=i.text.replace(chr(32),' ').replace(chr(10),'').replace(chr(160),'')


                    if i.name=="table":
                        text=self.extract_table(i)
                        f.write("<table>")
                        f.write(text)
                        f.write("</table>"+'\n')
                    elif i.name=='h1':
                        f.write('<h1 id="1">')
                        f.write(info.strip())
                        f.write('</h1>'+'\n')

                    elif "level-2" in i.get('class'):
                        f.write('<h2 id="1">')
                        f.write(info.strip())
                        f.write('</h2>'+'\n')
                    elif "level-3" in i.get('class'):
                        f.write('<h2 id="2">')
                        f.write(info.strip())
                        f.write('</h2>'+'\n')
                    # elif i.select('b'):
                    #     f.write('<h2 id="3">')
                    #     f.write(info.strip())
                    #     f.write('</h2>'+'\n')

                    else:
                        p=i.parents
                        flag=False
                        for k in p:
                            if k.name=="table":
                                flag=True
                        if flag:
                            continue
                        if info.strip()=='':
                            continue
                        f.write("<p>")
                        f.write(info.strip()+'</p>\n')
                f.write("</body>\n")

            #半结构化数据写入
            f.write('<box>')
            box={}
            if self.box_key_css!='' and self.box_value_css!='':
                key=soup.select(self.box_key_css)
                val=soup.select(self.box_value_css)
            
                #单独定位k，v处理
                for k,v in zip(key,val):
                    self.clear_rubbish(k)
                    self.clear_rubbish(v)

                    k=self.clear_tab(k.text)
                    v=self.clear_tab(v.text)

                    box[k]=v
            if self.box_item_css!='':
                h2=soup.select(self.h2_css)
                if len(h2)>0:
                    item_h2=soup.select(self.box_item_h2_css)
                    item=self.clear_item(item_h2)
                else:
                #定位kv item处理
                    item=soup.select(self.box_item_css)
                #清洗。妈的，万万没想到这个中医药的网站会这么垃圾，，真的太垃圾了
                index=0
                for i in item:
                    try:
                        k=i.select('span')[0]
                        key=k.text
                    except Exception as e:
                        
                        box[index]=self.clear_tab(i.text)
                        index+=1
                    else:
                        k.extract()
                        v=self.clear_tab(i.text)
                        box[key]=v
            json_data=json.dumps(box,ensure_ascii=False)
            f.write(json_data+'\n')
            f.write("</box>")
            f.close()

        

    def parse(self,file):

        #
        with open(self.input_path+'\\'+file,'r',encoding='utf-8') as source_html:
            response=source_html.read()

            if not response:
                #当get失败时，加入dead_urls_tbl
                return 

            #用soup解析
            soup=BeautifulSoup(response,'lxml')
            
            self.catch_data(soup)

            self.catch_data(soup)
            source_html.close()
    def work(self):
        os.chdir(self.output_path)
        for i in self.file_lst:
            self.parse(i)

        

def main():
    psh=ParseSourceHtml()

    psh.work()
    # bc.init_urls()

if __name__=='__main__':
    main()