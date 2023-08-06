class KidsMixin(object):
    @property
    def kids(self):
        if self._kids is not None:
            for kid in self._kids:
                yield kid
        else:
            kid_ids = self.kid_ids or []
            self._kids = []

            for kid in self.client.items(kid_ids):
                self._kids.append(kid)
                yield kid


class UserMixin(object):
    @property
    def by(self):
        if self.username is not None and self._by is None:
            self._by = self.client.user(self.username)

        return self._by


class ContentMixin(object):
    @property
    def content(self):
        if self.url is not None and self._content is None:
            self._content = self.client.download(self.url)

        return self._content
