## Data preprocessing
This folder contains a notebook to turn readability html into tokenized text, and then to numerical ids for classifier.

Notebook is written either for Postgresql database with all htmls (commented code), or for `../htmls_sample.jl.bz2` sample of 100k articles. Final output - sequence of token ids at each article - is an input to LM classifier

`itos.pkl` - token dictionaries, composed during fine-tuning of language model. A list of up to 60k most common words with minimum frequency 15.
`classify_tech_tags.pkl` - scikit-learn LogisticRegressionClassifier to detect technical html elements, such as datetime, "read also" paragraps, social media buttons etc.

`langdetect.py` - simple script to detect language with `cld2` or python `langid`.
