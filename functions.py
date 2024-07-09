from newspaper import Article, ArticleException
from nltk.corpus import stopwords
from nltk import *


def main_function(text, stopwords_cstm, pos_dict, neg_dict):
    words = word_tokenize(text)
    num_words = len(words)


    # TASK 1: Sentimental Analysis
    positive_score, negative_score, polarity_score, subjectivity_score = getSentimentAnalysisData(stopwords_cstm, pos_dict, neg_dict, words)

    # TASK 4: COMPLEX WORD COUNT
    Complex_Word_Count, num_syll =  count_complex_words(words)

    # TASK 2: ANALYSIS OF READABILITY
    Average_Number_of_Words_Per_Sentence = round(avg_num_of_words_per_sent(text, words),5)
    percentage_of_Complex_words = round(((Complex_Word_Count/num_words)*100),2)
    Fog_Index = round((0.4*(Average_Number_of_Words_Per_Sentence + percentage_of_Complex_words)),5)

    # TASK 3: AVERAGE NUMBER OF WORDS PER SENTANCE !!!!

    # TASK 5: COUNT OF WORDS AFTER REMOVAL OF STOPWORDS AND  SPECIAL CHARACTERS
    Word_Count = round(count_after_removed_stopwords(words, stopwords),5)

    # TASK 6: SYLLABLE COUNT PER WORD
    Syllable_Count_Per_Word = round((num_syll/num_words), 5)

    # TASK 7: COUNTING THE PERSONAL PRONOUNS
    Personal_Pronouns = count_personal_pronouns(text)

    # TASK 8: AVERAGE WORD LENGTH
    Average_Word_Length = round(average_word_length(text,words),5)

    return (
    positive_score,
    negative_score,
    polarity_score,
    subjectivity_score,
    Average_Number_of_Words_Per_Sentence,
    percentage_of_Complex_words,
    Fog_Index,
    Complex_Word_Count,
    Word_Count,
    Syllable_Count_Per_Word,
    Personal_Pronouns,
    Average_Word_Length
    )


def is_directory_empty(directory):
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return None

    contents = os.listdir(directory)
    if len(contents) == 0:
        return True
    else:
        return False


def getArticleData(url):
    try:
        article = Article(url, language="en")
        article.download()
        article.parse()
        article.nlp()
        article_title = article.title
        article_text = article.text
        return article_title, article_text
    except ArticleException as e:
        print("Skipping URL:", url, "- Reason: INVALID URL")
        return None, None
    
def saveArticleData(id, article_title, article_text):
    if article_text != None and article_title != None:
        store_data_file_path = f"StoredDataFiles/{id}.txt"
        with open(store_data_file_path, 'w', encoding='utf-8') as file:
            file.write(article_title)
            file.write("\n")
            file.write(article_text)
        print("Data has been saved to", store_data_file_path)

def load_master_dict(path):
    with open(path, 'r') as file:
        return set(map(str.lower, file.read().split()))

# TASK 1: SENTIMENTAL ANALYSIS

def getSentimentAnalysisData(stopwords, pos_dict, neg_dict,words):

    cleaned_words = [word for word in words if word.lower() not in stopwords]

    # Calculate positive and negative scores
    positive_score = sum(1 for word in cleaned_words if word.lower() in pos_dict)
    negative_score = sum(1 for word in cleaned_words if word.lower() in neg_dict)

    # Calculating polarity and subjectivity scores
    total_score = positive_score + negative_score
    polarity_score = (positive_score - negative_score) / (total_score + 0.000001)
    subjectivity_score = total_score / (len(cleaned_words) + 0.000001)

    positive_score = round(positive_score,5)
    negative_score = round(negative_score,5)
    polarity_score = round(polarity_score,5)
    subjectivity_score = round(subjectivity_score,5)

    return positive_score, negative_score, polarity_score, subjectivity_score

# TASK 2 & 3 : AVERAGE NUMBER OF WORDS PER SENTANCE
def avg_num_of_words_per_sent(text, words):
    sentences = sent_tokenize(text)
    num_sentences = len(sentences)
    num_words = len(words)
    return (num_words/num_sentences)

# TASK 4: COMPLEX WORDS AND SYLLABLES

def count_complex_words(words):
    num_syll=0
    Complex_Word_Count=0
    for word in words:
        syllable_count = count_syllables(word)
        num_syll+=syllable_count
        if syllable_count > 2:
            Complex_Word_Count+=1

    return Complex_Word_Count, num_syll

# TASK 5: COUNT OF WORDS AFTER REMOVAL OF STOPWORDS AND  SPECIAL CHARACTERS
def count_after_removed_stopwords(words, stopwords):
    punctuation = ['.', ',', ';', ':', "-", "?","!"]
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.lower() not in stop_words and word.lower() not in punctuation]
    return len(filtered_words)

# TASK 6: COUNT SYLLABLES
def count_syllables(word):
    word = word.lower()
    vowels = "aeiouy"
    count = 0
    prev = False
    for char in word:
        if char in vowels:
            if not prev:
                count += 1
            prev = True
        else:
            prev = False
    
    if word.endswith("es") or word.endswith("ed"):
        count -= 1
    count = max(count, 1)
    return count

# TASK 7: COUNTING THE PERSONAL PRONOUNS
def count_personal_pronouns(text):
    pattern = r'\b(I|we|my|ours|us)\b'
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    #print("MATCHES: ",matches)
    matches = [match for match in matches if match != 'US']
    count = len(matches)
    return count

# TASK 8: AVERAGE WORD LENGTH
def average_word_length(text,words):
    num_words = len(words)
    num_char = sum(1 for char in text if char != ' ')
    return num_char/num_words


