from .utils import random_string, sha1


class Kanmi:
    SPLITER = '#'
    SALT_LENGTH = 8

    def __init__(self, salt, hashed):
        self.salt = salt
        self.hashed = hashed

    @classmethod
    def hash(cls, source, salt):
        '''
            you can subclass Kanmi and provide another hash function
        '''
        return sha1(salt + cls.SPLITER + source)

    @classmethod
    def from_str(cls, s):
        salt, hashed = s.split(cls.SPLITER)
        return cls(salt, hashed)

    def to_str(self):
        return self.salt + self.SPLITER + self.hashed

    @classmethod
    def create(cls, source, salt=None):
        if salt is None:
            salt = random_string(length=cls.SALT_LENGTH)

        hashed = cls.hash(source, salt)

        return cls(salt, hashed)

    def validate(self, other_source):
        other_hashed = self.hash(other_source, self.salt)
        return self.hashed == other_hashed
