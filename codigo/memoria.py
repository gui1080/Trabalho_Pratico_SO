import sys

def gerencia_de_memoria():

    # gets the file from the command line
    file = sys.argv[2]

    with open(file) as f:
        accessed_pages = [int(x) for x in f]

    max_pages = accessed_pages[0]
    accessed_pages.pop(0)  

    def fifo(max_pages, accessed_pages):
        current_pages = []
        page_faults = 0

        for i in range(len(accessed_pages)):
            if accessed_pages[i] not in current_pages:
                if len(current_pages) < max_pages:
                    current_pages.append(accessed_pages[i])
                else:
                    current_pages.pop(0)
                    current_pages.append(accessed_pages[i])
                page_faults += 1
                #print(current_pages)
                
            else:
                pass
                #print(current_pages) 

        return page_faults

    #a = fifo(max_pages, accessed_pages)
    #print(f'\n{a}\n')        


    def second_chance(max_pages, accessed_pages):
        current_pages = []
        page_faults = 0
        victim_frame = 0
        r = []

        for i in range(len(accessed_pages)):
            if accessed_pages[i] not in current_pages:
                if len(current_pages) < max_pages:
                    current_pages.append(accessed_pages[i])
                    r.append(1)
                    page_faults += 1
                else:
                    while True:
                        if r[victim_frame] == 0:
                            current_pages[victim_frame] = accessed_pages[i]
                            page_faults += 1
                            r[victim_frame] = 1
                            victim_frame = (victim_frame+1)%max_pages
                            break
                        elif r[victim_frame] == 1:
                            r[victim_frame] = 0
                            victim_frame = (victim_frame+1)%max_pages

            else:
                for j in range(max_pages):
                    if accessed_pages[i] == current_pages[j]:
                        r[j] = 1
                        break
            #print(f'{current_pages}   {accessed_pages[i]}')

        return page_faults
    a = second_chance(max_pages, accessed_pages)
    #print(a)
        

    def lru():
        pass