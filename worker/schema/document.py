import datetime

from pydantic import BaseModel, Field, field_validator

from worker.helpers.data_preprocessors.strip_spaces import remove_leading_trailing_spaces


class ItemDocumentBase(BaseModel):
    feed_id: str = Field(..., description="Manual reference to the feed_id")
    title: str = Field(..., description="This is the article/item title")
    description: str = Field(..., description="An article will have a description (may be optional)")
    published_date: str = Field(default="", description="Published Date")
    item_url: str = Field(..., description="https://www.meltwater.com/slug")
    source_url: str = Field(..., description="https://www.meltwater.com")
    source_name: str = Field(..., description="Meltwater")
    image_url: str = Field(..., description="https://www.meltwater.com/image.jpeg")
    indexed_date: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
        description="Timestamp when the item was indexed"
    )

    @field_validator(
        "title",
        "description",
        "published_date",
        "item_url",
        "source_url",
        "source_name",
        "image_url",
        mode="before"
    )
    def clean_fields(cls, v):
        return_field = remove_leading_trailing_spaces(v)
        return return_field