from unittest.mock import Mock

import pytest
from aws_lambda_powertools.event_handler.exceptions import ForbiddenError, NotFoundError

from gigs_db_service import GigsDbService


class TestGetUserById:
    def test_user_cannot_access_other_users_data(self):
        service = GigsDbService(table=Mock())

        with pytest.raises(ForbiddenError):
            service.get_user_by_id(user_id="123", requesting_user_id="456")

    def test_404_thrown_when_user_not_found(self):
        table = Mock()
        table.query.return_value = {"Count": 0, "Items": []}
        service = GigsDbService(table=table)

        with pytest.raises(NotFoundError):
            service.get_user_by_id(user_id="123", requesting_user_id="123")

    def test_user_returned_by_id(self):
        table = Mock()
        table.query.return_value = {"Count": 1, "Items": ["user"]}
        service = GigsDbService(table=table)

        assert service.get_user_by_id(user_id="123", requesting_user_id="123") == "user"


class TestGetGigsForUser:
    def test_user_cannot_access_other_users_gigs(self):
        service = GigsDbService(table=Mock())

        with pytest.raises(ForbiddenError):
            service.get_gigs_for_user(user_id="123", requesting_user_id="456")

    def test_gigs_returned_for_user(self):
        table = Mock()
        table.query.return_value = {"Count": 2, "Items": ["gig1", "gig2"]}
        service = GigsDbService(table=table)

        assert service.get_gigs_for_user(user_id="123", requesting_user_id="123") == ["gig1", "gig2"]