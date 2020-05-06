import sys, os, time, traceback
from pdfrw import PdfReader, PdfWriter, PageMerge

def processFile(file):
    inpfn = file
    outfn = 'out\\' + os.path.basename(inpfn)
    reader = PdfReader(inpfn)
    writer = PdfWriter(outfn)

    sorter = [None] * len(reader.pages)

    for idx, page in enumerate(reader.pages):
        sorter[len(sorter) - idx - 1] = page

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
