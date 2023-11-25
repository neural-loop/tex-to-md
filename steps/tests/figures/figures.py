import unittest
import os

from steps.tex_figures import process_figures_in_file

class TestProcessFigures(unittest.TestCase):
    def setUp(self):
        # Set up any necessary data or state
        self.input_path = 'steps/tests/figures/tests'
        self.expected_output_path = 'steps/tests/figures/pass_condition'

    def tearDown(self):
        # Clean up any changes made in setUp or tests
        pass

    def test_process_figures(self):
        # Check the output
        for filename in os.listdir(self.input_path):
            if filename.endswith(".tex"):
                with open(os.path.join(self.input_path, filename), 'r') as f:
                    data = f.read()
                    # Call the function with the test data
                    actual_content = process_figures_in_file(data)
                with open(os.path.join(self.expected_output_path, filename), 'r') as f:
                    expected_content = f.read()


                self.maxDiff = None
                self.assertEqual(actual_content, expected_content)

if __name__ == '__main__':
    unittest.main()