import en_core_web_md

nlp = en_core_web_md.load()


def get_similarity(sentence1: str, sentence2: str) -> float:
    """
    Calculates the similarity between two sentences

    Args:
        sentence1: The first sentence to be compared
        sentence2: The second sentence to be compared

    Returns:
        The similarity between the two sentences
    """
    doc1 = nlp(sentence1)
    doc2 = nlp(sentence2)
    return doc1.similarity(doc2)
