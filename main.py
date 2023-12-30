import argparse
from mikanani.src.worker import MikanamiAnimeSubWorker

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, default="direct")
    args = parser.parse_args()
    
    if args.mode == "direct":
        MikanamiAnimeSubWorker().run()

if __name__ == '__main__':
    main()
