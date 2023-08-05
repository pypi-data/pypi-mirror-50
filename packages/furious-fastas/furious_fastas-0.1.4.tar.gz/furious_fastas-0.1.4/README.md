## In Mainz, we believe that fastas are the future

# Rationale
There ain't much to do with fastas but to download them and use.
For this you could open the terminal (or powershell on windows) and type

```console
wget -O human.fasta "http://www.uniprot.org/uniprot/?query=reviewed:yes+AND+organism:9606&format=fasta"
```
to download human database.
Then, to get contaminants used in our group, you could simply type
```console
wget -O contaminants.fasta "https://raw.githubusercontent.com/MatteoLacki/protein_contaminants/master/contaminants.fasta"
```
Finally, you would merge the two files as simple as
```console
cat human.fasta contaminants.fasta > ready.fasta
```
and would feed `ready.fasta` into the software (on Windows you might use `type` instead of `cat`).

However, some software that from a company that I wouldn't like to mention (let me clear my throat with some waters first), require for their scripts to have the files to include reversed sequences.
This can be done easily in Python, as we do it here.

Moreover, we would like to forget about the whole business of updating the fastas.
This can be also achieved with this simple module.
Finally, it's sometimes good to simply parse fasta files for Python scripting.
Well, here it is, too.

Finally, you might want to be sure, that the sequences you input, are not the same, just to be sure that proteins differ.
This is also here.

Best Regards,
Matteo Lacki
