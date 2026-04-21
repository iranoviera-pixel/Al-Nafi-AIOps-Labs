import pandas as pd
import matplotlib.pyplot as plt

def create_tool_comparison():
    """Create a comparison matrix of AI configuration tools"""
    
    tools_data = {
        'Tool': ['Netdata', 'Ansible', 'Prometheus', 'Custom Python'],
        'AI_Capability': [8, 6, 7, 10],
        'Ease_of_Use': [9, 7, 6, 5],
        'Scalability': [8, 9, 9, 7],
        'Community_Support': [8, 10, 9, 6],
        'Cost': [10, 10, 10, 10]  # All open-source
    }
    
    df = pd.DataFrame(tools_data)
    
    # Create visualization
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create radar chart data
    categories = ['AI_Capability', 'Ease_of_Use', 'Scalability', 'Community_Support', 'Cost']
    
    for i, tool in enumerate(df['Tool']):
        values = df.iloc[i, 1:].values
        ax.plot(categories, values, marker='o', label=tool, linewidth=2)
        ax.fill(categories, values, alpha=0.1)
    
    ax.set_ylim(0, 10)
    ax.set_title('AI Configuration Tools Comparison', size=16, weight='bold')
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    ax.grid(True)
    
    plt.tight_layout()
    plt.savefig('tools_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return df

if __name__ == "__main__":
    comparison_df = create_tool_comparison()
    print("Tool Comparison Matrix:")
    print(comparison_df.to_string(index=False))


