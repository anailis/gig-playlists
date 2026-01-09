from datetime import date
from unittest.mock import Mock

import pytest
from aws_lambda_powertools.event_handler.exceptions import ForbiddenError, NotFoundError

from gigs_db_service import GigsDbService, Gig


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


class TestGetGigById:
    def test_user_cannot_access_other_users_gig(self):
        table = Mock()
        gig = {"id": "GIG#gig123", "userId": "USER#user456"}
        table.query.return_value = {"Count": 1, "Items": [gig]}
        service = GigsDbService(table=table)

        with pytest.raises(ForbiddenError):
            service.get_gig_by_id(gig_id="gig123", requesting_user_id="unauthorized_user")

    def test_404_thrown_when_gig_not_found(self):
        table = Mock()
        table.query.return_value = {"Count": 0, "Items": []}
        service = GigsDbService(table=table)

        with pytest.raises(NotFoundError):
            service.get_gig_by_id(gig_id="gig123", requesting_user_id="user456")

    def test_gig_returned_by_id(self):
        table = Mock()
        gig = {"id": "GIG#gig123", "userId": "USER#user456"}
        table.query.return_value = {"Count": 1, "Items": [gig]}
        service = GigsDbService(table=table)

        assert service.get_gig_by_id(gig_id="gig123", requesting_user_id="user456") == gig


class TestPostGig:
    def test_user_cannot_create_gig_for_other_user(self):
        service = GigsDbService(table=Mock())
        gig = Gig(
            userId="USER#user456",
            artist="artist",
            date=date(year=2025, month=1, day=2),
            venue="venue",
            spotifyArtistId="spotify123"
        )

        with pytest.raises(ForbiddenError):
            service.post_gig(gig, requesting_user_id="unauthorized_user")

    def test_gig_created(self):
        table = Mock()
        service = GigsDbService(table=table)
        gig = Gig(
            userId="USER#user456",
            artist="artist",
            date=date(year=2025, month=1, day=2),
            venue="venue",
            spotifyArtistId="spotify123"
        )

        assert service.post_gig(gig, requesting_user_id="user456") == {
            "message": "Created gig with ID " + str(gig.id)
        }
        table.put_item.assert_called_once_with(Item={
            "id": "GIG#" + str(gig.id),
            "userId": "USER#user456",
            "date": "2025-01-02",
            "artist": "artist",
            "venue": "venue",
            "spotifyArtistId": "spotify123",
        })


class TestDeleteGig:
    def test_user_cannot_delete_other_users_gig(self):
        table = Mock()
        gig = {"id": "GIG#gig123", "userId": "USER#user456"}
        table.query.return_value = {"Count": 1, "Items": [gig]}
        service = GigsDbService(table=table)

        table.delete_item.assert_not_called()
        with pytest.raises(ForbiddenError):
            service.delete_gig(gig_id="gig123", requesting_user_id="unauthorized_user")

    def test_404_thrown_when_gig_not_found(self):
        table = Mock()
        table.query.return_value = {"Count": 0, "Items": []}
        service = GigsDbService(table=table)

        table.delete_item.assert_not_called()
        with pytest.raises(NotFoundError):
            service.delete_gig(gig_id="gig123", requesting_user_id="user456")

    def test_gig_deleted(self):
        table = Mock()
        gig = {"id": "GIG#gig123", "userId": "USER#user456"}
        table.query.return_value = {"Count": 1, "Items": [gig]}
        service = GigsDbService(table=table)

        assert service.delete_gig(gig_id="gig123", requesting_user_id="user456") == {
            "message": "Deleted gig with ID gig123"
        }
        table.delete_item.assert_called_once_with(Key={"id": "GIG#gig123", "userId": "USER#user456"})