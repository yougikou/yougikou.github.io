import sys, os, time, traceback
from pdfrw import PdfReader, PdfWriter, PageMerge

if __name__ == "__main__":
    inputs = sys.argv[1:]
    try:
        assert inputs
        outfn = 'out\\' + os.path.basename(inputs[0])
        writer = PdfWriter()

        for inpfn in inputs:
            # skip first arg - py itself and check pdf
            if inpfn.lower().endswith(".pdf"):
                if not os.path.exists("out"):
                    os.mkdir("out")
                writer.addpages(PdfReader(inpfn).pages)
        writer.write(outfn)
    except Exception as e:
        traceback.print_exc()
        time.sleep(10)