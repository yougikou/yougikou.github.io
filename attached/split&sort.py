import sys, os, time, traceback
from pdfrw import PdfReader, PdfWriter, PageMerge

def splitpage(src, srcIdx, sorter, upOrDown):
    # [0, 1, 2, 3, 4, 5]
    # up page [0, 1, (2), (3), 4, 5]
    # dn page [0, <1>, (2), (3), <4>, 5]
    LPage = PageMerge().add(src, viewrect=(0, 0, 0.5, 1)).render()
    RPage = PageMerge().add(src, viewrect=(0.5, 0, 0.5, 1)).render()
    if upOrDown:
        # up - page asc
        LIdx = int(len(sorter)/2 - srcIdx - 1)
        RIdx = int(len(sorter)/2 + srcIdx)
        sorter[LIdx] = LPage
        sorter[RIdx] = RPage
    else:
        # down - page desc
        RIdx = int(len(sorter)/2 - srcIdx - 1)
        LIdx = int(len(sorter)/2 + srcIdx)
        sorter[LIdx] = LPage
        sorter[RIdx] = RPage

def processFile(file):
    inpfn = file
    outfn = 'out\\' + os.path.basename(inpfn).replace("_B4", "")
    reader = PdfReader(inpfn)
    writer = PdfWriter(outfn)

    # first page is up
    upOrDown = True
    sorter = [None] * len(reader.pages) * 2

    for idx, page in enumerate(reader.pages):
        splitpage(page, idx, sorter, upOrDown)
        upOrDown = not upOrDown

    writer.addpages(sorter)
    writer.write()

if __name__ == "__main__":
    inputs = sys.argv[1:]
    try:
        assert inputs
        for input in inputs:
            # skip first arg - py itself and check pdf
            if input.lower().endswith(".pdf"):
                if not os.path.exists("out"):
                    os.mkdir("out")
                processFile(input)
    except Exception as e:
        traceback.print_exc()
        time.sleep(10)
