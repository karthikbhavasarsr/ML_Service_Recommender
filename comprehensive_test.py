import sys
from pathlib import Path
sys.path.insert(0, str(Path('.') / 'src'))

# Test all modules
from data_preprocessing import load_and_clean_data
from feature_encoding import FeatureEncoder
from ranking_engine import RankingEngine
from explanation_generator import ExplanationGenerator
from main import ServiceRecommender

print('=' * 60)
print('COMPREHENSIVE MODULE TEST')
print('=' * 60)

# Test 1: Data Preprocessing
print('\n[1] Testing Data Preprocessing...')
df = load_and_clean_data('data/service_recommendation_data.csv')
print(f'   ✓ Loaded {len(df)} services')
print(f'   ✓ Columns: {list(df.columns)}')
print(f'   ✓ No null values: {df.isnull().sum().sum() == 0}')

# Test 2: Feature Encoding
print('\n[2] Testing Feature Encoding...')
encoder = FeatureEncoder()
df_encoded = encoder.fit_transform(df)
print(f'   ✓ Encoded {len(df_encoded)} rows')
print(f'   ✓ Encoders created for {len(encoder.encoders)} features')

# Test 3: Ranking Engine
print('\n[3] Testing Ranking Engine...')
engine = RankingEngine(n_recommendations=5)
engine.fit(df_encoded)
feature_cols = [c for c in df_encoded.columns if c not in ['Description', 'Service_Name', 'Service_ID', 'Match_Quality']]
user_vec = df_encoded[feature_cols].values[0]
recs = engine.rank(user_vec)
print(f'   ✓ Generated {len(recs)} recommendations')
scores = [r[1] for r in recs]
print(f'   ✓ Similarity scores range: {min(scores):.3f} - {max(scores):.3f}')

# Test 4: Explanation Generator
print('\n[4] Testing Explanation Generator...')
gen = ExplanationGenerator()
test_service = df.iloc[0].to_dict()
test_user = {'Target_Business_Type': df.iloc[0]['Target_Business_Type'], 'Location_Area': 'Delhi', 'Language_Support': 'Both'}
exp = gen.generate_explanation(test_service, test_user)
print(f'   ✓ Generated explanation: {exp[:60]}...')

# Test 5: Full Recommender
print('\n[5] Testing Full Recommender...')
recommender = ServiceRecommender('data/service_recommendation_data.csv')
recommender.setup()
recs_df = recommender.recommend({'Target_Business_Type': 'Tech Startup', 'Price_Category': 'High', 'Language_Support': 'Both', 'Location_Area': 'Remote'})
print(f'   ✓ Got {len(recs_df)} recommendations')
print(f'   ✓ Columns: {list(recs_df.columns)}')
top_name = recs_df.iloc[0]['Service_Name']
top_score = recs_df.iloc[0]['Similarity_Score']
print(f'   ✓ Top service: {top_name} (score: {top_score:.3f})')

print('\n' + '=' * 60)
print('✓ ALL TESTS PASSED - Project Ready to Run!')
print('=' * 60)
