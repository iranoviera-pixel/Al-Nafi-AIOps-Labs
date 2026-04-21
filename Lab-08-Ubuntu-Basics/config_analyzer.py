import json
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

class AIConfigAnalyzer:
    def __init__(self):
        self.scaler = StandardScaler()
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.cluster_model = KMeans(n_clusters=3, random_state=42)
        
    def load_metrics(self, filename='system_metrics.json'):
        """Load metrics from file"""
        try:
            with open(filename, 'r') as f:
                metrics_data = json.load(f)
            return pd.DataFrame(metrics_data)
        except FileNotFoundError:
            print("Metrics file not found. Generating sample data...")
            return self.generate_sample_data()
    
    def generate_sample_data(self, samples=100):
        """Generate sample system metrics for demonstration"""
        np.random.seed(42)
        
        data = []
        for i in range(samples):
            # Simulate different system states
            if i < 30:  # Normal operation
                cpu_base = 20
                mem_base = 40
            elif i < 60:  # High load
                cpu_base = 70
                mem_base = 80
            else:  # Low usage
                cpu_base = 5
                mem_base = 20
            
            metrics = {
                'timestamp': f"2024-01-01T{i//4:02d}:{(i%4)*15:02d}:00",
                'cpu_percent': max(0, min(100, cpu_base + np.random.normal(0, 10))),
                'memory_percent': max(0, min(100, mem_base + np.random.normal(0, 15))),
                'disk_percent': max(0, min(100, 30 + np.random.normal(0, 5))),
                'load_avg_1min': max(0, (cpu_base/100) * 4 + np.random.normal(0, 0.5)),
                'process_count': max(50, int(100 + np.random.normal(0, 20))),
                'network_bytes_sent': max(0, int(1000000 + np.random.normal(0, 500000))),
                'network_bytes_recv': max(0, int(800000 + np.random.normal(0, 400000)))
            }
            data.append(metrics)
        
        return pd.DataFrame(data)
    
    def analyze_patterns(self, df):
        """Analyze system usage patterns using AI"""
        print("Analyzing system usage patterns...")
        
        # Select numeric columns for analysis
        numeric_cols = ['cpu_percent', 'memory_percent', 'disk_percent', 
                       'load_avg_1min', 'process_count']
        
        # Ensure all columns exist
        available_cols = [col for col in numeric_cols if col in df.columns]
        
        if not available_cols:
            print("No numeric columns available for analysis")
            return None
        
        # Prepare data
        X = df[available_cols].fillna(0)
        X_scaled = self.scaler.fit_transform(X)
        
        # Detect anomalies
        anomalies = self.anomaly_detector.fit_predict(X_scaled)
        df['anomaly'] = anomalies
        
        # Cluster analysis
        clusters = self.cluster_model.fit_predict(X_scaled)
        df['cluster'] = clusters
        
        # Generate insights
        insights = self.generate_insights(df, available_cols)
        
        return insights
    
    def generate_insights(self, df, numeric_cols):
        """Generate AI-based configuration insights"""
        insights = {
            'summary': {},
            'anomalies': {},
            'clusters': {},
            'recommendations': []
        }
        
        # Summary statistics
        insights['summary'] = {
            'total_samples': len(df),
            'avg_cpu': df['cpu_percent'].mean() if 'cpu_percent' in df.columns else 0,
            'avg_memory': df['memory_percent'].mean() if 'memory_percent' in df.columns else 0,
            'anomaly_count': len(df[df['anomaly'] == -1]) if 'anomaly' in df.columns else 0
        }
        
        # Anomaly analysis
        if 'anomaly' in df.columns:
            anomaly_data = df[df['anomaly'] == -1]
            if not anomaly_data.empty:
                insights['anomalies'] = {
                    'count': len(anomaly_data),
                    'avg_cpu_during_anomalies': anomaly_data['cpu_percent'].mean() if 'cpu_percent' in anomaly_data.columns else 0,
                    'avg_memory_during_anomalies': anomaly_data['memory_percent'].mean() if 'memory_percent' in anomaly_data.columns else 0
                }
        
        # Cluster analysis
        if 'cluster' in df.columns:
            cluster_summary = {}
            for cluster_id in df['cluster'].unique():
                cluster_data = df[df['cluster'] == cluster_id]
                cluster_summary[f'cluster_{cluster_id}'] = {
                    'size': len(cluster_data),
                    'avg_cpu': cluster_data['cpu_percent'].mean() if 'cpu_percent' in cluster_data.columns else 0,
                    'avg_memory': cluster_data['memory_percent'].mean() if 'memory_percent' in cluster_data.columns else 0
                }
            insights['clusters'] = cluster_summary
        
        # Generate recommendations
        insights['recommendations'] = self.generate_recommendations(insights)
        
        return insights
    
    def generate_recommendations(self, insights):
        """Generate AI-based configuration recommendations"""
        recommendations = []
        
        # CPU-based recommendations
        avg_cpu = insights['summary'].get('avg_cpu', 0)
        if avg_cpu > 80:
            recommendations.append({
                'category': 'CPU',
                'priority': 'HIGH',
                'recommendation': 'Consider CPU scaling or process optimization',
                'config_change': 'Increase CPU governor to performance mode'
            })
        elif avg_cpu < 20:
            recommendations.append({
                'category': 'CPU',
                'priority': 'MEDIUM',
                'recommendation': 'CPU resources are underutilized',
                'config_change': 'Switch CPU governor to powersave mode'
            })
        
        # Memory-based recommendations
        avg_memory = insights['summary'].get('avg_memory', 0)
        if avg_memory > 85:
            recommendations.append({
                'category': 'Memory',
                'priority': 'HIGH',
                'recommendation': 'Memory usage is critically high',
                'config_change': 'Increase swap space or add more RAM'
            })
        elif avg_memory < 30:
            recommendations.append({
                'category': 'Memory',
                'priority': 'LOW',
                'recommendation': 'Memory is underutilized',
                'config_change': 'Consider reducing memory allocation for VMs'
            })
        
        # Anomaly-based recommendations
        anomaly_count = insights['summary'].get('anomaly_count', 0)
        if anomaly_count > 0:
            recommendations.append({
                'category': 'Anomaly',
                'priority': 'MEDIUM',
                'recommendation': f'Detected {anomaly_count} anomalous patterns',
                'config_change': 'Review system logs and implement monitoring alerts'
            })
        
        return recommendations
    
    def visualize_analysis(self, df):
        """Create visualizations of the analysis"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # CPU and Memory usage over time
        if 'cpu_percent' in df.columns and 'memory_percent' in df.columns:
            axes[0, 0].plot(df.index, df['cpu_percent'], label='CPU %', alpha=0.7)
            axes[0, 0].plot(df.index, df['memory_percent'], label='Memory %', alpha=0.7)
            axes[0, 0].set_title('CPU and Memory Usage Over Time')
            axes[0, 0].set_xlabel('Sample Index')
            axes[0, 0].set_ylabel('Usage %')
            axes[0, 0].legend()
            axes[0, 0].grid(True)
        
        # Anomaly detection visualization
        if 'anomaly' in df.columns and 'cpu_percent' in df.columns and 'memory_percent' in df.columns:
            normal_data = df[df['anomaly'] == 1]
            anomaly_data = df[df['anomaly'] == -1]
            
            axes[0, 1].scatter(normal_data['cpu_percent'], normal_data['memory_percent'], 
                             c='blue', label='Normal', alpha=0.6)
            axes[0, 1].scatter(anomaly_data['cpu_percent'], anomaly_data['memory_percent'], 
                             c='red', label='Anomaly', alpha=0.8)
            axes[0, 1].set_title('Anomaly Detection: CPU vs Memory')
            axes[0, 1].set_xlabel('CPU %')
            axes[0, 1].set_ylabel('Memory %')
            axes[0, 1].legend()
            axes[0, 1].grid(True)
        
        # Cluster visualization
        if 'cluster' in df.columns and 'cpu_percent' in df.columns and 'memory_percent' in df.columns:
            scatter = axes[1, 0].scatter(df['cpu_percent'], df['memory_percent'], 
                                       c=df['cluster'], cmap='viridis', alpha=0.7)
            axes[1, 0].set_title('System Usage Clusters')
            axes[1, 0].set_xlabel('CPU %')
            axes[1, 0].set_ylabel('Memory %')
            plt.colorbar(scatter, ax=axes[1, 0])
            axes[1, 0].grid(True)
        
        # Usage distribution
        if 'cpu_percent' in df.columns:
            axes[1, 1].hist(df['cpu_percent'], bins=20, alpha=0.7, label='CPU %')
            if 'memory_percent' in df.columns:
                axes[1, 1].hist(df['memory_percent'], bins=20, alpha=0.7, label='Memory %')
            axes[1, 1].set_title('Usage Distribution')
            axes[1, 1].set_xlabel('Usage %')
            axes[1, 1].set_ylabel('Frequency')
            axes[1, 1].legend()
            axes[1, 1].grid(True)
        
        plt.tight_layout()
        plt.savefig('system_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()

if __name__ == "__main__":
    analyzer = AIConfigAnalyzer()
    
    # Load or generate data
    df = analyzer.load_metrics()
    print(f"Loaded {len(df)} samples for analysis")
    
    # Perform analysis
    insights = analyzer.analyze_patterns(df)
    
    if insights:
        print("\n=== AI ANALYSIS RESULTS ===")
        print(f"Total samples analyzed: {insights['summary']['total_samples']}")
        print(f"Average CPU usage: {insights['summary']['avg_cpu']:.2f}%")
        print(f"Average Memory usage: {insights['summary']['avg_memory']:.2f}%")
        print(f"Anomalies detected: {insights['summary']['anomaly_count']}")
        
        print("\n=== RECOMMENDATIONS ===")
        for i, rec in enumerate(insights['recommendations'], 1):
            print(f"{i}. [{rec['priority']}] {rec['category']}: {rec['recommendation']}")
            print(f"   Suggested config: {rec['config_change']}")
        
        # Create visualizations
        analyzer.visualize_analysis(df)
        
        # Save insights
        with open('ai_insights.json', 'w') as f:
            json.dump(insights, f, indent=2)
        print("\nInsights saved to ai_insights.json")


