import sys
import os
import math
import tracemalloc as tm
import heapq

order = None                         # asc/desc
csize = 0                            #tuple size
rsize = 0                            #main mem
cols = list()                        #col name in int
tcolsize = list()                    #list of cell size  
ifile = str                          #input filename
ofile = str                          # output filename
tempfiles = list()                   #list of name of tempfiles
chunk = 0                            # chunk size     
no_of_files = 0                      # no of temp file
colToind = dict()                    # {'c1':0,'c2':1.......}
heap = list()
filepointer = list()


class node:
    def __init__(self):
        self.data = list()
        self.fp = -1

def asc(datal,datai):
    for i in cols:
        if(datal[i]<datai[i]):
            return True
        elif datal[i]>datai[i]:
            return False    
    # print('qwer')
    return False

def desc(datal,datai):
    for i in cols:
        if(datal[i]>datai[i]):
            return True
        elif datal[i]<datai[i]:
            return False    
    # print('qwer')
    return False

def min_heap(i):
    global heap
    temp = node()
    l = i*2+1
    r = i*2+2
    min_elm = -1
    
    if l < len(heap):
        if order == 'asc':
            cmp = asc(heap[l].data,heap[i].data)
        elif order == 'desc':
            cmp = desc(heap[l].data,heap[i].data)
        if cmp == 'True':
            min_elm = l
        elif cmp == 'False':
            min_elm = i
    else:
        min_elm = i

    if r < len(heap):
        if order == 'asc':
            cmp = asc(heap[r].data,heap[min_elm].data)
        elif order == 'desc':
            cmp = desc(heap[l].data,heap[min_elm].data)
        if cmp == 'True':
            min_elm = r

    if min_elm != i:
        temp = heap[min_elm]
        heap[min_elm] = heap[i]
        heap[i] = temp
        min_heap(min_elm)


def heap_pop():
    global heap
    temp = heap[0]
    l1 = len(heap)
    heap[0] = heap[l1-1]
    heap.pop()
    min_heap(0)
    return temp

def rebal(i):
    global heap
    c = i
    p = math.floor((i-1)/2)
    if order == 'asc':
        while(p>=0 and asc(heap[c].data,heap[p].data)):
            temp= heap[c]
            heap[c]=heap[p]
            heap[p] = temp
            c=p
            p = math.floor((c-1)/2)

def write_output():
    global filepointer,ofile,no_of_files
    f = open(ofile,'w')
    i=0
    while i != no_of_files:
        result = []
        td = heap_pop()
        result.append(td.data)
        for item1 in result:
            line = ''
            for word in item1:
                line = line + word + '  '
            line = line[:-1]
            line = line + '\n'
            f.write(line)    
        line = filepointer[td.fp]   
        # print(line.readline())
        line1 = extract_string_from_tuple(line.readline())
        if(len(line1) != 0):
            td.data = line1
            heap.append(td)
            rebal(len(heap)-1)
        else: 
            i+=1 
            print(i)   
    for i in range(len(tempfiles)):
        filepointer[i]= open(tempfiles[i])
        # print('Writing')
    return 1


def merge_files():
    global tempfiles,cols,heap,filepointer,no_of_files
    filepointer = [None]*no_of_files

    for i,fname in enumerate(tempfiles):
        f = open(fname)
        filepointer[i] = f
        line = f.readline()
        tuple_ = extract_string_from_tuple(line)
        temp = node()
        temp.fp = i
        temp.data = tuple_
        heap.append(temp)
    l = len(heap)
    while(l>0):
        l-=1
        min_heap(l)
    print('write output')
    write_output()
    print('Files is sorted')
    print('Deleting Tempfiles')
    for i in range(0,no_of_files):
        os.remove(tempfiles[i])

'''creating temp sorted file'''
def create_temp_file(filechunk):
    global no_of_files
    fname = 'temp'+str(no_of_files)+'.txt'
    tempfiles.append(fname)
    no_of_files+=1
    tf = open(fname,'w')
    for item in filechunk:
        # print(item)
        line = ''
        for word in item:
            #print(word)
            line = line + word + '  '
        # print(line)
        line = line[:-1]
        line = line + '\n'
        tf.write(line)    
    tf.close()
    # return fname

def extract_string_from_tuple(line):
    if line:
        idx=0
        temp = list()
        for idx2 in tcolsize:
            temp.append(line[idx:idx+idx2])
            idx += idx2 + 2
        return temp
    else:
        return []
def phase1(filechunk):
    if order == 'asc':
        filechunk.sort(key=lambda i:cols)
    if order == 'desc':
        filechunk = sorted(filechunk,key=lambda i:cols, reverse=True)
    create_temp_file(filechunk)
    # filechunk.clear()
  
    return 1

def dividefile():
    global tempfiles,ifile,chunk,order,no_of_files
    flag = 0
    f = open(ifile)
    filechunk = []
    for i,line in enumerate(f):
        eof = i+1
        if eof%chunk != 0:
            colcell = []
            colcell = extract_string_from_tuple(line)
            #print(colcell)
            filechunk.append(colcell)
            flag=1
            # colcell.clear()
            # line = line.split('  ')
            # print(line)
            # if i == 0:
            #     return

        elif eof%chunk == 0:
            flag = 2
            # tf = open(create_temp_file(),'w')
            '''Create seperate func for this'''
            phase1(filechunk)
            # if order == 'asc':
            #     filechunk = sorted(filechunk)
            # if order == 'desc':
            #     filechunk = sorted(filechunk,reverse=True)
            # create_temp_file(filechunk)
            filechunk.clear()
        if flag == 2:
            filechunk.append(extract_string_from_tuple(line))

    if flag:
        '''above func'''
        phase1(filechunk)
    print('No. of Subfiles ',str(no_of_files))    
    merge_files()    

def assign_int_col(tcol,cols):
    global colToind
    num_list = list()
    j = len(tcol)
    for i in range(0,j):
        num_list.append(i)
    colToind = dict(zip(tcol,num_list))
    for i,val in enumerate(cols):
        cols[i] = int(colToind[val])

    return





def Main():
    global order,cols,csize,rsize,chunk,ifile,ofile,tcolsize
    try:
        f = open('metadata.txt','r')
    except:
        print('Meta Not Found')  
        sys.exit(0)  
    f=f.readlines()
    tcol = []
    for line in f:
        item = line.split(',')
        tcol.append(item[0])
        item[1] = item[1].split('\n')[0]
        tcolsize.append(int(item[1]))
        csize += int(item[1])
    #f.close()
    print(sys.argv)
    print(tcol)
    inp = sys.argv
    ifile = inp[1]
    ofile = inp[2]
    order = inp[4]
    rsize = int(inp[3])
    rsize*=byts
    cols = (inp[5:])

   

    # cols.append(inp[6])
    try:
        open(ifile,'r')
    except:
        print('Input file not Found')
        sys.exit(0)    
    set1 = set(cols)
    set2 = set(tcol)
    if (set1.issubset(set2)):
        0            
    else:
        print('Input column/s not present in metadata.txt')
        sys.exit(0)
    print('Chunk size',str(csize))
    print('Sorting on columns ',cols)
    print('Max memory allowed ',str(rsize))    
    assign_int_col(tcol,cols)   
   
    print('Phase 1 Sorting started')
    print('Sorting Data in '+order+'ending order')
    tm.start()
    csize *= 4
    chunk = math.floor(rsize/csize)
    dividefile()
    c,p = tm.get_traced_memory()

    c/=byts
    p/=byts
    print('Max memory consumed ',p)
    tm.stop()
    # if phase1():
    print('Done')




if __name__ == '__main__':
    byts = pow(10,6)
    chunk
    Main()
