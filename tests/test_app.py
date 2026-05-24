def test_get_activities_returns_all_activities(client):
    # Arrange: no extra setup needed

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Programming Class"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    updated = client.get("/activities").json()
    assert email in updated[activity_name]["participants"]


def test_signup_duplicate_participant_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_remove_participant_from_activity(client):
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants?email={email}"
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}

    updated = client.get("/activities").json()
    assert email not in updated[activity_name]["participants"]


def test_remove_missing_participant_returns_404(client):
    # Arrange
    activity_name = "Programming Class"
    email = "missing@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants?email={email}"
    )

    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]
