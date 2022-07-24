
# TODO dodati created at i updated_at
loan = Table(
    "loan",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("book_id", ForeignKey("book.id"), primary_key=True)
)


