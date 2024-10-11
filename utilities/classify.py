



def is_financial_article(article, classifier):
    categories = ["Finance", "Non-Finance"]
    content = article['content'] or article['title']
    result = classifier(content, categories)
    return result['labels'][0] == 'Finance'


def article_sentiment(article, sentiment_classifier):
    content = article.get('content') or article.get('title')
    
    if content is None:
        return None

    try:
        result = sentiment_classifier(content)
        # print(f"Raw classifier output for article '{article['title']}': {result}")

        # Extract sentiment label and confidence score
        sentiment = result[0]['label']
        confidence = result[0]['score']

        # Convert sentiment label to numerical encoding
        if sentiment == 'POSITIVE':
            return 1 * confidence 
        elif sentiment == 'NEGATIVE':
            return -1 * confidence  
        elif sentiment == 'NEUTRAL':  
            return 0
    except Exception as e:
        print(f"Error processing article '{article['title']}': {e}")
        return None