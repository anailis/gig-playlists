from datetime import date
from unittest.mock import Mock

import pytest
from boto3.dynamodb.conditions import Key

from gigs_db.gigs_db_service import GigsDbService, Gig, Integration, IntegrationType


class TestGetUserById:
    def test_none_returned_when_user_not_found(self):
        table = Mock()
        table.query.return_value = {"Count": 0, "Items": []}
        service = GigsDbService(table=table)

        assert service.get_user_by_id(user_id="123") is None

    def test_user_returned_by_id(self):
        table = Mock()
        table.query.return_value = {"Count": 1, "Items": ["user"]}
        service = GigsDbService(table=table)

        assert service.get_user_by_id(user_id="123") == "user"


class TestGetGigsForUser:
    def test_gigs_returned_for_user(self):
        table = Mock()
        table.query.return_value = {"Count": 2, "Items": ["gig1", "gig2"]}
        service = GigsDbService(table=table)

        assert service.get_gigs_for_user(user_id="123") == [
            "gig1",
            "gig2",
        ]


class TestGetGigById:
    def test_none_returned_when_gig_not_found(self):
        table = Mock()
        table.query.return_value = {"Count": 0, "Items": []}
        service = GigsDbService(table=table)

        assert service.get_gig_by_id(gig_id="gig123") is None

    def test_gig_returned_by_id(self):
        table = Mock()
        gig = {"id": "GIG#gig123", "userId": "USER#user456"}
        table.query.return_value = {"Count": 1, "Items": [gig]}
        service = GigsDbService(table=table)

        assert (
            service.get_gig_by_id(gig_id="gig123") == gig
        )


class TestPostGig:
    def test_gig_created(self):
        table = Mock()
        service = GigsDbService(table=table)
        gig = Gig(
            userId="USER#user456",
            artist="artist",
            date=date(year=2025, month=1, day=2),
            venue="venue",
            spotifyArtistId="spotify123",
        )

        assert service.post_gig(gig) == {
            "message": "Created gig with ID " + str(gig.id)
        }
        table.put_item.assert_called_once_with(
            Item={
                "id": "GIG#" + str(gig.id),
                "userId": "USER#user456",
                "date": "2025-01-02",
                "artist": "artist",
                "venue": "venue",
                "spotifyArtistId": "spotify123",
            }
        )


class TestDeleteGig:
    def test_gig_deleted(self):
        table = Mock()
        service = GigsDbService(table=table)

        assert service.delete_gig(gig_id="GIG#gig123", user_id="USER#user456") == {
            "message": "Deleted gig with ID GIG#gig123"
        }
        table.delete_item.assert_called_once_with(
            Key={"id": "GIG#gig123", "userId": "USER#user456"}
        )

class TestPostIntegration:
    def test_integration_created(self, mocker):
        table = Mock()
        service = GigsDbService(table=table)
        integration = Integration(
            userId="USER#user456",
            timestamp="timestamp",
            refreshToken="encrypted_refresh_token",
            type=IntegrationType.SPOTIFY,
            scope="playlist-read-private"
        )
        mocker.patch(f"{GigsDbService.__module__}.GigsDbService.get_user_by_id", return_value={"integrations": []})

        assert service.post_integration(integration) == {
            "message": "Created integration with ID " + str(integration.id)
        }
        table.put_item.assert_called_once_with(
            Item={
                "id": "INTEGRATION#" + str(integration.id),
                "userId": "USER#user456",
                "timestamp": "timestamp",
                "type": IntegrationType.SPOTIFY,
                "refreshToken": "encrypted_refresh_token",
                "scope": "playlist-read-private",
            }
        )
        table.update_item.assert_called_once_with(
            Key={
                "id": "USER#user456",
                "userId": "USER#user456",
            },
            UpdateExpression="""
                SET integrations = list_append(
                    if_not_exists(integrations, :empty_list),
                    :new_item
                )
            """,
            ExpressionAttributeValues={
                ":empty_list": [],
                ":new_item": [
                    {
                        "type": IntegrationType.SPOTIFY,
                        "id": "INTEGRATION#" + str(integration.id),
                    }
                ],
            },
        )

    def test_existing_integrations_are_not_overwritten(self, mocker):
        table = Mock()
        service = GigsDbService(table=table)
        integration = Integration(
            userId="USER#user456",
            refreshToken="encrypted_refresh_token",
            type=IntegrationType.SPOTIFY,
            scope="playlist-read-private"
        )
        mocker.patch(
            f"{GigsDbService.__module__}.GigsDbService.get_user_by_id",
            return_value={"integrations": [{"id": "INTEGRATION#existing_id", "type": "SPOTIFY"}]})

        with pytest.raises(ValueError):
            service.post_integration(integration)

class TestGetIntegrationForUser:
    def test_integration_returned_for_user(self, mocker):
        table = Mock()
        service = GigsDbService(table=table)
        mocker.patch(
            f"{GigsDbService.__module__}.GigsDbService.get_user_by_id",
            return_value={
                "integrations": [
                    {"id": "INTEGRATION#existing_id", "type": "SPOTIFY"},
                    {"id": "INTEGRATION#another_id", "type": "TIDAL"}
                ]
            }
        )
        table.query.return_value = {"Count": 1, "Items": ["integration"]}

        result = service.get_integration_for_user(IntegrationType.SPOTIFY, user_id="user456")
        assert result == "integration"
        table.query.assert_called_once_with(
            KeyConditionExpression=Key("id").eq("INTEGRATION#existing_id")
        )

    def test_value_error_thrown_if_no_integration_of_given_type(self, mocker):
        table = Mock()
        service = GigsDbService(table=table)
        mocker.patch(
            f"{GigsDbService.__module__}.GigsDbService.get_user_by_id",
            return_value={
                "integrations": [
                    {"id": "INTEGRATION#another_id", "type": "TIDAL"}
                ]
            }
        )
        table.query.return_value = {"Count": 1, "Items": ["integration"]}

        with pytest.raises(ValueError, match="User does not have an integration of type SPOTIFY"):
            service.get_integration_for_user(IntegrationType.SPOTIFY, user_id="user456")

    def test_value_error_thrown_if_user_has_multiple_integrations_of_given_type(self, mocker):
        table = Mock()
        service = GigsDbService(table=table)
        mocker.patch(
            f"{GigsDbService.__module__}.GigsDbService.get_user_by_id",
            return_value={
                "integrations": [
                    {"id": "INTEGRATION#existing_id", "type": "SPOTIFY"},
                    {"id": "INTEGRATION#another_id", "type": "SPOTIFY"}
                ]
            }
        )
        table.query.return_value = {"Count": 1, "Items": ["integration"]}

        with pytest.raises(ValueError, match="User has multiple integrations of type SPOTIFY"):
            service.get_integration_for_user(IntegrationType.SPOTIFY, user_id="user456")

    def test_value_error_thrown_if_integration_not_found_in_table(self, mocker):
        table = Mock()
        service = GigsDbService(table=table)
        mocker.patch(
            f"{GigsDbService.__module__}.GigsDbService.get_user_by_id",
            return_value={
                "integrations": [
                    {"id": "INTEGRATION#existing_id", "type": "SPOTIFY"}
                ]
            }
        )
        table.query.return_value = {"Count": 0, "Items": []}

        with pytest.raises(ValueError, match="Could not find integration INTEGRATION#existing_id"):
            service.get_integration_for_user(IntegrationType.SPOTIFY, user_id="user456")