def test_home_page_returns_200(client):
    """Test 1: Verify the home page loads with HTTP 200."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"JalaRaksha" in response.data
    assert b"Report Damage / Wastage" in response.data
    assert b"Track Report Status" in response.data
    assert b"Cyclone Arnab" in response.data


def test_awareness_page_returns_200(client):
    """Test 2: Verify the awareness page loads with HTTP 200."""
    response = client.get('/awareness')
    assert response.status_code == 200
    assert b"Water Conservation in Everyday Life" in response.data
    assert b"At Home" in response.data
    assert b"At School and College" in response.data
    assert b"In the Community" in response.data
    assert b"Climate Resilience: Surviving Droughts & Floods" in response.data


def test_404_error_page(client):
    """Verify clean 404 handler for nonexistent routes."""
    response = client.get('/nonexistent-page-url')
    assert response.status_code == 404
    assert b"404" in response.data
    assert b"Page Not Found" in response.data
