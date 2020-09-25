# Dependencies
from flask import Flask, render_template
import pandas as pd
import lib.config as config
from sqlalchemy import *
import altair as alt

application = Flask(__name__)
application.debug = True

@application.route("/")
def main():
    alt.renderers.enable('html')
    # Set Database connection string
    engine = create_engine(f'mysql+pymysql://{config.user}:{config.password}@scriptingknurd.com/{config.db}')
    
    # Bring back random record from quote table
    data = pd.read_sql_query('select * from tblSiteContent where insert_date = (select max(insert_date) from tblSiteContent)', engine)
    
    data_filter = data['insert_date'] == data['insert_date'].max()
    current_data = data[data_filter]
    current_data = current_data[['guild','id']]
    current_data = current_data.groupby('guild').count()
    current_data = current_data.reset_index()
    current_data

    chart = alt.Chart(current_data).mark_bar().encode(
        x=alt.X('id', axis=alt.Axis(title='Post Count')),
        y=alt.Y('guild',
            sort=alt.EncodingSortField(field='id', order='descending', op='sum'),
            axis=alt.Axis(title='Source')
        ),
        color=alt.Color('guild', legend=None)
    )

    text = chart.mark_text(
        align='left',
        baseline='middle',
        dx=1  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='id'
    )

    final_chart = (chart + text).properties(width=1024).to_json()
    last_update = pd.read_sql_query('select max(insert_date) as last_update from tblSiteContent', engine)
    total_posts = data['id'].count()
    
    return render_template('index.htm', chart=final_chart, last_update=last_update['last_update'][0], total_posts=total_posts)


if __name__ == "__main__":
    application.run()


 