import pandas as pd
from django.core.management.base import BaseCommand
from car_selectors.models import Make, Model, CarType

class Command(BaseCommand):
    help = 'Import car data from Excel'

    def handle(self, *args, **kwargs):
        df = pd.read_excel('cars.xlsx', engine='openpyxl')

        for index, row in df.iterrows():
            make_data = row['Make']

            start_paren_index = make_data.find('(')
            region = ""
            if start_paren_index != -1:
                end_paren_index = make_data.find(')', start_paren_index)
                if end_paren_index != -1:
                    region = make_data[start_paren_index + 1:end_paren_index].strip()
                    name = make_data[:start_paren_index].strip()
                else:
                    name = make_data.strip()
            else:
                name = make_data.strip()

            region = region.replace(" ", "")

            if region == "":
                region = None

            make, _ = Make.objects.get_or_create(name=name, region=region)

            model, _ = Model.objects.get_or_create(name=row['Model'], make=make)

            car_type_str = row['Type']

            end_paren_index = car_type_str.rfind(')')
            start_paren_index = car_type_str.rfind('(', 0, end_paren_index)

            if start_paren_index != -1 and end_paren_index != -1:
                years_str = car_type_str[start_paren_index + 1:end_paren_index].strip()
                years = years_str.split('-')
                
                start_year = int(years[0].strip())
                
                end_year = int(years[1].strip()) if len(years) > 1 and years[1].strip() else None
            else:
                start_year = None
                end_year = None

            name = car_type_str[:start_paren_index].strip()

            CarType.objects.get_or_create(
                name=name,
                model=model,
                start_year=start_year,
                end_year=end_year
            )

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
