1. https://trace.ncbi.nlm.nih.gov/Traces/?view=run_browser&acc=SRR24658891&display=download
2. Установка, использование bwa mem, samtools
  https://github.com/bwa-mem2/bwa-mem2

  
    pip install bwa

4. Алгоритм получения генетических вариантов


- Скачать необоходимые данные

- Провести контроль качества видов

  fastqc ecoli.fastq -> ecoli_fastqc.html

- Индексирование ссылочной последовательности (требуется 28N ГБ памяти, где N - размер ссылочной последовательности).

./индекс bwa-mem2 [префикс-p] <в.fasta>

Где 

<в.fasta> - это путь к файлу fasta с ссылочной последовательностью и 

<префикс> - это префикс имен файлов, в которых хранится результирующий индекс. По умолчанию используется.fasta.

Сопоставление 

Запустите "./bwa-mem2 mem", чтобы получить все параметры 

./bwa-mem2 mem -t <num_threads> <префикс> <считывает.fq/fa> > out.sam

Где <префикс> - это префикс, указанный при создании индекса или пути к ссылочному файлу fasta в случае, когда префикс не был указан.

Конвертировать формат sam в bam

samtools view -b alignments.sam -o alignments.bam -> alignments.bam

Построить оценку

samtools flagstat alignments.bam > flagstat.txt -> flagstat.txt

Получить результат оценивания при помощи скрипта

./get_percent.sh flagstat.txt

. Этапы выравнивания:

git clone https://github.com/bwa-mem2/bwa-mem2.git

cd bwa-mem2

make CXX=icpc (using intel C/C++ compiler)

or make (using gcc compiler)

./bwa-mem2 index <ref.fa>

./bwa-mem2 mem [-t <#threads>] <ref.fa> <in_1.fastq> [<in_2.fastq>] > <output.sam>

numactl -m 0 -C 0-27,56-83 ./bwa-mem2 index human_g1k_v37.fasta  

numactl -m 0 -C 0-27,56-83 ./bwa-mem2 mem -t 56 human_g1k_v37.fasta SRR7733443_1.fastq SRR7733443_2.fastq > d2_align.sam

Скрипт для получения оценки

#!/bin/bash
grep -E "[0-9]+ \+ [0-9]+ mapped" $1 | cut -d " " -f 5 | sed 's/^.//;s/.$//' | cut -d "." -f 1

#!/bin/bash
percent=$(grep -E "[0-9]+ \+ [0-9]+ mapped" $1 | cut -d " " -f 5 | sed 's/^.//;s/.$//' | cut -d "." -f 1)
if [[ "$percent" -lt "90" ]]; then
	echo "Not ok"
else
	echo "OK"
fi

Установка Prefect

pip install prefect
prefect server start

prefect.engine - Created flow run 'pragmatic-barracuda' for flow 'foo'
Hello world
Flow run 'pragmatic-barracuda' - Finished in state Completed()

    
19:32:49.988 | INFO    | prefect.engine - Created flow run 'impartial-scorpion' for flow 'оценка качества'
19:32:50.063 | INFO    | Flow run 'impartial-scorpion' - Created task run 'index.mmi-0' for task 'index.mmi'
19:32:50.063 | INFO    | Flow run 'impartial-scorpion' - Executing 'index.mmi-0' immediately...
[M::mm_idx_gen::0.093*1.03] collected minimizers
[M::mm_idx_gen::0.111*1.35] sorted minimizers
[M::main::0.172*1.19] loaded/built the index for 1 target sequence(s)
[M::mm_idx_stat] kmer size: 15; skip: 10; is_hpc: 0; #seq: 1
[M::mm_idx_stat::0.180*1.18] distinct minimizers: 838542 (98.18% are singletons); average occurrences: 1.034; average spacing: 5.352; total length: 4641652
[M::main] Version: 2.26-r1175
[M::main] CMD: ./minimap2/minimap2 -d index.mmi GCF_000005845.2_ASM584v2_genomic.fna
[M::main] Real time: 0.188 sec; CPU: 0.220 sec; Peak RSS: 0.075 GB
19:32:50.316 | INFO    | Task run 'index.mmi-0' - Finished in state Completed()
19:32:50.330 | INFO    | Flow run 'impartial-scorpion' - Created task run 'res.sam-0' for task 'res.sam'
19:32:50.330 | INFO    | Flow run 'impartial-scorpion' - Executing 'res.sam-0' immediately...
[M::main::0.048*1.02] loaded/built the index for 1 target sequence(s)
[M::mm_mapopt_update::0.058*1.02] mid_occ = 12
[M::mm_idx_stat] kmer size: 15; skip: 10; is_hpc: 0; #seq: 1
[M::mm_idx_stat::0.065*1.02] distinct minimizers: 838542 (98.18% are singletons); average occurrences: 1.034; average spacing: 5.352; total length: 4641652
[M::worker_pipeline::1.620*1.00] mapped 1 sequences
[M::main] Version: 2.26-r1175
[M::main] CMD: ./minimap2/minimap2 -a index.mmi GCF_000005845.2_ASM584v2_genomic.fna
[M::main] Real time: 1.626 sec; CPU: 1.626 sec; Peak RSS: 0.115 GB
19:32:52.016 | INFO    | Task run 'res.sam-0' - Finished in state Completed()
19:32:52.031 | INFO    | Flow run 'impartial-scorpion' - Created task run 'flagstat-0' for task 'flagstat'
19:32:52.031 | INFO    | Flow run 'impartial-scorpion' - Executing 'flagstat-0' immediately...
19:32:52.094 | INFO    | Task run 'flagstat-0' - Finished in state Completed()
19:32:52.107 | INFO    | Flow run 'impartial-scorpion' - Created task run 'get_percent-0' for task 'get_percent'
19:32:52.107 | INFO    | Flow run 'impartial-scorpion' - Executing 'get_percent-0' immediately...
19:32:52.150 | INFO    | Task run 'get_percent-0' - Finished in state Completed()
19:32:52.163 | INFO    | Flow run 'impartial-scorpion' - Created task run 'ok_or_not-0' for task 'ok_or_not'
19:32:52.164 | INFO    | Flow run 'impartial-scorpion' - Executing 'ok_or_not-0' immediately...
OK
19:32:52.206 | INFO    | Task run 'ok_or_not-0' - Finished in state Completed()
19:32:52.224 | INFO    | Flow run 'impartial-scorpion' - Finished in state Completed('All states completed.')
