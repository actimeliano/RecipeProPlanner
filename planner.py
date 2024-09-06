import pandas as pd
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import os

class DinnerPlanner:
    def __init__(self):
        self.dinner_plan_file = 'dinner_plan.csv'
        if os.path.exists(self.dinner_plan_file):
            self.dinner_plan = pd.read_csv(self.dinner_plan_file)
        else:
            self.dinner_plan = pd.DataFrame(columns=['date', 'recipe'])

    def save_dinner_plan(self, plan_dict):
        new_plan = pd.DataFrame(list(plan_dict.items()), columns=['date', 'recipe'])
        self.dinner_plan = pd.concat([self.dinner_plan, new_plan]).drop_duplicates(subset='date', keep='last')
        self.dinner_plan = self.dinner_plan.sort_values('date').reset_index(drop=True)
        self.dinner_plan.to_csv(self.dinner_plan_file, index=False)

    def get_dinner_plan(self):
        if os.path.exists(self.dinner_plan_file):
            return pd.read_csv(self.dinner_plan_file)
        return pd.DataFrame(columns=['date', 'recipe'])

    def export_to_calendar(self):
        cal = Calendar()
        cal.add('prodid', '-//Recipe Dinner Planner//mxm.dk//')
        cal.add('version', '2.0')

        for _, row in self.dinner_plan.iterrows():
            event = Event()
            event.add('summary', f"Dinner: {row['recipe']}")
            event_date = datetime.strptime(row['date'], "%Y-%m-%d")
            event.add('dtstart', event_date.date())
            event.add('dtend', (event_date + timedelta(days=1)).date())
            cal.add_component(event)

        return cal.to_ical()
