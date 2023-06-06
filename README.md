# AICUP 2023 NLP
This contest is about NLI tasks this year.
They will input a claim and we need to judge if this claim "supports", "refutes" or "not enough info"
If they are supports or refutes, we need to provide evidences.

The dataset is based on Wikipedia.

# :pencil2: Instructions for use
* Environment: 
  * Colab or local Jupyter
* Data resources:
  * Google drive link (shown in the Resources block or use gdown in the code to download)
* GPT3 babbage for document retrieval
  * fine-tuning code in in gpt3-helper
  * First, we convert the training data into a format that the model can understand, 
  * using the prompt and completion format (conversion script, conversion result). 
  * Then, we call the OpenAI API to start the training: 
    ``` shell
      "openai api fine_tunes.create -t filled_data.jsonl -m Babbage". 
    ```
  * The training process can be referred to on the OpenAI official website.
  * **Note: We have saved the result files, so you can skip the fine-tuning part**
* RoBERTa-wwm-ext-large for sentence retrieval and claim verification
  * Just follow the code in "AICUP_NLP_2023_final.ipynb" to fine-tuneing

# :triangular_ruler: Structure(overall pass) and Evolution

## Document Retrieval (GPT3.5 Babbage model):
* Search for potential wiki pages that may be relevant to the claim.
* The results of this step will influence the subsequent prediction of test data, including the predicted pages, which will further impact the accuracy of the sentence and label models.
* Input: claim
* Output: possible wiki pages

## Sentence Retrieval (RoBERTa model) (sentence model):
* Utilize a BERT model for sentence retrieval to determine whether a sentence serves as supporting evidence.
* This involves examining the sentences within the identified wiki pages.
* Input: wiki sentences
* Output: predict evidences

## Claim Verification (RoBERTa model) (label model):
* Employ a BERT model for claim verification to assess whether the claim aligns with the predicted evidence as support, refutes, or not enough info.
* Input: claim, predict evidences
* Output: predict label

**Note: The process should be considered separately for training, validation, and testing.**

## Evolution
* Document Retrieval:
  * Rule base: NPs => NER => keyBERT, jieba topk => NPs + NER
  * LLM: GPT3 Babbage (the best)
* Sentence Retrieval: BERT-base-chinese =>  RoBERTa-wwm-ext => RoBERTa-wwm-ext-large
* Claim Verification: BERT-base-chinese =>  RoBERTa-wwm-ext => RoBERTa-wwm-ext-large

# :books: Resources
[Colab Link](https://colab.research.google.com/drive/1LFZKq-gYclWj1r8bbeeBwTmGLjfnyh2a?authuser=1#scrollTo=mHniOctr4AU4)

[Google Drive Data](https://drive.google.com/drive/u/1/folders/1MR8iSpJSNnaVbnZYw2Mrf0Pf0MFrU6VB) (including data and checkpoints model file)

[RoBERTa Chinese](https://github.com/ymcui/Chinese-BERT-wwm)

[OpenAI doc](https://platform.openai.com/docs/guides/fine-tuning)

