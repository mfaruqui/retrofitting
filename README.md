#Retrofitting
Manaal Faruqui, manaalfar@gmail.com

This tool is used to post-process word vectors to incorporate
knowledge from semantic lexicons. As shown in Faruqui et al, 2015
these word vectors are generally better in performance on semantic
tasks than the original word vectors. This tool can be used for
word vectors obtained from any vector training model.

###Requirements

1. Python 2.7

###Data you need
1. Word vector file
2. Lexicon file (provided here)

Each vector file should have one word vector per line as follows (space delimited):-

```the -1.0 2.4 -0.3 ...```

###Running the program

```python retrofit.py -i word_vec_file -l lexicon_file -n num_iter -o out_vec_file```

```python retrofit.py -i sample_vec.txt -l lexicons/ppdb-xl.txt -n 10 -o out_vec.txt```

where, 'n' is an integer which specifies the number of iterations for which the
optimization is to be performed.  Usually n = 10 gives reasonable results.

###Output
File: ```out_vec.txt```

which are your new retrofitted and (hopefully) improved word vectors, enjoy !

###Reference

Main paper to be cited
```
@InProceedings{faruqui:2015:NAACL,
  author    = {Faruqui, Manaal and Dodge, Jesse and Jauhar, Sujay K.  and  Dyer, Chris and Hovy, Eduard and Smith, Noah A.},
  title     = {Retrofitting Word Vectors to Semantic Lexicons},
  booktitle = {Proceedings of NAACL},
  year      = {2015},
}
```

If you are using PPDB (Ganitkevitch et al, 2013), WordNet (Miller, 1995) or FrameNet (Baker et al, 1998) for enrichment please cite the corresponding papers.

