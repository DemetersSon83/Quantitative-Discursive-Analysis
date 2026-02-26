import numpy as np
import pytest

import QDA


def test_discursive_object_builds_graph_and_spectrum_simple():
    text = "Political economy policy reform creates social welfare outcomes for communities."
    obj = QDA.discursive_object(text, noun_extractor="simple")
    assert obj.graph.number_of_nodes() > 0
    assert obj.graph.number_of_edges() > 0
    assert len(obj.spectrum) == obj.graph.number_of_nodes()


def test_resonate_identical_objects_is_one_or_close():
    text = "Climate policy adaptation resilience planning governance collaboration."
    g1 = QDA.discursive_object(text, noun_extractor="simple")
    g2 = QDA.discursive_object(text, noun_extractor="simple")
    assert QDA.resonate(g1, g2) == pytest.approx(1.0)


def test_resonate_is_symmetric():
    g1 = QDA.discursive_object("economic growth labor market reforms innovation", noun_extractor="simple")
    g2 = QDA.discursive_object("art music creative culture education", noun_extractor="simple")
    assert QDA.resonate(g1, g2) == pytest.approx(QDA.resonate(g2, g1))


def test_resonate_as_series_shape_and_values():
    objects = [
        QDA.discursive_object("energy transition policy", noun_extractor="simple"),
        QDA.discursive_object("renewable power markets", noun_extractor="simple"),
        QDA.discursive_object("healthcare delivery systems", noun_extractor="simple"),
    ]
    series = QDA.resonate_as_series(objects)
    assert len(series) == len(objects) - 1
    assert all(isinstance(v, float) for v in series.values())


def test_resonate_as_matrix_shape_diagonal_and_symmetry():
    objects = [
        QDA.discursive_object("transport planning infrastructure", noun_extractor="simple"),
        QDA.discursive_object("urban housing affordability", noun_extractor="simple"),
        QDA.discursive_object("public finance budgeting", noun_extractor="simple"),
    ]
    matrix = QDA.resonate_as_matrix(objects)
    assert matrix.shape == (3, 3)
    assert np.allclose(np.diag(matrix), 0.0)
    assert np.allclose(matrix, matrix.T)


def test_discursive_community_builds_matrix_and_graph():
    objects = [
        QDA.discursive_object("water management systems", noun_extractor="simple"),
        QDA.discursive_object("food security programs", noun_extractor="simple"),
        QDA.discursive_object("education equity policy", noun_extractor="simple"),
    ]
    community = QDA.discursive_community(objects)
    assert community.A.shape == (3, 3)
    assert community.G.number_of_nodes() == 3


def test_get_nouns_textblob_missing_corpora_error_includes_fix(monkeypatch):
    class DummyBlob:
        def __init__(self, text):
            pass

        @property
        def noun_phrases(self):
            raise QDA.MissingCorpusError("missing corpus")

    monkeypatch.setattr(QDA, "TextBlob", DummyBlob)

    with pytest.raises(QDA.QDACorpusError) as exc:
        QDA.get_nouns("sample text", method="textblob")

    assert "python -m textblob.download_corpora" in str(exc.value)
