"""Test Home Assistant location util methods."""
# pylint: disable=too-many-public-methods
from unittest import TestCase
from unittest.mock import patch

import requests
import requests_mock

import scarlett_os.utility.location as location_util
from tests.common import load_fixture

# Paris
COORDINATES_PARIS = (48.864716, 2.349014)
# New York
COORDINATES_NEW_YORK = (40.730610, -73.935242)

# Results for the assertion (vincenty algorithm):
#      Distance [km]   Distance [miles]
# [0]  5846.39         3632.78
# [1]  5851            3635
#
# [0]: http://boulter.com/gps/distance/
# [1]: https://www.wolframalpha.com/input/?i=from+paris+to+new+york
DISTANCE_KM = 5846.39
DISTANCE_MILES = 3632.78

# FIXME: Convert to pytest
# FIXME: 5/10/2017
class TestLocationUtil(TestCase):
    """Test util location methods."""

    def test_get_distance_to_same_place(self):
        """Test getting the distance."""
        meters = location_util.distance(
            COORDINATES_PARIS[0],
            COORDINATES_PARIS[1],
            COORDINATES_PARIS[0],
            COORDINATES_PARIS[1],
        )

        assert meters == 0

    def test_get_distance(self):
        """Test getting the distance."""
        meters = location_util.distance(
            COORDINATES_PARIS[0],
            COORDINATES_PARIS[1],
            COORDINATES_NEW_YORK[0],
            COORDINATES_NEW_YORK[1],
        )

        assert meters / 1000 - DISTANCE_KM < 0.01

    def test_get_kilometers(self):
        """Test getting the distance between given coordinates in km."""
        kilometers = location_util.vincenty(COORDINATES_PARIS, COORDINATES_NEW_YORK)
        assert round(kilometers, 2) == DISTANCE_KM

    def test_get_miles(self):
        """Test getting the distance between given coordinates in miles."""
        miles = location_util.vincenty(
            COORDINATES_PARIS, COORDINATES_NEW_YORK, miles=True
        )
        assert round(miles, 2) == DISTANCE_MILES

    @patch("scarlett_os.utility.location.elevation", return_value=0)
    @patch("scarlett_os.utility.location._get_freegeoip", return_value=None)
    @patch("scarlett_os.utility.location._get_ip_api", return_value=None)
    def test_detect_location_info_both_queries_fail(
        self, mock_ipapi, mock_freegeoip, mock_elevation
    ):
        """Ensure we return None if both queries fail."""
        info = location_util.detect_location_info()
        assert info is None

    @patch(
        "scarlett_os.utility.location.requests.get",
        side_effect=requests.RequestException,
    )
    def test_freegeoip_query_raises(self, mock_get):
        """Test freegeoip query when the request to API fails."""
        info = location_util._get_freegeoip()
        assert info is None

    @patch(
        "scarlett_os.utility.location.requests.get",
        side_effect=requests.RequestException,
    )
    def test_ip_api_query_raises(self, mock_get):
        """Test ip api query when the request to API fails."""
        info = location_util._get_ip_api()
        assert info is None

    @patch(
        "scarlett_os.utility.location.requests.get",
        side_effect=requests.RequestException,
    )
    def test_elevation_query_raises(self, mock_get):
        """Test elevation when the request to API fails."""
        elevation = location_util.elevation(10, 10)
        assert elevation == 0

    @requests_mock.Mocker()
    def test_elevation_query_fails(self, mock_req):
        """Test elevation when the request to API fails."""
        mock_req.get(location_util.ELEVATION_URL, text="{}", status_code=401)
        elevation = location_util.elevation(10, 10)
        assert elevation == 0

    @requests_mock.Mocker()
    def test_elevation_query_nonjson(self, mock_req):
        """Test if elevation API returns a non JSON value."""
        mock_req.get(location_util.ELEVATION_URL, text="{ I am not JSON }")
        elevation = location_util.elevation(10, 10)
        assert elevation == 0
