import wikipedia


def search_wikipedia(query):

    results = []

    try:

        search_results = wikipedia.search(query)

        for title in search_results[:3]:

            try:

                page = wikipedia.page(title)

                results.append(page.summary[:500])

            except:
                continue

    except:
        pass

    return results