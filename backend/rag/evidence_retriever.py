import wikipedia


def search_wikipedia(query):

    results = []

    try:

        search_results = wikipedia.search(query)

        for title in search_results[:3]:

            try:

                page = wikipedia.page(title)
                summary = page.summary[:800]
                results.append(summary)

            except:
                continue

    except:
        pass

    return results


def search_evidence(query):

    evidence = []

    # Source 1 — Wikipedia
    wiki_results = search_wikipedia(query)
    evidence.extend(wiki_results)

    return evidence