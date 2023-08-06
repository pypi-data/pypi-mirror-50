import requests
import datetime
from unidecode import unidecode
from .models import *


class ConnectionError(Exception):
    """Raised when an error occurs in connecting to the API."""
    pass


class YaleDining:
    API_ROOT = 'https://www.yaledining.org/fasttrack/'
    API_VERSION = 3

    def __init__(self):
        pass

    def get(self, endpoint: str, params: dict = {}, json=True):
        """
        Make a GET request to the dining API.

        :param endpoint: path to resource desired.
        :param params: dictionary of custom params to add to request.
        """
        custom_params = {
            'version': self.API_VERSION,
        }
        custom_params.update(params)
        request = requests.get(self.API_ROOT + endpoint, params=custom_params)
        if not request.ok:
            raise ConnectionError('API request failed.')
        if json:
            data = request.json()
            # Restructure data into a list of dictionaries for easier manipulation
            data = [
                {data['COLUMNS'][index]: entry[index] for index in range(len(entry))}
                for entry in data['DATA']
            ]
            return data
        else:
            return request.text

    def locations(self):
        """
        Get all locations available from the dining API.
        """
        return [Location(raw, self) for raw in self.get('locations.cfm')]

    def _decompose(self, string: str):
        words = [unidecode(word.lower()) for word in string.split()]
        return [word for word in words if word not in ("cafe",)]

    def _lenient_equals(self, a, b):
        """
        Perform a series of decompositions on unequal location names to see if they're close enough.
        :param a: first name.
        :param b: second name.
        """
        a = self._decompose(a)
        b = self._decompose(b)
        return not set(a).isdisjoint(b)

    def location(self, identifier, lenient_matching: bool = True):
        """
        Get a single location by name or ID.
        :param identifier: numerical ID or name of location. If an integer is passed or a string that could be converted to
                           an integer, it will be assumed to be an ID. Otherwise, a location will be searched for by name.
        :param lenient_matching: if a name is provided, should close matches be tolerated as well?
        """
        if type(identifier) == str and identifier.isdigit():
            identifier = int(identifier)
        for location in self.locations():
            if type(identifier) == int:
                if location.id == identifier:
                    return location
            else:
                if location.name == identifier or lenient_matching and self._lenient_equals(location.name, identifier):
                    return location
        return None

    def meals(self, location_id: int):
        """
        Get all currently listed meals items for a specified location
        The API stores meals as a list of "menus" which each have data on one item and repeated data on a meal.
        To increase intuitiveness, we separate meal details into a Meal object, which has many Items.
        :param location_id: ID of location of which to get menus.
        """
        raw = self.get('menus.cfm', params={'location': location_id})

        # Dictionary mapping date strings to dictionaries mapping meal names to lists of items
        days = {}
        for raw_item in raw:
            date = raw_item['MENUDATE']
            meal_code = raw_item['MEALCODE']
            item = Item(raw_item, self)
            if date not in days:
                days[date] = {}
            if meal_code not in days[date]:
                days[date][meal_code] = Meal(raw_item, self)
            days[date][meal_code].items.append(item)
        meals = []
        for day in days:
            for meal in days[day]:
                meals.append(days[day][meal])
        return meals

    def nutrition(self, item_id: int):
        """
        Get nutrition data for a menu item.
        :param item_id: ID of item to get data on.
        """
        return Nutrition(self.get('menuitem-nutrition.cfm', params={'MENUITEMID': item_id})[0], self)

    def traits(self, item_id: int):
        """
        Get traits data of a menu item, for example whether it's vegetarian, whether it contains pork, nuts, etc.
        :param item_id: ID of item to get data on.
        """
        return Traits(self.get('menuitem-codes.cfm', params={'MENUITEMID': item_id})[0], self)

    def ingredients(self, item_id: int):
        """
        Get a list of ingredients of a menu item.
        :param item_id: ID of item to get data on.
        :return: list of string-format ingredient names, in descending order of prevalence.
        """
        return [raw['INGREDIENT'] for raw in self.get('menuitem-ingredients.cfm', params={'MENUITEMID': item_id})]

    def feedback(self, location_id, cleanliness, service, food, email, comments, meal_period, date=None):
        """
        Submit feedback to Yale Hospitality through an undocumented endpoint.
        :param location_id: ID of location on which you're giving feedback.
        :param cleanliness: 1-5 score of location cleanliness.
        :param service: 1-5 score of service quality.
        :param food: 1-5 score of food quality.
        :param email: your email.
        :param comments: further details.
        :param meal_period: meal you're giving feedback for—"Breakfast", "Brunch", "Lunch", or "Dinner".
        :param date: MM/DD/YYYY date, or datetime object, for which you want to submit data. Defaults to current day.
        :return: whether request was successful.
        """
        if date is None:
            date = datetime.date.today()
        if type(date) != str:
            date = date.strftime('%m/%d/%Y')
        raw = self.get('location-feedback-process.cfm', params={'Id_Location': location_id,
                                                                'Cleanliness': cleanliness,
                                                                'Service': service,
                                                                'Food': food,
                                                                'DateOfFeedback': date,
                                                                'MealPeriod': meal_period,
                                                                'EmailFrom': email,
                                                                'Comments': comments}, json=False)
        return raw == str(1)
