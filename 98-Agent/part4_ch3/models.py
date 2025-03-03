from pydantic import BaseModel, Field
class NewsletterThemeOutput(BaseModel):
    """Output model for structured theme and sub-theme generation."""
    theme: str = Field(
        description="The main newsletter theme based on the provided article titles."
    )
    sub_themes: list[str] = Field(
        description="List of sub-themes or key news itmes to investigate under the main theme, ensuring they are specific and researchable"
    )
