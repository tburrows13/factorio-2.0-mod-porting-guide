This page is a brief summary pointing you towards some 2.0 features you may wish to implement, to make your mod fit in better with base 2.0 and Space Age.

### Factoriopedia
Items, recipes, and entities will only be grouped under the same factoriopedia entry if they have the same internal name.
Use `hidden_in_factoriopedia` to hide things.
Use `factoriopedia_description` to give things longer descriptions.
Use `factoriopedia_simulation` for things like trains that don't look as good when just placed in the world (see base mod for examples).

### Auto-recycle
If quality-mod is generating recycling recipes that you don't want, you can set `auto_recycle = false` in the recipe to tell it not to.

### Item sounds
Every item now has sounds for inventory-move, pickup, and drop. You'll want to copy sounds from vanilla items that have a similar feel to yours.

### Rocket weight
If not specified, an item's [`weight`](https://lua-api.factorio.com/latest/prototypes/ItemPrototype.html#weight) is calculated from its ingredients. Best to set a specific weight if possible. I don't know how [`ingredient_to_weight_coefficient`](https://lua-api.factorio.com/latest/prototypes/ItemPrototype.html#ingredient_to_weight_coefficient) works.

### Surface conditions
You can use [`surface_conditions`](https://lua-api.factorio.com/latest/prototypes/EntityPrototype.html#surface_conditions) to restrict your entities or recipes to specific planets.

### Remote driving
Set [`allow_remote_driving`](https://lua-api.factorio.com/latest/prototypes/VehiclePrototype.html#allow_remote_driving) to true on locomotives, tanks, and other similar vehicles to allow them to be driven remotely.

### Default keybinds
If your mod adds new keybinds, you should check that they don't conflict with any of the new default keybinds in 2.0. You can consult [this spreadsheet](https://docs.google.com/spreadsheets/d/1ukhbZXI70zDkkoJwJch16xJKHe7weQtFsfsLZNfbNlY/edit?usp=sharing) to check.

### Color hints
2.0 has a new secret/experimental colorblind assistance mode. If your mod adds items which can only be distinguished by color, you can also add a `color_hint` to them (e.g. `color_hint = { text = "U" },`). This can be enabled ingame by checking "show-color-hints" in "The rest" settings.
Consider supporting [Icon badges](https://mods.factorio.com/mod/icon-badges) if you want a fully functional solution.

### Random tint color
Some base game items have `random_tint_color` specified. This is used for items on belts to help distinguish when the belt is moving fast. See the end of [FFF 393](https://www.factorio.com/blog/post/fff-393) for more details.

### Sprite usage hints
To improve graphics performance, sprites/animations that are only used in specific contexts or on specific planets should set [`usage`](https://lua-api.factorio.com/latest/prototypes/SpritePrototype.html#usage) or [`surface`](https://lua-api.factorio.com/latest/prototypes/SpritePrototype.html#surface)
