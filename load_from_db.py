import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns



def load_birds(db_name, user, password, host, port, table_name, plot_path):
    
    # Create the connection string
    connection_string = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'

    # Create a SQLAlchemy engine
    engine = create_engine(connection_string)

    # Read the data from the SQL database into a DataFrame, filtering for the bird class directly from the database to avoid loading unnecessary data
    query = f"SELECT * FROM {table_name} WHERE \"Class\" = 'bird'"
    bird_df = pd.read_sql_query(query, engine)
    
    print(f"Data loaded successfully from {db_name} database.")
    
    # Add a new column "Total number of seconds" by converting the 'Timestamp' column which has format hh:mm:ss
    bird_df['Seconds'] = bird_df['Timestamp'].apply(lambda x: sum(int(t) * 60 ** i for i, t in enumerate(reversed(x.split(':')))))

    #Important step to avoid duplicates of birds--> First we create a new df with the number of birds detected per frame
    # Group by 'Frame' to get the number of birds detected per frame
    birds_per_frame = bird_df.groupby('Frame').size().reset_index(name='Birds_Per_Frame')

    #Then we create a new merged df with the 'Seconds' column and the 'Birds_Per_Frame' column 
    # Merge the bird_df with birds_per_frame to maintain 'Seconds' information. Assuming all frames are unique
    merged_df = bird_df[['Frame', 'Seconds']].merge(birds_per_frame, on='Frame')

    # Now we group by seconds to get the maximum number of birds detected per second
    birds_per_second = merged_df.groupby('Seconds')['Birds_Per_Frame'].max().reset_index()


    plt.figure(figsize=(10, 6))
    sns.lineplot(data=birds_per_second, x='Seconds', y='Birds_Per_Frame')


    plt.title('Highest Number of Birds Detected Per Second')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Number of Birds')
    plt.grid(True)

    plt.savefig(plot_path)
    plt.show()