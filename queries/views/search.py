from queries.models import Query, Topic


class Link:
    def __init__(self, text, link):
        self.text = text
        self.link = link


# if a number, id search
# sorted by most ran in the past
def execute(request, term):
    topics = Topic.objects.filter(string__contains=term)
    queries = Query.objects.filter(string__contains=term)
