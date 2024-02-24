import sys, os, traceback, time
from pdfrw import PdfReader, PdfWriter, PageMerge

def rotate(file):
    inpfn = file
    outfn = 'out\\' + os.path.basename(inpfn)
    trailer = PdfReader(inpfn)
    outdata = PdfWriter(outfn)

    for page in trailer.pages:
        page.Rotate = (int(page.inheritable.Rotate or 0) + 270) % 360

    outdata.trailer = trailer
    outdata.write()

if __name__ == "__main__":
    inputs = sys.argv[1:]
    try:
        assert inputs
        for input in inputs:
            # skip first arg - py itself and check pdf
            if input.lower().endswith(".pdf"):
                if not os.path.exists("out"):
                    os.mkdir("out")
                rotate(input)
    except Exception as e:
        traceback.print_exc()
        time.sleep(10)
