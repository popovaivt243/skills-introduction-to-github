import unittest
import os
import sys

# Добавляем путь к проекту в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from main import app, find_most_common_word
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure:")
    print("1. main.py exists in the project")
    print("2. You're running tests from the correct directory")
    raise


class TestWordFrequencyApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        self.test_files = {
            'normal.txt': 'apple banana apple cherry banana apple',
            'empty.txt': '',
            'cyrillic.txt': 'яблоко груша яблоко вишня яблоко',
            'symbols.txt': 'hello! hello? hello, hello... hello'
        }

        for filename, content in self.test_files.items():
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)

    def tearDown(self):
        for filename in self.test_files.keys():
            if os.path.exists(filename):
                os.remove(filename)

    def test_english_words(self):
        """Test English words processing"""
        with open('normal.txt', 'rb') as f:
            response = self.app.post(
                '/',
                data={'file': f},
                content_type='multipart/form-data'
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'apple', response.data)
            self.assertIn(b'3', response.data)

    def test_cyrillic_words(self):
        """Test Russian words processing"""
        with open('cyrillic.txt', 'rb') as f:
            response = self.app.post(
                '/',
                data={'file': f},
                content_type='multipart/form-data'
            )
            self.assertEqual(response.status_code, 200)
            # Проверяем русский текст через decode
            response_text = response.data.decode('utf-8')
            self.assertIn('яблоко', response_text)
            self.assertIn('3', response_text)

    def test_empty_file(self):
        """Test empty file handling"""
        with open('empty.txt', 'rb') as f:
            response = self.app.post(
                '/',
                data={'file': f},
                content_type='multipart/form-data'
            )
            # Проверяем русский текст через decode
            response_text = response.data.decode('utf-8')
            self.assertIn('Ошибка обработки файла', response_text)


if __name__ == '__main__':
    unittest.main()