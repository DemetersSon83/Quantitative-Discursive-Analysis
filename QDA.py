#!/usr/bin/env python
"""Quantitative Discursive Analysis (QDA)."""

from __future__ import annotations

import itertools
import re
from typing import Dict, Iterable, List, Sequence, Tuple

import networkx as nx
import numpy as np
from textblob import TextBlob
from textblob.exceptions import MissingCorpusError


_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from",
    "has", "have", "he", "her", "his", "i", "if", "in", "into", "is", "it",
    "its", "me", "my", "of", "on", "or", "our", "ours", "she", "that", "the",
    "their", "theirs", "them", "they", "this", "to", "was", "we", "were", "will",
    "with", "you", "your", "yours",
}


class QDACorpusError(RuntimeError):
    """Raised when TextBlob corpora are required but missing."""


def _clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\x00-\x7f]", r"", text)
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"\n", " ", text)
    punctuations = '!()-[]{};:"\\,<>./?@#$%^&*_~'
    text = text.strip(punctuations)
    text = text.strip()
    return text.strip("'")


def _simple_nouns(text: str) -> List[str]:
    tokens = re.findall(r"[a-zA-Z']+", _clean_text(text))
    filtered = [token for token in tokens if token not in _STOPWORDS and len(token) > 1]
    noun_phrases: List[str] = []
    for size in (2, 3):
        for i in range(0, max(0, len(filtered) - size + 1)):
            noun_phrases.append(" ".join(filtered[i : i + size]))
    return noun_phrases


# Calculate resonance between two discursive objects.
def resonate(G1: "discursive_object", G2: "discursive_object") -> float:
    G1_nodes = list(G1.spectrum.keys())
    G2_nodes = list(G2.spectrum.keys())
    G_intersect = list(set(G1_nodes) & set(G2_nodes))
    if len(G_intersect) != 0:
        G1_list = [G1.spectrum[node] for node in G_intersect]
        G2_list = [G2.spectrum[node] for node in G_intersect]
        G1_vector = np.array(G1_list)
        G2_vector = np.array(G2_list)
        G1_norm = np.linalg.norm(G1_vector)
        G2_norm = np.linalg.norm(G2_vector)
        if G1_norm * G2_norm == 0.0:
            resonance = 0.0
        else:
            dot_prod = np.dot(G1_vector, G2_vector)
            resonance = dot_prod / (G1_norm * G2_norm)
    else:
        resonance = 0.0
    return float(resonance)


# Resonate list of discursive objects
def resonate_as_series(G_list: Sequence["discursive_object"]) -> Dict[int, float]:
    resonance_series = []
    resonance_keys = list(range(len(G_list) - 1))
    for i in range(len(G_list) - 1):
        a = resonate(G_list[i], G_list[i + 1])
        resonance_series.append(a)
    resonance_series_dict = dict(zip(resonance_keys, resonance_series))
    return resonance_series_dict


def resonate_as_matrix(G_list: Sequence["discursive_object"]) -> np.ndarray:
    n = len(G_list)
    A = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            value = resonate(G_list[i], G_list[j])
            A[i, j] = value
            A[j, i] = value
    return A


# The following functions build the discursive object.
def get_nouns(text: str, method: str = "textblob") -> List[str]:
    if method == "simple":
        return _simple_nouns(text)
    if method != "textblob":
        raise ValueError("method must be 'textblob' or 'simple'")

    new_text = _clean_text(text)
    try:
        blob = TextBlob(new_text)
        nouns = blob.noun_phrases
        return list(nouns)
    except (MissingCorpusError, LookupError) as exc:
        raise QDACorpusError(
            "TextBlob/NLTK corpora are missing; noun phrase extraction with method='textblob' "
            "requires corpora data. Install it by running: python -m textblob.download_corpora"
        ) from exc


def get_edges(nouns: Iterable[str]) -> List[Tuple[str, str]]:
    phrase_edges: List[Tuple[str, str]] = []
    for phrase in nouns:
        phrase_words = phrase.split()
        phrase_edges.extend(itertools.permutations(phrase_words, 2))
    return phrase_edges


def get_nodes(edges: Iterable[Tuple[str, str]]) -> List[str]:
    return sorted({word for edge in edges for word in edge})


def build_graph(phrase_nodes: Iterable[str], phrase_edges: Iterable[Tuple[str, str]]) -> nx.MultiGraph:
    G = nx.MultiGraph()
    G.add_nodes_from(phrase_nodes)
    G.add_edges_from(phrase_edges)
    return G


def spectrum(G: nx.Graph) -> Dict[str, float]:
    centrality = nx.betweenness_centrality(G)
    return centrality


class discursive_object:
    """Builds a discursive object from a body of text."""

    def __init__(self, text: str, noun_extractor: str = "textblob") -> None:
        self.nouns = get_nouns(text, method=noun_extractor)
        edges = get_edges(self.nouns)
        nodes = get_nodes(edges)
        self.graph = build_graph(nodes, edges)
        self.spectrum = spectrum(self.graph)


class discursive_community:
    """Builds a discursive community from a list of discursive objects."""

    def __init__(self, G_list: Sequence[discursive_object]) -> None:
        self.A = resonate_as_matrix(G_list)
        from_numpy = getattr(nx, "from_numpy_array", None)
        if from_numpy is None:
            from_numpy = nx.from_numpy_matrix
        self.G = from_numpy(self.A)
        self.spectrum = nx.betweenness_centrality(self.G, weight="weight")
