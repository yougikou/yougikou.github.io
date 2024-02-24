import sys, os, time, traceback
from pdfrw import PdfReader, PdfWriter, PageMerge

def processFile(file):
    inpfn = file
    outfn = 'out\\' + os.path.basename(inpfn)
    reader = PdfReader(inpfn)
    writer = PdfWriter(outfn)

    pagesNum = len(reader.pages)
    print(os.path.basename(inpfn) + ": page 1 - " + str(pagesNum))
    print("Please specify page with space (Ex. 2 4 11).")
    delPages = list(map(int, input().split()))

    for idx, page in enumerate(reader.pages):
        if (idx + 1) not in delPages:
            writer.addPage(page)
    writer.write()

if __name__ == "__main__":
    inpfn = sys.argv[1]
    try:
        assert inpfn
        if inpfn.lower().endswith(".pdf"):
            if not os.path.exists("out"):
                os.mkdir("out")
            processFile(inpfn)
        else:
            print("File is not pdf")
            time.sleep(10)
    except Exception as e:
        traceback.print_exc()
        time.sleep(10)
