from django.test import TestCase
from django.urls import reverse

from .models import Calculation
from .objects import GRAVITATIONAL_OBJECTS
from .utils import calculate_gravitational, calculate_relativistic


class UtilityTests(TestCase):
    def test_calculate_relativistic_returns_gamma_and_dilated_time(self):
        gamma, dilated = calculate_relativistic(0.5, 10)

        self.assertAlmostEqual(gamma, 1.1547005383792517)
        self.assertAlmostEqual(dilated, 11.547005383792516)

    def test_calculate_gravitational_returns_scaled_time(self):
        self.assertEqual(calculate_gravitational(10, 0.5), 5)


class ViewTests(TestCase):
    def test_home_page_loads_and_shows_health_route(self):
        response = self.client.get(reverse("core:home"))

        self.assertEqual(response.status_code, 200)

    def test_health_check_returns_ok(self):
        response = self.client.get(reverse("core:health"))

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok"})

    def test_relativistic_post_redirect_get_flow_persists_then_clears_result(self):
        post_response = self.client.post(
            reverse("core:relativistic"),
            {"velocity": 0.5, "proper_time": 10},
        )
        self.assertEqual(post_response.status_code, 302)
        self.assertEqual(
            post_response.headers["Location"], reverse("core:relativistic")
        )

        first_get = self.client.get(reverse("core:relativistic"))
        self.assertEqual(first_get.status_code, 200)
        self.assertIsNotNone(first_get.context["result"])
        self.assertEqual(first_get.context["result"]["velocity"], 0.5)

        second_get = self.client.get(reverse("core:relativistic"))
        self.assertEqual(second_get.status_code, 200)
        self.assertIsNone(second_get.context["result"])

    def test_gravitational_post_redirect_get_flow_persists_then_clears_result(self):
        object_key = next(iter(GRAVITATIONAL_OBJECTS))
        post_response = self.client.post(
            reverse("core:gravitational"),
            {"proper_time": 10, "object_key": object_key},
        )
        self.assertEqual(post_response.status_code, 302)
        self.assertEqual(
            post_response.headers["Location"], reverse("core:gravitational")
        )

        first_get = self.client.get(reverse("core:gravitational"))
        self.assertEqual(first_get.status_code, 200)
        self.assertIsNotNone(first_get.context["result"])
        self.assertEqual(first_get.context["result"]["object_key"], object_key)

        second_get = self.client.get(reverse("core:gravitational"))
        self.assertEqual(second_get.status_code, 200)
        self.assertIsNone(second_get.context["result"])


class SaveCalculationTests(TestCase):
    def test_relativistic_result_can_be_saved_once(self):
        session = self.client.session
        session["relativistic_result"] = {
            "velocity": 0.5,
            "proper_time": 10,
            "gamma": 1.1547,
            "dilated_time": 11.547,
        }
        session.save()

        response = self.client.post(
            reverse("core:save_calculation", args=["relativistic"])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], reverse("core:relativistic"))
        self.assertEqual(Calculation.objects.count(), 1)
        self.assertEqual(Calculation.objects.first().calculation_type, "relativistic")

        second_response = self.client.post(
            reverse("core:save_calculation", args=["relativistic"])
        )
        self.assertEqual(second_response.status_code, 302)
        self.assertEqual(
            second_response.headers["Location"], reverse("core:relativistic")
        )
        self.assertEqual(Calculation.objects.count(), 1)

    def test_gravitational_result_can_be_saved_once(self):
        session = self.client.session
        session["gravitational_result"] = {
            "calculation_type": "gravitational",
            "proper_time": 10,
            "dilated_time": 7.5,
            "gravitational_factor": 0.75,
            "object_key": "earth",
            "object_name": "Earth",
        }
        session.save()

        response = self.client.post(
            reverse("core:save_calculation", args=["gravitational"])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], reverse("core:gravitational"))
        self.assertEqual(Calculation.objects.count(), 1)
        self.assertEqual(Calculation.objects.first().calculation_type, "gravitational")

    def test_save_without_result_redirects_without_creating_record(self):
        response = self.client.post(
            reverse("core:save_calculation", args=["relativistic"])
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], reverse("core:relativistic"))
        self.assertEqual(Calculation.objects.count(), 0)
