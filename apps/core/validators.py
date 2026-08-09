from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class MaxFileSizeValidator:
    """Ограничивает размер загружаемого файла.

    Args:
        max_mb: максимальный размер в мегабайтах.
    """

    def __init__(self, max_mb: int = 2) -> None:
        self.max_mb = max_mb

    def __call__(self, file) -> None:
        limit = self.max_mb * 1024 * 1024
        if file.size > limit:
            raise ValidationError(
                _('File is too large. Maximum size is %(max)s MB.'),
                params={'max': self.max_mb},
                code='file_too_large',
            )

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, MaxFileSizeValidator)
            and self.max_mb == other.max_mb
        )