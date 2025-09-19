import pandas as pd
from typing import List, Dict, Any
from insurance_api.core.config import INSURANCE_CSV_PATH

class AnalysisService:
    def __init__(self, data_path: str):
        self.df = pd.read_csv(data_path)

    def perform_aggregation(self, group_by_cols: List[str], agg_cols: List[str], agg_funcs: List[str]) -> List[Dict[str, Any]]:
        """Performs dynamic aggregation."""
        agg_dict = {col: agg_funcs for col in agg_cols}
        
        grouped_df = self.df.groupby(group_by_cols).agg(agg_dict)
        grouped_df.columns = ['_'.join(col).strip() for col in grouped_df.columns.values]
        grouped_df = grouped_df.reset_index()
        
        return grouped_df.to_dict(orient='records')

    def find_outliers(self, region: str = None) -> Dict[str, Any]:
        """Finds charge outliers based on region and smoker status."""
        df_filtered = self.df.copy()
        if region:
            df_filtered = df_filtered[df_filtered['region'] == region]

        if df_filtered.empty:
            return {"filter_region": region or "all", "outlier_count": 0, "outliers": []}
            
        q1 = df_filtered.groupby(['region', 'smoker'])['charges'].transform(lambda x: x.quantile(0.25))
        q3 = df_filtered.groupby(['region', 'smoker'])['charges'].transform(lambda x: x.quantile(0.75))
        iqr = q3 - q1
        upper_bound = q3 + (1.5 * iqr)
        
        outliers_df = df_filtered[df_filtered['charges'] > upper_bound].copy()
        
        if outliers_df.empty:
            return {"filter_region": region or "all", "outlier_count": 0, "outliers": []}
        
        outliers_df['reason'] = (
            "Charge of " + outliers_df['charges'].round(2).astype(str) + 
            " exceeds upper bound of " + upper_bound[outliers_df.index].round(2).astype(str)
        )
        
        results = outliers_df.to_dict(orient='records')
        
        return {
            "filter_region": region or "all",
            "outlier_count": len(results),
            "outliers": results
        }

# Instantiate the service with the path from config
analysis_service = AnalysisService(data_path=INSURANCE_CSV_PATH)