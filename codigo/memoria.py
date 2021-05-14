import sys
import math

def fifo(max_pages, accessed_pages):
    # keeping track of pages in memory and page faults
    current_pages = []
    page_faults = 0

    # for each page that has to be loaded in memory, if there is enough free space,
    # insert the page at the end of the list. If there isn't enough free space, remove the
    # first page in the list and insert the new page at the end of the list.
    for i in range(len(accessed_pages)):
        if accessed_pages[i] not in current_pages:
            if len(current_pages) < max_pages:  #checks if there is enough free space in memory
                current_pages.append(accessed_pages[i])  #loads the page in memory
            else:
                current_pages.pop(0)  #removes the first page
                current_pages.append(accessed_pages[i]) #inserts the new page at the end of the list
            page_faults += 1
            #print(current_pages)
            
        else:
            pass
            #print(current_pages) 

    return page_faults


def second_chance(max_pages, accessed_pages):
    current_pages = [] #keeps track of current pages
    page_faults = 0    #keeps traack of page faults
    victim_frame = 0   #keeps track of the next frame that will be checked after a page is replaced
    r = []             #keeps track of each page r bit
    mem_counter = 0    #keeps track of how many times the memory was accessed
    
    #for each page that must be loaded in memory, if there is enough free space, 
    #insert the page at the end of the list and set it's r bit to 1 (insert it into
    # the r list at the same index as the page)
    for i in range(len(accessed_pages)):
        if mem_counter % 3 == 0: #at every 3 times the memory is accessed, all r bits are set to 0
            r = [0 for z in range(max_pages)]
        if accessed_pages[i] not in current_pages: 
            if len(current_pages) < max_pages:  #checks if there is enough free space in memory
                mem_counter += 1
                current_pages.append(accessed_pages[i])  #loads the page
                r.append(1)
                page_faults += 1
        #if there isn't enough free space, check all pages in memory, starting at the
        #victim frame's position. If the frame being checked has it's r bit set to 1, set it to 0
        #and check the next frame. If the frame being checked has it's r bit set to 0, replace it
        #and set the new page's r bit to 1.
            else:
                while True: #checks all loaded pages until it finds a page that can be replaced (R bit set to 0)
                    if r[victim_frame] == 0: #checks if the page can be replaced, starting at the victim frames's index
                        current_pages[victim_frame] = accessed_pages[i]
                        page_faults += 1
                        r[victim_frame] = 1
                        victim_frame = (victim_frame+1)%max_pages
                        break
                    elif r[victim_frame] == 1:
                        r[victim_frame] = 0
                        victim_frame = (victim_frame+1)%max_pages
        #if the page is already in memory, set it's r bit to 1
        else:
            for j in range(max_pages): #updates the page's r bit if it' already loaded in memory
                if accessed_pages[i] == current_pages[j]:
                    mem_counter += 1
                    r[j] = 1
                    break
        #print(f'{current_pages}   {accessed_pages[i]}')

    return page_faults


def lru(max_pages, accessed_pages):
    current_pages = [] #keeps track of current pages in memory
    page_faults = 0    #keeps track of page faults
    counter = []       #keeps track of the moments each page was loaded in memory
    counter_value = 0  #keeps track of when a specific page was loaded in memory
    swap_index = 0     #keeps track of the page that will be removed from the memory

    #for each page that must be loaded in memory, if there is enough free space,
    #insert the page at the end of the list and insert the moment the page entered (counter value) 
    #at the end of the counter.
    for i in range(len(accessed_pages)):
        if accessed_pages[i] not in current_pages:
            if len(current_pages) < max_pages:           #checks if there is enough free space in memory
                current_pages.append(accessed_pages[i])  #loads the page in memory
                counter.append(counter_value)            #keeps track of the moment the page was loaded in memory
                counter_value += 1
                page_faults += 1
        #if there isn't enough free space, find the page that has the the lowest counter value 
        #(the page that hasn't been referenced for the longest time), and insert the new page at 
        #it's position and replace the moment (counter value) in the counter list at the same index
            else:
                oldest = math.inf
                for k in range(max_pages):     #finds the page that hasn't been referenced for the longest time and replaces it
                    if counter[k] < oldest:
                        oldest = counter[k]
                        swap_index = k
                current_pages[swap_index] = accessed_pages[i]
                page_faults += 1
                counter[swap_index] = counter_value
                counter_value += 1    
    #if the page is already loaded in memory, update the reference moment (counter value)
    #in the counter list       
        else:
            for j in range(max_pages):     #updates the page's counter if it's already loaded in memory
                if accessed_pages[i] == current_pages[j]:
                    counter[j] = counter_value
                    counter_value += 1
                    break
        #print(f'{current_pages}   {accessed_pages[i]} \n{counter} \n')
    return page_faults







def gerencia_de_memoria():

    # gets the file from the command line
    file = sys.argv[2]

    # loads all values from the file in a list
    with open(file) as f:
        accessed_pages = [int(x) for x in f]

    # the first values, wich represents the maximum amount of pages that cna be loaded in memory
    # is loaded in a variable and removed from the list
    max_pages = accessed_pages[0]
    accessed_pages.pop(0)  

    fifo_page_faults = fifo(max_pages, accessed_pages)
    second_chance_page_faults = second_chance(max_pages, accessed_pages)
    lru_page_faults = lru(max_pages, accessed_pages)

    print(f'FIFO {fifo_page_faults}')
    print(f'SC {second_chance_page_faults}')
    print(f'LRU {lru_page_faults}')
