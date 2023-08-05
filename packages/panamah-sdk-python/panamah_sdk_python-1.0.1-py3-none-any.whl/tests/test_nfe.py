import os
from unittest import main, mock, TestCase
from panamah_sdk.nfe import Nfe


class TestNfe(TestCase):
    def test_parsing_file(self):
        models = Nfe.read_models_from_file(
            os.path.join(os.path.dirname(__file__),
                         'fixtures/NFe13190507128945000132650340000000111000000099.xml')
        )
        self.assertEqual(len(models), 9)

    def test_parsing_directory(self):
        models = Nfe.read_models_from_directory(
            os.path.join(os.path.dirname(__file__), 'fixtures')
        )
        self.assertEqual(len(models), 13)



if __name__ == '__main__':
    main()
