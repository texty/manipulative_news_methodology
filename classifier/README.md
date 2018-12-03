## Scripts, models and data to traine language model-based classifier of manipulations in news.
Based on [fast.ai](https://github.com/fastai/fastai) library, version 0.7.0.

* `training.ipynb` - notebook with classifier of relevant-irrelevant articles, and multilabel classifier of manipulative texts, both in Ukrainian and Russian
* `itos_<lang>.pkl` - token dictionaries
* `ru/`, `uk/` - folders with fastai models. Put models in \<lang\>/models - links to pretrained LM and classifiers:
  
* [Wikipedia language model for Russian, forward LSTM](http://texty.org.ua/d/2018/share/mnews/fwd_ru_lm.zip)
* [Wikipedia language model for Ukrainian, forward LSTM](http://texty.org.ua/d/2018/share/mnews/fwd_uk_lm.zip)
* [Finetuned on news corpus Wikipedia language model for Russian](http://texty.org.ua/d/2018/share/mnews/fwd_ru_finetuned_lm.zip)
* [Finetuned on news corpus Wikipedia language model for Ukrainian](http://texty.org.ua/d/2018/share/mnews/fwd_uk_finetuned_lm.zip)
* [Finetuned on news corpus Wikipedia language model for Russian, encoder only](http://texty.org.ua/d/2018/share/mnews/fwd_ru_finetuned_lm_enc.zip)
* [Finetuned on news corpus Wikipedia language model for Ukrainian, encoder only](http://texty.org.ua/d/2018/share/mnews/fwd_uk_finetuned_lm_enc.zip)
* [Classifier of relevant news in Russian](http://texty.org.ua/d/2018/share/mnews/ru_is_other_cls.zip)
* [Classifier of relevant news in Ukrainian](http://texty.org.ua/d/2018/share/mnews/uk_is_other_cls.zip)
* [Classifier of types of manipulation for Russian](http://texty.org.ua/d/2018/share/mnews/ru_arg_emo_cls.zip)
* [Classifier of types of manipulation for Ukrainian](http://texty.org.ua/d/2018/share/mnews/uk_emo_arg_cls.zip)

  
* `<lang>_test_set.jl` - more thoroughly annotated random sets of news in Russian and Ukraininan, that were not involved in training.
