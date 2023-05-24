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

