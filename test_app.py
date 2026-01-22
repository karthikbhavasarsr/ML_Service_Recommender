"""
Unit tests for the ML Service Recommender system.
"""

import unittest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_preprocessing import load_and_clean_data
from feature_encoding import FeatureEncoder
from ranking_engine import RankingEngine
from explanation_generator import ExplanationGenerator
from main import ServiceRecommender


class TestDataPreprocessing(unittest.TestCase):
    """Tests for data preprocessing module."""
    
    def setUp(self):
        self.data_path = Path(__file__).parent / 'data' / 'service_recommendation_data.csv'
    
    def test_load_data(self):
        """Test data loading."""
        df = load_and_clean_data(str(self.data_path))
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)
    
    def test_duplicates_removed(self):
        """Test that duplicates are removed."""
        df = load_and_clean_data(str(self.data_path))
        self.assertEqual(len(df), len(df.drop_duplicates()))
    
    def test_missing_values_handled(self):
        """Test that missing values are handled."""
        df = load_and_clean_data(str(self.data_path))
        self.assertEqual(df.isnull().sum().sum(), 0)


class TestFeatureEncoding(unittest.TestCase):
    """Tests for feature encoding module."""
    
    def setUp(self):
        self.data_path = Path(__file__).parent / 'data' / 'service_recommendation_data.csv'
        self.df = load_and_clean_data(str(self.data_path))
        self.encoder = FeatureEncoder()
    
    def test_encoder_fit(self):
        """Test encoder fitting."""
        self.encoder.fit(self.df)
        self.assertGreater(len(self.encoder.encoders), 0)
    
    def test_encoder_transform(self):
        """Test encoder transformation."""
        self.encoder.fit(self.df)
        df_encoded = self.encoder.transform(self.df)
        
        # Check that output is numeric where expected
        self.assertIsInstance(df_encoded, pd.DataFrame)
        self.assertEqual(len(df_encoded), len(self.df))
    
    def test_encoder_fit_transform(self):
        """Test fit_transform method."""
        df_encoded = self.encoder.fit_transform(self.df)
        self.assertEqual(len(df_encoded), len(self.df))


class TestRankingEngine(unittest.TestCase):
    """Tests for ranking engine module."""
    
    def setUp(self):
        self.data_path = Path(__file__).parent / 'data' / 'service_recommendation_data.csv'
        self.df = load_and_clean_data(str(self.data_path))
        self.encoder = FeatureEncoder()
        self.df_encoded = self.encoder.fit_transform(self.df)
        self.engine = RankingEngine(n_recommendations=5)
        self.engine.fit(self.df_encoded)
    
    def test_engine_fit(self):
        """Test ranking engine fitting."""
        self.assertIsNotNone(self.engine.service_features)
        self.assertIsNotNone(self.engine.service_ids)
    
    def test_rank_returns_correct_format(self):
        """Test that rank returns correct format."""
        feature_cols = [col for col in self.df_encoded.columns 
                       if col not in ['Description', 'Service_Name', 'Service_ID', 'Match_Quality']]
        user_profile = self.df_encoded[feature_cols].values[0]
        
        recommendations = self.engine.rank(user_profile)
        
        self.assertIsInstance(recommendations, list)
        self.assertLessEqual(len(recommendations), 5)
        
        # Check each recommendation has (id, score) format
        for service_id, score in recommendations:
            self.assertIsInstance(service_id, int)
            self.assertIsInstance(score, float)
    
    def test_rank_scores_normalized(self):
        """Test that similarity scores are between 0 and 1."""
        feature_cols = [col for col in self.df_encoded.columns 
                       if col not in ['Description', 'Service_Name', 'Service_ID', 'Match_Quality']]
        user_profile = self.df_encoded[feature_cols].values[0]
        
        recommendations = self.engine.rank(user_profile)
        
        for service_id, score in recommendations:
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 1)


class TestExplanationGenerator(unittest.TestCase):
    """Tests for explanation generator module."""
    
    def setUp(self):
        self.generator = ExplanationGenerator()
    
    def test_generate_explanation(self):
        """Test explanation generation."""
        service_row = pd.Series({
            'Service_Name': 'SEO Optimization',
            'Target_Business_Type': 'Tech Startup',
            'Price_Category': 'High',
            'Location_Area': 'Delhi',
            'Language_Support': 'Both',
            'Match_Quality': 'High',
            'Description': 'Advanced search engine optimization'
        })
        
        user_profile = {
            'business_type': 'Tech Startup',
            'price_category': 'High',
            'language': 'Both',
            'location': 'Delhi'
        }
        
        explanation = self.generator.generate_explanation(service_row, user_profile)
        
        self.assertIsInstance(explanation, str)
        self.assertGreater(len(explanation), 0)


class TestServiceRecommender(unittest.TestCase):
    """Integration tests for the complete recommender system."""
    
    def setUp(self):
        self.data_path = Path(__file__).parent / 'data' / 'service_recommendation_data.csv'
        self.recommender = ServiceRecommender(str(self.data_path))
    
    def test_recommender_setup(self):
        """Test recommender system setup."""
        self.recommender.setup()
        
        self.assertIsNotNone(self.recommender.df)
        self.assertIsNotNone(self.recommender.encoder)
        self.assertIsNotNone(self.recommender.ranking_engine)
        self.assertIsNotNone(self.recommender.explanation_generator)
    
    def test_recommender_gets_recommendations(self):
        """Test that recommender produces recommendations."""
        self.recommender.setup()
        
        user_profile = {
            'Target_Business_Type': 'Tech Startup',
            'Price_Category': 'High',
            'Language_Support': 'Both',
            'Location_Area': 'Delhi'
        }
        
        recommendations = self.recommender.recommend(user_profile)
        
        self.assertIsInstance(recommendations, pd.DataFrame)
        self.assertGreater(len(recommendations), 0)
        self.assertIn('Similarity_Score', recommendations.columns)
        self.assertIn('Explanation', recommendations.columns)
    
    def test_recommendations_have_explanations(self):
        """Test that all recommendations have explanations."""
        self.recommender.setup()
        
        user_profile = {
            'Target_Business_Type': 'Freelancer',
            'Price_Category': 'Medium',
            'Language_Support': 'English',
            'Location_Area': 'Remote'
        }
        
        recommendations = self.recommender.recommend(user_profile)
        
        for _, row in recommendations.iterrows():
            self.assertIsNotNone(row['Explanation'])
            self.assertGreater(len(row['Explanation']), 0)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDataPreprocessing))
    suite.addTests(loader.loadTestsFromTestCase(TestFeatureEncoding))
    suite.addTests(loader.loadTestsFromTestCase(TestRankingEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestExplanationGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestServiceRecommender))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit(run_tests())
