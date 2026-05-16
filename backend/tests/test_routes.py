def test_generate_and_list_routes(client, auth_headers):
    create_response = client.post(
        "/api/routes/generate",
        headers=auth_headers,
        json={
            "start_label": "CMU Main Gate",
            "target_distance_km": 5.0,
            "route_type": "loop",
            "environment": "park",
        },
    )
    assert create_response.status_code == 201
    assert create_response.json()["safety_level"] == "high"
    assert create_response.json()["center_lat"] > 0
    assert "lat" in create_response.json()["path_json"]

    list_response = client.get("/api/routes", headers=auth_headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
