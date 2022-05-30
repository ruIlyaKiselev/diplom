class TfIdfVectorizer:

    @staticmethod
    def vectorize_corpus_tokenized_sentence(
            current_tokenized_sentence,
            unique_words,
            idf_map
    ):
        current_vectorized_sentence_accumulator = []
        for current_unique_word in unique_words.tokens:
            if current_unique_word in current_tokenized_sentence.tokens:
                current_token_index = current_tokenized_sentence.tokens.index(current_unique_word)
                current_token = current_tokenized_sentence.tokens[current_token_index]
                tf = (current_token.count / current_tokenized_sentence.words_count)
                current_vectorized_sentence_accumulator.append(tf * idf_map[current_token.lemma])
            else:
                current_vectorized_sentence_accumulator.append(0)

        return current_vectorized_sentence_accumulator

    @staticmethod
    def vectorize_input_tokenized_sentence(
            current_tokenized_sentence,
            unique_words,
            idf_map,
            word_appear_map
    ):
        current_vectorized_sentence_accumulator = []
        for current_unique_word in unique_words.tokens:
            if current_unique_word in current_tokenized_sentence.tokens:
                current_token_index = current_tokenized_sentence.tokens.index(current_unique_word)
                current_token = current_tokenized_sentence.tokens[current_token_index]
                tf = (current_token.count / word_appear_map[current_token.lemma])
                current_vectorized_sentence_accumulator.append(tf * idf_map[current_token.lemma])
            else:
                current_vectorized_sentence_accumulator.append(0)

        return current_vectorized_sentence_accumulator
    