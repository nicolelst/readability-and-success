import sys
sys.path.append("pmidcite\\src")
#sys.path.append("C:\\Users\\User\\Desktop\\readabilityinscience")
from pmidcite.icite.downloader import get_downloader

dnldr = get_downloader()

pmids = [22882545, 31461780, 22882545, 20050301]
# nih_entries = dnldr.get_icites(pmids)
for p in pmids:
    entry = dnldr.get_icite(p)
    print(entry.dct["pmid"], entry.dct["citation_count"])
    # for key, val in entry.dct.items():
    #     print('{KEY:>27} {VAL}'.format(KEY=key, VAL=val))