from abc import ABCMeta, abstractmethod

from hackernewslib.mixins import KidsMixin, UserMixin, ContentMixin


class Item(object, metaclass=ABCMeta):
    def __init__(self, client, id, data):
        self.client = client
        self.id = id
        self.data = data
        self.type = data.get("type")

    @classmethod
    @abstractmethod
    def parse(cls, client, item):
        pass


class Story(Item, KidsMixin, UserMixin, ContentMixin):
    def __init__(self, client, id, data, by=None, descendants=None, score=None,
                 time=None, title=None, url=None, kids=None, text=None):
        super(Story, self).__init__(
            client=client,
            id=id,
            data=data
        )

        self.username = by
        self._by = None
        self.descendants = descendants
        self.score = score
        self.time = time
        self.title = title
        self.url = url
        self._content = None
        self.kid_ids = kids
        self._kids = None
        self.text = text

    @classmethod
    def parse(cls, client, item):
        return cls(
            client=client,
            id=item["id"],
            data=item,
            by=item.get("by"),
            descendants=item.get("descendants"),
            score=item.get("score"),
            time=item.get("time"),
            title=item.get("title"),
            url=item.get("url"),
            kids=item.get("kids"),
            text=item.get("text")
        )


class Comment(Item, KidsMixin, UserMixin):
    def __init__(self, client, id, data, by=None, text=None, time=None,
                 kids=None, parent=None):
        super(Comment, self).__init__(
            client=client,
            id=id,
            data=data
        )

        self.username = by
        self._by = None
        self.text = text
        self.time = time
        self.kid_ids = kids
        self._kids = None
        self.parent_id = parent
        self._parent = None

    @classmethod
    def parse(cls, client, item):
        return cls(
            client=client,
            id=item["id"],
            data=item,
            by=item.get("by"),
            text=item.get("text"),
            time=item.get("time"),
            kids=item.get("kids"),
            parent=item.get("parent")
        )

    @property
    def parent(self):
        if self.parent_id is not None and self._parent is None:
            self._parent = self.client.item(self.parent_id)

        return self._parent


class Job(Item, UserMixin, ContentMixin):
    def __init__(self, client, id, data, by=None, score=None, text=None,
                 time=None, title=None, url=None):
        super(Job, self).__init__(
            client=client,
            id=id,
            data=data
        )

        self.username = by
        self._by = None
        self.score = score
        self.text = text
        self.time = time
        self.title = title
        self.url = url
        self._content = None

    @classmethod
    def parse(cls, client, item):
        return cls(
            client=client,
            id=item["id"],
            data=item,
            by=item.get("by"),
            score=item.get("score"),
            text=item.get("text"),
            time=item.get("time"),
            title=item.get("title"),
            url=item.get("url")
        )


class Poll(Item, KidsMixin, UserMixin):
    def __init__(self, client, id, data, by=None, descendants=None, kids=None,
                 parts=None, score=None, text=None, time=None, title=None):
        super(Poll, self).__init__(
            client=client,
            id=id,
            data=data
        )

        self.username = by
        self._by = None
        self.descendants = descendants
        self.kid_ids = kids
        self._kids = None
        self.part_ids = parts
        self._parts = None
        self.score = score
        self.text = text
        self.time = time
        self.title = title

    @classmethod
    def parse(cls, client, item):
        return cls(
            client=client,
            id=item["id"],
            data=item,
            by=item.get("by"),
            descendants=item.get("descendants"),
            kids=item.get("kids"),
            parts=item.get("parts"),
            score=item.get("score"),
            text=item.get("text"),
            time=item.get("time"),
            title=item.get("title")
        )

    @property
    def parts(self):
        if self._parts is not None:
            for part in self._parts:
                yield part
        else:
            part_ids = self.part_ids or []
            self._parts = []

            for part in self.client.items(part_ids):
                self._parts.append(part)
                yield part


class Part(Item, UserMixin):
    fields = ["by", "poll", "score", "text", "time"]

    def __init__(self, client, id, data, by=None, poll=None, score=None,
                 text=None, time=None):
        super(Part, self).__init__(
            client=client,
            id=id,
            data=data
        )

        self.username = by
        self._by = None
        self.poll_id = poll
        self._poll = None
        self.score = score
        self.text = text
        self.time = time

    @classmethod
    def parse(cls, client, item):
        return cls(
            client=client,
            id=item["id"],
            data=item,
            by=item.get("by"),
            poll=item.get("poll"),
            score=item.get("score"),
            text=item.get("text"),
            time=item.get("time")
        )

    @property
    def poll(self):
        if self.poll_id is not None and self._poll is None:
            self._poll = self.client.item(self.poll_id)

        return self._poll


class Raw(Item):
    @classmethod
    def parse(cls, client, item):
        return cls(
            client=client,
            id=item["id"],
            data=item
        )


class User(object):
    def __init__(self, client, id, created, karma, about=None, delay=None,
                 submitted=None):
        self.client = client
        self.id = id
        self.created = created
        self.karma = karma
        self.about = about
        self.delay = delay
        self.submitted_ids = submitted
        self._submitted = None

    @property
    def submitted(self):
        if self._submitted is not None:
            for item in self._submitted:
                yield item
        else:
            submitted_ids = self.submitted_ids or []
            self._submitted = []

            for item in self.client.items(submitted_ids):
                self._submitted.append(item)
                yield item


class Content(object):
    def __init__(self, url, response):
        self.url = url
        self.status_code = response.status_code
        self.headers = dict(response.headers)
        self.content = response.content
        self.text = response.text
