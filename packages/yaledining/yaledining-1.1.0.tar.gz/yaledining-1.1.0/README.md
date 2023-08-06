# yaledining [![PyPI version](https://badge.fury.io/py/yaledining.svg)](https://badge.fury.io/py/yaledining)

> Python library for interfacing with the Yale Dining API, supporting the entire documented API plus undocumented endpoints.

[API documentation](https://developers.yale.edu/yale-dining)

## Guiding principles
This API seeks to enable Pythonic code using Yale Dining API data. For this reason, names and suboptimal data storage styles are often overridden.

For example:
- Names are put in standardized, Pythonic snake case (eg: `ISDEFAULTMEAL` becomes `is_default_meal`)
- Some clumsy naming is redone entirely (eg: locations' `ID_LOCATION` field simply is called `id` since the fact that it identifies a `Location` is implicit)
- More intuitive types are used, for example booleans over 0/1 integers
- `Location`'s `GEOLOCATION` property, while still accessible through `geolocation`, can be accessed through `latitude` and `longitude` propeties as well
- `Location` managers can be accessed as their own objects through the tuple `Location.managers`, with easier `name` and `email` properties
- Menu data from the API is split into `Meal` and `Item` objects to decrease data duplication and increase clarity
- `Meal` date and time fields use `datetime.date` and `datetime.time`

If you do **NOT** desire to use these enhancements, you may get the `raw` property of an object this wrapper returns:
```py
location = api.location('Branford')  # -> returns Location object
location.raw  # -> {'ID_LOCATION': '2', ... }
```
Doing so will get a dictionary of an object in similar format to how it's normally returned.

## Setup
First, install the module:

```sh
pip3 install yaledining
```

Then, to use these functions, you must import the module:

```py
import yaledining
```

Before using the library, you must instantiate its class, for example:

```py
api = yaledining.YaleDining()
# "api" name is just an example, this may be anything you desire
```

This API does not require authentication.

## Retrieval Functions
- `locations()`: get a list of all `Location` objects on campus
- `location(identifier, lenient_matching=True)`: get a single `Location` object represented by either a numerical location ID or a name in `str` format. `lenient_matching` can be specified to match similarly-named locations.
- `meals(location_id)`: get a list of `Meal` objects representing all current and upcoming meals listed for the `location_id` specified. It is likely preferable to use the `Location.meals` method if you already have a `Location` object; this will abstract away ID manipulation. Note that you must access the `items` property to get data on specific items. While the standard API merges repeated meal data with individual menu items and calls its model "menus," this wrapper separates data into `Meal` and `Item` objects. This means that there is no direct API request to get items, but you can simply use `meals(location_id).items` to the same effect.
- `nutrition(item_id)`: get nutrition data for a menu item. Using `Item.nutrition` is preferred if you already have an `Item` object to avoid ID manipulation.
- `traits(item_id)`: get traits data for a menu item, predominantly boolean values stating whether the item conforms to various dietary restrictions, contains allergens, etc.). Using `Item.traits` is preferred if you already have an `Item` object.
- `ingredients(item_id)`: get a list of ingredients for a menu item, each in `str` format. Using `Item.ingredients` is preferred if you already have an `Item` object.

## Special Function
- `feedback(location_id, cleanliness, service, food, email, comments, meal_period, [date])`: submit feedback to Yale Hospitality using an undocumented endpoint.

Note that it almost always cleaner to use builder syntax such as:
```py
meal = api.location('Hopper').meals[0]
item = meal.items[0]
item.nutrition.calories  # => 340
```
See more examples in `example.py`.

## Models
* `Location`: a dining location.
    * `id`
    * `location_code`
    * `name`
    * `type`
    * `capacity`
    * `percent_capacity`
    * `geolocation`
    * `latitude`
    * `longitude`
    * `closed`
    * `open`
    * `address`
    * `phone`
    * `managers`: tuple of `Manager`s.
    * `meals`: shortcut to get `Meal`s from the current location.
    * `feedback(cleanliness, service, food, email, comments, meal_period, [date])`: shortcut to submit feedback for current location.
* `Manager`: a manager for a location, stored inside `Location` objects.
    * `name`
    * `email`
* `Meal`: a single meal.
    * `id`
    * `location_id`
    * `location_code`
    * `location_name`
    * `name`
    * `code`
    * `raw_date`: string-format date formatted like "June, 18 2019 00:00:00". (Time is always `00:00:00`, actual time can be found in (`raw)`)`open_time`/`close_time` properties
    * `date`: processed `datetime.date` object for ease of manipulation.
    * `raw_open_time`: time of day when meal begins, formatted like `08:00 AM`.
    * `open_time`: `datetime.time` representation of the opening time.
    * `raw_close_time`: see `raw_open_time`
    * `close_time`: see `open_time`
    * `is_default_meal`
    * `is_menu`
    * `items`: shortcut to get menu `Item`s in this meal.
* `Item`: a single menu item.
    * `id`
    * `name`
    * `course`
    * `course_code`
    * `nutrition`: shortcut to get `Nutrition` for the item.
    * `traits`: shortcut to get `Traits` for the item.
    * `ingredients`: shortcut to get list of ingredients for the item.
* `Nutrition`: index of nutrition facts for an `Item`.
    * `item`
    * `item_id`
    * `serving_size`
    * `calories`
    * `protein`
    * `fat`
    * `saturated_fat`
    * `cholesterol`
    * `carbohydrates`
    * `sugar`
    * `dietary_fiber`
    * `vitamin_c`
    * `vitamin_a`
    * `iron`
* `Traits`: information on dietary concerns pertinent to an `Item`.
    * `item`
    * `item_id`
    * `alcohol`
    * `nuts`
    * `shellfish`
    * `peanut`
    * `dairy`
    * `eggs`
    * `vegan`
    * `pork`
    * `seafood`
    * `soy`
    * `wheat`
    * `gluten`
    * `vegetarian`
    * `gluten_free`
    * `facility_warning`: string describing any additional dietary concerns.


See `example.py` for several usage examples.

## Author
[Erik Boesen](https://github.com/ErikBoesen)

This software isn't endorsed by Yale Dining, Yale Hospitality, or Yale University.

## License
[GPL](LICENSE)
