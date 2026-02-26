# Quantitative Discursive Analysis (QDA)

(C) 2019 Mark M. Bailey, PhD

## About
Quantitative Discursive Analysis (QDA) converts bodies of text into graph objects built from noun phrases. Each noun or modifier becomes a vertex, and edges are determined by how nouns and modifiers are linked within phrases. The more central a noun is to the overall text content, the higher its centrality measure. This makes the graph representation more robust than simple keyword frequencies.

QDA compares discursive content by calculating **resonance** between two texts. Resonance is the cosine similarity of the betweenness-centrality vectors for the intersection of vertices in both texts. Values are normalized to `[0, 1]`, where `0` indicates no overlap and `1` indicates perfect overlap.

## Installation
```bash
pip install .
```

### Dependencies
- Python 3.10+
- `networkx`
- `numpy`
- `textblob`

### Important: TextBlob corpora required for default extractor
The default noun phrase extraction method (`textblob`) requires TextBlob/NLTK corpora.

```bash
python -m textblob.download_corpora
```

If corpora are unavailable, use the fallback extractor documented below.

## Quickstart

### Default extractor (`textblob`)
```python
import QDA

text_a = "This is a string of text about politics and economics."
text_b = "This is a different string of text about music and art."

g1 = QDA.discursive_object(text_a)  # noun_extractor='textblob' by default
g2 = QDA.discursive_object(text_b)

print(QDA.resonate(g1, g2))
```

### Fallback extractor (`simple`, no corpora required)
```python
import QDA

text_a = "This is a string of text about politics and economics."
text_b = "This is a different string of text about music and art."

g1 = QDA.discursive_object(text_a, noun_extractor="simple")
g2 = QDA.discursive_object(text_b, noun_extractor="simple")

print(QDA.resonate(g1, g2))
```

## API summary
- `QDA.discursive_object(text, noun_extractor="textblob")`
- `QDA.resonate(g1, g2)`
- `QDA.resonate_as_series(G_list)`
- `QDA.resonate_as_matrix(G_list)`
- `QDA.discursive_community(G_list)`

## Development
Run tests with:

```bash
pytest
```

## Notes and limitations
- Large texts may be slow because betweenness centrality is computationally expensive.
- Results depend on noun phrase extraction method (`textblob` vs `simple`).
- `simple` is a compatibility fallback and may produce different phrase quality than TextBlob.

## Changelog
- **0.1.0**
  - Added Python 3.10+ packaging support and pytest test suite.
  - Added explicit TextBlob missing-corpora error messaging and optional simple extractor.
  - Added NetworkX compatibility shim for NumPy graph conversion.
  - Improved performance of matrix resonance and graph construction helpers.
  - Added GitHub Actions CI for Python 3.10/3.11/3.12.
