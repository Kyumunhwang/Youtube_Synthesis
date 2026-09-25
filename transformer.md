Title: Transformer (deep learning)

URL Source: https://en.wikipedia.org/wiki/Transformer_(deep_learning_architecture)

Published Time: 2019-08-25T16:32:02Z

Markdown Content:
Jump to content
Main menu
Search
Donate
Create account
Log in
Contents hide
(Top)
History
Toggle History subsection
Training
Toggle Training subsection
Architecture
Toggle Architecture subsection
Full transformer architecture
Toggle Full transformer architecture subsection
Subsequent work
Toggle Subsequent work subsection
Applications
See also
Notes
References
Further reading
Transformer (deep learning)
36 languages
Article
Talk
Read
Edit
View history
Tools
Appearance hide
From Wikipedia, the free encyclopedia
(Redirected from Transformer (deep learning architecture))
	
This article has multiple issues. Please help improve it or discuss these issues on the talk page. (Learn how and when to remove these messages)
This article needs more citations. (June 2026)
Some of this article's listed sources may not be reliable. (June 2026)
A standard transformer architecture, showing on the left an encoder, and on the right a decoder. Note: this uses the pre-LN convention, which is different from the post-LN convention used in the original 2017 transformer.
Part of a series on
Machine learning
and
data mining

Paradigms


Problems


Supervised learning
(classification • regression)


Clustering


Dimensionality reduction


Structured prediction


Anomaly detection


Neural networks
AutoencoderDeep learningFeedforward neural networkRecurrent neural network LSTMGRUESNreservoir computingBoltzmann machine RestrictedGANDiffusion modelSOMConvolutional neural network U-NetLeNetAlexNetDeepDreamNeural field Neural radiance fieldPhysics-informed neural networksTransformer VisionMambaSpiking neural networkMemtransistorElectrochemical RAM (ECRAM)


Reinforcement learning


Learning with humans


Model diagnostics


Mathematical foundations


Journals and conferences


Related articles

vte

In deep learning, the transformer is a family of artificial neural network architectures based on the multi-head attention mechanism, in which input data such as text, images, or audio, is converted to a sequence of numerical representations called tokens, and each token is converted into a vector through an embedding layer.[1] At each layer, each token is then contextualized within the scope of the context window with other (unmasked) tokens via a parallel multi-head attention mechanism, allowing the signal for key tokens to be amplified and less important tokens to be diminished. Because self-attention alone is permutation-invariant, transformers inject positional information, typically through positional encodings or learned positional embeddings, so token order can affect the output.[1]

Because transformers do not process tokens one at a time, their computations can be parallelized across sequence positions during training more readily than those of recurrent neural networks like long short-term memory (LSTM).[2] Later variations have been widely adopted for training large language models (LLMs) on large (language) datasets.[3] Modern transformer designs are commonly grouped into encoder-only, decoder-only, and encoder-decoder variants, depending on whether they are optimized for representation learning, autoregressive generation, or conditional sequence-to-sequence tasks.[4]

The original version of the transformer architecture was proposed in the 2017 paper "Attention Is All You Need" by researchers at Google.[1] The predecessors of transformers were developed as an improvement over previous architectures for machine translation,[5][6] but have found many applications since. They are used in large-scale natural language processing, computer vision (vision transformers), reinforcement learning,[7][8] audio,[9] multimodal learning, robotics,[10] and playing chess.[11] It has also led to the development of pre-trained systems, such as generative pre-trained transformers (GPTs)[12] and BERT[13] (bidirectional encoder representations from transformers).

Historyedit
	
This section's style of writing may not reflect the encyclopedic tone used on Wikipedia. See Wikipedia's guide to writing better articles for suggestions. (February 2026) (Learn how and when to remove this message)
See also: Timeline of machine learning
Predecessorsedit

Before transformers, recurrent neural networks (RNNs) were widely used for sequence modelling and generation. A well-cited early example was the Elman network (1990). In theory, the information from one token can propagate arbitrarily far down the sequence, but in practice the vanishing-gradient problem leaves the model's state at the end of a long sentence without precise, extractable information about preceding tokens.

A key breakthrough was LSTM (originally described in a 1995 technical report and formally published in 1997),[2][note 1] an RNN that introduced gating mechanisms to mitigate the vanishing gradient problem, allowing efficient learning of long-sequence modelling. One key architectural element was the use of multiplicative gating units, in which the outputs of some neurons modulate the outputs of others. These multiplicative units are conceptually distinct from the additive attention mechanism later introduced for sequence-to-sequence models. [14] Neural networks using multiplicative units were later called sigma-pi networks[15] or higher-order networks.[16] LSTM became the standard architecture for long sequence modelling until the 2017 publication of transformers. However, LSTM still used sequential processing, like most other RNNs.[note 2] Specifically, RNNs operate one token at a time from first to last; they cannot operate in parallel over all tokens in a sequence.

Transformers allow parallel processing of tokens during training, but standard self-attention has computational and memory costs that grow quadratically with sequence length. The fast weight controller, proposed in 1992, used one network to generate input-dependent weights for another network. This method built on earlier work on "fast weights" and "dynamic links".[17][18][19] A slow neural network learns by gradient descent to generate keys and values for computing the weight changes of the fast neural network which computes answers to queries.[20] This was later shown to be equivalent to the unnormalized linear transformer.[21][22]

Attention with seq2seqedit
Main article: Seq2seq § History

The idea of encoder–decoder sequence transduction had been developed in the early 2010s; commonly cited as the originators that produced seq2seq are two concurrently published papers from 2014.[23][24][original research?]

A 380M-parameter model for machine translation uses two long short-term memories (LSTM).[24] Its architecture consists of two parts. The encoder is an LSTM that takes in a sequence of tokens and turns it into a vector. The decoder is another LSTM that converts the vector into a sequence of tokens. Similarly, another 130M-parameter model used gated recurrent units (GRU) instead of LSTM.[23] Later research showed that GRUs are neither better nor worse than LSTMs for seq2seq.[25][26]

These early seq2seq models had no attention mechanism, and the state vector is accessible only after the last word of the source text was processed. Although in theory such a vector retains the information about the whole original sentence, in practice the information is poorly preserved. This is because the input is processed sequentially by one recurrent network into a fixed-size output vector, which is then processed by another recurrent network into an output. If the input is long, then the output vector would not be able to contain all relevant information, degrading the output. As evidence, reversing the input sentence improved seq2seq translation.[27]

The RNN search model introduced an attention mechanism to seq2seq for machine translation to solve the bottleneck problem (of the fixed-size output vector), allowing the model to process long-distance dependencies more easily. The name is because it "emulates searching through a source sentence during decoding a translation".[5]

The relative performances were compared between global (that of RNN search) and local (sliding window) attention model architectures for machine translation, finding that mixed attention had higher quality than global attention, while local attention reduced translation time.[28]

In 2016, Google Translate was revamped to Google Neural Machine Translation, which replaced the previous model based on statistical machine translation. The new model was a seq2seq model where the encoder and the decoder were both 8 layers of bidirectional LSTM.[29] It took nine months to develop, and it outperformed the statistical approach, which took ten years to develop.[30]

Parallelizing attentionedit
Main article: Attention (machine learning) § History

Seq2seq models with attention (including self-attention) still suffered from the same issue with recurrent networks, which is that they are hard to parallelize, which prevented them from being accelerated on GPUs. In 2016, decomposable attention applied a self-attention mechanism to feedforward networks, which are easy to parallelize, and achieved SOTA result in textual entailment with an order of magnitude fewer parameters than LSTMs.[31] One of its authors, Jakob Uszkoreit, suspected that attention without recurrence would be sufficient for language translation, thus the title "attention is All you need".[32] That hypothesis was against conventional wisdom at the time, and even his father Hans Uszkoreit, a well-known computational linguist, was skeptical.[32] In the same year, self-attention (called intra-attention or intra-sentence attention) was proposed for LSTMs.[33]

On 2017-06-12, the original (100M-parameter) encoder–decoder transformer model was published in the "Attention is All you need" paper. At the time, the focus of the research was on improving seq2seq for machine translation, by removing its recurrence to process all tokens in parallel, but preserving its dot-product attention mechanism to keep its text processing performance.[1] This led to the introduction of a multi-head attention model that was easier to parallelize due to the use of independent heads and the lack of recurrence. Its parallelizability was an important factor to its widespread use in large neural networks.[34]

AI boom eraedit

As early as spring 2017, even before the "Attention is All you need" preprint was published, one of the co-authors applied the "decoder-only" variation of the architecture to generate fictitious Wikipedia articles.[35] Transformer architecture is now used alongside many generative models that contribute to the ongoing AI boom.

The "reference implementation" of the original Transformer was written in a TensorFlow library.[36][37] In language modelling, ELMo (2018) was a bi-directional LSTM that produces contextualized word embeddings, improving upon the line of research from bag of words and word2vec. It was followed by BERT (2018), an encoder-only transformer model.[38] In October 2019, Google started using BERT to process search queries.[39] In 2020, Google Translate replaced the previous RNN-encoder–RNN-decoder model by a transformer-encoder–RNN-decoder model.[40]

Starting in 2018, the OpenAI GPT series of decoder-only transformers became state of the art in natural language generation. In November 2022, OpenAI released ChatGPT, a chatbot based on a fine-tuned variant of GPT-3.5. It's rapid public adoption increased public and commercial attention to large language models.[41][42][43][44]

The following development of multimodal systems improved transformer-based models beyond text by combining language processing with image, audio, video, or other data representations. Such systems typically encode each modality into vectors or tokens that can be processed jointly or connected through cross-attention mechanisms.[45]

Transformers have been applied in modalities beyond text. Four days after the publication of "Attention is All You Need", a multimodal transformer architecture, MultiModel, was published by most authors of that paper.[46] Other examples include the vision transformer,[47] speech recognition,[48] robotics,[7] and multimodal.[49] The vision transformer, in turn, stimulated new developments in convolutional neural networks.[50] Image and video generators like DALL-E (2021), Stable Diffusion 3 (2024),[51] and Sora (2024), use transformers to analyse input data (like text prompts) by breaking it down into "tokens" and then calculating the relevance between each token using self-attention, which helps the model understand the context and relationships within the data.

Trainingedit
Methods for stabilizing trainingedit

The plain transformer architecture had difficulty in converging. In the original paper,[1] the authors recommended using learning rate warmup. That is, the learning rate should linearly scale up from 0 to maximal value for the first part of the training (usually recommended to be 2% of the total number of training steps), before decaying again.

A 2020 paper found that using layer normalization before (instead of after) multihead attention and feedforward layers stabilizes training, not requiring learning rate warmup.[52] This is the "pre-LN Transformer" and is more commonly used, compared to the original "post-LN Transformer".

Pretrain-finetuneedit

Transformers typically are first pretrained by self-supervised learning on a large generic dataset, followed by supervised fine-tuning on a small task-specific dataset. The pretrain dataset is typically an unlabeled large corpus, such as The Pile. Tasks for pretraining and fine-tuning commonly include:

language modeling[13]
next-sentence prediction[13]
question answering[3]
reading comprehension
sentiment analysis[1]
paraphrasing[1]

The T5 transformer report[53] documents a large number of natural language pretraining tasks. Some examples are:

restoring or repairing incomplete or corrupted text. For example, the input, "Thank you ~~ me to your party ~~ week", might generate the output, "Thank you for inviting me to your party last week".
translation between natural languages (machine translation)
judging the pragmatic acceptability of natural language. For example, the following sentence might be judged "not acceptable",[54] because even though it is syntactically well-formed, it is improbable in ordinary human usage: The course is jumping well.

While each of these tasks is trivial or obvious for human native speakers of the language (or languages), they have typically proved challenging for previous generations of machine learning architecture.

Parameter-efficient fine-tuningedit
Main article: Parameter-efficient fine-tuning

Fine-tuning every parameter of a large transformer needs substantial memory and storage, particularly when separate versions of a model are needed for multiple tasks. Parameter-efficient fine-tuning methods adapt a pretrained model while updating only a relatively small set of additional or selected parameters. Examples include adapters, prompt tuning, and low-rank adaptation (LoRA).[55]

In low-rank adaptation, the original weight matrices are kept fixed while trainable low-rank matrices are added to selected layers. The method reduces the number of trainable parameters and can allow multiple task-specific adaptations to share the same base model.[56]

Tasksedit
See also: Large language model § Evaluation

In general, there are three classes of language modelling tasks: "masked",[57] "autoregressive",[58] and "prefixLM".[59] These classes are independent of a specific modeling architecture such as transformer, but they are often discussed in the context of transformer.

In a masked task,[57] one or more of the tokens is masked out, and the model would produce a probability distribution predicting what the masked-out tokens are based on the context. The loss function for the task is typically sum of log-perplexities for the masked-out tokens:
Loss
=
−
∑
𝑡
∈
masked tokens
ln
⁡
(
probability of 
𝑡
 conditional on its context
)
and the model is trained to minimize this loss function. The BERT series of models are trained for masked token prediction and another task. ("Masked" as in "masked language modelling" is not "masked" as in "masked attention".)

In an autoregressive task,[58] the entire sequence is masked at first, and the model produces a probability distribution for the first token. Then the first token is revealed and the model predicts the second token, and so on. The loss function for the task is still typically the same. The GPT series of models are trained by autoregressive tasks.

In a prefixLM task,[59] the sequence is divided into two parts. The first part is presented as context, and the model predicts the first token of the second part. Then that would be revealed, and the model predicts the second token, and so on. The loss function for the task is still typically the same. The T5 series of models are trained by prefixLM tasks. ("PrefixLM" as in "prefix language modeling" is not "prefixLM" as in "prefix language model".)

Architectureedit

All transformers have the same primary components:

Tokenizers, which convert text into tokens.
Embedding layer, which converts tokens and positions of the tokens into vector representations.
Transformer layers, which carry out repeated transformations on the vector representations, extracting more and more linguistic information. These consist of alternating attention and feedforward layers. There are two major types of transformer layers: encoder layers and decoder layers, with further variants.
Un-embedding layer, which converts the final vector representations back to a probability distribution over the tokens.

The following description follows exactly the transformer as described in the original paper. There are variants, described in the following section.

By convention, we write all vectors as row vectors. For example, pushing a vector through a linear layer means multiplying it by a weight matrix on the right, as 
𝑥
𝑊
.

Tokenizationedit

As the transformer architecture natively consists of operations over numbers (matrix multiplications, dot products, activation functions) rather than over text, there must first be a mapping from any input text to some numerical representation. This happens in three steps.

First, the input text is treated by a preprocessor, which performs both textual transformations and splits the text into coarse-grained segments called pretokens. The latter is referred to as pretokenization. Second, each pretoken is segmented further into tokens by a tokenizer that expects to only see pretokens output by its preprocessor. Each token it produces is a string of one or more characters belonging to a finite set of strings called the vocabulary 
𝑉
. Third, because the vocabulary is finite and known beforehand, each token can be assigned an integer identifier, and this mapping is applied to the sequence of tokens to represent any input text as a numerical sequence. Since this mapping is bijective, the output side can produce a sequence of integer identifiers which can then be turned back into tokens. After undoing some of the preprocessing, the result is again legible text.

Training a tokenizer (sometimes referred to as vocabularization) means finding a suitable vocabulary 
𝑉
, but also learning how to use it, since any given string 
𝑠
 of length 
|
𝑠
|
 has 
2
|
𝑠
|
−
1
 hypothetical segmentations, some of which containing segments that are not in the vocabulary. The most important hyperparameter during vocabularization is the vocabulary size 
|
𝑉
|
: when it is small, the learned vocabulary generally consists of characters and smaller strings, and words will be segmented into many tokens. At larger sizes, it becomes affordable to dedicate tokens to full words, although depending on the preprocessor and tokenizer, it is not necessarily the case that large vocabularies will always use the largest token(s) available to segment a word.

Because tokens are not always full words, they may also be referred to as subwords and tokenization algorithms may be referred to as subword tokenizers. This is also to differentiate these systems from traditional terminology used in older information retrieval and natural language processing systems, where "tokenization" was used to denote what is today called "pretokenization" (very crudely: splitting into words). In tokenizers that produce tokens that are not part of the vocabulary, a special token that does belong to the vocabulary is used as a generic stand-in, written as "[UNK]" for "unknown". In principle, any string could be hidden by such an [UNK]. Indeed, in information retrieval, pretokenizers were themselves used as tokenizers (and also called "tokenizers") with a word-level vocabulary that contained an [UNK].

Commonly used subword tokenization algorithms are byte pair encoding (BPE) and the unigram language model (ULM), which each include a vocabularization algorithm and a dedicated segmentation algorithm. There also exist several segmentation algorithms that require no learning and can be applied given a vocabulary (produced by BPE or ULM, for example), like greedily recognising tokens in a pretoken by moving through it left-to-right. Well-known software implementations of subword tokenizers are Hugging Face's tokenizers Python package implemented in Rust, and the sentencepiece Python package implemented in C++. The latter package is named as such because one of its configuration options allows disabling the built-in pretokenizer, hence effectively making entire sentences a pretoken and thus having the tokenizer see entire sentences, rather than individual words.

Embeddingedit
Further information: Word embedding

Each integer token identifier is converted into an embedding vector via a lookup table. Equivalently stated, it multiplies a one-hot representation of the token identifier by an embedding matrix 
𝑀
. For example, if the input token's identifier is 
3
, then the one-hot representation is 
[
0
,
0
,
0
,
1
,
0
,
0
,
…
]
, and its embedding vector is
E
m
b
e
d
(
3
)
=
[
0
,
0
,
0
,
1
,
0
,
0
,
…
]
𝑀
The token embedding vectors are added to their respective positional encoding vectors (see below), producing the sequence of input vectors.

The dimension of an embedding vector is called hidden size or embedding size and written as 
𝑑
emb
.[38] This size is written as 
𝑑
model
 in the original transformer paper.[1]

Un-embeddingedit

An un-embedding layer is almost the reverse of an embedding layer. Whereas an embedding layer converts a token identifier into a vector, an un-embedding layer converts a vector into a probability distribution over tokens.

An illustration of the top 16 token probabilities at temperature 1, for each output token in the chain-of-thought response, with colour representing how that output differs from the same prompt but at temperature 0.

The un-embedding layer is a linear-softmax layer:
U
n
E
m
b
e
d
(
𝑥
)
=
s
o
f
t
m
a
x
(
𝑥
𝑊
+
𝑏
)
The matrix has shape 
(
𝑑
emb
,
|
𝑉
|
)
. Some architectures use the transpose of the embedding matrix 
𝑀
 as the un-embedding matrix 
𝑊
 in order to avoid needing double the amount of embedding-related parameters and to avoid divergence during training. This practice is called weight tying.[60]

Positional encodingedit
Illustration of (absolute) positional encoding with parameters 
𝑁
=
10000
,
𝑑
=
100

A positional encoding is a fixed-size vector representation of the relative positions of tokens within a sequence: it provides the transformer model with information about where the words are in the input sequence. This induces a bias towards the order of the input sequence, so that, for example, the input sequence "man bites dog" is processed differently from "dog bites man".

The positional encoding is defined as a function of type 
𝑓
:
𝑅
→
𝑅
𝑑
, where 
𝑑
 is a positive even integer. The full positional encoding defined in the original paper[1] is:
(
𝑓
(
𝑡
)
2
𝑘
,
𝑓
(
𝑡
)
2
𝑘
+
1
)
=
(
sin
⁡
(
𝜃
)
,
cos
⁡
(
𝜃
)
)
∀
𝑘
∈
{
0
,
1
,
…
,
𝑑
/
2
−
1
}
where 
𝜃
=
𝑡
𝑟
𝑘
,
𝑟
=
𝑁
2
/
𝑑
.

Here, 
𝑁
 is a free parameter that should be significantly larger than the biggest 
𝑘
 that would be input into the positional encoding function. The original paper uses 
𝑁
=
10000
.

The function is in a simpler form when written as a complex function of type 
𝑓
:
𝑅
→
𝐶
𝑑
/
2
𝑓
(
𝑡
)
=
(
𝑒
𝑖
𝑡
/
𝑟
𝑘
)
𝑘
=
0
,
1
,
…
,
𝑑
2
−
1
where 
𝑟
=
𝑁
2
/
𝑑
.

The main reason for using this positional encoding function is that using it, shifts are linear transformations:
𝑓
(
𝑡
+
Δ
𝑡
)
=
d
i
a
g
(
𝑓
(
Δ
𝑡
)
)
𝑓
(
𝑡
)
where 
Δ
𝑡
∈
𝑅
 is the distance one wishes to shift. This allows the transformer to take any encoded position, and find the encoding of the position n-steps-ahead or n-steps-behind, by a matrix multiplication.

By taking a linear sum, any convolution can also be implemented as linear transformations:
∑
𝑗
𝑐
𝑗
𝑓
(
𝑡
+
Δ
𝑡
𝑗
)
=
(
∑
𝑗
𝑐
𝑗
d
i
a
g
(
𝑓
(
Δ
𝑡
𝑗
)
)
)
𝑓
(
𝑡
)
for any constants 
𝑐
𝑗
. This allows the transformer to take any encoded position and find a linear sum of the encoded locations of its neighbors. This sum of encoded positions, when fed into the attention mechanism, would create attention weights on its neighbors, much like what happens in a convolutional neural network language model. In the author's words, "we hypothesized it would allow the model to easily learn to attend by relative position."

In typical implementations, all operations are done over the real numbers, not the complex numbers, but since complex multiplication can be implemented as real 2-by-2 matrix multiplication, this is a mere notational difference.

Encoder–decoder (overview)edit
One encoder–decoder block
A transformer is composed of stacked encoder layers and decoder layers.

Like earlier seq2seq models, the original transformer model used an encoder–decoder architecture. The encoder consists of encoding layers that process all the input tokens together one layer after another, while the decoder consists of decoding layers that iteratively process the encoder's output and the decoder's output tokens so far.

The purpose of each encoder layer is to create contextualized representations of the tokens, where each representation corresponds to a token that "mixes" information from other input tokens via self-attention mechanism. Each decoder layer contains two attention sublayers: (1) cross-attention for incorporating the output of encoder (contextualized input token representations), and (2) self-attention for "mixing" information among the input tokens to the decoder (i.e. the tokens generated so far during inference time).[61][62]

Both the encoder and decoder layers have a feed-forward neural network for additional processing of their outputs and contain residual connections and layer normalization steps.[62] These feed-forward layers contain most of the parameters in a transformer model.

Feedforward networkedit

The feedforward network module. It is a two-layered network that maps 
𝑑
emb
-dimensional vectors into 
𝑑
emb
-dimensional vectors.

The feedforward network (FFN) modules in a transformer are 2-layered multilayer perceptrons:
F
F
N
(
𝑥
)
=
𝜙
(
𝑥
𝑊
(
1
)
+
𝑏
(
1
)
)
𝑊
(
2
)
+
𝑏
(
2
)
where 
𝑊
(
1
)
 and 
𝑊
(
2
)
 are weight matrices and 
𝑏
(
1
)
 and 
𝑏
(
2
)
 are bias vectors, and 
𝜙
 is its activation function. The original transformer used ReLU activation.

The number of neurons in the middle layer is called intermediate size (GPT),[63] filter size (BERT),[38] or feedforward size (BERT).[38] It is typically larger than the embedding size. For example, in both GPT-2 series and BERT series, the intermediate size of a model is 4 times its embedding size: 
𝑑
ffn
=
4
𝑑
emb
.

Scaled dot-product attentionedit
Main article: Dot-product attention
Attention headedit
Scaled dot-product attention, block diagram
Exact dimension counts within an attention head module

The attention mechanism used in the transformer architecture are scaled dot-product attention units. For each unit, the transformer model learns three weight matrices: the query weights 
𝑊
𝑄
, the key weights 
𝑊
𝐾
, and the value weights 
𝑊
𝑉
.

The module takes three sequences, a query sequence, a key sequence, and a value sequence. The query sequence is a sequence of length 
ℓ
seq, query
, and each entry is a vector of dimension 
𝑑
emb, query
. Similarly for the key and value sequences.

For each vector 
𝑥
𝑖
,
query
 in the query sequence, it is multiplied by a matrix 
𝑊
𝑄
 to produce a query vector 
𝑞
𝑖
=
𝑥
𝑖
,
query
𝑊
𝑄
. The matrix of all query vectors is the query matrix:
𝑄
=
𝑋
query
𝑊
𝑄
Similarly, we construct the key matrix 
𝐾
=
𝑋
key
𝑊
𝐾
 and the value matrix 
𝑉
=
𝑋
value
𝑊
𝑉
.

It is usually the case that all 
𝑊
𝑄
,
𝑊
𝐾
,
𝑊
𝑉
 are square matrices, meaning 
𝑑
emb, query
=
𝑑
query
, etc.

Attention weights are calculated using the query and key vectors: the attention weight 
𝑎
𝑖
𝑗
 from token 
𝑖
 to token 
𝑗
 is the dot product between 
𝑞
𝑖
 and 
𝑘
𝑗
. The attention weights are divided by the square root of the dimension of the key vectors, 
𝑑
𝑘
, which stabilizes gradients during training, and passed through a softmax which normalizes the weights. The fact that 
𝑊
𝑄
 and 
𝑊
𝐾
 are different matrices allows attention to be non-symmetric: if token 
𝑖
 attends to token 
𝑗
 (i.e. 
𝑞
𝑖
⋅
𝑘
𝑗
 is large), this does not necessarily mean that token 
𝑗
 will attend to token 
𝑖
 (i.e. 
𝑞
𝑗
⋅
𝑘
𝑖
 could be small). The output of the attention unit for token 
𝑖
 is the weighted sum of the value vectors of all tokens, weighted by 
𝑎
𝑖
𝑗
, the attention from token 
𝑖
 to each token.

The attention calculation for all tokens can be expressed as one large matrix calculation using the softmax function, which is useful for training due to computational matrix operation optimizations that quickly compute matrix operations. The matrices 
𝑄
, 
𝐾
 and 
𝑉
 are defined as the matrices where the 
𝑖
th rows are vectors 
𝑞
𝑖
, 
𝑘
𝑖
, and 
𝑣
𝑖
 respectively. Then we can represent the attention as
Attention
(
𝑄
,
𝐾
,
𝑉
)
=
softmax
(
𝑄
𝐾
T
𝑑
𝑘
)
𝑉

where the softmax is applied over each of the rows of the matrix.

The number of dimensions in a query vector is query size 
𝑑
query
 and similarly for the key size 
𝑑
key
 and value size 
𝑑
value
. The output dimension of an attention head is its head dimension 
𝑑
head
. The attention mechanism requires the following three equalities to hold:
ℓ
seq, key
=
ℓ
seq, value
,
𝑑
query
=
𝑑
key
,
𝑑
value
=
𝑑
head
but is otherwise unconstrained.

If the attention head is used in a self-attention fashion, then 
𝑋
query
=
𝑋
key
=
𝑋
value
. If the attention head is used in a cross-attention fashion, then usually 
𝑋
query
≠
𝑋
key
=
𝑋
value
. It is theoretically possible for all three to be different, but that is rarely the case in practice.

Multihead attentionedit
Multihead attention, block diagram
Exact dimension counts within a multihead attention module

One set of 
(
𝑊
𝑄
,
𝑊
𝐾
,
𝑊
𝑉
)
 matrices is called an attention head, and each layer in a transformer model has multiple attention heads. While each attention head attends to the tokens that are relevant to each token, multiple attention heads allow the model to do this for different definitions of "relevance". Specifically, the query and key projection matrices, 
𝑊
𝑄
 and 
𝑊
𝐾
 , which are involved in the attention score computation, defines the "relevance". Meanwhile, the value projection matrix 
𝑊
𝑉
, in combination with the part of the output projection matrix 
𝑊
𝑂
, determines how the attended tokens influence what information is passed to subsequent layers and ultimately the output logits. In addition, the scope of attention, or the range of token relationships captured by each attention head, can expand as tokens pass through successive layers. This allows the model to capture more complex and long-range dependencies in deeper layers. Many transformer attention heads encode relevance relations that are meaningful to humans. For example, some attention heads can attend mostly to the next word, while others mainly attend from verbs to their direct objects.[64] The computations for each attention head can be performed in parallel, which allows for fast processing. The outputs for the attention layer are concatenated to pass into the feedforward neural network layers.

Concretely, let the multiple attention heads be indexed by 
𝑖
, then we have
MultiheadAttention
(
𝑄
,
𝐾
,
𝑉
)
=
Concat
𝑖
∈
[
𝑛
heads
]
(
Attention
(
𝑋
𝑊
𝑖
𝑄
,
𝑋
𝑊
𝑖
𝐾
,
𝑋
𝑊
𝑖
𝑉
)
)
𝑊
𝑂
where the matrix 
𝑋
 is the concatenation of word embeddings, and the matrices 
𝑊
𝑖
𝑄
,
𝑊
𝑖
𝐾
,
𝑊
𝑖
𝑉
 are "projection matrices" owned by individual attention head 
𝑖
, and 
𝑊
𝑂
 is a final projection matrix owned by the whole multihead attention head.

It is theoretically possible for each attention head to have a different head dimension 
𝑑
head
, but that is rarely the case in practice.

As an example, in the smallest GPT-2 model, there are only self-attention mechanisms. It has the following dimensions:
𝑑
emb
=
768
,
𝑛
head
=
12
,
𝑑
head
=
64
Since 
12
×
64
=
768
, its output projection matrix 
𝑊
𝑂
∈
𝑅
(
12
×
64
)
×
768
 is a square matrix.

Masked attentionedit

The transformer architecture is constructed to calculate output tokens iteratively. Assuming 
𝑡
=
0
 refers to the calculation of the first output token 
𝑖
=
0
, for step 
𝑡
>
0
, the output token 
𝑖
=
0
 shall remain constant. This ensures properties of the model similar to autoregressive models.[1] Therefore, at every time step 
𝑡
, the calculation for all outputs 
𝑖
 should not have access to tokens at position 
𝑗
 for 
𝑗
>=
𝑖
 (as it naturally is the case for time step 
𝑡
=
𝑖
, when tokens 
𝑗
>
𝑡
 are not yet calculated). This behavior may be accomplished before the softmax stage by adding a mask matrix 
𝑀
 that is 
−
∞
 at entries where the attention link must be cut, and 
0
 at other places:
MaskedAttention
(
𝑄
,
𝐾
,
𝑉
)
=
softmax
(
𝑀
+
𝑄
𝐾
T
𝑑
𝑘
)
𝑉
The following matrix is commonly used in decoder self-attention modules, called "causal masking":
𝑀
causal
=
[
0
	
−
∞
	
−
∞
	
…
	
−
∞


0
	
0
	
−
∞
	
…
	
−
∞


0
	
0
	
0
	
…
	
−
∞


⋮
	
⋮
	
⋮
	
⋱
	
⋮


0
	
0
	
0
	
…
	
0
]

In words, it means that each token can pay attention to itself, and every token before it, but not any after it. A non-masked attention module can be thought of as a masked attention module where the mask has all entries zero. As an example of an uncommon use of mask matrix, the XLNet considers all masks of the form 
𝑃
𝑀
causal
𝑃
−
1
, where 
𝑃
 is a random permutation matrix.[65]

Encoderedit
One encoder layer

An encoder consists of an embedding layer, followed by multiple encoder layers.

Each encoder layer consists of two major components: a self-attention mechanism and a feed-forward layer. It takes an input as a sequence of input vectors, applies the self-attention mechanism, to produce an intermediate sequence of vectors, then applies the feed-forward layer for each vector individually. Schematically, we have:
given input vectors 
	
ℎ
0
,
ℎ
1
,
…


combine them into a matrix 
𝐻
	
=
[
ℎ
0


ℎ
1


⋮
]


EncoderLayer
(
𝐻
)
	
=
[
FFN
(
MultiheadAttention
(
𝐻
,
𝐻
,
𝐻
)
0
)


FFN
(
MultiheadAttention
(
𝐻
,
𝐻
,
𝐻
)
1
)


⋮
]

where 
FFN
 stands for "feed-forward network". We can more succinctly write it as
EncoderLayer
(
𝐻
)
=
FFN
(
MultiheadAttention
(
𝐻
,
𝐻
,
𝐻
)
)
with the implicit convention that the 
FFN
 is applied to each row of the matrix individually.

The encoder layers are stacked. The first encoder layer takes the sequence of input vectors from the embedding layer, producing a sequence of vectors. This sequence of vectors is processed by the second encoder, and so on. The output from the final encoder layer is then used by the decoder.

As the encoder processes the entire input all at once, every token can attend to every other token (all-to-all attention), so there is no need for causal masking.

Decoderedit
One decoder layer

A decoder consists of an embedding layer, followed by multiple decoder layers, followed by an un-embedding layer.

Each decoder consists of three major components: a causally masked self-attention mechanism, a cross-attention mechanism, and a feed-forward neural network. The decoder functions in a similar fashion to the encoder, but an additional attention mechanism is inserted which instead draws relevant information from the encodings generated by the encoders. This mechanism can also be called the encoder–decoder attention.[1][62]

Like the first encoder, the first decoder takes positional information and embeddings of the output sequence as its input, rather than encodings. The transformer must not use the current or future output to predict an output, so the output sequence must be partially masked to prevent this reverse information flow.[1] This allows for autoregressive text generation. For decoding, all-to-all attention is inappropriate, because a token cannot attend to tokens not yet generated. Thus, the self-attention module in the decoder is causally masked.

In contrast, the cross-attention mechanism attends to the output vectors of the encoder, which is computed before the decoder starts decoding. Consequently, there is no need for masking in the cross-attention mechanism.

Schematically, we have:
𝐻
′
	
=
MaskedMultiheadAttention
(
𝐻
,
𝐻
,
𝐻
)


DecoderLayer
(
𝐻
)
	
=
FFN
(
MultiheadAttention
(
𝐻
′
,
𝐻
𝐸
,
𝐻
𝐸
)
)
where 
𝐻
𝐸
 is the matrix with rows being the output vectors from the encoder.

The last decoder is followed by a final un-embedding layer to produce the output probabilities over the vocabulary. Then, one of the tokens is sampled according to the probability, and the decoder can be run again to produce the next token, etc., autoregressively generating output text.

Full transformer architectureedit
Sublayersedit
(a) One encoder layer and one decoder layer. (b) Two encoder layers and two decoder layers. The sublayers are labelled as well.

Each encoder layer contains 2 sublayers: the self-attention and the feedforward network. Each decoder layer contains 3 sublayers: the causally masked self-attention, the cross-attention, and the feedforward network.

Transformer encoder with norm-first and norm-last
Transformer decoder with norm-first and norm-last
Block diagram for the full transformer architecture
Schematic object hierarchy for the full transformer architecture, in object-oriented programming style

The final points of detail are the residual connections and layer normalization, (denoted as "LayerNorm", or "LN" in the following), which while conceptually unnecessary, are necessary for numerical stability and convergence.

The residual connections are introduced to avoid vanishing gradient issues and stabilize the training process. They can be expressed by 
𝑥
↦
𝐹
(
𝑥
)
+
𝑥
, where 
𝐹
 is a given component of the transformer. Adding the input 
𝑥
 can preserve the input information and avoid issues when the gradient of 
𝐹
(
𝑥
)
 is close to zero.

Similarly to how the feedforward network modules are applied individually to each vector, the LayerNorm is also applied individually to each vector.

There are two common conventions in use: the post-LN and the pre-LN convention. In the post-LN convention, the output of each sublayer is
L
a
y
e
r
N
o
r
m
(
𝑥
+
S
u
b
l
a
y
e
r
(
𝑥
)
)
where 
S
u
b
l
a
y
e
r
(
𝑥
)
 is the function implemented by the sublayer itself.

In the pre-LN convention, the output of each sublayer is
𝑥
+
S
u
b
l
a
y
e
r
(
L
a
y
e
r
N
o
r
m
(
𝑥
)
)
The original 2017 transformer used the post-LN convention. It was difficult to train and required careful hyperparameter tuning and a "warm-up" in learning rate, where it starts small and gradually increases. The pre-LN convention, proposed several times in 2018,[66] was found to be easier to train, requiring no warm-up, leading to faster convergence.[52]

Pseudocodeedit

The following is the pseudocode for a standard pre-LN encoder–decoder transformer, adapted from Formal Algorithms for Transformers.[67]

input: Encoder input t_e
       Decoder input t_d
output: Array of probability distributions, with shape (decoder vocabulary size x length(decoder output sequence))

/* encoder */
z_e ← encoder.tokenizer(t_e)

for each t in 1:length(z_e) do
    z_e[t] ← encoder.embedding(z_e[t]) + encoder.positional_embedding(t)

for each l in 1:length(encoder.layers) do
    layer ← encoder.layers[l]

    /* first sublayer */
    z_e_copy ← copy(z_e)
    for each t in 1:length(z_e) do
        z_e[t] ← layer.layer_norm(z_e[t])
    z_e ← layer.multihead_attention(z_e, z_e, z_e)
    for each t in 1:length(z_e) do
        z_e[t] ← z_e[t] + z_e_copy[t]

    /* second sublayer */
    z_e_copy ← copy(z_e)
    for each t in 1:length(z_e) do
        z_e[t] ← layer.layer_norm(z_e[t])
    z_e ← layer.feedforward(z_e)
    for each t in 1:length(z_e) do
        z_e[t] ← z_e[t] + z_e_copy[t]

for each t in 1:length(z_e) do
    z_e[t] ← encoder.final_layer_norm(z_e[t])

/* decoder */
z_d ← decoder.tokenizer(t_d)

for each t in 1:length(z_d) do
    z_d[t] ← decoder.embedding(z_d[t]) + decoder.positional_embedding(t)

for each l in 1:length(decoder.layers) do
        layer ← decoder.layers[l]

        /* first sublayer */
        z_d_copy ← copy(z_d)
        for each t in 1:length(z_d) do
            z_d[t] ← layer.layer_norm(z_d[t])
        z_d ← layer.masked_multihead_attention(z_d, z_d, z_d)
        for each t in 1:length(z_d) do
            z_d[t] ← z_d[t] + z_d_copy[t]

        /* second sublayer */
        z_d_copy ← copy(z_d)
        for each t in 1:length(z_d) do
            z_d[t] ← layer.layer_norm(z_d[t])
        z_d ← layer.multihead_attention(z_d, z_e, z_e) 
       for each t in 1:length(z_d) do
           z_d[t] ← z_d[t] + z_d_copy[t]

        /* third sublayer */
        z_d_copy ← copy(z_d)
        for each t in 1:length(z_d) do
            z_d[t] ← layer.layer_norm(z_d[t])
        z_d ← layer.feedforward(z_d)
        for each t in 1:length(z_d) do
            z_d[t] ← z_d[t] + z_d_copy[t]

z_d ← decoder.final_layer_norm(z_d)

output_distributions ← []
for each t in 1:length(z_d) do
    output_distributions.append(decoder.unembed(z_d[t]))

return output_distributions
Terminologyedit

The transformer architecture, being modular, allows variations. Several common variations are described here.[53]

An "encoder-only" transformer applies the encoder to map an input text into a sequence of vectors that represent the input text. This is usually used for text embedding and representation learning for downstream applications. BERT is encoder-only. They are less often used currently, as they were found to be not significantly better than training an encoder–decoder transformer, then taking just the encoder.[59] They are also referred to as "all-to-all" or "BERT-like".

A "decoder-only" transformer is not literally decoder-only, since without an encoder, the cross-attention mechanism has nothing to attend to. Thus, the decoder layers in a decoder-only transformer is composed of just two sublayers: the causally masked self-attention, and the feedforward network. This is usually used for text generation and instruction following. The models in the GPT series and Chinchilla series are decoder-only. They are also referred to as "autoregressive" or "causal".

An "encoder–decoder" transformer is generally the same as the original transformer, with 2 sublayers per encoder layer and 3 sublayers per decoder layer, etc. They might have minor architectural improvements, such as alternative activation functions, changing the location of normalization, etc. This is also usually used for text generation and instruction following. The models in the T5 series are encoder–decoder.[53]

A "prefixLM" (prefix language model) is a decoder-only architecture, but with prefix masking, which is different from causal masking. Specifically, it has mask of the form[53]: Figure 3 
𝑀
prefixLM
=
[
0
	
−
∞


0
	
𝑀
causal
]
where the first columns correspond to the "prefix", and the subsequent columns correspond to the autoregressively generated text based on the prefix. They resemble encoder–decoder models, but has less "sparsity". Such models are rarely used, though they are cited as theoretical possibilities and benchmarked comparisons.[59]

There are also mixed seq2seq models. For example, in 2020, Google Translate replaced the previous RNN-encoder–RNN-decoder model with a transformer-encoder–RNN-decoder model, as transformer-based decoders did not appear to significantly increase quality unlike the encoder, while the RNN decoder was much faster.[40]

Subsequent workedit
Alternative activation functionsedit

The original transformer uses ReLU activation function. Other activation functions were developed. The Llama series and PaLM used SwiGLU;[68] both GPT-1 and BERT[38] used GELU.[69]

Alternative activation functions are often used in combination with Gated Linear Units in the feedforward module.[68]

Alternative normalizationsedit

The normalization used in the transformer can be different from LayerNorm. One example is RMSNorm[70] which is used in the Llama series. Other examples include ScaleNorm[71] and FixNorm.[71]

Alternative positional encodingsedit

Transformers may use other positional encoding methods than sinusoidal.[72]

The original transformer paper reported using a learned positional encoding,[73] but finding it not superior to the sinusoidal one.[1] Later,[74] found that causal masking itself provides enough signal to a transformer decoder that it can learn to implicitly perform absolute positional encoding without the positional encoding module.

RoPEedit

RoPE (rotary positional embedding),[75] is best explained by considering a list of 2-dimensional vectors 
[
(
𝑥
1
(
1
)
,
𝑥
1
(
2
)
)
,
(
𝑥
2
(
1
)
,
𝑥
2
(
2
)
)
,
(
𝑥
3
(
1
)
,
𝑥
3
(
2
)
)
,
.
.
.
]
. Now pick some angle 
𝜃
. Then RoPE encoding is
RoPE
(
𝑥
𝑚
(
1
)
,
𝑥
𝑚
(
2
)
,
𝑚
)
=
(
cos
⁡
𝑚
𝜃
	
−
sin
⁡
𝑚
𝜃


sin
⁡
𝑚
𝜃
	
cos
⁡
𝑚
𝜃
)
(
𝑥
𝑚
(
1
)


𝑥
𝑚
(
2
)
)
=
(
𝑥
𝑚
(
1
)
cos
⁡
𝑚
𝜃
−
𝑥
𝑚
(
2
)
sin
⁡
𝑚
𝜃


𝑥
𝑚
(
2
)
cos
⁡
𝑚
𝜃
+
𝑥
𝑚
(
1
)
sin
⁡
𝑚
𝜃
)
Equivalently, if we write the 2-dimensional vectors as complex numbers 
𝑧
𝑚
:=
𝑥
𝑚
(
1
)
+
𝑖
𝑥
𝑚
(
2
)
, then RoPE encoding is just multiplication by an angle:
RoPE
(
𝑧
𝑚
,
𝑚
)
=
𝑒
𝑖
𝑚
𝜃
𝑧
𝑚
For a list of 
2
𝑛
-dimensional vectors, a RoPE encoder is defined by a sequence of angles 
𝜃
(
1
)
,
.
.
.
,
𝜃
(
𝑛
)
. Then the RoPE encoding is applied to each pair of coordinates.

The benefit of RoPE is that the dot-product between two vectors depends on their relative location only:
RoPE
(
𝑥
,
𝑚
)
𝑇
RoPE
(
𝑦
,
𝑛
)
=
RoPE
(
𝑥
,
𝑚
+
𝑘
)
𝑇
RoPE
(
𝑦
,
𝑛
+
𝑘
)
for any integer 
𝑘
.

ALiBiedit

ALiBi (Attention with Linear Biases)[76] is not a replacement for the positional encoder on the original transformer. Instead, it is an additional positional encoder that is directly plugged into the attention mechanism. Specifically, the ALiBi attention mechanism is
Attention
(
𝑄
,
𝐾
,
𝑉
)
=
softmax
(
𝑄
𝐾
T
𝑑
𝑘
+
𝑠
𝐵
)
𝑉
Here, 
𝑠
 is a real number ("scalar"), and 
𝐵
 is the linear bias matrix defined by
𝐵
=
(
0
	
1
	
2
	
3
	
⋯


−
1
	
0
	
1
	
2
	
⋯


−
2
	
−
1
	
0
	
1
	
⋯


−
3
	
−
2
	
−
1
	
0
	
⋯


⋮
	
⋮
	
⋮
	
⋮
	
⋱
)
in other words, 
𝐵
𝑖
,
𝑗
=
𝑗
−
𝑖
. The idea being that the linear bias matrix is a softened mask. Just as 
0
 represent full attention paid, and 
−
∞
 represents no attention paid, the linear bias matrix increases attention paid in one direction and decreases attention paid in the other direction.

ALiBi allows pretraining on short context windows, then fine-tuning on longer context windows. Since it is directly plugged into the attention mechanism, it can be combined with any positional encoder that is plugged into the "bottom" of the entire network (which is where the sinusoidal encoder on the original transformer, as well as RoPE and many others, are located).

Relative Position Encodingsedit

Relative Position Encodings[77] is similar to ALiBi, but more generic:
Attention
(
𝑄
,
𝐾
,
𝑉
)
=
softmax
(
𝑄
𝐾
T
𝑑
𝑘
+
𝐵
)
𝑉
where 
𝐵
 is a Toeplitz matrix, that is, 
𝐵
𝑖
,
𝑗
=
𝐵
𝑖
′
,
𝑗
′
 whenever 
𝑖
−
𝑗
=
𝑖
′
−
𝑗
′
. This is contrasted with the original sinusoidal positional encoding, which is an "absolute positional encoding".[78]

Efficient implementationedit

The transformer model has been implemented in standard deep learning frameworks such as TensorFlow and PyTorch. Transformers is a library produced by Hugging Face that supplies transformer-based architectures and pretrained models.[12]

KV cachingedit

When an autoregressive transformer is used for inference, such as generating text, the query vector is different at each step, but the already-computed key and value vectors are always the same. The KV caching method saves the computed key and value vectors at each attention block, so that they are not recomputed at each new token. PagedAttention applies memory paging to KV caching.[79][80][81]

If a transformer is used with a baked-in prompt, such as ["You are a customer support agent..."], then the key and value vectors can be computed for the prompt, and saved on disk. The saving in compute is significant when the model is used for many short real-time interactions, such as in online chatbots.

In general, when a user uses an autoregressive transformer to generate a continuation to a sequence of tokens, the model would first perform a forward-pass on this sequence, whereby the KV caches over this sequence are computed. This is called prefilling. Hyperscalers serving large Transformer models may use disaggregated inference, wherein prefilling and decoding are performed on separately specialized hardware.[82]

FlashAttentionedit

FlashAttention[83] is an algorithm that implements the transformer attention mechanism efficiently on a GPU. It is a communication-avoiding algorithm that performs matrix multiplications in blocks, such that each block fits within the cache of a GPU, and by careful management of the blocks it minimizes data copying between GPU caches (as data movement is slow).

The FlashAttention method is a communication-avoiding algorithm that fuses these operations into a single loop, increasing the arithmetic intensity. It is an online algorithm that computes the following quantities:[84][85]
𝑧
𝑖
	
=
𝑞
𝑇
𝑘
𝑖
	

𝑚
𝑖
	
=
max
(
𝑧
1
,
…
,
𝑧
𝑖
)
	
=
	
max
(
𝑚
𝑖
−
1
,
𝑧
𝑖
)


ℓ
𝑖
	
=
𝑒
𝑧
1
−
𝑚
𝑖
+
⋯
+
𝑒
𝑧
𝑖
−
𝑚
𝑖
	
=
	
𝑒
𝑚
𝑖
−
1
−
𝑚
𝑖
ℓ
𝑖
−
1
+
𝑒
𝑧
𝑖
−
𝑚
𝑖


𝑜
𝑖
	
=
𝑒
𝑧
1
−
𝑚
𝑖
𝑣
1
+
⋯
+
𝑒
𝑧
𝑖
−
𝑚
𝑖
𝑣
𝑖
	
=
	
𝑒
𝑚
𝑖
−
1
−
𝑚
𝑖
𝑜
𝑖
−
1
+
𝑒
𝑧
𝑖
−
𝑚
𝑖
𝑣
𝑖
and returns 
𝑜
𝑁
/
ℓ
𝑁
. In practice, FlashAttention operates over multiple queries and keys per loop iteration, in a similar way as blocked matrix multiplication. If backpropagation is needed, then the output vectors and the intermediate arrays 
[
𝑚
1
,
…
,
𝑚
𝑁
]
,
[
ℓ
1
,
…
,
ℓ
𝑁
]
 are cached, and during the backward pass, attention matrices are rematerialized from these, making it a form of gradient checkpointing.


An improved version, FlashAttention-2,[86][87][88] was developed to cater to the rising demand for language models capable of handling longer context lengths. It offers enhancements in work partitioning and parallelism, enabling it to achieve up to 230 TFLOPs/s on A100 GPUs (FP16/BF16), a 2x speed increase over the original FlashAttention.

Key advancements in FlashAttention-2 include the reduction of non-matmul FLOPs, improved parallelism over the sequence length dimension, better work partitioning between GPU warps, and added support for head dimensions up to 256 and multi-query attention (MQA) and grouped-query attention (GQA).[89]

Benchmarks revealed FlashAttention-2 to be up to 2x faster than FlashAttention and up to 9x faster than a standard attention implementation in PyTorch. Future developments include optimization for new hardware like H100 GPUs and new data types like FP8.

FlashAttention-4 focuses on pipelining to increase instruction throughput, and was developed to perform particularly well on Blackwell GPUs.[90]

Multi-Query Attentionedit

Comparison between several different forms of attention mechanism and the amount of KV caching necessary for each

Multi-Query Attention changes the Multihead Attention mechanism.[91] Whereas normally,

MultiheadAttention
(
𝑄
,
𝐾
,
𝑉
)
=
Concat
𝑖
∈
[
𝑛
heads
]
(
Attention
(
𝑋
𝑊
𝑖
𝑄
,
𝑋
𝑊
𝑖
𝐾
,
𝑋
𝑊
𝑖
𝑉
)
)
𝑊
𝑂
with Multi-Query Attention, there is just one 
𝑊
𝐾
,
𝑊
𝑉
, thus:

MultiQueryAttention
(
𝑄
,
𝐾
,
𝑉
)
=
Concat
𝑖
∈
[
𝑛
heads
]
(
Attention
(
𝑋
𝑊
𝑖
𝑄
,
𝑋
𝑊
𝐾
,
𝑋
𝑊
𝑉
)
)
𝑊
𝑂

This has a neutral effect on model quality and training speed, but increases inference speed.

More generally, grouped-query attention (GQA) partitions attention heads into groups, each of which shares the key-value pair. MQA is GQA with one group, while standard Multihead Attention is GQA with the maximal number of groups.[92]

The architecture of V2, showing both MLA and a variant of mixture of experts[93]: Figure 2 

Multihead Latent Attention (MLA) is a low-rank approximation to standard MHA. Specifically, each hidden vector, before entering the attention mechanism, is first projected to two low-dimensional spaces ("latent space"), one for query and one for key-value (KV vector). This design minimizes the KV cache, as only the low-dimensional KV vector needs to be cached.[93]

Speculative decodingedit
Main article: Speculative decoding

Speculative decoding[94][95] is a method to accelerate token decoding. Similarly to speculative execution in CPUs, future tokens are computed quickly, then verified. If the quickly computed tokens are incorrect, they are discarded and computed slowly.

The key factor in speculative decoding is that a transformer decoder can verify faster than it can decode, in the following sense.

Suppose we have two transformer models like GPT-3 and GPT-3-small, both with a context window size of 512. To generate an entire context window autoregressively with greedy decoding with GPT-3, it must be run for 512 times, each time generating a token 
𝑥
1
,
𝑥
2
,
.
.
.
,
𝑥
512
, taking time 
512
𝑇
GPT-3
. However, if we had some educated guess for the values of these tokens, we could verify all of them in parallel, in one run of the model, by checking that each 
𝑥
𝑡
 is indeed the token with the largest log-likelihood in the 
𝑡
-th output.

In speculative decoding, a smaller model or some other simple heuristic is used to generate a few speculative tokens that are subsequently verified by the larger model. For example, suppose we use GPT-3-small to generate four speculative tokens: 
𝑥
~
1
,
𝑥
~
2
,
𝑥
~
3
,
𝑥
~
4
. This only takes 
4
𝑇
GPT-3-small
. These tokens are then run through the larger GPT-3 in one go. Suppose that 
𝑥
~
1
 and 
𝑥
~
2
 are verified by GPT-3 as what it would have picked, then those are kept, but 
𝑥
~
3
 is not, so 
𝑥
~
3
,
𝑥
~
4
 are discarded, and GPT-3 is run on those. This would take 
4
𝑇
GPT-3-small
+
3
𝑇
GPT-3
, which might be shorter than 
4
𝑇
GPT-3
.

For non-greedy decoding, similar ideas apply, except the speculative tokens are accepted or rejected stochastically, in a way that guarantees the final output distribution is the same as if speculative decoding was not used.[94][96]

Multi-token prediction

In Multi-Token Prediction, a single forward pass creates a final embedding vector, which then is un-embedded into a token probability. However, that vector can then be further processed by another transformer block to predict the next token, and so on for arbitrarily many steps into the future. This trades off accuracy for speed, since each new token costs just one more transformer block, rather than the entire stack.[97][98]

Sub-quadratic transformersedit

Training transformer-based architectures can be expensive, especially for long inputs.[99] Many methods have been developed to attempt to address the issue. In the image domain, Swin transformer is an efficient architecture that performs attention inside shifting windows.[100] In the audio domain, SepTr decouples the attention in time and frequency domains.[101] Long Range Arena (2020)[102] is a standard benchmark for comparing the behavior of transformer architectures over long inputs.

Alternative attention graphsedit

The standard attention graph is either all-to-all or causal, both of which scales as 
𝑂
(
𝑁
2
)
 where 
𝑁
 is the number of tokens in a sequence.

Reformer (2020)[99][103] reduces the computational load from 
𝑂
(
𝑁
2
)
 to 
𝑂
(
𝑁
ln
⁡
𝑁
)
 by using locality-sensitive hashing and reversible layers.[104]

Sparse attention[105] uses attention graphs that grows slower than 
𝑂
(
𝑁
2
)
. For example, BigBird (2020)[106] uses random small-world networks which grows as 
𝑂
(
𝑁
)
.

Ordinary transformers require a memory size that is quadratic in the size of the context window. Attention-free transformers[107] reduce this to a linear dependence while still retaining the advantages of a transformer by linking the key to the value.

Random Feature Attentionedit

Random Feature Attention (2021)[108] uses Fourier random features:
𝜑
(
𝑥
)
=
1
𝐷
[
cos
⁡
⟨
𝑤
1
,
𝑥
⟩
,
sin
⁡
⟨
𝑤
1
,
𝑥
⟩
,
⋯
cos
⁡
⟨
𝑤
𝐷
,
𝑥
⟩
,
sin
⁡
⟨
𝑤
𝐷
,
𝑥
⟩
]
𝑇
where 
𝑤
1
,
.
.
.
,
𝑤
𝐷
 are independent samples from the normal distribution 
𝑁
(
0
,
𝜎
2
𝐼
)
. This choice of parameters satisfy 
𝐸
[
⟨
𝜑
(
𝑥
)
,
𝜑
(
𝑦
)
⟩
]
=
𝑒
−
‖
𝑥
−
𝑦
‖
2
2
𝜎
2
, or
𝑒
⟨
𝑥
,
𝑦
⟩
/
𝜎
2
=
𝐸
[
⟨
𝑒
‖
𝑥
‖
2
/
2
𝜎
2
𝜑
(
𝑥
)
,
𝑒
‖
𝑦
‖
2
/
2
𝜎
2
𝜑
(
𝑦
)
⟩
]
≈
⟨
𝑒
‖
𝑥
‖
2
/
2
𝜎
2
𝜑
(
𝑥
)
,
𝑒
‖
𝑦
‖
2
/
2
𝜎
2
𝜑
(
𝑦
)
⟩
Consequently, the one-headed attention, with one query, can be written as
Attention
(
𝑞
,
𝐾
,
𝑉
)
=
softmax
(
𝑞
𝐾
T
𝑑
𝑘
)
𝑉
≈
𝜑
(
𝑞
)
𝑇
∑
𝑖
𝑒
‖
𝑘
𝑖
‖
2
/
2
𝜎
2
𝜑
(
𝑘
𝑖
)
𝑣
𝑖
𝑇
𝜑
(
𝑞
)
𝑇
∑
𝑖
𝑒
‖
𝑘
𝑖
‖
2
/
2
𝜎
2
𝜑
(
𝑘
𝑖
)
where 
𝜎
=
𝑑
𝐾
1
/
4
. Similarly for multiple queries, and for multihead attention.

This approximation can be computed in linear time, as we can compute the matrix 
𝜑
(
𝑘
𝑖
)
𝑣
𝑖
𝑇
 first, then multiply it with the query. In essence, we have managed to obtain a more precise version of
Attention
(
𝑄
,
𝐾
,
𝑉
)
=
softmax
(
𝑄
𝐾
T
𝑑
𝑘
)
𝑉
≈
𝑄
(
𝐾
𝑇
𝑉
/
𝑑
𝑘
)
Performer (2022)[109] uses the same Random Feature Attention, but 
𝑤
1
,
.
.
.
,
𝑤
𝐷
 are first independently sampled from the normal distribution 
𝑁
(
0
,
𝜎
2
𝐼
)
, then they are Gram–Schmidt processed.

Multimodalityedit

Transformers can also be used/adapted for modalities (input or output) beyond just text, usually by finding a way to "tokenize" the modality.

Multimodal models can either be trained from scratch, or by finetuning. A 2022 study found that transformers pretrained only on natural language can be finetuned on only 0.03% of parameters and become competitive with LSTMs on a variety of logical and visual tasks, demonstrating transfer learning.[110] The LLaVA was a vision-language model composed of a language model (Vicuna-13B)[111] and a vision model (ViT-L/14), connected by a linear layer. Only the linear layer is finetuned.[112]

Vision transformers[47] adapt the transformer to computer vision by breaking down input images as a series of patches, turning them into vectors, and treating them like embedding vector of tokens in a standard transformer.

Conformer[48] and later Whisper[113] follow the same pattern for speech recognition, first turning the speech signal into a spectrogram, which is then treated like an image, i.e. broken down into a series of patches, turned into vectors and treated like embedding vector of tokens in a standard transformer.

Perceivers[114][115] are a variant of transformers designed for multimodality.

For image generation, notable architectures are DALL-E 1 (2021), Parti (2022),[116] Phenaki (2023),[117] and Muse (2023).[118] Unlike later models, DALL-E is not a diffusion model. Instead, it uses a decoder-only transformer that autoregressively generates a text, followed by the token representation of an image, which is then converted by a variational autoencoder to an image.[119] Parti is an encoder–decoder transformer, where the encoder processes a text prompt, and the decoder generates a token representation of an image.[120] Muse is an encoder-only transformer that is trained to predict masked image tokens from unmasked image tokens. During generation, all input tokens are masked, and the highest-confidence predictions are included for the next iteration, until all tokens are predicted.[118] Phenaki is a text-to-video model. It is a bidirectional masked transformer conditioned on pre-computed text tokens. The generated tokens are then decoded to a video.[117]

Applicationsedit

The transformer has had great success in natural language processing (NLP). Many large language models such as GPT-2, GPT-3, GPT-4, Gemini, AlbertAGPT, Claude, BERT, Grok, XLNet, RoBERTa and ChatGPT demonstrate the ability of transformers to perform a wide variety of NLP-related subtasks and their related real-world applications, including:

machine translation
time series prediction
document summarization
document generation
named entity recognition (NER)[121]
writing computer code based on requirements expressed in natural language.
speech-to-text

Beyond traditional NLP, the transformer architecture has had success in other applications, such as:

biological sequence analysis
video understanding
protein folding (such as AlphaFold)
evaluating chess board positions. Using static evaluation alone (that is, with no Minimax search) transformer achieved an Elo of 2895, putting it at grandmaster level.[11]
service function chain embedding[122]
See alsoedit
seq2seq – Family of machine learning approaches
Circuit (neural network) – Interpretable computational sub-graphs within artificial neural networks
Perceiver – Variant of Transformer designed for multimodal data
Vision transformer – Machine learning model for vision processing
Large language model – Type of machine learning model
BERT (language model) – Series of language models developed by Google AI
Generative pre-trained transformer – Type of large language model
T5 (language model) – Series of large language models developed by Google AI
Notesedit
 Gated recurrent units (2014) further reduced its complexity.
 Some architectures, such as RWKV (Receptance Weighted Key Value) or state space models, avoid the issue.
Referencesedit
 Vaswani, Ashish; Shazeer, Noam; Parmar, Niki; Uszkoreit, Jakob; Jones, Llion; Gomez, Aidan N; Kaiser, Łukasz; Polosukhin, Illia (2017). "Attention is All You Need" (PDF). 31st Conference on Neural Information Processing Systems (NIPS 2017), 4-9 December 2017, Long Beach, CA, USA. Vol. 30. Curran Associates, Inc. arXiv:1706.03762. ISBN 978-1-5108-6096-4. Archived from the original (PDF) on 2024-02-21. Retrieved 2023-10-31.
 Hochreiter, Sepp; Schmidhuber, Jürgen (November 1997). "Long Short-Term Memory". Neural Computation. 9 (8): 1735–1780. doi:10.1162/neco.1997.9.8.1735. PMID 9377276.
 "Better Language Models and Their Implications". OpenAI. 2019-02-14. Archived from the original on 2020-12-19. Retrieved 2019-08-25.
 Raffel, Colin; Shazeer, Noam; Roberts, Adam; Lee, Katherine; Narang, Sharan; Matena, Michael; Zhou, Yanqi; Li, Wei; Liu, Peter J. (2019-10-23). "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer". arXiv:1910.10683 [cs.LG].
 Bahdanau; Cho, Kyunghyun; Bengio, Yoshua (September 1, 2014). "Neural Machine Translation by Jointly Learning to Align and Translate". arXiv:1409.0473 [cs.CL].
 Luong, Minh-Thang; Pham, Hieu; Manning, Christopher D. (August 17, 2015). "Effective Approaches to Attention-based Neural Machine Translation". arXiv:1508.04025 [cs.CL].
 Chen, Lili; Lu, Kevin; Rajeswaran, Aravind; Lee, Kimin; Grover, Aditya; Laskin, Michael; Abbeel, Pieter; Srinivas, Aravind; Mordatch, Igor (2021-06-24). "Decision Transformer: Reinforcement Learning via Sequence Modeling". arXiv:2106.01345 [cs.LG].
 Parisotto, Emilio; Song, Francis; Rae, Jack; Pascanu, Razvan; Gulcehre, Caglar; Jayakumar, Siddhant; Jaderberg, Max; Kaufman, Raphaël Lopez; Clark, Aidan; Noury, Seb; Botvinick, Matthew; Heess, Nicolas; Hadsell, Raia (2020-11-21). "Stabilizing Transformers for Reinforcement Learning". Proceedings of the 37th International Conference on Machine Learning. PMLR: 7487–7498. Archived from the original on 2024-08-09. Retrieved 2024-08-09.
 Radford, Alec; Jong Wook Kim; Xu, Tao; Brockman, Greg; McLeavey, Christine; Sutskever, Ilya (2022). "Robust Speech Recognition via Large-Scale Weak Supervision". arXiv:2212.04356 [eess.AS].
 Monastirsky, Maxim; Azulay, Osher; Sintov, Avishai (February 2023). "Learning to Throw With a Handful of Samples Using Decision Transformers". IEEE Robotics and Automation Letters. 8 (2): 576–583. Bibcode:2023IRAL....8..576M. doi:10.1109/LRA.2022.3229266.
 Ruoss, Anian; Delétang, Grégoire; Medapati, Sourabh; Grau-Moya, Jordi; Wenliang, Li; Catt, Elliot; Reid, John; Genewein, Tim (2024-02-07). "Grandmaster-Level Chess Without Search". arXiv:2402.04494v1 [cs.LG].
 Wolf, Thomas; Debut, Lysandre; Sanh, Victor; Chaumond, Julien; Delangue, Clement; Moi, Anthony; Cistac, Pierric; Rault, Tim; Louf, Remi; Funtowicz, Morgan; Davison, Joe; Shleifer, Sam; von Platen, Patrick; Ma, Clara; Jernite, Yacine; Plu, Julien; Xu, Canwen; Le Scao, Teven; Gugger, Sylvain; Drame, Mariama; Lhoest, Quentin; Rush, Alexander (2020). "Transformers: State-of-the-Art Natural Language Processing". Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System Demonstrations. pp. 38–45. doi:10.18653/v1/2020.emnlp-demos.6.
 "Open Sourcing BERT: State-of-the-Art Pre-training for Natural Language Processing". Google AI Blog. 2 November 2018. Archived from the original on 2021-01-13. Retrieved 2019-08-25.
 Feldman, J; Ballard, D (September 1982). "Connectionist models and their properties". Cognitive Science. 6 (3): 205–254. doi:10.1016/S0364-0213(82)80001-3.
 Rumelhart, David E.; McClelland, James L.; Hinton, Geoffrey E. (1986). Parallel Distributed Processing, Volume 1: Explorations in the Microstructure of Cognition: Foundations, Chapter 2 (PDF). Cambridge, Massachusetts: Bradford Books. ISBN 978-0-262-68053-0. OCLC 12837549. OL 21219798M. Archived (PDF) from the original on April 16, 2026.
 Giles, C. Lee; Maxwell, Tom (December 1987). "Learning, invariance, and generalization in high-order neural networks". Applied Optics. 26 (23): 4972–4978. doi:10.1364/AO.26.004972. PMID 20523475.
 Christoph von der Malsburg: The correlation theory of brain function. Internal Report 81-2, MPI Biophysical Chemistry, 1981. http://cogprints.org/1380/1/vdM_correlation.pdf Archived 2022-01-26 at the Wayback Machine See Reprint in Models of Neural Networks II, chapter 2, pages 95–119. Springer, Berlin, 1994.
 Feldman, Jerome A. (December 1982). "Dynamic connections in neural networks". Biological Cybernetics. 46 (1): 27–39. doi:10.1007/BF00335349. PMID 6307398.
 Hinton, Geoffrey E.; Plaut, David C. (1987). "Using Fast Weights to Deblur Old Memories". Proceedings of the Annual Meeting of the Cognitive Science Society. 9. Archived from the original on 2024-07-23. Retrieved 2024-07-23.
 Schmidhuber, Jürgen (January 1992). "Learning to Control Fast-Weight Memories: An Alternative to Dynamic Recurrent Networks". Neural Computation. 4 (1): 131–139. doi:10.1162/neco.1992.4.1.131.
 Katharopoulos, Angelos; Vyas, Apoorv; Pappas, Nikolaos; Fleuret, François (2020). "Transformers are RNNs: Fast autoregressive Transformers with linear attention". ICML 2020. PMLR. pp. 5156–5165.
 Schlag, Imanol; Irie, Kazuki; Schmidhuber, Jürgen (2021). "Linear Transformers Are Secretly Fast Weight Programmers". ICML 2021. Springer. pp. 9355–9366. Archived from the original on 2026-05-20. Retrieved 2026-05-20.
 Cho, Kyunghyun; van Merriënboer, Bart; Gulcehre, Caglar; Bahdanau, Dzmitry; Bougares, Fethi; Schwenk, Holger; Bengio, Yoshua (October 2014). "Learning Phrase Representations using RNN Encoder–Decoder for Statistical Machine Translation". In Moschitti, Alessandro; Pang, Bo; Daelemans, Walter (eds.). Proceedings of the 2014 Conference on Empirical Methods in Natural Language Processing (EMNLP). Doha, Qatar: Association for Computational Linguistics. pp. 1724–1734. arXiv:1406.1078. doi:10.3115/v1/D14-1179. Archived from the original on 2024-09-06. Retrieved 2024-08-09.
 Sutskever, Ilya; Vinyals, Oriol; Le, Quoc Viet (14 Dec 2014). "Sequence to sequence learning with neural networks". arXiv:1409.3215 [cs.CL]. [first version posted to arXiv on 10 Sep 2014]
 Chung, Junyoung; Gulcehre, Caglar; Cho, KyungHyun; Bengio, Yoshua (2014). "Empirical Evaluation of Gated Recurrent Neural Networks on Sequence Modeling". arXiv:1412.3555 [cs.NE].
 Gruber, Nicole; Jockisch, Alfred (30 June 2020). "Are GRU Cells More Specific and LSTM Cells More Sensitive in Motive Classification of Text?". Frontiers in Artificial Intelligence. 3 40. doi:10.3389/frai.2020.00040. PMC 7861254. PMID 33733157.
 Sutskever, Ilya; Vinyals, Oriol; Le, Quoc V (2014). "Sequence to Sequence Learning with Neural Networks". Advances in Neural Information Processing Systems. 27. Curran Associates, Inc. arXiv:1409.3215. Archived from the original on 2025-01-27. Retrieved 2024-07-23.
 Luong, Minh-Thang; Pham, Hieu; Manning, Christopher D. (2015). "Effective Approaches to Attention-based Neural Machine Translation". arXiv:1508.04025 [cs.CL].
 Wu, Yonghui; et al. (2016-09-01). "Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation". arXiv:1609.08144 [cs.CL].
 Lewis-Kraus, Gideon (2016-12-14). "The Great A.I. Awakening". The New York Times. Archived from the original on 24 May 2023. Retrieved 2023-06-22.
 Parikh, Ankur P.; Täckström, Oscar; Das, Dipanjan; Uszkoreit, Jakob (2016-09-25). "A Decomposable Attention Model for Natural Language Inference". arXiv:1606.01933 [cs.CL].
 Levy, Steven. "8 Google Employees Invented Modern AI. Here's the Inside Story". Wired. Archived from the original on 20 Mar 2024. Retrieved 2024-08-06.
 Cheng, Jianpeng; Dong, Li; Lapata, Mirella (November 2016). "Long Short-Term Memory-Networks for Machine Reading". In Su, Jian; Duh, Kevin; Carreras, Xavier (eds.). Proceedings of the 2016 Conference on Empirical Methods in Natural Language Processing. Austin, Texas: Association for Computational Linguistics. pp. 551–561. doi:10.18653/v1/D16-1053. Archived from the original on 2024-08-27. Retrieved 2024-08-27.
 Peng, Bo; Alcaide, Eric; Anthony, Quentin; Albalak, Alon; Arcadinho, Samuel; Biderman, Stella; Cao, Huanqi; Cheng, Xin; Chung, Michael (2023-12-10). "RWKV: Reinventing RNNs for the transformer Era". arXiv:2305.13048 [cs.CL].
 Marche, Stephen (2024-08-23). "Was Linguistic A.I. Created by Accident?". The New Yorker. Retrieved 2024-08-27.
 Vaswani, Ashish; Bengio, Samy; Brevdo, Eugene; Chollet, Francois; Gomez, Aidan; Gouws, Stephan; Jones, Llion; Kaiser, Łukasz; Kalchbrenner, Nal; Parmar, Niki; Sepassi, Ryan; Shazeer, Noam; Uszkoreit, Jakob (March 2018). Cherry, Colin; Neubig, Graham (eds.). "Tensor2Tensor for Neural Machine Translation". Proceedings of the 13th Conference of the Association for Machine Translation in the Americas (Volume 1: Research Track). Boston, MA: Association for Machine Translation in the Americas: 193–199. Archived from the original on 2026-04-29. Retrieved 2026-03-31.
 Kaiser, Łukasz (2017-06-19). "Accelerating Deep Learning Research with the Tensor2Tensor Library". Google Research Blog. Archived from the original on 2026-04-15. Retrieved 2026-03-31.
 Devlin, Jacob; Chang, Ming-Wei; Lee, Kenton; Toutanova, Kristina (11 October 2018). "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding". arXiv:1810.04805v2 [cs.CL].
 "Google: BERT now used on almost every English query". Search Engine Land. 2020-10-15. Archived from the original on 2022-05-06. Retrieved 2020-11-24.
 Caswell, Isaac; Liang, Bowen (June 8, 2020). "Recent Advances in Google Translate". Google Research. Archived from the original on 4 Jul 2024. Retrieved 2024-08-07.
 "Improving language understanding with unsupervised learning". openai.com. June 11, 2018. Archived from the original on 2023-03-18. Retrieved 2023-03-18.
 "finetune-transformer-lm". OpenAI. June 11, 2018. Archived from the original on 2023-05-19. Retrieved 2023-05-01.
 "The inside story of how ChatGPT was built from the people who made it". MIT Technology Review. Archived from the original on 2023-03-03. Retrieved 2024-08-06.
 "Introducing ChatGPT". OpenAI. 2022-11-30. Archived from the original on 2026-04-05. Retrieved 2026-05-16.
 Bommasani, Rishi; Hudson, Drew A.; Adeli, Ehsan; Altman, Russ; Arora, Simran; Arx, Sydney von; Bernstein, Michael S.; Bohg, Jeannette; Bosselut, Antoine (2022-07-12), On the Opportunities and Risks of Foundation Models, arXiv, doi:10.48550/arXiv.2108.07258, arXiv:2108.07258, retrieved 2026-09-23
 Kaiser, Lukasz; Gomez, Aidan N.; Shazeer, Noam; Vaswani, Ashish; Parmar, Niki; Jones, Llion; Uszkoreit, Jakob (2017-06-16). "One Model To Learn Them All". arXiv:1706.05137v1 [cs.LG].
 Dosovitskiy, Alexey; Beyer, Lucas; Kolesnikov, Alexander; Weissenborn, Dirk; Zhai, Xiaohua; Unterthiner, Thomas; Dehghani, Mostafa; Minderer, Matthias; Heigold, Georg; Gelly, Sylvain; Uszkoreit, Jakob (2021-06-03). "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale". arXiv:2010.11929 [cs.CV].
 Gulati, Anmol; Qin, James; Chiu, Chung-Cheng; Parmar, Niki; Zhang, Yu; Yu, Jiahui; Han, Wei; Wang, Shibo; Zhang, Zhengdong; Wu, Yonghui; Pang, Ruoming (2020). "Conformer: Convolution-augmented Transformer for Speech Recognition". arXiv:2005.08100 [eess.AS].
 Choromanski, Krzysztof; Likhosherstov, Valerii; Dohan, David; Song, Xingyou; Gane, Andreea; Sarlos, Tamas; Hawkins, Peter; Davis, Jared; Mohiuddin, Afroz (2022-11-19). "Rethinking Attention with Performers". arXiv:2009.14794 [cs.LG].
 Liu, Zhuang; Mao, Hanzi; Wu, Chao-Yuan; Feichtenhofer, Christoph; Darrell, Trevor; Xie, Saining (2022). A ConvNet for the 2020s. Conference on Computer Vision and Pattern Recognition (CVPR). pp. 11976–11986.
 Esser, Patrick; Kulal, Sumith; Blattmann, Andreas; Entezari, Rahim; Müller, Jonas; Saini, Harry; Levi, Yam; Lorenz, Dominik; Sauer, Axel (2024-03-05). "Scaling Rectified Flow Transformers for High-Resolution Image Synthesis". arXiv:2403.03206 [cs.CV].
 Xiong, Ruibin; Yang, Yunchang; He, Di; Zheng, Kai; Zheng, Shuxin; Xing, Chen; Zhang, Huishuai; Lan, Yanyan; Wang, Liwei; Liu, Tie-Yan (2020-06-29). "On Layer Normalization in the Transformer Architecture". arXiv:2002.04745 [cs.LG].
 Raffel, Colin; Shazeer, Noam; Roberts, Adam; Lee, Katherine; Narang, Sharan; Matena, Michael; Zhou, Yanqi; Li, Wei; Liu, Peter J. (2020). "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer". Journal of Machine Learning Research. 21 (140): 1–67. Archived from the original on 2026-04-10. Retrieved 2026-04-18.
 Raffel, Colin; Shazeer, Noam; Roberts, Adam; Lee, Katherine; Narang, Sharan; Matena, Michael; Zhou, Yanqi; Li, Wei; Liu, Peter J. (2019). "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer". arXiv:1910.10683 [cs.LG].
 "Verifying your browser | OpenReview". openreview.net. Retrieved 2026-09-24.
 "Verifying your browser | OpenReview". openreview.net. Retrieved 2026-09-24.
 "Masked language modeling". huggingface.co. Archived from the original on 2023-10-10. Retrieved 2023-10-05.
 "Causal language modeling". huggingface.co. Archived from the original on 2023-10-10. Retrieved 2023-10-05.
 Tay, Yi; Dehghani, Mostafa; Tran, Vinh Q.; Garcia, Xavier; Wei, Jason; Wang, Xuezhi; Chung, Hyung Won; Shakeri, Siamak; Bahri, Dara (2023-02-28). "UL2: Unifying Language Learning Paradigms". arXiv:2205.05131 [cs.CL].
 Press, Ofir; Wolf, Lior (2017-02-21). "Using the Output Embedding to Improve Language Models". arXiv:1608.05859 [cs.CL].
 Lintz, Nathan (2016-04-18). "Sequence Modeling with Neural Networks (Part 2): Attention Models". Indico. Archived from the original on 2020-10-21. Retrieved 2019-10-15.
 Alammar, Jay. "The Illustrated transformer". jalammar.github.io. Archived from the original on 2020-10-18. Retrieved 2019-10-15.
 Team, Keras. "Keras documentation: GPT2Backbone model". keras.io. Archived from the original on 2024-08-08. Retrieved 2024-08-08.
 Clark, Kevin; Khandelwal, Urvashi; Levy, Omer; Manning, Christopher D. (August 2019). "What Does BERT Look at? An Analysis of BERT's Attention". Proceedings of the 2019 ACL Workshop BlackboxNLP: Analyzing and Interpreting Neural Networks for NLP. Florence, Italy: Association for Computational Linguistics: 276–286. arXiv:1906.04341. doi:10.18653/v1/W19-4828. Archived from the original on 2020-10-21. Retrieved 2020-05-20.
 Yang, Zhilin; Dai, Zihang; Yang, Yiming; Carbonell, Jaime; Salakhutdinov, Russ R; Le, Quoc V (2019). "XLNet: Generalized Autoregressive Pretraining for Language Understanding". Advances in Neural Information Processing Systems. 32. Curran Associates, Inc. arXiv:1906.08237. Archived from the original on 2024-08-09. Retrieved 2024-08-09.
 Wang, Qiang; Li, Bei; Xiao, Tong; Zhu, Jingbo; Li, Changliang; Wong, Derek F.; Chao, Lidia S. (2019-06-04). "Learning Deep Transformer Models for Machine Translation". arXiv:1906.01787 [cs.CL].
 Phuong, Mary; Hutter, Marcus (2022-07-19). "Formal Algorithms for Transformers". arXiv:2207.09238 [cs.LG].
 Shazeer, Noam (2020-02-01). "GLU Variants Improve Transformer". arXiv:2002.05202 [cs.LG].
 Hendrycks, Dan; Gimpel, Kevin (2016-06-27). "Gaussian Error Linear Units (GELUs)". arXiv:1606.08415v5 [cs.LG].
 Zhang, Biao; Sennrich, Rico (2019). "Root Mean Square Layer Normalization". Advances in Neural Information Processing Systems. 32. Curran Associates, Inc. arXiv:1910.07467. Archived from the original on 2024-09-17. Retrieved 2024-08-09.
 Nguyen, Toan Q.; Salazar, Julian (2019-11-02). Niehues, Jan; Cattoni, Rolando; Stüker, Sebastian; Negri, Matteo; Turchi, Marco; Ha, Thanh-Le; Salesky, Elizabeth; Sanabria, Ramon; Barrault, Loic (eds.). "Transformers without Tears: Improving the Normalization of Self-Attention". Proceedings of the 16th International Conference on Spoken Language Translation. Hong Kong: Association for Computational Linguistics. arXiv:1910.05895. doi:10.5281/zenodo.3525484. Archived from the original on 2024-08-09. Retrieved 2024-08-09.
 Dufter, Philipp; Schmitt, Martin; Schütze, Hinrich (September 2022). "Position Information in Transformers: An Overview". Computational Linguistics. 48 (3): 733–763. arXiv:2102.11090. doi:10.1162/coli_a_00445.
 Gehring, Jonas; Auli, Michael; Grangier, David; Yarats, Denis; Dauphin, Yann N. (2017-07-17). "Convolutional Sequence to Sequence Learning". Proceedings of the 34th International Conference on Machine Learning. PMLR: 1243–1252. Archived from the original on 2024-08-09. Retrieved 2024-08-09.
 Haviv, Adi; Ram, Ori; Press, Ofir; Izsak, Peter; Levy, Omer (2022-12-05). "Transformer Language Models without Positional Encodings Still Learn Positional Information". arXiv:2203.16634 [cs.CL].
 Su, Jianlin; Lu, Yu; Pan, Shengfeng; Murtadha, Ahmed; Wen, Bo; Liu, Yunfeng (2021-04-01). "RoFormer: Enhanced Transformer with Rotary Position Embedding". arXiv:2104.09864 [cs.CL].
 Press, Ofir; Smith, Noah A.; Lewis, Mike (2021-08-01). "Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation". arXiv:2108.12409 [cs.CL].
 Shaw, Peter; Uszkoreit, Jakob; Vaswani, Ashish (2018). "Self-Attention with Relative Position Representations". arXiv:1803.02155 [cs.CL].
 Ke, Guolin; He, Di; Liu, Tie-Yan (2021-03-15). "Rethinking Positional Encoding in Language Pre-training". arXiv:2006.15595 [cs.CL].
 Kwon, Woosuk; Li, Zhuohan; Zhuang, Siyuan; Sheng, Ying; Zheng, Lianmin; Yu, Cody Hao; Gonzalez, Joseph; Zhang, Hao; Stoica, Ion (2023-10-23). "Efficient Memory Management for Large Language Model Serving with PagedAttention". Proceedings of the 29th Symposium on Operating Systems Principles. SOSP '23. New York, NY, USA: Association for Computing Machinery. pp. 611–626. arXiv:2309.06180. doi:10.1145/3600006.3613165. ISBN 979-8-4007-0229-7.
 "vllm-project/vllm". vLLM. 2024-06-20. Archived from the original on 2024-06-18. Retrieved 2024-06-20.
 Zhuohan Li, Woosuk Kwon; Zhuang, Siyuan; Sheng, Ying; Zheng, Lianmin; Yu, Cody; Gonzalez, Joey; Zhang, Hao; Stoica, Ion (2023-06-20). "vLLM: Easy, Fast, and Cheap LLM Serving with PagedAttention". vLLM Blog. Archived from the original on 2024-06-20. Retrieved 2024-06-20.
 Hu, Cunchen; Huang, Heyang; Xu, Liangliang; Chen, Xusheng; Xu, Jiang; Chen, Shuang; Feng, Hao; Wang, Chenxi; Wang, Sa (2024-01-20). "Inference without Interference: Disaggregate LLM Inference for Mixed Downstream Workloads". arXiv:2401.11181 [cs.DC].
 Dao, Tri; Ermon, Stefano; Fu, Dan; Ré, Christopher; Rudra, Atri (2022). "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness". Advances in Neural Information Processing Systems 35. pp. 16344–16359. doi:10.52202/068431-1189. ISBN 978-1-7138-7108-8.
 Milakov, Maxim; Gimelshein, Natalia (2018). "Online normalizer calculation for softmax". arXiv:1805.02867 [cs.PF].
 Dao, Tri; Fu, Dan; Ermon, Stefano; Rudra, Atri; Ré, Christopher (2022-12-06). "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness". Advances in Neural Information Processing Systems. 35: 16344–16359.
 "Stanford CRFM". crfm.stanford.edu. Archived from the original on 2023-07-18. Retrieved 2023-07-18.
 "FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning". Princeton NLP. 2023-06-17. Archived from the original on 2023-07-18. Retrieved 2023-07-18.
 "Introducing Together AI Chief Scientist Tri Dao, as he releases FlashAttention-2 to speed up model training and inference". TOGETHER. Archived from the original on 2023-07-17. Retrieved 2023-07-18.
 Ainslie, Joshua; Lee-Thorp, James; de Jong, Michiel; Zemlyanskiy, Yury; Lebrón, Federico; Sanghai, Sumit (2023-12-23). "GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints". arXiv:2305.13245 [cs.CL].
 "We reverse-engineered Flash Attention 4". Modal. Archived from the original on 2025-09-27. Retrieved 2025-09-26.
 Chowdhery, Aakanksha; Narang, Sharan; Devlin, Jacob; Bosma, Maarten; Mishra, Gaurav; Roberts, Adam; Barham, Paul; Chung, Hyung Won; Sutton, Charles; Gehrmann, Sebastian; Schuh, Parker; Shi, Kensen; Tsvyashchenko, Sasha; Maynez, Joshua; Rao, Abhishek (2022-04-01). "PaLM: Scaling Language Modeling with Pathways". arXiv:2204.02311 [cs.CL].
 Ainslie, Joshua; Lee-Thorp, James; de Jong, Michiel; Zemlyanskiy, Yury; Lebrón, Federico; Sanghai, Sumit (2023-12-23). "GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints". arXiv:2305.13245 [cs.CL].
 DeepSeek-AI; Liu, Aixin; Feng, Bei; Wang, Bin; Wang, Bingxuan; Liu, Bo; Zhao, Chenggang; Dengr, Chengqi; Ruan, Chong (19 June 2024). "DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model". arXiv:2405.04434 [cs.CL]..
 Leviathan, Yaniv; Kalman, Matan; Matias, Yossi (2023-05-18). "Fast Inference from Transformers via Speculative Decoding". arXiv:2211.17192 [cs.LG].
 Fu, Yao (2023-12-11). "Towards 100x Speedup: Full Stack Transformer Inference Optimization". yaofu.notion.site.
 Chen, Charlie; Borgeaud, Sebastian; Irving, Geoffrey; Lespiau, Jean-Baptiste; Sifre, Laurent; Jumper, John (2023-02-02). "Accelerating Large Language Model Decoding with Speculative Sampling". arXiv:2302.01318 [cs.CL].
 Gloeckle, Fabian; Badr Youbi Idrissi; Rozière, Baptiste; Lopez-Paz, David; Synnaeve, Gabriel (2024). "Better & Faster Large Language Models via Multi-token Prediction". arXiv:2404.19737 [cs.CL].
 DeepSeek-AI; et al. (2024). "DeepSeek-V3 Technical Report". arXiv:2412.19437 [cs.CL].
 Kitaev, Nikita; Kaiser, Łukasz; Levskaya, Anselm (2020). "Reformer: The Efficient Transformer". arXiv:2001.04451 [cs.LG].
 Liu, Ze; Lin, Yutong; Cao, Yue; Hu, Han; Wei, Yixuan; Zhang, Zheng; Lin, Stephen; Guo, Baining (2021). "Swin Transformer: Hierarchical Vision Transformer using Shifted Windows". 2021 IEEE/CVF International Conference on Computer Vision (ICCV). IEEE. pp. 9992–10002. arXiv:2103.14030. doi:10.1109/ICCV48922.2021.00986. ISBN 978-1-6654-2812-5.
 Ristea, Nicolaea Catalin; Ionescu, Radu Tudor; Khan, Fahad Shahbaz (2022-09-18). "SepTr: Separable Transformer for Audio Spectrogram Processing". Interspeech. ISCA: 4103–4107. arXiv:2203.09581. doi:10.21437/Interspeech.2022-249.
 Tay, Yi; Dehghani, Mostafa; Abnar, Samira; Shen, Yikang; Bahri, Dara; Pham, Philip; Rao, Jinfeng; Yang, Liu; Ruder, Sebastian; Metzler, Donald (2020-11-08). "Long Range Arena: A Benchmark for Efficient Transformers". arXiv:2011.04006 [cs.LG].
 "Reformer: The Efficient Transformer". Google AI Blog. 16 January 2020. Archived from the original on 2020-10-22. Retrieved 2020-10-22.
 Gomez, Aidan N; Ren, Mengye; Urtasun, Raquel; Grosse, Roger B (2017). "The Reversible Residual Network: Backpropagation Without Storing Activations". Advances in Neural Information Processing Systems. 30. Curran Associates, Inc. arXiv:1707.04585. Archived from the original on 2024-08-11. Retrieved 2024-08-11.
 Child, Rewon; Gray, Scott; Radford, Alec; Sutskever, Ilya (2019-04-23). "Generating Long Sequences with Sparse Transformers". arXiv:1904.10509 [cs.LG].
 "Constructing Transformers For Longer Sequences with Sparse Attention Methods". Google AI Blog. 25 March 2021. Archived from the original on 2021-09-18. Retrieved 2021-05-28.
 Zhai, Shuangfei; Talbott, Walter; Srivastava, Nitish; Huang, Chen; Goh, Hanlin; Zhang, Ruixiang; Susskind, Josh (2021-09-21). "An Attention Free Transformer". arXiv:2105.14103 [cs.LG].
 Peng, Hao; Pappas, Nikolaos; Yogatama, Dani; Schwartz, Roy; Smith, Noah A.; Kong, Lingpeng (2021-03-19). "Random Feature Attention". arXiv:2103.02143 [cs.CL].
 Choromanski, Krzysztof; Likhosherstov, Valerii; Dohan, David; Song, Xingyou; Gane, Andreea; Sarlos, Tamas; Hawkins, Peter; Davis, Jared; Belanger, David; Colwell, Lucy; Weller, Adrian (2020-09-30). "Masked Language Modeling for Proteins via Linearly Scalable Long-Context Transformers". arXiv:2006.03555 [cs.LG].
 Lu, Kevin; Grover, Aditya; Abbeel, Pieter; Mordatch, Igor (2022-06-28). "Frozen Pretrained Transformers as Universal Computation Engines". Proceedings of the AAAI Conference on Artificial Intelligence. 36 (7): 7628–7636. doi:10.1609/aaai.v36i7.20729. ISSN 2374-3468. Archived from the original on 2024-12-02. Retrieved 2024-08-11.
 "Vicuna: An Open-Source Chatbot Impressing GPT-4 with 90%* ChatGPT Quality | LMSYS Org". lmsys.org. 30 March 2023. Archived from the original on 2024-08-12. Retrieved 2024-08-11.
 Liu, Haotian; Li, Chunyuan; Wu, Qingyang; Lee, Yong Jae (2023-12-15). "Visual Instruction Tuning". Advances in Neural Information Processing Systems. Vol. 36. pp. 34892–34916. doi:10.52202/075280-1516. ISBN 978-1-7138-9911-2. Archived from the original on 2024-09-26. Retrieved 2024-08-11.
 Radford, Alec; Kim, Jong Wook; Xu, Tao; Brockman, Greg; McLeavey, Christine; Sutskever, Ilya (2022). "Robust Speech Recognition via Large-Scale Weak Supervision". arXiv:2212.04356 [eess.AS].
 Jaegle, Andrew; Gimeno, Felix; Brock, Andrew; Zisserman, Andrew; Vinyals, Oriol; Carreira, Joao (2021-06-22). "Perceiver: General Perception with Iterative Attention". arXiv:2103.03206 [cs.CV].
 Jaegle, Andrew; Borgeaud, Sebastian; Alayrac, Jean-Baptiste; Doersch, Carl; Ionescu, Catalin; Ding, David; Koppula, Skanda; Zoran, Daniel; Brock, Andrew; Shelhamer, Evan; Hénaff, Olivier (2021-08-02). "Perceiver IO: A General Architecture for Structured Inputs & Outputs". arXiv:2107.14795 [cs.LG].
 "Parti: Pathways Autoregressive Text-to-Image Model". sites.research.google. Archived from the original on 2024-08-10. Retrieved 2024-08-09.
 Villegas, Ruben; Babaeizadeh, Mohammad; Kindermans, Pieter-Jan; Moraldo, Hernan; Zhang, Han; Saffar, Mohammad Taghi; Castro, Santiago; Kunze, Julius; Erhan, Dumitru (2022-09-29). "Phenaki: Variable Length Video Generation from Open Domain Textual Descriptions". arXiv:2210.02399 [cs.CV].
 Chang, Huiwen; Zhang, Han; Barber, Jarred; Maschinot, A. J.; Lezama, Jose; Jiang, Lu; Yang, Ming-Hsuan; Murphy, Kevin; Freeman, William T. (2023-01-02). "Muse: Text-To-Image Generation via Masked Generative Transformers". arXiv:2301.00704 [cs.CV].
 Ramesh, Aditya; Pavlov, Mikhail; Goh, Gabriel; Gray, Scott; Voss, Chelsea; Radford, Alec; Chen, Mark; Sutskever, Ilya (2021-02-26). "Zero-Shot Text-to-Image Generation". arXiv:2102.12092 [cs.CV].
 Yu, Jiahui; Xu, Yuanzhong; Koh, Jing Yu; Luong, Thang; Baid, Gunjan; Wang, Zirui; Vasudevan, Vijay; Ku, Alexander; Yang, Yinfei (2022-06-21). "Scaling Autoregressive Models for Content-Rich Text-to-Image Generation". arXiv:2206.10789 [cs.CV].
 Kariampuzha, William; Alyea, Gioconda; Qu, Sue; Sanjak, Jaleal; Mathé, Ewy; Sid, Eric; Chatelaine, Haley; Yadaw, Arjun; Xu, Yanji; Zhu, Qian (2023). "Precision information extraction for rare disease epidemiology at scale". Journal of Translational Medicine. 21 (1): 157. doi:10.1186/s12967-023-04011-y. PMC 9972634. PMID 36855134.
 Hsu, Cyril Shih-Huan; Dalgkitsis, Anestis; Grosso, Paola; Papagianni, Chrysa (2026). "Transformer-Empowered Actor-Critic Reinforcement Learning for Sequence-Aware Service Function Chain Partitioning". IEEE Transactions on Network Science and Engineering. 13: 9247–9264. doi:10.1109/TNSE.2026.3689920. ISSN 2327-4697.
Further readingedit
Alexander Rush, The Annotated transformer Archived 2021-09-22 at the Wayback Machine, Harvard NLP group, 3 April 2018
Phuong, Mary; Hutter, Marcus (2022). "Formal Algorithms for Transformers". arXiv:2207.09238 [cs.LG].
Ferrando, Javier; Sarti, Gabriele; Bisazza, Arianna; Costa-jussà, Marta R. (2024-05-01). "A Primer on the Inner Workings of Transformer-based Language Models". arXiv:2405.00208 [cs.CL].
Leech, Gavin (2024-11-06). "Transformer++". argmin gravitas. Archived from the original on 2025-02-26. Retrieved 2025-05-08.
US patent 10452978, Noam M. Shazeer; Aidan Nicholas Gomez; Lukasz Mieczyslaw Kaiser; Jakob D. Uszkoreit; Llion Owen Jones; Niki J. Parmar; Illia Polosukhin; Ashish Teku Vaswani, "Attention-based sequence transduction neural networks", issued 2019-10-22, assigned to Google LLC
Raschka, Sebastian (2026-03-11). "The Big LLM Architecture Comparison: From DeepSeek V3 to GLM-5: A Look At Modern LLM Architecture Design". Sebastian Raschka’s AI Magazine. Archived from the original on 2026-03-21. Retrieved 2026-03-25.
vte
Google AI


GoogleGoogle BrainGoogle DeepMind

Computer
programs	
AlphaGo	
Versions	
AlphaGo (2015)Master (2016)AlphaGo Zero (2017)AlphaZero (2017)MuZero (2019)

Competitions	
Fan Hui (2015)Lee Sedol (2016)Ke Jie (2017)

In popular culture	
AlphaGo (2017)

Other	
AlphaFold (2018)AlphaStar (2019)AlphaTensor (2022)AlphaDev (2023)FunSearch (2023)AlphaGeometry (2024)AlphaProof (2024)AlphaEvolve (2025)AlphaGenome (2025)

Machine
learning	
Neural networks	
Inception (2014)WaveNet (2016)MobileNet (2017)Transformer (2017)EfficientNet (2019)Gato (2022)

Other	
Quantum Artificial Intelligence LabTensorFlowTensor Processing Unit

Generative
AI	
Chatbots	
Assistant (2016)Sparrow (2022)Gemini (2023)Nano Banana (2025)

Models	
BERT (2018)XLNet (2019)T5 (2019)LaMDA (2021)Chinchilla (2022)PaLM (2022)Imagen (2023)Gemini (2023)VideoPoet (2024)Gemma (2024)Genie (2024)Veo (2024)

Other	
DreamBooth (2022)NotebookLM (2023)Vids (2024)Gemini Robotics (2025)Antigravity (2025)

See also	
"Attention Is All You Need"Future of Go SummitGenerative pre-trained transformerGoogle LabsGoogle Workspace


 Category Commons
vte
Artificial intelligence (AI)


History timelineGlossaryLists AlgorithmsCompaniesInstitutionsProjectsSoftware Open-sourceProprietary

Concepts	
Automated reasoningAutomated planningConstraint satisfactionKnowledge representationParameter HyperparameterLoss functionsRegression Bias–variance tradeoffDouble descentOverfittingClusteringGradient descent SGDQuasi-Newton methodConjugate gradient methodBackpropagationAttentionConvolutionNormalization BatchnormActivation SoftmaxSigmoidRectifierGatingWeight initializationRegularizationDatasets AugmentationPrompt engineeringReinforcement learning Q-learningSARSAImitationPolicy gradientDiffusionLatent diffusion modelAutoregressionAdversaryRAGUncanny valleyLLM post-trainingRLHFSelf-supervised learningReflectionRecursive self-improvementHallucinationWord embeddingVibe codingBlended AIOpen-source AISovereign AISymbolic AINeuro-symbolic AISituated approachActor-critic algorithm

Applications	
Automated theorem provingGeneral game playingMachine learning In-context learningArtificial neural network Deep learningLanguage model LargeNMTReasoningModel Context ProtocolIntelligent agent AI agentArtificial human companionHumanity's Last ExamLethal autonomous weapons (LAWs)Generative AIWeak AIHypothetical Artificial general intelligence (AGI)Artificial superintelligence (ASI)Agent2Agent protocolPhysical AI

Implementations	
Audio–visual	
AlexNetWaveNetHuman image synthesisHWROCRComputer visionSpeech synthesis 15.aiElevenLabsSpeech recognition WhisperFacial recognitionAlphaFoldText-to-image models AuroraDALL-EFireflyFluxGPT ImageIdeogramImagenMidjourneyRecraftStable DiffusionText-to-video models Dream MachineRunway GenHailuo AIKlingSoraSeedanceVeoMusic generation RiffusionSunoUdioWorld models GenieOasis

Text	
List of large language modelsProject DebaterIBM Watson IBM Watsonx

Decisional	
AlphaGoAlphaZeroOpenAI FiveSelf-driving carMuZeroAction selection AutoGPTRobot control

Reasoning systems	
Deductive classifiersExpert systemsInference enginesKnowledge-based systemsLogic programsProcedural reasoning systemsSemantic reasonersRule-based systems

Cognitive architectures	
ACT-RSoarCLARIONLIDAOpenCog

Knowledge bases	
ConceptNetWikidataDBpediaYAGO

People	
Alan TuringWarren Sturgis McCullochWalter PittsJohn von NeumannChristopher D. ManningClaude ShannonShun'ichi AmariKunihiko FukushimaTakeo KanadeMarvin MinskyJohn McCarthyNathaniel RochesterAllen NewellCliff ShawHerbert A. SimonOliver SelfridgeFrank RosenblattBernard WidrowJoseph WeizenbaumSeymour PapertSeppo LinnainmaaPaul WerbosGeoffrey HintonJohn HopfieldJürgen SchmidhuberYann LeCunYoshua BengioLotfi A. ZadehStephen GrossbergAlex GravesJames GoodnightAndrew NgFei-Fei LiAlex KrizhevskyIlya SutskeverOriol VinyalsQuoc V. LeIan GoodfellowDemis HassabisDavid SilverAndrej KarpathyAshish VaswaniNoam ShazeerAidan GomezJohn SchulmanMustafa SuleymanJan LeikeDaniel KokotajloFrançois Chollet

Neural network
architectures	
Neural Turing machineDifferentiable neural computerTransformer Vision transformer (ViT)Recurrent neural network (RNN)Long short-term memory (LSTM)Gated recurrent unit (GRU)Echo state networkMultilayer perceptron (MLP)Convolutional neural network (CNN)Residual neural network (RNN)Highway networkMambaAutoencoderVariational autoencoder (VAE)Generative adversarial network (GAN)Graph neural network (GNN)

Political	
AI Cold WarAI in governmentAI safety (Alignment)AI takeoverElectionsEthics of AIEU AI ActNationalismPrecautionary principleRegulation of AI USVirtual politicianPropagandaOpposition to AI data centers

Social
and economic	
AI boomAI bubbleAI data centerAI effectAI infrastructureAI literacyAI slopAI winterAnthropomorphismArms raceCompetitionEnvironmental impactExplainable AIGenerative engine optimizationIn architectureIn educationIn fictionIn healthcare Chatbot psychosisIn marketingIn video gamesIn visual artMilitary applications AI warfareWorkplace impact


 Category
vte
Large language models (LLMs)


List of LLMsAI CompaniesBenchmarksList of chatbotsFoundation modelGenerative AI

Concepts	
Language modelNLPNLGComputational linguisticsFoundation modelSmall language modelReasoning modelGenerative pre-trained transformerTransformer AttentionKV cacheContext windowTokenizationWord embeddingParameterHyperparameterAutoregressionMixture of experts (MoE)InferenceModel compression Knowledge distillationSpeculative decodingPagedAttentionNeural scaling lawMultimodalityOpen weights

Training, prompting,
and alignment	
Self-supervised learningSupervised learningFine-tuning Instruction tuningRLHFConstitutional AIAI alignmentAI safetyMechanistic interpretabilityPrompt engineering In-context learningChain-of-thought promptingRAGPrompt injectionAdversarial machine learningHallucinationStochastic parrotGlitch tokenGenerative engine optimization

Models	
ApertusBERTBLOOMChinchillaClaudeDBRXDeepSeek-LLMGemini GemmaGloVeGLMGPTGPT-JPanGuGraniteHyInklingJaisLaMDALaguna SLlamaMiMoMinervaMistral and MixtralMuse Spark Muse GlimmerNemotronPaLMPhiQwenSeq2seqT5VicunaWord2vecXLNet

Chatbots and assistants	
Amazon QChatGPTCharacter.aiClaude Claude CodeDeepSeekDoubaoErnie BotGeminiGrokKimi Kimi CodeLumoMicrosoft CopilotMeta AIPerplexity AISparrowYou.com

Agents, coding,
and applications	
AI agentIntelligent agentAutoGPTCrewAILangChainManusModel Context ProtocolAgent2AgentOpenAI CodexVibe codingCode generationQuestion answeringMachine translationText summarizationChatbotVirtual assistant

Software	
PyTorchTensorFlowHugging Facellama.cppLM StudioOllamaSGLangTensorRT-LLMvLLMONNXOpenVINOVector databaseChromaDBDeep learning softwareOpen-source AI software

Hardware and infrastructure	
AI data centerCUDAGPUHigh Bandwidth MemoryNeural processing unit TPU

Benchmarks, evaluation,
and detection	
Language model benchmarkMMLUHumanity's Last ExamLMArenaLLM-as-a-JudgePerplexity metricGPTZeroArtificial intelligence content detectionUndetectable.ai

Datasets and data	
Data setText corpusCommon CrawlThe PileWeb scrapingSynthetic dataTraining, validation, and test data sets

Organizations	
AI21 LabsAlibabaAnthropicBaiduCohereDeepSeekEleutherAIGoogle DeepMindHugging FaceMeta AIMicrosoft AIMistral AIMiniMaxMoonshot AINvidiaOpenAIOpenRouterSarvam AIStepFunTechnology Innovation InstituteThinking Machines LabxAI

People	
Sam AltmanDario AmodeiYoshua BengioAidan GomezDemis HassabisGeoffrey HintonAndrej KarpathyYann LeCunPercy LiangLiang WenfengChristopher D. ManningArthur MenschMira MuratiAlec RadfordNoam ShazeerIlya SutskeverAshish VaswaniAndrew Ng

Social, economic,
and governance	
AI boomAI bubbleAI slopAI anthropomorphismAI arms raceChatbot psychosisCompetitionCopyrightDeaths linked to chatbotsDependency (GAID)Environmental impactRegulationEthicsExistential riskIn educationIn healthcareWorkplace impact


 Category:Large language models
Categories: Google softwareNeural network architectures2017 in artificial intelligence
This page was last edited on 24 September 2026, at 23:48 (UTC). Page was rendered with Parsoid.
Text is available under the Creative Commons Attribution-ShareAlike 4.0 License; additional terms may apply. By using this site, you agree to the Terms of Use and Privacy Policy. Wikipedia® is a registered trademark of the Wikimedia Foundation, Inc., a non-profit organization.
Privacy policy
About Wikipedia
Disclaimers
Contact Wikipedia
Legal & safety contacts
Code of Conduct
Developers
Statistics
Cookie statement
Mobile view
