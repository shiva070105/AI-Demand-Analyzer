from pytrends.request import TrendReq

# Initialize PyTrends session
pytrends = TrendReq(hl='en-US', tz=330)

def get_interest_score(keyword, country):
    """
    Returns the latest interest score and direction ('up', 'down', 'stable') for a keyword.
    """
    pytrends.build_payload([keyword], geo=country)
    df = pytrends.interest_over_time()

    if df.empty or keyword not in df.columns:
        return 0, "no data"

    if len(df[keyword]) == 1:
        return int(df[keyword].iloc[-1]), "stable"
    elif len(df[keyword]) > 1:
        last = df[keyword].iloc[-1]
        prev = df[keyword].iloc[-2]
        trend = "up" if last > prev else "down"
        return int(last), trend
    else:
        return 0, "no data"


def get_related_queries(keyword, country):
    """
    Fetches top 5 related queries for a keyword from Google Trends.
    """
    pytrends.build_payload([keyword], geo=country)
    related = pytrends.related_queries()
    try:
        top = related[keyword]['top'].head(5)
        return top.to_dict('records')
    except:
        return []


def extract_keywords(query):
    """
    Naive keyword extractor (can be improved with NLP).
    Removes common stopwords.
    """
    query = query.lower()
    common_words = {"top", "best", "trending", "products", "in", "the", "and", "of"}
    return [word for word in query.split() if word not in common_words]


def auto_trend_analysis_by_search(query, country="IN"):
    """
    Takes a search query, extracts product keywords,
    and returns demand score, trend direction, and related queries.
    """
    keywords = extract_keywords(query)
    result = []

    for keyword in keywords:
        score, direction = get_interest_score(keyword, country)
        related = get_related_queries(keyword, country)
        result.append({
            "product": keyword,
            "score": score,
            "trend": direction,
            "related_queries": related
        })

    return result
