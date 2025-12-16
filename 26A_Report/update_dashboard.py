import pandas as pd
import os

# --- Configuration ---
MASTER_FILE = 'master_bugs.csv'
BUGS_OUTPUT = 'bugs.csv'
STATS_OUTPUT = 'dateClosevsNew.csv'

def update_dashboard():
    # Check if master file exists
    if not os.path.exists(MASTER_FILE):
        print(f"❌ Error: Could not find '{MASTER_FILE}'")
        return

    try:
        # 1. Read the Master File
        print(f"📂 Reading {MASTER_FILE}...")
        df = pd.read_csv(MASTER_FILE)

        # DEBUG: Print columns to check for typos
        print(f"   Found columns: {list(df.columns)}")
        
        # CLEANUP: Remove accidental spaces from column names
        df.columns = df.columns.str.strip()
        
        # Validate Columns
        required_cols = ['Bug Info', 'Status', 'Created Date', 'Closed Date']
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            print(f"❌ Error: Missing columns in master_bugs.csv: {missing}")
            return

        # CLEANUP: Remove spaces from Status and make lowercase for comparison
        df['Status'] = df['Status'].astype(str).str.strip().str.lower()
        
        # Ensure date columns are actual dates
        df['Created Date'] = pd.to_datetime(df['Created Date'], errors='coerce')
        df['Closed Date'] = pd.to_datetime(df['Closed Date'], errors='coerce')

        # --- PART A: Generate dateClosevsNew.csv ---
        print("📊 Generating statistics...")
        
        # Count New Issues
        new_counts = df.groupby(df['Created Date'].dt.date).size().rename('new')
        
        # Count Closed Issues
        closed_bugs = df[df['Status'] == 'C']
        closed_counts = closed_bugs.groupby(closed_bugs['Closed Date'].dt.date).size().rename('closed')
        
        # Merge
        timeline = pd.DataFrame(new_counts).join(closed_counts, how='outer').fillna(0).astype(int)
        timeline.index.name = 'date'
        timeline = timeline.reset_index().sort_values('date')
        
        timeline.to_csv(STATS_OUTPUT, index=False)
        print(f"✅ Saved {STATS_OUTPUT} (Covering {len(timeline)} days)")

        # --- PART B: Generate bugs.csv ---
        print("🐞 Generating open bugs list...")
        
        # Filter for Open bugs
        open_bugs_df = df[df['Status'] == 'O']
        open_bugs_list = open_bugs_df['Bug Info'].tolist()
        
        print(f"   Found {len(open_bugs_list)} open bugs in master file.")

        # Save to bugs.csv
        with open(BUGS_OUTPUT, 'w', encoding='utf-8') as f:
            for bug_line in open_bugs_list:
                f.write(f"{str(bug_line).strip()}\n")
                
        print(f"✅ Saved {BUGS_OUTPUT} with {len(open_bugs_list)} lines.")
        
    except Exception as e:
        print(f"❌ Critical Error: {e}")

if __name__ == "__main__":
    update_dashboard()

# import pandas as pd


# # --- Configuration ---
# MASTER_FILE = 'master_bugs.csv'
# BUGS_OUTPUT = 'bugs.csv'
# STATS_OUTPUT = 'dateClosevsNew.csv'

# def update_dashboard():
#     try:
#         # 1. Read the Master File
#         df = pd.read_csv(MASTER_FILE)
        
#         # Ensure date columns are actual dates
#         df['Created Date'] = pd.to_datetime(df['Created Date'], errors='coerce')
#         df['Closed Date'] = pd.to_datetime(df['Closed Date'], errors='coerce')

#         # --- PART A: Generate dateClosevsNew.csv ---
#         print("📊 Generating statistics...")
        
#         # Count New Issues (Group by Created Date)
#         new_counts = df.groupby(df['Created Date'].dt.date).size().rename('new')
        
#         # Count Closed Issues (Group by Closed Date, only for Closed status)
#         closed_bugs = df[df['Status'].str.lower() == 'closed']
#         closed_counts = closed_bugs.groupby(closed_bugs['Closed Date'].dt.date).size().rename('closed')
        
#         # Merge and fill missing dates with 0
#         timeline = pd.DataFrame(new_counts).join(closed_counts, how='outer').fillna(0).astype(int)
#         timeline.index.name = 'date'
#         timeline = timeline.reset_index().sort_values('date')
        
#         # Save Stats File
#         timeline.to_csv(STATS_OUTPUT, index=False)
#         print(f"✅ Saved {STATS_OUTPUT} (Covering {len(timeline)} days)")

#         # --- PART B: Generate bugs.csv ---
#         print("🐞 Generating open bugs list...")
        
#         # Filter for Open bugs only
#         open_bugs = df[df['Status'].str.lower() == 'open']['Bug Info']
        
#         # Save as a clean list (just the text lines)
#         with open(BUGS_OUTPUT, 'w', encoding='utf-8') as f:
#             for bug_line in open_bugs:
#                 # Clean up newlines just in case
#                 f.write(f"{str(bug_line).strip()}\n")
                
#         print(f"✅ Saved {BUGS_OUTPUT} ({len(open_bugs)} open bugs)")
        
#     except Exception as e:
#         print(f"❌ Error: {e}")
#         print("Make sure 'master_bugs.csv' exists and has columns: Bug Info, Status, Created Date, Closed Date")

# if __name__ == "__main__":
#     update_dashboard()