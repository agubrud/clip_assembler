import os
import glob
import argparse
import subprocess

# C:\ffmpeg -f concat -safe 0 -i ffmpeg_proc.txt -c:v copy -qscale 0 -af "highpass=f=200, lowpass=f=1000" April2022_LagunaSeca_HOD_Miata_Session1.mp4
def main():
    files = list(filter(os.path.isfile, glob.glob(args.inputDir + "*.MOV")))
    files.sort(key=lambda x: os.path.getmtime(x))
    
    ffmpeg_cfg = os.path.join(args.inputDir, "ffmpeg_cfg.txt")
    try:
        os.remove(ffmpeg_cfg)
    except OSError:
        pass

    with open(ffmpeg_cfg, "w") as f:
        for file in files:
            f.write(f"file \'{file}\'\n")

    try:
        os.remove(args.outputVideo)
    except OSError:
        pass

    process = subprocess.Popen(['C:\\ffmpeg', 
                                '-f', 'concat', 
                                '-safe', '0', 
                                '-i', ffmpeg_cfg, 
                                '-c:v', 'copy', 
                                '-qscale', '0', 
                                '-af',  'highpass=f=200, lowpass=f=1000', 
                                args.outputVideo],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(f"{args.outputVideo} created!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-id", "--inputDir", required=True, help="Directory of videos to process", dest="inputDir")
    parser.add_argument("-ov", "--outputVideo", required=False, default=".\out.mp4", help="Filename of the video you want to save", dest="outputVideo")
    args = parser.parse_args()
    main()