# This script made for 映像メディア通信特論 final report.

import subprocess
import os
import csv

# webp image target path and result path
base = os.environ["VIDEO_COMM_LEC"]
src = base+"image-dataset/"
dest = base+"result/"

# webp quality
qualities = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 75]


class CSVLine:
    orign_name = ""
    output_file = ""
    quality = 0
    width = 0
    height = 0
    pixel = 0
    filesize_byte = 0
    filesize_bit = 0
    PSNR = 0.0
    BPP = 0.0

    def __init__(self, orign_name, quality):
        self.orign_name = orign_name
        self.output_file = orign_name.split(".")[0]+"_"+str(quality)+".webp"
        self.quality = quality

    def __str__(self):
        res = "origin_name: " + self.orign_name
        res += " output_file: " + self.output_file
        res += " quality: " + str(self.quality)
        res += " width: " + str(self.width)
        res += " height: " + str(self.height)
        res += " pixel: " + str(self.pixel)
        res += " filesize_byte: " + str(self.filesize_byte)
        res += " filesize_bit: " + str(self.filesize_bit)
        res += " PSNR: " + str(self.PSNR)
        res += " BPP: " + str(self.BPP)
        return res

    def set_filesize(self, filesize):
        self.filesize_byte = filesize
        self.filesize_bit = filesize * 8

    def set_pixelsize(self, pixel):
        self.width = int(pixel[0])
        self.height = int(pixel[1])
        self.pixel = self.width * self.height

    def calc_BPP(self):
        self.BPP = float(self.filesize_bit) / self.pixel

    def get_list_data(self):
        res = [self.orign_name]
        res.append(self.output_file)
        res.append(str(self.quality))
        res.append(str(self.width))
        res.append(str(self.height))
        res.append(str(self.pixel))
        res.append(str(self.filesize_byte))
        res.append(str(self.filesize_bit))
        res.append(str(self.PSNR))
        res.append(str(self.BPP))
        return res


def get_data(src):
    pics = [pic.name for pic in os.scandir(
        src) if not pic.name.startswith(".")]
    return pics


def cwebp(t):
    subprocess.run(["cwebp", "-q", str(t.quality), src +
                    t.orign_name, "-o", dest+str(t.quality)+"/"+t.output_file])


def psnr(t):
    out = subprocess.run(["compare", "-metric", "PSNR", src+t.orign_name, dest+str(t.quality)+"/" +
                          t.output_file, "diff.webp"], encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    t.PSNR = out.stderr


def csv_out(target):
    header = ["元ファイル", "出力ファイル名",	"quality",	"横サイズ",	"縦サイズ",
              "pixel",	"ファイルサイズ(byte)",	"ファイルサイズ(bit)",	"PSNR",	"BPP"]
    file_name = "/Users/futa/Library/Mobile Documents/com~apple~CloudDocs/M1/レポート課題/映像メディア通信/result.csv"
    with open(file_name, "w") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for t in target:
            writer.writerow(t.get_list_data())


def get_file_size(t):
    scan_path = dest + str(t.quality) + "/" + t.output_file
    pics = subprocess.run(["ls", "-l", scan_path],
                          stdout=subprocess.PIPE, encoding="utf-8")
    print(type(pics.stdout))
    right = pics.stdout.split("staff  ")[1]
    size = right.split(" ")[0]
    print("size = ", size)
    t.set_filesize(int(size))


def get_pixel_size(t):
    scan_path = dest + str(t.quality) + "/" + t.output_file
    out = subprocess.run(["identify", scan_path],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    right = out.stdout.split("WEBP ")[1]
    size = right.split(" ")[0]
    data = size.split("x")
    t.set_pixelsize(data)


def main():
    pics = get_data(src)
    target = []
    for pic in pics:
        for q in qualities:
            target.append(CSVLine(pic, q))

    for t in target:
        cwebp(t)
        psnr(t)
        get_file_size(t)
        get_pixel_size(t)
        t.calc_BPP()
        print(t)
    csv_out(target)


main()
