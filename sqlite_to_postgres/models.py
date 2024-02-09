import uuid
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class FilmWork:
    title: str
    file_path: str
    creation_date: datetime
    description: str
    type: str
    created: datetime
    updated_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    rating: float = field(default=0.0)


@dataclass
class Genre:
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Person:
    full_name: str
    created_at: datetime
    updated_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class GenreFilmWork:
    film_work_id: uuid
    genre_id: uuid
    created_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class PersonFilmWork:
    film_work_id: uuid
    person_id: uuid
    role: str
    created_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)
