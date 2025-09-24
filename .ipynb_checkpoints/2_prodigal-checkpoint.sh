git clone https://github.com/hyattpd/Prodigal.git

cd Prodigal/
make install

pip install biopython
# prodigal -i DATA.fasta -o DATA.gff -d gene.fasta -p meta -a HBV_protein.faa -f gff

# prodigal -i Human.fasta -o Human.gff -d Human_cds.fasta -p meta -a HBV_protein.faa -f gff

