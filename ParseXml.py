from bs4 import BeautifulSoup 
import bs4 
import json
import os 


class ParseXml():

    def __init__(self):
        self.path=os.getcwd()
        self.output_path=self.path+'\\'+r'output\json'
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)
        self.input_folder=self.path+'\\'+r'output\xml'
        self.file_lst=os.listdir(self.input_folder)
        
    def parse(self,file):
        with open(self.input_folder+'\\'+file,'r',encoding='utf-8') as f:
            response=f.read()
            soup=BeautifulSoup(response,'lxml')    
            f.close()
        #处理文本
        tag_lst=list(soup.select('body')[0].children)
        
        #便于处理栈所添加的首尾结点
        tag0=BeautifulSoup('<h0 id="0">','lxml')
        tag_tail=BeautifulSoup('<h0 id="1">','lxml')
        tag0=tag0.select('h0')[0]
        tag_tail=tag_tail.select('h0')[0]
        tag_lst.append(tag_tail)
        for i in tag_lst:
            if i=='\n':
                tag_lst.remove(i)

        key_stack=[tag0]
        index={}
        dict={0:{}}
        title=tag_lst.pop(0).text.strip()
        dict[0]['title']=title
        #处理结构数据 主要是为了添加到字典最前面，，，
        box=soup.select('box')[0]
        box_text=box.text.strip()
        box_data=json.loads(box_text)
        dict[0]['box']=box_data

        while len(tag_lst)>0:
            tag=tag_lst.pop(0)

            try:
                tag_id=int(tag.get('id'))
            except Exception as e:
                operation=1
            else:
                operation=0


            if operation==0:
                #标题标签
                while int(key_stack[-1].get('id'))>=tag_id:
                    tag_pop=key_stack.pop()
                    tag_pop_id=int(tag_pop.get('id'))

                    dict[int(key_stack[-1].get('id'))][tag_pop.text]=dict[tag_pop_id].copy()
                    dict[tag_pop_id].clear()
                    index[tag_pop_id]=0

                key_stack.append(tag)
                dict[tag_id]={}
                current=tag_id
                index[current]=0
                pass
            elif operation==1:
                #非标题标签
                dict[current][index[current]]=tag.text
                index[current]+=1
                pass
        #处理结构数据
        dict_final=dict[0].copy()
        with open(file.replace('.xml','.json'),'w',encoding='utf-8') as f:
            json_data=json.dumps(dict_final,ensure_ascii=False)
            f.write(json_data)
            f.close()

    def work(self):
        os.chdir(self.output_path)
        for i in self.file_lst:
            try:
                self.parse(i)
            except Exception as e:
                print(e)
                with open(self.path+'\\'+"error.txt",'a',encoding='utf-8') as f:
                    f.write(i+'\n')
                    f.close()

def main():
    px=ParseXml()
    px.work()

if __name__=='__main__':
    main()
