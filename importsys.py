import sys
import re
from prefect import task, flow
import subprocess
@task
def get_percent(line):
    t = line.split(" ")[4][1:][:-1]
    return float(t)

@task
def ok_or_not(percent):
    if percent < 90:
        print("Not OK")
    else:
        print("OK")

@task(name="index.bwa")
def get_index():
    p = subprocess.Popen("./bwa-mem index ref.fa GCF_000005845.2_ASM584v2_genomic.fna", shell=True)
    p.wait()
    return "index.bwa"

@task(name="res.sam")
def create_sam(index_file):
    p = subprocess.Popen(str.format("./bwa-mem2 mem -t {0} ref.fa GCF_000005845.2_ASM584v2_genomic.fna > out.sam ", index_file), shell=True)
    p.wait()
    return "res.sam"

@task(name="flagstat")
def flagstat(sam_file):
    p = subprocess.Popen(str.format("./bin/samtools flagstat {0} > res_samtools", sam_file), shell=True)
    p.wait()

@flow(name="оценка качества")
def estiamte():
    index_file = get_index()
    sam_file = create_sam(index_file)
    flagstat(sam_file)
    f = open("res_samtools", "r")
    lines = f.readlines()
    for line in lines:
        if re.match("[0-9]+ \+ [0-9]+ mapped", line.strip()):
            percent = get_percent(line)
            ok_or_not(percent)

def main():
    estiamte()

		
    

if __name__ == "__main__":
    main()
