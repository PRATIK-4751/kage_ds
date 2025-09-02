import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

def create_visualization(df, x_col, y_col=None):
    fig, ax = plt.subplots(figsize=(6, 4))
    
    ax.set_facecolor("#000")
    fig.patch.set_facecolor("#000")
    ax.tick_params(colors="#00ff88")
    for spine in ax.spines.values():
        spine.set_color("#00ff8830")
    
    if y_col and y_col != "(None)":
        ax.scatter(df[x_col], df[y_col], color="#00ff88", alpha=0.7)
        ax.set_title(f"{x_col} vs {y_col}", color="#00ff88", fontsize=12)
        ax.set_ylabel(y_col, color="#aaa")
    else:
        ax.hist(df[x_col], bins=20, color="#00ff88", alpha=0.7)
        ax.set_title(f"Distribution of {x_col}", color="#00ff88", fontsize=12)
        ax.set_ylabel("Frequency", color="#aaa")
    
    ax.set_xlabel(x_col, color="#aaa")
    return fig

def get_data_context(df, num_cols, x_col=None):
    data_context = f"Dataset has {len(df)} rows and {len(df.columns)} columns."
    data_context += f"\nColumns: {', '.join(df.columns.tolist())}"
    data_context += f"\nNumeric columns: {', '.join(num_cols)}"
    
    if len(num_cols) > 0:
        data_context += "\nSummary statistics:"
        for col in num_cols[:3]:
            data_context += f"\n- {col}: mean={df[col].mean():.2f}, min={df[col].min():.2f}, max={df[col].max():.2f}"
    
    return data_context