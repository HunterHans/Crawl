import os 
import json

def main():
    path=os.getcwd()
    with open('init/init_schema.sql','r') as f:
        text=f.read()
        f.close()
    with open('config/config.json','r') as f:
        data=json.load(f)
        f.close()
    db=data['database']
    text=text.replace("default_database_",db)
    
    with open('init/schema.sql','w') as f:
        f.write(text)
        f.close()

if __name__=="__main__":
    main()