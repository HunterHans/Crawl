import requests 
from bs4 import BeautifulSoup 
import os 
import json 
import pymysql 
import re

class Crawl():
    def __init__(self):
        with open('config/config.json','r') as f:
            data=json.load(f)
            f.close()

        self.database=data['database']
        self.host=data['host']
        self.user=data['user']
        self.password=data['password']

        self.url_search=data['url_search']+'{}'
        print(self.url_search)

        self.new_urls_css=''
        self.data_css=''
        self.box_key_css=''
        self.box_value_css=''   
        self.box_item_css=''
        self.rubbish=''

        self.path=os.getcwd()
        os.chdir(self.path)
        self.output_path=self.path+r'\output'

        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

        self.output_path_html=self.output_path+'\\html'
        if not os.path.exists(self.output_path_html):
            os.mkdir(self.output_path_html)

        self.db=pymysql.connect(self.host,self.user,self.password,self.database)
        self.cursor=self.db.cursor()

        self.new_urls=[]
        self.old_urls=[]
        self.dead_urls=[]
        self.url_pool=[]

        self.start_url=[]
        self.start_url_file=self.path+r'/config/start_url.txt'
        self.start_entity_file=self.path+r'/config/start_entity.txt'

        self.num=0
        self.max=1

    def request(self,url):
        print('Now Reques:',url)
        try:
            response=requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36',})
        except Exception as e:
            print(e)
            return None
        else:
            response.encoding='utf=8'
            return response.text

    def parse_entity_to_url(self):
        entity_lst=[]
        if os.path.exists(self.start_url_file):
            with open(self.start_url_file,'r',encoding='utf-8') as f:
                entity_lst=f.read().split('\n')
                for e in entity_lst:
                    if e=="":
                        entity_lst.remove(e)

                f.close()
        else:
            entity_lst=[]

        if os.path.exists(self.start_entity_file):
            with open(self.start_entity_file,'r',encoding='utf-8') as f:
                text=f.read().split()
                for i in text:
                    print(i)
                    url=self.url_search.format(i)
                    
                    entity_lst.append(url)
                    print(entity_lst)
                f.close()
        else:
            return 
        
        with open(self.start_url_file,'w',encoding='utf-8') as f:
            for e in entity_lst:
                f.write(e+'\n')
            f.close()

    def import_urls(self,tbl):
        sql="select url,title,relative,tags from {};".format(tbl)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
            return None 
        else:
            result=self.cursor.fetchall()
            return list(result)
    def init_urls(self):
        with open(self.start_url_file,'r',encoding='utf-8') as f:
            text=f.read().split('\n')
            for url in text:
                if url=='':
                    continue
                self.start_url.append(url)
            f.close()
        self.new_urls=self.import_urls('new_urls_tbl')
        self.old_urls=self.import_urls('old_urls_tbl')
        self.dead_urls=self.import_urls('dead_urls_tbl')
        url_list=[self.new_urls,self.old_urls,self.dead_urls]
        for l in url_list:
            for u in l:
                self.url_pool.append(u[0])
        for url in self.start_url:
            if url not in self.url_pool:
                self.insert(url,'new_urls_tbl')
                self.new_urls.append((url,'null','False',''))


    def insert(self,url,tbl,dict={}):
        sql="INSERT INTO {}(url)VALUES('{}')".format(tbl,url)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            # print(e)
            pass
        else:
            self.db.commit()

        for k,v in dict.items():
            sql="UPDATE {} SET {}='{}' WHERE url='{}';".format(tbl,k,v,url)
            try:
                self.cursor.execute(sql)
            except Exception as e:
                print(e)
            else:
                self.db.commit()

    def delete(self,url,tbl):
        sql="DELETE FROM {} WHERE url='{}'".format(tbl,url)
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
        else:
            self.db.commit()

    def is_relative(self,title,tags=''):
        for t in self.tag_lst:
            if title.find(t)>-1:
                return True 
            elif tags.find(t)>-1:
                return True
        return False

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
    
    #identify
    def regular_href(self,url):
        if url[:5].find('item')>-1:
            return self.url_head+url
        elif url.find('http://help.baidu.com')>-1:
            return None 
        elif url[:5].find('http')>-1:
            return url
        else:
            return None

    def catch_new_urls(self,soup):
        #如果页面是搜索列表
        if self.new_urls_css=='':
            return 
        tag_as=soup.select(self.new_urls_css)
        for a in tag_as:
            #清洗广告
            #获取a标签中的href
            try:
                url=a.get('href')
            except Exceptions as e:
                continue
            #如果get到的href本身是个NoneType
            if not url:
                continue

            url=self.regular_href(url)
            #如果处理过后的url仍然不符合规则
            if not url:
                continue
            
            title=a.text.strip()
            relative=self.is_relative(title)

            dict={"title":title,"relative":relative}
            item=(url,title,relative,"")
            if url not in self.url_pool:
                self.insert(url,'new_urls_tbl',dict)
                self.new_urls.append(item)
                self.url_pool.append(url)

    def save_data(self,soup,response):
        try:
            title=soup.select('h1')[0].text.strip()
        except Exception as e:
            print('[ERROR] catch title')
            title='null'
        #identify
        tags_lst=soup.select('.taglist')
        tags=''
        for t in tags_lst:
            tags+=t.text.strip()+';'
        relative=self.is_relative(title,tags)
        
        dict={"title":title,'relative':relative,'tags':tags}
        #若不相关，直接返回
        # if not relative:
        #     print(tags)
        #     if title=='null':
        #         return {}
        #     else:
        #         return dict.copy()

        #文本数据
        result=soup.select('h1,.level-2,.level-3,.para,table')
        #半结构化数据
        key=soup.select('.basicInfo-block  dt')
        val=soup.select('.basicInfo-block dd')

        os.chdir(self.output_path_html)
        with open(title+'.html','w',encoding='utf-8') as f:
            f.write(response)
            f.close()

        if title=='null':
            return {}
        else:
            return dict.copy()

    def catch_new_urls_by_js(self,soup):

        target=soup.select('.main-content > script')
        if len(target)==0:
            return None
        str_=target[0].get_text()
        pattern=re.compile('"fentryTableId":(\d+),')
        result=pattern.findall(str_)

        for i in result:        
            url_json=self.url_json.format(i)
            response=self.request(url_json)
            response_dict=json.loads(response)
            html=response_dict['html']
            soup=BeautifulSoup(html,'lxml')
            tag_as=soup.select('a')
            for a in tag_as:
                url=a.get('href')
                if url.find('http')<0:
                    continue
                title=a.get("title")
                if not title:
                    continue
                relative=self.is_relative(title)
                #构造item字典
                dict={"title":title,"relative":relative}
                item=(url,title,relative,"")
                if url not in self.url_pool:
                    self.insert(url,'new_urls_tbl',dict)
                    self.new_urls.append(item)
                    self.url_pool.append(url)

    def parse(self):
        self.init_urls()

        while len(self.new_urls)>0 and self.num<self.max :
            print('new_urls len:',len(self.new_urls))
            print('count:',self.num)
            self.num+=1
            url_item=self.new_urls.pop(0)
            #url,title,relative,tags
            url=url_item[0]
            title=url_item[1]
            relative=url_item[2]
            tags=url_item[3]
            dict_current={'title':title,'relative':relative,'tags':tags}
            response=self.request(url)

            if not response:
                #当get失败时，加入dead_urls_tbl
                self.dead_urls.append(url_item)
                self.insert(url,'dead_urls_tbl',dict_current)
                self.url_pool.append(url)
            
            

            #用soup解析
            soup=BeautifulSoup(response,'lxml')
            # self.catch_new_urls(soup)
            # self.catch_new_urls_by_js(soup)
            # self.save_data(soup,response)

            dict_after=self.save_data(soup,response)
            if not dict_after:
                dict=dict_current
            else:
                dict=dict_after

            #删改数据库
            self.old_urls.append(url_item)
            self.insert(url,'old_urls_tbl',dict)
            self.delete(url,'new_urls_tbl')

            if len(self.new_urls)==0:
                self.new_urls=self.import_urls('new_urls_tbl')
                for i in self.new_urls:
                    self.url_pool.apend(i[0])


    def test(self):
        pass

def main():
    crawl=Crawl()
    # crawl.parse_entity_to_url()
    crawl.parse()

if __name__=='__main__':
    main()