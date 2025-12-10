import pandas as pd
import numpy as np

# --- Configuration ---
MASTER_FILE = 'master_bugs.csv'
BUGS_OUTPUT = 'bugs.csv'
STATS_OUTPUT = 'dateClosevsNew.csv'

def update_dashboard():
    try:
        # 1. Read the Master File
        df = pd.read_csv(MASTER_FILE)
        
        # Ensure date columns are actual dates
        df['Created Date'] = pd.to_datetime(df['Created Date'], errors='coerce')
        df['Closed Date'] = pd.to_datetime(df['Closed Date'], errors='coerce')

        # --- PART A: Generate dateClosevsNew.csv ---
        print("📊 Generating statistics...")
        
        # Count New Issues (Group by Created Date)
        new_counts = df.groupby(df['Created Date'].dt.date).size().rename('new')
        
        # Count Closed Issues (Group by Closed Date, only for Closed status)
        closed_bugs = df[df['Status'].str.lower() == 'closed']
        closed_counts = closed_bugs.groupby(closed_bugs['Closed Date'].dt.date).size().rename('closed')
        
        # Merge and fill missing dates with 0
        timeline = pd.DataFrame(new_counts).join(closed_counts, how='outer').fillna(0).astype(int)
        timeline.index.name = 'date'
        timeline = timeline.reset_index().sort_values('date')
        
        # Save Stats File
        timeline.to_csv(STATS_OUTPUT, index=False)
        print(f"✅ Saved {STATS_OUTPUT} (Covering {len(timeline)} days)")

        # --- PART B: Generate bugs.csv ---
        print("🐞 Generating open bugs list...")
        
        # Filter for Open bugs only
        open_bugs = df[df['Status'].str.lower() == 'open']['Bug Info']
        
        # Save as a clean list (just the text lines)
        with open(BUGS_OUTPUT, 'w', encoding='utf-8') as f:
            for bug_line in open_bugs:
                # Clean up newlines just in case
                f.write(f"{str(bug_line).strip()}\n")
                
        print(f"✅ Saved {BUGS_OUTPUT} ({len(open_bugs)} open bugs)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure 'master_bugs.csv' exists and has columns: Bug Info, Status, Created Date, Closed Date")

if __name__ == "__main__":
    update_dashboard()