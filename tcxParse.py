import argparse
import os
from parser import parseSession


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse TCX XML file(s).')
    # parser.add_argument('dir', type=str, help='Directory of TCX file(s)')
    parser.add_argument('index', type=int, nargs='?', default=None, help='Index of file to parse (optional)')
    parser.add_argument('graph', type=int, nargs='?', default=None, help='Generate graph (optional)')

    args = parser.parse_args()
    
    dir = "../garmin-acts/"

    verbose = False
    filelist = [f for f in os.listdir(dir) if f.endswith(".tcx")]
    if args.index is not None:
        filelist = [filelist[args.index]] if 0 <= args.index < len(filelist) else []
        verbose = True

    i = 0
    for filename in filelist:
        path = os.path.join(dir, filename)
        basename = os.path.splitext(filename)[0]

        try:
            session = parseSession(path, verbose=verbose, graph=(args.graph is not None))
            print(f"[{i}] {basename}: {session}")
        except Exception as e:
            print(f"[{i}] Error parsing {basename}: {e}")
            continue
        finally:
            i += 1
