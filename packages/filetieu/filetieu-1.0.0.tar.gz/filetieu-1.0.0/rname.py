#rename type of all file in forder
import os

def open_path(p):
    now=os.getcwd()
    try:
        os.chdir(now+"/"+p)
    except:
        pass

def rename(file,last='none',new='new'):
    open_path(file)
    list_file=os.listdir()
    for eachfile in list_file:
        try:
            if last=='none':
                (name,typ)=eachfile.split(".",1)
            else:
                index_split=eachfile.find('.'+last)
                (name,typ)=(eachfile[0:index_split],eachfile[index_split+1:len(eachfile)])
            os.rename(eachfile,name+'.'+new)
        except Exception as ex:
            print(ex)
        
#rename('a','new','txt')