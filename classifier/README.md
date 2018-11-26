## Scripts, models and data for training language model-based classifier of manipulative news texts

* `training.ipynb` - notebook with classifier of relevant-irrelevant articles, and multilabel classifier of manipulative texts, both in Ukrainian and Russian
* `itos.pkl` - token dictionaries
* `ru/`, `uk/` - folders with fastai models. Contains pretrained language model encoder for each language, as well as relevance and manipulation classifiers 
* `.._test_set.jl` - more thoroughly annotated random sets of news in Russian and Ukraininan, that were not involved in training.