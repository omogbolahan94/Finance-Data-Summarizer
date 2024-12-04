def search_documents(input_text, top_k=10):
    # Step 1: Generate embedding for the input text
    query_embedding = generate_embedding(data)

    # Step 2: Query Pinecone with the embedding
    search_results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True  # Include metadata to get document details
    )

    # Step 3: Process and return the search results
    documents = []
    for match in search_results['matches']:
        documents.append({
            "id": match['id'],
            "score": match['score'],
            "metadata": match['metadata']
        })

    return documents