import string
import random

from tenderplan.base import Base


class Generation(Base):
    def random(self):
        rand_eml = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))  # Рандом почты
        return rand_eml
