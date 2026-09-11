


import data_access.embeddings


def get_embedding(message):
    try:
        return data_access.embeddings.get_embedding(message)
    except Exception as e:
        raise ValueError(f"Error occurred while getting embedding: {str(e)}")


def get_embedding_result(embedded_vector):
    try:
        return data_access.embeddings.search_embedding(embedded_vector)
    except Exception as e:
        raise ValueError(f"Error occurred while searching embedding: {str(e)}")