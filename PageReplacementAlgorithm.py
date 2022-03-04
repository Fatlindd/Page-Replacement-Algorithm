from colorama import Fore, Back, Style

print('''
       .__. .__. .___   .___     .___, .___ .___. .    .___. .___ .___ ..  .. .___ ..  . _____     .___. .    .___  .___. .___,  . _____ .   . ..  ..
       |__| |__| |___,  |___     |___| |___ |___) |    |___| |    |___ | \/ | |___ | \ |   |       |___| |    |___. |   | |___)  |   |   |___| | \/ |
       |    |  | |___|  |___     |`,.  |___ |     |___ |   | |___ |___ |    | |___ |  \|   |       |   | |___ |___| |___| |`,.   |   |   |   | |    |
        ''')


def displaySimulation(algo, reference_string, frames, arr_data, page_fault, page_fault_arr):
    rows, cols = (frames, len(reference_string))
    line = [" ----"] * cols
    print("\n\t\t\t\t\t\t\t\t>>> " + Back.WHITE + " Tabela e stimulimit per ", algo, " PAGE REPLACEMENT ALGORITHM ",
          end='')
    print(Style.RESET_ALL, end=' <<<\n\n')
    print("\n\t Ref_String", end="")  # Print Reference String
    print("\t ", (Back.LIGHTYELLOW_EX + "{:>5}" * len(reference_string)).format(*reference_string), end='')
    print(Style.RESET_ALL)
    # Print frames
    for i in range(rows):
        print("\t\t\t\t  ", ("{:5}" * len(line)).format(*line))
        print("\t  " + Back.LIGHTCYAN_EX + "|Frame {}|".format(i + 1) + Style.RESET_ALL, end="")
        print("\t ", ("{:5}" * len(arr_data[i][:])).format(*arr_data[i][:]))
    print("\t\t\t\t  ", ("{:5}" * len(line)).format(*line))
    print("\t  " + Back.LIGHTRED_EX + "Fault >>>" + Style.RESET_ALL, end="")
    print("\t   ", end="")

    for txt in page_fault_arr:
        if txt == ' Miss':
            print(Fore.RED + txt, end='')
            print(Style.RESET_ALL, end='')
        elif txt == ' Hit':
            print(Fore.BLUE + ' ' + txt, end='')
            print(Style.RESET_ALL, end='')
    # Print Fault Columns
    print("\n\n\t\t\t\t\t\t\t\t\t\t\t\t\t >>> " + Back.LIGHTYELLOW_EX + "Total Page Fault =", page_fault, end='')
    print(Style.RESET_ALL, "<<<\n")
    input("\n\nPress any key to continue...")


def FIFO(algo, reference_string, frames, output):

    rows, cols = (frames, len(reference_string))
    arr_data = [[''] * cols for _ in range(rows)]       # Ruajtja Stimulimit te algoritmit
    current_pages = [] * rows                           # Ruajtja e faqes ne memorie ne kordinim me fifo_pages
    fifo_pages = [] * rows                              # Ruan faqet paraprake qe jane vendosur ne radhen e FIFO

    page_fault_arr = [] * cols            # Ruajtja e Stringjeve Miss per gabime dhe Hit nese ekziston faqja ne memorie
    page_fault = 0                  # Regjistrimi i gabimeve totale

    for i, page in enumerate(reference_string):
        # Nese te gjitha frames jane te zëna
        if len(current_pages) == rows:
            if page not in current_pages:
                for n, j in enumerate(current_pages):
                    if j == fifo_pages[0]:
                        current_pages[n] = page
                        page_fault = page_fault + 1
                        page_fault_arr.append(" Miss")
                        fifo_pages.pop(0)
                        fifo_pages.append(page)
                        break
            else:
                page_fault_arr.append(" Hit")
        # Frames ne memorie jane fillimisht te zbrazeta
        if len(current_pages) != rows:
            if page not in current_pages:
                current_pages.append(page)
                page_fault = page_fault + 1
                page_fault_arr.append(" Miss")
            else:
                page_fault_arr.append(" Hit")

            fifo_pages = list(current_pages)
        # Regjistrimi i faqeve ne arr_data(Simulimi)
        for k in range(len(current_pages)):
            if page_fault_arr[-1] == " Miss" or page_fault_arr[-1] == " Hit":
                arr_data[k][i] = current_pages[k]
    if output == "DISPLAY":
        displaySimulation(algo, reference_string, frames, arr_data, page_fault, page_fault_arr)
    if output == "PAGEFAULT":
        return page_fault


def OPR(algo, reference_string, frames, output):
    # Ruajtja e ref te ardhshme ne queue
    opt_ref_str = list(reference_string)
    rows, cols = (frames, len(reference_string))
    arr_data = [[''] * cols for _ in range(rows)]     # Ruajtja Stimulimit te algoritmit
    current_pages = [] * rows                        # Ruajtja e faqes aktuale ne memorie
    page_fault_arr = [] * cols           # Ruajtja e Stringjeve Miss per gabime dhe Hit nese ekziston faqja ne memorie
    page_fault = 0
    for i, element in enumerate(reference_string):
        # Nese te gjitha frames jane te zëna
        if len(current_pages) == rows:
            if element not in current_pages:
                # kontrollimi nese faqja aktuale ekziston ne opt_ref_str
                check = all(item in opt_ref_str for item in current_pages)

                # nese faqja ne current_page nuk eshte ne queue e ardhme
                if check is not True:
                    for n, j in enumerate(current_pages):
                        if j not in opt_ref_str:
                            current_pages[n] = element
                            page_fault += 1
                            page_fault_arr.append(" Miss")
                            break
                # Nese faqja ne current_page eshte ne queue te ardhshme
                if check is True:
                    longest = 0
                    for n, j in enumerate(current_pages):
                        index = opt_ref_str.index(j)
                        if index > longest:
                            longest = index
                    index = current_pages.index(opt_ref_str[longest])
                    current_pages[index] = element
                    page_fault += 1
                    page_fault_arr.append(" Miss")
            else:
                page_fault_arr.append(" Hit")
            opt_ref_str.pop(0)

        # nëse ka ende kornizë të pa zëna
        if len(current_pages) != rows:
            if element not in current_pages:
                current_pages.append(element)
                page_fault += 1
                page_fault_arr.append(" Miss")
            else:
                page_fault_arr.append(" Hit")
            opt_ref_str.pop(0)

        # Regjistrimi i faqeve ne arr_data(Simulimi)
        for k in range(len(current_pages)):
            if page_fault_arr[-1] == " Miss" or page_fault_arr[-1] == " Hit":
                arr_data[k][i] = current_pages[k]
    if output == "DISPLAY":
        displaySimulation(algo, reference_string, frames,
                          arr_data, page_fault, page_fault_arr)
    if output == "PAGEFAULT":
        return page_fault


def LRU(algo, reference_string, frames, output):

    rows, cols = (frames, len(reference_string))
    arr_data = [[''] * cols for _ in range(rows)]   # Ruajtja Stimulimit te algoritmit
    current_pages = [] * rows                       # Ruajtja e faqes aktuale ne memorie
    page_fault_arr = [] * cols          # Ruajtja e Stringjeve Miss per gabime dhe Hit nese ekziston faqja ne memorie
    page_fault = 0
    # Ruajtja aktuale e faqes te algoritmit LRU
    ru_page = reference_string[0]
    lru_arr = [] * rows  # Ruajtja e faqeve aktuale
    for i, element in enumerate(reference_string):
        # Kornizat të gjitha të zëna
        if len(current_pages) == rows:
            if element not in current_pages:
                for n, j in enumerate(current_pages):
                    if j == ru_page:
                        current_pages[n] = element
                        page_fault += 1
                        page_fault_arr.append(" Miss")

                        lru_arr.pop(0)
                        lru_arr.append(element)
            else:
                lru_arr.remove(element)
                lru_arr.append(element)
                page_fault_arr.append(" Hit")
        # nëse ka ende kornizë të lira
        if len(current_pages) != rows:
            if element not in current_pages:
                current_pages.append(element)
                page_fault += 1
                page_fault_arr.append(" Miss")

                lru_arr.append(element)
            else:
                lru_arr.remove(element)
                lru_arr.append(element)
                page_fault_arr.append(" Hit")
        # Regjistrimi i faqeve ne arr_data(Simulimi)
        for k in range(len(current_pages)):
            if page_fault_arr[-1] == " Miss" or page_fault_arr[-1] == " Hit":
                arr_data[k][i] = current_pages[k]
        # Perditesimi i faqeve
            ru_page = lru_arr[0]

    if output == "DISPLAY":
        displaySimulation(algo, reference_string, frames,
                          arr_data, page_fault, page_fault_arr)
    elif output == "PAGEFAULT":
        return page_fault


def display():
    print("\t ", "_" * 115, sep="")
    print("\n\t\t\t\t\t\t\t\t\t  >>> " + Back.WHITE + " Zgjedhni njerin algoritem per te stimuluar ", end='')
    print(Style.RESET_ALL, end='')
    print(" <<<", end='\n')
    print("""
          \t\t[1] FIRST-IN-FIRST-OUT
          \t\t[2] OPTIMAL ALGORITHM
          \t\t[3] LEAST RECENTLY USED
          \t\t[4] CLEAR QUEUE
            """)


choice_algo = None
while choice_algo != 0:
    # ref_str = 1 2 3 4 3 3 5
    print("\t\t", "_" * 140, sep="")
    ref_str = list(map(int, input("\t\tJep referencen e stringut:").split(" ")))
    frame = int(input("\t\tJep numrin e Frames: "))
    display()
    print("\t ", "_" * 115)
    choice_algo = int(input("\t\tSelect: "))
    if choice_algo == 1:
        if len(ref_str) == 0:
            input("Nuk eshte dhene asnje reference e stringut!\nShtyp dikqa per te vazhduar... ")
        else:
            FIFO("FIFO", ref_str, frame, "DISPLAY")
    if choice_algo == 2:
        if len(ref_str) == 0:
            input("Nuk eshte dhene asnje reference e stringut!\nShtyp dikqa per te vazhduar... ")
        else:
            OPR("OPT", ref_str, frame, "DISPLAY")
    if choice_algo == 3:
        if len(ref_str) == 0:
            input("Nuk eshte dhene asnje reference e stringut!\nShtyp dikqa per te vazhduar... ")
        else:
            LRU("LRU", ref_str, frame, "DISPLAY")
    if choice_algo == 4:
        frame = 0

