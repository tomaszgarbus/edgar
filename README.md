# EDGAR - Entity Driven GPT-2-based Automatic wRiter

EDGAR* is a wrapper around [gpt-2-simple](https://github.com/minimaxir/gpt-2-simple).

It's built of 3 main components:

* gpt-2-simple, forked from the original repository
* A `ner` (Named Entity Recognition) module, capable of annotating text and
  extracting entities after proper configuration.
* Scripts connecting those two dots -- `build_prompts`, which you'll use to annotate
  your dataset; `finetune`, to fit the Transformer to your needs and `generate`,
  to produce your own domain-specific texts.

<sup><sub>*named after my favorite writer</sub></sup>
## Usage
The key step in using EDGAR is building a configuration file for your
domain-specific problem (see the [JSON schema](https://github.com/tomaszgarbus/edgar/blob/master/ner/schema.py)
to see how to do it).

Everything boils down to defining a set of categories
of objects you wish to extract from texts and, for each category, a set of
entities (see the [example football-specific config](https://raw.githubusercontent.com/tomaszgarbus/edgar/master/configs/football.json)).

### Demo Colab notebooks
[Run a demo on Colab](https://colab.research.google.com/drive/1oB6UicgeQEIaGrf2JHD_8AwJXel4gjV0?usp=sharing)
to see EDGAR work on [E2E dataset](https://github.com/tuetschek/e2e-dataset) and
learn how the quality of generated text benefits from using EDGAR versus raw GPT-2.

Alternatively, check out [this notebook](https://colab.research.google.com/drive/1PURy7p7jscwRxjLBnqNaKzxV6hyHPhJe?usp=sharing) to generate football articles using provided config Json.

## License
GPL-3
