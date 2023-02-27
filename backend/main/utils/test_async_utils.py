from django.core.exceptions import SynchronousOnlyOperation
from django.test import TestCase

from main import testing_utils
from main.models import Crush
from main.utils.async_utils import get_model_prop


class GetModelPropTest(TestCase):
    async def test_can_get_lazy_loaded_relation_on_async_context(self):
        await testing_utils.create_user_and_their_crush_async("user", "crush")
        crush = await Crush.objects.afirst()
        with self.assertRaises(SynchronousOnlyOperation):
            _ = crush.crusher
        self.assertIsNotNone(await get_model_prop(crush, 'crusher'))
